"""Regression tests for the Zendesk polling-fallback reconciler (AC-113)."""
from __future__ import annotations

import asyncio
from datetime import datetime, timedelta, timezone

import httpx
import pytest

from agent_cascade.connectors.zendesk.polling import ZendeskReconciler

BASE = "https://contoso.zendesk.com/api/v2"
SINCE = datetime(2026, 8, 14, 12, 0, tzinfo=timezone.utc)


def _reconciler(pages: dict[str, dict]) -> tuple[ZendeskReconciler, list[str]]:
    """Build a reconciler backed by a fake Search API.

    `pages` maps a full request URL to the JSON body to return; any URL not in
    the mapping responds 404. Also returns the list of URLs actually requested.
    """
    requested: list[str] = []

    def handler(request: httpx.Request) -> httpx.Response:
        url = str(request.url)
        requested.append(url)
        body = pages.get(url)
        if body is None:
            return httpx.Response(404, json={"error": "not found"})
        return httpx.Response(200, json=body)

    client = httpx.AsyncClient(transport=httpx.MockTransport(handler), base_url=BASE)
    return ZendeskReconciler(client), requested


def _first_page_url(account_id: str, since: datetime = SINCE) -> str:
    ts = since.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    query = f"type:ticket organization:{account_id} updated>{ts}"
    return str(httpx.URL(f"{BASE}/search.json", params={"query": query}))


def test_reconcile_emits_results_from_every_page():
    """A backlog spanning two pages must not lose the second page's signals."""
    page_two = f"{BASE}/search.json?page=2"
    pages = {
        _first_page_url("acct-a"): {
            "results": [{"id": 1, "status": "open"}],
            "next_page": page_two,
        },
        page_two: {"results": [{"id": 2, "status": "pending"}], "next_page": None},
    }
    reconciler, requested = _reconciler(pages)

    signals = asyncio.run(reconciler.reconcile("acct-a", SINCE))

    assert [s.payload["ticket_id"] for s in signals] == [1, 2]
    assert requested == [_first_page_url("acct-a"), page_two]
    assert all(s.payload["backfilled"] for s in signals)


def test_reconcile_raises_when_a_later_page_errors():
    """Every page's status is checked, not just the first."""
    pages = {
        _first_page_url("acct-a"): {
            "results": [{"id": 1, "status": "open"}],
            "next_page": f"{BASE}/search.json?page=2",
        },
    }
    reconciler, _ = _reconciler(pages)

    with pytest.raises(httpx.HTTPStatusError):
        asyncio.run(reconciler.reconcile("acct-a", SINCE))


def test_same_ticket_id_is_emitted_once_for_each_account():
    """Ticket IDs are tenant-local: account A must not suppress account B."""
    pages = {
        _first_page_url("acct-a"): {"results": [{"id": 42, "status": "open"}],
                                    "next_page": None},
        _first_page_url("acct-b"): {"results": [{"id": 42, "status": "open"}],
                                    "next_page": None},
        _first_page_url("acct-a", SINCE + timedelta(minutes=1)): {
            "results": [{"id": 42, "status": "open"}], "next_page": None,
        },
    }
    reconciler, _ = _reconciler(pages)

    async def run():
        first_a = await reconciler.reconcile("acct-a", SINCE)
        first_b = await reconciler.reconcile("acct-b", SINCE)
        repeat_a = await reconciler.reconcile("acct-a", SINCE + timedelta(minutes=1))
        return first_a, first_b, repeat_a

    first_a, first_b, repeat_a = asyncio.run(run())

    assert [(s.account_id, s.payload["ticket_id"]) for s in first_a] == [("acct-a", 42)]
    assert [(s.account_id, s.payload["ticket_id"]) for s in first_b] == [("acct-b", 42)]
    # Deduplication still holds within a single account.
    assert repeat_a == []
