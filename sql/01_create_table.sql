-- SQL Server / T-SQL
-- Run after python/01_prepare_data.py creates data/processed/jewelry_clean.csv.

DROP TABLE IF EXISTS dbo.jewelry_sales;
GO

CREATE TABLE dbo.jewelry_sales (
    event_time          datetimeoffset(0) NOT NULL,
    order_id            varchar(30) NOT NULL,
    product_id          varchar(30) NOT NULL,
    quantity            int NOT NULL,
    category_id         varchar(30) NULL,
    category_code       varchar(100) NULL,
    brand_code          int NULL,
    price               decimal(12,2) NOT NULL,
    user_id             varchar(30) NOT NULL,
    gender              varchar(10) NULL,
    color               varchar(50) NULL,
    metal               varchar(50) NULL,
    gem                 varchar(100) NULL,
    line_revenue        decimal(14,2) NOT NULL,
    order_date          date NOT NULL,
    year_month          char(7) NOT NULL,
    category_name       varchar(100) NOT NULL,
    price_band          varchar(20) NOT NULL,
    is_exact_duplicate  bit NOT NULL,
    CONSTRAINT CK_jewelry_sales_quantity_positive CHECK (quantity > 0),
    CONSTRAINT CK_jewelry_sales_price_nonnegative CHECK (price >= 0)
);
GO

CREATE INDEX IX_jewelry_sales_order_id
    ON dbo.jewelry_sales(order_id);
CREATE INDEX IX_jewelry_sales_user_id
    ON dbo.jewelry_sales(user_id);
CREATE INDEX IX_jewelry_sales_event_time
    ON dbo.jewelry_sales(event_time);
CREATE INDEX IX_jewelry_sales_product_id
    ON dbo.jewelry_sales(product_id);
CREATE INDEX IX_jewelry_sales_category
    ON dbo.jewelry_sales(category_name);
GO

-- Import the cleaned CSV using SSMS Import Flat File, BULK INSERT,
-- Azure Data Factory, or another ETL process appropriate to your environment.
