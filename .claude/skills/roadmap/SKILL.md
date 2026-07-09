---
name: roadmap
description: Display a phase-organized table of every task across `tasks/{backlog,active,blocked,completed}/` — including completed tasks. Triggered when the user wants a per-phase progress view — e.g. "show me the roadmap", "/roadmap", "how is Phase N going", "everything we've delivered and queued".
---

# /roadmap — Task list by phase (full history)

When invoked, produce a markdown summary grouped by **Phase**.
Each phase gets its own table containing every task in that
phase regardless of state (completed / active / backlog). The
output should be the only thing in the response (no preamble, no
closing commentary). It needs to render cleanly in the UI and let
the reviewer see "how is Phase N going" at a glance.

This is a pure read-and-render view. It reads `tasks/ROADMAP.md`
and the task files; it never edits anything.

## What to do

1. **Parse `tasks/ROADMAP.md`** to build a `task ID → phase`
   mapping. The ROADMAP has `## Phase N — <name>` sections
   followed by bulleted lists of `TASK-NNN — <title>`. Extract
   each phase's task IDs (preserving letter suffixes like
   `018a`). ROADMAP.md is the sole phase registry — task files do
   not declare their own phase, so the mapping comes from here and
   nowhere else.

2. **Read every task file** in `tasks/active/`,
   `tasks/blocked/`, `tasks/backlog/`, `tasks/completed/`. For
   each:
   - **ID** — from the filename (`TASK-014` from
     `TASK-014-intake-review.md`; `HOTFIX-007` from
     `HOTFIX-007-…`). Preserve letter suffixes.
   - **Title** — first H1, with the `TASK-XXX:` / `HOTFIX-XXX:`
     prefix stripped.
   - **State** — derived from directory:
     - `🚧 Active` — `tasks/active/`
     - `🚫 Blocked` — `tasks/blocked/`
     - `📋 Backlog` — `tasks/backlog/`
     - `✅ Done` — `tasks/completed/`
   - **Category** — from the `category:` frontmatter
     (`stub` / `spec` / `bug` / `hotfix`). For non-Done rows,
     render it as an icon (see Style rules). Falls back to `spec`
     when no `category:` is present, except a file in the
     `HOTFIX-` id space is `hotfix`.
   - **Delivered in** — for Done items only, look up the release
     in `tasks/RELEASES.md` if the domain keeps one: a ✅ shipped
     release names the phases and tasks it landed, so a Done
     task's release is the one naming its phase (or naming the
     task directly). If no release names it — or the domain keeps
     no `RELEASES.md` — mark `(unversioned)`.

3. **Skip non-task files:** `.gitkeep`, `README.md`,
   `ROADMAP.md`, `AUDIT.md`, `CHANGES.md`, `RELEASES.md`,
   `intake.md`, anything not matching a `TASK-` or `HOTFIX-`
   prefix.

4. **Output the document** with this exact structure:

```markdown
# 📋 Task overview by Phase

<one-line summary>: total tasks · ✅ N completed · 🚧 N active · 🚫 N blocked · 📋 N backlog (M specs / K stubs)

---

## Phase 1 — <name from ROADMAP>

<one-line phase status>: ✅ delivered / 🚧 in flight / 📋 not started

| ID | Title | State | Category | Delivered in |
|---|---|---|---|---|
| TASK-XXX | … | ✅ Done | — | v1.0.0 |
| TASK-YYY | … | 🚧 Active | 📄 Spec | — |
| TASK-ZZZ | … | 📋 Backlog | 📝 Stub | — |

## Phase 2 — <name>
...

## Phase N — <name>
...

## Cross-cutting / unphased

(Tasks that aren't in any Phase section of the ROADMAP — by the
phase rule these are the unphased ones: anything still in
`tasks/triage/` is unphased by design and not in ROADMAP, and
every Hotfix skips ROADMAP entirely. Bug follow-ups that haven't
been placed land here too.)

| ID | Title | State | Category | Notes |
|---|---|---|---|---|
| HOTFIX-XXX | … | … | 🔥 Hotfix | … |
| TASK-YYY | … | … | … | … |
```

5. **Sort within each phase** by ID ascending, with letter
   suffixes following their parent (014, 015, …, 018, 018a, 018b,
   …). In the cross-cutting table, list `HOTFIX-` ids after the
   `TASK-` ids.

6. **Phase status line** rules:
   - `✅ delivered` if every task in the phase is Done
   - `🚧 in flight` if any task is Active or Blocked, or Done
     items are mixed with Backlog
   - `📋 not started` if every task is Backlog

## Style rules

- The `Category` column is empty (`—`) for Done rows; for
  non-Done rows render the category as an icon: `📝 Stub`,
  `📄 Spec`, `🐞 Bug`, `🔥 Hotfix`.
- The `Delivered in` column is empty (`—`) for non-Done rows.
- Use the exact emoji set: 🚧 🚫 📋 ✅ 📝 📄 🐞 🔥. Don't
  substitute.
- Keep titles ≤ 60 chars; tables stay readable.
- No commentary outside the tables and headers — the data is
  the answer.
- If a phase has zero tasks (rare — empty phase in ROADMAP),
  skip its table but mention it in the summary line.

## When NOT to use this skill

- The user wants to *modify* a task — that's an edit, not a view.
- The user wants the roadmap *prose* (phase rationale, scope,
  tradeoffs) — point them at `tasks/ROADMAP.md` directly.
- A specific task's content — read the file with `Read`.
