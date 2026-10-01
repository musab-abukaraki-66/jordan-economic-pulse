# Model Documentation — JordanPulse semantic model

Built with the Power BI Modeling MCP (not hand-written TMDL), exported to `powerbi/JordanPulse.SemanticModel/definition`. Architecture decision: **Power Query over curated CSVs; no DuckDB or Parquet.** The whole model is about 50 KB of source data (1,200 fact rows), so extra infrastructure would add cost and no benefit.

## Tables (7 + measure container)

| Table | Type | Grain | Notes |
|---|---|---|---|
| `DimYear` | dimension | year 1990–2025 | `Year` (key), `Decade`, `IsProvisional` (2025) |
| `FactEconomy` | fact (wide) | one row per year | 14 World Bank measure columns, all hidden; every number is reached through a measure |
| `FactTradeCommodity` | fact | year × flow × commodity | CBJ, JD thousand |
| `FactTradePartner` | fact | year × flow × partner | CBJ, JD thousand |
| `DimFlow` | dimension | flow | Imports, Domestic exports |
| `DimCommodity` | dimension | commodity group | 10 groups, display names shortened; sort order column hidden |
| `DimPartner` | dimension | partner group | 8 groups |
| `_Measures` | measure container | none | about 100 measures in display folders 00–07 |

A single parameter `DataFolder` points at `data/curated/`; change that one value if the project moves.

## Relationships (7, single direction, many-to-one)

`FactEconomy[Year]`, `FactTradeCommodity[Year]`, `FactTradePartner[Year]` → `DimYear[Year]`; `FactTradeCommodity[FlowKey]`, `FactTradePartner[FlowKey]` → `DimFlow`; `FactTradeCommodity[CommodityKey]` → `DimCommodity`; `FactTradePartner[PartnerKey]` → `DimPartner`. No snowflaking, integer keys, hidden keys and numeric columns, attribute hierarchies off for hidden fields.

## Measure design

- **Base measures** (`01 Growth & Prices`, `02 External Position`, `03 Trade Structure (CBJ)`): stocks and rates show the latest year in context (`LASTNONBLANK`); flows sum; ratios are per-year ratios (mean of annual ratios over several years).
- **Reference-year pinned KPIs** (`06`, `07`): `VAR ry = [Reference Year]` then `CALCULATE(..., DimYear[Year] = ry)`. `[Reference Year]` is the selected year, or the latest complete year (2024) when nothing is selected, so the default is correct whatever the slicer holds. For CBJ tables `[CBJ Year]` caps it at 2022.
- **Chart helpers** (`04`): measures already in US$ bn or %, blank for the provisional year, so every time-series chart ends at 2024 and axes need no display-unit tricks.
- **Captions** (`05`): text measures that keep every caption in sync with the selected year.
- **Definitions preserved:** "Merch Exports" is total merchandise exports including re-exports (World Bank); "CBJ Domestic Exports" excludes re-exports; "Remittances + FDI (% of Merch Deficit)" is a context ratio, not an identity; "Import Coverage (months)" is derived.

## Validation

- 38 independent baseline KPIs reconcile 38 of 38 against live DAX (`docs/validation/Baseline_Reconciliation.md`).
- DAX rules applied: no reserved variable names; no RANKX is used (the CBJ bar charts sort by the share measure itself, and each returns exactly the categories in its dimension: 10 commodity groups, 8 partners).
- Performance: see `Final_Project_Report.md`.
