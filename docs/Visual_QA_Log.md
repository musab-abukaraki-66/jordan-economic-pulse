# Visual QA Log — Jordan Economic Pulse

All findings come from the real report rendered in Power BI Desktop 2.158.1177.0 (not from JSON validity). Every fix was applied **by class** in the generator (`scripts/report_builder/pbir_lib.py`, `scripts/report_builder/build_report.py`), then the report was rebuilt and re-rendered.

## Reference probe (before any bulk authoring)

Desktop opened a minimal PBIP, then saved it. The diff between what the generator wrote and what Desktop re-saved showed Desktop **kept** every property family used (rounded shapes, drop shadow, page image background, series selectors via `metadata`, visual links for page navigation, textbox paragraphs, card labels, slicer, sync groups) and **dropped only** five unsupported properties: category-axis `lineColor` / `showAxisLine`, slicer `fontSize` / `transparency`, and `dropdown.show`. Desktop also showed the canonical slicer default: `objects.general[].properties.filter.filter`.

## Defect classes found in render, and how each was fixed

| # | Class | Seen as | Root cause | Fix (once, in the design system) | Verified |
|---|---|---|---|---|---|
| 1 | Axis scale | Hero drew as one solid block; axes read "$0bnbn" | Axis limits set in raw dollars; display-unit and format-string scaling applied twice | Dedicated chart-helper measures already in US$ bn (provisional year blank); axis units off | Yes |
| 2 | Default year | KPIs showed multi-year sums (−$269.7bn) | Slicer default not applied | KPI measures pinned to `[Reference Year]` (selected year, else latest complete year); slicer default written in the canonical `general.filter` form | Yes |
| 3 | Card text | Values clipped ("−$13.4...bn"), then captions blank or cut | Cards too narrow / too short for the text; `Auto` display units appended a second "bn" | Explicit widths and heights (value 150×50, caption 236×48); measures already scaled, display units none | Yes |
| 4 | Gap shading | Overlapping areas hid each other; lines doubled | Area series order and outline colour cannot produce a gap band | Stacked-area "gap band" (transparent base + gap) under an exact-colour line chart; legends off on both and a manual legend so the two charts align | Yes |
| 5 | Crowded category axes | Rotated year labels, horizontal scroll bars | Categorical axis on 35 years | Scalar (numeric) year axis; flows chart changed to lines | Yes |
| 6 | Sparklines | Placeholder chart icon instead of a line | Below Power BI's minimum render size | 112×84 frames | Yes (closeout render) |
| 7 | Smoothed lines | Curved lines overshooting peaks | Base theme `Fluent2-CY26SU09` forces `lineChartType: smooth` | `linear` in the theme and on every line / area chart | Yes |
| 8 | Bar labels | Long commodity names truncated | Source labels too long for the axis | Short display names in `DimCommodity` (source names kept in the brief); smaller label font | Yes |
| 9 | Trade page bars | Partner charts showed a scroll bar (6 of 8 bars) | Power BI needs about 27 px per bar | Shorter top panels, taller bottom row, tighter bar padding | Yes (closeout render: all 8 partners visible) |
| 12 | Year slicer list | Dropdown listed only 2024; with a saved selection alone the dropdown crashed ("Object reference not set") | Default written as a visual-level filter on the slicer itself, then as a saved selection without that filter | Removed both; the default is handled in DAX (`[Reference Year]` = latest complete year when nothing is selected) | Yes: all years listed; selecting 2017 switched every KPI and caption |
| 10 | Misleading annotation | Figma concept said imports peaked "on fuel and food prices" | Claim not supported by the data | Removed; annotations are dynamic figures only | n/a |
| 11 | Desktop refresh | UI refresh reported "cyclic reference" | Report opened with pending query changes | Apply once via Close & Apply; afterwards Refresh loads all seven tables cleanly | Yes |

## Functional checks (performed by actually using the report)

- **Native rich tooltip** on the Executive hero: hovering a year shows imports, exports, gap, export coverage, current account, remittances and reserves for that year (2007: gap $8.0bn, coverage 41.8%, reserves $7.9bn). A report-page tooltip was tried first; after two failed attempts (its binding never showed) the mechanism was switched to the chart's native Tooltips field well, which works.
- **Page navigation:** rail buttons and the page tabs reach all four pages; the active page shows the bright glass pill, petrol bar and petrol dot.
- **Reference-year slicer** (single select, synced across pages) drives the KPIs and captions; time-series charts ignore it by design.

Remaining checks and the final full-resolution pass are recorded in `Final_Project_Report.md`.
