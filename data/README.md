# Data

The full raw source dataset is **not committed** to this repository. The source data belongs to its original authors and is available from Kaggle.

## Source

**eCommerce Purchase History from Jewelry Store** — Michael Kechinov / REES46  
Kaggle: https://www.kaggle.com/datasets/mkechinov/ecommerce-purchase-history-from-jewelry-store

The source covers jewelry purchase history from December 2018 through December 2021. Each row represents a purchased product line; multiple product lines may share the same `order_id`.

## Power BI input tables included in this repository

- `jewelry_clean.csv` — **95,911 transaction lines**, cleaned and normalized for the Power BI fact table.
- `customer_rfm.csv` — **33,397 unique customers**, with full-history RFM metrics and customer segments.
- `sample_jewelry.csv` — 20 normalized records retained only as a lightweight schema/sample reference.

Validated portfolio totals for the full Power BI model:

- Gross Sales: **$33,179,324.75**
- Orders: **74,760**
- Customers: **33,397**
- Products: **9,613**
- Transaction date range: **2018-12-01 to 2021-12-01**

## Reproduce the project

1. Download the source CSV from Kaggle.
2. Save it as:

```text
data/raw/jewelry.csv
```

3. Run:

```bash
python python/01_prepare_data.py
python python/02_eda_rfm.py
python python/03_validate_outputs.py
```

The pipeline writes the detailed cleaned file to `data/processed/jewelry_clean.csv`, generates the detailed customer RFM table under `outputs/generated/`, and refreshes the curated analytical summaries in `outputs/`.

The GitHub Actions workflow `.github/workflows/sync-full-data.yml` reproduces the pipeline, validates the expected QA totals, and publishes the validated Power BI input tables to this `data/` directory.
