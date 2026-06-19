# Frontier sign-up page — UX spec (WIP)

> Status: in progress (AC-37). The page UI is being built; it's **soft-blocked on final launch copy**. This spec captures the flow + the mental model so the build isn't waiting on me, and so the copy slot is well-defined when marketing lands it.

## Who this is for

The private-preview prospect — but the people who forward them the link are **CSMs**. Before we wrote a line of this I wanted to know: what did the CSMs we talked to actually say? Consistently, two things:

1. They don't want to vouch for something they can't describe. The page has to let a CSM understand Cascade in ~10 seconds so they're comfortable forwarding it.
2. "Agent" means a dozen things. If the page over-promises autonomy, the CSM gets questions they can't answer.

So the page leads with the **one** concrete thing (renewal-nudge drafting), not the five-capability vision.

## Flow

```
Landing → "What Cascade does" (1 capability, concrete) → Sign-up form → Confirmation
```

- **Landing:** one-line value prop + a single screenshot of a drafted renewal nudge. No feature grid.
- **Form:** name, work email, company, CSM team size. Keep it to 4 fields — every extra field drops completion.
- **Confirmation:** set expectations honestly — "private preview, we'll be in touch," not "instant access."

## Friction points to design against (from research)

- **Over-claiming autonomy.** Copy must say Cascade *drafts* actions a CSM reviews — not that it acts on its own. This matched the loudest CSM concern.
- **Connector name-drops.** Don't list Salesforce + Zendesk as "available" on the page until they're actually green. Right now they're yellow/red; the page shouldn't imply day-1 parity.
- **Form length.** 4 fields max. We can enrich later.

## Copy slot (blocked)

The headline + sub-head are owned by marketing (final launch copy). The page is built to drop them in. Until then, placeholder copy is flagged in the build so it can't ship by accident.

## Open question

Have we shown this flow to even two real CSMs end-to-end? I want one more pass with a CSM on the confirmation-state wording before we call it done.
