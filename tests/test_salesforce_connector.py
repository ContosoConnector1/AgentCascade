"""Focused tests for the Salesforce connector."""

import asyncio

import pytest

from agent_cascade.connectors.salesforce.client import SalesforceConnector


def test_fetch_signals_rejects_malicious_account_id() -> None:
    async def run() -> None:
        connector = SalesforceConnector("https://example.my.salesforce.com", "token")
        try:
            with pytest.raises(ValueError):
                await connector.fetch_signals("001000000000000' OR Name != '")
        finally:
            await connector.aclose()

    asyncio.run(run())


def test_async_context_manager_closes_http_client() -> None:
    async def run() -> None:
        connector = SalesforceConnector("https://example.my.salesforce.com", "token")
        assert not connector._client.is_closed

        async with connector:
            assert not connector._client.is_closed

        assert connector._client.is_closed

    asyncio.run(run())
