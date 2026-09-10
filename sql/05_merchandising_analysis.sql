-- Product, category, metal, gemstone, and price-band analysis

-- 1. Category performance
SELECT
    category_name,
    COUNT(*) AS transaction_lines,
    SUM(quantity) AS units,
    COUNT(DISTINCT order_id) AS orders,
    COUNT(DISTINCT user_id) AS customers,
    SUM(line_revenue) AS revenue,
    AVG(price) AS avg_item_price,
    100.0 * SUM(line_revenue) / SUM(SUM(line_revenue)) OVER () AS revenue_share_pct
FROM dbo.jewelry_sales
GROUP BY category_name
ORDER BY revenue DESC;

-- 2. Metal performance
SELECT
    COALESCE(metal, 'Unknown') AS metal,
    SUM(quantity) AS units,
    COUNT(DISTINCT order_id) AS orders,
    SUM(line_revenue) AS revenue,
    AVG(price) AS avg_item_price,
    100.0 * SUM(line_revenue) / SUM(SUM(line_revenue)) OVER () AS revenue_share_pct
FROM dbo.jewelry_sales
GROUP BY COALESCE(metal, 'Unknown')
ORDER BY revenue DESC;

-- 3. Gemstone performance
SELECT
    COALESCE(gem, 'Unknown') AS gem,
    SUM(quantity) AS units,
    COUNT(DISTINCT order_id) AS orders,
    SUM(line_revenue) AS revenue,
    AVG(price) AS avg_item_price,
    100.0 * SUM(line_revenue) / SUM(SUM(line_revenue)) OVER () AS revenue_share_pct
FROM dbo.jewelry_sales
GROUP BY COALESCE(gem, 'Unknown')
ORDER BY revenue DESC;

-- 4. Price-band performance
SELECT
    price_band,
    SUM(quantity) AS units,
    COUNT(DISTINCT order_id) AS orders,
    SUM(line_revenue) AS revenue,
    AVG(price) AS avg_item_price,
    100.0 * SUM(line_revenue) / SUM(SUM(line_revenue)) OVER () AS revenue_share_pct
FROM dbo.jewelry_sales
GROUP BY price_band
ORDER BY CASE price_band
    WHEN 'Under $100' THEN 1
    WHEN '$100-$249' THEN 2
    WHEN '$250-$499' THEN 3
    WHEN '$500-$999' THEN 4
    WHEN '$1,000+' THEN 5
    ELSE 6
END;

-- 5. Top products by revenue
-- Python uses the modal category/metal/gem value for each product. The OUTER
-- APPLY blocks below mirror that rule and use alphabetical order as a stable
-- tie-break, matching pandas mode().iat[0] behavior.
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
SELECT TOP (100)
    p.product_id,
    cat.category_name,
    met.metal,
    gem_attr.gem,
    p.units,
    p.orders,
    p.revenue,
    p.avg_item_price,
    DENSE_RANK() OVER (ORDER BY p.revenue DESC) AS revenue_rank
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
) gem_attr
ORDER BY p.revenue DESC;

-- 6. Category x gemstone matrix
SELECT
    category_name,
    COALESCE(gem, 'Unknown') AS gem,
    SUM(line_revenue) AS revenue,
    COUNT(DISTINCT order_id) AS orders,
    AVG(price) AS avg_item_price
FROM dbo.jewelry_sales
GROUP BY category_name, COALESCE(gem, 'Unknown')
HAVING SUM(line_revenue) > 0
ORDER BY revenue DESC;
