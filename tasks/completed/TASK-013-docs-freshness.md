---
id: TASK-013
category: bug
status: completed
---

# TASK-013: Docs + handoff freshness (review findings H3, M4/M5/M6, L1/L2/L3)

Docs written before HOTFIX-001 / before the worktree advanced still describe a
pre-artifact-lane, pre-a5f6ff1 world. The delivered handoff copy actively
misleads the frontend team.

## What's broken

- **H3 (HIGH):** FRONTEND_RASAOS_GAPS.md F1 tells the team to BUILD HtmlEmbed —
  which already ships at a5f6ff1 (our own canon draft says "F1 done"). Rewrite
  F1 to "shell half DONE @ a5f6ff1; remaining = rendered-set docs +
  _contract.py/COMPONENTS when the kernel enum (K1) lands; confirm the CSP/
  height deltas." Re-deliver the copy in the frontend repo.
- **M4:** ui-engine-and-architecture.md §1 table + §2 rejected-alt still say
  artifacts "absent in shell" two sections above the "LIVE" banner. Correct
  the stale cells.
- **M5:** html-embed-spec.md §A is now-false present-tense claims ("shell has
  NO artifact path / NO CSP") under a global "superseded" banner — inline-mark
  the individual bullets.
- **M6:** BUILD_ORDER.md lists shipped work (items 1,2,4,5,6) as pending;
  mark done with versions, update 7/8.
- **L1:** binding-model.md header still says "no HTML-artifact rendering path".
- **L2:** stale components.tsx line numbers in F1/F2/ui-engine §A2 (HtmlEmbed
  shifted them) — re-cite @ a5f6ff1 or drop pending the F3 manifest.
- **L3:** "verified against kernel v0.27.0" → re-confirmed @ v0.32.0 (substance
  holds).

## Scope

In: docs/handoff/FRONTEND_RASAOS_GAPS.md, docs/design/{ui-engine-and-architecture,
html-embed-spec,binding-model,BUILD_ORDER}.md, content/KERNEL_ASKS.md +
binding-model §A8 (version labels). Re-deliver the frontend handoff copy.
Docs-only — no runtime behavior change.

## Acceptance

- [x] F1 describes the shell half as DONE; delivered copy re-synced.
- [x] No design doc contains an un-annotated "artifacts absent in shell" claim.
- [x] BUILD_ORDER reflects shipped vs open accurately.
- [x] Version labels current (kernel v0.32.0; module-tasks 0.1.3).

## Artifacts

- docs/handoff/FRONTEND_RASAOS_GAPS.md (+ the delivered copy in frontend-rasaos),
  docs/design/{ui-engine-and-architecture,html-embed-spec,binding-model,BUILD_ORDER}.md,
  content/KERNEL_ASKS.md
