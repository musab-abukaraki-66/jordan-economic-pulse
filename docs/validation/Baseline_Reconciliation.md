# Baseline reconciliation — DAX vs independent Python baseline

Baseline: `scripts/m05_baseline.py` (reads the raw World Bank zips and raw CBJ workbooks with its own code path) → `docs/baseline_kpis.csv`.
DAX: live query against the semantic model open in Power BI Desktop 2.158.1177.0 (`JordanPulse.pbip`, full refresh).
Result: **38 of 38 KPIs match** (World Bank B01–B26, CBJ C01–C12). The baseline sanity check also caught one error in the baseline script itself (wrong CBJ column for fuel share); it was fixed before reconciling.

| ID | KPI | Year(s) | Baseline | DAX | Match |
|---|---|---|---|---|---|
| B01 | GDP (USD) | 2024 | 58,618,380,563.38 | 58,618,380,563.38 | yes |
| B02 | Real GDP growth (%) | 2024 | 2.5561 | 2.5561 | yes |
| B03 | GDP per capita (USD) | 2024 | 5,073.92 | 5,073.92 | yes |
| B04 | CPI inflation (%) | 2024 | 1.5566 | 1.5566 | yes |
| B05 | Unemployment (%) | 2024 | 16.693 | 16.693 | yes |
| B06 | Population | 2024 | 11,552,876 | 11,552,876 | yes |
| B07 | Population growth (%) | 2024 | 0.9936 | 0.9936 | yes |
| B08 | Merchandise exports (USD) | 2024 | 13,534,000,000 | 13,534,000,000 | yes |
| B09 | Merchandise imports (USD) | 2024 | 26,895,000,000 | 26,895,000,000 | yes |
| B10 | Merchandise trade balance (USD) | 2024 | −13,361,000,000 | −13,361,000,000 | yes |
| B11 | Trade balance (% GDP) | 2024 | −22.7932 | −22.7932 | yes |
| B12 | Export coverage of imports (%) | 2024 | 50.3216 | 50.3216 | yes |
| B13 | Net goods & services (USD) | 2024 | −7,712,253,521 | −7,712,253,521 | yes |
| B14 | Current account (USD) | 2024 | −3,126,507,042 | −3,126,507,042 | yes |
| B15 | Current account (% GDP) | 2024 | −5.3337 | −5.3337 | yes |
| B16 | Remittances (USD) | 2024 | 4,431,126,761 | 4,431,126,761 | yes |
| B17 | FDI net inflows (USD) | 2024 | 1,634,647,887 | 1,634,647,887 | yes |
| B18 | Reserves incl. gold (USD) | 2024 | 21,939,099,362 | 21,939,099,362 | yes |
| B19 | Import coverage (months) | 2024 | 9.7888 | 9.7888 | yes |
| B20 | Remittances + FDI as % of merchandise deficit | 2024 | 45.3991 | 45.3991 | yes |
| B21 | Reserve change (USD) | 2024 | 2,870,197,671 | 2,870,197,671 | yes |
| B22 | Avg real GDP growth | 2010–2024 | 2.3919 | 2.3919 | yes |
| B23 | Cumulative remittances (USD) | 2015–2024 | 46,645,352,113 | 46,645,352,113 | yes |
| B24 | Avg trade balance (% GDP) | 1990–2024 | −31.3010 | −31.3010 | yes |
| B25 | Peak unemployment (%) | 1991–2025 | 21.439 | 21.439 | yes |
| B26 | Merchandise trade balance (USD, provisional) | 2025 | −14,032,000,000 | −14,032,000,000 | yes |
| C01 | CBJ imports, sum of commodity groups (JD k) | 2022 | 19,428,480.5 | 19,428,480.5 | yes |
| C02 | CBJ domestic exports (JD k) | 2022 | 8,365,530 | 8,365,530 | yes |
| C03 | Fuel share of imports (%) | 2022 | 18.4038 | 18.4038 | yes |
| C04 | Food share of imports (%) | 2022 | 18.8328 | 18.8328 | yes |
| C05 | Arab share of domestic exports (%) | 2022 | 32.762 | 32.762 | yes |
| C06 | EU share of imports (%) | 2022 | 16.3027 | 16.3027 | yes |
| C07 | Domestic export coverage of imports (%) | 2022 | 43.0581 | 43.0581 | yes |
| C08 | Chemicals share of domestic exports (%) | 2022 | 27.9281 | 27.9281 | yes |
| C09 | China share of imports (%) | 2022 | 15.2302 | 15.2302 | yes |
| C10 | Fuel share of imports (%) | 2000 | 15.6106 | 15.6106 | yes |
| C11 | Imports 2012 via partner table (JD k) | 2012 | 14,733,750 | 14,733,750 | yes |
| C11b | Imports 2012 via commodity table | 2012 | unavailable (source copy error) | blank | yes (expected) |
| C12 | CBJ imports (JD k) | 2010 | 11,050,126 | 11,050,126 | yes |

Notes
- Ratio measures are annual ratios; over several years they return the mean of annual ratios (B22, B24 are computed that way).
- Import coverage (months) is derived: WB reserves ÷ WB merchandise imports × 12.
- "Remittances + FDI as % of merchandise deficit" is a context ratio, not an accounting identity.
