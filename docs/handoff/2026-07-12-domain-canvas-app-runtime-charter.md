# Handoff → domain-canvas: the app-runtime charter (SA-035)

**From:** `rasa.frontend.rasaos`, 2026-07-12.
**Read first:** [`2026-07-12-app-runtime-sync-contract.md`](2026-07-12-app-runtime-sync-contract.md)
(shared frame + sequencing + ownership). This doc is the build-time half.
**Companion:** [`2026-07-12-kernel-app-runtime-charter.md`](https://github.com/RasaOS/frontend-rasaos/blob/main/docs/handoff/2026-07-12-kernel-app-runtime-charter.md).
**Extends:** [`2026-07-12-model-a-viewport-is-a-website.md`](https://github.com/RasaOS/frontend-rasaos/blob/main/docs/handoff/2026-07-12-model-a-viewport-is-a-website.md)
— that handoff is the **immediate** doctrine work (persist-without-render, `fill:true`,
client-side authoring) and holds value **even if the runtime never ships.** This doc
is the **forward view**: how your doctrine shifts once SA-035's server tier exists.

All file:line refs below are on your **canonical line** — see §0, this is load-bearing.

---

## 0. FIRST: land TASK-011 — everyone is reading the wrong doctrine

Your canonical doctrine is **v0.11.0 on `claude/core-internal-structure-12c464`**
(the task-tracked line: binding registry `bindings[]`/`writes[]`, three binding
modes, the eight-process canon, hardened `bin/check-app`). The branch **and tags
v0.6.0–v0.11.0 are pushed to `origin`** — but the line is **not merged into `main`.**
`origin/main` and `canvas-doctrine-reconcile` are **stale at v0.5.3**.

Consequence: the kernel team, canon authors, and we all read pushed `main` to "see
how the builder works" — and get the **wrong (v0.5.x) doctrine**, which predates the
binding registry and the eight-process canon. **TASK-011**
(`tasks/backlog/TASK-011-reconcile-main-line-and-push.md`) — its remaining work is
the **merge into `main`** (the branch backup is already done) — **blocks the entire
app-runtime effort** (sync contract §3, step ①).

While you're at it, **consolidate the scattered inbound handoffs onto the canonical
line**: `FROM_FRONTEND_RASAOS` (untracked on the main worktree), `FROM_KERNEL` (only
on `claude/deliver-kernel-gaps-reply`), and the two 2026-07-12 frontend handoffs
(model-a + this one) live only in the frontend repo. Pull all onto v0.11.0.

---

## 1. The shift: the AI stops being the run-time backend

Today your doctrine is explicit that **you are the backend**: "You are also the
app's backend. `ui_event` turns arrive in this session; handle them by the EVENT
process" (`content/BUILDER.md:46-47`). Every routine emit re-authors the screen file
and re-publishes via `canvas_set` (`content/PROCESSES.md:83-97`, EVENT §3 `:95-96`;
the write-order law's terminal step, `content/APP_MODEL.md:133`).

SA-035 moves you from **run-time backend** to **build-time tool**: you write a
deployable app **once** (client + server handlers + schema); the kernel's runtime
serves requests. Two doctrine changes get you there — one you can start now, one that
waits for the runtime.

---

## 2. NOW (holds value without the runtime): persist-without-re-rendering

This is the load-bearing rule from the model-a handoff, and grounding confirms it is
**not yet in your doctrine** — and, crucially, it **INVERTS the current EVENT law
rather than extending it.**

- Today: `content/PROCESSES.md` §EVENT step 3 (`:95-96`) and the `APP_MODEL.md:133`
  write-order law make `canvas_set` the **mandatory terminal step of every event**
  ("Never reversed, never partial"). Every `canvas_set` **fully re-mounts the
  artifact iframe** (`COMPONENTS.md:97-99`) — which wipes the user's in-page state
  (scroll, open tab, unsaved input, live counter).
- The rule: **on a durable-state `emit`, update the app's state file and STOP — do
  NOT `canvas_set`.** `canvas_set` is only for a **structural rebuild from the chat**,
  not a data save. The client already holds live state; the emit is just persistence.

**Where it lands (fork the law, don't append):**
- `content/PROCESSES.md` §EVENT — split "durable-state emit → write state file, STOP"
  from "structural rebuild-from-chat → `canvas_set`".
- `content/BUILDER.md` §Interaction doctrine (`:109-120`) + `:46-47` — make re-publish
  **conditional**.
- `content/APP_MODEL.md` §Persistence — the write-order law's `canvas_set` step
  becomes conditional on structural change.

**Reconcile with your own open asks:** `KERNEL_ASKS #11` (file-event→canvas bridge)
already contemplates the same loop-protection class ("the session's own writes must
not re-trigger it"), and `#12` (direct edit → file write, **no LLM turn**) is the
lighter-than-a-turn write path. Persist-without-render must not fight #11: a *durable
emit persists without re-rendering*, but an *external file change should still refresh
the canvas.* Spell out which is which so the two mechanisms don't loop.

> The shell already does its half: an emit is fire-and-forget from the client (DC-22,
> v0.8.15) and never posts to the Builder transcript (DC-20, v0.8.13). But **the shell
> cannot stop a re-publish from resetting the iframe** — a new version always
> re-renders. So this has to be doctrine. It's yours.

---

## 3. NOW: two gate fixes the shell is waiting on

From testing Model A live, two drifts your own builder flagged:

- **`bin/check-app` rejects `html-embed`.** `bin/_contract.py` `KERNEL_ALLOWLIST`
  (`:8-18`) does not contain `html-embed`, so `check-app:211-214` hard-fails any
  `component:"html-embed"` region — even though the live kernel accepts it. Today
  your sanctioned path is the `code-block{render:true}` carriage (`COMPONENTS.md:74-83`).
  **Fix:** add `html-embed` to `KERNEL_ALLOWLIST` (+ `SHELL_RENDERED`) so authoring a
  website doesn't trip your own gate. (This reconciles with your `KERNEL_ASKS #3`.)
- **Teach `props.fill: true`.** The shell's full-bleed opt-in is the boolean
  `props.fill: true` on the artifact region (DC-21; `app/src/canvas/components.tsx`
  `fullBleedArtifact()`, `:189-197`). Your doctrine doesn't teach it (no `props.fill`
  / `fill?: boolean` appears anywhere in `content/`). **Fix:** document `fill?: boolean` in
  `content/COMPONENTS.md` §artifact and register it in `bin/check-app`/`_contract`.
  **Keep `height` numeric** — `fill` is a *separate* boolean deliberately, so it can't
  collide with numeric `height`. (Note: `check-app` doesn't actually type-check
  `height` today, so `height:"full"` wouldn't literally error — but `fill:true` is the
  sanctioned signal. Author against `fill:true`.)

---

## 4. LATER (waits for the kernel runtime): app = client + server + schema

Today an "app" is a **directory of screen LAYOUT docs + JSON state**, where the
*model is the runtime* — you re-author layout on every event (`APP_MODEL.md:1-18`:
"A vertical is a directory… the canvas is a projection of one screen of it"; the dir
is `app.json` + `screens/*.json` + `state/` + `data/`). **There are no server-handler
files and no per-app schema** — the "backend" is your LLM session (`BUILDER.md:46`).

SA-035's model is a genuine **new shape**, not an increment: author `client/` +
`server/` (handler code) + `schema/` **once**, and the kernel runs it. Your nearest
existing seam is the artifact/`html-embed` lane (`COMPONENTS.md:67-107`) — but that's
currently an "escape hatch" (`COMPONENTS.md:67`), **capped at one artifact region per
screen** (`COMPONENTS.md:103`), with no server + no schema. The charter **inverts the
priority** (self-contained website becomes the default app model for interactive
apps) and collides with the one-artifact-per-screen fence — both need doctrine
decisions when SA-035 is authored.

**Hook points for that later shift:** `content/APP_MODEL.md` §The workspace (`:1-45`,
grow the dir to client+server+schema); `content/BUILDER.md` mission header (default
app model = artifact/website); and the vocabulary re-scope below.

---

## 5. Vocabulary re-scope (canon wants this precise)

- **`canvas`** ≈ AI-authored layout doc — **already matches** the charter
  (`APP_MODEL.md:1-4`).
- **`app`** — today `app == vertical == directory-of-layout-docs+state`. The charter
  re-scopes `app` to the **executed client+server+schema artifact.** `vertical` is a
  third synonym that needs a decided fate.
- Land the re-scope in `content/APP_MODEL.md` §1, `content/BUILDER.md`, and the
  repo-root `CLAUDE.md`.

---

## What we need from domain-canvas now

1. **Land TASK-011** — **merge v0.11.0 into `main`** (the branch + tags are already
   pushed); consolidate the scattered handoffs. This unblocks everyone — do it first.
2. **Adopt persist-without-render + the two gate fixes** (§2, §3) on the canonical
   line — these are live doctrine value now, independent of SA-035.
3. **Weigh in on the seam** (sync contract §4): the **handler ABI** and the
   **`app.json` shape** — you write both; the kernel executes them.
4. A position on the **later shift** (§4/§5): making the self-contained app the
   default model, and the `app`/`vertical` vocabulary. Not now — when SA-035 is
   authored — but flag concerns early.

The immediate work (§2/§3) makes Model A feel like a website today. The rest waits
for the runtime and the canon lock.
