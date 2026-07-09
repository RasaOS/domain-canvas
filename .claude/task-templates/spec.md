---
id: TASK-XXX
category: spec
status: backlog
---

# TASK-XXX: <short title>

> Spec-category task — the default full work contract. Copy this file to
> `tasks/backlog/TASK-XXX-slug.md`, fill in every section, then move to
> `tasks/active/` when work begins.
>
> Before starting: read `CLAUDE.md`, `.claude/task-rules.md`, and
> `.claude/done-gate.md`. If this domain ships an extension
> (`.claude/<domain>-task-rules.md`), read it too.
>
> **Phase lives in `ROADMAP.md`, not here.** Do not declare a phase in
> this file — `tasks/ROADMAP.md` is the sole phase registry.
>
> For other categories: `stub.md` (light tracking), `bug.md` (fix broken
> behavior), `hotfix.md` (urgent fix that ships now).

## User story

As a **<role>**, I want **<capability>** so that **<outcome>**.

## Why this matters

One or two sentences. What is missing or wrong today without this? What
does it unblock? Link the relevant `CLAUDE.md` section if applicable.

## Scope

**In scope:**
-

**Out of scope (explicit):**
-

If you find yourself doing something not on the in-scope list, that's a
separate task — file it separately rather than expanding this one.

## References

Point at the prior art and source-of-truth this task depends on. Use
whatever your domain produces — a clause set, a care pathway, a chapter,
a module — not a fixed file shape.

- Existing pattern to follow: `<artifact, section, or precedent>`
- Source of truth / authority being conformed to: `<doc or reference>`
- Related `CLAUDE.md` / done-gate section: `<heading>`

## Artifacts expected to change

List every artifact you expect to create or modify — source files,
contract clauses, care-pathway documents, manuscript chapters, config:
whatever this domain produces. Per the scope-discipline rule in
`task-rules.md`, do not touch anything outside this list without adding
it here first with a one-line justification.

-
-
- (new) `<artifact created by this task>`

> If any artifact above is on the gated list (`.claude/done-gate.md` or
> `CLAUDE.md` names the canonical / high-blast-radius artifacts), that's
> a blocker, not autonomous work — surface it in **Blocker notes** and
> stop.

## Execution order

Step-by-step, numbered. Guides the worker on what to do first, second,
third, so they don't get stuck mid-task.

1. <first change>
2. <next change, building on the first>
3. Verify the affected unit of work in isolation.
4. <remaining changes>
5. Run the done-gate (per `.claude/done-gate.md`) end to end.
6. Manual check: <specific verification step>

## Acceptance criteria

Specific and verifiable. Each item must be checkable — by a done-gate
check, an objective inspection, or a one-line manual verification — not
by a feeling.

- [ ]
- [ ]
- [ ]

## Verification plan (per the done-gate)

Write this **before** doing the work. The plan is a contract, not a
rationalization of whatever the work ended up being. It says how each
acceptance criterion will be shown true.

Do **not** hardcode a verification mechanism here — the *how* lives in
`.claude/done-gate.md` (the domain's verification contract). This section
maps *this task's* criteria onto that gate.

1. **Setup:** <starting state needed to verify — seeded inputs, the
   matter/manuscript/pathway under test, the reviewer lined up>
2. **Checks:** for each acceptance criterion, the gate that proves it.
   -
   -
3. **Done-gate run:** confirm every gate in `.claude/done-gate.md` passes
   for the affected work and record the evidence (command output, named
   approver, produced document) for the closing report.

## Manual verification (in addition to the done-gate)

Steps a second party (the reviewer) will perform to confirm the work:

1.
2.

## Gotchas & learned lessons

Specific to this task. Things to watch for, things that broke in prior
attempts, anti-patterns for this area.

- **Don't do X** — here's why it goes wrong, and what to do instead.
- **Watch for Y** — easy to miss, but it matters because…
- **Backwards-compat note:** what older work/paths exist and why they
  still matter.

## Open questions / risks

-

## Blocker notes

(Filled in if the work gets stuck on an *external* dependency — a decision
from another party, missing access, an upstream task. Per `task-rules.md`,
"I don't know how" or "this is hard" is not blocked. Leave empty when
creating.)

## Self-review checklist

Before reporting the task ready for review, the worker should verify:

- [ ] I followed the execution order in the spec.
- [ ] Every acceptance criterion is met and individually verified.
- [ ] I verified each step, not just the end state.
- [ ] No gotchas / learned lessons were missed.
- [ ] Backwards-compat verified (if applicable).
- [ ] The work follows the conventions documented in the spec and `CLAUDE.md`.
- [ ] **The done-gate passes** (every gate in `.claude/done-gate.md`).
- [ ] I didn't touch artifacts outside "Artifacts expected to change"
      (or updated the task first if I needed to).

## Optional sections (include if applicable)

### Decision rationale

Why this approach over the alternatives. Reference any recon findings.

### Dependencies

- **Blocks / blocked by:** <task list, if any>
- **Owned by:** <party / N/A>
- **Requires:** <coordination, approval, an upstream task / N/A>

### Scale contract

- **Expected scale / volume:** <numbers / N/A>
- **Threshold that changes the approach:** <when / N/A>

### Backwards compatibility

- **Breaking change?** <yes / no / N/A>
- **Migration path:** <if breaking>
- **Deprecation plan:** <if applicable>

---

**Definition of done** (per `.claude/task-rules.md` → "The done-gate"):

- All acceptance criteria checked and individually verified.
- The verification plan above ran and the evidence is recorded.
- **The domain's done-gate (`.claude/done-gate.md`) passes** — no gate
  bypassed.
- Closing report posted (per `task-rules.md` → "Closing report").
