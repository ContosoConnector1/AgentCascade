"""Zendesk polling-fallback reconciliation (WIP — AC-113).

Webhook delivery alone drops events under sustained load. This reconciler
periodically queries the Search API for tickets updated since the last
checkpoint and emits signals for any the webhook stream missed — so the
connector's signal stream is complete even when deliveries are dropped.

This is the redesign decided in the Teams blocker thread; it's what moves the
Zendesk connector off RED.
"""
from __future__ import annotations

from datetime import datetime, timezone

import httpx

from agent_cascade.connectors.base import CustomerSignal

# How far back each reconciliation pass looks (overlaps to avoid gaps).
LOOKBACK_SECONDS = 900

# Safety valve: a malformed/looping `next_page` chain must not hang a pass.
MAX_PAGES = 100


class ZendeskReconciler:
    """Backfills missed ticket updates via the Search API."""

    def __init__(self, client: httpx.AsyncClient) -> None:
        self._client = client
        # Ticket IDs are tenant-local, so dedup state must be scoped per account.
        self._seen_ids: set[tuple[str, int]] = set()

    async def reconcile(self, account_id: str, since: datetime) -> list[CustomerSignal]:
        """Return signals for ticket updates the webhook stream may have missed.

        Walks the Search API's `next_page` chain so a backlog spanning more than
        one page is fully reconciled.
        """
        ts = since.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        out: list[CustomerSignal] = []

        url: str | None = "/search.json"
        params: dict[str, str] | None = {
            "query": f"type:ticket organization:{account_id} updated>{ts}"
        }
        pages = 0

        while url is not None:
            resp = await self._client.get(url, params=params)
            resp.raise_for_status()
            body = resp.json()

            for t in body.get("results", []):
                key = (account_id, t["id"])
                if key in self._seen_ids:
                    continue
                self._seen_ids.add(key)
                out.append(CustomerSignal(
                    account_id=account_id,
                    source="zendesk",
                    kind="ticket_update",
                    observed_at=datetime.now(timezone.utc),
                    payload={"ticket_id": t["id"], "status": t.get("status"),
                             "backfilled": True},
                ))

            pages += 1
            if pages >= MAX_PAGES:
                break
            # `next_page` is an absolute URL that already carries the query params.
            url = body.get("next_page")
            params = None

        return out
