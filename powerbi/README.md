# Power BI Dashboard Specification

This folder documents a production-style Power BI model that can be built from `data/processed/jewelry_clean.csv` or the SQL Server views in `sql/06_powerbi_views.sql`.

## Recommended model

### Fact table

`jewelry_sales`

Grain: one purchased product line.

### Dimensions

- `DimDate` — one row per calendar date, related to `jewelry_sales[order_date]`
- Optional `DimProduct` — one row per `product_id` with representative category/metal/gem attributes
- Optional `DimCustomer` — one row per `user_id` for customer/RFM enrichment

Relationship direction should be single-direction from dimensions to the fact table.

## Page 1 — Executive Overview

**KPI cards**
- Gross Sales
- Orders
- Customers
- Average Order Value
- Repeat Customer Rate

**Visuals**
- Monthly sales trend with YoY / MoM context
- Revenue by category
- Revenue by price band
- Revenue by metal and gemstone

**Slicers**
- Date
- Category
- Metal
- Gem
- Price Band

## Page 2 — Product & Merchandising

- Top 20 products by revenue
- Category revenue share and average item price
- Price-band revenue / order mix
- Gemstone x metal matrix
- Product detail drill-through: product ID, category, gem, metal, revenue, orders, units, average selling price

**Business question:** Which assortment areas drive revenue, and where do taxonomy gaps limit merchandising decisions?

## Page 3 — Customer & Retention

- New/recent vs repeat customer KPIs
- Customer lifetime value distribution
- Orders per customer distribution
- RFM segment customer share vs revenue share
- Top customer table
- Segment drill-through

**Business question:** Which customers should be retained, reactivated, or nurtured?

## Page 4 — Data Quality

- Missing category, gem, metal, color, and gender rates
- Structurally repaired row count
- Exact duplicate-group flags
- Trend of missing taxonomy over time

This page is intentionally included because the row-structure issue materially affects business conclusions if left untreated.

## Design guidance

- Keep the executive page limited to 5–7 visuals.
- Use a consistent currency format and explicit partial-period labels.
- Use tooltips for revenue share, orders, AOV, and missingness context.
- Use conditional formatting to highlight segments with high revenue but deteriorating recency.
- Do not present 2018 or December 2021 as full-period comparisons.

See `dax_measures.md` for core measures.
