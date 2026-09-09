-- Optional SQL views for a Power BI semantic model

CREATE OR ALTER VIEW dbo.vw_powerbi_sales
AS
SELECT
    event_time,
    order_id,
    product_id,
    quantity,
    category_id,
    category_code,
    category_name,
    brand_code,
    price,
    price_band,
    user_id,
    gender,
    color,
    metal,
    gem,
    line_revenue,
    order_date,
    year_month,
    is_exact_duplicate
FROM dbo.jewelry_sales;
GO

CREATE OR ALTER VIEW dbo.vw_customer_lifetime
AS
SELECT
    user_id,
    COUNT(DISTINCT order_id) AS orders,
    SUM(quantity) AS units,
    SUM(line_revenue) AS lifetime_value,
    MIN(event_time) AS first_purchase,
    MAX(event_time) AS last_purchase,
    SUM(line_revenue) / NULLIF(COUNT(DISTINCT order_id), 0) AS customer_aov
FROM dbo.jewelry_sales
GROUP BY user_id;
GO

CREATE OR ALTER VIEW dbo.vw_product_performance
AS
SELECT
    product_id,
    MAX(category_name) AS category_name,
    MAX(metal) AS metal,
    MAX(gem) AS gem,
    SUM(quantity) AS units,
    COUNT(DISTINCT order_id) AS orders,
    SUM(line_revenue) AS revenue,
    AVG(price) AS avg_item_price
FROM dbo.jewelry_sales
GROUP BY product_id;
GO
