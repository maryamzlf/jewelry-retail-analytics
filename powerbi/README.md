# Power BI Portfolio Build

This folder contains the complete implementation package for the Power BI portion of the Jewelry Retail Analytics portfolio project.

The only artifact that must still be created manually in **Power BI Desktop** is the binary `.pbix` file itself. Everything needed to build it consistently is documented here.

## Files

| File | Purpose |
|---|---|
| [`dashboard_blueprint.md`](dashboard_blueprint.md) | Exact 4-page dashboard layout, visual types, field assignments, interactions, drill-through, sizing and portfolio design rules |
| [`model_schema.md`](model_schema.md) | Table grain, relationships, cross-filter direction and RFM snapshot modeling logic |
| [`dax_measures.md`](dax_measures.md) | Complete DAX measure library for KPIs, retention, RFM, merchandising, time intelligence and data quality |
| [`JewelryRetailAnalyticsTheme.json`](JewelryRetailAnalyticsTheme.json) | Importable Power BI theme with professional gold/charcoal retail-analytics styling |
| [`build_checklist.md`](build_checklist.md) | Step-by-step QA checklist from data import through final GitHub screenshots |

## Required data inputs

Run the Python pipeline first:

```bash
python python/01_prepare_data.py
python python/02_eda_rfm.py
python python/03_validate_outputs.py
```

Then import these into Power BI Desktop:

1. `data/processed/jewelry_clean.csv` → `jewelry_sales`
2. `outputs/generated/customer_rfm.csv` → `CustomerRFM`
3. Optional: `outputs/data_quality_summary.csv` → `DataQualitySummary`

All large identifiers such as `order_id`, `product_id`, `user_id`, and `category_id` must be imported as **Text** to protect 19-digit precision.

## Final report structure

### Page 1 — Executive Overview

Focus:
- Gross Sales
- Orders
- Customers
- AOV
- Repeat Customer Rate
- Monthly sales trend
- Category performance
- Price-band mix
- Metal/gem mix

### Page 2 — Product & Merchandising

Focus:
- Top products
- Category revenue vs selling price
- Category × gemstone matrix
- Product attribute completeness
- Product drill-through

### Page 3 — Customer & Retention

Focus:
- Snapshot RFM segmentation
- Customer share vs revenue share
- Customer value vs recency
- Top customers
- At Risk reactivation opportunity

`CustomerRFM` is a fixed snapshot built from each customer's full observed history. Do not imply that a normal date slicer dynamically recalculates the RFM segments.

### Page 4 — Data Quality & Audit

Focus:
- 5,352 structurally repaired source rows
- Missing category/gem/metal/gender/color rates
- Category completeness trend
- Exact duplicate-group audit
- Explanation of why duplicates are flagged rather than automatically deleted

## Model

```text
                    DimDate
                       │
                       │ 1 : *
                       ▼
                 jewelry_sales
                       ▲
                       │ * : 1
                       │
                  CustomerRFM
```

Relationships are active and single-direction.

## Theme

In Power BI Desktop:

`View → Themes → Browse for themes`

Import:

`JewelryRetailAnalyticsTheme.json`

The design intentionally avoids decorative jewelry imagery and uses a restrained gold/charcoal palette so the work reads as **business intelligence and retail analytics**, not as a consumer marketing presentation.

## Portfolio validation targets

With report filters cleared, the final model should reconcile approximately to:

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

Key RFM check:

- Champions: 2,362 customers / 45.03% of revenue
- At Risk: 1,995 customers / 15.24% of revenue

If these do not reconcile, check data types, relationships, active filters and ID precision before styling the report.

## GitHub finishing step

After the `.pbix` is built, add four high-resolution screenshots under:

```text
powerbi/screenshots/
```

Recommended names:

```text
01_executive_overview.png
02_merchandising.png
03_customer_retention.png
04_data_quality.png
```

Then embed the Executive Overview screenshot near the top of the repository's main README.

At that point the Power BI portion is fully demonstrated visually and the project can accurately be described on a resume as an **interactive Power BI dashboard**, not only a dashboard design/specification.
