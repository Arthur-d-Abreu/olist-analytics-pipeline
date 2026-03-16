CREATE VIEW vw_dim_estado_geo AS
SELECT
    geolocation_state,
    AVG(geolocation_lat) AS latitude,
    AVG(geolocation_lng) AS longitude
FROM dbo.olist_geolocation_dataset_clean
GROUP BY geolocation_state;
