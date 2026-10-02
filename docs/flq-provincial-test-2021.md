# FLQ regionalization: provincial test, 2021

Notes from 2026-10-02. All numbers are for 2021 and the 10 provinces. Territories and CE are excluded.

## Goal

Regionalize the national symmetric IO table to each province with FLQ, then compare against StatCan's real provincial tables. This tests the method where ground truth exists, before using it below the province level, where none does.

## Strategy

### Data

- **National input:** `Domestic` sheet of `IOTs national symmetric domestic and imports {S,D} 2021.xlsx`. This sheet excludes international imports, as FLQ requires.
  ```
  a_ij = Z_ij / X_j          # X_j = TOTAL row (gross output, basic prices)
  ```
- **Ground truth:** each province's `DomesticUse` sheet, which counts only inputs made in that province. It excludes both interprovincial and international imports.
  ```
  r_ij = DomesticUse_ij / X_j^r
  ```
  `DomesticUse + InterprovImportUse + InternatImportUse = BasicPrice` holds cell for cell (tested). Never compare against `BasicPrice`.
- **Levels:** Summary (32 industries, $M) and Detail (234 industries, $K). Both levels use the same loaders.

### Location quotients

- **Basis:** jobs (paid + self-employed), StatCan table 36-10-0676-01, 2021. Flegg & Tohmo also used employment. Below the province level, employment is the only regional data we'll have.
- **Summary mapping:** NAICS groups mapped to IO industries by hand (`employment.SUMMARY_NAICS`). Business and government industries share a group: BS610 and GS610 are both NAICS 61.
- **Detail mapping:** a rule. Strip the sector prefix and trailing zeros (`BS311700` → NAICS 3117), then fall back to the nearest parent code the jobs table has (`employment.detail_naics`).
  - 224 of 234 industries match a jobs code exactly.
  - Three overrides: conventional oil and gas, oil sands, and owner-occupied dwellings.
- **No jobs at all:** owner-occupied dwellings and "other non-profits" get SLQ = 1.

```
SLQ_i   = (RE_i / TRE) / (NE_i / TNE)
CILQ_ij = SLQ_i / SLQ_j            # SLQ_i on the diagonal (Smith & Morrison; Flegg & Tohmo)
FLQ_ij  = CILQ_ij * lambda
lambda  = [log2(1 + TRE/TNE)]^delta
r_ij    = min(FLQ_ij, 1) * a_ij
```

### δ

δ is fixed at **0.25**, the single value Flegg & Tohmo recommend from 20 Finnish regions ("we would recommend using δ = 0.25 as the best single value", UWE DP 1005). We use one δ with no tuning, by design.

### Baselines and metrics

- **Baselines:**
  - `national`: national coefficients used unchanged.
  - SLQ and CILQ.
  - **LQ floor:** the lowest cell error any `r_ij = c_ij * a_ij` with `c_ij` in [0, 1] could reach. LQ methods only ever scale national coefficients down, so wherever the true regional coefficient exceeds the national one, the gap can't be closed.
- **Metrics:** all computed over industries the province actually has.
  - **Cell WAPE on flows:** `Σ|Ẑ − Z| / ΣZ`, where `Z = coefficient × the province's real output`. Big cells count more. Over- and underestimates don't cancel.
  - **Output multiplier bias:** the mean % error in Type I output multipliers (column sums of `(I − A)⁻¹`). This is Flegg & Tohmo's µ1. Signed: negative means impacts are understated.
  - **Local-input share error:** estimated minus actual `Σ_i r_ij`, averaged over industries, in percentage points.

## Results: all provinces

Means over the 10 provinces:

| | national | SLQ | CILQ | FLQ(0.25) | LQ floor |
|---|---:|---:|---:|---:|---:|
| Summary: cell WAPE % | 66.9 | 45.3 | 45.5 | 45.0 | 10.4 |
| Summary: multiplier bias % | +16.5 | +6.3 | +5.5 | −7.9 | |
| Detail: cell WAPE % | 72.5 | 51.7 | 52.2 | 57.3 | 15.8 |
| Detail: multiplier bias % | +17.0 | +3.8 | +4.5 | −5.6 | |

FLQ(0.25) by province:

