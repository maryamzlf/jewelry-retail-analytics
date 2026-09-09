# Power BI Dashboard Blueprint

This document is the exact build specification for the portfolio dashboard.

## Canvas and visual system

- Page size: **16:9 — 1280 x 720**
- Background: `#F7F5F2`
- Primary text: `#222222`
- Secondary text: `#6B6B6B`
- Accent gold: `#B58A3B`
- Deep charcoal: `#2F3136`
- White cards: `#FFFFFF`
- Border: `#E4DED5`
- Positive indicator: `#3E7C59`
- Warning / risk: `#A55353`
- Font: Segoe UI
- Page title: 24 pt semibold
- KPI value: 24–28 pt semibold
- Visual title: 12–14 pt semibold
- Body / labels: 10–11 pt
- Card corner radius: 8–10 px
- Card shadow: subtle only

Do not use jewelry photography, gradients, 3D charts, gauges, pie charts, or decorative icons that compete with the data. The dashboard should look like a professional retail analytics product rather than a jewelry advertisement.

---

# Page 1 — Executive Overview

**Purpose:** Give a hiring manager or business leader the complete story in less than 30 seconds.

## Header

**Position:** x=32, y=24, w=1168, h=48  
**Text:** `Jewelry Retail Performance Overview`  
**Subtitle:** `Sales, customers, product mix and retention | Dec 2018–Dec 2021 snapshot`

## KPI row

Five cards, each approximately 216 x 94, y=88.

| Card | Measure | Position |
|---|---|---|
| Gross Sales | `[Gross Sales]` | x=32 |
| Orders | `[Orders]` | x=264 |
| Customers | `[Customers]` | x=496 |
| Average Order Value | `[Average Order Value]` | x=728 |
| Repeat Customer Rate | `[Repeat Customer Rate]` | x=960 |

Formatting:
- Gross Sales: `$0.00,,M`
- Orders / Customers: `0.0,K`
- AOV: `$0.00`
- Repeat Customer Rate: `0.0%`

## Visual 1 — Monthly Gross Sales Trend

**Type:** Line chart  
**Position:** x=32, y=208, w=744, h=270

- X-axis: `DimDate[Year Month]`
- Y-axis: `[Gross Sales]`
- Tooltip: `[Orders]`, `[Customers]`, `[Average Order Value]`, `[MoM Sales %]`
- Sort by: `DimDate[Year Month Sort]`
- Add a vertical annotation/note that December 2021 is partial.

Title: `Monthly Gross Sales`

## Visual 2 — Revenue by Category

**Type:** Horizontal bar chart  
**Position:** x=800, y=208, w=400, h=270

- Y-axis: `jewelry_sales[category_name]`
- X-axis: `[Gross Sales]`
- Tooltip: `[Orders]`, `[Average Item Price]`, `[Category Revenue Share]`
- Sort descending by Gross Sales
- Data labels: on

Title: `Revenue by Category`

## Visual 3 — Revenue by Price Band

**Type:** Column chart  
**Position:** x=32, y=502, w=550, h=178

- X-axis: `jewelry_sales[price_band]`
- Y-axis: `[Gross Sales]`
- Sort using a numeric `Price Band Sort` column: 1–5
- Tooltip: `[Orders]`, `[Units]`, `[Average Item Price]`

Title: `Revenue by Price Band`

## Visual 4 — Product Mix

**Type:** 100% stacked bar chart  
**Position:** x=606, y=502, w=594, h=178

- Y-axis: `jewelry_sales[metal]`
- Legend: `jewelry_sales[gem]`
- X-axis: `[Gross Sales]`
- Visual-level filter: Top 8 gems by Gross Sales

Title: `Revenue Mix by Metal & Gemstone`

## Slicers

Use compact dropdown slicers aligned in the upper-right/header area or in a collapsible filter pane:
- Date
- Category
- Metal
- Gem
- Price Band

**Sync these slicers across Pages 1–3.**

---

# Page 2 — Product & Merchandising

**Purpose:** Demonstrate retail, assortment, pricing and product-performance analysis.

## KPI row

Four cards:
- `[Products]`
- `[Average Item Price]`
- `[Units]`
- `[Items per Order]`

## Visual 1 — Top Products by Revenue

**Type:** Horizontal bar chart  
**Position:** x=32, y=190, w=600, h=310

- Y-axis: `jewelry_sales[product_id]`
- X-axis: `[Gross Sales]`
- Filter: Top N = 15 by `[Gross Sales]`
- Tooltip: category, metal, gem, `[Orders]`, `[Units]`, `[Average Item Price]`

Title: `Top 15 Products by Revenue`

## Visual 2 — Category Revenue vs Average Selling Price

**Type:** Scatter chart  
**Position:** x=656, y=190, w=544, h=310

- X-axis: `[Average Item Price]`
- Y-axis: `[Gross Sales]`
- Details: `jewelry_sales[category_name]`
- Size: `[Units]`
- Tooltip: `[Orders]`, `[Customers]`, `[Category Revenue Share]`

Title: `Category Value Map`

This visual should make earrings and rings visibly dominant while showing price-positioning differences.

## Visual 3 — Gemstone x Category Matrix

**Type:** Matrix  
**Position:** x=32, y=524, w=750, h=164

- Rows: `jewelry_sales[category_name]`
- Columns: `jewelry_sales[gem]`
- Values: `[Gross Sales]`
- Conditional formatting: background color scale
- Limit columns to the highest-revenue gems plus Unknown.

