# Power BI Build Checklist

Use this checklist to turn the documented model into the final `.pbix` portfolio artifact.

## A. Data preparation

- [ ] Run `python/01_prepare_data.py`
- [ ] Run `python/02_eda_rfm.py`
- [ ] Run `python/03_validate_outputs.py`
- [ ] Confirm `data/processed/jewelry_clean.csv` exists
- [ ] Confirm `outputs/generated/customer_rfm.csv` exists
- [ ] Confirm all reconciliation checks return PASS

## B. Import into Power BI Desktop

Import:

1. `data/processed/jewelry_clean.csv` → rename table to `jewelry_sales`
2. `outputs/generated/customer_rfm.csv` → rename table to `CustomerRFM`
3. Optional: `outputs/data_quality_summary.csv` → rename table to `DataQualitySummary`

Set IDs such as `order_id`, `product_id`, `user_id`, and `category_id` to **Text**, not Whole Number, to prevent loss of precision on 19-digit identifiers.

## C. Data types

### jewelry_sales

- `event_time` → Date/Time/Timezone if available; otherwise Date/Time
- `order_date` → Date
- `quantity` → Whole Number
- `price` → Fixed Decimal Number
- `line_revenue` → Fixed Decimal Number
- `order_id` → Text
- `product_id` → Text
- `user_id` → Text
- `category_id` → Text
- `brand_code` → Whole Number
- `is_exact_duplicate` → True/False

### CustomerRFM

- `user_id` → Text
- `first_purchase` → Date/Time
- `last_purchase` → Date/Time
- `frequency` → Whole Number
- `monetary` → Fixed Decimal Number
- `customer_aov` → Fixed Decimal Number
- `recency_days` → Whole Number
- `r_score`, `f_score`, `m_score`, `fm_score` → Whole Number
- `segment` → Text

## D. Date table

- [ ] Create `DimDate` using the DAX in `dax_measures.md`
- [ ] Add `Year Month Sort = YEAR([Date]) * 100 + MONTH([Date])`
- [ ] Sort `DimDate[Year Month]` by `DimDate[Year Month Sort]`
- [ ] Mark `DimDate` as the Date Table
- [ ] Relate `DimDate[Date]` 1 → * `jewelry_sales[order_date]`

## E. Customer relationship

- [ ] Relate `CustomerRFM[user_id]` 1 → * `jewelry_sales[user_id]`
- [ ] Cross-filter direction = Single
- [ ] Confirm `CustomerRFM[user_id]` is unique

## F. Theme

In Power BI Desktop:

`View → Themes → Browse for themes`

Import:

`powerbi/JewelryRetailAnalyticsTheme.json`

Then set page canvas background to `#F7F5F2` if the theme does not apply it automatically to the page.

## G. Measures

Create every measure in `powerbi/dax_measures.md`.

Recommended display folders:

- `01 Executive KPIs`
- `02 Customer & Retention`
- `03 Merchandising`
- `04 Time Intelligence`
- `05 Data Quality`

## H. Build pages

Follow `dashboard_blueprint.md` exactly.

- [ ] Page 1 — Executive Overview
- [ ] Page 2 — Product & Merchandising
- [ ] Page 3 — Customer & Retention
- [ ] Page 4 — Data Quality & Audit
- [ ] Product Detail drill-through page

## I. Verify portfolio numbers

With all report filters cleared, cards should reconcile approximately to:

| KPI | Expected value |
|---|---:|
| Gross Sales | $33,179,324.75 |
| Orders | 74,760 |
| Customers | 33,397 |
| Products | 9,613 |
| Average Order Value | $443.81 |
| Repeat Customers | 8,976 |
| Repeat Customer Rate | 26.88% |

RFM cross-check:

| Segment | Customers | Revenue Share |
|---|---:|---:|
| Champions | 2,362 | 45.03% |
| At Risk | 1,995 | 15.24% |
| Recent Customers | 10,997 | 12.89% |
| Potential Loyalists | 7,399 | 10.92% |
| Loyal Customers | 878 | 8.57% |
| Hibernating | 9,766 | 7.35% |

If these values do not reconcile, stop and check relationships, data types, filters, and whether IDs were imported as numbers rather than text.

## J. Interaction QA

- [ ] Date slicer filters Pages 1–3 correctly
- [ ] Category selection cross-filters related visuals
- [ ] RFM segment filters Customer page visuals
- [ ] Share measures retain intended denominators
- [ ] Drill-through works from product visuals
- [ ] Tooltips show correct metrics
- [ ] No visual displays `(Blank)` when `Unknown` is the intended label

## K. Presentation QA

- [ ] Currency measures use consistent formatting
- [ ] Percentage measures use one decimal place unless needed
- [ ] 2018 is labeled as a partial period
- [ ] December 2021 is labeled as partial
- [ ] Visual titles state business meaning
- [ ] No pie/donut charts
- [ ] No 3D charts
- [ ] No excessive data labels
- [ ] All visuals align to a consistent grid
- [ ] Each page has sufficient white space
- [ ] Alt text added to major visuals

## L. GitHub screenshots

Create folder locally:

`powerbi/screenshots/`

Capture at high resolution:

- `01_executive_overview.png`
- `02_merchandising.png`
- `03_customer_retention.png`
- `04_data_quality.png`

After screenshots are committed, embed `01_executive_overview.png` near the top of the main README.

## M. Resume wording after `.pbix` is actually built

Once the dashboard exists, it is accurate to write:

> Built an end-to-end jewelry retail analytics solution using Python, SQL Server, and Power BI, analyzing 95K+ transaction lines, 74K+ orders, 33K+ customers, and $33M+ in sales; developed interactive executive, merchandising, retention, and data-quality dashboards with RFM segmentation and DAX-based KPI reporting.
