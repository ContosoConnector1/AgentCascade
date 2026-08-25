"""Salesforce OAuth — proactive token refresh (WIP, AC-114).

The bug (AC-114): reactive refresh (refresh only after a 401) fails after
~60 min in staging — the session loses its token and can't recover cleanly.

The fix: track token expiry and refresh **proactively**, a safety margin
ahead of expiry, so a valid token is always in hand. Unblocks AC-15.
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone

import httpx

# Refresh this far ahead of expiry rather than waiting for a 401.
REFRESH_MARGIN = timedelta(minutes=5)


class ProactiveTokenRefresher:
    """Holds a Salesforce access token and refreshes before it expires."""

    def __init__(self, token_url: str, client_id: str, client_secret: str,
                 refresh_token: str) -> None:
        self._token_url = token_url
        self._client_id = client_id
        self._client_secret = client_secret
        self._refresh_token = refresh_token
        self._access_token: str | None = None
        self._expires_at: datetime | None = None

    def _expired_soon(self) -> bool:
        if self._access_token is None or self._expires_at is None:
            return True
        return datetime.now(timezone.utc) >= self._expires_at - REFRESH_MARGIN

    async def token(self) -> str:
        """Return a valid access token, refreshing proactively if needed."""
        if self._expired_soon():
            await self._refresh()
        assert self._access_token is not None
        return self._access_token

    async def _refresh(self) -> None:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.post(self._token_url, data={
                "grant_type": "refresh_token",
                "client_id": self._client_id,
                "client_secret": self._client_secret,
                "refresh_token": self._refresh_token,
            })
            resp.raise_for_status()
            body = resp.json()
        self._access_token = body["access_token"]
        # Salesforce returns issued_at/expiry; default to ~2h if absent.
        ttl = int(body.get("expires_in", 7200))
        self._expires_at = datetime.now(timezone.utc) + timedelta(seconds=ttl)
