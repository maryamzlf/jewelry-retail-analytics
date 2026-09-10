# Power BI Portfolio Report

The Power BI portion of this project is complete and validated as a four-page portfolio report.

## Final report

**Desktop artifact:** `Maryam_Jewelry_Portfolio_FINAL.pbix`  
**Canvas:** 1280 × 720  
**Pages:** 4

The PBIX binary is intentionally kept outside version control. This repository stores the validated input tables, reproducible analytical pipeline, implementation documentation, and lightweight visual previews of the final report.

For presentation, begin with **Executive Overview**. The PBIX itself preserves the validated working Desktop state rather than being externally repackaged solely to force a saved opening page.

## Report previews

- [`screenshots/01_executive_overview.svg`](screenshots/01_executive_overview.svg)
- [`screenshots/02_merchandising.svg`](screenshots/02_merchandising.svg)
- [`screenshots/03_customer_retention.svg`](screenshots/03_customer_retention.svg)
- [`screenshots/04_data_quality.svg`](screenshots/04_data_quality.svg)

## Page 1 — Executive Overview

**Header:** Jewelry Retail Performance

Purpose: give a hiring manager or business leader the complete portfolio story quickly.

Content:
- Gross Sales — **$33.18M**
- Orders — **74,760**
- Customers — **33,397**
- Average Order Value — **$443.81**
- Repeat Customer Rate — **26.9%**
- Monthly Gross Sales
- Revenue by Category
- Revenue by RFM Segment
- Executive readout with merchandising and retention implications

December 2021 is explicitly treated as a partial month.

## Page 2 — Product & Merchandising

**Header:** Merchandising & Assortment

Purpose: demonstrate assortment, pricing, category, gemstone, and SKU-level analysis.

Content:
- Category, Metal, Gemstone, and Price Band slicers
- Portfolio Revenue — **$33.18M**
- Average Item Price — **$345.94**
- Products — **9,613**
- Premium Revenue Share — **80.4%**
- Top SKU Revenue Leaders
- Revenue by Gemstone
- Average Selling Price by Category
- Merchandising Readout

The four slicers are data-bound and support interactive exploration of the merchandising charts. Headline KPI tiles and compact Top-SKU/readout panels are intentionally validated **full-snapshot reference callouts**, so they remain stable portfolio benchmarks rather than changing with exploratory filters.

## Page 3 — Customer & Retention

**Header:** Customer Value & Retention

Purpose: translate full-history RFM segmentation into retention priorities.

Content:
- RFM Customers — **33,397**
- Repeat Customers — **8,976**
- Average Customer Value — **$993.48**
- At Risk Revenue — **$5.06M**
- Champions Revenue — **$14.94M**
- Revenue by RFM Segment
- Average Customer Lifetime Value by Segment
- Highest-Value Customers
- Retention Priorities

RFM is a **fixed full-history snapshot** calculated relative to one day after the maximum observed transaction timestamp. It is not presented as dynamically recalculated by a historical date slicer.

## Page 4 — Data Quality & Audit

Purpose: make analytical controls and source limitations visible rather than hiding them.

Content:
- Source Rows — **95,911**
- Structurally Repaired Rows — **5,352**
- Missing Category — **15.9%**
- Missing Gemstone — **35.5%**
- Rows in Duplicate Groups — **5.1%**
- Revenue by Category — Taxonomy Exposure
- Duplicate Flag — Units Represented
- Attribute Completeness
- Audit Control Notes

## Data inputs

Validated Power BI-ready tables are committed under `data/`:

1. `data/jewelry_clean.csv` — 95,911 transaction lines
2. `data/customer_rfm.csv` — 33,397 customer-level RFM records

The pipeline also produces reproducible working copies at `data/processed/jewelry_clean.csv` and `outputs/generated/customer_rfm.csv`.

## As-built semantic layer

The validated final PBIX preserves the stable working import model used during development. Its report visuals bind to two imported tables:

- **`jewelry_clean (2)`** — transaction-level purchase fact table
- **`customer_rfm (2)`** — one-row-per-customer full-history RFM snapshot

Transaction, merchandising, and data-quality charts aggregate directly from `jewelry_clean (2)`. RFM charts aggregate directly from `customer_rfm (2)`. The monthly trend uses the prepared `year_month` field in the clean transaction table, so the final working artifact does **not require a separate `DimDate` table**.

The current report pages do not depend on cross-table calculations to render their business story; each analytical visual is bound to the appropriate validated import table. This keeps the portfolio artifact stable while the Python/SQL layer remains fully reproducible.

The source CSVs preserve full identifiers. The final report abbreviates product/customer IDs only in compact presentation snapshots. For a future semantic-model rebuild, identifier columns should be assigned a categorical/Text data type rather than used as continuous numeric axes.

See [`model_schema.md`](model_schema.md) for the exact as-built modeling notes. [`dax_measures.md`](dax_measures.md) is an optional reference library for extending the report with reusable measures and a date dimension; it is not a claim that every listed measure is embedded in the validated PBIX.

## Validation targets

| KPI | Value |
|---|---:|
| Transaction lines | 95,911 |
| Orders | 74,760 |
| Customers | 33,397 |
| Products | 9,613 |
| Gross Sales | $33,179,324.75 |
| Average Order Value | $443.81 |
| Repeat Customers | 8,976 |
| Repeat Customer Rate | 26.88% |

| RFM Segment | Customers | Revenue Share |
|---|---:|---:|
| Champions | 2,362 | 45.03% |
| At Risk | 1,995 | 15.24% |
| Recent Customers | 10,997 | 12.89% |
| Potential Loyalists | 7,399 | 10.92% |
| Loyal Customers | 878 | 8.57% |
| Hibernating | 9,766 | 7.35% |

## Design system

The report uses a restrained retail-analytics visual system: deep charcoal header, warm off-white canvas, muted gold commercial accent, slate/sage supporting series, muted red for risk and data-quality exceptions, Segoe UI typography, and rounded analytical cards. Decorative jewelry photography, 3D visuals, gauges, and pie charts are intentionally avoided.

## Supporting documentation

- [`dashboard_blueprint.md`](dashboard_blueprint.md) — as-built page specification
- [`model_schema.md`](model_schema.md) — exact as-built import-model notes
- [`dax_measures.md`](dax_measures.md) — optional DAX extension/reference library
- [`JewelryRetailAnalyticsTheme.json`](JewelryRetailAnalyticsTheme.json) — reusable project palette
- [`build_checklist.md`](build_checklist.md) — completed release QA record
