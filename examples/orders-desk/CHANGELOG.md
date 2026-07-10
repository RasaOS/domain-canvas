# Changelog — Orders Desk

- 0.4.0 — 2026-07-09 — coherence: the KPI now shows the bound follow-up-tasks count (matches its read-write tasks binding); dropped the redundant data_source (the orders-table binding is the single source of the csv); one consistent tenant-relative path; illustrative-placeholder note
- 0.3.0 — 2026-07-09 — bindings registry: orders table bound to the tenant csv (read); open-tasks KPI bound read-write to module-tasks' tasks collection; "Log follow-up task" action writes the bound collection + filters state
- 0.2.0 — 2026-07-08 — orders screen added (table + actions), nav contract wired
- 0.1.0 — 2026-07-08 — bootstrapped: home screen with open-orders KPI
