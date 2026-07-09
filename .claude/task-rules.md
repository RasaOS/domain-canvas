# Task Rules — `rasa.module.tasks`

These rules govern **every** task in `tasks/`. They are the portable,
domain-agnostic task-management lifecycle distilled from
`rasa.domain.code` and shipped as a mountable Element. They apply
unchanged whether the parent is a software domain, a legal domain, a
healthcare domain, a writing domain, or an orchestrator coordinating
across many of them.

> **This file is domain-neutral by design.** Anything stack-specific —
> what "verified" means, what a "change" is, which files are gated, the
> commands to run — lives in two places this file points to, never
> inline:
>
> 1. **`.claude/done-gate.md`** — the parent domain's definition of
>    *what "done" requires* (the verification contract). Code fills it
>    with build+test+review; legal with cite-check + partner review;
>    health with clinical-rule validation + compliance sign-off. This
>    file references the done-gate; it never hardcodes one. See
>    "The done-gate" below.
> 2. **Domain extension files** — `.claude/<domain>-task-rules.md`
>    (e.g. `code-task-rules.md`, `legal-task-rules.md`). A domain that
>    needs extra task discipline beyond the portable core adds a prefix
>    file; this file is read first, the extension second. The prefix is
>    a discovery hint, not a gate. Pure cross-domain work reads only
>    this file. See "Domain extensions" below.
>
> The parent's `CLAUDE.md` owns project-specific conventions, the
> concrete done-gate commands, and the gated-file list. Read it
> alongside this file before starting work.

## The done-gate

A task is **done** when two things are both true:

1. **Its acceptance criteria are met** — every checklist item in the
   task spec is satisfied and *actually verified*, not assumed.
2. **The domain's done-gate passes** — the verification contract the
   parent domain defines in `.claude/done-gate.md`.

The done-gate is the one piece of "done" that varies by domain, so it
is the one piece this file refuses to hardcode. The portable contract
is only the *shape*:

- The done-gate is a checklist of gates, each of which must pass before
  a task leaves `active/` for `completed/`.
- Each gate is **objectively checkable** — a command that exits zero, a
  named reviewer's approval, a document that exists — not a feeling.
