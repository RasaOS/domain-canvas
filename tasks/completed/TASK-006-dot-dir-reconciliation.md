---
id: TASK-006
category: spec
status: completed
---

> **DECISION (user, 2026-07-09): branch (b) — keep `.rasaos/apps/`, file
> upstream.** Rationale: the live shell (`VerticalCanvasPane` @ `a5f6ff1`)
> bootstraps `.rasaos/apps/<id>`; migrating now would open a doctrine/shell
> divergence window (the class of bug HOTFIX-001 just closed), and the naming
> is platform-owned (kernel resolves the cwd, shell bootstraps it) — per the
> kernel-heavy principle the call belongs to canon. Draft filed:
> `docs/canon-drafts/SA-0XX-tenant-app-state-directory.md` (rides TASK-007's
> canon batch). Decision recorded in binding-model §3. If canon rules
> `.rasa/apps/`, migrate in one coordinated pass with the frontend.

# TASK-006: Reconcile `.rasaos/` vs canon `.rasa/` (decide + migrate or file upstream)

## User story

As the **substrate maintainer**, I want **one hidden-dir convention per
tenant** so tooling, docs, and the audit walk never juggle two dot-roots
(`.rasaos/apps/` from this element vs canon's `.rasa/holding/`).

## Why this matters

Design review #12: our app tree (`<tenant>/.rasaos/apps/<app-id>/`) and
canon's SA-019 hidden dir (`.rasa/`) coexist unreconciled. Migrating is
cheap NOW (no production tenants); it only gets more expensive.

## Scope

**In scope:**
- Decide: (a) migrate this element to `<tenant>/.rasa/apps/` (aligns with
  canon; recommended), or (b) keep `.rasaos/` and file the naming question as
  a canon triage task.
- If (a): update every path reference — `CLAUDE.md`, `content/BUILDER.md` +
  `APP_MODEL.md` + `PROCESSES.md`, `rasa.json#rasa.session_model`, design docs
  — and note the change in KERNEL_ASKS (the kernel keys sessions by cwd; the
  cwd convention is ours, but the shell/kernel docs that mention
  `.rasaos/apps` need the flag).
- Patch version bump + CHANGELOG.

**Out of scope (explicit):**
- Migrating any live tenant data (none exists) · canon edits (that's the
  canon session's work if (b)).

## References

- Canon §53 SA-019 (`.rasa/holding/`, `elements/` visible path).
- `docs/design/binding-model.md` §3 rules ("Naming tension, on the record").

## Artifacts expected to change

- `CLAUDE.md` ⚠ gated · `content/{BUILDER,APP_MODEL,PROCESSES}.md`
- `rasa.json` (session_model prose) · `docs/design/*.md`
- `VERSION` + `CHANGELOG.md`

## Execution order

1. Confirm the decision with the user (one question: migrate to `.rasa/apps/`
   or file upstream?).
2. Execute the chosen branch; grep-sweep `\.rasaos` to zero (or to a
   documented decision record).
3. Gate GREEN; bump; commit.

## Acceptance criteria

- [x] Exactly one convention documented everywhere;
      the canon task filed + linked (branch (b) kept: draft at
      `docs/canon-drafts/SA-0XX-tenant-app-state-directory.md`, linked from
      binding-model §3; `.rasaos/apps/` remains the one documented convention,
      matching the live shell).
- [x] check-doctrine GREEN.

## Verification plan (per the done-gate)

1. **Setup:** none.
2. **Checks:** the grep sweep output · the canon-task link if (b).
3. **Done-gate run:** all gates; gated-file approval for CLAUDE.md.

## Manual verification (in addition to the done-gate)

1. Reviewer greps and finds one story.

## Gotchas & learned lessons

- **The kernel doesn't care about the dir name** (cwd is just a path) — the
  risk is doc/tool drift, not runtime breakage. Don't over-engineer.

## Open questions / risks

- User's call on (a) vs (b) — step 1.

## Blocker notes

(empty)

## Self-review checklist

- [x] I followed the execution order in the spec (step 1 asked; branch (b)
      needed no CLAUDE.md/content/ edits — docs-only).
- [x] Every acceptance criterion is met and individually verified.
- [x] I verified each step, not just the end state.
- [x] The done-gate passes (every gate in `.claude/done-gate.md`).
- [x] I didn't touch artifacts outside "Artifacts expected to change" (the
      (b) branch touched only the canon draft + binding-model note — a subset).

### Dependencies

- **Blocks / blocked by:** independent; best before TASK-003 ships paths into
  new schema/doctrine (else those need the sweep too).

---

**Definition of done** (per `.claude/task-rules.md`): all criteria verified ·
plan ran with evidence · done-gate passes · closing report posted.
