CREATE VIEW vw_dim_cliente AS
SELECT
	customer_id					AS sk_customer,
	customer_zip_code_prefix	AS customer_zip_code,
	UPPER(customer_city)		AS customer_city,
	customer_state				AS customer_state
FROM olist_customers_dataset_clean;

SELECT * FROM vw_dim_cliente