"""Memory write-path (WIP — AC-19).

Persists CSM interactions into per-account memory using the v1 schema (AC-18).
The orchestrator/sub-agents already *read* memory via AccountMemory.recent();
this is the write half that keeps it current.

Still in progress: the store here is in-memory for staging. Durable backing
(per-account partition) lands before dogfood.
"""
from __future__ import annotations

from datetime import datetime, timezone

from agent_cascade.memory.schema import AccountMemory, MemoryEntry, MemoryKind


class MemoryWriter:
    """Append entries to per-account memory."""

    def __init__(self) -> None:
        # Staging-only store. Swapped for a durable per-account backing pre-dogfood.
        self._store: dict[str, AccountMemory] = {}

    def _account(self, account_id: str) -> AccountMemory:
        return self._store.setdefault(account_id, AccountMemory(account_id=account_id))

    def record_interaction(self, account_id: str, summary: str, source: str) -> MemoryEntry:
        entry = MemoryEntry(
            kind=MemoryKind.INTERACTION,
            summary=summary,
            source=source,
            occurred_at=datetime.now(timezone.utc),
        )
        self._account(account_id).entries.append(entry)
        return entry

    def record_action_taken(self, account_id: str, summary: str, source: str = "cascade") -> MemoryEntry:
        entry = MemoryEntry(
            kind=MemoryKind.ACTION_TAKEN,
            summary=summary,
            source=source,
            occurred_at=datetime.now(timezone.utc),
        )
        self._account(account_id).entries.append(entry)
        return entry

    def memory_for(self, account_id: str) -> AccountMemory:
        return self._account(account_id)
