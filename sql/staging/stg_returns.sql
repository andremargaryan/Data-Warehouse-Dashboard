-- stg_returns.sql

DROP TABLE IF EXISTS stg_returns;

CREATE TABLE stg_returns AS
SELECT DISTINCT
    TRIM(return_id)                                     AS return_id,
    TRIM(order_id)                                      AS order_id,
    CAST(return_date AS DATE)                           AS return_date,
    TRIM(COALESCE(reason, 'Raison inconnue'))           AS reason,
    CAST(refund_amount AS DOUBLE)                       AS refund_amount
FROM raw_returns
WHERE return_id IS NOT NULL;