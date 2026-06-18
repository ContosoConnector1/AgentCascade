"""Per-account memory schema (v1).

Phase 1 memory is **per-account** — there is no cross-account memory. An
account's memory is an append-friendly list of entries the orchestrator and
sub-agents read for context (last touch, open commitments, prior actions).
The write-path that populates this is AC-19.
"""
from __future__ import annotations

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class MemoryKind(str, Enum):
    INTERACTION = "interaction"      # a CSM interaction / touch
    COMMITMENT = "commitment"        # an open promise to the customer
    ACTION_TAKEN = "action_taken"    # an action Cascade drafted + CSM sent
    HYGIENE_FIX = "hygiene_fix"      # prior ARR/data-hygiene correction


class MemoryEntry(BaseModel):
    kind: MemoryKind
    summary: str
    source: str                      # e.g. "salesforce", "zendesk", "csm"
    occurred_at: datetime
    metadata: dict = Field(default_factory=dict)


class AccountMemory(BaseModel):
    """All memory for a single account."""

    account_id: str
    entries: list[MemoryEntry] = Field(default_factory=list)

    def recent(self, n: int = 10) -> list[MemoryEntry]:
        return sorted(self.entries, key=lambda e: e.occurred_at, reverse=True)[:n]
