"""Salesforce connector client.

Read-only adapter: surfaces renewal-date and ARR-change signals for an account.
OAuth-based; Phase 1 scope is read adapters only.

KNOWN ISSUE (AC-114): the OAuth access token refresh fails after ~60 minutes
in staging — long-running sessions lose their token and can't transparently
refresh. Workaround (in fix/salesforce-oauth-refresh): a shorter-lived token
with *proactive* refresh ahead of expiry. Until that lands this connector is
YELLOW and not deployed to staging.
"""
from __future__ import annotations

from datetime import datetime, timezone
import re

import httpx

from agent_cascade.connectors.base import Connector, CustomerSignal


_SALESFORCE_ACCOUNT_ID_RE = re.compile(r"^001[A-Za-z0-9]{12}(?:[A-Za-z0-9]{3})?$")


class SalesforceConnector(Connector):
    source = "salesforce"

    def __init__(self, instance_url: str, access_token: str) -> None:
        self._client = httpx.AsyncClient(
            base_url=instance_url,
            headers={"Authorization": f"Bearer {access_token}"},
            timeout=10.0,
        )

    async def __aenter__(self) -> SalesforceConnector:
        return self

    async def __aexit__(self, exc_type: object, exc: object, tb: object) -> None:
        await self.aclose()

    async def aclose(self) -> None:
        """Close the underlying HTTP client and release pooled connections."""
        await self._client.aclose()

    async def healthcheck(self) -> bool:
        resp = await self._client.get("/services/data/v60.0/limits")
        return resp.status_code == 200

    async def fetch_signals(self, account_id: str) -> list[CustomerSignal]:
        """Return renewal-date and ARR signals for one account."""
        if not _SALESFORCE_ACCOUNT_ID_RE.fullmatch(account_id):
            raise ValueError(
                "account_id must be a 15- or 18-character Salesforce Account ID"
            )

        soql = (
            "SELECT Id, Name, Renewal_Date__c, ARR__c "
            f"FROM Account WHERE Id = '{account_id}'"
        )
        resp = await self._client.get(
            "/services/data/v60.0/query", params={"q": soql}
        )
        resp.raise_for_status()
        records = resp.json().get("records", [])
        now = datetime.now(timezone.utc)
        signals: list[CustomerSignal] = []
        for r in records:
            if r.get("Renewal_Date__c"):
                signals.append(CustomerSignal(
                    account_id=account_id, source=self.source,
                    kind="renewal_date", observed_at=now,
                    payload={"renewal_date": r["Renewal_Date__c"]},
                ))
            if r.get("ARR__c") is not None:
                signals.append(CustomerSignal(
                    account_id=account_id, source=self.source,
                    kind="arr_change", observed_at=now,
                    payload={"arr": r["ARR__c"]},
                ))
        return signals
