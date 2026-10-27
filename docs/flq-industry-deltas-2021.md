# FLQ with one δ per industry: provincial test, 2021

Notes from 2026-10-27. All numbers are for 2021, the 10 provinces and the Summary level. Territories and CE are excluded. This follows [flq-provincial-test-2021.md](flq-provincial-test-2021.md), which uses a single fixed δ = 0.25. Data, location quotients and metrics are the same as there.

## Goal

Find out how much FLQ improves if each industry gets its own δ instead of one δ for all. This is an experiment. The main pipeline keeps the single δ = 0.25.

## Strategy

### δ by selling industry

Each selling industry i gets its own δ, applied across its whole row:

```
FLQ_ij   = CILQ_ij * lambda_i
lambda_i = [log2(1 + TRE/TNE)]^delta_i
r_ij     = min(FLQ_ij, 1) * a_ij
```

The δ belongs to the seller rather than the buyer, so that it can reflect how easily each input is imported. This targets the single-δ test's finding #2: services like repair construction and physicians are bought locally even in small regions, but one δ cuts them by as much as tradable goods.

In NS (2.5% of Canada's jobs), λ ranges from 1.00 at δ = 0 through 0.67 at δ = 0.12 and 0.43 at δ = 0.25, down to 0.26 at δ = 0.40.

### Fitting

```
loss_i(δ) = (1/10) Σ_p  Σ_j |r̂_pij(δ) X_pj − Z_pij|  /  Σ_ij Z_pij     # p = province
δ_i       = argmin of loss_i over δ ∈ {0, 0.01, …, 1}
```

- **Loss is the mean provincial WAPE.** Summed over sellers, `loss_i` is exactly the mean of the 10 provincial cell WAPEs, the headline number. Each province's errors are divided by its own total flows, so Ontario and Quebec don't set every δ.
- **Each δ is fitted on its own.** Row i depends only on δ_i, so each δ is a 1-D grid search over its row, pooled across the 10 provinces.
- **Rows that don't depend on δ keep 0.25.** These are industries that sell no intermediate inputs: residential, non-residential and engineering construction, owner-occupied dwellings, and other aboriginal government services.
- **Best single δ.** Adding all rows' loss curves together gives the best single δ: **0.12**.
- **In-sample only.** The δ's are fitted and scored on the same 10 provinces, about 27 parameters in all. The gain is an upper bound, like the LQ floor, not what a new region would get.

### What's compared

The fair comparison for per-industry δ is FLQ(0.12): the single δ fitted the same way to the same data. FLQ(0.25) is the fixed value from the single-δ test. CILQ is FLQ with δ = 0 for every industry.

## Results: all provinces

Means over the 10 provinces:

| | national | SLQ | CILQ | FLQ(0.25) | FLQ(0.12) | FLQ by industry | LQ floor |
|---|---:|---:|---:|---:|---:|---:|---:|
| Cell WAPE % | 66.9 | 45.3 | 45.5 | 45.0 | 40.6 | **34.2** | 10.4 |
| Multiplier bias % | +16.5 | +6.3 | +5.5 | −7.9 | −1.8 | −2.4 | |
| Local-input share error, pp | +10.0 | +4.2 | +3.3 | −6.9 | −1.9 | −2.3 | |

By province:

| | NL | PE | NS | NB | QC | ON | MB | SK | AB | BC | mean |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| WAPE %, FLQ(0.25) | 62.9 | 68.1 | 55.2 | 50.6 | 23.1 | 14.7 | 46.2 | 55.6 | 39.9 | 33.4 | 45.0 |
| WAPE %, FLQ(0.12) | 52.4 | 63.0 | 46.3 | 51.2 | 21.0 | 15.4 | 39.9 | 51.1 | 34.3 | 30.9 | 40.6 |
| WAPE %, by industry | 46.2 | 53.7 | 36.3 | 34.0 | 17.1 | 13.6 | 30.4 | 47.8 | 36.3 | 27.0 | 34.2 |
| LQ floor % | 15.3 | 23.0 | 11.6 | 10.1 | 3.5 | 3.0 | 6.9 | 12.5 | 9.7 | 8.4 | 10.4 |
| Multiplier bias %, FLQ(0.12) | −5.5 | −2.6 | −2.6 | −2.0 | +0.1 | +2.9 | +1.2 | −3.5 | −5.4 | −0.9 | −1.8 |
| Multiplier bias %, by industry | −5.6 | −3.0 | −3.1 | −3.2 | 0.0 | +2.0 | +0.1 | −3.9 | −5.5 | −1.7 | −2.4 |

- **Per-industry δ cuts mean WAPE by 6.4 points** over the best single δ (40.6% → 34.2%), and by 10.8 over FLQ(0.25).
- **Small provinces gain most:** NB −17.2 points, NS −10.0, MB −9.5, PE −9.3.
- **Alberta gets worse** (34.3% → 36.3%). Most of that is Manufacturing: its δ of 0.28 adds 2.4 points to AB's WAPE and takes 4.8 off NS's.
- **Multiplier bias barely moves,** and is slightly worse than FLQ(0.12). The fit targets cell error, and per-industry δ mostly moves local purchases between sellers rather than changing their total.

### Fitted δ's

The error column is each seller's share of the mean provincial WAPE, in percentage points. It sums to 40.6 at δ = 0.12 and 34.2 at each seller's own δ.

| δ | Seller | Error at 0.12 → own δ, pp |
|---:|---|---:|
| 0.00 | Repair construction | 2.99 → 2.57 |
| 0.00 | Retail trade | 1.53 → 1.15 |
| 0.00 | Other municipal government services | 0.46 → 0.43 |
| 0.00 | Non-profit institutions serving households | 0.27 → 0.26 |
| 0.00 | Support activities for agriculture and forestry | 0.27 → 0.21 |
| 0.01 | Finance, insurance, real estate (FIRE) | 4.29 → 2.64 |
| 0.01 | Utilities | 1.50 → 1.29 |
| 0.03 | Other provincial government services | 0.73 → 0.73 |
| 0.04 | Other federal government services | 0.30 → 0.29 |
| 0.05 | Accommodation and food services | 0.73 → 0.68 |
| 0.05 | Government education services | 0.25 → 0.25 |
| 0.06 | Educational services | 0.25 → 0.25 |
| 0.09 | Other services | 0.57 → 0.57 |
| 0.10 | Health care and social assistance | 1.75 → 1.72 |
| 0.10 | Government health services | 0.57 → 0.57 |
| 0.11 | Professional, scientific and technical services | 2.75 → 2.75 |
| 0.11 | Other activities of the construction industry | 0.11 → 0.11 |
| 0.13 | Transportation and warehousing | 2.44 → 2.41 |
| 0.13 | Administrative and support, waste management | 1.61 → 1.60 |
| 0.16 | Information and cultural industries | 0.89 → 0.88 |
| 0.17 | Forestry and logging | 0.63 → 0.62 |
| 0.20 | Arts, entertainment and recreation | 0.21 → 0.20 |
| 0.24 | Wholesale trade | 1.89 → 1.60 |
| 0.28 | Manufacturing | 6.81 → 4.55 |
| 0.29 | Crop and animal production | 2.67 → 2.57 |
| 0.39 | Fishing, hunting and trapping | 1.31 → 1.30 |
| 0.40 | Mining, quarrying, and oil and gas extraction | 2.78 → 2.02 |

- **Services want little or no penalty, goods want more.**
  - Most services fit δ = 0–0.13.
  - Goods producers fit 0.28–0.40.
  - Wholesale, forestry and arts sit between.
- **Best single δ is a compromise.** The best single δ of 0.12 falls between the two groups. Manufacturing alone did almost as well at 0.25 (4.62) as at its own δ.
- **Seven sellers account for 94% of the gain** over FLQ(0.12): Manufacturing 2.3 points, FIRE 1.7, mining 0.8, repair construction 0.4, retail 0.4, wholesale 0.3, utilities 0.2. Most other rows barely change.
- **Five sellers end at δ = 0,** the lowest the formula allows. None end at 1.

## Nova Scotia close-up

NS flows below are the estimated coefficient times NS's real output, in $M. "National" is the unadjusted national coefficient times NS's output.

### Summary statistics

| NS, Summary | national | CILQ | FLQ(0.25) | FLQ(0.12) | FLQ by industry |
|---|---:|---:|---:|---:|---:|
| Cell WAPE % | 73.2 | 54.0 | 55.2 | 46.3 | 36.3 |
| Multiplier bias % | +20.1 | +8.8 | −10.3 | −2.6 | −3.1 |
| Multiplier mean abs error %, output-weighted | 18.9 | 10.0 | 11.5 | 6.2 | 5.7 |
| Worst industry multiplier error % (abs) | 36.1 | 26.8 | 23.4 | 18.2 | 17.3 |
| NS output from NS's real final demand, % error | +18.5 | +5.7 | −12.2 | −5.1 | −5.4 |
| Local intermediate purchases, % error | +50.1 | +15.2 | −46.9 | −18.9 | −19.5 |

Per-industry δ cuts NS's cell error by 10 points over FLQ(0.12). Total local purchases stay where they were, about 19% short. The worst multiplier under both FLQ(0.12) and per-industry δ is federal government's.

### Local sales by seller

Each seller's total sales to NS industries, $M:

| Seller | δ | SLQ | Actual | National | FLQ(0.25) | FLQ(0.12) | By industry |
|---|---:|---:|---:|---:|---:|---:|---:|
| FIRE | 0.01 | 0.77 | 3,612 | 4,727 | 1,557 | 2,398 | 3,434 |
| Manufacturing | 0.28 | 0.83 | 1,872 | 5,377 | 1,945 | 2,992 | 1,761 |
| Professional services | 0.11 | 0.71 | 1,798 | 3,136 | 966 | 1,482 | 1,532 |
| Transportation and warehousing | 0.13 | 0.76 | 1,387 | 2,216 | 759 | 1,167 | 1,129 |
| Repair construction | 0.00 | 0.76 | 1,377 | 1,265 | 415 | 639 | 950 |
| Health care (business) | 0.10 | 1.25 | 1,299 | 1,742 | 620 | 957 | 1,022 |
| Retail | 0.00 | 1.18 | 978 | 821 | 412 | 624 | 748 |
| Utilities | 0.01 | 1.10 | 907 | 571 | 287 | 437 | 531 |
| Wholesale | 0.24 | 0.73 | 712 | 1,642 | 525 | 804 | 542 |
| Crop and animal production | 0.29 | 0.92 | 451 | 717 | 329 | 509 | 288 |
| Fishing | 0.39 | 14.20 | 395 | 30 | 30 | 30 | 30 |
| Mining, oil and gas | 0.40 | 0.22 | 116 | 1,203 | 139 | 214 | 84 |

- **FIRE and Manufacturing are now close.** FIRE is 3,434 vs 3,612 actual. Manufacturing is 1,761 vs 1,872, where a single δ either under- or overshoots it.
- **Repair construction, retail and utilities sell more in NS than national coefficients imply.** No scaling-down method can reach their actuals: repair construction is 1,377 actual vs 1,265 even unadjusted, and utilities 907 vs 571. This is why their δ's sit at 0. A negative δ would only help the cells where CILQ is below 1, because each cell is still capped at its national coefficient.
- **Fishing's δ is irrelevant in NS.** Its SLQ of 14.2 puts every cell at the cap at any δ. National coefficients themselves only give 30 against 395 actual: the Summary aggregation problem from the single-δ test, finding #4.
- **Mining's high δ (0.40) is right for NS.** National coefficients would have NS sell 1,203 locally against 116 actual.

### Local purchases by buyer

Each buyer's total local inputs, $M:

| Buyer | SLQ | Actual | FLQ(0.25) | FLQ(0.12) | By industry | National |
|---|---:|---:|---:|---:|---:|---:|
| Manufacturing | 0.83 | 2,575 | 1,777 | 2,727 | 2,057 | 4,938 |
| FIRE | 0.77 | 2,484 | 1,321 | 2,017 | 2,426 | 3,293 |
| Provincial government | 1.61 | 2,014 | 750 | 1,155 | 1,256 | 2,523 |
| Federal government | 2.10 | 1,765 | 336 | 514 | 572 | 1,895 |
| Retail | 1.18 | 1,135 | 498 | 767 | 890 | 1,679 |
| Residential construction | 1.05 | 1,047 | 564 | 870 | 709 | 1,648 |
| Owner-occupied dwellings | 1.00 | 658 | 253 | 391 | 562 | 758 |
| Government health | 1.25 | 579 | 352 | 543 | 571 | 977 |
| Fishing | 14.20 | 166 | 11 | 16 | 15 | 368 |

- **Buyers that mostly purchase services improve most.** FIRE, owner-occupied dwellings and retail are now 2%, 15% and 22% short.
- **Buyers that mostly purchase goods move down.** Manufacturing and residential construction fall, because Manufacturing as a seller now has a higher δ. Manufacturing goes from 6% over to 20% under.
- **The two governments are still far short.** Provincial government is at 62% of actual, federal government at 32%. CILQ divides every seller's quotient by the buyer's SLQ (1.61 and 2.10). A seller-side δ can't undo that: the single-δ test's finding #3.

### Key cells

$M:

| Seller → buyer | Actual | National | FLQ(0.25) | FLQ(0.12) | By industry |
|---|---:|---:|---:|---:|---:|
| FIRE → FIRE | 1,237 | 1,623 | 543 | 838 | 1,210 |
| FIRE → retail | 525 | 604 | 171 | 265 | 382 |
| Repair construction → owner-occupied dwellings | 461 | 409 | 134 | 208 | 310 |
| Repair construction → FIRE | 281 | 218 | 93 | 144 | 215 |
| Manufacturing → manufacturing | 506 | 1,752 | 629 | 972 | 569 |
| Manufacturing → residential construction | 329 | 878 | 301 | 464 | 272 |
| Mining → manufacturing | 37 | 859 | 101 | 156 | 61 |
| Wholesale → manufacturing | 162 | 391 | 149 | 230 | 154 |
| Crops → manufacturing | 333 | 519 | 251 | 387 | 219 |
| Health care (business) → provincial government | 951 | 1,304 | 440 | 679 | 726 |
| Fishing → manufacturing | 379 | 23 | 23 | 23 | 23 |

- **Services sold to services are now close.** FIRE → FIRE and manufacturing → manufacturing were the two biggest single gains in NS.
- **Manufacturing's diagonal is close again** (569 vs 506). FLQ(0.12) overstated it by 92%. The single-δ test's finding #5 was about this cell.
- **One δ per seller applies to every buyer.** Crops' δ of 0.29 fits on average but cuts crops → manufacturing (NS food processing) from 387 to 219, against 333 actual.

### Largest errors left

The biggest cells per-industry δ still misses, $M:

| Seller → buyer | Actual | National | By industry |
|---|---:|---:|---:|
| Fishing → manufacturing | 379 | 23 | 23 |
| Professional services → federal government | 370 | 443 | 104 |
| Repair construction → federal government | 285 | 123 | 44 |
| Health care (business) → provincial government | 951 | 1,304 | 726 |
| Repair construction → owner-occupied dwellings | 461 | 409 | 310 |
| Manufacturing → federal government | 169 | 137 | 21 |
| Government health → federal government | 147 | 38 | 16 |
| Transportation → federal government | 143 | 118 | 28 |
| Repair construction → provincial government | 151 | 79 | 37 |
| Administrative services → provincial government | 130 | 42 | 15 |

Most of these cells involve a government buyer, for two separate reasons:
- **The buyer-SLQ division:** professional services → federal government is 104 against 370 actual, though national coefficients give 443.
- **The LQ floor:** government health → federal government is 147 actual vs 38 even from national coefficients.

## What we learned

1. **The single best δ blends two groups.** Services sold to local buyers fit δ ≈ 0–0.1; goods fit about 0.3. Fitting them separately cuts mean WAPE from 40.6% to 34.2% in-sample, and the improvement is largest in the small provinces.
2. **Seller tradability matters, as the single-δ test suspected.** FIRE, repair construction, retail and utilities are bought locally even in NS. With δ near 0, NS's FIRE sales and FIRE → FIRE come out nearly right.
3. **Per-industry δ fixes the mix of local purchases, not their total.** NS local intermediate purchases are about 19% short with either FLQ(0.12) or per-industry δ, and multiplier bias is essentially unchanged. If multipliers are what matter for impact analysis, the best single δ already gets most of the way.
4. **Three error sources are untouched:**
   - CILQ's division by the buyer's SLQ. NS's governments still get a third to two-thirds of their real local inputs.
   - Summary aggregation: fishing → manufacturing.
   - The LQ floor: repair construction, retail and utilities sell more locally than national coefficients allow. That's why five δ's end at 0.
5. **One δ per seller is still a compromise across buyers and provinces.** Manufacturing's 0.28 helps NS by 4.8 points and costs AB 2.4. Crops' 0.29 undercuts NS's food processing.

## Caveats

- **In-sample.** About 27 δ's are fitted to the same 10 provinces they're scored on. 34.2% is a best case; leave-one-province-out or another year would show how much of it holds up.
- **One year (2021, a pandemic year), Summary level only.**
- **δ is limited to [0, 1] in steps of 0.01.** Ties go to the δ nearest 0.25.
- **The NS close-up isn't reproducible from the repo.** It came from a scratch script that isn't saved here. The province tables and fitted δ's are reproducible.

## Open

- Do the δ's hold up on other years or held-out provinces?
- Does Detail level, which already fixes some aggregation errors, change the pattern? Answered in [flq-industry-deltas-detail-2021.md](flq-industry-deltas-detail-2021.md): a single δ at Detail, added up to Summary, beats per-industry δ at Summary.
- The buyer-SLQ division is now the largest fixable error in NS. Should CILQ's buyer term be revisited separately?

## Code

- `src/small_io/flq.py`: `flq_matrix` accepts a δ per industry (a Series), applied by selling row.
- `src/small_io/io_table.py`: `industry_names` reads industry titles from the national table.
- `scripts/fit_industry_deltas.py`: fits the δ's, compares methods across provinces, and writes `results/industry_deltas_S_2021.csv` (δ and row errors by industry) and `results/fit_industry_deltas_S_2021.csv` (statistics by province and method).

```
uv run python scripts/fit_industry_deltas.py
uv run pytest
```
