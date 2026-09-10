# Power BI Final QA Record

This checklist records the completed validation status of the Jewelry Retail Analytics portfolio report.

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

## RFM validation

- [x] Champions = **2,362 customers / 45.03% of revenue**
- [x] At Risk = **1,995 customers / 15.24% of revenue**
- [x] Recent Customers = **10,997 customers / 12.89% of revenue**
- [x] Potential Loyalists = **7,399 customers / 10.92% of revenue**
- [x] Loyal Customers = **878 customers / 8.57% of revenue**
- [x] Hibernating = **9,766 customers / 7.35% of revenue**
- [x] RFM documented as a fixed full-history snapshot

## Final Power BI report

Validated Desktop artifact: `Maryam_Jewelry_Portfolio_FINAL7.pbix`

- [x] 4 report pages
- [x] 1280 × 720 report canvas
- [x] Executive Overview
- [x] Product & Merchandising
- [x] Customer & Retention
- [x] Data Quality & Audit
- [x] Consistent charcoal / gold / warm-white design system
- [x] Business-oriented titles and narrative callouts
- [x] No pie/donut charts
- [x] No 3D charts
- [x] No decorative jewelry photography
- [x] Partial-period context included for December 2021
- [x] Data-quality limitations presented explicitly
- [x] Product and customer identifiers abbreviated only in presentation snapshots, not in source data

## Page-level review

### Executive Overview

- [x] Gross Sales displayed
- [x] Orders displayed
- [x] Customers displayed
- [x] Average Order Value displayed
- [x] Repeat Customer Rate displayed
- [x] Monthly sales trend displayed
- [x] Category revenue ranking displayed
- [x] RFM revenue concentration displayed
- [x] Executive business readout included

### Product & Merchandising

- [x] Category slicer included
- [x] Metal slicer included
- [x] Gemstone slicer included
- [x] Price Band slicer included
- [x] Portfolio benchmark KPIs included
- [x] Top SKU revenue leaders included
- [x] Revenue by gemstone included
- [x] Average selling price by category included
- [x] Merchandising readout included

### Customer & Retention

- [x] RFM customer count included
- [x] Repeat customer count included
- [x] Average customer value included
- [x] At Risk revenue included
- [x] Champions revenue included
- [x] Revenue by segment included
- [x] Average customer lifetime value by segment included
- [x] Highest-value customer snapshot included
- [x] Retention-priority narrative included

### Data Quality & Audit

- [x] Source row count included
- [x] Structurally repaired row count included
- [x] Missing category rate included
- [x] Missing gemstone rate included
- [x] Duplicate-group rate included
- [x] Taxonomy exposure visual included
- [x] Duplicate exposure visual included
- [x] Attribute completeness summary included
- [x] Audit-control narrative included

## GitHub portfolio packaging

- [x] Main README updated to final project status
- [x] Full validated Power BI input tables committed
- [x] Analytical findings documented
- [x] Methodology documented
- [x] Data dictionary documented
- [x] SQL analytical layer documented
- [x] Power BI implementation documentation aligned with final report
- [x] Final dashboard screenshot paths standardized
- [x] README embeds Executive Overview near the top

## Optional future extensions

These are not required for the current portfolio release:

- Publish to Power BI Service and add a public/demo link if appropriate
- Add report-page tooltips
- Add accessibility alt text if the report is published for broader consumption
- Add inventory, cost, returns, or promotion data if a richer source becomes available
- Add cohort retention or CLV forecasting with a dataset that supports those analyses reliably

## Resume-ready project statement

> Built an end-to-end jewelry retail analytics solution using Python, SQL Server, and Power BI, analyzing 95K+ transaction lines, 74K+ orders, 33K+ customers, and $33M+ in sales; developed executive, merchandising, retention, RFM, and data-quality reporting with structural data repair and cross-output reconciliation.
