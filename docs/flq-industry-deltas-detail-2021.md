# FLQ with one δ per industry: Detail level, 2021

Notes from 2026-10-27. All numbers are for 2021 and the 10 provinces. Territories and CE are excluded. This repeats [flq-industry-deltas-2021.md](flq-industry-deltas-2021.md) on the Detail table (234 industries, $K) instead of Summary (32). Data, location quotients and metrics are the same as in [flq-provincial-test-2021.md](flq-provincial-test-2021.md).

## Goal

Fit one δ per selling industry at Detail level, and compare it fairly with the Summary-level fit.

## Strategy

### Fitting

The method is the same as at Summary:
- one δ per selling industry, applied across its row;
- each δ grid-searched over 0, 0.01, …, 1;
- the loss is the mean of the 10 provincial cell WAPEs, here on the 234 × 234 table.

Results:
- **Best single δ is 0.06**, down from 0.12 at Summary.
- **Twelve rows don't depend on δ and keep 0.25.** They sell no intermediate inputs: building and engineering construction, unlicensed cannabis stores, owner-occupied dwellings, private households, other educational services and other aboriginal government services.
- **That leaves 222 fitted δ's** for 10 provinces, all scored in-sample.

### Scoring at Summary

Cell WAPE on a 234 × 234 table isn't comparable with a 32 × 32 one, because a finer table has more cells to miss. The fair comparison adds each Detail estimate up to Summary and scores it against the real Summary table:

```
Ẑ_ij  = r̂_ij X_j                        # Detail, the province's real Detail output
Ẑ_IJ  = Σ_{i∈I, j∈J} Ẑ_ij                # I, J = Summary industries
r̂_IJ  = Ẑ_IJ / X_J                       # scored against the real Summary DomesticUse table
```

- **The concordance is a prefix rule.** Each Detail code maps to a Summary industry by its NAICS digits. Holding companies (`BS551113`) go to FIRE.
- **It reproduces the Summary tables.** The national and NS Detail tables add up to their Summary tables to within $10K (`tests/test_data.py`).
- **It reproduces the earlier Detail → Summary result.** The single-δ test reported 42.8% WAPE and −9.1% multiplier bias for FLQ(0.25); this gives the same.
- **The δ's are fitted on Detail error, not on the Summary score.**

## Results: all provinces

### Scored at Detail

Means over the 10 provinces:

| | national | SLQ | CILQ | FLQ(0.25) | FLQ(0.06) | FLQ by industry | LQ floor |
|---|---:|---:|---:|---:|---:|---:|---:|
| Cell WAPE % | 72.5 | 51.7 | 52.2 | 57.3 | 51.6 | **47.1** | 15.8 |
| Multiplier bias % | +17.0 | +3.8 | +4.5 | −5.6 | +2.0 | −1.1 | |
| Local-input share error, pp | +10.7 | +2.5 | +3.2 | −4.4 | +1.5 | −0.8 | |

At Detail, per-industry δ cuts mean WAPE by 4.5 points over the best single δ. At Summary the gain was 6.4 points.

### Scored at Summary: the fair comparison

Means over the 10 provinces, every estimate scored against the real Summary table:

| | FLQ(0.25) | Best single δ | δ by industry |
|---|---:|---:|---:|
| Cell WAPE %, fitted at Summary | 45.0 | 40.6 (δ = 0.12) | 34.2 |
| Cell WAPE %, fitted at Detail and added up | 42.8 | **31.2** (δ = 0.06) | **30.0** |
| Multiplier bias %, fitted at Summary | −7.9 | −1.8 | −2.4 |
| Multiplier bias %, fitted at Detail and added up | −9.1 | −1.9 | −4.0 |
| Local-input share error, pp, fitted at Summary | −6.9 | −1.9 | −2.3 |
| Local-input share error, pp, fitted at Detail and added up | −7.9 | −1.7 | −3.4 |

- **Working at Detail beats per-industry δ.** A single δ at Detail scores 31.2%, better than one δ per industry at Summary (34.2%), with a little less bias.
- **Per-industry δ at Detail adds only 1.2 points at Summary,** against 4.5 points when scored at Detail. Part of the Detail gain comes from moving flows between Detail cells inside the same Summary cell, and that cancels out when the cells are added up.
- **It also lowers totals.** Multiplier bias doubles (−1.9% → −4.0%), and the local-input share error goes from −1.7 to −3.4 points.

