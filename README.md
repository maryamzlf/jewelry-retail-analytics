# Jewelry Retail Analytics

End-to-end **SQL + Python + Power BI** portfolio project that transforms messy jewelry e-commerce purchase history into decision-ready sales, merchandising, customer-retention, and data-quality insights.

![Jewelry Retail Performance — Executive Overview](powerbi/screenshots/01_executive_overview.svg)

## Project at a Glance

| Metric | Result |
|---|---:|
| Transaction lines | **95,911** |
| Orders | **74,760** |
| Customers | **33,397** |
| Products | **9,613** |
| Gross sales represented | **$33.18M** |
| Average order value | **$443.81** |
| Repeat customers | **8,976** |
| Repeat customer rate | **26.88%** |

The completed Power BI report contains four portfolio pages: **Executive Overview**, **Product & Merchandising**, **Customer & Retention**, and **Data Quality & Audit**. The validated Desktop artifact is `Maryam_Jewelry_Portfolio_FINAL7.pbix`. The PBIX binary is kept outside version control; this repository contains the reproducible pipeline, validated Power BI input tables, SQL analytical layer, documentation, and lightweight dashboard previews.

## Key Business Findings

- **Earrings + Rings generate 65.93% of revenue**, making them the commercial center of the category mix.
- **Gold represents 98.54% of revenue**, while diamond products contribute **44.81%**.
- **80.42% of revenue comes from items priced at $250+**, indicating a strongly premium sales mix.
- Only **26.88% of customers are repeat buyers**, making retention a major growth opportunity.
- **Champions are 7.07% of customers but generate 45.03% of revenue**.
- **At Risk customers are 5.97% of customers but represent 15.24% of historical revenue**, creating a high-value reactivation opportunity.
- **5,352 source rows contain 11 physical fields instead of 13**. The ingestion layer repairs them before parsing so price and customer identifiers do not shift into incorrect columns.
- Product-master completeness is material: category code is missing on **15.94%** of rows and gemstone on **35.51%**.

See [`docs/findings.md`](docs/findings.md) for the full analytical interpretation and recommendations.

## Power BI Portfolio Pages

| Executive Overview | Merchandising & Assortment |
|---|---|
| ![Executive Overview](powerbi/screenshots/01_executive_overview.svg) | ![Merchandising](powerbi/screenshots/02_merchandising.svg) |
| **Customer Value & Retention** | **Data Quality & Audit** |
| ![Customer & Retention](powerbi/screenshots/03_customer_retention.svg) | ![Data Quality & Audit](powerbi/screenshots/04_data_quality.svg) |

The report uses a restrained charcoal, warm-white, gold, sage, and risk-red visual system so the work reads as **business intelligence and retail analytics**, not as a consumer jewelry advertisement.

## Business Questions

1. How are revenue, order volume, and average order value trending over time?
2. Which categories, metals, gemstones, products, and price bands drive revenue?
3. How concentrated is revenue among high-value and repeat customers?
4. Which customer segments should be protected, nurtured, or reactivated?
5. Where are the strongest premium assortment opportunities?
6. Which data-quality issues materially constrain decision quality?

## Analytical Workflow

```text
Kaggle source: jewelry.csv
        │
        ▼
Python structural repair + validation
        │
        ├──► Clean transaction fact table
        ├──► Customer RFM table
        └──► Curated analytical outputs
        │
        ▼
SQL Server analytical layer
        │
        ▼
Power BI dashboard
        ├──► Executive performance
        ├──► Merchandising & assortment
        ├──► Customer value & retention
        └──► Data quality & audit
```

## Why the Data Preparation Matters

The source snapshot mixes two physical record layouts:

- **90,559** standard 13-field rows
- **5,352** irregular 11-field rows

In the 11-field layout, `category_code` and `brand` are absent. A naive CSV import can shift downstream fields such as `price` and `user_id` into the wrong columns. [`python/01_prepare_data.py`](python/01_prepare_data.py) repairs the physical record structure **before** type conversion and analysis.

