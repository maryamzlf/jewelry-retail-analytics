-- Data quality audit

-- 1. Coverage and grain
SELECT
    COUNT(*) AS transaction_lines,
    COUNT(DISTINCT order_id) AS orders,
    COUNT(DISTINCT product_id) AS products,
    COUNT(DISTINCT user_id) AS customers,
    MIN(event_time) AS first_purchase,
    MAX(event_time) AS last_purchase
FROM dbo.jewelry_sales;

-- 2. Missingness counts and percentages
SELECT
    COUNT(*) AS total_rows,
    SUM(CASE WHEN category_id IS NULL THEN 1 ELSE 0 END) AS missing_category_id,
    100.0 * SUM(CASE WHEN category_id IS NULL THEN 1 ELSE 0 END) / COUNT(*) AS missing_category_id_pct,
    SUM(CASE WHEN category_code IS NULL THEN 1 ELSE 0 END) AS missing_category_code,
    100.0 * SUM(CASE WHEN category_code IS NULL THEN 1 ELSE 0 END) / COUNT(*) AS missing_category_code_pct,
    SUM(CASE WHEN brand_code IS NULL THEN 1 ELSE 0 END) AS missing_brand_code,
    SUM(CASE WHEN gender IS NULL THEN 1 ELSE 0 END) AS missing_gender,
    100.0 * SUM(CASE WHEN gender IS NULL THEN 1 ELSE 0 END) / COUNT(*) AS missing_gender_pct,
    SUM(CASE WHEN color IS NULL THEN 1 ELSE 0 END) AS missing_color,
    SUM(CASE WHEN metal IS NULL THEN 1 ELSE 0 END) AS missing_metal,
    SUM(CASE WHEN gem IS NULL THEN 1 ELSE 0 END) AS missing_gem,
    100.0 * SUM(CASE WHEN gem IS NULL THEN 1 ELSE 0 END) / COUNT(*) AS missing_gem_pct
FROM dbo.jewelry_sales;

-- 3. Duplicate-group audit. These are flags, not automatic deletions.
SELECT
    is_exact_duplicate,
    COUNT(*) AS row_count,
    SUM(line_revenue) AS represented_revenue
FROM dbo.jewelry_sales
GROUP BY is_exact_duplicate;

-- 4. Required-field and numeric integrity
SELECT
    SUM(CASE WHEN quantity <= 0 THEN 1 ELSE 0 END) AS nonpositive_quantity_rows,
    SUM(CASE WHEN price < 0 THEN 1 ELSE 0 END) AS negative_price_rows,
    SUM(CASE WHEN line_revenue <> quantity * price THEN 1 ELSE 0 END) AS revenue_mismatch_rows
FROM dbo.jewelry_sales;

-- 5. Price distribution
SELECT
    MIN(price) AS min_price,
    AVG(price) AS avg_price,
    MAX(price) AS max_price
FROM dbo.jewelry_sales;

SELECT TOP (25)
    product_id,
    category_name,
    metal,
    gem,
    price
FROM dbo.jewelry_sales
ORDER BY price DESC;

-- 6. Taxonomy completeness by year-month
SELECT
    year_month,
    COUNT(*) AS transaction_lines,
    SUM(CASE WHEN category_code IS NULL THEN 1 ELSE 0 END) AS missing_category_lines,
    100.0 * SUM(CASE WHEN category_code IS NULL THEN 1 ELSE 0 END) / COUNT(*) AS missing_category_pct
FROM dbo.jewelry_sales
GROUP BY year_month
ORDER BY year_month;
