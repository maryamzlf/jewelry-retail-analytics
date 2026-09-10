# Power BI Portfolio Report

The Power BI portion of this project is complete and validated as a four-page portfolio report.

## Final report

**Desktop artifact:** `Maryam_Jewelry_Portfolio_FINAL.pbix`  
**Canvas:** 1280 × 720  
**Pages:** 4  
**Default opening page:** Executive Overview

The PBIX binary is intentionally kept outside version control. This repository stores the validated input tables, reproducible analytical pipeline, implementation documentation, and lightweight visual previews of the final report.

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

The KPI tiles are full-snapshot portfolio benchmarks; slicers support exploratory chart analysis rather than redefining those baseline tiles.

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

RFM is a **fixed full-history snapshot** calculated relative to the maximum transaction date. It is not presented as dynamically recalculated by a historical date slicer.

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

All large identifiers such as `order_id`, `product_id`, `user_id`, and `category_id` are treated as **Text** in the semantic layer to avoid precision loss on 19-digit identifiers.

## Semantic model

```text
                    DimDate
                       │
                       │ 1 : *
                       ▼
                 Jewelry Sales
                       ▲
                       │ * : 1
                       │
                  Customer RFM
```

The customer relationship is single-direction from the customer snapshot into transactions. Reference documentation uses the business-friendly aliases `jewelry_sales` and `CustomerRFM` for readability while the final Desktop file preserves the working model lineage used during development.

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
- [`model_schema.md`](model_schema.md) — model design and RFM filter logic
- [`dax_measures.md`](dax_measures.md) — reference DAX library
- [`JewelryRetailAnalyticsTheme.json`](JewelryRetailAnalyticsTheme.json) — reusable project palette
- [`build_checklist.md`](build_checklist.md) — completed release QA record
