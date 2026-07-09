# The component contract — what a canvas region may be

The layout document is `rasa.layout.v1`:

```json
{ "layout": "1.0.0",
  "screen": { "name": "orders", "title": "Orders" },
  "regions": [ { "id": "kpis", "component": "kpi-tile", "props": { } } ] }
```

Regions flow vertically unless a region carries `frame {x,y,w,h}` (absolute,
canvas-local px; overlap legal; z = document order).

## Kernel allowlist (canvas_set validates component names)

`card-strip · inbox-list · matter-detail · doc-viewer · table · chart ·
kanban · timeline · kpi-tile · filter-bar · nav · modal · form ·
calendar-grid · media-viewer · code-block · ai-rail · map ·
markdown-block · button-row · card-list`

The RasaOS shell currently RENDERS this subset (the rest error-tile —
author ONLY these): `table · card-strip · card-list · form · chart · code-block ·
media-viewer · kpi-tile · timeline · markdown-block · button-row`

## Prop shapes the shell actually consumes (verified against the renderer, 2026-07-09)

These are the REAL shapes from frontend-rasaos `app/src/canvas/components.tsx`.
The renderer reads props defensively — a wrong key doesn't crash, it renders
EMPTY. Author exactly these:

- **kpi-tile** `{value, label, delta?}` — delta colored by leading `-`
- **table** `{title?, columns: [string | {key,label}], rows: [[…] | {…keyed by column key}]}`
- **card-strip** `{cards: [{title, subtitle?}]}` — horizontal, non-interactive
- **card-list** `{cards: [{title, subtitle?}], on_card_click?}` — with
  `on_card_click` set, each card is a button (see emission grammar)
- **chart** `{data: [{label, value}]}` — horizontal bars ONLY (no line type,
  no axes)
- **form** `{fields: [{id, label?, type?, placeholder?}], submit_label?}` —
  `type:'textarea'` special-cased, else a raw input type
- **timeline** `{events: [{at, label}]}`
- **button-row** `{buttons: [{id, intent, label?, style?}]}` — `style:'primary'`
  for the accent button; ALWAYS set `intent` (it is the emitted action; `id` is
  just the button's identity)
- **markdown-block** `{content}` — escaped subset only: `#/##/###`, `**bold**`,
  `` `code` ``, `- ` lists, paragraphs (raw HTML is escaped, never rendered)
- **code-block** `{code}` — plain `<pre>` text; NO syntax highlight, NO
  render carriage (`render:true` does nothing)
- **media-viewer** `{src}` — renders a safe LINK (http/https only, opens in a
  new tab); it never embeds. data:/javascript: render as inert text.

## Interactions — the emission grammar (what actions actually arrive)

Every interaction arrives in this session as `[canvas] <action> (<region-id>)`.
The shell computes the action string as follows — register every emittable
action in `app.json#events`:

- **button-row**: emits `intent`, else `'on_click'` with `{button_id}` in the
  payload. An intent-less button is ambiguous — always set `intent`.
  Navigation buttons carry `intent: "nav:<screen-id>"`.
- **card-list** with `on_card_click`: emits `on_card_click` with
  `{card_index, title}`.
- **form**: emits `on_submit` with `{<field-id>: value, …}` (uncontrolled).
- **any non-form region** with `props.on_click`: the whole region is clickable
  and emits `on_click` with `{region_id}`.

## §custom-visuals — 3D / animation (IN FLIGHT — do NOT author artifacts today)

Custom visuals, animation, drawing, and 3D land via a **sandboxed `html-embed`
escape region** — one self-contained HTML document in a sandboxed iframe with a
`window.rasa.emit` bridge. **It is not renderable yet** (verified 2026-07-09:
the shell has no artifact/iframe path; `code-block{render:true}` renders as
plain text; `media-viewer` never embeds). The implementable spec is
`docs/design/html-embed-spec.md` in this element's repo; the kernel half is
KERNEL_ASKS #3 (rewritten), the shell half is filed with frontend-rasaos.

Until it ships:

- Express every screen in the rendered subset above — data UIs (tables, KPIs,
  lists, forms, timelines) need nothing else.
- If a request genuinely needs 3D/animation, say so honestly on-canvas (a
  markdown-block noting the capability is in flight) and build the best
  declarative approximation. Never emit an artifact region — it error-tiles.
- When it ships: ONE artifact region per screen, self-contained document
  ≤ ~10KB (check-app already enforces the caps), CDN-loaded procedural
  three.js/WebGL works, runtime asset fetches (textures/GLTF/wasm) do not.

## Versioning

Every `canvas_set` bumps the canvas version; the shell renders monotonically
and rehydrates from snapshot on reload. Publish complete, coherent states.
