"""Invariants of the raw StatCan files. Skipped when data/ isn't on disk."""

import numpy as np
import pytest

from small_io.employment import SUMMARY_NAICS, detail_naics, load_jobs
from small_io.io_table import (
    DATA_DIR,
    load_national_domestic,
    load_provincial_domestic,
    provincial_path,
    read_sheet,
)

pytestmark = pytest.mark.skipif(not DATA_DIR.exists(), reason="data/ not present")
YEAR = 2021


@pytest.mark.parametrize("level", ["S", "D"])
def test_domestic_use_plus_imports_equals_basic_price(level):
    path = provincial_path("NS", YEAR, level)
    dom, _ = load_provincial_domestic("NS", YEAR, level)
    inter = read_sheet(path, "InterprovImportUse").loc[dom.index, dom.columns]
    intl = read_sheet(path, "InternatImportUse").loc[dom.index, dom.columns]
    basic = read_sheet(path, "BasicPrice").loc[dom.index, dom.columns]
    # Detail is in $K, rounded to the dollar
    np.testing.assert_allclose((dom + inter + intl).to_numpy(), basic.to_numpy(), atol=1e-3 if level == "S" else 2)


def test_provincial_output_matches_basic_price_total():
    _, X = load_provincial_domestic("NS", YEAR)
    basic = read_sheet(provincial_path("NS", YEAR), "BasicPrice")
    np.testing.assert_allclose(X.to_numpy(), basic.loc["TOTAL", X.index].to_numpy(), atol=1e-3)


@pytest.mark.parametrize("level", ["S", "D"])
def test_national_output_is_sum_of_regions(level):
    _, X = load_national_domestic(YEAR, level)
    regions = ["NL", "PE", "NS", "NB", "QC", "ON", "MB", "SK", "AB", "BC", "YT", "NT", "NU", "CE"]
    total = sum(load_provincial_domestic(r, YEAR, level)[1] for r in regions)
    np.testing.assert_allclose(total.to_numpy(), X.to_numpy(), rtol=1e-3)


def test_national_block_is_32_summary_industries():
    Z, X = load_national_domestic(YEAR)
    assert Z.shape == (32, 32)
    assert list(Z.columns) == list(X.index)
    assert set(SUMMARY_NAICS) == set(Z.columns) - {"BS53C"}


def test_every_mapped_naics_code_has_jobs_data():
    jobs = load_jobs(YEAR)
    codes = {c for naics in SUMMARY_NAICS.values() for c in naics}
    assert codes <= set(jobs.index)
    assert jobs.notna().all().all()


def test_detail_industries_map_to_their_own_naics_code_or_a_parent():
    Z, _ = load_national_domestic(YEAR, "D")
    assert Z.shape == (234, 234)
    mapping = detail_naics(list(Z.columns), load_jobs(YEAR).index)
    assert mapping["BS311700"] == ["3117"]  # seafood: exact
    assert mapping["BS23C100"] == ["23C1"]  # letters inside the code
    assert mapping["BS610000"] == ["61"]  # trailing zeros stripped
    assert mapping["BS111CL0"] == ["111"]  # cannabis -> crop production
    assert mapping["BS211140"] == ["211114"]  # oil sands override
    assert mapping["BS5311A0"] == []  # owner-occupied dwellings: no jobs
    unmapped = [io for io, naics in mapping.items() if not naics]
    assert unmapped == ["BS5311A0", "NP999999"]