By province:

| | NL | PE | NS | NB | QC | ON | MB | SK | AB | BC | mean |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Detail WAPE %, FLQ(0.25) | 76.9 | 79.1 | 65.1 | 64.3 | 40.7 | 26.9 | 60.1 | 64.6 | 49.9 | 45.5 | 57.3 |
| Detail WAPE %, FLQ(0.06) | 68.0 | 73.4 | 58.0 | 56.4 | 37.6 | 25.6 | 52.9 | 58.2 | 45.1 | 41.2 | 51.6 |
| Detail WAPE %, by industry | 59.4 | 67.1 | 52.2 | 50.7 | 35.9 | 25.0 | 45.5 | 52.8 | 44.5 | 38.0 | 47.1 |
| Detail LQ floor % | 22.1 | 28.2 | 17.3 | 17.3 | 10.8 | 7.1 | 13.4 | 16.1 | 13.6 | 12.1 | 15.8 |
| Detail → Summary WAPE %, FLQ(0.06) | 44.8 | 48.9 | 37.9 | 34.2 | 19.5 | 11.4 | 29.4 | 35.4 | 27.2 | 23.4 | 31.2 |
| Detail → Summary WAPE %, by industry | 43.7 | 49.5 | 33.8 | 31.6 | 20.6 | 12.6 | 24.2 | 32.4 | 30.1 | 21.9 | 30.0 |
| Summary fit, by industry, for comparison | 46.2 | 53.7 | 36.3 | 34.0 | 17.1 | 13.6 | 30.4 | 47.8 | 36.3 | 27.0 | 34.2 |
| Detail → Summary multiplier bias %, FLQ(0.06) | −4.9 | −2.6 | −1.5 | −1.4 | −1.0 | +1.0 | +0.2 | −2.5 | −4.1 | −1.9 | −1.9 |
| Detail → Summary multiplier bias %, by industry | −6.9 | −4.4 | −4.1 | −3.6 | −2.9 | −0.4 | −2.5 | −4.8 | −6.2 | −4.2 | −4.0 |

- **At Detail, per-industry δ helps every province.**
- **Scored at Summary, it is worse than the single Detail δ in PE, QC, ON and AB.**
- **AB is no worse than at Summary** (30.1% against 36.3% for the Summary per-industry fit). At Summary, Manufacturing's single δ was the problem; at Detail, manufacturing industries get their own δ's.

### Fitted δ's

- **Distribution.** Of the 222 fitted δ's, the median is 0.16 and the quartiles are 0.01 and 0.36. Weighted by local sales, the mean is 0.14.
- **Bounds.** 55 end at 0 and 6 at 1.
- **Noise.** Twenty rows each contribute less than 0.01 points of WAPE, so their δ's are noise. Diamond mining's δ of 1, for example, rests on $1.4K of local sales.

Detail δ's grouped by their Summary industry:

