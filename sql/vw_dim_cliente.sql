CREATE VIEW vw_dim_cliente AS
SELECT
    customer_unique_id AS sk_customer,
    MIN(customer_zip_code_prefix) AS customer_zip_code,
    UPPER(MIN(customer_city)) AS customer_city,
    MIN(customer_state) AS customer_state
FROM olist_customers_dataset_clean
GROUP BY customer_unique_id;

SELECT * FROM vw_dim_cliente
