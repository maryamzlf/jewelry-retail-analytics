"""Normalize and clean the jewelry purchase-history source file.

The user's snapshot has no header and contains two physical row widths:
13-field rows and 11-field rows. The shorter rows omit category_code and brand
while retaining an empty category_id field. This script repairs those records
before pandas type conversion so price/user_id do not shift into wrong columns.

The script also supports a source file that *does* contain the standard header.
"""

from __future__ import annotations

from pathlib import Path
import csv
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW_FILE = ROOT / "data" / "raw" / "jewelry.csv"
OUTPUT_FILE = ROOT / "data" / "processed" / "jewelry_clean.csv"
QUALITY_FILE = ROOT / "outputs" / "data_quality_summary.csv"

SOURCE_COLUMNS = [
    "event_time",
    "order_id",
    "product_id",
    "quantity",
    "category_id",
    "category_code",
    "brand_code",
    "price",
    "user_id",
    "gender",
    "color",
    "metal",
    "gem",
]

RAW_HEADER = [
    "event_time",
    "order_id",
    "product_id",
    "quantity",
    "category_id",
    "category_code",
    "brand",
    "price",
    "user_id",
    "gender",
    "color",
    "metal",
    "gem",
]


def read_and_normalize(path: Path) -> tuple[pd.DataFrame, dict[int, int]]:
    """Read raw lines, detect optional header, and normalize short records."""
    rows: list[list[str]] = []
    row_width_counts: dict[int, int] = {}

    with path.open("r", encoding="utf-8", errors="replace", newline="") as handle:
        for line_number, raw_line in enumerate(handle, start=1):
            if not raw_line.strip():
                continue

            row = next(csv.reader([raw_line]))

            if line_number == 1 and [c.strip() for c in row] == RAW_HEADER:
                continue

            row_width_counts[len(row)] = row_width_counts.get(len(row), 0) + 1

            if len(row) == 11 and row[4] == "":
                # 11-field form observed in this snapshot:
                # event_time, order_id, product_id, quantity, category_id(empty),
                # price, user_id, gender, color, metal, gem.
                # category_code and brand are physically absent.
                row = row[:5] + ["", ""] + row[5:]

            if len(row) != 13:
                raise ValueError(
                    f"Unexpected row width {len(row)} at source line {line_number}."
                )

            rows.append(row)

    return pd.DataFrame(rows, columns=SOURCE_COLUMNS), row_width_counts


def clean_types(df: pd.DataFrame) -> pd.DataFrame:
    """Apply types, derived fields, and non-destructive duplicate auditing."""
    result = df.copy()

    result["event_time"] = pd.to_datetime(
        result["event_time"], utc=True, errors="coerce"
    )
    result["quantity"] = pd.to_numeric(
        result["quantity"], errors="coerce"
    ).astype("Int64")
    result["price"] = pd.to_numeric(result["price"], errors="coerce")
    result["brand_code"] = pd.to_numeric(
        result["brand_code"], errors="coerce"
    ).astype("Int64")

    text_columns = [
        "order_id",
        "product_id",
        "category_id",
        "category_code",
        "user_id",
        "gender",
        "color",
        "metal",
        "gem",
    ]
    for column in text_columns:
        result[column] = result[column].replace("", pd.NA)

    required_checks = {
        "event_time": result["event_time"].isna().sum(),
        "order_id": result["order_id"].isna().sum(),
        "product_id": result["product_id"].isna().sum(),
        "quantity": result["quantity"].isna().sum(),
        "price": result["price"].isna().sum(),
        "user_id": result["user_id"].isna().sum(),
    }
    invalid_required = {k: int(v) for k, v in required_checks.items() if v > 0}
    if invalid_required:
        raise ValueError(f"Invalid required values after normalization: {invalid_required}")

    if (result["quantity"] <= 0).any():
        raise ValueError("Quantity must be positive for purchase records.")
    if (result["price"] < 0).any():
        raise ValueError("Negative price values were found.")

    result["line_revenue"] = result["quantity"] * result["price"]
    result["order_date"] = result["event_time"].dt.date
    result["year_month"] = result["event_time"].dt.strftime("%Y-%m")
    result["category_name"] = (
        result["category_code"]
        .str.replace("jewelry.", "", regex=False)
        .fillna("Unknown")
        .str.replace("electronics.clocks", "clocks", regex=False)
        .str.title()
    )
    result["price_band"] = pd.cut(
        result["price"],
        bins=[float("-inf"), 100, 250, 500, 1000, float("inf")],
        labels=["Under $100", "$100-$249", "$250-$499", "$500-$999", "$1,000+"],
        right=False,
    ).astype("string")

    duplicate_basis = SOURCE_COLUMNS
    result["is_exact_duplicate"] = result.duplicated(
        subset=duplicate_basis, keep=False
    )

    return result


def build_quality_summary(
    df: pd.DataFrame, row_width_counts: dict[int, int]
) -> pd.DataFrame:
    """Create a compact audit table that can be versioned in the repository."""
    duplicate_excess = int(df.duplicated(subset=SOURCE_COLUMNS, keep="first").sum())
    metrics = [
        ("transaction_lines", len(df)),
        ("source_13_field_rows", row_width_counts.get(13, 0)),
        ("source_11_field_rows_normalized", row_width_counts.get(11, 0)),
        ("missing_category_id", int(df["category_id"].isna().sum())),
        ("missing_category_code", int(df["category_code"].isna().sum())),
        ("missing_brand_code", int(df["brand_code"].isna().sum())),
        ("missing_gender", int(df["gender"].isna().sum())),
        ("missing_color", int(df["color"].isna().sum())),
        ("missing_metal", int(df["metal"].isna().sum())),
        ("missing_gem", int(df["gem"].isna().sum())),
        ("exact_duplicate_rows_in_groups", int(df["is_exact_duplicate"].sum())),
        ("exact_duplicate_excess_rows", duplicate_excess),
    ]
    quality = pd.DataFrame(metrics, columns=["metric", "value"])
    quality["pct_of_rows"] = quality["value"] / len(df) * 100
    quality.loc[quality["metric"] == "transaction_lines", "pct_of_rows"] = 100.0
    return quality


def main() -> None:
    if not RAW_FILE.exists():
        raise FileNotFoundError(
            f"Raw file not found: {RAW_FILE}\n"
            "Download the source dataset and save it as data/raw/jewelry.csv."
        )

    raw, row_width_counts = read_and_normalize(RAW_FILE)
    df = clean_types(raw)

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    QUALITY_FILE.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_FILE, index=False)
    build_quality_summary(df, row_width_counts).to_csv(QUALITY_FILE, index=False)

    print(f"Source row widths: {row_width_counts}")
    print(f"Rows: {len(df):,}")
    print(f"Orders: {df['order_id'].nunique():,}")
    print(f"Customers: {df['user_id'].nunique():,}")
    print(f"Products: {df['product_id'].nunique():,}")
    print(f"Revenue represented: ${df['line_revenue'].sum():,.2f}")
    print(f"Saved clean data: {OUTPUT_FILE}")
    print(f"Saved quality audit: {QUALITY_FILE}")


if __name__ == "__main__":
    main()