- If a gate cannot pass and you cannot make it pass in scope, the task
  is **not done**: write a blocker and park it (see "The blocked
  state"), or report it honestly (see "Honest reporting").
- **Never bypass the gate.** Whatever the domain's mechanism, the
  equivalent of "skip verification to ship faster" is forbidden.

If `.claude/done-gate.md` is absent, the default gate is the minimum
honest bar: *every acceptance criterion is checked and a second party
(human reviewer) has approved.* A domain SHOULD replace this with its
real gate; running on the default is a smell, not a destination.

## Scope discipline

- One task = one unit of shippable work. Do not bundle unrelated
  changes into a single task.
- Touch only the artifacts listed in the task's "Artifacts expected to
  change" section. If you need to touch something outside that list,
  **add it to the task file with a one-line justification before
  changing it.**
- Do not "improve adjacent work while you're in there." Out of scope.
- Do not add scope — features, structure, options — not required by the
  acceptance criteria.

("Artifacts" is deliberately neutral: source files, contract clauses,
care-pathway documents, manuscript chapters — whatever this domain
produces.)

## Every change is task-linked (the change-audit rule)

**Every change to a domain artifact is linked to a task.** No exception
— not a planned piece of work, not a one-line urgent fix, not a "quick
change" made under pressure. The task is the audit trail; a change with
no task is a hole in the record no one can review later.

This applies to **the artifacts the domain ships and to its
running/operative configuration**. It does not apply to documentation,
the task files themselves, or `.claude/` meta — those carry no
operative risk and need no task.

- **Before a change, there should be a task.** Working something
  trivial? It still gets a task. If a full spec is overkill, a one-line
  stub is enough — but the task must exist and be linked.
- **A stub is acceptable; nothing is not.** The bar is "a task exists,"
  not "a task is fully spec'd." An honestly-flagged stub — title, why
  it wasn't spec'd, the artifacts touched — keeps the audit trail
  whole. Spec it retroactively with `/task` if it matters.
- **The change ledger.** `tasks/CHANGES.md` is the append-only record:
  every artifact/config change, its linked task, who made it, the date,
  the artifacts. This is the long-term audit-and-review surface.

**Enforcement is domain-specific.** A software domain can enforce this
with a pre-commit hook (e.g. a `task-guard` that auto-stubs an
unlinked commit); a domain whose "commits" are document revisions
enforces it at its own checkpoint. The *rule* holds regardless of
whether any automated enforcement is wired; the parent domain decides
the mechanism and documents it in `.claude/done-gate.md` or its
extension file.

## Files that require explicit permission to modify

Touching any of these = blocker, not autonomous work. The exact list is
domain-specific — the parent's `CLAUDE.md` enumerates the gated
artifacts. Process files are gated everywhere:

- **This task system's own files** — `CLAUDE.md`, `.claude/task-rules.md`,
  `.claude/done-gate.md`, `.claude/task-templates/`, `.claude/skills/`,
  and any `.claude/<domain>-task-rules.md` extension.
- **Whatever the domain marks as canonical / high-blast-radius** — its
  source-of-truth schema, its operative configuration, its
  infrastructure or compliance-controlled files. The done-gate or the
  parent `CLAUDE.md` names them.

If a task requires changing a gated artifact, surface it in the task
file's blocker section and stop.

## State machine

```
tasks/intake.md  →  tasks/triage/  →  tasks/backlog/  →  tasks/active/  ⇄  tasks/blocked/  →  tasks/completed/
   (raw)            (formalized,       (phase +              (in              (parked,            (done-gate
                     no phase/cat)      category assigned)    flight)          ext. dep)            passed)
```

- **`intake.md`** is a single markdown file holding raw notes,
  observations, and complaints that haven't yet decided to become
  tasks. Pre-triage. No `TASK-NNN` id. The lowest-friction capture
  layer. See "The intake layer" below.
- **`triage/`** holds tracked-but-untriaged tasks — filed with a
  `TASK-NNN` id but no phase, no category, no priority. A task sits here
  until it is *graduated* (category + phase assigned → `mv` to
  `backlog/`) or pulled straight to `active/`. Triage tasks are the one
  exception to the phase rule — they are deliberately not in
  `ROADMAP.md`. See "The triage holding area" below.
- **`backlog/`** holds phase-placed, category-assigned tasks ready to be
  worked. The category (Stub / Spec / Bug / Hotfix) is declared in the
  task's frontmatter. See "Categories" below.
- **`active/`** should hold at most one task at a time per worker.
- **`blocked/`** is a *parked state* for tasks that were in `active/`
  but hit an external blocker (missing access, waiting on another
  party, third-party outage, undecided call). The task file moves to
  `tasks/blocked/`; status becomes `blocked`; the blocker is named in
  the file. See "The blocked state" below.
- **`completed/`** is the terminal state — acceptance criteria met and
  the done-gate passed. Work that is finished-but-not-yet-verified stays
  in `active/`.
- Move the task file as you transition states (use your domain's
  version-control move, e.g. `git mv`, when one applies).

**Hotfixes skip part of the lifecycle.** A Hotfix-category task uses the
`HOTFIX-NNN` id space (not `TASK-NNN`), is filed directly to
`tasks/active/`, and bypasses phase placement entirely — it doesn't go
in `ROADMAP.md`. See "Categories" below.

### The status field

Every task spec declares `status:` in its frontmatter, matching the
directory it lives in:

```yaml
status: triage | backlog | active | blocked | completed
```

Status and directory must agree — the same fact recorded twice for ease
of inspection. The directory move and the frontmatter change happen
together. A task in `tasks/blocked/` with `status: active` is a bug; fix
the frontmatter or fix the directory.

### The blocked state

A task in `blocked/` was being worked but hit an **external** dependency
that prevents progress. Examples:

- Waiting on a decision from another party / an owner / the user.
- A third party is unavailable or undocumented.
- Missing access or a credential only a specific person can grant.
- Waiting on an upstream task that hasn't shipped.

The blocked file must have a `## Blocker` section with: what's blocking,
who or what would unblock it, when to check back. Without that section
the task is not blocked — it's abandoned, which is a different problem.

Returning from blocked to active is a move back to `active/` plus a
status flip. A task is **not blocked** if the obstacle is "I don't know
how" (recon problem), "this is hard" (just work), or "I forgot" (move
back to `backlog/`). Blocked is for *external* dependencies only.

## Closing report (mandatory)

When a task reaches the done-gate, the closer **must** post a completion
report with this shape. The point is one-glance status — a reviewer
scans it in five seconds and decides whether to dig in. "What you need
to do next" is non-negotiable; every task tells the reviewer exactly
what action to take.

