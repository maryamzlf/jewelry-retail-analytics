# Power BI Semantic Model

This document describes the **reference semantic model** used for the final Jewelry Retail Analytics report.

The final Desktop artifact preserves the working import lineage created during development. For documentation readability, the tables are referred to by business-friendly aliases:

- `jewelry_sales` — transaction fact table
- `CustomerRFM` — full-history customer snapshot
- `DimDate` — calendar dimension

## Model shape

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

## `jewelry_sales`

**Grain:** one purchased product line.

Validated source: `data/jewelry_clean.csv`

Primary analytical fields:

- `event_time`
- `order_date`
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

All 19-digit identifiers must be treated as **Text** in Power BI to avoid precision loss.

## `DimDate`

A standard date dimension can be created from the minimum and maximum `order_date`.

Relationship:

`DimDate[Date]` **1 → *** `jewelry_sales[order_date]`

Recommended attributes:

- Date
- Year
- Quarter
- Month
- Month Number
- Year Month
- Year Month Sort

`DimDate[Year Month]` should be sorted by `DimDate[Year Month Sort]`.

## `CustomerRFM`

**Grain:** one row per customer.

Validated source: `data/customer_rfm.csv`

Fields:

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

Relationship:

`CustomerRFM[user_id]` **1 → *** `jewelry_sales[user_id]`

Cross-filter direction: **Single, from CustomerRFM to the transaction fact table.**

## Why RFM is modeled as a snapshot

The RFM table is calculated from each customer's complete observed purchase history relative to the dataset end date. It is therefore a **snapshot classification**, not a historical segment that is recomputed for every report date.

Implications:

- Segment selections may filter transaction analysis.
- Historical transaction filters should not be presented as recalculating RFM membership.
- Customer reporting should be labeled and interpreted as a full-history snapshot.

## Data-quality modeling

`outputs/data_quality_summary.csv` can be used as a disconnected source for fixed audit callouts such as the 5,352 structurally repaired rows.

No relationship is required because those metrics describe the complete input snapshot.

## Why there is no asserted authoritative product dimension

A dedicated `DimProduct` would be appropriate in a production environment with a governed product master. In this source, category, gemstone, metal, and other attributes contain material missingness. Keeping those attributes at fact level avoids implying a cleaner product master than the source supports.

## Model validation targets

With full-snapshot filters cleared:

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

1. `CustomerRFM[user_id]` is unique.
2. `DimDate[Date]` is unique.
3. IDs are represented as Text in Power BI.
4. No many-to-many relationship is required.
5. Customer and fact-table revenue reconcile to the same portfolio total.
