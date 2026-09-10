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

-- Product performance with representative attributes selected by modal value,
-- matching the Python portfolio pipeline instead of using MAX() as an arbitrary
-- attribute selector.
CREATE OR ALTER VIEW dbo.vw_product_performance
AS
WITH product_perf AS (
    SELECT
        product_id,
        SUM(quantity) AS units,
        COUNT(DISTINCT order_id) AS orders,
        SUM(line_revenue) AS revenue,
        AVG(price) AS avg_item_price
    FROM dbo.jewelry_sales
    GROUP BY product_id
)
SELECT
    p.product_id,
    cat.category_name,
    met.metal,
    gem_attr.gem,
    p.units,
    p.orders,
    p.revenue,
    p.avg_item_price
FROM product_perf p
OUTER APPLY (
    SELECT TOP (1)
        COALESCE(s.category_name, 'Unknown') AS category_name
    FROM dbo.jewelry_sales s
    WHERE s.product_id = p.product_id
    GROUP BY COALESCE(s.category_name, 'Unknown')
    ORDER BY COUNT(*) DESC, COALESCE(s.category_name, 'Unknown') ASC
) cat
OUTER APPLY (
    SELECT TOP (1)
        COALESCE(s.metal, 'Unknown') AS metal
    FROM dbo.jewelry_sales s
    WHERE s.product_id = p.product_id
    GROUP BY COALESCE(s.metal, 'Unknown')
    ORDER BY COUNT(*) DESC, COALESCE(s.metal, 'Unknown') ASC
) met
OUTER APPLY (
    SELECT TOP (1)
        COALESCE(s.gem, 'Unknown') AS gem
    FROM dbo.jewelry_sales s
    WHERE s.product_id = p.product_id
    GROUP BY COALESCE(s.gem, 'Unknown')
    ORDER BY COUNT(*) DESC, COALESCE(s.gem, 'Unknown') ASC
) gem_attr;
GO