| Summary industry | Detail rows | δ, local-sales-weighted mean | δ range | Summary δ | Gain over FLQ(0.06), pp |
|---|---:|---:|---:|---:|---:|
| Fishing, hunting and trapping | 1 | 0.00 | | 0.39 | 0.02 |
| Repair construction | 1 | 0.00 | | 0.00 | 0.18 |
| Other municipal government services | 1 | 0.00 | | 0.00 | 0.01 |
| Other federal government services | 2 | 0.00 | 0–0.13 | 0.04 | 0.00 |
| Accommodation and food services | 3 | 0.00 | 0–0.39 | 0.05 | 0.02 |
| Crop and animal production | 6 | 0.01 | 0–0.29 | 0.29 | 0.20 |
| Retail trade | 13 | 0.01 | 0–0.31 | 0.00 | 0.11 |
| Forestry and logging | 1 | 0.01 | | 0.17 | 0.05 |
| Support activities for agriculture and forestry | 2 | 0.02 | 0–0.03 | 0.00 | 0.02 |
| Other provincial government services | 1 | 0.03 | | 0.03 | 0.00 |
| Educational services | 1 | 0.03 | | 0.06 | 0.00 |
| FIRE | 14 | 0.05 | 0–0.49 | 0.01 | 0.33 |
| Utilities | 3 | 0.05 | 0–0.62 | 0.01 | 0.07 |
| Health care and social assistance | 5 | 0.05 | 0–0.31 | 0.10 | 0.13 |
| Other services | 6 | 0.09 | 0–0.33 | 0.09 | 0.02 |
| Transportation and warehousing | 13 | 0.10 | 0–0.55 | 0.13 | 0.11 |
| Other activities of the construction industry | 1 | 0.11 | | 0.11 | 0.00 |
| Professional, scientific and technical services | 9 | 0.13 | 0.02–0.29 | 0.11 | 0.29 |
| Administrative and support, waste management | 8 | 0.14 | 0.02–0.23 | 0.13 | 0.08 |
| Arts, entertainment and recreation | 3 | 0.14 | 0.05–0.49 | 0.20 | 0.01 |
| Government health services | 2 | 0.16 | 0.15–0.22 | 0.10 | 0.02 |
| Non-profit institutions serving households | 7 | 0.20 | 0–0.57 | 0.00 | 0.02 |
| Wholesale trade | 9 | 0.21 | 0.08–0.50 | 0.24 | 0.36 |
| Information and cultural industries | 11 | 0.26 | 0–0.71 | 0.16 | 0.33 |
| Manufacturing | 82 | 0.30 | 0–1 | 0.28 | 1.79 |
| Government education services | 3 | 0.33 | 0–0.76 | 0.05 | 0.04 |
| Mining, quarrying, and oil and gas extraction | 14 | 0.42 | 0–1 | 0.40 | 0.29 |

- **Group averages match the Summary δ's.** Examples: Manufacturing 0.30 vs 0.28, mining 0.42 vs 0.40, wholesale 0.21 vs 0.24, professional services 0.13 vs 0.11, transportation 0.10 vs 0.13. The services-low, goods-high pattern holds.
- **Primary industries flip to δ ≈ 0:**
  - fishing, from 0.39 at Summary;
  - crops and animals, from 0.29;
  - forestry, from 0.17.

  At Summary their main buyer is all of Manufacturing, and national manufacturing barely buys fish. At Detail the buyers are seafood processing, meat and food processing, and sawmills, and these buy their inputs locally.
- **Within groups, δ follows how tradable the product is:**
  - Manufacturing ranges from cement and concrete (0.05), furniture (0.02) and animal food (0.07) up to meat (0.59), grain milling (0.87), dairy (0.95), fruit and vegetable preserving (1.00) and non-ferrous metals (1.00).
  - Information has telecommunications at 0.00, but software publishers at 0.71, data processing at 0.69 and pay TV at 0.67.
  - Transportation has rail at 0.01 and trucking at 0.09, but air at 0.36.

  So the split is between products sold close to home and products shipped far, rather than simply goods and services.
- **The gain is spread thin.** The top 10 rows give 36% of the 4.5 points and the top 40 give 75%. Manufacturing's 82 rows give 1.8 points. The biggest single gains are meat products, computer systems design, repair construction, non-ferrous metals, food wholesale and dairy.
- **δ = 1:**
  - oil and gas extraction (except oil sands);
  - non-ferrous metals;
  - fruit and vegetable preserving;
  - resins and synthetic rubber;
  - tobacco;
  - diamond mining, which is noise.

## Nova Scotia close-up

Flows are the estimated coefficient times NS's real output, in $M. "National" is the unadjusted national coefficient times NS's output.

### Summary statistics

| NS, Detail | national | CILQ | FLQ(0.25) | FLQ(0.06) | FLQ by industry |
|---|---:|---:|---:|---:|---:|
| Cell WAPE % | 76.1 | 59.4 | 65.1 | 58.0 | 52.2 |
| Cell WAPE %, added up and scored at Summary | 59.7 | 39.2 | 52.7 | 37.9 | 33.8 |
| Multiplier bias % | +18.9 | +7.4 | −6.0 | +4.0 | +0.3 |
| Multiplier mean abs error %, output-weighted | 15.3 | 7.4 | 12.3 | 7.0 | 7.1 |
| Worst industry multiplier error % (abs) | 81.4 | 61.4 | 44.0 | 56.5 | 50.7 |
| NS output from NS's real final demand, % error | +15.1 | −0.5 | −12.9 | −4.0 | −6.3 |
| Local intermediate purchases, % error | +41.4 | −3.2 | −49.6 | −14.7 | −22.5 |

