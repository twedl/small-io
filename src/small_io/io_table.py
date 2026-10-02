"""Parse StatCan symmetric IO workbooks into industry-by-industry blocks.

Every sheet we read has the same layout: a header row whose third cell is
"Code" lists the column codes, and each data row carries its row code in the
second column. The square intermediate block is the set of industry codes
(BS*, NP*, GS*) that appear as both rows and columns; the TOTAL row holds
each industry's gross output at basic prices.
"""

from pathlib import Path

import pandas as pd

DATA_DIR = Path(__file__).resolve().parents[2] / "data"

PROVINCES = ["NL", "PE", "NS", "NB", "QC", "ON", "MB", "SK", "AB", "BC"]

# business sector, non-profits serving households, government
INDUSTRY_PREFIXES = ("BS", "NP", "GS")

LEVEL_DIRS = {"S": "Summary level", "D": "Detail level", "L61": "Link-1961 level", "L97": "Link-1997 level"}


def national_domestic_path(year: int, level: str = "S") -> Path:
    prefix = "IOT national" if year >= 2022 else "IOTs national symmetric"
    return DATA_DIR / "National" / str(year) / f"{prefix} domestic and imports {level} {year}.xlsx"


def provincial_path(prov: str, year: int, level: str = "S") -> Path:
    prefix = "IOT provincial" if year >= 2022 else "IOTs provincial symmetric"
    return DATA_DIR / "iot" / str(year) / LEVEL_DIRS[level] / f"{prefix} {prov} {level} {year}.xlsx"


def read_sheet(path: Path, sheet: str) -> pd.DataFrame:
    """Whole sheet as a DataFrame indexed by row code, columns by column code."""
    raw = pd.read_excel(path, sheet_name=sheet, header=None)
    header = raw.index[raw[2] == "Code"][0]
    cols = raw.iloc[header, 3:].tolist()
    body = raw.iloc[header + 2 :]
    body = body[body[1].notna()]
    out = body.iloc[:, 3:].set_axis(cols, axis=1).set_axis(body[1].tolist(), axis=0)
    # provincial sheets repeat region codes (exports and imports by partner);
    # we only ever need the industry columns, which are unique
    out = out.loc[:, ~out.columns.duplicated()]
    return out.apply(pd.to_numeric, errors="coerce").fillna(0.0)


def industry_block(sheet: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    """Square industry x industry block and the TOTAL row (gross output)."""
    industries = [c for c in sheet.columns if c in sheet.index and str(c)[:2] in INDUSTRY_PREFIXES]
    return sheet.loc[industries, industries], sheet.loc["TOTAL", industries]


def load_national_domestic(year: int, level: str = "S") -> tuple[pd.DataFrame, pd.Series]:
    """National flows of Canadian-made inputs (Z) and gross output (X)."""
    return industry_block(read_sheet(national_domestic_path(year, level), "Domestic"))


def load_provincial_domestic(prov: str, year: int, level: str = "S") -> tuple[pd.DataFrame, pd.Series]:
    """Provincial flows of inputs made in the province itself (Z) and gross output (X).

    DomesticUse, not BasicPrice: BasicPrice also includes interprovincial and
    international imports, which FLQ's regional coefficient excludes.
    """
    return industry_block(read_sheet(provincial_path(prov, year, level), "DomesticUse"))


def coefficients(Z: pd.DataFrame, X: pd.Series) -> pd.DataFrame:
    """Input coefficients a_ij = Z_ij / X_j (zero where an industry has no output)."""
    return Z.div(X.where(X != 0), axis=1).fillna(0.0)
