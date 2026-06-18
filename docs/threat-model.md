# Phase 1 threat model (WIP)

> Status: in progress (AC-34). Sequenced to **follow** the architecture lock
> (AC-43 / AC-20), not precede it. In review with the Security partner.

## Scope

The Phase 1 system: M365 Copilot → orchestrator → sub-agents, read-only
Salesforce + Zendesk connectors, per-account memory.

## Trust boundaries

1. **M365 Copilot ↔ orchestrator** — inbound requests carry user/tenant context.
2. **Orchestrator ↔ connectors** — outbound, read-only, OAuth to customer systems.
3. **Orchestrator ↔ memory** — per-account read/write, account-scoped.

## Threats (STRIDE, abbreviated)

| Threat | Surface | Mitigation |
|---|---|---|
| Spoofing | Copilot → orchestrator | Validate tenant/user context per request |
| Tampering | Connector tokens | Tokens in secret store; short-lived (see AC-114 fix) |
| Info disclosure | Cross-account memory leak | Memory is **per-account**, account-scoped reads only |
| Elevation | Connector write-back | Connectors are **read-only** in Phase 1 |
| Repudiation | Drafted actions | Every action cites its source signal; human CSM in the loop |

## Open items

- Confirm secret-store rotation policy with the Security partner.
- Pen-test the connector OAuth flows once the Salesforce refresh fix lands.
