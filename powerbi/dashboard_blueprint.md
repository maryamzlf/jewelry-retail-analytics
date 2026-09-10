# Implemented Power BI Dashboard Specification

This document describes the **final implemented four-page report**. It is an as-built specification, not a future build plan.

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

The visual direction is intentionally closer to an executive retail-analytics product than a consumer-facing jewelry presentation.

---

## Page 1 — Executive Overview

**Visible header:** `Jewelry Retail Performance`

**Purpose:** communicate the commercial story in under 30 seconds.

### Snapshot KPIs

- Gross Sales — **$33.18M**
- Orders — **74,760**
- Customers — **33,397**
- Average Order Value — **$443.81**
- Repeat Customer Rate — **26.9%**

### Visuals

- **Monthly Gross Sales** — revenue momentum across the observed period. December 2021 is a partial month and is not interpreted as a complete-period decline.
- **Revenue by Category** — horizontal category ranking with `Unknown` retained to expose taxonomy limitations.
- **Revenue by RFM Segment** — historical revenue concentration by full-history customer segment.
- **Executive Readout** — highlights Earrings + Rings at **65.9% of revenue**, $250+ items at **80.4% of revenue**, and the retention / premium-assortment implications.

---

## Page 2 — Product & Merchandising

**Visible header:** `Merchandising & Assortment`

**Purpose:** demonstrate assortment, pricing, gemstone, and SKU-level analysis.

### Exploration slicers

- Category
- Metal
- Gemstone
- Price Band

The slicers support exploratory visual analysis. The KPI tiles are intentionally full-portfolio benchmark values.

### Snapshot KPIs

- Portfolio Revenue — **$33.18M**
- Average Item Price — **$345.94**
- Products — **9,613**
- Premium Revenue Share — **80.4%**

### Visuals

- **Top SKU Revenue Leaders** — compact top-five snapshot; long product IDs are abbreviated only in the presentation layer.
- **Revenue by Gemstone** — horizontal revenue ranking.
- **Average Selling Price by Category** — category price-positioning comparison.
- **Merchandising Readout** — premium mix, Earrings/Rings concentration, gold dominance, and uncategorized-revenue caveat.

---

## Page 3 — Customer & Retention

**Visible header:** `Customer Value & Retention`

**Purpose:** translate full-history customer value and RFM segmentation into retention priorities.

### Snapshot KPIs

- RFM Customers — **33,397**
- Repeat Customers — **8,976**
- Average Customer Value — **$993.48**
- At Risk Revenue — **$5.06M**
- Champions Revenue — **$14.94M**

### Visuals

- **Revenue by RFM Segment** — historical revenue concentration by segment.
- **Average Customer Lifetime Value by Segment** — segment-level value comparison.
- **Highest-Value Customers** — compact top-five customer snapshot; IDs are abbreviated only for visual readability.
- **Retention Priorities** — Champions are **7.1% of customers / 45.0% of revenue**; At Risk are **6.0% / 15.2%**. Recommended actions focus on protecting Champions, reactivating At Risk customers, and improving second-purchase conversion for Recent Customers.

### RFM interpretation rule

RFM is a **fixed full-history snapshot** relative to the end of the observed dataset. The report does not imply that historical date filtering recalculates customer segments.

---

## Page 4 — Data Quality & Audit

**Visible header:** `Data Quality & Audit`

**Purpose:** demonstrate analytical controls and make source limitations visible alongside business results.

### Snapshot KPIs

- Source Rows — **95,911**
- Structurally Repaired — **5,352**
- Missing Category — **15.9%**
- Missing Gemstone — **35.5%**
- Rows in Exact-Duplicate Groups — **5.1%**

### Visuals

- **Revenue by Category — Taxonomy Exposure** — shows the commercial impact of uncategorized products.
- **Duplicate Flag — Units Represented** — compares rows inside and outside exact-duplicate groups without deleting source records.
- **Attribute Completeness** — Gender **50.2%**, Gemstone **35.5%**, Category Code **15.9%**, Brand Code **10.6%**, Color **8.0%**, Metal **5.7%** missing.
- **Audit Control Notes** — explains 11-field structural repair, non-destructive duplicate policy, and cross-output revenue reconciliation.

---

## Interaction and interpretation rules

1. Merchandising slicers are used for exploratory chart analysis.
2. Snapshot benchmark tiles remain full-portfolio reference values.
3. RFM segmentation is not presented as dynamically recomputed by historical date selections.
4. `Unknown` product attributes remain visible when analytically material.
5. Exact duplicate groups are flagged rather than automatically removed.
6. 2018 and December 2021 are treated as partial periods.
7. Revenue is never described as profit because cost and margin data are unavailable.
8. Long product/customer identifiers are preserved in source data and abbreviated only in presentation snapshots.

## Portfolio preview set

GitHub stores lightweight vector previews of the implemented pages:

```text
powerbi/screenshots/01_executive_overview.svg
powerbi/screenshots/02_merchandising.svg
powerbi/screenshots/03_customer_retention.svg
powerbi/screenshots/04_data_quality.svg
```

The Executive Overview preview is embedded near the top of the repository README. The authoritative interactive artifact is `Maryam_Jewelry_Portfolio_FINAL.pbix`, distributed outside version control.