- **Best NS score so far.** Scored at Summary, per-industry δ at Detail gives NS 33.8%. The Summary per-industry fit gave 36.3%, and FLQ(0.25) 55.2%.
- **Totals fall further short.** Local purchases go from −14.7% at FLQ(0.06) to −22.5%, and output from −4.0% to −6.3%.
- **The near-zero multiplier bias (+0.3%) is misleading.** It is an unweighted average over 234 industries. The output-weighted error is unchanged at about 7%.
- **CILQ (δ = 0 for every industry) gets NS's totals almost exactly right at Detail** (local purchases −3.2%, output −0.5%), though its cells are worse.
- **Grain and oilseed milling has the worst multiplier under every method.**

### Local sales by seller

Each seller's total sales to NS industries, $M:

| Seller | δ | SLQ | Actual | National | FLQ(0.25) | FLQ(0.06) | By industry |
|---|---:|---:|---:|---:|---:|---:|---:|
| Repair construction | 0.00 | 0.76 | 1,377 | 1,294 | 387 | 718 | 866 |
| Lessors of real estate | 0.07 | 1.38 | 984 | 959 | 586 | 889 | 879 |
| Offices of physicians | 0.00 | 0.84 | 948 | 1,195 | 269 | 508 | 620 |
| Electric power | 0.00 | 1.03 | 880 | 503 | 213 | 366 | 407 |
| Banking | 0.00 | 0.84 | 709 | 1,031 | 453 | 750 | 845 |
| Insurance carriers | 0.00 | 0.67 | 527 | 616 | 190 | 347 | 410 |
| Architectural and engineering services | 0.02 | 0.66 | 502 | 750 | 175 | 323 | 364 |
| Truck transportation | 0.09 | 0.72 | 444 | 728 | 232 | 421 | 384 |
| Fishing | 0.00 | 14.20 | 395 | 400 | 242 | 400 | 400 |
| Telecommunications | 0.00 | 0.86 | 365 | 408 | 166 | 295 | 340 |
| Computer systems design | 0.29 | 0.65 | 281 | 737 | 226 | 417 | 198 |
| Building material wholesale | 0.14 | 0.76 | 267 | 411 | 130 | 238 | 186 |
| Hospitals | 0.15 | 1.50 | 250 | 216 | 109 | 182 | 148 |
| Seafood processing | 0.40 | 10.38 | 133 | 163 | 161 | 162 | 161 |

- **Fishing is right** (400 vs 395 actual; FLQ(0.25) gave 242). The low single δ already fixed it: any δ up to about 0.09 gives fishing → seafood processing its full national coefficient.
- **Physicians, repair construction and electric power reach δ = 0 and are still short:**
  - Physicians (620 vs 948): mostly CILQ's division by the buyer's SLQ. Their biggest buyer is provincial government.
  - Repair construction (1,377 actual vs 1,294 even from national coefficients) and electric power (880 vs 503): both sell more than national coefficients allow, so no scaling-down method can reach them.
- **Two pooled δ's miss NS in opposite directions:**
  - Computer systems design's δ of 0.29 takes it from 417 to 198, against 281 actual.
  - Banking at δ = 0 overshoots: 845 vs 709.
- **Seafood processing is stuck at its national coefficients.** With an SLQ of 10.38, its cells are capped at any δ up to about 0.70, and its pooled δ is 0.40.

### Local purchases by buyer

Each buyer's total local inputs, $M:

| Buyer | SLQ | Actual | FLQ(0.25) | FLQ(0.06) | By industry | National |
|---|---:|---:|---:|---:|---:|---:|
| Provincial government | 1.61 | 2,014 | 605 | 1,126 | 1,150 | 2,507 |
| Federal government (except defence) | 1.28 | 1,206 | 280 | 525 | 493 | 999 |
| Residential construction | 1.05 | 1,047 | 512 | 946 | 742 | 1,602 |
| Lessors of real estate | 1.38 | 776 | 219 | 411 | 435 | 834 |
| Seafood processing | 10.38 | 672 | 415 | 600 | 590 | 973 |
| Owner-occupied dwellings | 1.00 | 658 | 248 | 467 | 554 | 758 |
| Defence | 4.27 | 560 | 70 | 129 | 117 | 786 |
| Hospitals | 1.50 | 488 | 224 | 415 | 341 | 800 |
| Food services and drinking places | 1.09 | 369 | 238 | 436 | 302 | 730 |
| Shipbuilding | 12.57 | 171 | 9 | 16 | 13 | 321 |
| Rubber products | 9.42 | 167 | 40 | 50 | 45 | 381 |
| Fishing | 14.20 | 166 | 10 | 18 | 16 | 287 |