Exact duplicate groups are **flagged rather than blindly deleted**. Because rows represent purchased product lines, identical records can indicate either a duplicate-data problem or legitimate identical units when no authoritative line key is available.

## Repository Structure

```text
jewelry-retail-analytics/
├── .github/workflows/
│   └── sync-full-data.yml
├── data/
│   ├── README.md
│   ├── jewelry_clean.csv
│   ├── customer_rfm.csv
│   └── sample_jewelry.csv
├── docs/
│   ├── data_dictionary.md
│   ├── methodology.md
│   └── findings.md
├── outputs/
│   ├── kpi_summary.csv
│   ├── annual_sales.csv
│   ├── monthly_sales.csv
│   ├── category_performance.csv
│   ├── metal_performance.csv
│   ├── gem_performance.csv
│   ├── price_band_performance.csv
│   ├── rfm_segment_summary.csv
│   ├── top_products.csv
│   ├── top_customers.csv
│   └── data_quality_summary.csv
├── powerbi/
│   ├── screenshots/
│   │   ├── 01_executive_overview.svg
│   │   ├── 02_merchandising.svg
│   │   ├── 03_customer_retention.svg
│   │   └── 04_data_quality.svg
│   ├── README.md
│   ├── dashboard_blueprint.md
│   ├── dax_measures.md
│   ├── model_schema.md
│   ├── build_checklist.md
│   └── JewelryRetailAnalyticsTheme.json
├── python/
│   ├── 01_prepare_data.py
│   ├── 02_eda_rfm.py
│   └── 03_validate_outputs.py
├── sql/
│   ├── 01_create_table.sql
│   ├── 02_data_quality.sql
│   ├── 03_business_kpis.sql
│   ├── 04_customer_analysis.sql
│   ├── 05_merchandising_analysis.sql
│   └── 06_powerbi_views.sql
├── requirements.txt
└── README.md
```

## Skills Demonstrated

**Python:** defensive CSV ingestion, structural normalization, type validation, feature engineering, RFM segmentation, KPI generation, merchandising analysis, and cross-output reconciliation.

**SQL Server / T-SQL:** analytical schema design, indexes, data-quality audits, CTEs, window functions, customer value analysis, RFM scoring, merchandising queries, and Power BI-ready views.

**Power BI:** executive dashboard design, merchandising analysis, RFM storytelling, data-quality reporting, KPI presentation, interactive exploration, business-focused visual design, and portfolio-grade information hierarchy.

## Reproduce the Analysis

```bash
pip install -r requirements.txt
```

Download the Kaggle source and save it as:

```text
data/raw/jewelry.csv
```

Run the pipeline:

```bash
python python/01_prepare_data.py
python python/02_eda_rfm.py
python python/03_validate_outputs.py
```

The validation step reconciles represented revenue across the clean fact table, category, metal, gemstone, price-band, and RFM outputs.

For the SQL Server layer, run the files under `sql/` in numeric order after importing the cleaned transaction table.

See [`powerbi/README.md`](powerbi/README.md) for the implemented report, validation targets, model notes, and page-level design details.

## Dataset

**Source:** *eCommerce Purchase History from Jewelry Store* by Michael Kechinov / REES46  
https://www.kaggle.com/datasets/mkechinov/ecommerce-purchase-history-from-jewelry-store

The raw Kaggle source is not committed. This repository **does include validated cleaned Power BI input tables** (`data/jewelry_clean.csv` and `data/customer_rfm.csv`) plus curated analytical outputs so reviewers can inspect the actual analytical results without reproducing the pipeline first.

## Interpretation Notes

- 2018 is a partial period in the analyzed snapshot.
- December 2021 contains only December 1 activity and is not a complete month.
- Revenue is not profit because cost and margin fields are unavailable.
- Inventory, returns, promotions, traffic, and conversion data are not present.
- Missing product attributes constrain some assortment conclusions and are treated as a business finding rather than hidden through imputation.
- RFM segments are a **full-history snapshot** relative to the end of the observed dataset; they should not be interpreted as dynamically recalculated historical segments.
