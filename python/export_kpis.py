import argparse
import os
import sqlite3
import pandas as pd

def q(conn, sql: str) -> pd.DataFrame:
    return pd.read_sql_query(sql, conn)

def ensure_dir(p: str):
    os.makedirs(p, exist_ok=True)

def main():
    p = argparse.ArgumentParser(description="Export KPI datasets (CSV) for Excel dashboards.")
    p.add_argument("--db", required=True)
    p.add_argument("--out", required=True)
    args = p.parse_args()

    ensure_dir(args.out)
    conn = sqlite3.connect(args.db)

    kpi_orders_monthly = q(conn, '''
    SELECT
      substr(order_purchase_timestamp, 1, 7) AS year_month,
      COUNT(DISTINCT order_id) AS orders,
      SUM(revenue) AS revenue,
      SUM(freight) AS freight,
      SUM(gmv) AS gmv,
      AVG(revenue) AS aov,
      AVG(items) AS avg_items_per_order,
      AVG(is_late_delivery) AS late_delivery_rate,
      AVG(delivery_days) AS avg_delivery_days,
      AVG(avg_review_score) AS avg_review_score
    FROM vw_orders_full
    WHERE order_status = 'delivered'
    GROUP BY 1
    ORDER BY 1;
    ''')
    kpi_orders_monthly.to_csv(os.path.join(args.out, "kpi_orders_monthly.csv"), index=False)

    kpi_delivery_sla_state = q(conn, '''
    SELECT
      customer_state,
      COUNT(DISTINCT order_id) AS delivered_orders,
      AVG(is_late_delivery) AS late_delivery_rate,
      AVG(delivery_days) AS avg_delivery_days,
      AVG(avg_review_score) AS avg_review_score
    FROM vw_orders_full
    WHERE order_status = 'delivered'
    GROUP BY 1
    ORDER BY delivered_orders DESC;
    ''')
    kpi_delivery_sla_state.to_csv(os.path.join(args.out, "kpi_delivery_sla_state.csv"), index=False)

    kpi_seller_performance = q(conn, '''
    WITH seller_orders AS (
      SELECT
        oi.seller_id,
        s.seller_state,
        o.order_id,
        o.order_status,
        o.is_late_delivery,
        o.revenue,
        o.avg_review_score
      FROM order_items oi
      LEFT JOIN vw_orders_full o ON o.order_id = oi.order_id
      LEFT JOIN sellers s ON s.seller_id = oi.seller_id
      GROUP BY oi.seller_id, o.order_id
    )
    SELECT
      seller_id,
      seller_state,
      COUNT(DISTINCT order_id) AS orders,
      SUM(CASE WHEN order_status='delivered' THEN revenue ELSE 0 END) AS delivered_revenue,
      AVG(CASE WHEN order_status='delivered' THEN is_late_delivery END) AS late_delivery_rate,
      AVG(CASE WHEN order_status='delivered' THEN avg_review_score END) AS avg_review_score
    FROM seller_orders
    GROUP BY 1,2
    HAVING orders >= 50
    ORDER BY delivered_revenue DESC;
    ''')
    kpi_seller_performance.to_csv(os.path.join(args.out, "kpi_seller_performance.csv"), index=False)

    kpi_category_performance = q(conn, '''
    SELECT
      COALESCE(product_category_name_english, product_category_name, 'unknown') AS category,
      COUNT(DISTINCT order_id) AS orders,
      SUM(price) AS revenue,
      SUM(freight_value) AS freight,
      AVG(freight_value / NULLIF(price,0)) AS avg_freight_to_price_ratio,
      AVG(gmv_item) AS avg_item_gmv
    FROM vw_items_full
    GROUP BY 1
    HAVING orders >= 100
    ORDER BY revenue DESC;
    ''')
    kpi_category_performance.to_csv(os.path.join(args.out, "kpi_category_performance.csv"), index=False)

    kpi_payment_mix_monthly = q(conn, '''
    SELECT
      substr(o.order_purchase_timestamp, 1, 7) AS year_month,
      p.payment_type,
      COUNT(DISTINCT p.order_id) AS orders,
      SUM(p.payment_value) AS payment_value,
      AVG(p.payment_installments) AS avg_installments
    FROM order_payments p
    LEFT JOIN orders o ON o.order_id = p.order_id
    GROUP BY 1,2
    ORDER BY 1, payment_value DESC;
    ''')
    kpi_payment_mix_monthly.to_csv(os.path.join(args.out, "kpi_payment_mix_monthly.csv"), index=False)

    conn.close()
    print(f"Exported KPI CSVs to: {args.out}")

if __name__ == "__main__":
    main()