| | NL | PE | NS | NB | QC | ON | MB | SK | AB | BC | mean |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Summary WAPE % | 62.9 | 68.1 | 55.2 | 50.6 | 23.1 | 14.7 | 46.2 | 55.6 | 39.9 | 33.4 | 45.0 |
| Summary floor % | 15.3 | 23.0 | 11.6 | 10.1 | 3.5 | 3.0 | 6.9 | 12.5 | 9.7 | 8.4 | 10.4 |
| Summary multiplier bias % | −12.1 | −9.6 | −10.3 | −10.1 | −4.1 | +0.7 | −6.2 | −9.6 | −10.6 | −6.6 | −7.9 |
| Detail WAPE % | 76.9 | 79.1 | 65.1 | 64.3 | 40.7 | 26.9 | 60.1 | 64.6 | 49.9 | 45.5 | 57.3 |
| Detail floor % | 22.1 | 28.2 | 17.3 | 17.3 | 10.8 | 7.1 | 13.4 | 16.1 | 13.6 | 12.1 | 15.8 |
| Detail multiplier bias % | −6.6 | −8.5 | −6.0 | −6.3 | −5.6 | −2.8 | −4.4 | −5.5 | −5.2 | −4.7 | −5.6 |
| Detail → Summary WAPE % | 63.3 | 67.2 | 52.7 | 49.0 | 25.7 | 13.8 | 42.9 | 48.0 | 35.9 | 29.1 | 42.8 |

- **Unadjusted national coefficients overstate multipliers by about 17%.** SLQ and CILQ remove most of that.
- **FLQ(0.25) overcorrects.** It understates multipliers in 9 of 10 provinces at Summary; Ontario is the exception. In Finland, δ = 0.25 gave +0.4% bias. Here an in-sample sweep put zero bias near δ ≈ 0.1. We didn't pursue it, because we keep a single δ.
- **Cell WAPE isn't comparable across levels.** A 234 × 234 table has more cells to miss. The fair comparison is the last row: estimate at Detail, aggregate to Summary, and score against the real Summary table. On that basis Detail slightly beats Summary at δ = 0.25 (42.8% vs 45.0%). Its multiplier bias is a bit worse, though (−9.1% vs −7.9%).
- **The floor rises with detail** (10.4% → 15.8%). Within a Summary cell, Detail cells where the province buys more than the national coefficient can be offset by cells where it buys less. Separate Detail cells can't offset each other.

## Nova Scotia close-up

NS has 2.5% of Canada's jobs, so λ = 0.434 at δ = 0.25. FLQ flows below are the estimated coefficient times NS's real output, in $M.

### Summary

| NS, Summary | national | SLQ | CILQ | FLQ(0.25) |
|---|---:|---:|---:|---:|
| Multiplier bias % | +20.1 | +7.8 | +8.8 | −10.3 |
| Multiplier mean abs error %, output-weighted | 18.9 | 7.3 | 10.0 | 11.5 |
| Worst industry multiplier error % (abs) | 36.1 | 21.6 | 26.8 | 23.4 |
| NS output from NS's real final demand, % error | +18.5 | +6.4 | +5.7 | −12.2 |
| Local intermediate purchases, % error | +50.1 | +19.2 | +15.2 | −46.9 |

Total local inputs by buyer, $M:

| Buyer | Actual | FLQ | National, unadjusted |
|---|---:|---:|---:|
| Manufacturing | 2,575 | 1,777 | 4,938 |
| Finance, insurance, real estate | 2,484 | 1,321 | 3,293 |
| Federal government | 1,765 | 336 | 1,895 |
| Provincial government | 2,014 | 750 | 2,523 |
| Retail | 1,135 | 498 | 1,679 |
| Residential construction | 1,047 | 564 | 1,648 |
| Government health | 579 | 352 | 977 |
| Fishing | 166 | 11 | 368 |

Key cells, $M:

| Seller → buyer | Actual | FLQ |
|---|---:|---:|
| Fishing → manufacturing | 379 | 23 |
| Health care (business) → provincial government | 951 | 440 |
| FIRE → FIRE | 1,237 | 543 |
| Repair construction → federal government | 285 | 19 |
| Repair construction → FIRE | 281 | 93 |
| Manufacturing → manufacturing | 506 | 629 |
| Manufacturing → residential construction | 329 | 301 |
| Wholesale → manufacturing | 162 | 149 |

### Detail

Total local inputs by buyer, $M. SLQ is the buyer's jobs-based quotient in NS.