Title: `Category × Gemstone Revenue Matrix`

## Visual 4 — Taxonomy Completeness

**Type:** KPI / stacked bar  
**Position:** x=806, y=524, w=394, h=164

Show:
- `[Missing Category Rate]`
- `[Missing Gem Rate]`
- `[Missing Metal Rate]`

Title: `Product Attribute Completeness`

## Drill-through page behavior

Create a drill-through target called **Product Detail** using `product_id`.

Show:
- Product ID
- Category
- Metal
- Gem
- Revenue
- Orders
- Units
- Average Item Price
- Monthly sales trend

---

# Page 3 — Customer & Retention

**Purpose:** Make customer concentration, repeat behavior and RFM opportunity obvious.

Load the full generated customer table:

`outputs/generated/customer_rfm.csv`

Rename it to `CustomerRFM` and relate:

`CustomerRFM[user_id]` **1 → *** `jewelry_sales[user_id]`

Cross-filter direction: single.

## KPI row

Five cards:
- `[Customers]`
- `[Repeat Customers]`
- `[Repeat Customer Rate]`
- `[Average Customer Value]`
- `[At Risk Revenue]`

## Visual 1 — Customer Share vs Revenue Share by RFM Segment

**Type:** Clustered bar chart  
**Position:** x=32, y=202, w=640, h=284

- Y-axis: `CustomerRFM[segment]`
- Values: `[RFM Customer Share]`, `[RFM Revenue Share]`
- Sort by RFM Revenue Share descending

Title: `RFM Segments: Customer Share vs Revenue Share`

The key portfolio story should be immediately visible: Champions are a small share of customers but contribute a disproportionate share of revenue.

## Visual 2 — Customer Value vs Recency

**Type:** Scatter chart  
**Position:** x=696, y=202, w=504, h=284

- X-axis: `CustomerRFM[recency_days]`
- Y-axis: `CustomerRFM[monetary]`
- Size: `CustomerRFM[frequency]`
- Legend: `CustomerRFM[segment]`
- Use logarithmic Y-axis only if readability materially improves.

Title: `Customer Value & Recency`

## Visual 3 — Top Customers

**Type:** Table  
**Position:** x=32, y=510, w=720, h=178

Columns:
- user_id
- segment
- monetary
- frequency
- recency_days
- customer_aov

Sort by monetary descending. Show top 15.

Title: `Highest-Value Customers`

## Visual 4 — Retention Opportunity

**Type:** Two cards plus narrative  
**Position:** x=776, y=510, w=424, h=178

Cards:
- At Risk customer count
- At Risk revenue

Narrative text:
`At Risk customers represent a relatively small customer group but a material share of historical revenue, making reactivation a high-priority retention opportunity.`

---

# Page 4 — Data Quality & Audit

**Purpose:** Show analytical rigor and explain why the cleaning pipeline matters.

Do **not** sync normal business slicers to this page unless useful.

## KPI cards

- Source Rows: 95,911
- Structurally Repaired Rows: 5,352
- Missing Category Rate
- Missing Gem Rate
- Exact Duplicate Group Rows

## Visual 1 — Missingness by Attribute

**Type:** Horizontal bar chart

Attributes:
- Gender
- Gem
- Category Code
- Brand Code
- Color
- Metal

Measure: missing-rate percentage.

Title: `Missing Product & Customer Attributes`

## Visual 2 — Category Completeness Over Time

**Type:** Line chart

- X-axis: `DimDate[Year Month]`
- Y-axis: `[Missing Category Rate]`

Title: `Missing Category Rate Over Time`

## Visual 3 — Structural Repair Callout

Use a large text/card callout:

`5,352 source rows contained 11 fields instead of the expected 13. The Python ingestion pipeline reconstructs the two missing positions before parsing, preventing price and customer identifiers from shifting into incorrect columns.`

## Visual 4 — Duplicate Audit

Show:
- Rows belonging to exact duplicate groups
- Excess duplicate rows beyond first occurrence
- Represented revenue associated with duplicate-group rows if calculated

Add the note:
`Duplicates are flagged rather than automatically removed because identical purchase lines may represent legitimate repeated units.`

---

# Interaction rules

1. Category, Metal, Gem, Price Band and Date slicers should filter all relevant visuals on Pages 1–3.
2. Selecting a category on Page 1 should cross-filter price-band and product-mix visuals.
3. RFM segment selection should filter the customer scatter and top-customer table.
4. Disable interactions where a selection creates misleading denominator changes in share KPIs.
5. Use report-page tooltips for category and customer segment details when possible.

# Accessibility and portfolio polish

- Maintain at least 4.5:1 contrast for body text.
- Never encode meaning with color alone.
- Add alt text to each visual.
- Keep visual titles business-oriented rather than technical.
- Use `$33.18M`, not long unformatted dollar values, on cards.
- Use one or two decimal places only where decision-useful.
- Add a small footer: `Portfolio project | Source: REES46 jewelry purchase-history dataset`.

# Final screenshot set for GitHub

After the `.pbix` is built, export or capture these four pages at high resolution:

1. `powerbi/screenshots/01_executive_overview.png`
2. `powerbi/screenshots/02_merchandising.png`
3. `powerbi/screenshots/03_customer_retention.png`
4. `powerbi/screenshots/04_data_quality.png`

The first screenshot should be embedded near the top of the repository README because it will have the highest recruiting value.
