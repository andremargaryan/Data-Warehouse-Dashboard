-- load_raw.sql
-- Charge les CSV bruts dans DuckDB tel quel, sans transformation

DROP TABLE IF EXISTS raw_orders;
DROP TABLE IF EXISTS raw_products;
DROP TABLE IF EXISTS raw_customers;
DROP TABLE IF EXISTS raw_returns;

CREATE TABLE raw_customers AS
    SELECT * FROM read_csv_auto('data/raw/customers.csv', header=true);

CREATE TABLE raw_products AS
    SELECT * FROM read_csv_auto('data/raw/products.csv', header=true);

CREATE TABLE raw_orders AS
    SELECT * FROM read_csv_auto('data/raw/orders.csv', header=true);

CREATE TABLE raw_returns AS
    SELECT * FROM read_csv_auto('data/raw/returns.csv', header=true);