| Buyer | SLQ | Actual | FLQ | National, unadjusted | Local-input share, actual / FLQ |
|---|---:|---:|---:|---:|---:|
| Provincial government | 1.61 | 2,014 | 605 | 2,523 | 43% / 13% |
| Federal government (except defence) | 1.28 | 1,206 | 280 | 1,011 | 36% / 8% |
| Defence | 4.27 | 560 | 70 | 819 | 18% / 2% |
| Hospitals | 1.50 | 488 | 224 | 808 | 16% / 7% |
| Residential construction | 1.05 | 1,047 | 512 | 1,648 | 28% / 14% |
| Seafood processing | 10.38 | 672 | 415 | 982 | 40% / 25% |
| Fishing | 14.20 | 166 | 10 | 369 | 11% / 1% |
| Tires/rubber | 9.42 | 167 | 40 | 435 | 11% / 3% |
| Shipbuilding | 12.57 | 171 | 9 | 387 | 17% / 1% |

Key cells, $M:

| Seller → buyer | Actual | FLQ |
|---|---:|---:|
| Fishing → seafood processing | 375.4 | 231.0 |
| Seafood processing → seafood processing | 94.6 | 154.2 |
| Offices of physicians → provincial government | 925 | 260 |
| Repair construction → federal government | 258 | 18 |
| Engineering services → defence | 162 | 14 |
| Building materials wholesale → shipbuilding | 40.3 | 1.0 |
| Truck transportation → tires/rubber | 28.0 | 1.0 |

## What we learned

1. **FLQ(0.25) undercounts local buying across the board.** In NS at Summary, it puts local intermediate purchases at about half the real level (−47%), and multipliers come out 10% low.
2. **Locally bought services get the same import penalty as tradable goods.** λ applies to every input. Repair construction, physicians, FIRE and admin services are hard to import and are mostly bought locally even in a small region. In NS, FLQ often cuts them by half or more: repair construction → federal government is 285 actual vs 19 estimated. Goods flows come out closer.
3. **CILQ penalizes buyers the region specializes in.** It divides each supplier's quotient by the buyer's SLQ. At Summary this hits NS's federal and provincial government. At Detail, SLQs reach 4–14, so fishing, tires, shipbuilding and defence get 1–3% local-input shares against 11–18% actual. A large shipyard doesn't force the shipyard to import its trucking.
4. **Aggregation causes some errors, and Detail fixes them.** At Summary, national manufacturing barely buys fish, so fishing → manufacturing is 379 actual vs 23 estimated, even with the full national coefficient. At Detail, fishing → seafood processing is 375 vs 231.
5. **Diagonals of specialized industries are overestimated.** When SLQ × λ ≥ 1 the diagonal gets the full national coefficient, but these industries buy less from themselves locally. Examples: manufacturing → manufacturing at Summary, seafood → seafood at Detail.
6. **Some regional coefficients exceed national ones, and no LQ method can reach them.** At Detail, NS federal government's (non-defence) real local inputs ($1,206M) exceed what national coefficients alone give ($1,011M).

## Caveats

- **The national and provincial tables don't add up exactly.**
  - Summing `DomesticUse + InterprovImportUse` over all regions misses the national `Domestic` table by 1.25% of flows at Summary and 3.4% at Detail.
  - 46 Summary cells have more province-made input, summed across provinces, than the national table has from all of Canada.
  - Both come from the same release (supply and use tables of November 7, 2024). The likely cause is that each symmetric table is derived separately from its own supply-use table.
  - Differences this small aren't meaningful.
- **One year only,** and 2021 was a pandemic year.
- **Rough mapping spots:**
  - At Summary, NAICS 813 goes entirely to non-profits, though business associations belong to BS810.
  - Non-profits also run schools, clinics and arts groups, which the 813 mapping misses.
  - At Detail, business and non-profit education use all of NAICS 61, which is dominated by public schools and universities.
- **Multipliers hide most of the error.** The direct effect ("1") is exact, so a −47% miss on local purchases shows up as only −12% in NS output.
- **Not all of this is reproducible from the repo.** The Detail → Summary comparison and the NS close-ups came from scratch scripts that aren't saved here.

## Open

How to judge whether a regional table is good enough is not settled. That includes which numbers matter for the intended use, what tolerance counts as acceptable, and which provinces are realistic stand-ins for small sub-provincial regions.

## Code

- `src/small_io/io_table.py`: reads the workbooks and builds coefficients.
- `src/small_io/employment.py`: jobs data, the NAICS-to-IO mappings and SLQs.
- `src/small_io/flq.py`: SLQ, CILQ and FLQ matrices, and `FLEGG_TOHMO_DELTA = 0.25`.
- `src/small_io/compare.py`: error statistics and the LQ floor.
- `scripts/run_flq_provinces.py`: runs every province and writes `results/flq_provinces_{S,D}_2021.csv`.

```
uv run python scripts/run_flq_provinces.py --level S    # or --level D
uv run pytest
```
