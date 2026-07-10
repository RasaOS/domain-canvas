---
id: TASK-010
category: bug
status: completed
---

# TASK-010: Harden check-app (enforcement review findings)

Closes review findings E1(completion)/E2/E3/E4/E7/E8 + D9 + the E6 traversal
guard (user-approved). The gate's happy-path logic is sound; its edges leak.

## What's broken

- **E1 (crash, completion of TASK-009):** 4+ sites still traceback on
  wrong-typed JSON (region-as-string, screen-file-array, non-iterable
  buttons/events, props-as-list). Need a `try/except` backstop in `main()`
  so the gate can NEVER traceback, plus inner guards for good messages.
- **E2:** a `writes[]` against a `read` binding is accepted (should FAIL).
- **E3:** an intent-less button emits `on_click` the checker never records →
  unregistered event slips the gate.
- **E4:** `rasa.emit(\`backtick\`)` inside artifacts is invisible to the scan.
- **E7:** stray recognized-but-uncounted keys in `source` pass silently.
- **E8:** malformed-present context.json yields a misleading "absent" message.
- **D9:** `mode:"provision"` bindings must carry `provisioned:true` — unenforced.
- **E6 (user-approved):** binding/data paths can escape `_tenant_root`
  (`../../../../etc/passwd`) despite the schema forbidding it — enforce the
  escape check (NOT existence; provision creates files).

## Scope

In: `bin/check-app` only. Out: running the JSON schemas (jsonschema dep —
deferred per user; instead mirror the writes `oneOf` in code + soften the
"contract"/"lockstep" claims in TASK-011); path EXISTENCE.

## Acceptance

- [x] The 4 residual crash shapes → clean FAIL, exit 1, no traceback.
- [x] write→read-only binding FAILs; intent-less button FAILs (unregistered
      on_click); backtick emit is seen; stray source key FAILs;
      mode:provision w/o provisioned:true FAILs; path escaping _tenant_root
      FAILs; `{binding,op,state}` writes entry FAILs (oneOf mirror).
- [x] Golden GREEN; 5 fixtures RED; check-doctrine GREEN.

## Artifacts

- `bin/check-app`

## Verification

Re-run the review probes (scratchpad) + the golden/fixtures/gate.
