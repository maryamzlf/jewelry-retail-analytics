"""Generate business summaries, RFM segmentation, and optional local charts."""

from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
INPUT_FILE = ROOT / "data" / "processed" / "jewelry_clean.csv"
OUTPUT_DIR = ROOT / "outputs"
GENERATED_DIR = OUTPUT_DIR / "generated"
CHART_DIR = GENERATED_DIR / "charts"


def assign_rfm_segment(row: pd.Series) -> str:
    """Map recency and combined frequency/monetary scores to business segments."""
    if row["r_score"] >= 4 and row["fm_score"] >= 4:
        return "Champions"
    if row["r_score"] >= 3 and row["fm_score"] >= 4:
        return "Loyal Customers"
    if row["r_score"] >= 4 and row["fm_score"] <= 3:
        return "Recent Customers"
    if row["r_score"] <= 2 and row["fm_score"] >= 4:
        return "At Risk"
    if row["r_score"] <= 2 and row["fm_score"] <= 2:
        return "Hibernating"
    return "Potential Loyalists"


def create_kpi_summary(df: pd.DataFrame) -> pd.DataFrame:
    customer_orders = df.groupby("user_id")["order_id"].nunique()
    order_items = df.groupby("order_id")["quantity"].sum()
    order_lines = df.groupby("order_id").size()
    gross_sales = df["line_revenue"].sum()
    orders = df["order_id"].nunique()

    return pd.DataFrame(
        {
            "metric": [
                "transaction_lines",
                "orders",
                "customers",
                "products",
                "gross_sales",
                "average_order_value",
                "average_item_price",
                "average_items_per_order",
                "multi_line_order_rate_pct",
                "repeat_customers",
                "repeat_customer_rate_pct",
            ],
            "value": [
                len(df),
                orders,
                df["user_id"].nunique(),
                df["product_id"].nunique(),
                gross_sales,
                gross_sales / orders,
                df["price"].mean(),
                order_items.mean(),
                (order_lines > 1).mean() * 100,
                int((customer_orders > 1).sum()),
                (customer_orders > 1).mean() * 100,
            ],
        }
    )


def group_performance(
    df: pd.DataFrame, dimension: str, unknown_label: str = "Unknown"
) -> pd.DataFrame:
    temp = df.copy()
    temp[dimension] = temp[dimension].fillna(unknown_label)
    result = (
        temp.groupby(dimension, as_index=False, dropna=False)
        .agg(
            transaction_lines=("product_id", "size"),
            units=("quantity", "sum"),
            orders=("order_id", "nunique"),
            customers=("user_id", "nunique"),
            revenue=("line_revenue", "sum"),
            avg_item_price=("price", "mean"),
        )
        .sort_values("revenue", ascending=False)
    )
    result["revenue_share_pct"] = result["revenue"] / df["line_revenue"].sum() * 100
    return result


def create_monthly_sales(df: pd.DataFrame) -> pd.DataFrame:
    monthly = (
        df.groupby("year_month", as_index=False)
        .agg(
            revenue=("line_revenue", "sum"),
            orders=("order_id", "nunique"),
            customers=("user_id", "nunique"),
            units=("quantity", "sum"),
        )
        .sort_values("year_month")
    )
    monthly["average_order_value"] = monthly["revenue"] / monthly["orders"]
    monthly["mom_revenue_pct"] = monthly["revenue"].pct_change() * 100
    return monthly


def create_annual_sales(df: pd.DataFrame) -> pd.DataFrame:
    temp = df.assign(year=df["event_time"].dt.year)
    annual = (
        temp.groupby("year", as_index=False)
        .agg(
            revenue=("line_revenue", "sum"),
            orders=("order_id", "nunique"),
            customers=("user_id", "nunique"),
            units=("quantity", "sum"),
        )
        .sort_values("year")
    )
    annual["average_order_value"] = annual["revenue"] / annual["orders"]
    annual["yoy_revenue_pct"] = annual["revenue"].pct_change() * 100
    return annual


def create_price_band_performance(df: pd.DataFrame) -> pd.DataFrame:
    order = ["Under $100", "$100-$249", "$250-$499", "$500-$999", "$1,000+"]
    temp = df.copy()
    temp["price_band"] = pd.Categorical(temp["price_band"], categories=order, ordered=True)
    result = (
        temp.groupby("price_band", as_index=False, observed=False)
        .agg(
            transaction_lines=("product_id", "size"),
            units=("quantity", "sum"),
            orders=("order_id", "nunique"),
            revenue=("line_revenue", "sum"),
            avg_item_price=("price", "mean"),
        )
        .sort_values("price_band")
    )
    result["revenue_share_pct"] = result["revenue"] / df["line_revenue"].sum() * 100
    return result


