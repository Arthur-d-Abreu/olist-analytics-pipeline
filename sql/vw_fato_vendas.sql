CREATE VIEW vw_fato_vendas AS 
SELECT
	oi.order_id						AS order_id,
	oi.product_id					AS sk_product,
	c.customer_unique_id			AS sk_customer,
	oi.seller_id					AS sk_seller,

	CAST(o.order_purchase_timestamp AS date) AS sk_date,
	
	oi.price,
	oi.freight_value,
	(oi.price + oi.freight_value)	AS total_value

FROM olist_order_items_dataset_clean oi

JOIN olist_orders_dataset_clean o
	ON oi.order_id = o.order_id

JOIN olist_customers_dataset_clean c
	ON o.customer_id = c.customer_id;