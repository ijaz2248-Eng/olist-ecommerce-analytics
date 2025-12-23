# Data setup

Download the **Olist Brazilian E-Commerce Public Dataset** from Kaggle
(search: “Brazilian E-Commerce Public Dataset by Olist”).  

## Expected folder structure
Place the CSVs here:

```
data/raw/brazilian-ecommerce/
├─ olist_customers_dataset.csv
├─ olist_sellers_dataset.csv
├─ olist_orders_dataset.csv
├─ olist_order_items_dataset.csv
├─ olist_order_payments_dataset.csv
├─ olist_order_reviews_dataset.csv
├─ olist_products_dataset.csv
├─ olist_geolocation_dataset.csv
└─ product_category_name_translation.csv
```

The raw dataset is not stored in this repo because it is large and third-party.
## Note on raw data
The original Olist raw dataset is not included in this repository.
To rebuild the database from scratch, download the dataset from Kaggle
and place the CSV files into:

data/raw/brazilian-ecommerce/

The provided SQLite database and KPI exports can be used directly
for analysis and dashboards.
## Dashboard Preview
![Dashboard](assets/images/dashboard_full.png)
