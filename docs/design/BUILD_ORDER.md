# BUILD_ORDER — the merged plan (binding-model + ui-engine specs)

One dependency-ordered plan across `binding-model.md` and
`ui-engine-and-architecture.md` (design review #24 asked for exactly one).
Updated 2026-07-09.

## Done (2026-07-09 — the truth-pass)

- ✅ `COMPONENTS.md` rewritten to the verified shell prop shapes + emission grammar;
  §artifact → §custom-visuals (status honest: not renderable; path = html-embed).
- ✅ `BUILDER.md` / `APP_MODEL.md` / `CLAUDE.md` artifact + nav-`intent` corrections.
- ✅ `KERNEL_ASKS.md`: ask #3 rewritten (false claim corrected); asks #11 + #12 filed.
- ✅ `bin/check-app`: emission grammar corrected (intent‖on_click · on_submit ·
  on_card_click · region on_click); nav targets from `intent`; intent-less buttons warn.
- ✅ Golden app fixed (`markdown`→`content`; intents added); unregistered-event fixture
  updated; `schemas/rasa.app.v1.schema.json#$id` → `domain-canvas`.
- ✅ Design docs corrected per review (~20 findings) + `html-embed-spec.md` authored.
- ✅ Handoffs authored: `docs/handoff/KERNEL_GAPS.md` + `docs/handoff/FRONTEND_RASAOS_GAPS.md`.

## Element work (this repo), in order

| # | Item | Blocked by |
|---|---|---|
| 1 | **Ship the truth-pass**: version bump (v0.6.0), CHANGELOG entry, commit (check-doctrine green) | nothing — next commit |
| 2 | **Step-0 re-role (SA-023)**: CLAUDE.md/README/CHANGELOG titles + rasa.json prose (`session_model` etc.) drop "orchestrator"; `contract_version` → 1.4.0 **coordinated with the workspace sweep** (OQ-5) | nothing; one clean commit |
| 3 | ~~**Decision gate**~~ ✅ **RESOLVED 2026-07-09**: OQ-1 = app store + the **kernel-heavy/domain-light principle** · OQ-4 = module-mediated writes first, direct fallback · OQ-7 = nudge-session v1, registered-bindings as committed target | — |
| 4 | **`context.json` + AUDIT process**: schema, the three-flavor structural detection, seam-first discovery, staleness rules; fold into PROCESSES/APP_MODEL; check-app additions | nothing — buildable now |
| 5 | **`bindings[]` contract**: schema additions (additive within v1), `writes[]` + the resolved executor rule, check-app checks (ids unique, module resolution, writes targets), golden `context.json` + binding, `binding-unknown-module` fixture (WITH context.json) | nothing — buildable now |
| 6 | **Three-modes doctrine fold** (bound/derived/provision) into BUILDER/PROCESSES | #4, #5 |
| 7 | **`.rasaos/` vs `.rasa/` reconciliation** — migrate or file as canon question | decision |
| 8 | **Canon tasks**: `DOC-10-edit-html-embed-escape-region` (FE-022); track SA-026/027/028; later `provides.collections[]` proposal (OQ-3b) | canon-workspace session |

## External work (handoffs — not this repo)

| Owner | Doc | Items |
|---|---|---|
| **kernel** | `docs/handoff/KERNEL_GAPS.md` | K1 html-embed kernel half · K2 file-event→canvas bridge (#11) · K3 direct edit→file (#12) · K4 supporting asks (canvas_id, durability, revert, history, mount handle, schema validation) |
| **frontend-rasaos** | `docs/handoff/FRONTEND_RASAOS_GAPS.md` | F1 html-embed component · F2 emission-grammar confirmation · F3 component manifest for lockstep · F4 CSS-var theme tokens · F5 doc-10 convergence (grids/nav) · F6 CSP cautions |

## Later / deferred

- `module.sessions` generalization (OQ-2 — after provision-then-bind proves out on
  module-research).
- Purpose-built declarative visual components (promote recurring html-embed patterns).
- check-app → full doc-10 11-step validator parity (prop-schema first — F3 feeds it).
- Full-workspace profile (ai-rail etc.) — only if we ever target it.
