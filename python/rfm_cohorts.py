import argparse
import os
import sqlite3
import pandas as pd

def ensure_dir(p: str):
    os.makedirs(p, exist_ok=True)

def main():
    p = argparse.ArgumentParser(description="Compute RFM segments + cohort retention exports.")
    p.add_argument("--db", required=True)
    p.add_argument("--out", required=True)
    args = p.parse_args()

    ensure_dir(args.out)
    conn = sqlite3.connect(args.db)

    orders = pd.read_sql_query('''
    SELECT
      customer_unique_id,
      order_id,
      order_purchase_timestamp,
      revenue
    FROM vw_orders_full
    WHERE order_status='delivered' AND revenue IS NOT NULL;
    ''', conn)

    orders["order_purchase_timestamp"] = pd.to_datetime(orders["order_purchase_timestamp"], errors="coerce")
    max_date = orders["order_purchase_timestamp"].max()

    rfm = orders.groupby("customer_unique_id").agg(
        recency_days=("order_purchase_timestamp", lambda x: (max_date - x.max()).days),
        frequency=("order_id", "nunique"),
        monetary=("revenue", "sum"),
    ).reset_index()

    rfm["r_score"] = pd.qcut(rfm["recency_days"], 5, labels=[5,4,3,2,1]).astype(int)
    rfm["f_score"] = pd.qcut(rfm["frequency"].rank(method="first"), 5, labels=[1,2,3,4,5]).astype(int)
    rfm["m_score"] = pd.qcut(rfm["monetary"].rank(method="first"), 5, labels=[1,2,3,4,5]).astype(int)

    def segment(row):
        r,f,m = row["r_score"], row["f_score"], row["m_score"]
        if r>=4 and f>=4 and m>=4: return "Champions"
        if r>=4 and f>=3: return "Loyal"
        if r>=4 and f<=2: return "New Customers"
        if r==3 and f>=3: return "Potential Loyalist"
        if r<=2 and f>=4: return "At Risk (High F)"
        if r<=2 and m>=4: return "At Risk (High M)"
        if r<=2: return "Hibernating"
        return "Others"

    rfm["segment"] = rfm.apply(segment, axis=1)
    rfm.to_csv(os.path.join(args.out, "kpi_customer_rfm.csv"), index=False)

    orders["order_month"] = orders["order_purchase_timestamp"].dt.to_period("M").astype(str)
    first = orders.groupby("customer_unique_id")["order_month"].min().reset_index().rename(columns={"order_month":"cohort_month"})
    orders = orders.merge(first, on="customer_unique_id", how="left")

    cohort = orders.groupby(["cohort_month", "order_month"])["customer_unique_id"].nunique().reset_index()
    cohort["cohort_month_dt"] = pd.to_datetime(cohort["cohort_month"] + "-01")
    cohort["order_month_dt"] = pd.to_datetime(cohort["order_month"] + "-01")
    cohort["cohort_index"] = (cohort["order_month_dt"].dt.year - cohort["cohort_month_dt"].dt.year)*12 + (cohort["order_month_dt"].dt.month - cohort["cohort_month_dt"].dt.month)

    pivot = cohort.pivot_table(index="cohort_month", columns="cohort_index", values="customer_unique_id")
    sizes = pivot[0]
    retention = pivot.divide(sizes, axis=0)
    retention.to_csv(os.path.join(args.out, "kpi_cohort_retention.csv"))

    conn.close()
    print(f"Exported RFM + cohorts to: {args.out}")

if __name__ == "__main__":
    main()
