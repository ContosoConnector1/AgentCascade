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


class ZendeskReconciler:
    """Backfills missed ticket updates via the Search API."""

    def __init__(self, client: httpx.AsyncClient) -> None:
        self._client = client
        self._seen_ids: set[int] = set()

    async def reconcile(self, account_id: str, since: datetime) -> list[CustomerSignal]:
        """Return signals for ticket updates the webhook stream may have missed."""
        ts = since.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        resp = await self._client.get(
            "/search.json",
            params={"query": f"type:ticket organization:{account_id} updated>{ts}"},
        )
        resp.raise_for_status()
        out: list[CustomerSignal] = []
        for t in resp.json().get("results", []):
            if t["id"] in self._seen_ids:
                continue
            self._seen_ids.add(t["id"])
            out.append(CustomerSignal(
                account_id=account_id,
                source="zendesk",
                kind="ticket_update",
                observed_at=datetime.now(timezone.utc),
                payload={"ticket_id": t["id"], "status": t.get("status"),
                         "backfilled": True},
            ))
        return out
