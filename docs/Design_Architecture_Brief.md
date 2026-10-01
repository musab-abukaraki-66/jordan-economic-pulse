# Design Architecture Brief — Jordan Economic Pulse

## Direction

Approved: **Concept B, "Frosted Terminal"**, translated for Power BI. Light, airy and premium; cool near-white canvas; a persistent frosted left rail; glass KPI tiles; one strong hero per page; petrol teal as the primary colour, slate blue as secondary, sand-amber only for deficits and warnings.

The three concepts (A Editorial Ledger, B Frosted Terminal, C Asymmetric Spread) were built in Figma from the real 2024 values and are in `assets/design-concepts/`. References consulted: Dribbble and Behance premium light-glass dashboards, editorial chart practice (direct labels, one highlighted series, visible hairline grids) and institutional annual-report layouts. Nothing was copied.

## What was kept, what was translated, what was dropped

| B feature in Figma | In Power BI |
|---|---|
| Background blur behind glass | **Not reproducible.** Replaced by a soft tonal canvas image (a static, blurred cool field, no heavy mesh) that the panels sit on |
| Translucent white panels | Rounded-rectangle shapes, near-white fill at 38% transparency, 1 px white hairline, very soft outer shadow |
| Mesh gradient blobs | Reduced to four faint tonal areas baked into one 1440×900 canvas image |
| Frosted nav rail | Glass shape plus page-navigation buttons; the active page gets a brighter glass pill, a petrol bar and a petrol dot |
| KPI tiles with sparklines | Glass tile + text label + card (value) + card (caption) + borderless line-chart sparkline |
| Hero gap shading | A stacked-area "gap band" drawn under exact-colour lines (two aligned charts with identical axes) |
| Gap and year annotations | Dynamic caption measures that follow the selected year |
| Inter typeface | **Segoe UI / Segoe UI Semibold**, the closest reliable fonts in Power BI |

## Design system (centralised in `scripts/report_builder/pbir_lib.py`, `DS` and helper functions)

- **Canvas:** 1440×900. Grid: rail x24–256; content x288–1416; KPI row y112; hero y250; bottom row y658; 16 px gutters.
- **Colour:** canvas `#EDF1F3`, ink `#16222E`, muted `#5F6E7C`, petrol `#0F5C63`, slate `#6E86A0`, amber `#B7862E`, hairline `#D4DDE3`. One family plus one alert accent; no rainbow series. The theme file `JordanPulseGlass.json` supplies data colours and visual defaults (axes, legends, gridlines, line widths).
- **Type:** Segoe UI Semibold for titles and values, Segoe UI for labels; page title 20 pt, KPI value 22 pt, panel title 12.5 pt, captions 9 pt, kicker labels 7.5 pt.
- **Surfaces:** `glass()` for rail, KPI, hero, side and bottom panels (radius 18–22, rail 22). One function controls every panel, so a surface fix is one edit.
- **Charts:** hairline gridlines only, no chart borders, plot areas transparent, series colours from selectors, manual legends where two charts overlay.

## Page architecture

1. **Executive Pulse:** four KPIs, the exports-vs-imports hero with the shaded gap, "Inflows in context", and three supporting panels (GDP growth, inflation and unemployment, reserves).
2. **Growth & Prices:** real growth against population growth, GDP per capita, inflation, unemployment, population.
3. **External Position:** the three measures of the gap (merchandise, goods and services, current account), reserves, remittances and FDI as % of GDP, change in reserves.
4. **Trade Structure:** CBJ commodity and partner mix for imports and domestic exports, domestic export coverage over time, and a definitions and sources panel.

## Interactions

- A **Reference year** slicer in the rail (single select, synced across all pages) drives every KPI and caption; time-series charts are excluded from it (`NoFilter`) so they always show the full history.
- **Page navigation** from the rail on every page.
- A **report tooltip page** (`ttYear`) shows the full snapshot for any year hovered on the hero charts.