- **Governments and specialized buyers are far short at every δ:**

  | Buyer | Share of actual local inputs, by industry |
  |---|---:|
  | Provincial government | 57% |
  | Federal government (except defence) | 41% |
  | Defence | 21% |
  | Rubber products | 27% |
  | Fishing | 9% |
  | Shipbuilding | 8% |

  CILQ divides every seller's quotient by the buyer's SLQ (1.3 to 14), and no seller-side δ can undo that. This is the single-δ test's finding #3, unchanged.
- **Buyers that mostly purchase goods fall.** Residential construction goes from 946 to 742 (against 1,047) as wood, plastic and metal products get higher δ's. Food services goes from 436 to 302 (against 369), mostly from dairy and meat. That one moves closer.
- **Owner-occupied dwellings improve** (467 → 554, against 658), mostly from repair construction's δ of 0.

### Key cells

The cells from the single-δ test's Detail close-up, $M:

| Seller → buyer | Actual | National | FLQ(0.25) | FLQ(0.06) | By industry |
|---|---:|---:|---:|---:|---:|
| Fishing → seafood processing | 375.4 | 389.3 | 231.0 | 389.3 | 389.3 |
| Seafood processing → seafood processing | 94.6 | 154.2 | 154.2 | 154.2 | 154.2 |
| Offices of physicians → provincial government | 925 | 1,149 | 260 | 490 | 598 |
| Repair construction → federal government (except defence) | 258 | 69 | 18 | 34 | 41 |
| Engineering services → defence | 162.5 | 214.6 | 14.4 | 27.2 | 31.1 |
| Building materials wholesale → shipbuilding | 40.3 | 39.2 | 1.0 | 1.9 | 1.5 |
| Truck transportation → rubber products | 28.0 | 29.2 | 1.0 | 1.8 | 1.7 |

Fishing → seafood processing is right with any low δ. Seafood processing → seafood processing is capped at its national coefficient, so no δ in the fitted range changes it. The single-δ test's finding #5 holds. The cells sold to specialized buyers (defence, shipbuilding, rubber) hardly move.

Cells that changed most compared with FLQ(0.06), $M:

| Seller → buyer | Seller's δ | Actual | FLQ(0.06) | By industry |
|---|---:|---:|---:|---:|
| Offices of physicians → provincial government | 0.00 | 925 | 490 | 598 |
| Repair construction → owner-occupied dwellings | 0.00 | 461 | 254 | 310 |
| Other wood products → residential construction | 0.45 | 14.0 | 54.1 | 14.7 |
| Plastic products → residential construction | 0.30 | 23.1 | 61.9 | 27.8 |
| Dairy products → food services | 0.95 | 3.0 | 37.1 | 1.9 |
| Meat products → food services | 0.59 | 4.0 | 35.4 | 6.0 |
| Nursing and residential care → hospitals | 0.31 | 29.9 | 61.4 | 26.6 |
| Food wholesale → food services | 0.47 | 7.3 | 29.6 | 7.5 |
| *Worse:* | | | | |
| Computer systems design → computer systems design | 0.29 | 67.4 | 65.7 | 30.5 |
| Banking → owner-occupied dwellings | 0.00 | 91.8 | 125.2 | 153.0 |
| Forestry → sawmills | 0.01 | 132.6 | 131.9 | 155.9 |
| Miscellaneous ambulatory health care → hospitals | 0.16 | 147.4 | 76.4 | 54.7 |
| Telecommunications → telecommunications | 0.00 | 86.6 | 90.8 | 111.0 |

- **NS imports manufactured goods sold to construction and restaurants.** High δ's for wood, plastic, dairy and meat products get these cells nearly exactly right.
- **The losses are the same pooled-δ problem as at Summary.** A δ that fits the 10 provinces on average misses NS's own cells, in either direction.

### Largest errors left

The biggest cells per-industry δ still misses in NS, $M:

