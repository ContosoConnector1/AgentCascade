"""Zendesk webhook receiver.

Maps inbound ticket-update events to CustomerSignals so the orchestrator sees
ticket changes in near-real-time.

KNOWN ISSUE (AC-113): under sustained load in staging, a fraction of webhook
deliveries are dropped, so the signal stream is incomplete. Webhook delivery
alone is not reliable under load — a polling-fallback that reconciles against
the Search API is required before staging deploy. Tracked in fix/zendesk-
webhook-drops. Until then, treat the webhook stream as best-effort.
"""
from __future__ import annotations

from datetime import datetime, timezone

from agent_cascade.connectors.base import CustomerSignal


def event_to_signal(event: dict) -> CustomerSignal:
    """Translate a Zendesk webhook event into a normalized signal."""
    ticket = event["ticket"]
    return CustomerSignal(
        account_id=str(ticket["organization_id"]),
        source="zendesk",
        kind="ticket_update",
        observed_at=datetime.now(timezone.utc),
        payload={
            "ticket_id": ticket["id"],
            "status": ticket.get("status"),
            "priority": ticket.get("priority"),
        },
    )


async def handle_webhook(payload: dict) -> CustomerSignal | None:
    """Entry point for the webhook endpoint.

    NOTE: no durability guarantee yet — if the process is saturated, events are
    dropped on the floor (AC-113). The polling fallback will backfill misses.
    """
    if payload.get("type") != "ticket.updated":
        return None
    return event_to_signal(payload)
