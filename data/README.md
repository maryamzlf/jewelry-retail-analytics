# Data

The full raw dataset is **not committed** to this repository. The source data belongs to its original authors and is available from Kaggle.

## Source

**eCommerce Purchase History from Jewelry Store** — Michael Kechinov / REES46  
Kaggle: https://www.kaggle.com/datasets/mkechinov/ecommerce-purchase-history-from-jewelry-store

The source page describes purchase history from a medium-sized online jewelry store covering December 2018 to December 2021. Each row represents a purchased product; multiple products can share an `order_id`.

## Reproduce this project

1. Download the source CSV.
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

The cleaned full file is written to `data/processed/jewelry_clean.csv` and intentionally ignored by Git. Curated summary outputs in `outputs/` are versioned so portfolio reviewers can inspect the actual analytical results without downloading the full source file.

## Included sample

`sample_jewelry.csv` contains 20 normalized records from the uploaded snapshot for schema inspection only.
