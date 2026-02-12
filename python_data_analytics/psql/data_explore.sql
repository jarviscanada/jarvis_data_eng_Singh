-- =====================================================
-- LGS Retail Data Exploration
-- Purpose: Basic OLAP profiling queries
-- =====================================================

-- Show table schema (psql meta-command)
\d+ retail;

-- Q1: Show first 10 rows
SELECT *
FROM retail
LIMIT 10;

-- Q2: Check # of records
SELECT COUNT(*) AS total_records
FROM retail;

-- Q3: Number of clients (unique customer_id)
SELECT COUNT(DISTINCT customer_id) AS unique_customers
FROM retail
WHERE customer_id IS NOT NULL;

-- Q4: Invoice date range (max/min dates)
SELECT
  MAX(invoice_date) AS max_date,
  MIN(invoice_date) AS min_date
FROM retail;

-- Q5: Number of SKU (unique stock_code)
SELECT COUNT(DISTINCT stock_code) AS unique_sku
FROM retail
WHERE stock_code IS NOT NULL;

-- Q6: Average invoice amount excluding invoices with negative amount
WITH invoice_totals AS (
  SELECT
    invoice_no,
    SUM(quantity * unit_price) AS invoice_amount
  FROM retail
  GROUP BY invoice_no
  HAVING SUM(quantity * unit_price) > 0
)
SELECT AVG(invoice_amount) AS avg_invoice_amount
FROM invoice_totals;

-- Q7: Total revenue (sum of unit_price * quantity)
SELECT SUM(unit_price * quantity) AS total_revenue
FROM retail;

-- Q8: Total revenue by YYYYMM
SELECT
  (EXTRACT(YEAR FROM invoice_date)::int * 100 + EXTRACT(MONTH FROM invoice_date)::int) AS yyyymm,
  SUM(unit_price * quantity) AS monthly_revenue
FROM retail
GROUP BY yyyymm
ORDER BY yyyymm;

