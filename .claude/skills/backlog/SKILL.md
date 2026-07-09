---
name: backlog
description: Show what's actively being worked on, what's queued up next, and what's parked in triage. Forward-looking only — completed work is not included. Triggered when the user wants to know "what are we doing now and what's next" — e.g. "show me the backlog", "/backlog", "what's queued", "what's next".
---

# /backlog — Active + queued + triage tasks

When invoked, produce a single markdown table of every task that
is **not yet done** — i.e. everything in `tasks/active/`,
`tasks/blocked/`, `tasks/backlog/`, and `tasks/triage/`. Completed
tasks are deliberately excluded. The user wants to see what's in
flight, what's parked, what's coming up, and what hasn't been
triaged yet — not what's already shipped.

This is a **pure read-and-render** skill: it reads the task files and
`ROADMAP.md` and renders a table. It changes nothing.

The output is the only thing in the response (no preamble, no
closing commentary). Render in under 5 seconds.

## What to do

1. **Read** every task file in `tasks/active/`, `tasks/blocked/`,
   `tasks/backlog/`, and `tasks/triage/`. Skip `tasks/completed/`
   entirely. Skip `.gitkeep`, `README.md`, `ROADMAP.md`, `AUDIT.md`,
   `CHANGES.md`, `intake.md`, and anything whose id is not in the
   `TASK-NNN` or `HOTFIX-NNN` space.

2. **Parse `tasks/ROADMAP.md`** to map task IDs → phase names.
   Phase sections are headed `Phase N: <short noun-phrase>` (also
   accept the `## Phase N — <name>` heading form), with bulleted
   task IDs (`- TASK-NNN — <title>`) listed under each phase's scope
   paragraph. A task that appears in no phase gets phase =
   `Cross-cutting` — **except** two cases that are unphased by
   design and always show phase = `—`:
   - **Triage tasks** (`tasks/triage/`), which are deliberately not
     in `ROADMAP.md` until they graduate.
   - **Hotfixes** (`HOTFIX-NNN`), which skip phase placement entirely
     and route straight to `active/`.

3. **For each task, extract:**
   - **ID** — from the filename, with any letter suffix preserved
     (e.g. `TASK-018a`). Hotfix tasks carry the `HOTFIX-NNN` prefix.
   - **Title** — the first H1, with the `TASK-XXX:` / `HOTFIX-XXX:`
     prefix stripped.
   - **State** — by directory:
     - `🚧 Active` — `tasks/active/`
     - `⏸ Blocked` — `tasks/blocked/`
     - `📋 Backlog` — `tasks/backlog/`
     - `🗂 Triage` — `tasks/triage/` (tracked, not yet triaged
       into a phase)
   - **Type** — from the `category:` frontmatter (`stub` / `spec` /
     `bug` / `hotfix`); a task with no `category:` defaults to
     `spec`:
     - `📝 Stub` — `category: stub`, **or** the literal string
       `STATUS: STUB` appears anywhere in the file (a spec-category
       task filed at stub-content level). Still needs detail before
       starting.
     - `📄 Spec` — `category: spec` with full content; ready to work.
     - `🐞 Bug` — `category: bug`.
     - `🔥 Hotfix` — `category: hotfix`.
   - **Phase** — from step 2. Triage tasks and hotfixes show `—`.

4. **Sort the rows** by readiness, so the things shipping
   soonest are at the top:

   1. All `🚧 Active` rows first, by ID ascending.
   2. Then `⏸ Blocked` rows, by ID ascending — in flight but parked.
   3. Then `📋 Backlog · 📄 Spec` rows, by ID ascending.
   4. Then `📋 Backlog · 📝 Stub` rows, by ID ascending.
   5. Then `🗂 Triage` rows last, by ID ascending — tracked,
      but not yet planned.

   Within each group, `TASK-018a` comes after `TASK-018` and
   before `TASK-018b`.

5. **Output** with this exact structure:

```markdown
# 📋 Backlog — what's now, next & parked

**Active**: N · **Blocked**: N · **Specs ready**: N · **Stubs to flesh out**: N · **In triage**: N

| ID | Title | State | Type | Phase |
|---|---|---|---|---|
| TASK-XXX | … | 🚧 Active | 📄 Spec | Phase 3 |
| TASK-YYY | … | ⏸ Blocked | 📄 Spec | Phase 2 |
| TASK-ZZZ | … | 📋 Backlog | 📄 Spec | Phase 1 |
| TASK-WWW | … | 📋 Backlog | 📝 Stub | Phase 4 |
| TASK-VVV | … | 🗂 Triage | 📝 Stub | — |
```

## Style rules

- One single table — don't subdivide by phase or state. Phase and
  state show as columns for context, not as groupings. (User has
  `/roadmap` for the phase-organized view.)
- Use the exact emoji set: 🚧 ⏸ 📋 🗂 📄 📝 🐞 🔥. Don't substitute.
- Trim titles to ≤ 60 chars.
- No commentary outside the header line and table — the data
  is the answer.
- If `active/`, `blocked/`, `backlog/`, and `triage/` are all empty,
  output a single line: *"No active, blocked, queued, or triage
  tasks. See `/roadmap` for the full history."*

## When NOT to use this skill

- The user wants to see completed work or per-phase progress —
  point them at `/roadmap` instead.
- The user wants the roadmap *prose* (rationale, tradeoffs) —
  point them at `tasks/ROADMAP.md`.
- A specific task's content — read the file with `Read`.
