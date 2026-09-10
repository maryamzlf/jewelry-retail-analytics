# Power BI Final QA Record

This checklist records the completed validation status of the Jewelry Retail Analytics portfolio release.

## Data pipeline

- [x] Raw CSV ingestion logic implemented
- [x] 11-field structural repair implemented before parsing
- [x] Required-field and numeric validation implemented
- [x] Exact duplicate groups flagged non-destructively
- [x] Full cleaned fact table generated
- [x] Full customer RFM table generated
- [x] Curated analytical outputs generated
- [x] Cross-output revenue reconciliation implemented
- [x] GitHub Actions full-data sync completed successfully

## Portfolio data validation

- [x] Transaction lines = **95,911**
- [x] Orders = **74,760**
- [x] Customers = **33,397**
- [x] Products = **9,613**
- [x] Gross Sales = **$33,179,324.75**
- [x] Average Order Value = **$443.81**
- [x] Repeat Customers = **8,976**
- [x] Repeat Customer Rate = **26.88%**
- [x] Customer RFM revenue reconciles to fact-table gross sales
- [x] `line_revenue = quantity × price` for all transaction rows
- [x] No nonpositive quantities, negative prices, or missing required IDs

## RFM validation

- [x] Champions = **2,362 customers / 45.03% of revenue**
- [x] At Risk = **1,995 customers / 15.24% of revenue**
- [x] Recent Customers = **10,997 customers / 12.89% of revenue**
- [x] Potential Loyalists = **7,399 customers / 10.92% of revenue**
- [x] Loyal Customers = **878 customers / 8.57% of revenue**
- [x] Hibernating = **9,766 customers / 7.35% of revenue**
- [x] RFM documented as a fixed full-history snapshot
- [x] SQL RFM scoring aligned with Python tie-to-even `np.rint()` behavior

## Final Power BI report

Validated Desktop artifact: `Maryam_Jewelry_Portfolio_FINAL.pbix`

- [x] PBIX archive integrity check passed
- [x] Embedded DataModel preserved from the validated working file
- [x] 4 report pages
- [x] 1280 × 720 report canvas
- [x] Opens on **Executive Overview** by default
- [x] Executive Overview
- [x] Product & Merchandising
- [x] Customer & Retention
- [x] Data Quality & Audit
- [x] Consistent charcoal / gold / warm-white design system
- [x] Business-oriented titles and narrative callouts
- [x] No pie/donut charts, 3D charts, gauges, or decorative jewelry photography
- [x] Partial-period context included for December 2021
- [x] Data-quality limitations presented explicitly
- [x] Product and customer identifiers abbreviated only in presentation snapshots, not in source data

## Page-level review

### Executive Overview

- [x] Gross Sales, Orders, Customers, Average Order Value, Repeat Customer Rate
- [x] Monthly Gross Sales trend
- [x] Category revenue ranking
- [x] RFM revenue concentration
- [x] Executive business readout

### Product & Merchandising

- [x] Category, Metal, Gemstone, and Price Band slicers
- [x] Portfolio benchmark KPIs
- [x] Top SKU revenue leaders
- [x] Revenue by gemstone
- [x] Average selling price by category
- [x] Merchandising readout

### Customer & Retention

- [x] RFM Customers, Repeat Customers, Average Customer Value
- [x] At Risk and Champions revenue
- [x] Revenue by segment
- [x] Average customer lifetime value by segment
- [x] Highest-value customer snapshot
- [x] Retention-priority narrative

### Data Quality & Audit

- [x] Source row and structural-repair counts
- [x] Missing category and gemstone rates
- [x] Duplicate-group rate
- [x] Taxonomy exposure visual
- [x] Duplicate exposure visual
- [x] Attribute completeness summary
- [x] Audit-control narrative

## GitHub portfolio packaging

- [x] Main README reflects final project status
- [x] Full validated Power BI input tables committed
- [x] Analytical findings, methodology, and data dictionary documented
- [x] SQL analytical layer documented and aligned with Python logic
- [x] Power BI implementation documentation aligned with final report
- [x] Lightweight dashboard previews committed under `powerbi/screenshots/`
- [x] README embeds Executive Overview near the top
- [x] PBIX and Power BI cache/local state excluded from Git
- [x] No unfinished TODO/checklist items remain in the release documentation

## Optional future extensions

These are enhancements, not release blockers:

- Publish to Power BI Service and add a demo link if appropriate
- Add report-page tooltips and accessibility alt text for a published version
- Add inventory, cost, returns, promotions, traffic, or conversion data if a richer source becomes available
- Add cohort retention or CLV forecasting with a source that reliably supports those analyses

## Resume-ready project statement

> Built an end-to-end jewelry retail analytics solution using Python, SQL Server, and Power BI, analyzing 95K+ transaction lines, 74K+ orders, 33K+ customers, and $33M+ in sales; developed executive, merchandising, retention, RFM, and data-quality reporting with structural data repair and cross-output reconciliation.
