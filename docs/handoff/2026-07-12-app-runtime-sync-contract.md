# Sync contract → kernel + domain-canvas: the app-runtime charter (SA-035)

**From:** `rasa.frontend.rasaos`, 2026-07-12.
**Audience:** BOTH the kernel team and the domain-canvas team. This is the shared
anchor — read it first, then your team-specific doc:
- kernel → [`2026-07-12-kernel-app-runtime-charter.md`](https://github.com/RasaOS/frontend-rasaos/blob/main/docs/handoff/2026-07-12-kernel-app-runtime-charter.md)
- domain-canvas → [`2026-07-12-domain-canvas-app-runtime-charter.md`](2026-07-12-domain-canvas-app-runtime-charter.md)

**What triggered this:** canon task **SA-035 — kernel app-runtime charter** is
filed (`canon/tasks/triage/SA-035-app-runtime-charter.md`). It proposes taking the
AI **off the run-time hot path**: the AI writes a deployable app at *build-time*
(client + server handlers + data schema); a real kernel-hosted runtime serves it
at *run-time* in ms, no model in the loop. That change lands across **two repos at
once** — the kernel grows an app-runtime; the builder stops being the run-time
backend. This doc is the seam and the sequencing so the two halves don't drift.

Every claim here was verified against kernel `@v0.31.0` and the live domain-canvas
line (2026-07-12). Where SA-035's first draft was wrong, it's been corrected —
see SA-035's own "Grounding note".

---

## 0. Start from what is ALREADY shipped — don't rebuild it

The charter is the tier **above** what's live, not a redo of it. Shipped in the
shell (rely on these):

- **Client-side Model-A websites (DC-20/21/22, shell v0.8.13–v0.8.15).** A canvas
  that is a single full-bleed artifact runs its own JS in a sandboxed iframe. A
  **click is already 0 turns** — in-page JS, zero `/v1/commands`. So the "a button
  takes 15–40 s" complaint is **already fixed for the client-side case.**
- **`window.rasa.emit(action, payload)`** reaches the builder session as a bare
  `ui_event` (never a `[canvas]` transcript line, DC-20) and is **fire-and-forget**
  from the client (DC-22).

**The gap the charter fills is the SERVER tier a document can't provide:** durable
data, real queries, a request path, auth. And the honest limit that survives DC-22:
**a durable `emit` is still a full kernel turn on the wire** (fire-and-forget from
the client, but dispatcher → claude-runner → subprocess underneath). The AI is off
the *click* path; it is still on the *persist* path. The runtime is what takes it
off the persist path too.

> Framing rule for both teams: SA-035 is **"add a server/data tier to Model A,"**
> not **"fix click latency"** (Model A already did that).

---

## 1. The seam — where kernel and domain-canvas meet

One artifact, the **app directory**, is the contract surface. Today the shell
already homes canvas apps at `<tenant-cwd>/.rasaos/apps/<name>/` (DC-17, v0.8.8);
SA-035 keeps that root and adds executed pieces:

```
<tenant-cwd>/.rasaos/apps/<id>/
  app.json        # manifest — TODAY: domain doctrine the kernel refuses to parse.
                  #            CHARTER: the kernel EXECUTES it (routes, runtime, data).
  client/         # the website (Model A html-embed is the seed of this)
  server/         # handler code   ← NET-NEW. does not exist in either repo today.
  schema/         # per-app data schema ← NET-NEW.
  state/ data/    # JSON app memory (exists in domain-canvas APP_MODEL today)
```

**Two lanes run over that directory. Keeping them separate is the whole point —
it's the "two wirings" the user asked for:**

| | **BUILD lane** (slow, all AI) | **RUN lane** (fast, no AI) |
|---|---|---|
| Wiring | Builder rail ↔ `rasa.domain.canvas` | Viewport ↔ kernel app-runtime |
| Trigger | a chat message / structural rebuild | an HTTP request to `/apps/<id>/*` |
| Path | `canvas_set` publishes `rasa.layout.v1` | reverse-proxy → per-app process → handler → SQLite |
| Owner | **domain-canvas** | **kernel** |
| Today | this is ALL there is (the rail *is* the backend) | **does not exist** |

**Invariant (already agreed, DC-20 — do not soften):** *interacting with the
viewport must NOT message the build chat.* The RUN lane never posts into the
Builder transcript.

The seam contract itself — the two things the teams must agree on the shape of:

1. **`app.json`** — what domain-canvas **writes** and the kernel **executes**
   (routes, runtime kind, data bindings). Shape is an open question (§4).
2. **The handler ABI** — `handler(req, ctx)`: what domain-canvas **authors** and
   the kernel **invokes**, and what `ctx` exposes (data handle, secrets, egress).
   Also open (§4).

---

## 2. Ownership — who builds which half

| Piece | Owner | Status today |
|---|---|---|
| Canon charter (build-time/run-time boundary; is `app` a 9th kind; 4th FE profile) | **orchestrator-workspace** (canon) | SA-035 triage |
| App-runtime primitive, handler sandbox, per-app SQLite, `/apps/<id>/*` proxy, hot-reload | **kernel** | net-new (nothing exists — SA-035/`/apps` appear nowhere in the kernel repo) |
| Build-time app authoring (write client+server+schema once), persist-without-render, vocabulary | **domain-canvas** | doctrine shift on the canonical v0.11.0 line |
| The viewport that proxies the running app; the app-viewport frontend profile | **frontend-rasaos** (us) | Model-A viewport shipped (DC-21); proxy-a-live-server is future |

**We (frontend) are the requester, not an owner of the runtime.** The shell already
ships the honest thin version (client-side Model A). We can't build the server tier —
that's the kernel — and we can't change the build doctrine — that's domain-canvas.
This doc exists to get the two owners aligned.

---

## 3. Sequencing gate — the order that keeps the halves in sync

This is the coordination that matters. **Do not start building the runtime.** The
SA-034 precedent (the shell built the Canvas tab as an honest client-side affordance
*because the decision wasn't canon yet*) applies here: **canon leads.**

```
① domain-canvas TASK-011  ─ MERGE the canonical v0.11.0 line into main
   (BLOCKS EVERYONE)        (branch+tags already pushed; origin/main stale v0.5.3 — §5)
        │
② canon: LOCK the canvas family  ─ SA-026/027/028/030/034 + DOC-10 profiles
   (still triage/not-locked)       are the foundation SA-035 builds on
        │
③ canon: SA-035 dedicated cycle  ─ resolve the open questions (§4), author
        │                          Doc 01/10/02, decide the 9th kind / 4th profile
        │
④ THEN kernel builds the Phase-1 seam  ─ against a LOCKED charter
   AND domain-canvas authors the build-time app model
```

**Why ① blocks everything:** the canonical builder doctrine (v0.11.0, binding
registry + eight-process canon + hardened `check-app`) is **pushed to `origin` but
not merged into `main`** (branch `claude/core-internal-structure-12c464` + tags
v0.6.0–v0.11.0 are on origin). `origin/main` is stale at **v0.5.3**. Any team that
reads pushed `main` to "see how the builder works today" reads the *wrong* doctrine.
Merge it first (§5).

---

## 4. Joint open questions (need BOTH teams in the room)

These can't be answered by one team alone — they are the seam:

1. **The handler ABI** — `handler(req, ctx)`. What capabilities does `ctx` carry
   (data, secrets, egress)? Does canon spec the ABI, or only the charter and leave
   the ABI to a kernel spec? *(kernel + domain-canvas + canon)*
2. **`app.json` shape** — the manifest the builder writes and the kernel executes.
   Reuse the `rasa.json` `compose_fragment`+`ports` hook, or a new schema? *(all)*
3. **Is `app` a 9th Element kind, or an app-dir that is not an Element?** Decides
   whether apps are installable/shareable (the moat) or purely local. Reopens the
   "eight kinds, period" lock — SA-018-weight. *(canon, with both teams' input)*
4. **Sandbox tier** — Deno-perms default + Firecracker escape-hatch, or commit to
   one? The single most consequential choice (get it wrong → cross-tenant breach).
   *(kernel, needs security review)*
5. **Does the `/apps` run-lane reuse the canvas snapshot/watch shape** (`canvas.go`)
   or is it a plain reverse-proxy? If it reuses canvas, it inherits the `tenant='dev'`
   hardcode (TASK-074) and the 16-watcher cap. *(kernel + frontend)*
6. **How does persist-without-render (domain-canvas doctrine) reconcile with a
   real runtime?** Once the RUN lane persists to SQLite, the builder's durable-emit
   path may go away entirely — or coexist during migration. *(domain-canvas + kernel)*

---

## 5. Shared hazards (both teams inherit these)

- **The doctrine-line hazard (blocks ①).** Canonical domain-canvas doctrine is
  v0.11.0, **pushed to origin but not merged into `main`**; `origin/main` = v0.5.3.
  TASK-011 (the merge) is open. Until it lands, "the current builder doctrine" means
  different things depending on which branch you read. **Fix before anyone designs
  against it.**
- **`emit` is still a kernel turn.** Non-turn writes are the open domain-canvas
  ask `KERNEL_ASKS #12` (direct edit → file write, no LLM turn). The runtime is the
  real answer; #12 is the interim.
- **KA-28 resume risk.** If the long-lived runtime ever resumes turns via
  `--resume`, it inherits the kernel-drops-system-prompt-on-resume bug (KA-28).
- **Kernel is `v0.31.0`** (git tag). `core/package.json`'s `0.1.0` is stale — don't
  cite it.

---

## TL;DR for each team

- **kernel:** you own the runtime (primitive + sandbox + SQLite + `/apps` proxy +
  reload). It's all net-new — nothing exists today. **Don't build yet** — weigh in
  on the open questions (§4) and the sandbox tier; build when the charter locks.
  Details: your doc.
- **domain-canvas:** you own the build-time shift (write client+server+schema once;
  persist-without-render, which *inverts* today's EVENT law; vocabulary). **First
  land TASK-011** so everyone's on v0.11.0. Details: your doc.
- **both:** the seam is `app.json` + the handler ABI. Agree on those two shapes
  before either half is real.
