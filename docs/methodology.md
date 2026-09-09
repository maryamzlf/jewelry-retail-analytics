# Methodology

## 1. Scope

This is a purchase-history analysis, not a web-behavior funnel analysis. The dataset contains completed purchase lines, so the project focuses on sales, product mix, customer value, retention, and merchandising rather than views, carts, or conversion rate.

## 2. Ingestion and structural normalization

The uploaded snapshot does not include the original header row and contains two row widths:

- 90,559 standard 13-field records
- 5,352 irregular 11-field records

The 11-field rows omit `category_code` and `brand`. They are repaired at the CSV-line level before the DataFrame is constructed. This prevents silent column shifting, which would otherwise corrupt price and customer identifiers.

## 3. Type and quality controls

The preparation pipeline:

1. parses `event_time` as UTC;
2. preserves large IDs as strings to avoid numeric precision loss;
3. converts quantity, price, and brand code to numeric types;
4. rejects missing required identifiers, invalid dates, non-positive quantities, or negative prices;
5. retains missing product attributes for transparent quality reporting;
6. calculates line revenue, month, friendly category, and price bands;
7. flags exact duplicates without automatically deleting them.

### Why duplicates are flagged, not dropped

An exact repeated purchase line can be a data-quality problem, but it can also represent two identical units recorded as separate unit-level rows. Because the dataset documentation states that rows represent purchased products, removing identical rows without another authoritative key could understate revenue. The project therefore reports both the number of rows involved in duplicate groups and the number of excess duplicates, while preserving source revenue.

## 4. KPI definitions

- **Gross Sales:** sum of `quantity * price`.
- **Orders:** distinct `order_id`.
- **Customers:** distinct `user_id`.
- **Products:** distinct `product_id`.
- **Average Order Value (AOV):** Gross Sales / Orders.
- **Repeat Customer:** customer with more than one distinct order in the snapshot.
- **Repeat Customer Rate:** Repeat Customers / Customers.
- **Average Items per Order:** sum of quantity / distinct orders.

## 5. RFM segmentation

RFM is calculated at customer level using:

- **Recency:** days between the customer's last purchase and one day after the dataset's maximum timestamp.
- **Frequency:** distinct order count.
- **Monetary:** total customer revenue.

Recency and monetary are scored by quintile. Frequency is intentionally **not** quintile-binned because 73% of customers have exactly one order, which would create arbitrary tie-breaking. Instead, frequency uses transparent business-rule bins: 1 order = score 1; 2 = 2; 3–4 = 3; 5–9 = 4; 10+ = 5. Frequency and monetary are averaged into an `FM` score and combined with recency into six interpretable segments: Champions, Loyal Customers, Recent Customers, Potential Loyalists, At Risk, and Hibernating.

## 6. Reconciliation

`python/03_validate_outputs.py` reconciles gross sales across the cleaned dataset, category, metal, gem, price-band, and RFM summaries. This prevents a portfolio dashboard from presenting internally inconsistent totals.

## 7. Limitations

- The uploaded snapshot has 95,911 purchase lines, while the public source page describes a larger overall dataset; findings apply to this snapshot.
- 2018 and December 2021 are partial periods in this snapshot and should not be treated as full-year/full-month comparisons.
- There are no cost, margin, inventory, promotion, traffic, or return fields; revenue is not profit.
- Missing category, gemstone, gender, color, and metal values constrain some segmentation analyses.
- Customer IDs are anonymous, so recommendations are analytical rather than directly executable CRM campaigns.
