"""Runtime configuration for Agent Cascade.

Connector enablement is feature-flagged per the Phase 1 rollback plan: each
connector + capability slice can be turned off independently.
"""
from __future__ import annotations

from pydantic import BaseModel, Field


class FeatureFlags(BaseModel):
    salesforce_connector: bool = False
    zendesk_connector: bool = False
    renewal_nudge: bool = True
    arr_hygiene: bool = False


class Settings(BaseModel):
    """Top-level settings. Loaded from env in real deployments."""

    environment: str = Field(default="staging")
    flags: FeatureFlags = Field(default_factory=FeatureFlags)
