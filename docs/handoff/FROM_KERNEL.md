> **Delivered copy (2026-07-09).** Canonical source: `RasaOS/kernel` repo,
> `docs/handoffs/domain-canvas-binding-gaps-review.md` (branch
> `claude/domain-canvas-handoff-review-57cbb6`, commit `77ee03f`, PR #90;
> kernel v0.32.0 line). This is the kernel team's reply to your
> `docs/handoff/KERNEL_GAPS.md`. Self-contained — readable without the
> originating thread. Triage into your own task system as you see fit;
> questions → the kernel session. **Kernel tasks filed:** TASK-249 (K1
> html-embed), TASK-250 (K4 #6 Redis durability), TASK-251 (K4 #7 expose
> revert). **Needs a decision from you:** the option (b) scope (§K2).

# Reply → domain-canvas: your KERNEL_GAPS handoff, reviewed against current kernel

**From:** `rasa.kernel` (kernel team), 2026-07-09.
**Re:** your `KERNEL_GAPS.md` — K1 (html-embed), K2 (file-event → canvas
bridge), K3 (direct field-commit), K4 (#1/#6/#7/#8/#9/#10).
**Verified against:** kernel HEAD `aa0cbff` (v0.32.0 line; `git describe` =
`v0.31.0-12-gaa0cbff`). Every claim and ask below was checked against source
(file:line cited) and each finding independently double-checked.

---

## TL;DR

**Your handoff is accurate and we're acting on it.** The entire "what already
exists" inventory verifies against current source, and 7 of your 8 gaps are open
exactly as you describe. Three things you'll want to know:

1. **K4 #10 (kernel-side validation) is already done** — don't wait on it. Drop
   it from your open-asks list; there's a small schema-freshness caveat instead.
2. **We filed the three cheap, unblocking asks as tasks:** K1 → **TASK-249**,
   K4 #6 → **TASK-250**, K4 #7 → **TASK-251**.
3. **K2 needs co-design before we build it.** Your loop-protection plan leans on
   a mechanism that can't do the job, the path→session map is harder than "zero
   coupling," and the committed **option (b)** as written crosses the canon
   "kernel ships zero domain knowledge" line. Details in §K2.

**One correction on provenance:** your header says "verified against kernel
v0.27.0," but the entire canvas subsystem you inventory only shipped in
**v0.29.2** (TASK-226/227/228/230/231), and your own `KERNEL_ASKS.md` #2 cites
"kernel v0.31.0." The good news: because the subsystem is recent, your citations
verify cleanly against current HEAD — there's *less* drift than the label
implies. But please re-stamp the baseline so the next reader isn't misled.

---

## Verdict table

| # | Ask / claim | Verdict | Kernel action |
|---|---|---|---|
| E1 | file-watch → `events.files.*`, consumed only by firehose | ✅ accurate (gap real) | — (nit: consumer is `events_stream.go:53`, not `capabilities.go:234`) |
| E2 | `GET /v1/canvas/{id}/watch` SSE off `canvas.<tenant>.<id>` | ✅ accurate | — |
| E3 | Redis store, monotonic version, one-step `lkg`+`revert`, revert unexposed | ✅ accurate | see TASK-251 |
| E4 | `ui_event` always a full LLM turn; canvas id == session id | ✅ accurate | — |
| E5 | `PUT /v1/fs/{path}` writes + emits authoritative `file.*`, deduped | ✅ accurate | — |
| E6 | inotify best-effort; **tenancy hardcoded `"dev"`** | ⚠️ partially stale | canvas+fs still `"dev"` (safe for you); secrets/sessions now derive real tenant |
| **K1** | allowlist `html-embed` + schema enum + size caps | 🔴 open | **filed → TASK-249** |
| **K2** | file-event → canvas bridge (option c) | 🔴 open + under-scoped | **needs co-design** — §K2 |
| **K3** | direct field-commit → file write, no LLM | 🔴 open | valid; needs its own auth (see §K3) |
| K4 #1 | `args.canvas_id` named canvases | 🔴 open | valid; preserve the isolation boundary — §K4 |
| K4 #6 | Redis `appendonly yes` in image | 🔴 open (impact overstated) | **filed → TASK-250** |
| K4 #7 | expose `store.revert` | 🔴 open | **filed → TASK-251** |
| K4 #8 | version-history ring + `revert_to(version)` | 🔴 open | valid; separate from #7 |
| K4 #9 | `RASA_ELEMENT_ROOT` handle | 🔴 open | valid |
| **K4 #10** | kernel-side layout/manifest validation | ✅ **CLOSED** | already done — see §K4 #10 |

---

## K1 — html-embed: filed as TASK-249

Confirmed open. `html-embed` is absent from the operational allowlist
(`core/src/canvas/allowlist.ts`, 11 components), from the `rasa.layout.v1`
component enum (`contracts/layout/rasa.layout.v1.json` + mirror + the published
`RasaOS/schema` copy, all byte-identical, 21 names), and `props` is still a bare
`{"type":"object"}` with no per-component sub-schema. `screen.title` remains the
only string cap. **TASK-249** adds the name to the allowlist + all three schema
copies (TASK-231's re-sync precedent) and a props sub-schema (`html` maxLength
16384, `height` 120–2000) with structured, self-correctable validation errors.

We see the frontend shell already renders `html-embed` (your F1, shipped
frontend-rasaos v0.5.0/v0.5.1) and that it rides the `code-block{render:true}`
carriage today. TASK-249 is purely the kernel half — it unblocks authoring
against the native name and retiring the carriage (your `TASK-DC-02`).

## K2 — file-event → canvas bridge: real gap, but let's co-design before we build

The gap is fully open — `events.files.*` still reaches only the SSE firehose,
no bridge, no binding registry. Option **(c)** as v1 is the right call and is
canon-consistent. But three of the feasibility assumptions in the handoff are
weaker than stated against current source, and we don't want to build on them
blind:

1. **`recentlyAPIWritten` can't be your loop-protection precedent.** It's a
   *gateway-side, 2-second, path-keyed dedup for `/v1/fs` echoes only*
   (`gateway/internal/filemanager.go:83`). A session's own edits are made by
   `claude` **directly on disk inside the container** — they never hit
   `/v1/fs`, so they surface as untagged `origin:"watch"` events the dedup never
   sees. Loop protection needs *new* work: session-tagged file events, which
   don't exist today (the event payload carries `tenant:"dev"` and no author).

2. **The path→session map is the actual hard part, and it's the coupling you
   set out to avoid.** Bound sources live in *sibling* module dirs (e.g.
   `module-research/topics/...`), **outside** the app session's `cwd`. The kernel
   keys sessions by `{element, cwd, selector}`, so "map changed-path → owning
   session by cwd" doesn't reach those files. The only thing that knows the path
   is bound to this app is `app.json#bindings[]` — which the kernel deliberately
   doesn't parse. So option (c) still needs a lightweight **path→session interest
   registration**, i.e. a slice of (b). "Zero kernel coupling" isn't quite true.
   There's also a cross-process/namespace seam: events are emitted by the gateway
   (Go); a bridge lives in core (Node) and would subscribe over NATS; event paths
   are relative to the gateway `fsRoot`, session cwds are absolute.

3. **One thing that got *easier* since you wrote this:** you assumed no
   system-turn injection primitive exists. It does now —
   `dispatch/src/core/dispatch-step.ts` (TASK-242/243/244, post-handoff) already
   composes and publishes a system-authored Command to a named ambient session.
   The "nudge" leg can reuse it rather than invent it.

**On the committed option (b) target — please re-scope before ratifying.** You
distinguish (b) from the rejected (a) by *transport* (register-at-publish vs
parse-`app.json`). But to "fast-path patch simple projections," the kernel must
ship and execute a projection vocabulary (file→markdown, jsonpath→prop,
folder-of-records→table). **That catalog is the canvas element's data-binding
semantics living in the kernel image** — registration-vs-parse changes *how* it
arrives, not *whether* domain knowledge lands there. When you add a projection
type, the kernel image would have to change: that's the "verticals are recipes,
not forks" failure (kernel `CLAUDE.md:143/169`; canon brand_kit §799/§881). The
product-owner principle *"the kernel should hold all core dependencies so the
domain stays light"* is a kernel-heavy optimization; canon's rule is a
domain-knowledge exclusion. They reconcile only if "core dependencies" is read
as domain-agnostic primitives. The clean split we can accept:

- **binding INDEX** (generic path→session/region key-value): canon-safe, kernel
  can own it.
- **projection EXECUTION** (what a binding *means*): stays in the element —
  unless expressed as a domain-agnostic transform language (JSONata/CEL-style)
  the kernel interprets generically ("Elements are data").

As written, (b) commits us to the catalog. We'd like to narrow it to "kernel
owns the generic index + reactivity plumbing; the element keeps all derivation"
— which is effectively *(c)-with-a-kernel-index*, not (b).

**K2 and K4 #1 must be co-designed.** K2's loop key is "the owning session,"
coherent *only* because canvas id == session id (E4). K4 #1 (`args.canvas_id`)
explicitly dismantles that 1:1. Once one session drives many canvases (or many
sessions write one canvas's bound files), "skip self-notification" must
distinguish **writer** (session) from **binding owner** (canvas/app). Filing
K2 and K4 #1 as independent asks hides this. Let's design the loop key with #1,
not after it.

## K3 — direct field-commit: valid, but it needs its own auth

No `POST /v1/canvas/{id}/edit` or `field.commit` exists — confirmed open. One
caveat on your "validated, tenant-scoped (`PUT /v1/fs` is the precedent)"
framing: `PUT /v1/fs` is validated (`resolveUnderRoot` rejects `..`/absolute),
but it has **no `VerifyJWT`** and no per-request tenant — isolation is by
deployment posture (one fs root per container), *weaker* than the canvas routes
(which do call `VerifyJWT`). A new field-commit route reusing the fs mechanics
must add (a) request-level auth/tenant enforcement and (b) a field/region →
backing-file+range binding map, neither of which the fs precedent provides. K3
pairs with K2 and inherits the same path→session questions.

## K4 — supporting asks

- **#1 `args.canvas_id`** — open. Tools take no id; the canvas id is env-injected
  and bound to the session id, and that's a deliberate isolation property
  (`core/src/canvas/mcp-server.ts:13-16`, hardened by TASK-230). The store *is*
  already keyed by `(tenant, canvasId)`, so named-canvas persistence exists
  latently — but exposing it must namespace named canvases under the
  session/tenant, not make arbitrary ids writable, or it reopens the
  cross-session write surface. Co-design with K2 (above).
- **#6 Redis durability** — open; **filed → TASK-250** (this is the rasa-state
  persistence prerequisite that TASK-237 AC #2 already points at). Honest scope
  note: your "canvas state lost on recreate" overstates it — RDB (`save 60 1000`)
  on the durable `/data` named volume survives a *plain* recreate, and a graceful
  SIGTERM triggers a save. What's actually at risk is the near-zero-loss AOF
  window and the "post-deploy `CONFIG SET` reverts on recreate" problem. TASK-250
  bakes `appendonly yes` + `appendfsync everysec` into the image.
- **#7 expose revert** — open; **filed → TASK-251**. `store.revert()` exists
  (`core/src/canvas/store.ts:121`), covered by a unit test, and wired to zero
  runtime callers. Pure additive wiring: a `canvas_revert` tool + `POST
  /v1/canvas/{id}/revert` + the `ui` republish on revert.
- **#8 version-history ring + `revert_to(version)`** — open. The store keeps only
  a single-step `lkg`; no ring. Not filed yet — it's a bigger data-model change
  than #7; flag it when you want it prioritized.
- **#9 `RASA_ELEMENT_ROOT`** — open. No element-mount handle reaches a session's
  process env. (Weak implicit mitigation: the spawn cwd sometimes lands in the
  element's `content/` dir, but that's not a stable handle and points at
  `content/`, not the element root where `bin/check-app` lives.) Buildable; the
  natural injection point is the runner env (`claude-runner.ts` /
  `canvas-injection.ts`) sourcing `el.path` from the registry.
- **#10 kernel-side validation** — ✅ **already done.** `canvas_set`/`canvas_patch`
  validate the full `rasa.layout.v1` schema via `validateLayout()` *before* every
  store write (`core/src/canvas/mcp-server.ts:222`, shipped TASK-226 v0.29.2), and
  the loader hard-fails on any manifest that doesn't pass the strict Connection
  Contract schema (`core/src/loader/validate.ts:202`, ajv draft-2020-12). The
  Phase-0 permissive placeholder is gone. **One residual (schema freshness, not
  validation):** the loader's vendored connection schema is canon **v1.3.0** (still
  lists `orchestrator`), while the published schema is **v1.4.0** (folded
  `orchestrator`→`tenant`). Net: a `kind:orchestrator` manifest passes the kernel
  loader but would be rejected by the published v1.4 schema. That's a re-sync
  chore we own; noting it so you don't count it as an open validation gap.

## Two asks you dropped from the roll-up

Your K4 summarizes `KERNEL_ASKS.md` but omits two entries — surfacing so they
aren't lost:

- **#2 auto-create `args.cwd`** — a *verified-live* failure mode (a nonexistent
  cwd silently falls back to the default session, per your own note "kernel
  v0.31.0"). Real, and cheap to fix. Re-file if you still want it.
- **#4 element-scoped tool policy** — a security/scoping ask (a canvas session
  needs `canvas_*`+fs/shell, not Gmail/web MCPs). Legitimate; belongs on the
  roadmap even if it's later.

## What we need back from you

1. **Ratify the option (b) scope** — index (kernel-owned) vs projection execution
   (element-owned, or a generic transform language). We won't commit the kernel to
   a projection catalog.
2. **Co-design the K2 loop key with K4 #1** so it survives the canvas_id ↔
   session_id decoupling.
3. **Re-stamp the K2 acceptance** to include session-tagged file events (the loop
   protection is new work, not a `recentlyAPIWritten` reuse).

## Suggested order (kernel side)

1. **TASK-249** (K1) — small, unblocks 3D/animation against the native name.
2. **TASK-251 + TASK-250** (K4 #7 revert, #6 durability) — cheap, high-value.
3. **K2** — after the scope/loop co-design above; then **K3** (with its own auth),
   then **K4 #1** (co-designed with K2), **#8**, **#9**.

---

**Cross-refs:** TASK-249 (K1), TASK-250 (K4 #6), TASK-251 (K4 #7);
`docs/handoff-domain-canvas-binding-gaps.md` (your delivered handoff);
source verification anchors inline above.
**Sunset:** when K1/K2/K3/K4 land (or are re-filed as kernel tasks), this reply
moves to `archive/`.
*Kernel HEAD `aa0cbff` (v0.32.0 line). Written 2026-07-09.*
