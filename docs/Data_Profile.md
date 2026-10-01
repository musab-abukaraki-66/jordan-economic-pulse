# Data Profile — Jordan Economic Pulse

Scope: the approved case (see `Case_Study_Brief.md`). Raw files in `data/raw` are immutable. Everything here was reproduced by `scripts/data_pipeline/` (`m02_recon.py`, `m03_build_tidy.py`, `m03c_wb_audit.py`, `m04_curate.py`, `m05_baseline.py`); logs are in `docs/`.

## 1. Source coverage (full acquisition, then scoped)

| Source | Files | What it holds | Coverage |
|---|---|---|---|
| World Bank WDI | 36 zips (265 countries and aggregates each) | Annual indicators | 1960–2025 (Jordan series start between 1960 and 1997) |
| Central Bank of Jordan (CBJ) | 13 workbooks, bilingual bulletin tables | Trade by commodity / function / geography, indices, monetary survey, reserves | 1964–2022 (monetary survey and reserves end 2021) |

**In scope (model):** 14 WB series for Jordan (GDP, real growth, per capita, CPI inflation, unemployment, population, merchandise exports and imports, net goods and services, current account in US$ and % GDP, remittances, FDI, reserves) for 1990–2025, and 4 CBJ tables (imports and domestic exports by commodity; imports and domestic exports by partner), 1990–2022.

**Out of scope (files retained, not modelled):** WB services trade (`NE.*`, ends 2007), REER (empty for Jordan), fiscal series, interest rates, bank NPL and capital, broad money, private credit, CPI index, GDP deflator, constant-price GDP, exchange rate, all non-Jordan countries; CBJ monetary survey, reserves, unit price and volume indices, imports from Arab countries, economic-function tables. Reasons: a structural break in the monetary series (Dec 1993), a definition that differs from the WB reserves series, redundancy, or no contribution to the approved story.

## 2. Grain (proved by row counts and distinct keys; zero duplicate keys)

| Table | One row = | Rows |
|---|---|---|
| `DimYear` | one calendar year, 1990–2025 | 36 |
| `FactEconomy` | one year, 14 measure columns | 36 |
| `FactTradeCommodity` | year × flow × commodity group | 650 |
| `FactTradePartner` | year × flow × partner group | 528 |
| `DimFlow` / `DimCommodity` / `DimPartner` | flow (2) / commodity group (10) / partner group (8) | 20 |

## 3. Quality audit (full population, no sampling)

- **Totals reconcile.** In every CBJ trade table the category columns sum to the Grand Total within rounding (max difference 3 JD thousand). Export totals agree across the geographic, commodity and function tables; import totals agree in all but one year (0.66% difference, 2012).
- **Source defects (excluded, logged in `docs/audit/m03_excluded_rows.csv`, nothing invented):**
  1. Imports by commodity, 2012: the row is an exact copy of 2011 (same total 13,440,215) and is labelled 2011. The correct 2012 import total, 14,733,749 JD thousand, is in the geographic and function tables. The commodity breakdown for 2012 is therefore null; partner totals are intact.
  2. Monetary survey, 1998 appears twice; the restated `(7)1998` row was kept (not modelled in the approved case).
  3. CBJ reserves 1993 "import coverage" holds a stray value (1153.6); not modelled.
- **Structural break.** Money supply is M1 + quasi-money before Dec 1993 and M2 after; not modelled for that reason.
- **World Bank nulls are almost all structural** (before a series starts or after its last release). Genuine interior gaps: CPI inflation (1 year) and central government debt (1 year; out of scope). Jordan unemployment starts in 1991, so 1990 is structurally null.
- **Real anomalies kept, not deleted:** population jumps of 6–10% in 1967, 1990–91, 2006–07 and 2014–15 (refugee and returnee flows); negative FDI in 1976, 1989, 1991 and 1993; GDP growth from −10.7% (1989) to +20.8% (1979). 2025 is provisional and several balance-of-payments series end in 2024.

## 4. Source reconciliation (what may and may not be mixed)

- WB merchandise **imports** vs CBJ imports at WB official FX: median ratio 1.000 (0.977–1.027). They agree.
- WB merchandise **exports** are about 1.23× CBJ exports because the CBJ tables are **domestic exports** (identical across its geographic and commodity tables) and WB includes re-exports. The report therefore labels WB exports "total merchandise exports" and CBJ exports "domestic exports", and never mixes them.
- WB total reserves (incl. gold) are about 1.05–1.09× CBJ gross reserves (valuation and definition). Only the WB series is used.

## 5. Additivity rules

| Type | Fields | Rule |
|---|---|---|
| Additive flows | merchandise exports and imports, net goods and services, current account, remittances, FDI, CBJ trade values | sum across years and categories; never together with a Grand Total column |
| Snapshots | reserves, GDP level, population | latest year in context; never summed over years |
| Non-additive | growth, inflation, unemployment, % of GDP, coverage ratios, months of import cover | per-year values; over several years a mean of annual ratios; never summed |
| Derived | import coverage (months) = reserves ÷ merchandise imports × 12 | labelled derived |
