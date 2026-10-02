"""Jobs by IO industry and region, from StatCan table 36-10-0676-01.

The employment table is NAICS-based and does not split business, non-profit
and government producers the way the IO table does, so several IO industries
share one NAICS group (BS610 and GS610 are both NAICS 61). That's fine for
location quotients: an LQ only needs each industry's regional share relative
to its national share, and the shared group's share applies to both.
"""

import pandas as pd

from small_io.io_table import DATA_DIR

JOBS_CSV = DATA_DIR / "employment" / "36100676_filtered.csv"

GEO_CODES = {
    "Canada": "CA",
    "Newfoundland and Labrador": "NL",
    "Prince Edward Island": "PE",
    "Nova Scotia": "NS",
    "New Brunswick": "NB",
    "Quebec": "QC",
    "Ontario": "ON",
    "Manitoba": "MB",
    "Saskatchewan": "SK",
    "Alberta": "AB",
    "British Columbia": "BC",
    "Yukon": "YT",
    "Northwest Territories": "NT",
    "Nunavut": "NU",
}

# IO Summary industry -> NAICS codes in the jobs table. BS53C (owner-occupied
# dwellings) has no jobs at all; it gets no entry here and an SLQ of 1.
SUMMARY_NAICS = {
    "BS11A": ["11A"],
    "BS113": ["113"],
    "BS114": ["114"],
    "BS115": ["115"],
    "BS210": ["21"],
    "BS220": ["22"],
    "BS23A": ["23A"],
    "BS23B": ["23B"],
    "BS23C": ["23C"],
    "BS23D": ["23D"],
    "BS23E": ["23E"],
    "BS3A0": ["31-33"],
    "BS410": ["41"],
    "BS4A0": ["44-45"],
    "BS4B0": ["48-49"],
    "BS510": ["51"],
    "BS5B0": ["52", "53", "551113"],
    "BS540": ["54"],
    "BS560": ["56"],
    "BS610": ["61"],
    "BS620": ["62"],
    "BS710": ["71"],
    "BS720": ["72"],
    "BS810": ["811", "812", "814"],
    "NP000": ["813"],
    "GS610": ["61"],
    "GS620": ["62"],
    "GS911": ["911"],
    "GS912": ["912"],
    "GS913": ["913"],
    "GS914": ["914"],
}


# IO Detail codes are NAICS codes behind a sector prefix, zero-padded to six
# characters (BS311700 is NAICS 3117), and the jobs table mostly breaks out the
# same codes. These are the exceptions the prefix rule in `detail_naics` gets
# wrong; an empty list means no jobs (SLQ of 1).
DETAIL_OVERRIDES = {
    "BS211110": ["211113"],  # oil and gas extraction (except oil sands) = conventional
    "BS211140": ["211114"],  # oil sands extraction = non-conventional oil
    "BS5311A0": [],  # owner-occupied dwellings
}


def detail_naics(industries: list[str], naics_codes) -> dict[str, list[str]]:
    """IO Detail industry -> its NAICS code, or the nearest parent the jobs table has.

    Cannabis (BS111CL0, BS453BL0) falls back to its parent, crop production or
    miscellaneous store retailers; NP999999 (other non-profits) has no parent.
    """
    codes = set(naics_codes)
    mapping = {}
    for io in industries:
        if io in DETAIL_OVERRIDES:
            mapping[io] = DETAIL_OVERRIDES[io]
            continue
        code = io[2:].rstrip("0")
        while code and code not in codes:
            code = code[:-1]
        mapping[io] = [code] if code else []
    return mapping


def naics_mapping(level: str, industries: list[str], jobs: pd.DataFrame) -> dict[str, list[str]]:
    if level == "S":
        return SUMMARY_NAICS
    if level == "D":
        return detail_naics(industries, jobs.index)
    raise ValueError(f"no NAICS mapping for level {level!r}")


def load_jobs(year: int) -> pd.DataFrame:
    """Total jobs (paid + self-employed), NAICS code x region code."""
    df = pd.read_csv(JOBS_CSV)
    df = df[(df["REF_DATE"] == year) & df["GEO"].isin(GEO_CODES)]
    df = df.assign(
        naics=df.iloc[:, 3].str.extract(r"\[([^\]]+)\]$", expand=False),
        region=df["GEO"].map(GEO_CODES),
    )
    return df.pivot_table(index="naics", columns="region", values="VALUE", aggfunc="sum")


def io_industry_jobs(jobs: pd.DataFrame, mapping: dict[str, list[str]]) -> pd.DataFrame:
    """Jobs by IO industry x region. Industries sharing a NAICS group get the same row."""
    return pd.DataFrame({io: jobs.loc[naics].sum() for io, naics in mapping.items() if naics}).T


def slq(
    jobs: pd.DataFrame, region: str, industries: list[str], mapping: dict[str, list[str]] = SUMMARY_NAICS
) -> tuple[pd.Series, float]:
    """Simple location quotients for `region`, plus its share of national jobs.

    SLQ_i = (RE_i / TRE) / (NE_i / TNE). Industries with no jobs mapping get 1.
    """
    by_io = io_industry_jobs(jobs, mapping)
    tre, tne = jobs.loc["T001", region], jobs.loc["T001", "CA"]
    lq = (by_io[region] / tre) / (by_io["CA"] / tne)
    return lq.reindex(industries).fillna(1.0), tre / tne
