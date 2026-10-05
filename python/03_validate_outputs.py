"""Cross-check analytical outputs, snapshot KPIs, and portfolio tables."""

from __future__ import annotations

from pathlib import Path
import math
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "outputs"
CLEAN_FILE = ROOT / "data" / "processed" / "jewelry_clean.csv"
CUSTOMER_RFM_FILE = OUTPUT_DIR / "generated" / "customer_rfm.csv"

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

EXPECTED = {
    "transaction_lines": 95911,
    "orders": 74760,
    "customers": 33397,
    "products": 9613,
    "gross_sales": 33179324.75,
    "repeat_customers": 8976,
    "source_13_field_rows": 90559,
    "source_11_field_rows_normalized": 5352,
}

EXPECTED_RFM_COUNTS = {
    "Champions": 2362,
    "At Risk": 1995,
    "Recent Customers": 10997,
    "Potential Loyalists": 7399,
    "Loyal Customers": 878,
    "Hibernating": 9766,
}


def metric(kpis: pd.DataFrame, name: str) -> float:
    values = kpis.loc[kpis["metric"] == name, "value"]
    if len(values) != 1:
        raise AssertionError(f"Expected exactly one KPI row for {name!r}")
    return float(values.iloc[0])


def quality_metric(quality: pd.DataFrame, name: str) -> int:
    values = quality.loc[quality["metric"] == name, "value"]
    if len(values) != 1:
        raise AssertionError(f"Expected exactly one quality row for {name!r}")
    return int(values.iloc[0])


def bool_series(series: pd.Series) -> pd.Series:
    if pd.api.types.is_bool_dtype(series):
        return series.fillna(False)
    return series.astype(str).str.strip().str.lower().eq("true")


def mode_or_unknown(series: pd.Series) -> str:
    clean = series.dropna()
    return str(clean.mode().iat[0]) if not clean.empty else "Unknown"


