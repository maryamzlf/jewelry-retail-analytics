# Jewelry Retail Analytics

End-to-end **SQL + Python + Power BI** portfolio project that turns messy jewelry e-commerce purchase data into decision-ready sales, merchandising, customer-retention, and data-quality insights.

## Executive Snapshot

| Metric | Result |
|---|---:|
| Transaction lines | **95,911** |
| Orders | **74,760** |
| Customers | **33,397** |
| Products | **9,613** |
| Gross sales represented | **$33.18M** |
| Average order value | **$443.81** |
| Repeat customer rate | **26.88%** |

## Key Business Findings

- **Earrings + rings generate 65.93% of revenue**, making them the core merchandising categories.
- **Gold represents 98.54% of revenue** and diamond products contribute **44.81%**.
- **80.42% of revenue comes from items priced at $250+**, showing a strongly premium sales mix.
- Only **26.88% of customers are repeat buyers**.
- **Champions are just 7.07% of customers but generate 45.03% of revenue**.
- **At Risk customers are 5.97% of customers yet represent 15.24% of historical revenue**, creating a clear reactivation opportunity.
- A major data-quality issue was found: **5,352 source rows had only 11 physical fields instead of 13**. The Python pipeline repairs them before parsing so price and customer fields do not shift into the wrong columns.

See [`docs/findings.md`](docs/findings.md) for the full analytical interpretation and recommendations.

## Business Questions

1. How are revenue, order volume, and AOV trending over time?
2. Which jewelry categories, metals, gemstones, products, and price bands drive revenue?
3. How concentrated is revenue among repeat and high-value customers?
4. Which customers should be retained, nurtured, or reactivated?
5. What basket-expansion opportunities exist?
6. Which data-quality issues could distort business conclusions?

## Analytical Workflow

```text
Raw jewelry.csv
      │
      ▼
Python structural repair + validation
      │
      ├──► Clean analytical dataset
      │
      ├──► Curated KPI / merchandising / RFM outputs
      │
      ▼
SQL Server analytical layer
      │
      ▼
Power BI semantic model + dashboard specification
```

## Why the Data Preparation Matters

The uploaded source snapshot has **no header row** and mixes two physical record layouts:

- 90,559 rows with 13 fields
- 5,352 rows with 11 fields

In the 11-field form, `category_code` and `brand` are absent. A normal `pandas.read_csv()` call causes later fields such as `price` and `user_id` to shift into the wrong columns. `python/01_prepare_data.py` repairs this structure at the raw CSV-line level before any type conversion or analysis.

The project also flags exact duplicate groups instead of deleting them blindly because identical purchase lines may represent legitimately repeated units.

## Repository Structure

```text
jewelry-retail-analytics/
├── data/
│   ├── README.md
│   └── sample_jewelry.csv
├── docs/
│   ├── data_dictionary.md
│   ├── methodology.md
│   └── findings.md
├── outputs/
│   ├── README.md
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
│   ├── README.md
│   └── dax_measures.md
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
├── .gitignore
├── requirements.txt
└── README.md
```

## Skills Demonstrated

### Python
- Defensive CSV ingestion
- Structural data repair
- Type validation and null auditing
- Feature engineering
- KPI and merchandising analysis
- Customer lifetime value
- RFM segmentation
- Cross-output reconciliation / QA

### SQL Server / T-SQL
- Data modeling and indexes
- Data-quality auditing
- CTEs
- Window functions (`LAG`, `NTILE`, `DENSE_RANK`)
- Customer LTV and repeat-rate analysis
- Merchandising and price-band analysis
- Power BI-ready views

### Power BI
- Star-schema design
- Executive, merchandising, customer, and data-quality dashboard pages
- Core DAX measures for sales, AOV, retention, MoM, and YoY performance
- Drill-through and slicer strategy

## Reproduce the Analysis

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Add the source file

Place the downloaded dataset at:

```text
data/raw/jewelry.csv
```

### 3. Prepare and validate the data

```bash
python python/01_prepare_data.py
```

This writes the full cleaned file to:

```text
data/processed/jewelry_clean.csv
```

### 4. Generate analytical outputs

```bash
python python/02_eda_rfm.py
```

### 5. Reconcile outputs

```bash
python python/03_validate_outputs.py
```

The validation script confirms that revenue reconciles across the cleaned data, category, metal, gemstone, price-band, and RFM outputs.

### 6. SQL Server

Run the SQL files in order after importing `jewelry_clean.csv`:

1. `sql/01_create_table.sql`
2. `sql/02_data_quality.sql`
3. `sql/03_business_kpis.sql`
4. `sql/04_customer_analysis.sql`
5. `sql/05_merchandising_analysis.sql`
6. `sql/06_powerbi_views.sql`

### 7. Power BI

Use the cleaned CSV or SQL views, then follow [`powerbi/README.md`](powerbi/README.md) and [`powerbi/dax_measures.md`](powerbi/dax_measures.md).

## Dataset

**Source:** *eCommerce Purchase History from Jewelry Store* by Michael Kechinov / REES46  
https://www.kaggle.com/datasets/mkechinov/ecommerce-purchase-history-from-jewelry-store

The public source describes purchase data from a medium-sized online jewelry store from December 2018 to December 2021. Each row represents a purchased product, and multiple products can share one `order_id`.

This repository analyzes the uploaded snapshot used for this portfolio project. The full source dataset is not committed; only a 20-row normalized sample and curated analytical outputs are included.

## Important Interpretation Notes

- 2018 is a partial period in this snapshot.
- December 2021 contains only December 1 activity and should not be compared as a complete month.
- Revenue is not profit because product cost and margin fields are not available.
- Missing category and gemstone attributes are material and are reported explicitly rather than silently imputed.
