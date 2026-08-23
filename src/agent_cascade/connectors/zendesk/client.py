"""Zendesk connector client.

Read-only adapter: surfaces open-ticket signals for an account. OAuth-based;
Phase 1 scope is read adapters only (no write-back).
"""
from __future__ import annotations

from datetime import datetime, timezone

import httpx

from agent_cascade.connectors.base import Connector, CustomerSignal


class ZendeskConnector(Connector):
    source = "zendesk"

    def __init__(self, subdomain: str, access_token: str) -> None:
        self._base = f"https://{subdomain}.zendesk.com/api/v2"
        self._client = httpx.AsyncClient(
            base_url=self._base,
            headers={"Authorization": f"Bearer {access_token}"},
            timeout=10.0,
        )

    async def healthcheck(self) -> bool:
        resp = await self._client.get("/tickets/count.json")
        return resp.status_code == 200

    async def fetch_signals(self, account_id: str) -> list[CustomerSignal]:
        """Return open-ticket signals for one account (by organization id)."""
        resp = await self._client.get(
            "/search.json",
            params={"query": f"type:ticket status:open organization:{account_id}"},
        )
        resp.raise_for_status()
        results = resp.json().get("results", [])
        return [
            CustomerSignal(
                account_id=account_id,
                source=self.source,
                kind="open_ticket",
                observed_at=datetime.now(timezone.utc),
                payload={
                    "ticket_id": t["id"],
                    "subject": t.get("subject"),
                    "priority": t.get("priority"),
                    "updated_at": t.get("updated_at"),
                },
            )
            for t in results
        ]