```markdown
## TASK-XXX completion report

| | |
|---|---|
| **Name** | <descriptive name from the task spec> |
| **Status** | ✅ Ready for review / ⚠️ Blocked / ❌ Failed |
| **Category** | stub / spec / bug / hotfix |

**Done-gate** (per `.claude/done-gate.md`)
- <gate 1>: ✅/❌ · <evidence — command output, reviewer, doc link>
- <gate 2>: ✅/❌ · <evidence>

**What changed**
- One-line bullets, the actual deltas

**What you need to do next** (in order)
1. Concrete action
2. Concrete action

**Things I noticed** (not blockers — can be empty)
- ...
```

Rules:

- **Status** is one of three states. Never "almost ready" or "mostly
  done." If acceptance criteria aren't met, status is ⚠️ Blocked or
  ❌ Failed and the report says why.
- **Done-gate results are evidence, not adjectives.** Cite the real
  command output / the named approver / the produced artifact — not
  "verified."
- **Don't tick boxes you didn't check.** Same rule as the rest of this
  file.

## Audit log (mandatory)

`tasks/AUDIT.md` is the curated, append-only chronological record of
meaningful actions on the project — ships, milestones, rule changes,
scaffolding events, incidents. Version-control history is the ground
truth; this file is the human-readable layer on top.

### What to log

- 📦 **Task ships** (a task reached `completed/`). One line per task.
- 🚀 **Milestones / releases / publications** — whatever "shipped to the
  world" means in this domain. Include the receipt (tag, matter number,
  publication ref).
- 📜 **Rule / process changes** in `task-rules.md` or the done-gate.
- 🏗 **Major scaffolding** (new convention, new tooling affecting
  everyone).
- 🔥 **Hotfixes.** One line per hotfix, with a link to the postmortem.
- ⚠️ **Incidents** and **honest tradeoff calls** future readers will
  need to understand.

### What NOT to log

- Every change. Version-control history already has those.
- Routine work that doesn't change behavior.
- Drafts that don't ship.

### How to write entries

- **Newest entries on top** within their date section.
- ISO date headers (`## YYYY-MM-DD`).
- One to a few lines per entry, bullet form. Lead with the *what*, end
  with the receipt.
- Use the emoji set sparingly: 📦 ships, 🚀 milestones, 📜 rules,
  🏗 scaffolding, 🔥 hotfixes, ⚠️ incidents/tradeoffs.
- Don't backdate. If you forgot to log something, log it today with
  `(retroactive)`.

## Phase structure (mandatory)

Phases are first-class. Every task **in `ROADMAP.md`** belongs to
exactly one phase — no orphans, no "we'll figure out where this fits
later." The one exception is the **triage holding area**: tasks parked
in `tasks/triage/` are tracked but deliberately unphased and are not in
`ROADMAP.md` until they graduate.

### Each phase has three things

1. **A name.** "Phase N: \<short noun-phrase\>". Communicates the scope
   at a glance.
2. **A scope paragraph.** 2–4 sentences in `tasks/ROADMAP.md` directly
   under the phase heading. Says what's in, what's out, and (when
   useful) what success looks like. The scope is the *contract* — if a
   task doesn't fit it, the task belongs in a different phase.
3. **An ordered list of tasks.** Bulleted under the scope paragraph.
   Each entry is `- TASK-NNN — <title>`. Order implies suggested ship
   order.

### `tasks/ROADMAP.md` is the registry

Phase membership lives in ROADMAP.md, nowhere else. Tasks do **not**
declare their phase in their own spec file (that would drift). The
skills (`/roadmap`, `/backlog`) parse ROADMAP to build the task→phase
map. The invariant: *in `ROADMAP.md` ⟺ has a phase ⟺ triaged.*

### Adding, creating, moving phases

- **Add a task:** decide the phase first; if there's no phase for it
  yet, file to triage and stop — don't force a phase. Otherwise add the
  task line under that phase in `ROADMAP.md` and create the spec file in
  `tasks/backlog/`.
- **Create a phase:** pick a name, write the scope paragraph (in/out
  explicit), add it to `ROADMAP.md` in sequence, then file tasks under
  it. Don't create empty phases speculatively.
- **Move a task between phases:** single edit to `ROADMAP.md` (remove
  from old list, add to new). The spec file doesn't move — its directory
  reflects *state*, not phase.

## Categories (mandatory)

