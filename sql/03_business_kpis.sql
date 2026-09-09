-- Executive KPI and trend analysis

-- 1. Executive KPIs
SELECT
    SUM(line_revenue) AS gross_sales,
    COUNT(DISTINCT order_id) AS total_orders,
    COUNT(DISTINCT user_id) AS customers,
    COUNT(DISTINCT product_id) AS products,
    SUM(quantity) AS units,
    SUM(line_revenue) / NULLIF(COUNT(DISTINCT order_id), 0) AS average_order_value,
    1.0 * SUM(quantity) / NULLIF(COUNT(DISTINCT order_id), 0) AS items_per_order
FROM dbo.jewelry_sales;

-- 2. Monthly sales trend with MoM growth
WITH monthly AS (
    SELECT
        year_month,
        SUM(line_revenue) AS revenue,
        COUNT(DISTINCT order_id) AS orders,
        COUNT(DISTINCT user_id) AS customers,
        SUM(quantity) AS units
    FROM dbo.jewelry_sales
    GROUP BY year_month
),
lagged AS (
    SELECT
        *,
        LAG(revenue) OVER (ORDER BY year_month) AS prior_month_revenue
    FROM monthly
)
SELECT
    year_month,
    revenue,
    orders,
    customers,
    units,
    revenue / NULLIF(orders, 0) AS average_order_value,
    100.0 * (revenue - prior_month_revenue)
        / NULLIF(prior_month_revenue, 0) AS mom_revenue_pct
FROM lagged
ORDER BY year_month;

-- 3. Annual sales trend. Interpret 2018 and 2021 with partial-period context.
WITH annual AS (
    SELECT
        YEAR(order_date) AS sales_year,
        SUM(line_revenue) AS revenue,
        COUNT(DISTINCT order_id) AS orders,
        COUNT(DISTINCT user_id) AS customers
    FROM dbo.jewelry_sales
    GROUP BY YEAR(order_date)
),
lagged AS (
    SELECT
        *,
        LAG(revenue) OVER (ORDER BY sales_year) AS prior_year_revenue
    FROM annual
)
SELECT
    sales_year,
    revenue,
    orders,
    customers,
    revenue / NULLIF(orders, 0) AS average_order_value,
    100.0 * (revenue - prior_year_revenue)
        / NULLIF(prior_year_revenue, 0) AS yoy_revenue_pct
FROM lagged
ORDER BY sales_year;
