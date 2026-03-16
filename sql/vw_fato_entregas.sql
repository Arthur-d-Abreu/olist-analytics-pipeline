CREATE OR ALTER VIEW vw_fato_entregas AS
SELECT
    o.order_id,
    c.customer_unique_id AS sk_customer,
    oi.seller_id,

    o.order_purchase_timestamp        AS data_compra,
    o.order_delivered_customer_date   AS data_entrega,
    o.order_estimated_delivery_date   AS data_estimada,

    DATEDIFF(DAY,
        o.order_purchase_timestamp,
        o.order_delivered_customer_date
    ) AS dias_entregas,

    DATEDIFF(DAY,
        o.order_purchase_timestamp,
        o.order_estimated_delivery_date
    ) AS dias_estimados,

    CASE
        WHEN CAST(o.order_delivered_customer_date AS DATE) >
             CAST(o.order_estimated_delivery_date AS DATE)
        THEN DATEDIFF(DAY,
                o.order_estimated_delivery_date,
                o.order_delivered_customer_date
        )
        ELSE 0
    END AS atraso_dias,

    CASE 
        WHEN CAST(o.order_delivered_customer_date AS DATE) >
             CAST(o.order_estimated_delivery_date AS DATE)
        THEN 1
        ELSE 0
    END AS flag_atraso

FROM olist_orders_dataset_clean o

JOIN olist_order_items_dataset_clean oi
    ON o.order_id = oi.order_id

JOIN olist_customers_dataset_clean c
    ON o.customer_id = c.customer_id

WHERE o.order_status = 'delivered';