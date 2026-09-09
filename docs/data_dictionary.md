# Data Dictionary

## Clean analytical table: `jewelry_sales`

| Field | Type | Origin | Description |
|---|---|---|---|
| `event_time` | datetime UTC | source | Purchase timestamp. |
| `order_id` | string / bigint-compatible | source | Order identifier. Multiple product rows can belong to one order. |
| `product_id` | string / bigint-compatible | source | Product identifier. |
| `quantity` | integer | source | Purchased quantity. In this snapshot every row has quantity = 1. |
| `category_id` | string / bigint-compatible | source | Source category identifier; missing in structurally short rows. |
| `category_code` | text | source | Product taxonomy such as `jewelry.ring`; may be missing. |
| `brand_code` | integer | source `brand` | Encoded/obfuscated brand value in this dataset; missing in structurally short rows. |
| `price` | decimal | source | Unit selling price. |
| `user_id` | string / bigint-compatible | source | Persistent customer identifier. |
| `gender` | text | source | Source gender field; heavily missing. |
| `color` | text | source | Product color attribute. |
| `metal` | text | source | Product metal, e.g. gold or silver. |
| `gem` | text | source | Gemstone attribute, e.g. diamond, topaz, fianit. |
| `line_revenue` | decimal | derived | `quantity * price`. |
| `order_date` | date | derived | Calendar date from `event_time`. |
| `year_month` | `YYYY-MM` text | derived | Month key for trend analysis. |
| `category_name` | text | derived | Friendly category label derived from `category_code`; missing taxonomy becomes `Unknown`. |
| `price_band` | text | derived | Merchandising band: Under $100, $100–$249, $250–$499, $500–$999, $1,000+. |
| `is_exact_duplicate` | boolean | derived | Flags all rows that belong to an exact duplicate group. Rows are preserved rather than automatically deleted. |

## Structural repair rule

The uploaded snapshot contains both 13-field and 11-field physical records. In the 11-field form, `category_code` and `brand` are absent while `category_id` is blank. If the raw file is parsed naively as a standard CSV, `price`, `user_id`, and downstream attributes shift into the wrong columns. `python/01_prepare_data.py` repairs this row structure *before* pandas parsing and type conversion.

## Null handling

Missing descriptive attributes are retained as nulls in the cleaned data. Analytical summaries convert them to `Unknown` only when grouping, so missingness remains measurable and is not confused with a real product attribute.
