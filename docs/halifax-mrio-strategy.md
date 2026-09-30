# Halifax Multiregional IO Model: Strategy Summary

Sep 30, 2026 · @jesse

A potential strategy for impact analysis below the province level, with Halifax as the first case.

## Goal

Estimate the impact of final demand shocks on Halifax, and spillovers to the rest of NS and the rest of Canada, using a multiregional input-output model built from Statistics Canada's Nova Scotia supply-use tables (SUT).

## Notation and basics

- x̂ = diag(x); 1 = vector of ones; ' = transpose
- Z = intermediate flows (z\_ij = sales from i to j)
- f = final demand; v = value added; x = gross output
- A = Z·x̂⁻¹; L = (I − A)⁻¹; x = L·f
- Price dual: p' = v\_c'·L, where v\_c' = v'·x̂⁻¹
- Multipliers: output = 1'L; employment/income = e'L, where e\_j = E\_j / x\_j

## Regions

- H = Halifax CMA
- S = rest of Nova Scotia
- C = rest of Canada (excluding NS)
- W = rest of world, exogenous: imports are a leakage row (m\_W'), exports are in f
- Report S + C together as "rest of Canada" after solving. Summing results after solving has no aggregation bias; merging regions before solving does.

Block system (each block n×n), where A\_rs = inputs from region r per unit of output in region s:

```latex
A = \begin{bmatrix} A_{HH} & A_{HS} & A_{HC} \\ A_{SH} & A_{SS} & A_{SC} \\ A_{CH} & A_{CS} & A_{CC} \end{bmatrix}
```

Consistency constraint (in flows, not coefficients):

```latex
Z_{HH} + Z_{HS} + Z_{SH} + Z_{SS} = Z_{NS,\text{intra}}
```

## Solving and decomposition

Partition H against R = \[S, C\]:

```latex
\begin{aligned}
L^0_H &= (I - A_{HH})^{-1} \\
L^0_R &= (I - A_{RR})^{-1} \\
L_{HH} &= (I - A_{HH} - A_{HR} L^0_R A_{RH})^{-1} \\
L_{RH} &= L^0_R A_{RH} L_{HH}
\end{aligned}
```

For a shock Δf\_H (demand for Halifax output):

```latex
\begin{aligned}
\text{Intraregional effect:} &\quad L^0_H \, \Delta f_H \\
\text{Interregional feedback:} &\quad (L_{HH} - L^0_H) \, \Delta f_H \\
\text{Spillover to } R\text{:} &\quad L^0_R A_{RH} L_{HH} \, \Delta f_H
\end{aligned}
```

For spending by Halifax residents, split Δf by region of origin. With trade-share matrix C (Chenery–Moses):

```latex
x = (I - CA)^{-1} C f
```

## Building Halifax coefficients (non-survey regionalization)

### 1. Halifax output x\_H

- StatCan table 36-10-0468-01: GDP at basic prices by CMA (latest year 2022)
- Convert value added to gross output using NS output/VA ratios by industry
- For finer detail: Census place-of-work employment × NS output per worker

### 2. Technology

- A\_tot,H = A\_tot,NS (NS total input coefficients, all origins)
- Use NS value-added coefficients

### 3. Origin split

Using the NS SUT by product i:

- t\_NS,i = share of NS use of product i made in NS
- t\_C,i = interprovincial import share
- t\_W,i = international import share

```latex
\begin{aligned}
a_{HH,ij} &= \min(1, FLQ_{ij}) \, t_{NS,i} \, a_{tot,ij} && \text{(bought in Halifax)} \\
a_{SH,ij} &= t_{NS,i} \, a_{tot,ij} - a_{HH,ij} && \text{(bought in rest of NS)} \\
a_{CH,ij} &= t_{C,i} \, a_{tot,ij} && \text{(bought in RoC)} \\
m_{W,ij} &= t_{W,i} \, a_{tot,ij} && \text{(RoW leakage)}
\end{aligned}
```

Flegg location quotient (FLQ), NS as reference:

```latex
\begin{aligned}
SLQ_i &= \frac{x_{H,i} / x_H}{x_{NS,i} / x_{NS}} \\
CILQ_{ij} &= SLQ_i / SLQ_j \quad (SLQ_i \text{ on the diagonal}) \\
\lambda &= \left[\log_2(1 + x_H / x_{NS})\right]^{\delta}, \quad \delta \approx 0.2 \text{ to } 0.3 \\
FLQ_{ij} &= \lambda \, CILQ_{ij}
\end{aligned}
```

- Halifax is about 60% of NS GDP, so λ ≈ 0.9
- Alternative: CHARM (commodity balance allowing cross-hauling)

### 4. Sales side

- Halifax output not used in Halifax is exported. Split it among S, C, and W using NS's export pattern.
- Derive S blocks by subtraction, e.g. Z\_SS = Z\_NS,intra − Z\_HH − Z\_HS − Z\_SH

### 5. Calibration

- Use GRAS to remove negative entries and match known totals.
- Replace sectors where NS-average technology fits poorly with survey or administrative data: port, defence, universities, hospitals, provincial government.

## Why NS rather than national coefficients

**For NS:**

- Within-industry product mix is closer to Halifax's (e.g., NS food manufacturing is mostly seafood)
- Regional prices (wages, rents, margins, taxes) are closer to Halifax's
- Halifax is about 60% of NS GDP, so NS coefficients are largely Halifax's
- H + S = NS consistency holds by construction, and trade shares come from the same table

**For national:**

- NS cells may be thin or suppressed for small industries
- Urban-type firms (finance, head offices) may resemble other CMAs
- Finer industry and product detail is available

**In practice:**

- Use NS as the default
- Substitute national coefficients industry by industry where NS cells are weak
- Run both versions and compare Halifax multipliers
- Where the two differ materially, collect local data

## Caveats

- Aggregation bias: don't merge regions or sectors with different purchase patterns before solving.
- Type II (induced) effects: many Halifax jobs are held by rest-of-NS residents, so allocate labour income by place of residence.
- The method assumes Halifax's interprovincial and international import shares by product equal NS's.

## Open questions

An earlier feasibility check in this project tested the same NS → {Halifax, rest of NS} split. It used Summary-level symmetric tables, δ = 0, and LFS employment for the Halifax economic region.

- [ ] **Does `min(1, FLQ)` understate Halifax?** The cap stops any Halifax coefficient from exceeding NS's. But Halifax should be more self-sufficient than the NS average, which blends it with rural NS. In the check, 87% of Halifax's diagonal (self-supply) value was pinned at the NS coefficient.
- [ ] **Is the implied Halifax ↔ rest-of-NS trade credible?** In the check, the two synthetic regions summed to $15,490M of NS's real $17,575M domestic intermediate flows (88%). That leaves only $2,084M (12%) for trade between them. Test it against commuting, trucking or port data.
- [ ] **Get the inputs.** This plan needs the NS supply-use tables, table 36-10-0468-01 (GDP by CMA) and Census place-of-work employment. So far `data/` holds only symmetric IO tables.

## References

- Miller & Blair (2009), *Input-Output Analysis: Foundations and Extensions*, 2nd ed. (ch. 2, 3, 5, 7–8)
- Flegg, Webber & Elliott (1995), *Regional Studies* (FLQ)
- Kronenberg (2009), *International Regional Science Review* (CHARM)
