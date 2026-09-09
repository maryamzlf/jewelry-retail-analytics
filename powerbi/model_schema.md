# Power BI Model Schema

## Recommended semantic model

Use a compact star-style model with two analytical areas: transaction analysis and snapshot customer segmentation.

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

## Table 1 — `jewelry_sales`

**Grain:** one purchased product line.

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
- `metal`
- `gem`
- `color`
- `price_band`
- `is_exact_duplicate`

Treat all 19-digit identifiers as **Text** in Power BI.

## Table 2 — `DimDate`

Created with DAX from the minimum and maximum `order_date`.

Relationship:

`DimDate[Date]` **1 → *** `jewelry_sales[order_date]`

Settings:

- Active relationship: Yes
- Cross-filter direction: Single
- Mark as Date Table: Yes

Recommended fields:

- Date
- Year
- Quarter
- Month
- Month Number
- Year Month
- Year Month Sort

## Table 3 — `CustomerRFM`

Source:

`outputs/generated/customer_rfm.csv`

**Grain:** one row per customer.

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

Settings:

- Active relationship: Yes
- Cross-filter direction: Single, from CustomerRFM to jewelry_sales

## Why the RFM relationship is single-direction

`CustomerRFM` is a snapshot calculated using the customer's full history through the final dataset date. It should filter transactions when a segment is selected, but normal transaction filters should not silently change the precomputed RFM classification.

For that reason:

- An RFM segment slicer **may filter** jewelry transaction visuals.
- A date/category/product slicer on the fact table should **not be presented as recalculating RFM**.
- Keep Page 3 labeled `Snapshot RFM Segmentation`.

## Optional `DataQualitySummary`

You may import `outputs/data_quality_summary.csv` as a disconnected table for fixed source-quality callouts such as the 5,352 structurally repaired rows.

Do not create a relationship between `DataQualitySummary` and the fact table; its metrics describe the full source snapshot.

## Optional product dimension

For a larger production model, a dedicated `DimProduct` would be appropriate. For this portfolio snapshot, product attributes are incomplete and can vary in missingness, so using the fact table directly avoids implying a cleaner authoritative product master than the source actually provides.

## Model QA

Before building visuals confirm:

1. `CustomerRFM[user_id]` is unique.
2. `DimDate[Date]` is unique.
3. `jewelry_sales[order_id]`, `product_id`, `user_id`, and `category_id` are Text.
4. All relationships are active and single-direction.
5. No many-to-many relationship exists.
6. Gross Sales with no filters = **$33,179,324.75**.
7. Customers with no filters = **33,397**.
8. `RFM Customers` with no filters = **33,397**.
