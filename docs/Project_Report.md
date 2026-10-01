# Final Project Report — Jordan Economic Pulse

**Growth, Prices and the External Gap** · a four-page Power BI case study on official World Bank and Central Bank of Jordan data, 1990–2025. Design direction: Concept B, "Frosted Terminal", translated for Power BI.

## What was delivered

| Item | Location |
|---|---|
| Power BI project (open this) | `powerbi/JordanPulse.pbip` |
| Semantic model (TMDL) | `powerbi/JordanPulse.SemanticModel/definition/` |
| Report (PBIR, theme, canvas image) | `powerbi/JordanPulse.Report/` |
| Curated data (Power Query source) | `data/curated/*.csv` (7 files, 44 KB) |
| Build scripts (reproducible) | `scripts/data_pipeline/` (`m02`–`m05` data and baseline, `pbir_lib.py` + `build_report.py` report generator) |
| Final screenshots of all four pages | `assets/screenshots/` |
| Design concepts A / B / C (Figma renders) | `assets/design-concepts/` |
| Documents | `Case_Study_Brief.md`, `Data_Profile.md`, `Model_Documentation.md`, `Design_Architecture_Brief.md`, `Visual_QA_Log.md`, this report, `docs/validation/Baseline_Reconciliation.md` |

The four pages: **Executive Pulse**, **Growth & Prices**, **External Position**, **Trade Structure**. A frosted navigation rail, a synced reference-year slicer and a native hover tooltip on the hero charts are included.

## What was verified (in Power BI Desktop 2.158.1177.0, with real data)

- **Files intact** after an interrupted session: 272 JSON files parse, 4 pages, 105 measures, raw source files untouched (`data/raw` not modified).
- **Reopen:** the project opens cleanly from disk. **Native Refresh** loads all seven tables with no error.
- **All four pages render** with real data. Final screenshots were taken from Desktop.
- **Page 1 sparklines** draw as lines (the placeholder-icon issue was fixed by enlarging the frame).
- **Page 4 partner bars** show all 8 partners in both charts, with no scroll bars.
- **Navigation:** the rail buttons reach Growth & Prices and External Position; the page tab reaches Trade Structure.
- **Year slicer:** opens, lists all years, and selecting 2017 switched every KPI and caption to 2017 (deficit −$13.0bn, coverage 36.6%, reserves $15.6bn, gap callout updated), while the time-series charts correctly keep their full history. Clearing the selection returns the 2024 default.
- **Hover tooltip** (Executive hero) shows imports, exports, gap, coverage, current account, remittances and reserves for the hovered year.
- **Numbers:** 38 of 38 independent baseline KPIs equal the live DAX results (`docs/validation/Baseline_Reconciliation.md`).

## Performance (measured, this machine: 2 cores, 7.8 GB RAM)

| Metric | Result |
|---|---|
| Source data | 7 CSV files, 44 KB; 1,214 fact rows |
| Semantic model on disk | about 88 KB data cache plus 83 KB of TMDL; report folder 2.8 MB (mostly generated JSON) |
| Cold refresh (first external engine refresh after opening) | about 90 s wall-clock |
| Native Desktop Refresh | about 30–45 s when the UI was responsive; up to about 2 min when the UI was lagging |
| Desktop memory while all four pages were loaded and refreshed | PBIDesktop 588 MB, model engine 647 MB (working set at the time of measurement; a true peak was not recorded) |
| Representative DAX timings (live) | 38 baseline KPIs in single queries: 0.3 s warm to 2 s cold for the headline set; a 15-measure caption set took 9 s cold |
| Slow visuals | none identified; no benchmark-driven optimisation was needed because the model is tiny |

Warm and cold timings are reported separately; the warm numbers are not a substitute for cold refresh.

## Known limitations and imperfections

**Data**
- CBJ exports are **domestic exports** (no re-exports); World Bank exports include re-exports. The report labels both and never mixes them. The WB/CBJ export ratio is about 1.23.
- CBJ trade tables end in 2022. The Trade Structure page therefore shows 2022 when the reference year is later and says so on the page.
- 2012 imports by commodity are missing in the source (a copied 2011 row was excluded). Partner and total series for 2012 are intact.
- 2025 World Bank values are provisional and several balance-of-payments series end in 2024; charts stop at 2024.
- WB total reserves include gold and differ from the CBJ definition; import coverage in months is derived (reserves ÷ merchandise imports × 12).
- "Remittances + FDI as % of the merchandise deficit" is a context ratio, not an accounting identity.

**Design and Power BI**
- Background blur and mesh gradients from the Figma concept cannot be reproduced in Power BI. The glass look is approximated with near-white translucent panels, hairline borders, soft shadows and a soft tonal canvas image.
- Power BI smooths lines by default in the Fluent base theme; the report overrides this to straight lines.
- Charts below a minimum size will not draw (sparklines need about 112×84 px).
- **Year slicer behaves as a multi-select checklist**: the single-select option did not take effect in this build, so KPIs use the latest selected year. A saved default selection crashed the dropdown in this build and was removed; the default is instead handled in DAX (no selection shows the latest complete year, 2024).
- A report-page tooltip did not bind after two attempts; the native chart tooltip (verified) is used instead.
- Hero line charts overlay a stacked-area gap band; both must keep identical axes and plot areas to stay aligned, so their settings should be edited together.
- The UI of this PC is slow; Power BI Desktop needs roughly 1–2 minutes to open the report and load visuals.

**Not done (out of scope by decision)**
- No drill-through pages, no bookmarks, and no dark mode.
- No additional CBJ tables were downloaded; none were required by the approved story.

## Reproducing the build

1. `scripts/data_pipeline/m03_build_tidy.py` → `m04_curate.py` → `m05_baseline.py` rebuild the curated data and the independent baseline from the immutable raw files.
2. `scripts/report_builder/build_report.py` regenerates the whole report folder from the design system in `pbir_lib.py` (close Desktop first).
3. Open `JordanPulse.pbip` in Power BI Desktop and press **Refresh**. If the project is moved, change the single `DataFolder` parameter.
