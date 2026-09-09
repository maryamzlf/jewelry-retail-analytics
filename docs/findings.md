# Analytical Findings

These findings are calculated from the uploaded `jewelry.csv` snapshot after structural normalization. They describe the snapshot, not necessarily every record in the larger public source dataset.

## Executive snapshot

| KPI | Result |
|---|---:|
| Transaction lines | 95,911 |
| Orders | 74,760 |
| Customers | 33,397 |
| Products | 9,613 |
| Gross sales represented | $33,179,324.75 |
| Average order value | $443.81 |
| Average item price | $345.94 |
| Average items per order | 1.28 |
| Multi-line order rate | 19.70% |
| Repeat customers | 8,976 |
| Repeat customer rate | 26.88% |

## 1. Revenue accelerated materially over the observed period

| Year | Revenue | Orders | AOV | YoY revenue growth |
|---|---:|---:|---:|---:|
| 2018* | $33,935.77 | 104 | $326.31 | — |
| 2019 | $4,312,999.77 | 8,864 | $486.57 | — |
| 2020 | $9,340,612.87 | 20,810 | $448.85 | +116.57% |
| 2021** | $19,491,776.34 | 44,982 | $433.32 | +108.68% |

\* 2018 contains only December activity in this snapshot.  
\** 2021 runs through December 1 and is therefore not a fully completed calendar year.

November 2021 was the highest complete month in the snapshot at approximately **$3.71M** in revenue.

**Interpretation:** growth is being driven primarily by substantially higher order volume, while AOV remains in the low-to-mid $400s rather than increasing at the same rate.

## 2. Earrings and rings dominate category revenue

| Category | Revenue | Revenue share |
|---|---:|---:|
| Earring | $11.51M | 34.70% |
| Ring | $10.36M | 31.24% |
| Unknown | $4.76M | 14.35% |
| Bracelet | $3.06M | 9.21% |
| Pendant | $2.20M | 6.63% |

Earrings and rings together contribute **65.93% of total revenue**.

**Business implication:** category planning, assortment depth, and merchandising attention should prioritize earrings and rings, but the 14.35% of revenue sitting in `Unknown` category materially limits category-level decision quality.

## 3. High-value sales are concentrated in gold and diamond products

- **Gold** represents **98.54% of revenue** in the snapshot.
- **Diamond** products account for **44.81% of revenue**.
- Records with an unknown gemstone still represent **25.24% of revenue**.
- Products priced at **$250 or above generate 80.42% of revenue**.
- The single largest price band is **$250–$499**, contributing **31.01% of revenue**.

**Business implication:** the commercial center of gravity is clearly premium gold jewelry. Product storytelling, inventory depth, and promotional strategy should reflect this, while gemstone-data completeness should be improved before deeper gem-level assortment optimization.

## 4. Retention is the largest customer-growth opportunity

Only **26.88%** of customers placed more than one distinct order; **73.12%** purchased once in the snapshot.

The RFM segmentation makes the concentration of value even clearer:

| RFM segment | Customers | Customer share | Revenue | Revenue share | Avg. orders | Avg. recency |
|---|---:|---:|---:|---:|---:|---:|
| Champions | 2,362 | 7.07% | $14.94M | 45.03% | 11.37 | 55 days |
| At Risk | 1,995 | 5.97% | $5.06M | 15.24% | 5.07 | 460 days |
| Recent Customers | 10,997 | 32.93% | $4.28M | 12.89% | 1.14 | 64 days |
| Potential Loyalists | 7,399 | 22.15% | $3.62M | 10.92% | 1.24 | 270 days |
| Loyal Customers | 878 | 2.63% | $2.84M | 8.57% | 6.18 | 217 days |
| Hibernating | 9,766 | 29.24% | $2.44M | 7.35% | 1.09 | 433 days |

**Business implication:**

1. Protect Champions with loyalty/VIP treatment and early access.
2. Prioritize At Risk customers for reactivation because a small customer group controls **15.24% of historical revenue**.
3. Build a structured second-purchase journey for Recent Customers; they are the largest near-term retention pool.

## 5. Basket expansion is a secondary growth lever

Average items per order are only **1.28**, and just **19.70%** of orders contain more than one purchase line.

**Business implication:** cross-sell opportunities are meaningful—especially complementary earrings, pendants, bracelets, and gemstone/metal pairings—but retention should remain the higher-priority lever because customer value is much more concentrated in repeat behavior.

## 6. Data quality is a business finding, not just a technical issue

| Quality issue | Rows | Share of rows |
|---|---:|---:|
| 11-field rows structurally repaired | 5,352 | 5.58% |
| Missing category code | 15,285 | 15.94% |
| Missing brand code | 10,137 | 10.57% |
| Missing gender | 48,168 | 50.22% |
| Missing gemstone | 34,058 | 35.51% |
| Missing metal | 5,462 | 5.69% |
| Rows involved in exact duplicate groups | 4,887 | 5.10% |
| Excess exact duplicate rows beyond first occurrence | 2,589 | 2.70% |

Six of the top ten products by revenue have an `Unknown` category, reinforcing that taxonomy gaps affect high-value items—not only low-value tail products.

**Recommendation:** before using this data for assortment automation or customer personalization, strengthen product master-data governance and define an authoritative rule for duplicate purchase-line treatment.
