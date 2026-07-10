---
id: TASK-011
category: bug
status: completed
---

# TASK-011: Doctrine correctness (CRITICAL + HIGH review findings)

Closes C1, H1, and D3/D4/D5/D6/D7/D8 — real contradictions inside the
doctrine that the gate can't see.

## What's broken

- **C1 (CRITICAL):** COMPONENTS.md line ~47 still says "render:true does
  nothing" (dead sentence from the v0.6.0 over-correction) while §artifact
  uses `render:true` as the LIVE carriage. Re-kills the artifact/3D lane for a
  top-down reader.
- **H1 (HIGH):** the write-order law is stated two incompatible ways —
  BUILDER/PROCESSES/CLAUDE/rasa.json say screen→app.json→canvas_set (PROCESSES
  even labels it "never reordered"); APP_MODEL + the real EVENT/provision
  steps write records/state FIRST. Unify every short-form site to the
  data-first law; kill "never reordered".
- **D3:** provision "best-fit writable collection" is undefined for 0/2 fits;
  "fits" has no operational meaning; the reference context has no collection a
  "goalkeeping session" fits, so the CHANGELOG "runs cold" over-promises.
  Define fits (record-field compatibility), handle 0 (offer closest / say so)
  and 2 (ask on-canvas, never silently pick).
- **D4:** a provisioned read-write binding needs a writer event — provision
  steps never say to add one → surprise RED. Add the step.
- **D5:** "check-doctrine keeps files in lockstep" over-claims; soften to what
  it checks AND extend check-doctrine to scan rasa.json for the 8 process
  names (closes D5+D6 cheaply).
- **D6:** rasa.json process list says 7 (missing AUDIT); make it 8.
- **D7:** BOOTSTRAP skeleton omits required manifest fields; point at
  APP_MODEL's full required set.
- **D8:** provision recipe triplicated + BUILDER carries schema detail
  (8KB budget) — keep the recipe in BUILDER §binding-modes, PROCESSES
  references it.

## Scope

In: content/{COMPONENTS,BUILDER,APP_MODEL,PROCESSES}.md, CLAUDE.md, rasa.json,
bin/check-doctrine. Order: fix rasa.json (add AUDIT) BEFORE tightening
check-doctrine, else RED.

## Acceptance

- [x] No doc says render:true "does nothing"; §artifact is the single source.
- [x] Every write-order statement is data-first (or points at APP_MODEL);
      "never reordered" removed. No file contradicts another.
- [x] rasa.json lists 8 processes incl. AUDIT; check-doctrine asserts the 8
      appear in rasa.json too; GREEN.
- [x] Provision doctrine handles 0/2 fits + the writer-event step; CHANGELOG
      "runs cold" claim reconciled (softened or backed by a fitting collection).
- [x] BUILDER still < 8KB; check-doctrine GREEN.

## Artifacts

- content/{COMPONENTS,BUILDER,APP_MODEL,PROCESSES}.md, CLAUDE.md ⚠ gated,
  rasa.json, bin/check-doctrine, CHANGELOG.md (the "runs cold" line)
