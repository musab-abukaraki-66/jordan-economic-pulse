# Case Study Brief — Jordan Economic Pulse

**Growth, Prices and the External Gap**

## 1. Selected case

A focused, four-page Power BI case study on Jordan's economy, 1990–2025, built only from official World Bank (WDI) and Central Bank of Jordan (CBJ) data.

**Analytical framing.** How has Jordan's external gap evolved, and what external inflows and reserve dynamics provide context for its sustainability?

The case does **not** present the merchandise trade deficit as an accounting identity equal to remittances plus FDI plus reserve drawdown. Each concept is shown separately and with its source definition:

| Concept | Source | Note |
|---|---|---|
| Merchandise trade balance | World Bank (`TX.VAL.MRCH.CD.WT` − `TM.VAL.MRCH.CD.WT`) | Total merchandise exports include re-exports |
| Net goods and services | World Bank BoP (`BN.GSR.GNFS.CD`) | Adds services (e.g. tourism) |
| Current account | World Bank BoP (`BN.CAB.XOKA.CD`, `.GD.ZS`) | Broader than trade; includes transfers and income |
| Remittances received | World Bank (`BX.TRF.PWKR.CD.DT`) | Inflow, context for financing |
| FDI net inflows | World Bank (`BX.KLT.DINV.CD.WD`) | Inflow, context for financing |
| Reserve level | World Bank (`FI.RES.TOTL.CD`, includes gold) | Level; change is shown as context, not as a "funding" line |
| Domestic exports | CBJ (JD thousand) | Excludes re-exports; not comparable to WB total exports |
| Imports | CBJ (JD thousand) | Reconciles to WB merchandise imports (median ratio 1.000) |

## 2. Business / analytical objective

Give an executive viewer a fast, defensible read of (a) how the economy is performing and (b) how large the external gap is and what external inflows and reserves sit around it.

## 3. Target audience

Senior economists, policy analysts, bank and development-finance executives, and portfolio reviewers who need a trustworthy briefing rather than a statistics browser.

## 4. Key questions

1. How large is the merchandise trade deficit (USD and % of GDP), and is it structural?
2. How do remittances, FDI and the current account move around it, and how stable was each?
3. Is growth beating population growth, and how did inflation and unemployment move through shock years?
4. What does Jordan import and (domestically) export, and how has the commodity mix changed?
5. Which partner groups account for domestic exports and imports, and has the mix shifted?
6. How many months of imports do reserves cover, and is the cushion changing?

## 5. In-scope sources

**World Bank WDI (Jordan, 1990–2025), 14 series** — GDP (current US$), real GDP growth, GDP per capita, CPI inflation, unemployment, population, merchandise exports, merchandise imports, net goods and services, current account (US$ and % GDP), remittances, FDI, total reserves.

**CBJ Annual Statistical Bulletin (JD thousand, 1990–2022), 4 tables** — imports by commodity (SITC), domestic exports by commodity (SITC), geographic distribution of exports, geographic distribution of imports.

## 6. Out-of-scope sources (raw files retained, immutable, excluded from the model)

- World Bank: services-inclusive trade (`NE.*`, ends 2007), REER (empty for Jordan), fiscal series, interest rates, bank NPL/capital, broad money, private credit, CPI index, deflator, constant-price GDP, exchange rate, all non-Jordan countries and aggregates.
- CBJ: monetary survey (structural break in Dec 1993), CBJ reserves (definition differs from WB), unit price and volume indices, imports from Arab countries, economic-function tables, and the 57 CBJ tables that were never downloaded.
- Years before 1990.

No additional downloads were required.

## 7. Grain of each in-scope table

| Table | One row = |
|---|---|
| `DimYear` | One calendar year (1990–2025) |
| `FactEconomy` | One year, wide (14 World Bank measures) |
| `FactTradeCommodity` | Year × Flow (Imports / Domestic exports) × Commodity group |
| `FactTradePartner` | Year × Flow (Imports / Domestic exports) × Partner group |
| `DimFlow` | Trade flow |
| `DimCommodity` | CBJ SITC commodity group (10) |
| `DimPartner` | CBJ partner group (8) |

## 8. Key metrics

Merchandise trade balance (USD, % GDP); export coverage of imports; current account (USD, % GDP); remittances and FDI (USD, % GDP); reserves (USD) and import coverage in months (derived); real GDP growth, population growth, GDP per capita; CPI inflation; unemployment; commodity and partner shares (CBJ, JD).

**Additivity rules.** Flows (trade, remittances, FDI, current account) sum over years. Reserves, population and GDP level are snapshots. Rates, ratios, % of GDP, growth and inflation are never summed.

## 9. Limitations

- CBJ exports are domestic exports and exclude re-exports; they are never mixed with WB total merchandise exports.
- CBJ trade tables are in JD; WB series are in USD. Units are labelled and not silently converted.
- 2012 imports-by-commodity is missing in the source (the row is a copy of 2011 and is excluded); the partner and total series for 2012 are intact.
- 2025 World Bank values are provisional; several BoP series end in 2024.
- WB reserves include gold and differ from the CBJ definition.
- Import coverage in months is derived (WB reserves ÷ WB merchandise imports × 12), not a published CBJ figure.
- Annual frequency only.

## 10. Proposed page architecture

1. **Executive Pulse** — headline KPIs, the external-gap hero, one editorial callout.
2. **Growth & Domestic Conditions** — growth vs population growth, GDP per capita, inflation, unemployment.
3. **External Position** — exports and imports, the balance, current account, remittances, FDI, reserves and import coverage.
4. **Trade Structure & Sources** — commodity and partner mix (CBJ) with a compact definitions and sources panel.
