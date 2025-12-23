# KPI Definitions

## Revenue
Sum of item price across order items.  
`SUM(oi.price)`

## GMV
Item price + freight.  
`SUM(oi.price + oi.freight_value)`

## AOV
Revenue / delivered orders in period.  
`SUM(revenue) / COUNT(DISTINCT order_id)` (delivered only)

## Late Delivery Rate
Delivered orders where delivered date > estimated date.  
`late_orders / delivered_orders`

## Average Delivery Days
`AVG(julianday(delivered) - julianday(purchase))`

## Average Review Score
`AVG(review_score)` for orders with reviews.

## RFM
- Recency = days since last purchase (as of max dataset date)
- Frequency = number of orders
- Monetary = total revenue