def create_customer_outputs(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    customer = (
        df.groupby("user_id", as_index=False)
        .agg(
            first_purchase=("event_time", "min"),
            last_purchase=("event_time", "max"),
            frequency=("order_id", "nunique"),
            transaction_lines=("product_id", "size"),
            units=("quantity", "sum"),
            monetary=("line_revenue", "sum"),
        )
    )
    customer["customer_aov"] = customer["monetary"] / customer["frequency"]

    analysis_date = df["event_time"].max() + pd.Timedelta(days=1)
    customer["recency_days"] = (analysis_date - customer["last_purchase"]).dt.days

    # Recency and monetary use quintiles. Frequency is highly zero-inflated at
    # one order (73% of customers), so business-rule bins avoid arbitrary
    # tie-breaking that would otherwise promote one-order customers.
    customer["r_score"] = pd.qcut(
        customer["recency_days"].rank(method="first"),
        5,
        labels=[5, 4, 3, 2, 1],
    ).astype(int)
    customer["f_score"] = pd.cut(
        customer["frequency"],
        bins=[0, 1, 2, 4, 9, float("inf")],
        labels=[1, 2, 3, 4, 5],
    ).astype(int)
    customer["m_score"] = pd.qcut(
        customer["monetary"].rank(method="first"),
        5,
        labels=[1, 2, 3, 4, 5],
    ).astype(int)
    customer["fm_score"] = np.rint(
        (customer["f_score"] + customer["m_score"]) / 2
    ).astype(int)
    customer["segment"] = customer.apply(assign_rfm_segment, axis=1)

    segment_summary = (
        customer.groupby("segment", as_index=False)
        .agg(
            customers=("user_id", "size"),
            revenue=("monetary", "sum"),
            avg_lifetime_value=("monetary", "mean"),
            avg_orders=("frequency", "mean"),
            avg_recency_days=("recency_days", "mean"),
        )
        .sort_values("revenue", ascending=False)
    )
    segment_summary["customer_share_pct"] = (
        segment_summary["customers"] / len(customer) * 100
    )
    segment_summary["revenue_share_pct"] = (
        segment_summary["revenue"] / customer["monetary"].sum() * 100
    )

    top_customers = customer.sort_values(
        ["monetary", "frequency"], ascending=False
    ).head(25)

    return customer, segment_summary, top_customers


def create_top_products(df: pd.DataFrame) -> pd.DataFrame:
    def mode_or_unknown(series: pd.Series) -> str:
        clean = series.dropna()
        return str(clean.mode().iat[0]) if not clean.empty else "Unknown"

    return (
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
    )


def save_local_charts(
    monthly: pd.DataFrame,
    category: pd.DataFrame,
    rfm_summary: pd.DataFrame,
) -> None:
    """Create local chart previews; generated files are intentionally git-ignored."""
    CHART_DIR.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(11, 5))
    ax.plot(monthly["year_month"], monthly["revenue"])
    ax.set_title("Monthly Gross Sales")
    ax.set_xlabel("Month")
    ax.set_ylabel("Revenue")
    ax.tick_params(axis="x", rotation=75)
    fig.tight_layout()
    fig.savefig(CHART_DIR / "monthly_sales_trend.png", dpi=150)
    plt.close(fig)

    top_categories = category.head(8).sort_values("revenue")
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.barh(top_categories["category_name"], top_categories["revenue"])
    ax.set_title("Revenue by Category")
    ax.set_xlabel("Revenue")
    fig.tight_layout()
    fig.savefig(CHART_DIR / "category_revenue.png", dpi=150)
    plt.close(fig)

    segment_chart = rfm_summary.sort_values("revenue")
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.barh(segment_chart["segment"], segment_chart["revenue"])
    ax.set_title("Revenue by RFM Segment")
    ax.set_xlabel("Revenue")
    fig.tight_layout()
    fig.savefig(CHART_DIR / "rfm_segment_revenue.png", dpi=150)
    plt.close(fig)


def main() -> None:
    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"Clean file not found: {INPUT_FILE}. Run 01_prepare_data.py first."
        )

    df = pd.read_csv(INPUT_FILE, parse_dates=["event_time"])
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    GENERATED_DIR.mkdir(parents=True, exist_ok=True)

    kpis = create_kpi_summary(df)
    category = group_performance(df, "category_name")
    metal = group_performance(df, "metal")
    gem = group_performance(df, "gem")
    price_band = create_price_band_performance(df)
    monthly = create_monthly_sales(df)
    annual = create_annual_sales(df)
    customer, rfm_summary, top_customers = create_customer_outputs(df)
    top_products = create_top_products(df)

    outputs = {
        "kpi_summary.csv": kpis,
        "annual_sales.csv": annual,
        "monthly_sales.csv": monthly,
        "category_performance.csv": category,
        "metal_performance.csv": metal,
        "gem_performance.csv": gem,
        "price_band_performance.csv": price_band,
        "rfm_segment_summary.csv": rfm_summary,
        "top_products.csv": top_products,
        "top_customers.csv": top_customers,
    }
    for filename, table in outputs.items():
        table.to_csv(OUTPUT_DIR / filename, index=False)

    customer.sort_values(["monetary", "frequency"], ascending=False).to_csv(
        GENERATED_DIR / "customer_rfm.csv", index=False
    )
    save_local_charts(monthly, category, rfm_summary)

    print(f"Curated analysis outputs written to: {OUTPUT_DIR}")
    print(f"Detailed customer RFM and charts written to: {GENERATED_DIR}")


if __name__ == "__main__":
    main()