Every task in `backlog/`, `active/`, `blocked/`, or `completed/` has a
**category** in its frontmatter. The category answers: *what kind of
work is this, and how do we treat it?*

```yaml
---
id: TASK-042            # or HOTFIX-042 for the Hotfix category
category: spec          # stub | spec | bug | hotfix
status: backlog         # triage | backlog | active | blocked | completed
---
```

There is **no `phase:` field** in a task's frontmatter — phase
membership lives in `ROADMAP.md` and nowhere else (see "Phase
structure"). Recording a phase in the spec file too would create a
second source of truth that drifts.

- **`stub`** — track lightly, no full spec. Title, brief description,
  optional notes. Signals: don't expand this; it exists to be visible
  and counted. Template: `task-templates/stub.md`. Stub tasks still
  belong to a phase, appear in `ROADMAP.md`, and move through the state
  machine.
- **`spec`** — the default. Full work contract: as-a / I-want /
  so-that, scope, acceptance criteria, verification plan. Template:
  `task-templates/spec.md`. May start as stub-content and be expanded
  close to execution.
- **`bug`** — fix broken behavior. Spec shape plus: steps to reproduce,
  expected vs. actual, root-cause notes, acceptance criteria for the
  fix. Template: `task-templates/bug.md`. Bugs belong to the phase whose
  work is broken — not a separate "bugs" phase.
- **`hotfix`** — urgent fix that must ship now. Procedurally distinct:
  `HOTFIX-NNN` id space, **no phase placement** (not in `ROADMAP.md`),
  **direct routing to `tasks/active/`**, a dedicated template
  (`task-templates/hotfix.md`: urgency justification, what's broken, the
  smallest fix, rollback plan, post-fix verification), and a 🔥 AUDIT
  entry when shipped. If the urgency dissipates, re-categorize as `bug`,
  switch the id prefix to `TASK-NNN`, and route normally.

### Stub-content vs. category

The priority-signal rule (below) governs *content level* at filing time
(stub-content vs. full-content). The category governs *intended shape*.
Both apply: a `spec`-category task may be filed as stub-content and
expanded later; a `hotfix` always has full content.

### Backwards compatibility

Tasks with no `category:` frontmatter default to `category: spec`.
Adding categories does not require re-filing existing tasks.

## Adding tasks to the backlog (priority rule)

When the user says "add a task" without specifying urgency, **append to
`tasks/backlog/` as a minimal stub and stop there.** Don't promote it
ahead of others, don't draft a full spec (specs are expanded close to
execution), don't reshuffle phase ordering to "make room," don't
subdivide into siblings unless asked.

A minimal stub is title + 1-line user story + 1-line "why" +
`STATUS: STUB — full spec drafted before execution`. Anything more is
speculative.

## Full spec vs. stub: the priority signal rule

**Default: stub.** A full spec is created *only* if the user explicitly
signals urgency — "emergency" / "urgent" / "do it now", "needs to ship
before X", "this is next up", "top priority". These trigger both
placement (ahead in the roadmap) and an immediate full spec.

**Placement without spec:** "needs to ship before X" → place ahead of X,
spec later. "X first, then this" → place after X, stub until X ships.
"future phase" / "later" / no qualifier → backlog only, no
re-sequencing, stub.

When unsure, ask: *"backlog only, or should this jump the queue?"* — one
round trip beats a wrong placement.

## The triage holding area

`tasks/triage/` holds tasks you want **tracked long-term but not yet
triaged** — no phase, no priority, no commitment on when (or whether)
they get worked. A triage task is real (a `TASK-NNN` id and a spec
file, usually a stub) but lacks a phase, so by the phase rule it is
**not in `ROADMAP.md`**.

- **Filing to triage:** when the user files a task with no phase for it
  yet — or can't name one — file it to `tasks/triage/` rather than
  forcing a phase. A stub is the norm. Do **not** edit `ROADMAP.md`.
- **Graduating out of triage:** either assign a phase + `mv` to
  `backlog/` + add the `ROADMAP.md` line, or pull it straight to
  `active/` (still assign a phase + ROADMAP line as part of starting).
- Don't let triage rot. When it accumulates, run a triage pass:
  graduate what matters, move what won't be done to `.claude/wont-do.md`.

## The intake layer

`tasks/intake.md` is the **pre-triage capture surface** — a single
markdown file where raw notes, complaints, observations, and rough ideas
land before anyone has decided whether they should become tasks. The
lowest-friction layer in the lifecycle.

