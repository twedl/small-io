"""Compare an estimated regional coefficient matrix against the real one."""

import numpy as np
import pandas as pd


def output_multipliers(A: pd.DataFrame) -> pd.Series:
    """Type I output multipliers: column sums of the Leontief inverse (I - A)^-1."""
    L = np.linalg.inv(np.eye(len(A)) - A.to_numpy())
    return pd.Series(L.sum(axis=0), index=A.columns)


def compare(A_hat: pd.DataFrame, A_true: pd.DataFrame, X: pd.Series) -> dict[str, float]:
    """Summary error statistics, over industries the region actually has (X_j > 0).

    - wape: cell-level error in flows, sum|Z_hat - Z| / sum Z, with Z = A * X
      using the region's real output (so big buyers count for more)
    - mad: mean absolute difference of coefficients, x100 (Flegg & Tohmo's unit)
    - local_share_err: mean of sum_i(r_hat_ij) - sum_i(r_ij), the error in the
      share of each industry's output spent on locally made inputs
    - mult_mpe / mult_mape: mean (absolute) percentage error in output multipliers
    """
    present = X[X > 0].index
    a_hat, a = A_hat.loc[present, present], A_true.loc[present, present]
    x = X[present]
    z_hat, z = a_hat * x, a * x
    m_hat, m = output_multipliers(a_hat), output_multipliers(a)
    pct = (m_hat - m) / m * 100
    return {
        "wape": float((z_hat - z).abs().to_numpy().sum() / z.to_numpy().sum() * 100),
        "mad": float((a_hat - a).abs().to_numpy().mean() * 100),
        "local_share_err": float((a_hat.sum() - a.sum()).mean()),
        "mult_mpe": float(pct.mean()),
        "mult_mape": float(pct.abs().mean()),
    }


def lq_floor(A_nat: pd.DataFrame, A_true: pd.DataFrame, X: pd.Series) -> float:
    """Lowest cell WAPE any r_ij = c_ij * a_ij with c_ij in [0, 1] could reach.

    LQ methods only ever scale national coefficients down, so wherever the
    region's true coefficient exceeds the national one the shortfall is
    unreachable, however good the quotient.
    """
    present = X[X > 0].index
    gap = (A_true - A_nat).loc[present, present].clip(lower=0) * X[present]
    z = A_true.loc[present, present] * X[present]
    return float(gap.to_numpy().sum() / z.to_numpy().sum() * 100)
