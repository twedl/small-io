"""Location-quotient regionalization (Flegg & Webber 1997; Flegg & Tohmo 2013).

All three methods scale national coefficients by a capped quotient,
r_ij = min(LQ_ij, 1) * a_ij: the region keeps the nation's technology and the
quotient estimates how much of each input it can supply itself.
"""

import numpy as np
import pandas as pd

# Flegg & Tohmo (2013), 20 Finnish regions: "we would recommend using
# delta = 0.25 as the best single value" (working paper version, UWE DP 1005)
FLEGG_TOHMO_DELTA = 0.25


def slq_matrix(slq: pd.Series) -> pd.DataFrame:
    """SLQ_i applied across every buying column j."""
    return pd.DataFrame(np.repeat(slq.to_numpy()[:, None], len(slq), axis=1), index=slq.index, columns=slq.index)


def cilq_matrix(slq: pd.Series) -> pd.DataFrame:
    """CILQ_ij = SLQ_i / SLQ_j off the diagonal, SLQ_i on it (Smith & Morrison 1974)."""
    s = slq.to_numpy()
    with np.errstate(divide="ignore", invalid="ignore"):
        m = s[:, None] / s[None, :]
    np.fill_diagonal(m, s)
    # 0/0 means the region has neither the seller nor the buyer: supply nothing locally
    return pd.DataFrame(np.nan_to_num(m, nan=0.0, posinf=np.inf), index=slq.index, columns=slq.index)


def flq_lambda(region_share: float, delta: float) -> float:
    """lambda* = [log2(1 + TRE/TNE)]^delta; shrinks quotients more for small regions."""
    return float(np.log2(1 + region_share) ** delta)


def flq_matrix(slq: pd.Series, region_share: float, delta: float) -> pd.DataFrame:
    """FLQ_ij = CILQ_ij * lambda* (diagonal SLQ_i * lambda*)."""
    return cilq_matrix(slq) * flq_lambda(region_share, delta)


def regionalize(A: pd.DataFrame, lq: pd.DataFrame) -> pd.DataFrame:
    """Regional coefficients r_ij = min(LQ_ij, 1) * a_ij."""
    return A * lq.clip(upper=1.0).loc[A.index, A.columns]
