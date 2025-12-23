-- Reporting layer views (SQLite)

DROP VIEW IF EXISTS vw_orders_enriched;
CREATE VIEW vw_orders_enriched AS
SELECT
  o.order_id,
  o.customer_id,
  c.customer_unique_id,
  c.customer_city,
  c.customer_state,
  o.order_status,
  o.order_purchase_timestamp,
  o.order_approved_at,
  o.order_delivered_carrier_date,
  o.order_delivered_customer_date,
  o.order_estimated_delivery_date,
  CASE
    WHEN o.order_delivered_customer_date IS NOT NULL AND o.order_estimated_delivery_date IS NOT NULL
     AND julianday(o.order_delivered_customer_date) > julianday(o.order_estimated_delivery_date) THEN 1
    ELSE 0
  END AS is_late_delivery,
  CASE
    WHEN o.order_delivered_customer_date IS NOT NULL AND o.order_purchase_timestamp IS NOT NULL
    THEN julianday(o.order_delivered_customer_date) - julianday(o.order_purchase_timestamp)
    ELSE NULL
  END AS delivery_days
FROM orders o
LEFT JOIN customers c ON c.customer_id = o.customer_id;

DROP VIEW IF EXISTS vw_order_financials;
CREATE VIEW vw_order_financials AS
SELECT
  o.order_id,
  SUM(oi.price) AS revenue,
  SUM(oi.freight_value) AS freight,
  SUM(oi.price + oi.freight_value) AS gmv,
  COUNT(oi.order_item_id) AS items
FROM orders o
LEFT JOIN order_items oi ON oi.order_id = o.order_id
GROUP BY o.order_id;

DROP VIEW IF EXISTS vw_order_reviews;
CREATE VIEW vw_order_reviews AS
SELECT
  order_id,
  AVG(review_score) AS avg_review_score,
  COUNT(*) AS review_count
FROM order_reviews
GROUP BY order_id;

DROP VIEW IF EXISTS vw_orders_full;
CREATE VIEW vw_orders_full AS
SELECT
  e.*,
  f.revenue,
  f.freight,
  f.gmv,
  f.items,
  r.avg_review_score,
  r.review_count
FROM vw_orders_enriched e
LEFT JOIN vw_order_financials f ON f.order_id = e.order_id
LEFT JOIN vw_order_reviews r ON r.order_id = e.order_id;

DROP VIEW IF EXISTS vw_items_full;
CREATE VIEW vw_items_full AS
SELECT
  oi.order_id,
  oi.order_item_id,
  oi.product_id,
  p.product_category_name,
  t.product_category_name_english,
  oi.seller_id,
  s.seller_state,
  oi.price,
  oi.freight_value,
  (oi.price + oi.freight_value) AS gmv_item
FROM order_items oi
LEFT JOIN products p ON p.product_id = oi.product_id
LEFT JOIN category_translation t ON t.product_category_name = p.product_category_name
LEFT JOIN sellers s ON s.seller_id = oi.seller_id;
