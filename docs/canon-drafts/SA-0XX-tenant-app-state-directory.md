---
id: SA-0XX (canon session assigns)
status: draft — authored in elements/domain-canvas (TASK-006), to be filed to canon/tasks/triage/
target_version: 1.5.0 (proposed)
target_docs:
  - 01_system_specification.html (Part X — tenant directory layout, alongside §53 SA-019)
  - elements/ELEMENT_CONTRACT.md (§8 mount/state surfaces, if adopted)
filed_by: rasa.domain.canvas session 2026-07-09 (TASK-006 dot-dir reconciliation)
---

# SA-0XX: Where does tenant app-state live — `.rasa/` or a runtime dot-dir?

## The question

Two hidden directory conventions now coexist in a tenant:

- **`.rasa/`** — canon's hidden dir (SA-019): `holding/<name>/` working copies
  for the install/promote sync mechanic. Install-time machinery.
- **`.rasaos/`** — a runtime convention (not in canon): `apps/<app-id>/` holds
  canvas-app instances (`app.json`, `screens/`, `state/`, `context.json`) —
  the per-app persistent store AND the session key (the kernel keys the app's
  session by this cwd; frontend-rasaos `VerticalCanvasPane` bootstraps it,
  verified @ `a5f6ff1`).

Should tenant app-state fold under canon's `.rasa/` (e.g. `.rasa/apps/`), or
does runtime surface-state deserve its own namespace (ratify `.rasaos/` — or
another name — as the runtime dot-dir)?

## Why it's worth a canon answer

- One tenant, two hidden roots is un-taught structure: every audit/tooling
  path check must know both, and nothing in canon says which is authoritative
  for what.
- The naming is **platform-owned in practice** — the kernel resolves the cwd,
  the shell bootstraps the directory. Per the kernel-heavy/domain-light
  principle, elements should not unilaterally pick platform-level names.
- Deciding is cheap NOW (no production tenants); every shipped tenant makes a
  migration more expensive.

## Considerations for the decision

- **For `.rasa/apps/`:** one hidden root; SA-019's dir gains a natural
  sibling (`holding/` = install-time, `apps/` = runtime); no new vocabulary.
- **For a separate runtime dir:** `.rasa/` is currently pure install
  machinery (safe to wipe/rebuild from remotes); app-state is **tenant working
  data** (survives everything, backed up). Mixing lifecycles in one root
  muddies "what is disposable."
- **Migration cost if `.rasa/apps/` wins:** frontend-rasaos
  `VerticalCanvasPane` cwd bootstrap + domain-canvas doctrine/schema paths +
  any kernel docs — one coordinated pass, trivial while tenants are dev-only.

## Interim posture (already in effect)

domain-canvas doctrine keeps `.rasaos/apps/` (matching the live shell) and
records the tension in its design docs. Whatever canon decides, the element
migrates in one pass with the frontend.
