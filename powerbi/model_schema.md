# Power BI Semantic Model — As Built

This document describes the **actual stable import model used by the validated final Desktop artifact** `Maryam_Jewelry_Portfolio_FINAL.pbix`.

## Final model shape

The working PBIX preserves two imported tables:

- `jewelry_clean (2)` — transaction-level purchase fact table
- `customer_rfm (2)` — one-row-per-customer full-history RFM snapshot

The final report deliberately keeps the model simple and stable. Transaction, merchandising, and data-quality visuals aggregate directly from `jewelry_clean (2)`. Customer/RFM visuals aggregate directly from `customer_rfm (2)`.

The report does not require a separate date dimension to render the implemented pages. Monthly Gross Sales uses the prepared `year_month` field from the transaction table and sorts it ascending.

## `jewelry_clean (2)`

**Grain:** one purchased product line.

Validated source: `data/jewelry_clean.csv`

Fields used by the final report include:

- `year_month`
- `order_id`
- `product_id`
- `user_id`
- `quantity`
- `price`
- `line_revenue`
- `category_name`
- `category_code`
- `brand_code`
- `metal`
- `gem`
- `gender`
- `color`
- `price_band`
- `is_exact_duplicate`

The underlying CSV preserves complete identifier values. Compact product/customer snapshots abbreviate long IDs only in the presentation text; the source data are not truncated.

For a future rebuild, identifier fields should be treated as categorical/Text fields in Power BI so they are not interpreted as continuous numeric axes.

## `customer_rfm (2)`

**Grain:** one row per customer.

Validated source: `data/customer_rfm.csv`

Fields include:

- `user_id`
- `first_purchase`
- `last_purchase`
- `frequency`
- `transaction_lines`
- `units`
- `monetary`
- `customer_aov`
- `recency_days`
- `r_score`
- `f_score`
- `m_score`
- `fm_score`
- `segment`

RFM is calculated from each customer's complete observed history relative to **one day after the maximum observed transaction timestamp**. It is therefore a snapshot classification, not a historical segment that is recomputed for every report date.

Implications:

- RFM visuals are interpreted as full-history customer segmentation.
- The final RFM page does not imply dynamic historical re-segmentation.
- Revenue by RFM Segment on the Executive page is sourced directly from the RFM snapshot table.

## Data-quality reporting

The final page combines:

- data-bound transaction visuals for category exposure and duplicate-flag units; and
- validated full-snapshot audit callouts from the Python pipeline, including the **5,352** structurally repaired rows and attribute-missingness rates.

This keeps source limitations visible without pretending the dataset has a governed product master.

## Why there is no asserted product dimension

A dedicated product dimension would be appropriate in a production environment with a governed product master. In this source, category, gemstone, metal, gender, color, and brand attributes contain material missingness. Keeping the implemented report close to the validated transaction source avoids implying cleaner master data than the source supports.

## Validation targets

With the full snapshot represented:

| Check | Expected result |
|---|---:|
| Transaction lines | 95,911 |
| Orders | 74,760 |
| Customers | 33,397 |
| Products | 9,613 |
| Gross Sales | $33,179,324.75 |
| RFM Customers | 33,397 |
| RFM Revenue | $33,179,324.75 |

Additional controls:

1. `customer_rfm (2)[user_id]` is unique at customer grain.
2. Transaction revenue reconciles to customer RFM monetary value.
3. The monthly axis is the prepared `year_month` field sorted ascending.
4. Long identifiers are preserved in source data and abbreviated only in compact presentation snapshots.
5. No cross-table dynamic calculation is required for the current four-page report to render correctly.

## Optional extension model

The repository's [`dax_measures.md`](dax_measures.md) contains reusable DAX patterns and an optional `DimDate` design for future extension. Those patterns are **reference material**, not a description of extra tables that must exist in the validated final PBIX.
