"""Shared contract constants — MUST match content/COMPONENTS.md exactly.

bin/check-doctrine enforces the lockstep (it parses COMPONENTS.md and
compares against these lists). Edit the doc and this file together.
"""

# The kernel allowlist: component names canvas_set accepts.
KERNEL_ALLOWLIST = [
    "card-strip", "inbox-list", "matter-detail", "doc-viewer", "table",
    "chart", "kanban", "timeline", "kpi-tile", "filter-bar", "nav", "modal",
    "form", "calendar-grid", "media-viewer", "code-block", "ai-rail", "map",
    "markdown-block", "button-row", "card-list",
]

# The subset the RasaOS shell actually renders (the rest error-tile).
SHELL_RENDERED = [
    "table", "card-strip", "card-list", "form", "chart", "code-block",
    "media-viewer", "kpi-tile", "timeline", "markdown-block", "button-row",
]
