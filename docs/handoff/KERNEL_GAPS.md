# Handoff → kernel team: gaps for canvas data-binding + the html-embed region

**From:** `rasa.domain.canvas` (elements/domain-canvas), 2026-07-09.
**Self-contained** — written to be read in a kernel session without the originating
conversation. Findings below were verified against **kernel v0.27.0 source** (file:line
cited); design context lives in domain-canvas `docs/design/{binding-model,
ui-engine-and-architecture,html-embed-spec}.md`.

**The product goal:** domain.canvas authors tenant-internal UIs (canvas layouts) **bound
to tenant/module files** — when a bound file changes (any writer), the canvas updates in
near-real-time; when the user interacts, files update. The kernel already has most of the
plumbing; three gaps remain.

## What already exists (verified — don't rebuild)

- **File-watch:** fsnotify watcher at boot — `gateway/internal/filewatch.go:36`
  (`StartFileWatcher`, wired `gateway/cmd/gateway/main.go:338`); walks root + subdirs,
  emits `file.created/modified/removed/renamed` → NATS `events.files.*`
  (`filemanager.go:378`, origin `"watch"`). Consumed ONLY by the SSE firehose
  (`capabilities.go:234`) — **wired to nothing on the canvas side**.
- **Per-canvas push:** `GET /v1/canvas/{id}/watch` (`canvas.go:202`) — SSE off NATS
  `canvas.<tenant>.<id>`; every `canvas_set` reaches the client instantly. Robust
  client-side (version dedup, gap re-snapshot).
- **Canvas store:** Redis `rasa:canvas:{tenant}:{id}` (`core/src/canvas/store.ts`),
  monotonic version, one-step `lkg` + `revert` (revert is **unexposed** — no tool/route).
- **ui_event round-trip:** POST `/v1/commands` `ui_event{}` → dispatcher →
  session (keyed `{element, cwd, selector}`, canvas id == session id) → model turn →
  `canvas_set` → publish (`commands.go:312`, `dispatcher.ts:214/459`,
  `mcp-main.ts:56`). Works, but ALWAYS a full LLM turn.
- **Direct file write:** `PUT /v1/fs/{path}` (`main.go:257`) writes + emits authoritative
  `file.*`, deduped vs the watcher (`recentlyAPIWritten`, `filewatch.go:124`).
- **Known limits (your own code documents):** inotify over the macOS Docker bind-mount is
  best-effort (`filewatch.go:20-25`); tenancy hardcoded `"dev"` (TASK-074).

## K1 — html-embed: the kernel half (SMALL)

Add `"html-embed"` to the canvas component allowlist (`canvas_set` currently rejects it)
and to the published `rasa.layout.v1` schema enum (RasaOS/schema; precedent: the 18→21
additions), with a props sub-schema: `html` (string, **maxLength ~16384**) + `height`
(integer, 120–2000). Size caps become schema-enforced (today only `screen.title` is
capped). The shell half (sandboxed iframe + CSP + bridge) is specced in domain-canvas
`docs/design/html-embed-spec.md` §B/§C and filed with frontend-rasaos.

**Acceptance:** `canvas_set` accepts an `html-embed` region; an oversized `html` prop is
rejected with a structured error the session can self-correct on.

## K2 — the file-event → canvas bridge (KERNEL_ASKS #11) — the big one

**Gap:** nothing routes `events.files.*` to a canvas. A bound file changed by another
session/cron/user is invisible until the next user interaction.

**Mechanism decision needed** (the binding registry lives in the app's `app.json`, which
the kernel does not parse):

| Option | How | Verdict |
|---|---|---|
| (a) kernel parses `app.json` | read the element-doctrine manifest | ❌ couples kernel to element doctrine; canon says kernel ships zero domain knowledge |
| (b) register bindings at publish | `canvas_set` (or a `/bindings` route) carries `{path → region, projection}`; bridge patches the region directly | fast (no LLM), but the kernel can only re-derive **trivial projections** (file→markdown content, jsonpath→prop); complex derivations (folder-of-records → table rows) still need the session |
| (c) **nudge the session** (recommended v1) | bridge maps changed path → owning session (its cwd/app scope), enqueues a system turn ("source changed: <path>"); the session re-derives + republishes via the normal write-order | ✅ works for EVERY binding shape, zero kernel coupling; latency = one model turn (seconds) |

**DECIDED (2026-07-09, domain.canvas + product owner):** ship **(c) as v1**; **(b) is the
committed target state**, not a maybe — the product owner set a standing principle ("the
kernel should hold all core dependencies so the domain stays light"), so the kernel
eventually owns the live binding index (registered at publish) and fast-path patches
simple projections, with complex derivations still routing via (c). Both reuse the
existing store + `canvas.<tenant>.<id>` publish — the client side needs nothing.

**Must-handle:** loop protection — the session's own writes must not re-trigger a nudge
(precedent: `recentlyAPIWritten`; suggest tagging events with the writing session and
skipping self-notifications) — and debounce (a burst of writes → one nudge).

**Acceptance (v1):** edit a bound file via `PUT /v1/fs` from OUTSIDE the app's session →
the app's canvas version bumps and the `/watch` stream delivers the update, with no user
action, within one turn's latency.

## K3 — direct edit → file write, no LLM turn (KERNEL_ASKS #12) (SMALL–MEDIUM)

For bound form fields / inline edits: `POST /v1/canvas/{id}/edit` (or a `field.commit`
command variant) that writes the target file directly (validated, tenant-scoped —
`PUT /v1/fs` is the precedent) and emits both `file.*` and `ui` events. Pairs with K2:
the write triggers the bridge → canvas refreshes. Together they close "user edits a bound
field → file updates → UI reflects" with no model in the loop.

**Acceptance:** a field commit updates the file, emits `file.*`, and (via K2) the canvas
reflects the new value — sub-second, no LLM turn.

## K4 — supporting asks already filed (see domain-canvas `content/KERNEL_ASKS.md`)

- **#1 `args.canvas_id`** — named canvases; unlocks true multi-page apps (screens ↔
  canvases 1:1; the app model is already shaped for it).
- **#6 Redis durability in the image** (`appendonly yes`) — container recreate currently
  reverts the post-deploy hardening.
- **#7 expose `store.revert`** (MCP tool + `POST /v1/canvas/{id}/revert`) — storage half
  already written, wired to nothing.
- **#8 bounded version-history ring** + `revert_to(version)`.
- **#9 stable element-mount handle** (e.g. `RASA_ELEMENT_ROOT`) — sessions must invoke
  their element's `bin/check-app` gate.
- **#10 kernel-side layout/manifest validation** adopting the published schemas.
- **Note:** ask #3's original claim ("the shell already renders html-embed sandboxed") was
  verified FALSE and has been corrected in KERNEL_ASKS — K1 above is the accurate kernel
  half.

## Suggested order

K1 (unblocks 3D/animation end-to-end once the shell lands its half) → K2 option (c)
(makes every binding live) → K3 (instant field edits) → K4 #7/#6 (undo + durability).
