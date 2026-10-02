# EK home shares vs SLQ/FLQ for regionalizing IO tables

Notes from 2026-10-02. The EK mapping is our own derivation, not from Flegg & Tohmo.

## LQ setup (for reference)

```
r_ij = min(LQ, 1) * a_ij                    # a_ij: national technology, assumed same in region
                                            # r_ij: locally supplied part; (1 - LQ) * a_ij imported
SLQ_i  = (RE_i / TRE) / (NE_i / TNE)        # industry i's share of regional vs national employment
CILQ_ij = SLQ_i / SLQ_j
FLQ_ij  = CILQ_ij * lambda
lambda  = [log2(1 + TRE/TNE)]^delta         # TRE/TNE = region's share of national employment, in (0, 1]
                                            # 0 <= delta < 1; delta ~ 0.3 common default
```

- Technology is unchanged; the LQ only estimates the local sourcing share.
- Standard LQs understate interregional imports, so multipliers are overstated. The FLQ's λ makes small regions import more.
- Use a national table that excludes foreign imports.

## Core mapping: LQ local share = EK sectoral home share

```
r_ij^n = pi_nn^i * a_ij       # EK with IO links (Caliendo-Parro style)
```

The LQ is a reduced-form guess at π_nn^i.

## EK model (one industry i)

```
pi_nk  = S_k * phi_nk / Phi_n           # share of n's absorption of i bought from k
S_k    = T_k * c_k^(-theta)             # unobserved supplier capability
phi_nk = d_nk^(-theta)                  # trade freeness in (0, 1]; diagonal = internal freeness
Phi_n  = sum_k S_k * phi_nk
```

Market clearing eliminates S (T and c drop out):

```
Y_k = S_k * sum_n phi_nk * X_n / Phi_n  # Y_k: output of i in k; X_n: absorption of i in n
pi_nn = S_n / Phi_n                     # solve S by fixed point (multilateral resistance), up to scale
```

**Result:** home share depends only on observed output Y, absorption X, and industry-specific freeness φ.

## Two-region closed form (region vs rest of nation)

```
y = SLQ_i * s                 # region share of national output of i; s = TRE/TNE
x                             # region share of national absorption of i (x = s under LQ assumption)
B = x + (1 - x) * phi_i^2 + (1 - phi_i^2) * y
h_i = 2y / (B + sqrt(B^2 - 4 * (1 - phi_i^2) * x * y))
```

Limits:

```
phi_i = 1 (frictionless):     h_i = SLQ_i * s
phi_i -> 0 (prohibitive):     h_i = min(SLQ_i, 1)     # exactly the SLQ rule
```

- The SLQ is the infinite-trade-cost case of EK. This is why it understates imports.
- The frictionless case shows SLQ overstates the home share by a factor of 1/s for small regions.
- The FLQ interpolates between the limits with one size factor and a common δ. Effectively δ is a reduced-form stand-in for trade costs. Higher δ is closer to frictionless; δ → 0 means no size adjustment.
- EK interpolates industry by industry through φ_i. Home shares are not proportional to SLQ.

Example values (s = 1%, x = s, θ = 4, φ = d⁻⁴):

| d_i | SLQ = 0.5 | SLQ = 1 | SLQ = 2 |
|---|---|---|---|
| 1 | 0.005 | 0.010 | 0.020 |
| 1.25 | 0.028 | 0.054 | 0.104 |
| 1.5 | 0.095 | 0.177 | 0.308 |
| 2 | 0.319 | 0.543 | 0.764 |
| 3 | 0.486 | 0.885 | 0.985 |
| ∞ | 0.500 | 1.000 | 1.000 |
| FLQ, δ = 0.3 | 0.14 | 0.28 | 0.56 |

## Estimating industry-specific φ

Only φ = d^(−θ) is needed; θ does not need to be identified separately.

1. **Gravity on observed flows** (coarser geography, e.g. states/provinces or a commodity flow survey), PPML by industry:
   ```
   Z_nk^i = exp(alpha_n^i + gamma_k^i - eps_i * ln(dist_nk) + beta_i * border_nk)
   phi_nk^i = dist_nk^(-eps_i) * exp(beta_i * border_nk)
   ```
   Fixed effects absorb S and Φ, consistent with the model. Apply ε_i to finer regions' distances, with internal distance ≈ (2/3)·sqrt(area/π).
2. **Head–Ries freeness** where internal flows are observed:
   ```
   phi_nk = sqrt(pi_nk * pi_kn / (pi_nn * pi_kk))
   ```
3. **No flow data:** use published industry distance elasticities, then calibrate a scale factor to a survey-based regional table (as Flegg & Tohmo do with δ).

## Absorption

Compute directly instead of assuming it is proportional to size (no circularity):

```
X_n^i = sum_j a_ij * Y_n^j + f_i * FD_n     # national technology + regional final demand
```

This captures the buyer composition the CILQ tries to proxy.

## Differences from LQ methods

- **Cross-hauling:** EK gives π_nn < 1 for finite trade costs, so regions both import and export every good. LQs set imports to zero when LQ ≥ 1 (motivation for Kronenberg's CHARM).
- **Buyer independence:** EK sourcing share depends on supplier sector i and destination only, not buyer j. SLQ shares this structure; CILQ/FLQ vary with j.
- **Foundations:** EK home shares are equilibrium outcomes of T, wages, trade costs, θ. FLQ is a calibrated rule; δ fit to survey tables.

## Caveats

- Closed nation for good i. To relax, add rest of world as an extra region with its own φ.
- Using employment for Y assumes equal labour productivity across regions.

## Code

An earlier `ek_home_share.py` was deleted; we'll remake it later if we need it. It had:
- `home_share_two_region(slq, s, phi, x=None)`: closed form above
- `home_shares(Y, X, phi)`: N-region fixed-point solver, returns π_nn and full π matrix
- `freeness_from_distance(dist, eps, internal_dist)`: φ = dist^(−ε)
- `absorption(A, Yall, fd_share, FD)`: X from national technology + final demand
- Checks the solver against the closed form.

## Key references

- Flegg, Webber & Elliott (1995), *Regional Studies* 29(6): 547–561. Original FLQ.
- Flegg & Webber (1997), *Regional Studies* 31(8): 795–805. Refined FLQ with δ.
- Flegg & Tohmo (2013), *Regional Studies* 47(5): 703–721. Finland; choosing δ. Free: https://uwe-repository.worktribe.com/output/937988
- Kowalewski (2015), *Regional Studies* 49(2): 240–250. SFLQ (industry-specific δ). Free WP: https://www.econstor.eu/bitstream/10419/59515/1/71786202X.pdf
- Caliendo & Parro (2015), multi-sector EK with IO linkages.