Triage costs a small but real thing: an ID is spent, a file exists.
Intake is a one-line append: a bullet in `intake.md`. No ID, no file, no
commitment beyond "I wrote it down."

### Format

A single markdown file at `tasks/intake.md`. Loosely structured — "easy
to add to" first, "consistent" second. H2 by date, bulleted entries with
a bolded short title and a sentence of context:

```markdown
# Task Intake

Pre-triage capture. Raw notes that may or may not become tasks. When an
entry matures, promote it to triage via `/task promote` (creates a
TASK-NNN in `tasks/triage/`) — or delete it.

## 2026-06-18

- **Intake feels noisy** — three half-ideas about onboarding; revisit.
- **Recurring question from reviewers** — worth a standing answer.
```

### Promoting / dropping

- `/task promote "<identifier>"` creates a `TASK-NNN` stub in
  `tasks/triage/`, removes the entry from `intake.md`, and stops. The
  new task has no phase, no category — decided at graduation.
- `/task drop "<identifier>"` removes an entry without creating a task.
  Optionally move the rationale to `.claude/wont-do.md`.

## Postmortem rule (incidents get captured)

The audit log records what shipped. The postmortem records what *broke*
and what changed to prevent recurrence.

### When to write one

- Any operative failure, rollback, or harm event in the domain's terms.
- Any hotfix (every 🔥 entry pairs with a postmortem).
- Any data-loss / corruption / integrity event.
- Any regression caught after shipping rather than at the done-gate.
- Near-misses that revealed a real gap.

Issues caught at the done-gate or in normal review do **not** need
postmortems — that's the system working.

### Where it lives, and linkage

`docs/postmortems/YYYY-MM-DD-short-slug.md` (create the directory on
first use; use `/postmortem` if the domain ships it). Every postmortem
appends a ⚠️ entry to `tasks/AUDIT.md` linking the file, and
hotfix-driven postmortems also link the 🔥 entry that triggered them.

### Action items become tasks

A postmortem with no action items isn't done — it's a story. Real
postmortems end with concrete, owned, linked tasks. File them via
`/task` immediately after drafting.

## Orchestrator coordination notices (when mounted under an orchestrator)

When this task system runs inside an Element coordinated by a parent
orchestrator (per `CLAUDE.md`), the orchestrator may drop **read-only**
coordination signals into this project's `.claude/` as
`.claude/active-*.md` files (e.g. `active-migrations.md`).

- **Read each `active-*.md` on session start and at task start;** surface
  open entries in your orientation. Migrations open and close mid-task —
  don't trust one early read.
- **Treat as authoritative** for cross-Element state. To update state,
  go back to the orchestrator — don't edit these files by hand or delete
  them; they're auto-managed.
- **Don't propagate** orchestrator state into local task specs or
  `CLAUDE.md`. Reference, don't copy.

If `CLAUDE.md` declares no orchestrator (solo project), this section
doesn't apply; any `active-*.md` that appears is stale — flag it, don't
read it.

## Honest reporting

- If acceptance criteria can't all be met, the task is **not done.**
  Mark unchecked criteria, write a blocker, report it.
- If you discover the task's premise is wrong, stop and write a blocker.
  Do not silently redesign the work.
- Never mark a checklist item complete that you didn't actually verify.
- "Verified" means you ran the done-gate and saw it pass — not "it looks
  like it should pass."

## Domain extensions

The portable core above is everything that is true of task management in
*any* domain. A domain that needs more — stack-specific verification
steps, additional gated artifacts, extra categories, naming overrides —
adds a `.claude/<domain>-task-rules.md` extension file and points to it
from `CLAUDE.md`. Read this file first, then the extension that matches
the work at hand. The extension *adds to* and *refines* this file; it
does not replace the lifecycle, the categories, or the done-gate
contract.

Examples of what belongs in an extension, not here:

- **Software (`code-task-rules.md`):** branch/PR conventions, the exact
  build/test commands, the `task-guard` pre-commit hook, schema-mirror
  discipline, platform sub-extensions (`ios-`, `web-`).
- **Legal (`legal-task-rules.md`):** matter-number id conventions,
  conflict-check gates, privilege handling, filing deadlines as
  done-gate items.
- **Health (`health-task-rules.md`):** clinical-rule validation gates,
  PHI handling, compliance sign-off as a done-gate item.

Whatever the domain, the lifecycle and the discipline are the same. Only
the done-gate and the extension change.
