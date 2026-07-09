# Done-Gate — rasa.domain.canvas

**This file is project-owned** (seeded by `rasa.module.tasks`, filled by this
domain). A task leaves `active/` for `completed/` only when **both** hold:

1. every acceptance criterion in the task spec is met and verified, and
2. **every gate below passes.**

Each gate is objectively checkable. Never bypass a gate to ship faster.

---

## Gates

- [ ] **Acceptance criteria** — every checklist item in the task spec is
      satisfied and individually verified (not assumed).
- [ ] **`bin/check-doctrine` exits 0 (GREEN)** — the element's own machine gate:
      seven-process lockstep, COMPONENTS.md ↔ `bin/_contract.py` component
      lockstep, version plumbing (VERSION == rasa.json == newest CHANGELOG),
      schema parses, BUILDER terseness, golden example passes `check-app`, all
      negative fixtures fail. This is also the pre-commit hook
      (`git config core.hooksPath .githooks`) and CI.
- [ ] **Doctrine-truth rule** — any claim added to `content/` about what the
      shell, kernel, or canon DOES carries verified evidence (a date + a
      source file:line or doc anchor). No capability is documented as working
      that has not been seen working. *(This gate exists because the element
      shipped an artifact contract the renderer never implemented — found
      2026-07-09.)*
- [ ] **Design-doc consistency** — if the task changed `content/`, `schemas/`,
      or `bin/`, the design corpus (`docs/design/*.md`, `BUILD_ORDER.md`) is
      updated in the same commit; the docs never lag the law.
- [ ] **Ship shape (version-bearing tasks only)** — VERSION + `rasa.json#version`
      + CHANGELOG entry land in the same commit (workspace convention).
- [ ] **Gated-file review** — changes to `CLAUDE.md`, `.claude/task-rules.md`,
      `.claude/done-gate.md`, `.claude/task-templates/`, `.claude/skills/`, or
      `bin/check-doctrine`'s process canon get explicit user (Chazz) approval
      before the task closes.

---

## Enforcement note

"Every change is task-linked" (task-rules → change-audit rule) applies to this
element's shipped artifacts: `content/`, `schemas/`, `bin/`, `examples/`,
`rasa.json`. Enforcement today: the pre-commit hook runs `check-doctrine`
(mechanical half), and closing reports cite the task id (audit half). A
`task-guard` style commit hook is a possible future addition — not wired yet.
Documentation (`docs/`), the task files themselves, and `.claude/` meta need
no task.