| Seller → buyer | Actual | National | By industry | Buyer's SLQ |
|---|---:|---:|---:|---:|
| Offices of physicians → provincial government | 925 | 1,149 | 598 | 1.61 |
| Repair construction → owner-occupied dwellings | 461 | 409 | 310 | 1.00 |
| Repair construction → lessors of real estate | 275 | 239 | 132 | 1.38 |
| Repair construction → federal government (except defence) | 258 | 69 | 41 | 1.28 |
| Engineering services → defence | 163 | 215 | 31 | 4.27 |
| Repair construction → provincial government | 151 | 80 | 37 | 1.61 |
| Miscellaneous ambulatory health care → hospitals | 147 | 166 | 55 | 1.50 |
| Hospitals → federal government (except defence) | 145 | 24 | 17 | 1.28 |
| Electric power → municipal government | 116 | 25 | 25 | 0.82 |
| Provincial government → provincial government | 111 | 39 | 39 | 1.61 |
| Provincial government → municipal government | 108 | 28.5 | 28.5 | 0.82 |
| Aerospace products → defence | 86 | 38 | 5.5 | 4.27 |

These cells fall into two groups:
- **Cut by the buyer's SLQ.** The national coefficient is above actual, but CILQ's division by the buyer's SLQ cuts the estimate below it. Examples: physicians → provincial government, engineering services → defence, ambulatory health care → hospitals.
- **Above the LQ floor.** Actual is above even the national coefficient, so no scaling-down can reach it. Examples: repair construction's government sales, hospitals → federal government, electric power and provincial government → municipal government.

Nearly all the largest errors involve a government buyer or repair construction.

## What we learned

1. **Detail level matters more than per-industry δ.** A single δ fitted at Detail, added up to Summary, scores 31.2% WAPE, better than a δ for every industry at Summary (34.2%). Its multiplier bias is −1.9%.
2. **Per-industry δ at Detail barely survives adding up.** It gains 4.5 points at Detail but only 1.2 at Summary. It is worse than the single Detail δ in four provinces, and it doubles the multiplier bias to −4.0%.
3. **δ tracks tradability, and it shows more clearly at Detail.** Products sold close to home get δ ≈ 0: concrete, telecoms, trucking, banking, physicians. Products shipped long distances get 0.6–1: digital services, much of food and metal manufacturing. Averaged within each Summary industry, the Detail δ's match the Summary δ's.
4. **Primary industries look local once their buyers are separate.** Fishing, crops and animals, and forestry all go to δ ≈ 0. Fishing → seafood processing is right at any δ up to about 0.09.
5. **The same three error sources remain:**
   - CILQ's division by the buyer's SLQ: governments, defence, shipbuilding, rubber.
   - The LQ floor: repair construction, electric power, government-to-government purchases.
   - Diagonals of specialized industries stuck at the national coefficient: seafood → seafood.
6. **Per-industry δ pushes totals down.** NS local purchases go from −14.7% to −22.5% short. CILQ (δ = 0 everywhere) gets NS's Detail totals nearly right, though its cells are worse.

## Caveats

- **In-sample with 222 parameters.** Ten provinces is little data for this many δ's, more so than at Summary. Twenty δ's rest on rows that carry almost no error.
- **The δ's are fitted on Detail error.** A fit aimed directly at the Summary score could do better there, but that would be a different experiment.
- **One year (2021, a pandemic year).** The grid limits δ to [0, 1] in steps of 0.01.
- **The NS close-up isn't reproducible from the repo.** It came from a scratch script that isn't saved here. Province tables, the Summary scoring and fitted δ's are reproducible.

## Open

- Should the Detail δ's be fitted on the Summary-scored error, since that's the fair comparison?
- Do the δ's hold up on another year or held-out provinces? With 222 parameters this matters more than at Summary.
- The buyer-SLQ division is the biggest fixable error in NS at both levels.

## Code

- `src/small_io/io_table.py`: `summary_code` maps a Detail industry to its Summary industry, and `to_summary` adds Detail flows or outputs up to Summary.
- `tests/test_data.py`: checks that national and NS Detail tables add up to their Summary tables.
- `scripts/fit_industry_deltas.py --level D`: fits the Detail δ's and also scores every estimate at Summary. It writes:
  - `results/industry_deltas_D_2021.csv`;
  - `results/fit_industry_deltas_D_2021.csv`, where the `scored_at` column is `D` or `S`.

```
uv run python scripts/fit_industry_deltas.py --level D
uv run pytest
```
