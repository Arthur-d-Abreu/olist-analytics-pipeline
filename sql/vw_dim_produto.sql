CREATE VIEW vw_dim_produto AS
SELECT
	product_id					AS sk_product,
	product_category_name		AS product_category,
	product_weight_g			AS product_weight,
	product_length_cm			AS product_length,
	product_height_cm			AS product_height,
	product_width_cm			AS product_width,

	(product_length_cm * product_height_cm * product_width_cm) as volume_cm3,

	CASE
		WHEN(product_length_cm * product_height_cm * product_width_cm) <= 20000
			THEN 'Pequeno'
		WHEN(product_length_cm * product_height_cm * product_width_cm) <= 100000
			THEN 'Médio'
		ELSE 'Grande'
	END AS product_size
FROM olist_products_dataset_clean;