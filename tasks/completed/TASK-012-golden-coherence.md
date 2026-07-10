---
id: TASK-012
category: bug
status: completed
---

# TASK-012: Golden example coherence (review findings M1/M2/M3/L4)

The golden is THE exemplar every session imitates and every commit gates on —
it must be internally honest.

## What's broken

- **M1:** the `task-queue` KPI is bound read-write to the *tasks* module, but
  the `kpis` region renders *orders* data (value 12, "Open orders"). The
  binding and the visible content disagree. Fix: make the read-write demo's
  region actually show the bound tasks data (relabel + a plausible value), so
  binding ⇄ content are coherent.
- **M2:** the golden double-declares `../../data/orders.csv` as BOTH a
  `data_sources[]` row AND the `orders-table` binding — the exact redundancy
  APP_MODEL warns against. Drop the `data_sources[]` row; keep the binding.
- **M3:** the csv path is dangling and cited 3 inconsistent ways; off-by-one
  vs `_tenant_root: "../../.."`. Make ALL citations one consistent form
  (`../../../data/orders.csv`, which resolves at the tenant root) and add a
  one-line "illustrative placeholder" note (per user: no fake tenant tree).
- **L4:** module-tasks version cited as 0.1.2 here / 0.1.1 in binding-model /
  real is 0.1.3 — align to 0.1.3, note it's an install-time snapshot.

## Scope

In: examples/orders-desk/{app.json, context.json, screens/home.json,
data/orders-summary.json}, docs/design/binding-model.md §3 example version.
Must pass check-app under TASK-010's hardened checks (incl. the new traversal
guard — `../../../data/...` stays within `_tenant_root`).

## Acceptance

- [x] The read-write binding's region shows the bound (tasks) data — binding
      and content coherent.
- [x] One representation per source (no data_source+binding duplication).
- [x] One consistent csv path everywhere + the placeholder note; versions
      aligned to 0.1.3.
- [x] Golden GREEN under the hardened check-app.

## Artifacts

- examples/orders-desk/{app.json, context.json, screens/home.json,
  data/orders-summary.json}, docs/design/binding-model.md
