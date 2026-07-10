# Roadmap

This is the **sole phase registry** for the project. Every task that
belongs to a phase is listed here, under that phase, and nowhere else —
tasks never declare their phase in their own spec file (that would
drift). The invariant: *in `ROADMAP.md` ⟺ has a phase ⟺ triaged.* Tasks
parked in `tasks/triage/` are deliberately unphased and do **not** appear
here until they graduate.

---

## Phase 1: The binding brain — design → doctrine

Fold the ratified design corpus (`docs/design/binding-model.md`,
`ui-engine-and-architecture.md`, `html-embed-spec.md`, per
`BUILD_ORDER.md`) into this element's law: ship the verified truth-pass,
finish the SA-023 domain identity, then build the context index, the
binding registry, and the three-modes doctrine — with every step gated by
`check-doctrine` and honest to what the platform actually renders. In
scope: this element's `content/`, `schemas/`, `bin/`, `examples/`,
`rasa.json`, and the coordination surfaces (canon task drafts, team
handoffs). Out of scope: kernel/shell implementation (external handoffs
K1–K3 / F1–F6), `module.sessions`, full doc-10 11-step validator parity,
and the full-workspace profile. Success: a fresh runtime session reads
`content/` and can audit a tenant, declare bindings, and build bound
screens cold — with the design docs and the doctrine agreeing everywhere.

- TASK-001 — Ship the truth-pass + design corpus + task system as v0.6.0
- TASK-002 — Finish the SA-023 re-role (domain identity, rasa.json prose, contract_version)
- TASK-003 — The context index: `context.json` schema + the AUDIT procedure
- TASK-004 — The binding registry: `bindings[]` + `writes[]` contract + enforcement
- TASK-005 — The three-modes doctrine fold (bound / derived / provision)
- TASK-006 — Reconcile `.rasaos/` vs canon `.rasa/` (decide + migrate or file upstream)
- TASK-007 — Draft the canon amendments (html-embed FE-022; track SA-026/027/028; provides.collections[])
- TASK-008 — Relay + track the external handoffs (kernel K1–K3, frontend F1–F6)
- TASK-009 — Bug: check-app tracebacks on wrong-typed JSON (fail cleanly) [review pass]
