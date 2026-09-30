# small-io

Building sub-provincial (eventually) input-output tables for Canada by
regionalizing StatCan's national symmetric IO table with FLQ (Flegg's
Location Quotient). Before trying that on regions with no ground truth, this
project tests the method where ground truth *does* exist: start from the
national table, regionalize it down to each province, and compare against
StatCan's real published provincial IO tables.

## Data

Not checked into git (`/data/` is gitignored, ~5GB). Raw StatCan downloads:

- `data/National/<year>/` — national symmetric IO tables (StatCan catalogue
  15-207-X), 1997–2024p, at Detail (~234 industries) and Summary (~32)
  levels. Filenames switched from `IOTs national symmetric {LEVEL}
  <year>.xlsx` to `IOT national {LEVEL} <year>.xlsx` starting with the 2022
  vintage.
- `data/iot/<year>/<Level> level/` — the REAL provincial symmetric IO tables
  (catalogue 15-211-X), 2014–2022, all provinces/territories. This is the
  ground truth. Same filename-convention switch in 2022.
- `data/employment/` — extract of StatCan table 36-10-0676-01 (jobs by
  industry, provincial economic accounts), downloaded via the WDS API.

### What's in each file family

All IO data here is symmetric (industry × industry). The level codes are `S`
Summary (32 industries, $M), `L61` Link-1961 (110, $K), `L97` Link-1997
(186, $K) and `D` Detail (234, $K).

- **National** (`IOTs national symmetric <L> <year>.xlsx`, 2010–2021;
  `IOT national <L> <year>.xlsx`, 2022–2024p). One Canada-wide table per
  year and level, with final demand columns and value-added rows around the
  square intermediate block. It comes at purchaser prices, with the
  margin/tax sheets that convert them, and at basic prices (`BasicPrice`).
- **National domestic and imports** (`... domestic and imports ...`). This
  is the same national table split by where the inputs were made, into
  `Domestic` and imports. Imports are broken out by US, China, Mexico and
  rest of world, and `Total` is domestic plus imports.
- **National taxes** (`... taxes ...`, through 2022). These are the taxes on
  products paid on each transaction, broken out by tax. There's one sheet
  per tax (federal, provincial and municipal excise, fuel and sales taxes)
  plus a `Total`.
- **National, old `.xls`** (1997–2009). The 1997–2008 files come at `S`
  (Small) and `L-Public` (Link-Public) levels, with old industry codes
  (`1A`, `11A0`), modified basic prices and one sheet per margin type. 2009
  is also `.xls` but uses the current codes, at `S` and `L61`.
- **National preliminary vintages** (`National/Preliminary data/<year>_<release year>/`,
  2009–2023). These are superseded releases, e.g. `2014_2018` is the 2014
  table as published in 2018 and `2022p_2024` is the 2022 advance estimate.
  The current vintage of each year is in `National/<year>/`.
- **Provincial** (`IOTs provincial symmetric <PR> <L> <year>.xlsx`,
  2014–2021 at all four levels; `IOT provincial <PR> <L> 2022.xlsx`, `S`/`D`
  only). There's one table per region (10 provinces, `YT`/`NT`/`NU`, and
  `CE`, Canadian territorial enclaves abroad), laid out like the national
  table but with interprovincial trade columns by partner region. It also
  splits `BasicPrice` into `DomesticUse`, `InterprovImportUse` and
  `InternatImportUse`, and `DomesticUse` is the ground truth.
- **Provincial taxes** (`IOTs provincial symmetric taxes ...`, 2014–2021;
  `IOT provincial tax detail ...`, 2022). This is the same tax-by-type
  breakdown as the national taxes files, one workbook per region. It covers
  the same regions, years and levels as the provincial tables.
- **Employment** (`employment/36100676_*`). This is StatCan table
  36-10-0676-01, jobs by industry and province from the provincial economic
  accounts. The folder holds the raw download (`-eng.zip`, `_MetaData.csv`)
  and an extracted CSV, saved twice as `_jobs.csv` and `_filtered.csv`.

**Important gotcha**: each provincial workbook's `BasicPrice` sheet is
domestic + interprovincial + international imports *combined*. FLQ's
regional coefficient is defined to exclude anything not produced within the
region itself, so the real ground truth is the `DomesticUse` sheet, not
`BasicPrice`. Using `BasicPrice` by mistake produces plausible-looking but
wrong results.
