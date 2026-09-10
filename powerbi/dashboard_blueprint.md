# Implemented Power BI Dashboard Specification

This document describes the **final implemented four-page report**, not a future build plan.

## Visual system

- Canvas: **1280 × 720**
- Background: warm off-white
- Header: deep charcoal
- Commercial accent: muted gold
- Secondary series: slate / sage
- Risk and data-quality exceptions: muted red
- Typography: Segoe UI
- Cards: white, rounded, light borders
- Design rule: no jewelry photography, gradients, 3D charts, gauges, or pie charts

The visual direction is intentionally closer to an executive retail analytics product than a consumer-facing jewelry presentation.

---

# Page 1 — Executive Overview

**Visible header:** `Jewelry Retail Performance`

**Purpose:** communicate the entire commercial story in under 30 seconds.

## Snapshot KPIs

- Gross Sales — **$33.18M**
- Orders — **74,760**
- Customers — **33,397**
- Average Order Value — **$443.81**
- Repeat Customer Rate — **26.9%**

## Visuals

### Monthly Gross Sales

Line chart showing revenue momentum across the observed period.

Interpretation rule: December 2021 is a partial month and should not be compared with complete months.

### Revenue by Category

Horizontal ranking of category revenue. Earrings and rings dominate the known category mix; `Unknown` remains visible to preserve taxonomy-quality context.

### Revenue by RFM Segment

Horizontal ranking of historical customer revenue by full-history RFM segment.

### Executive Readout

Business narrative highlighting:
- Earrings + Rings = **65.9% of revenue**
- $250+ items = **80.4% of revenue**
- growth is primarily volume-led rather than driven by a rising basket value
- retention and premium-category depth are the principal opportunities

---

# Page 2 — Product & Merchandising

**Visible header:** `Merchandising & Assortment`

**Purpose:** demonstrate retail assortment, pricing, gemstone, and SKU-level analysis.

## Exploration slicers

- Category
- Metal
- Gemstone
- Price Band

These slicers support exploratory chart analysis. The KPI tiles on this page are intentionally **full-portfolio benchmark values** rather than restated filter-context KPIs.

## Snapshot KPIs

- Portfolio Revenue — **$33.18M**
- Average Item Price — **$345.94**
- Products — **9,613**
- Premium Revenue Share — **80.4%**

## Visuals

### Top SKU Revenue Leaders

Compact ranked snapshot of the highest-revenue products. Product IDs are abbreviated in the presentation layer for readability while the underlying model retains the full identifier.

### Revenue by Gemstone

Horizontal bar chart highlighting gemstone revenue concentration.

### Average Selling Price by Category

Column chart comparing category price positioning.

### Merchandising Readout

Narrative interpretation covering premium pricing, category concentration, gold dominance, and the limitation created by uncategorized product revenue.

---

# Page 3 — Customer & Retention

**Visible header:** `Customer Value & Retention`

**Purpose:** translate full-history customer value and RFM segmentation into retention priorities.

## Snapshot KPIs

- RFM Customers — **33,397**
- Repeat Customers — **8,976**
- Average Customer Value — **$993.48**
- At Risk Revenue — **$5.06M**
- Champions Revenue — **$14.94M**

## Visuals

### Revenue by RFM Segment

Historical revenue concentration by segment.

### Average Customer Lifetime Value by Segment

Segment-level comparison of average historical customer value.

### Highest-Value Customers

Compact top-five customer snapshot. Customer IDs are abbreviated only for visual readability.

### Retention Priorities

Narrative highlighting:
- Champions = **7.1% of customers / 45.0% of revenue**
- At Risk = **6.0% of customers / 15.2% of revenue**
- protect Champions, reactivate At Risk customers, and create a structured second-purchase journey for Recent Customers

## RFM interpretation rule

RFM is a **fixed full-history snapshot** relative to the end of the observed dataset. The page intentionally does not imply that historical date filtering recalculates customer segments.

---

# Page 4 — Data Quality & Audit

**Visible header:** `Data Quality & Audit`

**Purpose:** demonstrate data-governance awareness and make source limitations visible alongside business results.

## Snapshot KPIs

- Source Rows — **95,911**
- Structurally Repaired — **5,352**
- Missing Category — **15.9%**
- Missing Gemstone — **35.5%**
- Rows in Exact-Duplicate Groups — **5.1%**

## Visuals

### Revenue by Category — Taxonomy Exposure

Shows that material revenue sits in uncategorized products, making taxonomy quality a business issue rather than a purely technical one.

### Duplicate Flag — Units Represented

Compares rows inside and outside exact-duplicate groups while preserving the source records.

### Attribute Completeness

Snapshot of major missingness rates:
- Gender — **50.2%**
- Gemstone — **35.5%**
- Category code — **15.9%**
- Brand code — **10.6%**
- Color — **8.0%**
- Metal — **5.7%**

### Audit Control Notes

Explains the 11-field structural repair, the non-destructive duplicate policy, and cross-output revenue reconciliation.

---

# Interaction and interpretation rules

1. Merchandising slicers are intended for exploratory chart analysis.
2. Snapshot benchmark tiles remain clearly positioned as full-portfolio reference values.
3. RFM segmentation is not presented as dynamically recomputed by a historical date selection.
4. `Unknown` product attributes remain visible when they are analytically material.
5. Exact duplicate groups are flagged rather than automatically removed.
6. 2018 and December 2021 are interpreted as partial periods.
7. Revenue is never described as profit because cost and margin fields are unavailable.

# Portfolio screenshot set

The final report is represented in GitHub by:

```text
powerbi/screenshots/01_executive_overview.jpg
powerbi/screenshots/02_merchandising.jpg
powerbi/screenshots/03_customer_retention.jpg
powerbi/screenshots/04_data_quality.jpg
```

The Executive Overview is embedded near the top of the repository README for immediate recruiting visibility.
