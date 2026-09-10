# Power BI Portfolio Report

The Power BI portion of this project is complete and validated as a four-page portfolio report.

## Final report

**Desktop artifact:** `Maryam_Jewelry_Portfolio_FINAL7.pbix`  
**Canvas:** 1280 × 720  
**Pages:** 4

The binary PBIX is intentionally kept outside version control. This repository stores the validated input tables, reproducible analytical pipeline, implementation documentation, and final report screenshots.

## Final screenshots

- [`screenshots/01_executive_overview.jpg`](screenshots/01_executive_overview.jpg)
- [`screenshots/02_merchandising.jpg`](screenshots/02_merchandising.jpg)
- [`screenshots/03_customer_retention.jpg`](screenshots/03_customer_retention.jpg)
- [`screenshots/04_data_quality.jpg`](screenshots/04_data_quality.jpg)

## Page 1 — Executive Overview

**Header:** Jewelry Retail Performance

Purpose: give a hiring manager or business leader the complete portfolio story quickly.

Content:
- Gross Sales — **$33.18M**
- Orders — **74,760**
- Customers — **33,397**
- Average Order Value — **$443.81**
- Repeat Customer Rate — **26.9%**
- Monthly Gross Sales trend
- Revenue by Category
- Revenue by RFM Segment
- Executive readout with the principal merchandising and retention implications

The time-series page explicitly treats December 2021 as a partial month.

## Page 2 — Product & Merchandising

**Header:** Merchandising & Assortment

Purpose: demonstrate assortment, pricing, category, gemstone, and SKU-level analysis.

Content:
- Category, Metal, Gemstone, and Price Band slicers
- Full-portfolio revenue benchmark
- Average item price
- Product count
- Premium revenue share
- Top SKU revenue leaders
- Revenue by gemstone
- Average selling price by category
- Merchandising readout

The KPI tiles on this page are full-snapshot portfolio benchmarks; slicers are used for exploratory chart analysis rather than redefining those baseline tiles.

## Page 3 — Customer & Retention

**Header:** Customer Value & Retention

Purpose: translate full-history RFM segmentation into retention priorities.

Content:
- RFM customers — **33,397**
- Repeat customers — **8,976**
- Average customer value — **$993.48**
- At Risk revenue — **$5.06M**
- Champions revenue — **$14.94M**
- Revenue by RFM segment
- Average customer lifetime value by segment
- Highest-value customer snapshot
- Retention priorities narrative

RFM is a **fixed full-history snapshot** calculated relative to the maximum transaction date. It is not presented as dynamically recalculated by a historical date slicer.

## Page 4 — Data Quality & Audit

**Header:** Data Quality & Audit

Purpose: make analytical controls and source limitations visible rather than hiding them.

Content:
- Source rows — **95,911**
- Structurally repaired rows — **5,352**
- Missing category — **15.9%**
- Missing gemstone — **35.5%**
- Rows in duplicate groups — **5.1%**
- Category revenue / taxonomy exposure
- Duplicate-flag unit exposure
- Attribute-completeness summary
- Audit control notes

## Data inputs

Validated Power BI-ready tables are committed under `data/`:

1. `data/jewelry_clean.csv` — 95,911 transaction lines
2. `data/customer_rfm.csv` — 33,397 customer-level RFM records

The source-level pipeline still writes reproducible working copies to:

- `data/processed/jewelry_clean.csv`
- `outputs/generated/customer_rfm.csv`

All large identifiers such as `order_id`, `product_id`, `user_id`, and `category_id` should be treated as **Text** in Power BI to avoid 19-digit precision loss.

## Semantic model

Conceptually, the report uses a compact transaction + customer-snapshot model:

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

The customer relationship is single-direction from the customer snapshot into transactions so segment selections can filter transaction analysis without implying that transaction filters recalculate historical RFM classifications.

The final Desktop file preserves the working model lineage used during report development. The reference documentation uses business-friendly semantic aliases (`jewelry_sales`, `CustomerRFM`) for readability.

## Validation targets

With full-snapshot filters cleared, the analytical model reconciles to:

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

RFM checks:

| Segment | Customers | Revenue Share |
|---|---:|---:|
| Champions | 2,362 | 45.03% |
| At Risk | 1,995 | 15.24% |
| Recent Customers | 10,997 | 12.89% |
| Potential Loyalists | 7,399 | 10.92% |
| Loyal Customers | 878 | 8.57% |
| Hibernating | 9,766 | 7.35% |

## Design system

The report uses a restrained retail-analytics visual system:

- Deep charcoal header
- Warm off-white canvas
- Gold commercial accent
- Slate secondary series
- Sage supporting category color
- Muted red for risk / quality exceptions
- Segoe UI typography
- Rounded white analytical cards
- No decorative jewelry photography, 3D visuals, gauges, or pie charts

The goal is to present the work as a decision-support product rather than a consumer-facing jewelry advertisement.

## Supporting files

- [`dashboard_blueprint.md`](dashboard_blueprint.md) — implemented page specification
- [`model_schema.md`](model_schema.md) — model design and RFM filter logic
- [`dax_measures.md`](dax_measures.md) — reference DAX library
- [`JewelryRetailAnalyticsTheme.json`](JewelryRetailAnalyticsTheme.json) — reusable project palette
- [`build_checklist.md`](build_checklist.md) — completed final QA record
