---
id: TASK-009
category: bug
status: completed
---

# TASK-009: check-app tracebacks on parseable-but-wrong-typed JSON

## Steps to reproduce

```
cp -r examples/orders-desk /tmp/x
echo '["not an object"]' > /tmp/x/context.json
python3 bin/check-app /tmp/x
```

## Expected vs actual

- **Expected:** a clean `FAIL context.json: not a JSON object` and `RED` exit 1.
- **Actual:** `Traceback (most recent call last): AttributeError: 'list'
  object has no attribute 'get'` — an unhandled exception. The same happens
  for a non-object `app.json`, and for a binding whose `source` is a string.

## Root cause

`load_json` catches JSON *parse* errors but returns whatever parsed —
including a list/str/number. Three reachable sites then call `.get()` on the
parsed value without an `isinstance(..., dict)` guard: `check_context` (the
context doc), `main()` (the manifest `m`), and `check_bindings` (a binding's
`source`). A wrong top-level/nested type throws instead of failing cleanly.
`check-app` is the publish gate — it must FAIL, never crash.

> Found in the Phase-1 review pass (adversarial probe H). Same defect *class*
> exists pre-Phase-1 in field-level access, but deep per-field type
> robustness is the published schema's job (kernel-side, KERNEL_ASKS #10);
> this task closes only the reachable top-level/source **crash** surface.

## Scope

**In scope:** guard the three reachable sites so a parseable-but-wrong-typed
value produces a clean `FAIL`, never a traceback. Verify by re-running the
probes. Patch bump 0.10.1.

**Out of scope:** field-by-field type validation (schema's job); the golden's
dangling data path (separate review finding); strengthening check-doctrine's
fixture gate to detect tracebacks (recommended follow-up, noted below).

## Artifacts expected to change

- `bin/check-app` (three `isinstance` guards)
- `VERSION` + `rasa.json#version` + `CHANGELOG.md` (0.10.1)

## Acceptance criteria

- [x] A non-object `context.json` → clean `FAIL context.json: not a JSON
      object`, exit 1, NO traceback.
- [x] A non-object `app.json` → clean `FAIL app.json: not a JSON object`,
      exit 1, NO traceback.
- [x] A binding `source` that is not an object → clean `FAIL … source must be
      an object`, exit 1, NO traceback.
- [x] Golden still GREEN; all five fixtures still RED; check-doctrine GREEN.

## Verification plan (per the done-gate)

1. **Setup:** temp copies of the golden with each malformed shape.
2. **Checks:** each acceptance case → run check-app, confirm clean FAIL +
   `echo $?` = 1 + no "Traceback" in output.
3. **Done-gate run:** all gates.

## Gotchas & learned lessons

- **A crashing fixture reads as GREEN to check-doctrine** — its fixture gate
  only checks `returncode != 0`, and a traceback also exits non-zero. So a
  malformed-input fixture would NOT regression-guard the "no traceback"
  property. Verify by asserting no "Traceback" in output, not by a fixture.
  (Strengthening the fixture gate to catch tracebacks is the recommended
  follow-up, left out of scope here.)

## Blocker notes

(empty)

## Self-review checklist

- [x] I followed the execution order in the spec.
- [x] Every acceptance criterion is met and individually verified.
- [x] I verified each step, not just the end state.
- [x] The done-gate passes (every gate in `.claude/done-gate.md`).
- [x] I didn't touch artifacts outside "Artifacts expected to change".

### Dependencies

- **Blocks / blocked by:** blocks the release (0.10.x → main); found in review.

---

**Definition of done** (per `.claude/task-rules.md`): all criteria verified ·
plan ran with evidence · done-gate passes · closing report posted.