def main() -> None:
    missing = [name for name in REQUIRED_OUTPUTS if not (OUTPUT_DIR / name).exists()]
    if missing:
        raise FileNotFoundError(f"Missing expected output files: {missing}")
    if not CLEAN_FILE.exists():
        raise FileNotFoundError(f"Missing clean dataset: {CLEAN_FILE}")
    if not CUSTOMER_RFM_FILE.exists():
        raise FileNotFoundError(f"Missing customer RFM detail: {CUSTOMER_RFM_FILE}")

    df = pd.read_csv(CLEAN_FILE, low_memory=False)
    event_time = pd.to_datetime(df["event_time"], utc=True, errors="coerce")

    kpis = pd.read_csv(OUTPUT_DIR / "kpi_summary.csv")
    annual = pd.read_csv(OUTPUT_DIR / "annual_sales.csv")
    monthly = pd.read_csv(OUTPUT_DIR / "monthly_sales.csv")
    category = pd.read_csv(OUTPUT_DIR / "category_performance.csv")
    metal = pd.read_csv(OUTPUT_DIR / "metal_performance.csv")
    gem = pd.read_csv(OUTPUT_DIR / "gem_performance.csv")
    price_band = pd.read_csv(OUTPUT_DIR / "price_band_performance.csv")
    rfm = pd.read_csv(OUTPUT_DIR / "rfm_segment_summary.csv")
    customer_rfm = pd.read_csv(CUSTOMER_RFM_FILE, low_memory=False)
    top_products = pd.read_csv(OUTPUT_DIR / "top_products.csv", dtype={"product_id": str})
    top_customers = pd.read_csv(OUTPUT_DIR / "top_customers.csv", dtype={"user_id": str})
    quality = pd.read_csv(OUTPUT_DIR / "data_quality_summary.csv")

    gross_sales = float(df["line_revenue"].sum())
    orders = int(df["order_id"].nunique())
    customers = int(df["user_id"].nunique())
    products = int(df["product_id"].nunique())
    customer_orders = df.groupby("user_id")["order_id"].nunique()
    repeat_customers = int((customer_orders > 1).sum())

    revenue_formula = (
        pd.to_numeric(df["quantity"], errors="raise")
        * pd.to_numeric(df["price"], errors="raise")
    )
    revenue_diff = np.abs(
        pd.to_numeric(df["line_revenue"], errors="raise").to_numpy(dtype=float)
        - revenue_formula.to_numpy(dtype=float)
    )

    checks: dict[str, bool] = {
        "snapshot_row_count": len(df) == EXPECTED["transaction_lines"],
        "snapshot_orders": orders == EXPECTED["orders"],
        "snapshot_customers": customers == EXPECTED["customers"],
        "snapshot_products": products == EXPECTED["products"],
        "snapshot_gross_sales": math.isclose(
            gross_sales, EXPECTED["gross_sales"], rel_tol=0, abs_tol=0.01
        ),
        "snapshot_repeat_customers": repeat_customers == EXPECTED["repeat_customers"],
        "date_parse_complete": event_time.notna().all(),
        "snapshot_start_date": event_time.min().date().isoformat() == "2018-12-01",
        "snapshot_end_date": event_time.max().date().isoformat() == "2021-12-01",
        "required_ids_complete": df[
            ["order_id", "product_id", "user_id"]
        ].notna().all().all(),
        "quantity_positive": (pd.to_numeric(df["quantity"]) > 0).all(),
        "snapshot_quantity_is_one": pd.to_numeric(df["quantity"]).eq(1).all(),
        "price_nonnegative": (pd.to_numeric(df["price"]) >= 0).all(),
        "line_revenue_formula": float(revenue_diff.max(initial=0.0)) <= 0.005,
        "kpi_row_count": int(metric(kpis, "transaction_lines")) == len(df),
        "kpi_orders": int(metric(kpis, "orders")) == orders,
        "kpi_customers": int(metric(kpis, "customers")) == customers,
        "kpi_products": int(metric(kpis, "products")) == products,
        "kpi_gross_sales": math.isclose(
            metric(kpis, "gross_sales"), gross_sales, rel_tol=0, abs_tol=0.01
        ),
        "kpi_aov": math.isclose(
            metric(kpis, "average_order_value"),
            gross_sales / orders,
            rel_tol=0,
            abs_tol=1e-10,
        ),
        "kpi_repeat_customers": int(metric(kpis, "repeat_customers"))
        == repeat_customers,
        "kpi_repeat_rate": math.isclose(
            metric(kpis, "repeat_customer_rate_pct"),
            100.0 * repeat_customers / customers,
            rel_tol=0,
            abs_tol=1e-10,
        ),
        "annual_reconciliation": math.isclose(
            gross_sales, float(annual["revenue"].sum()), rel_tol=0, abs_tol=0.01
        ),
        "monthly_reconciliation": math.isclose(
            gross_sales, float(monthly["revenue"].sum()), rel_tol=0, abs_tol=0.01
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
        "category_share_100": math.isclose(
            float(category["revenue_share_pct"].sum()), 100.0, rel_tol=0, abs_tol=1e-8
        ),
        "metal_share_100": math.isclose(
            float(metal["revenue_share_pct"].sum()), 100.0, rel_tol=0, abs_tol=1e-8
        ),
        "gem_share_100": math.isclose(
            float(gem["revenue_share_pct"].sum()), 100.0, rel_tol=0, abs_tol=1e-8
        ),
        "price_band_share_100": math.isclose(
            float(price_band["revenue_share_pct"].sum()), 100.0, rel_tol=0, abs_tol=1e-8
        ),
        "rfm_customer_count": int(rfm["customers"].sum()) == customers,
        "rfm_revenue_reconciliation": math.isclose(
            gross_sales, float(rfm["revenue"].sum()), rel_tol=0, abs_tol=0.01
        ),
        "customer_rfm_unique": customer_rfm["user_id"].is_unique,
        "customer_rfm_count": len(customer_rfm) == customers,
        "customer_rfm_revenue": math.isclose(
            gross_sales, float(customer_rfm["monetary"].sum()), rel_tol=0, abs_tol=0.01
        ),
        "quality_13_field_rows": quality_metric(quality, "source_13_field_rows")
        == EXPECTED["source_13_field_rows"],
        "quality_11_field_rows": quality_metric(
            quality, "source_11_field_rows_normalized"
        )
        == EXPECTED["source_11_field_rows_normalized"],
        "quality_missing_category_code": quality_metric(
            quality, "missing_category_code"
        )
        == int(df["category_code"].isna().sum()),
        "quality_missing_gem": quality_metric(quality, "missing_gem")
        == int(df["gem"].isna().sum()),
        "quality_duplicate_group_rows": quality_metric(
            quality, "exact_duplicate_rows_in_groups"
        )
        == int(bool_series(df["is_exact_duplicate"]).sum()),
        "quality_duplicate_excess_rows": quality_metric(
            quality, "exact_duplicate_excess_rows"
        )
        == int(df.duplicated(subset=SOURCE_COLUMNS, keep="first").sum()),
    }

    actual_rfm_counts = dict(zip(rfm["segment"], rfm["customers"].astype(int)))
    checks["rfm_regression_counts"] = actual_rfm_counts == EXPECTED_RFM_COUNTS

    detail_summary = (
        customer_rfm.groupby("segment", as_index=False)
        .agg(customers=("user_id", "size"), revenue=("monetary", "sum"))
        .sort_values("segment")
        .reset_index(drop=True)
    )
    summary_compare = (
        rfm[["segment", "customers", "revenue"]]
        .sort_values("segment")
        .reset_index(drop=True)
    )
    checks["rfm_detail_segment_counts"] = np.array_equal(
        detail_summary["customers"].to_numpy(dtype=int),
        summary_compare["customers"].to_numpy(dtype=int),
    )
    checks["rfm_detail_segment_revenue"] = np.allclose(
        detail_summary["revenue"].to_numpy(dtype=float),
        summary_compare["revenue"].to_numpy(dtype=float),
        rtol=0,
        atol=0.01,
    )

    expected_top_customers = (
        customer_rfm.sort_values(["monetary", "frequency"], ascending=False)
        .head(25)
        .reset_index(drop=True)
    )
    checks["top_customer_ids"] = (
        expected_top_customers["user_id"].astype(str).tolist()
        == top_customers["user_id"].astype(str).tolist()
    )
    checks["top_customer_values"] = np.allclose(
        expected_top_customers["monetary"].to_numpy(dtype=float),
        top_customers["monetary"].to_numpy(dtype=float),
        rtol=0,
        atol=0.01,
    )

    recomputed_products = (
        df.groupby("product_id", as_index=False)
        .agg(
            category=("category_name", mode_or_unknown),
            metal=("metal", mode_or_unknown),
            gem=("gem", mode_or_unknown),
            transaction_lines=("product_id", "size"),
            units=("quantity", "sum"),
            orders=("order_id", "nunique"),
            revenue=("line_revenue", "sum"),
            avg_item_price=("price", "mean"),
        )
        .sort_values("revenue", ascending=False)
        .head(100)
        .reset_index(drop=True)
    )
    checks["top_product_ids"] = (
        recomputed_products["product_id"].astype(str).tolist()
        == top_products["product_id"].astype(str).tolist()
    )
    checks["top_product_revenue"] = np.allclose(
        recomputed_products["revenue"].to_numpy(dtype=float),
        top_products["revenue"].to_numpy(dtype=float),
        rtol=0,
        atol=0.01,
    )

    failed = [name for name, passed in checks.items() if not bool(passed)]
    if failed:
        raise AssertionError(f"Validation failed: {failed}")

    print(f"Validated {len(checks)} analytical controls.")
    print(f"Gross sales: ${gross_sales:,.2f}")
    print(f"Orders / customers / products: {orders:,} / {customers:,} / {products:,}")
    print(f"Repeat customers: {repeat_customers:,}")
    print("RFM counts:", actual_rfm_counts)
    for name in checks:
        print(f"  PASS - {name}")


if __name__ == "__main__":
    main()
