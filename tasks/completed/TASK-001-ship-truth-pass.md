---
id: TASK-001
category: spec
status: completed
---

# TASK-001: Ship the truth-pass + design corpus + task system as v0.6.0

## User story

As the **element maintainer**, I want **the verified truth-pass, the design
corpus, and the installed task system shipped as one v0.6.0 release** so that
runtime sessions everywhere stop authoring UIs the shell can't render, and the
design work has a committed baseline.

## Why this matters

The working tree holds ~15 files of verified corrections (COMPONENTS.md real
prop shapes + emission grammar, the nav-`intent` fix, KERNEL_ASKS #3
correction + #11/#12, check-app grammar fix, golden/fixture/schema-$id fixes),
the full design corpus under `docs/`, and the module-tasks install — all
uncommitted. Until this ships, every runtime session still pulls the broken
doctrine from the last commit.

## Scope

**In scope:**
- Version bump 0.5.0 → 0.6.0 (`VERSION` + `rasa.json#version`).
- CHANGELOG entry: the truth-pass, the design corpus, the handoffs, the
  module-tasks install + Phase 1.
- One commit of the whole working tree; local tag `v0.6.0`.

**Out of scope (explicit):**
- Any new doctrine/content change (this ships what exists).
- Pushing to GitHub (user-run, per workspace rule).
- The re-role (TASK-002).

## References

- `docs/design/BUILD_ORDER.md` → "Done (2026-07-09 — the truth-pass)" is the
  shipping manifest.
- Workspace convention: VERSION + rasa.json#version + CHANGELOG same commit.

## Artifacts expected to change

- `VERSION`
- `rasa.json` (`#version` only)
- `CHANGELOG.md` (new `## 0.6.0` entry)
- (commit) everything already modified/untracked per `git status`

## Execution order

1. Bump `VERSION` and `rasa.json#version` to `0.6.0`.
2. Write the `## 0.6.0 — <date>` CHANGELOG entry (truth-pass · design corpus ·
   handoffs · module-tasks install + Phase 1).
3. Run `bin/check-doctrine` — must be GREEN (version plumbing now checks 0.6.0).
4. `git add -A && git commit` (pre-commit hook runs the gate again).
   **4b (added mid-task, justification below):** `git merge main` — main moved
   past our branch point (v0.5.1 kit-aware bin/init + /sync + /promote;
   v0.5.2 identity layer). Resolve CHANGELOG (stack 0.6.0 > 0.5.2 > 0.5.1 >
   0.5.0), VERSION (0.6.0), rasa.json (keep main's additions + ours), favor
   the truth-pass for any content-contract conflict. Gate GREEN on the merged
   tree, THEN tag `v0.6.0` on the merge commit — a v0.6.0 whose ancestry
   lacked 0.5.1/0.5.2 would be semantically wrong.
5. Post the closing report; append the 📦/🚀 entries to `tasks/AUDIT.md`.

## Acceptance criteria

- [x] `check-doctrine` GREEN at the committed tree.
- [x] `VERSION` == `rasa.json#version` == newest CHANGELOG heading == `0.6.0`.
- [x] One commit contains the full working set; local tag `v0.6.0` exists —
      *amended mid-task:* the working set lands in one commit; `v0.6.0` tags
      the post-merge tree so the release contains 0.5.1 + 0.5.2 (see step 4b).
- [x] `kit/` is NOT in the commit (gitignored).

## Verification plan (per the done-gate)

1. **Setup:** clean run of `git status` before commit to enumerate the set.
2. **Checks:** criterion 1 → `bin/check-doctrine; echo $?` = 0 · criterion 2 →
   the plumbing check inside check-doctrine · criterion 3 → `git show --stat
   v0.6.0` · criterion 4 → `git ls-files kit/` empty.
3. **Done-gate run:** all gates in `.claude/done-gate.md`; evidence in the
   closing report.

## Manual verification (in addition to the done-gate)

1. Reviewer reads the CHANGELOG entry and confirms it honestly describes the set.
2. `git show v0.6.0 --stat` matches the BUILD_ORDER "Done" list.

## Gotchas & learned lessons

- **Don't split the version plumbing across commits** — check-doctrine fails on
  any drift between the three surfaces.
- **The pre-commit hook only runs if** `git config core.hooksPath .githooks`
  is set in this worktree — verified already set (shared repo config).
- **(learned this task) Check main's tags BEFORE picking the version** — main
  had shipped v0.5.1/v0.5.2 on a parallel branch; blind-tagging v0.6.0 from a
  stale branch point would have produced a release not containing them. The
  merge-then-tag step (4b) is the fix; future ship tasks should start with
  `git tag -l` + `git log main --oneline -3`.

## Open questions / risks

- None.

## Blocker notes

(empty)

## Self-review checklist

- [x] I followed the execution order in the spec (incl. the amended 4b).
- [x] Every acceptance criterion is met and individually verified.
- [x] I verified each step, not just the end state.
- [x] The done-gate passes (every gate in `.claude/done-gate.md`).
- [x] I didn't touch artifacts outside "Artifacts expected to change" (the
      merge step was added to the spec with justification before executing).

---

**Definition of done** (per `.claude/task-rules.md` → "The done-gate"): all
criteria verified · verification plan ran with evidence recorded · the
done-gate passes · closing report posted.
