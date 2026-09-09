"""Cross-check generated analytical outputs for internal consistency."""

from __future__ import annotations

from pathlib import Path
import math
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "outputs"
CLEAN_FILE = ROOT / "data" / "processed" / "jewelry_clean.csv"

REQUIRED_OUTPUTS = [
    "kpi_summary.csv",
    "annual_sales.csv",
    "monthly_sales.csv",
    "category_performance.csv",
    "metal_performance.csv",
    "gem_performance.csv",
    "price_band_performance.csv",
    "rfm_segment_summary.csv",
    "top_products.csv",
    "top_customers.csv",
    "data_quality_summary.csv",
]


def metric(kpis: pd.DataFrame, name: str) -> float:
    return float(kpis.loc[kpis["metric"] == name, "value"].iloc[0])


def main() -> None:
    missing = [name for name in REQUIRED_OUTPUTS if not (OUTPUT_DIR / name).exists()]
    if missing:
        raise FileNotFoundError(f"Missing expected output files: {missing}")
    if not CLEAN_FILE.exists():
        raise FileNotFoundError(f"Missing clean dataset: {CLEAN_FILE}")

    df = pd.read_csv(CLEAN_FILE)
    kpis = pd.read_csv(OUTPUT_DIR / "kpi_summary.csv")
    category = pd.read_csv(OUTPUT_DIR / "category_performance.csv")
    metal = pd.read_csv(OUTPUT_DIR / "metal_performance.csv")
    gem = pd.read_csv(OUTPUT_DIR / "gem_performance.csv")
    price_band = pd.read_csv(OUTPUT_DIR / "price_band_performance.csv")
    rfm = pd.read_csv(OUTPUT_DIR / "rfm_segment_summary.csv")

    gross_sales = metric(kpis, "gross_sales")
    checks = {
        "row_count": metric(kpis, "transaction_lines") == len(df),
        "gross_sales_vs_clean": math.isclose(
            gross_sales, float(df["line_revenue"].sum()), rel_tol=0, abs_tol=0.01
        ),
        "category_reconciliation": math.isclose(
            gross_sales, float(category["revenue"].sum()), rel_tol=0, abs_tol=0.01
        ),
        "metal_reconciliation": math.isclose(
            gross_sales, float(metal["revenue"].sum()), rel_tol=0, abs_tol=0.01
        ),
        "gem_reconciliation": math.isclose(
            gross_sales, float(gem["revenue"].sum()), rel_tol=0, abs_tol=0.01
        ),
        "price_band_reconciliation": math.isclose(
            gross_sales, float(price_band["revenue"].sum()), rel_tol=0, abs_tol=0.01
        ),
        "rfm_customer_count": int(rfm["customers"].sum())
        == int(metric(kpis, "customers")),
        "rfm_revenue_reconciliation": math.isclose(
            gross_sales, float(rfm["revenue"].sum()), rel_tol=0, abs_tol=0.01
        ),
    }

    failed = [name for name, passed in checks.items() if not passed]
    if failed:
        raise AssertionError(f"Validation failed: {failed}")

    print("All analytical reconciliation checks passed:")
    for name in checks:
        print(f"  PASS - {name}")


if __name__ == "__main__":
    main()
