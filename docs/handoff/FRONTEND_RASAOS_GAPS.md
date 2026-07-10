# Handoff → frontend-rasaos team: the html-embed component + contract confirmations

**From:** `rasa.domain.canvas` (elements/domain-canvas), 2026-07-09.
**Self-contained** — written to be read in a frontend-rasaos session without the
originating conversation. We verified the renderer from source (`app/src/canvas/*`,
2026-07-09) and reconciled our authoring doctrine to it; this doc carries (1) the one net-new
component we need, (2) five-minute confirmations, and (3) smaller convergence items.

**Context:** domain.canvas is the element whose sessions author `rasa.layout.v1` canvas
layouts your shell renders — tenant-internal UIs built live, bound to tenant/module data.
Your renderer is the render engine; our `content/COMPONENTS.md` now mirrors your real prop
shapes exactly and treats your 11-component subset as the whole authoring vocabulary.

## F1 — the `html-embed` component (the priority item: 3D/animation)

3D + animation in canvas pages is a hard product requirement — and **the shell already
ships it** at current HEAD (`a5f6ff1`, "v0.5.0 — canvas-vertical lane + artifact studio").
We verified `app/src/canvas/components.tsx` line-by-line: the `html-embed` arm + the
`code-block{render:true}` carriage, and the full `HtmlEmbed` component —
`sandbox="allow-scripts"` (opaque origin), a srcDoc-injected CSP with `connect-src 'none'`
+ the four CDNs, the `window.rasa.emit` postMessage bridge with the `e.source` / `__rasa`
checks, and a fixed `height`. It is independently convergent with
`docs/design/html-embed-spec.md` §B — **there is nothing to build.** (This handoff's
original F1 said "there is no path, build it" — that read a pre-`a5f6ff1` checkout; it is
corrected here. See our postmortem `docs/postmortems/2026-07-09-artifact-lane-overcorrection.md`.)

**Remaining (small):**
- When the kernel enum lands (their **K1** — `html-embed` in the canvas allowlist + the
  `rasa.layout.v1` schema), add `html-embed` to your rendered-set docs so the direct form
  is first-class. Today it rides the `code-block{render:true}` carriage, which is
  kernel-legal — so the capability works now.
- Please **confirm the CSP/height deltas** we noted vs our spec (see the `html-embed-spec.md`
  status header): your `style-src` omits `esm.sh`; no `base-uri`/`form-action` directives;
  an empty document → warn tile. Intentional?

**Acceptance (already met):** a self-contained three.js scene from esm.sh renders sandboxed;
a hostile document (fetch/XHR, parent-DOM, top-nav) is contained; `rasa.emit` arrives as a
ui_event turn.

## F2 — emission-grammar confirmation (5 minutes, please)

We reconciled our authoring contract + validator to your renderer's real behavior. Please
confirm (or correct) these four readings of `components.tsx`:

1. **button-row**: emitted action = `button.intent ?? 'on_click'`, payload `{button_id}`
   (`:323-351`). *(We now require `intent` on every authored button.)*
2. **card-list** with `props.on_card_click`: emitted action is the **literal string
   `'on_card_click'`** (payload `{card_index, title}`) — or is it the *value* of
   `props.on_card_click`? (`:140-177`) ← our one real uncertainty.
3. **form**: emits `'on_submit'` with `{<field-id>: value}` (`:182-226`).
4. **region-level `props.on_click`** (non-form): whole region clickable, emits
   `'on_click'` with `{region_id}` — is the prop a boolean flag or does its value matter?
   (`CanvasPane.tsx:163-167`)

If any differ, flag it — our `bin/check-app` gate now encodes these exact rules.

## F3 — a generated component manifest (small, high leverage)

Our doctrine drifted from your renderer once already (we shipped
`markdown-block{markdown}`; you consume `{content}` — rendered empty, and our gate passed
it because it checks names, not props). Ask: a small build-step script that emits a JSON
manifest of the real contract — component names + consumed prop keys + emitted actions —
checked into your repo (e.g. `app/src/canvas/components.manifest.json`). We'll pin +
diff it in our `check-doctrine` so contract drift fails OUR gate, not a user's screen.

## F4 — theme tokens as CSS variables (small–medium)

`theme.json` values are Tailwind-baked at build; nothing is inheritable at runtime (no
`:root` custom properties — `index.css:19-26` only sets body colors). Ask: also emit the
tokens as `--rasa-*` (or canon doc-10 §18's `--color-substrate/essence/accent-*`,
`--font-*`, `--spacing-unit`) custom properties on `:root`. Lets html-embed artifacts and
any future surface inherit the theme instead of hardcoding hexes; aligns with doc-10's
CSS-variable theming layer ahead of time.

## F5 — doc-10 convergence (medium, later; flagging so it's on the roadmap)

Canon's locked frontend spec (doc 10 v1.0.0) defines things the shell doesn't render yet:
`screen.layout_grid` (parsed into your types but never read — `CanvasProvider` /
`CanvasPane.tsx:152-154` renders a flat column), the 6 named grids + slots, and the `nav`
component. We author `layout_grid` as intent and degrade gracefully today; when you honor
grids/slots, existing layouts upgrade with no re-authoring. (`ai-rail` we do NOT need —
the profiles edit scopes FE-005 to full-workspace, and the chat pane is our rail.)

## F6 — CSP cautions (so future hardening doesn't break F1)

The page currently ships **no CSP** (nginx.conf / index.html / vite). F1 does not need
one (containment is per-iframe). If a page-level CSP is ever added: it must permit
`srcdoc` frames (`frame-src`), Google Fonts (`index.html:8-13` loads them cross-origin —
consider self-hosting for offline tenants), and must not strip the iframe sandbox. Don't
couple that hardening to F1.

## Suggested order

F2 (5-min confirmations) → F1 (the capability) → F3 (keeps us honest) → F4 → F5.
