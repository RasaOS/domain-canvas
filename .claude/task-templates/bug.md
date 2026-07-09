---
id: TASK-XXX
category: bug
status: backlog | active | blocked | completed
severity: low | medium | high
---

<!-- Phase is NOT declared here. tasks/ROADMAP.md is the sole phase
     registry (see .claude/task-rules.md → "Phase structure"). -->

# TASK-XXX: <short title — describe the bug, not the fix>

> Bug-category task. Same user-story shape as a Spec, plus
> bug-specific fields: reproduction, expected vs. actual, root
> cause (where determinable without fixing), and acceptance
> criteria for the fix. Belongs to the phase whose work is
> broken — *not* a separate "bugs" phase. Phase membership lives
> in `tasks/ROADMAP.md` only; do **not** record a phase in this
> file.
>
> Before starting: read `CLAUDE.md`, `.claude/task-rules.md`, and
> `.claude/done-gate.md` (the done-gate defines what "verified"
> means in this domain — this template never assumes a mechanism).

## User story

As a **<role>**, I want **<the broken capability>** to **<work
correctly>** so that **<outcome>**.

## Why this matters

What breaks today because of this bug? Who is affected? Frequency
— is this everyone, a subset, an edge case? Link the relevant
`CLAUDE.md` or `.claude/<domain>-task-rules.md` section if
applicable.

## Steps to reproduce

Numbered, specific, and re-runnable by another author who hasn't
seen the bug yet. The point is that someone else can stand the bug
back up on demand — that is what makes the fix verifiable.

1.
2.
3.

**Conditions:** <the relevant state — inputs, the artifact or
matter in hand, the environment, who the actor is, any version of
the work that matters>

## Expected behavior

What *should* happen at the end of those steps.

## Actual behavior

What *does* happen. Include the exact output verbatim — error
text, the wrong clause produced, the contradicted timeline, the
mis-classified record. Cite artifact paths or attach evidence
where it helps.

## Root cause *(where determinable without fixing)*

What you currently suspect or know about why the bug occurs.
Partial is acceptable — "the intake step records the date, but the
downstream summary reads a stale copy; somewhere between capture
and the rollup." A guess flagged as a guess is fine. A guess
presented as fact is not.

If the root cause is unknown, say `Unknown — to be determined
during fix.`

## Scope

**In scope:**
- <bullet — what the fix changes>

**Out of scope (explicit):**
- <bullet — adjacent problems that should be their own bug tasks>

(Per `task-rules.md` scope discipline: do not fix adjacent breakage
"while you're in there." File it as its own bug.)

## References

- Existing reproduction artifact: `<path>` (if one exists)
- Adjacent working pattern to mirror: `<path>`
- Related task / matter / issue: `<link>`
- Related `CLAUDE.md` section: `<heading>`

## Artifacts expected to change

List every artifact you expect to create or modify. If you discover
mid-fix you must touch something not listed, add it here with a
one-line justification before changing it (scope discipline).

-

## Execution order

Reproduce first, then fix, then re-verify through the done-gate.
The reproduction is the regression contract: it must fail against
the broken work and pass against the fix.

1. Stand up a reproduction that triggers the bug on demand
   (the "Steps to reproduce" above, captured so it can be re-run)
2. Confirm it reproduces for the documented reason — not some
   adjacent failure
3. Apply the fix to the responsible artifact(s)
4. Confirm the reproduction no longer reproduces
5. Run the domain's done-gate (`.claude/done-gate.md`) and confirm
   every gate passes with no regression elsewhere

## Acceptance criteria

Each item must be checkable, not a feeling. The first criterion is
always "reproduction no longer reproduces."

- [ ] Following "Steps to reproduce" now produces "Expected behavior"
- [ ] The reproduction is captured so it can be re-run later (cite it)
- [ ] The domain's done-gate passes (`.claude/done-gate.md`)
- [ ]

## Regression check

The reproduction, locked down so the bug can't return unnoticed.
This is the regression contract — it must fail against the broken
work and pass against the fix. How it is mechanized is the domain's
call (a test, a continuity check against the bible, a cite-check, a
clinical-rule validation) and is defined in `.claude/done-gate.md`.

1. **Setup:** <the seeded state the reproduction needs>
2. **Steps:** <the smallest reproduction>
3. **Check:** <what confirms correct behavior>

## Blast radius / reversal

What else does the fix touch? If the fix turns out wrong after it
lands, what gets reverted, and how is the prior state restored?
Name the dependents so a reviewer can judge the risk.
