"""Fit one FLQ delta per selling industry, pooled over the 10 provinces, and
compare it with a single delta.

    uv run python scripts/fit_industry_deltas.py [--year 2021] [--level S]

Row i of the regional matrix depends only on delta_i, so with cell WAPE as
the loss each industry's delta is a 1-D grid search over its own row. The
loss is the mean of the provincial WAPEs (each province's absolute errors
divided by its own total flows), so the big provinces don't set every delta.

Deltas are fitted and scored on the same provinces: the gain over the best
single delta is an in-sample upper bound, not what a new region would get.
Summary level only so far; at Detail, rows with tiny flows get noisy deltas.
"""

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

from small_io.compare import compare, lq_floor
from small_io.employment import load_jobs, naics_mapping, slq
from small_io.flq import FLEGG_TOHMO_DELTA, cilq_matrix, flq_matrix, regionalize
from small_io.io_table import (
    PROVINCES,
    coefficients,
    industry_names,
    load_national_domestic,
    load_provincial_domestic,
)

RESULTS = Path(__file__).resolve().parents[1] / "results"
GRID = np.round(np.linspace(0, 1, 101), 2)


def row_losses(A_nat: pd.DataFrame, A_true: pd.DataFrame, X: pd.Series, lq: pd.Series, share: float) -> pd.DataFrame:
    """Each selling industry's share of the province's cell WAPE (%), delta grid x industry.

    Summed over industries this is exactly compare()'s wape at that delta.
    """
    present = X[X > 0].index
    c = cilq_matrix(lq).loc[present, present].to_numpy()
    flows = (A_nat.loc[present, present] * X[present]).to_numpy()
    z = (A_true.loc[present, present] * X[present]).to_numpy()
    base = np.log2(1 + share)
    loss = [np.abs(np.minimum(c * base**d, 1.0) * flows - z).sum(axis=1) for d in GRID]
    return pd.DataFrame(np.array(loss) / z.sum() * 100, index=GRID, columns=present)


def pick_delta(loss: pd.Series) -> float:
    """Grid delta with the lowest loss; ties (flat rows) go to the one nearest 0.25."""
    best = loss.index[loss <= loss.min() + 1e-9]
    return float(best[np.argmin(np.abs(best - FLEGG_TOHMO_DELTA))])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--year", type=int, default=2021)
    parser.add_argument("--level", choices=["S", "D"], default="S")
    args = parser.parse_args()

    Z_nat, X_nat = load_national_domestic(args.year, args.level)
    A_nat = coefficients(Z_nat, X_nat)
    industries = list(A_nat.columns)
    jobs = load_jobs(args.year)
    mapping = naics_mapping(args.level, industries, jobs)

    provinces = {}
    loss = pd.DataFrame(0.0, index=GRID, columns=industries)
    for prov in PROVINCES:
        Z, X = load_provincial_domestic(prov, args.year, args.level)
        A_true = coefficients(Z, X)
        lq, share = slq(jobs, prov, industries, mapping)
        provinces[prov] = (Z, X, A_true, lq, share)
        loss = loss.add(row_losses(A_nat, A_true, X, lq, share), fill_value=0.0)
    loss /= len(PROVINCES)

    single = pick_delta(loss.sum(axis=1))
    deltas = loss.apply(pick_delta)
    by_industry = pd.DataFrame(
        {
            "name": industry_names(args.year, args.level).reindex(industries),
            "delta": deltas,
            "flat": loss.max() - loss.min() < 1e-9,
            # each row's contribution to the mean provincial WAPE, percentage points
            f"err_{FLEGG_TOHMO_DELTA:g}": loss.loc[FLEGG_TOHMO_DELTA],
            f"err_{single:g}": loss.loc[single],
            "err_own": loss.min(),
            "local_sales": sum(Z.sum(axis=1) for Z, *_ in provinces.values()).reindex(industries),
        }
    ).rename_axis("industry")

    best_single = f"FLQ({single:g}) best"
    rows = []
    for prov, (_, X, A_true, lq, share) in provinces.items():
        estimates = {
            "national": A_nat,
            f"FLQ({FLEGG_TOHMO_DELTA:g})": regionalize(A_nat, flq_matrix(lq, share, FLEGG_TOHMO_DELTA)),
            best_single: regionalize(A_nat, flq_matrix(lq, share, single)),
            "FLQ by industry": regionalize(A_nat, flq_matrix(lq, share, deltas)),
        }
        for method, A_hat in estimates.items():
            rows.append({"prov": prov, "share": share, "method": method, **compare(A_hat, A_true, X)})
        rows.append({"prov": prov, "share": share, "method": "LQ floor", "wape": lq_floor(A_nat, A_true, X)})
    results = pd.DataFrame(rows)

    RESULTS.mkdir(exist_ok=True)
    by_industry.to_csv(RESULTS / f"industry_deltas_{args.level}_{args.year}.csv")
    results.to_csv(RESULTS / f"fit_industry_deltas_{args.level}_{args.year}.csv", index=False)

    pd.set_option("display.width", 160, "display.precision", 2, "display.max_rows", 300)
    fitted = by_industry[~by_industry["flat"]]
    print(
        f"Best single delta {single:g}. By industry: {(fitted['delta'] == 0).sum()} at 0, "
        f"{(fitted['delta'] == 1).sum()} at 1, {by_industry['flat'].sum()} flat (kept {FLEGG_TOHMO_DELTA:g})"
    )
    print("\nDelta by selling industry; err = row's share of mean provincial WAPE, pp\n")
    print(by_industry.assign(name=by_industry["name"].str[:45]).sort_values("delta").to_string())

    pd.set_option("display.float_format", "{:.1f}".format)
    order = list(dict.fromkeys(results["method"]))
    for stat, label in [
        ("wape", "Cell WAPE on flows, %"),
        ("mult_mpe", "Output multiplier mean % error (bias)"),
        ("local_share_err", "Mean error in local-input share of output (x100)"),
    ]:
        scale = 100 if stat == "local_share_err" else 1
        table = results.pivot(index="prov", columns="method", values=stat).loc[PROVINCES, order] * scale
        table = table.dropna(axis=1, how="all")  # the LQ floor is only a cell WAPE
        table.loc["mean"] = table.mean()
        print(f"\n{label}, {args.level} {args.year}, in-sample\n{table}")


if __name__ == "__main__":
    main()
