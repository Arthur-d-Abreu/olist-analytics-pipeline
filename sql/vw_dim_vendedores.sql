CREATE VIEW vw_dim_vendedores AS
SELECT
	seller_id					AS sk_seller,
	seller_zip_code_prefix		AS seller_zip_code,
	UPPER(seller_city)			AS seller_city,
	seller_state				AS seller_state
FROM olist_sellers_dataset_clean;