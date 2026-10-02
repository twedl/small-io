"""Regionalize the national IO table to each province with FLQ and compare to
StatCan's real provincial tables.

    uv run python scripts/run_flq_provinces.py [--year 2021] [--level S|D] [--delta 0.25]

Prints per-province error statistics for four estimates of the regional
coefficient matrix (unadjusted national, SLQ, CILQ, FLQ), and the "LQ floor":
the error left even with a perfect quotient for every cell. Writes the table
to results/.
"""

import argparse
from pathlib import Path

import pandas as pd

from small_io.compare import compare, lq_floor
from small_io.employment import load_jobs, naics_mapping, slq
from small_io.flq import FLEGG_TOHMO_DELTA, cilq_matrix, flq_matrix, regionalize, slq_matrix
from small_io.io_table import PROVINCES, coefficients, load_national_domestic, load_provincial_domestic

RESULTS = Path(__file__).resolve().parents[1] / "results"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--year", type=int, default=2021)
    parser.add_argument("--level", choices=["S", "D"], default="S")
    parser.add_argument("--delta", type=float, default=FLEGG_TOHMO_DELTA)
    args = parser.parse_args()

    Z_nat, X_nat = load_national_domestic(args.year, args.level)
    A_nat = coefficients(Z_nat, X_nat)
    industries = list(A_nat.columns)
    jobs = load_jobs(args.year)
    mapping = naics_mapping(args.level, industries, jobs)

    rows = []
    for prov in PROVINCES:
        Z, X = load_provincial_domestic(prov, args.year, args.level)
        A_true = coefficients(Z, X)
        lq, share = slq(jobs, prov, industries, mapping)
        estimates = {
            "national": A_nat,
            "SLQ": regionalize(A_nat, slq_matrix(lq)),
            "CILQ": regionalize(A_nat, cilq_matrix(lq)),
            f"FLQ({args.delta})": regionalize(A_nat, flq_matrix(lq, share, args.delta)),
        }
        for method, A_hat in estimates.items():
            rows.append({"prov": prov, "share": share, "method": method, **compare(A_hat, A_true, X)})
        rows.append({"prov": prov, "share": share, "method": "LQ floor", "wape": lq_floor(A_nat, A_true, X)})

    results = pd.DataFrame(rows)
    RESULTS.mkdir(exist_ok=True)
    results.to_csv(RESULTS / f"flq_provinces_{args.level}_{args.year}.csv", index=False)

    pd.set_option("display.width", 140, "display.precision", 1)
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
        print(f"\n{label}, {args.level} {args.year}\n{table}")


if __name__ == "__main__":
    main()
