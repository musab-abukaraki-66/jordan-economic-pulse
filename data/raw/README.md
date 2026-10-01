# Raw official source files (not committed)

The raw World Bank and Central Bank of Jordan files are not stored in this repository. `../SOURCES.csv` lists every file with its official URL, retrieval date, byte size and SHA-256 so it can be re-downloaded and verified.

Layout expected by `scripts/data_pipeline/`:

```
data/raw/worldbank/WB_<INDICATOR>_all_countries_csv.zip
data/raw/cbj/<original CBJ workbook name>.xlsx
```
