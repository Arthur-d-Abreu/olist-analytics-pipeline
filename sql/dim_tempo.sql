CREATE TABLE dim_tempo (
    date_sk INT PRIMARY KEY,
    full_date DATE NOT NULL,

    year INT,
    quarter INT,
    month INT,
    month_name VARCHAR(20),

    day INT,
    day_of_week INT,
    day_name VARCHAR(20),

    week_of_year INT,
    is_weekend BIT
);

WITH calendario AS (
    SELECT CAST('2016-01-01' AS DATE) AS full_date
    UNION ALL
    SELECT DATEADD(DAY, 1, full_date)
    FROM calendario
    WHERE full_date < '2018-12-31'
)
INSERT INTO dim_tempo
SELECT
    CONVERT(INT, FORMAT(full_date, 'yyyyMMdd')) AS date_sk,
    full_date,

    YEAR(full_date) AS year,
    DATEPART(QUARTER, full_date) AS quarter,
    MONTH(full_date) AS month,
    DATENAME(MONTH, full_date) AS month_name,

    DAY(full_date) AS day,
    DATEPART(WEEKDAY, full_date) AS day_of_week,
    DATENAME(WEEKDAY, full_date) AS day_name,

    DATEPART(WEEK, full_date) AS week_of_year,

    CASE 
        WHEN DATEPART(WEEKDAY, full_date) IN (1,7)
            THEN 1 ELSE 0
    END AS is_weekend
FROM calendario
OPTION (MAXRECURSION 2000);