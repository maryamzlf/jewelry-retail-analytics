# Core DAX Measures

Assumed fact table: `jewelry_sales`  
Assumed date table: `DimDate`

```DAX
Gross Sales =
SUM ( jewelry_sales[line_revenue] )
```

```DAX
Orders =
DISTINCTCOUNT ( jewelry_sales[order_id] )
```

```DAX
Customers =
DISTINCTCOUNT ( jewelry_sales[user_id] )
```

```DAX
Products =
DISTINCTCOUNT ( jewelry_sales[product_id] )
```

```DAX
Units =
SUM ( jewelry_sales[quantity] )
```

```DAX
Average Order Value =
DIVIDE ( [Gross Sales], [Orders] )
```

```DAX
Average Item Price =
AVERAGE ( jewelry_sales[price] )
```

```DAX
Items per Order =
DIVIDE ( [Units], [Orders] )
```

```DAX
Repeat Customers =
COUNTROWS (
    FILTER (
        VALUES ( jewelry_sales[user_id] ),
        CALCULATE ( DISTINCTCOUNT ( jewelry_sales[order_id] ) ) > 1
    )
)
```

```DAX
Repeat Customer Rate =
DIVIDE ( [Repeat Customers], [Customers] )
```

```DAX
Sales Previous Month =
CALCULATE ( [Gross Sales], DATEADD ( DimDate[Date], -1, MONTH ) )
```

```DAX
MoM Sales % =
DIVIDE ( [Gross Sales] - [Sales Previous Month], [Sales Previous Month] )
```

```DAX
Sales Previous Year =
CALCULATE ( [Gross Sales], SAMEPERIODLASTYEAR ( DimDate[Date] ) )
```

```DAX
YoY Sales % =
DIVIDE ( [Gross Sales] - [Sales Previous Year], [Sales Previous Year] )
```

```DAX
Category Revenue Share =
DIVIDE (
    [Gross Sales],
    CALCULATE ( [Gross Sales], ALL ( jewelry_sales[category_name] ) )
)
```

```DAX
Missing Category Lines =
CALCULATE (
    COUNTROWS ( jewelry_sales ),
    ISBLANK ( jewelry_sales[category_code] )
)
```

```DAX
Missing Category Rate =
DIVIDE ( [Missing Category Lines], COUNTROWS ( jewelry_sales ) )
```

## Date table

```DAX
DimDate =
ADDCOLUMNS (
    CALENDAR ( MIN ( jewelry_sales[order_date] ), MAX ( jewelry_sales[order_date] ) ),
    "Year", YEAR ( [Date] ),
    "Month Number", MONTH ( [Date] ),
    "Month", FORMAT ( [Date], "MMM" ),
    "Year Month", FORMAT ( [Date], "YYYY-MM" ),
    "Quarter", "Q" & FORMAT ( [Date], "Q" )
)
```

After creation, mark `DimDate` as the model's date table and relate `DimDate[Date]` (1) to `jewelry_sales[order_date]` (*).
