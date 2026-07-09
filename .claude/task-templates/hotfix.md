---
id: HOTFIX-XXX
category: hotfix
status: active | blocked | completed
severity: high | critical
filed: <YYYY-MM-DD HH:MM UTC>
---

<!-- No phase field. Hotfixes are unphased by definition — they skip
     ROADMAP.md entirely (see .claude/task-rules.md → "Categories"). -->

# HOTFIX-XXX: <short title — describe what's broken in the live state>

> Hotfix-category task. **Something operative is broken or
> imminently failing. This task ships ASAP.** Filed straight to
> `tasks/active/` — no backlog stop, no phase placement, not in
> `ROADMAP.md`. Uses the `HOTFIX-NNN` id space, not `TASK-NNN`.
>
> Before starting: read `CLAUDE.md` and `.claude/task-rules.md`.
> If this is *not* genuinely urgent, re-categorize as `bug`, switch
> the id prefix to `TASK-NNN`, and route through the normal
> lifecycle.

## What's broken in the live state

One paragraph. The observable symptom AND the underlying cause
(where known). Be precise — a hotfix that says "it doesn't work"
without saying which artifact / which party / which step is harder
to ship than one with the specifics. Whatever "live state" means in
this domain — a running deployment, a filed document, a published
chapter, the operative configuration — name exactly what is wrong
and who or what is affected.

## Why this is a hotfix and not a bug

Bug or hotfix is a procedural distinction, not a technical one.
Name the urgency. Acceptable justifications (rotate to whatever
fits this domain):

- "The live service is down for all users."
- "Every new record is being corrupted as it's written."
- "A regulatory or filing deadline lands in <N hours>."
- "<Client X>'s deliverable goes out tomorrow and they're blocked."
- "A safety or compliance violation is active in the operative state."

Not justifications: "It would be nice to fix soon." "I want this in
the next release." Those are bugs, not hotfixes.

## The smallest fix

Hotfix discipline: **the smallest change that solves the problem**.
Not "the right structural answer" — that's a follow-on. Name what
the fix changes; flag anything left deliberately undone.

### What the fix changes
-
-

### What this fix does NOT do *(deliberate)*
- <follow-on improvements that should be a `bug` task afterward>

## Artifacts expected to change

List exactly. A hotfix that touches a sprawling set of artifacts is
not a hotfix; it's a rewrite under pressure.

-

## Verification

The fastest verification that proves the fix works — often a single
manual reproduction or a focused check, not the full done-gate.
Speed matters, but never skip *the* verification that proves the
observable symptom is gone. The relevant gates from
`.claude/done-gate.md` still apply before this leaves `active/` for
`completed/` — a hotfix shortens the path, it does not bypass the
gate.

1. **Reproduce the failure on the pre-fix state:** <steps>
2. **Apply the fix.**
3. **Re-run the reproduction:** must now resolve cleanly.
4. **Sanity-check adjacent work:** <the smallest check that the fix
   didn't break something nearby>

## Rollback plan *(domain-defined)*

If the hotfix itself breaks something, what reverts it? The exact
mechanism is domain-specific — define it in `.claude/done-gate.md`
or the domain extension and reference it here. Capture:

- **How to revert:** the domain's rollback mechanism for the
  affected surface (revert the change, restore the prior version,
  withdraw the filing, unpublish the revision — whatever applies).
- **What state we'll be in after rollback:** still broken on the
  original symptom, but no new regressions introduced by the hotfix.
- **Who can authorize the rollback:** the user, on this channel, or
  a named responsible party if escalation is needed.

## Post-fix follow-ups

The smallest-fix discipline leaves work undone. Capture each
follow-on as a stub `bug` task (note it here so the items get filed
*after* the hotfix ships, not during it).

- TASK-XXX (to be filed) — <follow-on>
- TASK-XXX (to be filed) — <follow-on>

## Postmortem

Every hotfix pairs with a postmortem (per `task-rules.md` →
"Postmortem rule"). Write it to
`docs/postmortems/YYYY-MM-DD-short-slug.md`, turn its action items
into tasks, and link it from the 🔥 AUDIT entry below.

## AUDIT entry *(when shipped)*

A 🔥 Hotfix entry in `tasks/AUDIT.md` when this ships, with the
domain's receipt (release tag, matter number, publication ref —
whatever this domain records) and a link to the postmortem:

```
- 🔥 **HOTFIX-XXX shipped** — <one-line description>. <domain receipt>.
  Postmortem: docs/postmortems/<file>.
```
