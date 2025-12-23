-- SQLite schema for Olist dataset (IDs as TEXT; timestamps as ISO TEXT)

PRAGMA foreign_keys = OFF;

DROP TABLE IF EXISTS customers;
CREATE TABLE customers (
  customer_id TEXT PRIMARY KEY,
  customer_unique_id TEXT,
  customer_zip_code_prefix INTEGER,
  customer_city TEXT,
  customer_state TEXT
);

DROP TABLE IF EXISTS sellers;
CREATE TABLE sellers (
  seller_id TEXT PRIMARY KEY,
  seller_zip_code_prefix INTEGER,
  seller_city TEXT,
  seller_state TEXT
);

DROP TABLE IF EXISTS orders;
CREATE TABLE orders (
  order_id TEXT PRIMARY KEY,
  customer_id TEXT,
  order_status TEXT,
  order_purchase_timestamp TEXT,
  order_approved_at TEXT,
  order_delivered_carrier_date TEXT,
  order_delivered_customer_date TEXT,
  order_estimated_delivery_date TEXT
);

DROP TABLE IF EXISTS order_items;
CREATE TABLE order_items (
  order_id TEXT,
  order_item_id INTEGER,
  product_id TEXT,
  seller_id TEXT,
  shipping_limit_date TEXT,
  price REAL,
  freight_value REAL,
  PRIMARY KEY (order_id, order_item_id)
);

DROP TABLE IF EXISTS order_payments;
CREATE TABLE order_payments (
  order_id TEXT,
  payment_sequential INTEGER,
  payment_type TEXT,
  payment_installments INTEGER,
  payment_value REAL,
  PRIMARY KEY (order_id, payment_sequential)
);

DROP TABLE IF EXISTS order_reviews;
CREATE TABLE order_reviews (
  review_id TEXT,
  order_id TEXT,
  review_score INTEGER,
  review_comment_title TEXT,
  review_comment_message TEXT,
  review_creation_date TEXT,
  review_answer_timestamp TEXT
);

DROP TABLE IF EXISTS products;
CREATE TABLE products (
  product_id TEXT PRIMARY KEY,
  product_category_name TEXT,
  product_name_lenght INTEGER,
  product_description_lenght INTEGER,
  product_photos_qty INTEGER,
  product_weight_g INTEGER,
  product_length_cm INTEGER,
  product_height_cm INTEGER,
  product_width_cm INTEGER
);

DROP TABLE IF EXISTS geolocation;
CREATE TABLE geolocation (
  geolocation_zip_code_prefix INTEGER,
  geolocation_lat REAL,
  geolocation_lng REAL,
  geolocation_city TEXT,
  geolocation_state TEXT
);

DROP TABLE IF EXISTS category_translation;
CREATE TABLE category_translation (
  product_category_name TEXT PRIMARY KEY,
  product_category_name_english TEXT
);

PRAGMA foreign_keys = ON;
