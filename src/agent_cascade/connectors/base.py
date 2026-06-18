"""Connector interface.

A connector is a read adapter over a customer system of record (Salesforce,
Zendesk, ...). Phase 1 connectors are read-only: they surface signals that the
orchestrator and sub-agents reason over. Write-back is out of scope for Phase 1.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime

from pydantic import BaseModel


class CustomerSignal(BaseModel):
    """A normalized signal emitted by a connector."""

    account_id: str
    source: str            # "salesforce" | "zendesk"
    kind: str              # e.g. "renewal_date", "open_ticket", "arr_change"
    observed_at: datetime
    payload: dict


class Connector(ABC):
    """Base class every connector implements."""

    #: stable source name, e.g. "salesforce"
    source: str

    @abstractmethod
    async def healthcheck(self) -> bool:
        """Return True if the connector can reach its system of record."""

    @abstractmethod
    async def fetch_signals(self, account_id: str) -> list[CustomerSignal]:
        """Return the current signals for one account."""
