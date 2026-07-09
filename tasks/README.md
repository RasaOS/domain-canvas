# tasks/

This is your project's task system, provided by `rasa.module.tasks`. It
is the portable, domain-agnostic lifecycle for tracking every unit of
work — whether this project is a software domain, a legal domain, a
healthcare domain, a writing domain, or an orchestrator coordinating
across many of them.

The rules that govern every task live in **`.claude/task-rules.md`**.
This README is the map; that file is the law. Read it before working a
task.

## The state machine

A task moves left to right through directories. Its directory is its
state, and the `status:` field in its frontmatter mirrors the directory
it lives in — the same fact recorded twice for easy inspection.

```
intake.md  →  triage/  →  backlog/  →  active/  ⇄  blocked/  →  completed/
  (raw)       (tracked,    (phase +     (in          (parked,      (done-gate
              no phase)     category)    flight)       ext. dep)     passed)
```

| Stage | What lives here |
|---|---|
| **`intake.md`** | A single file of raw notes — pre-triage capture. No id, no commitment. |
| **`triage/`** | Tracked tasks with a `TASK-NNN` id but no phase, category, or priority yet. Deliberately *not* in `ROADMAP.md`. |
| **`backlog/`** | Phase-placed, category-assigned tasks ready to be worked. |
| **`active/`** | In-flight work. At most one task per worker at a time. |
| **`blocked/`** | A *parked* state — was active, hit an **external** dependency (missing access, waiting on another party). Needs a `## Blocker` section naming what unblocks it. |
| **`completed/`** | Terminal state. Acceptance criteria met **and** the done-gate passed. |

Move the task file as you transition states (use your version-control
move when one applies). Status and directory must always agree.

## intake vs triage

Both are early stages, but they cost different things:

- **`intake.md`** is a one-line append — a bullet, no id, no file. The
  lowest-friction "I wrote it down" layer. Use it for half-ideas,
  observations, and complaints before you've decided they're real tasks.
- **`triage/`** is a real task: a `TASK-NNN` id and a spec file (usually
  a stub). It's tracked long-term but not yet committed to a phase.

When an intake note matures, *promote* it to triage. When a triage task
earns a phase, *graduate* it to `backlog/` (and add its `ROADMAP.md`
line). Don't let either layer rot — run a pass periodically.

## Categories

Every task in `backlog/` and beyond carries a `category:` in its
frontmatter, answering *what kind of work is this?*

| Category | Id space | What it is |
|---|---|---|
| **`stub`** | `TASK-NNN` | Tracked lightly — title + brief note. Exists to be visible and counted, not expanded. |
| **`spec`** | `TASK-NNN` | The default. Full work contract: user story, scope, acceptance criteria, verification plan. |
| **`bug`** | `TASK-NNN` | Fix broken behavior. Spec shape plus reproduce steps, expected vs. actual, root-cause notes. |
| **`hotfix`** | `HOTFIX-NNN` | Urgent fix that ships now. **Skips `ROADMAP.md`**, routes straight to `active/`, pairs with a postmortem. |

Templates for each live in `.claude/task-templates/<category>.md`.

## The done-gate

A task is **done** only when both hold:

1. its acceptance criteria are met and *actually verified*, and
2. the domain's done-gate passes.

What "done" requires is the one thing that varies by domain, so it is
**not** hardcoded here. It lives in **`.claude/done-gate.md`** — your
project fills that file with its real gates (a command that exits zero,
a named reviewer's approval, a produced document). Never bypass a gate
to finish faster.

## ROADMAP.md is the registry

**`ROADMAP.md` is the sole phase registry.** Every task that belongs to
a phase is listed there, under that phase, and nowhere else. Tasks do
**not** declare their phase in their own spec file — that would drift.
The one exception is `triage/`: triage tasks are deliberately unphased
and are not in `ROADMAP.md` until they graduate.

The invariant: *in `ROADMAP.md` ⟺ has a phase ⟺ triaged.*

## Recording surfaces

- **`AUDIT.md`** — curated, append-only log of meaningful actions
  (ships, milestones, rule changes, scaffolding, hotfixes, incidents).
  Newest on top; ISO date headers.
- **`CHANGES.md`** — append-only change ledger: every artifact/config
  change linked to its task. The long-term audit-and-review surface.

---

*Everything in this directory follows `.claude/task-rules.md`. When this
README and that file disagree, the rules file wins.*
