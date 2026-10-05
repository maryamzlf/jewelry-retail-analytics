-- Customer value, repeat behavior, and RFM analysis
-- The RFM logic mirrors python/02_eda_rfm.py so SQL and Python produce
-- the same scoring and business-segment interpretation.

-- 1. Customer lifetime value
WITH customer_value AS (
    SELECT
        user_id,
        COUNT(DISTINCT order_id) AS orders,
        SUM(quantity) AS units,
        SUM(line_revenue) AS lifetime_value,
        MIN(event_time) AS first_purchase,
        MAX(event_time) AS last_purchase
    FROM dbo.jewelry_sales
    GROUP BY user_id
)
SELECT TOP (100)
    *,
    lifetime_value / NULLIF(orders, 0) AS customer_aov
FROM customer_value
ORDER BY lifetime_value DESC, orders DESC;

-- 2. Repeat customer rate
WITH customer_orders AS (
    SELECT
        user_id,
        COUNT(DISTINCT order_id) AS orders
    FROM dbo.jewelry_sales
    GROUP BY user_id
)
SELECT
    COUNT(*) AS customers,
    SUM(CASE WHEN orders > 1 THEN 1 ELSE 0 END) AS repeat_customers,
    100.0 * SUM(CASE WHEN orders > 1 THEN 1 ELSE 0 END) / COUNT(*) AS repeat_customer_pct
FROM customer_orders;

-- 3. Basket-size distribution
WITH baskets AS (
    SELECT
        order_id,
        SUM(quantity) AS items,
        COUNT(*) AS lines,
        SUM(line_revenue) AS order_value
    FROM dbo.jewelry_sales
    GROUP BY order_id
)
SELECT
    items,
    COUNT(*) AS orders,
    AVG(order_value) AS avg_order_value
FROM baskets
GROUP BY items
ORDER BY items;

-- 4. RFM scoring aligned exactly with python/02_eda_rfm.py
-- Python uses elapsed whole days, pandas rank(method='first') followed by
-- qcut(..., 5), rule-based frequency bins, and NumPy tie-to-even rounding.
WITH anchor AS (
    SELECT DATEADD(day, 1, CAST(MAX(event_time) AS datetime2)) AS analysis_date
    FROM dbo.jewelry_sales
),
customer_rfm AS (
    SELECT
        s.user_id,
        CAST(
            FLOOR(
                DATEDIFF_BIG(
                    second,
                    MAX(CAST(s.event_time AS datetime2)),
                    a.analysis_date
                ) / 86400.0
            ) AS int
        ) AS recency_days,
        COUNT(DISTINCT s.order_id) AS frequency,
        SUM(s.line_revenue) AS monetary
    FROM dbo.jewelry_sales s
    CROSS JOIN anchor a
    GROUP BY s.user_id, a.analysis_date
),
ranked AS (
    SELECT
        *,
        ROW_NUMBER() OVER (ORDER BY recency_days ASC, user_id ASC) AS recency_rank,
        ROW_NUMBER() OVER (ORDER BY monetary ASC, user_id ASC) AS monetary_rank,
        COUNT(*) OVER () AS customer_count
    FROM customer_rfm
),
scored AS (
    SELECT
        *,
        CASE
            WHEN customer_count <= 1 THEN 5
            WHEN 1.0 * (recency_rank - 1) / (customer_count - 1) <= 0.20 THEN 5
            WHEN 1.0 * (recency_rank - 1) / (customer_count - 1) <= 0.40 THEN 4
            WHEN 1.0 * (recency_rank - 1) / (customer_count - 1) <= 0.60 THEN 3
            WHEN 1.0 * (recency_rank - 1) / (customer_count - 1) <= 0.80 THEN 2
            ELSE 1
        END AS r_score,
        CASE
            WHEN frequency = 1 THEN 1
            WHEN frequency = 2 THEN 2
            WHEN frequency BETWEEN 3 AND 4 THEN 3
            WHEN frequency BETWEEN 5 AND 9 THEN 4
            ELSE 5
        END AS f_score,
        CASE
            WHEN customer_count <= 1 THEN 5
            WHEN 1.0 * (monetary_rank - 1) / (customer_count - 1) <= 0.20 THEN 1
            WHEN 1.0 * (monetary_rank - 1) / (customer_count - 1) <= 0.40 THEN 2
            WHEN 1.0 * (monetary_rank - 1) / (customer_count - 1) <= 0.60 THEN 3
            WHEN 1.0 * (monetary_rank - 1) / (customer_count - 1) <= 0.80 THEN 4
            ELSE 5
        END AS m_score
    FROM ranked
),
segmented AS (
    SELECT
        *,
        -- Match NumPy np.rint(): .5 ties round to the nearest even integer.
        CAST(
            CASE
                WHEN (f_score + m_score) % 2 = 0
                    THEN (f_score + m_score) / 2
                WHEN ((f_score + m_score) / 2) % 2 = 0
                    THEN (f_score + m_score) / 2
                ELSE (f_score + m_score) / 2 + 1
            END AS int
        ) AS fm_score
    FROM scored
)
SELECT
    *,
    CASE
        WHEN r_score >= 4 AND fm_score >= 4 THEN 'Champions'
        WHEN r_score >= 3 AND fm_score >= 4 THEN 'Loyal Customers'
        WHEN r_score >= 4 AND fm_score <= 3 THEN 'Recent Customers'
        WHEN r_score <= 2 AND fm_score >= 4 THEN 'At Risk'
        WHEN r_score <= 2 AND fm_score <= 2 THEN 'Hibernating'
        ELSE 'Potential Loyalists'
    END AS segment
FROM segmented
ORDER BY monetary DESC;
