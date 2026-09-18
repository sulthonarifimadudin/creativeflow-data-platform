-- =========================================
-- 1. TOTAL REVENUE
-- =========================================

CREATE OR REPLACE VIEW vw_total_revenue AS
SELECT
    SUM(amount) AS total_revenue
FROM fact_payment
WHERE status = 'Paid';


-- =========================================
-- 2. TOTAL BOOKINGS
-- =========================================

CREATE OR REPLACE VIEW vw_total_bookings AS
SELECT
    COUNT(*) AS total_bookings
FROM fact_booking;


-- =========================================
-- 3. MONTHLY REVENUE
-- =========================================

CREATE OR REPLACE VIEW vw_monthly_revenue AS
SELECT
    DATE_TRUNC('month', payment_date) AS revenue_month,
    SUM(amount) AS total_revenue
FROM fact_payment
WHERE status = 'Paid'
GROUP BY DATE_TRUNC('month', payment_date);


-- =========================================
-- 4. BOOKINGS PER MONTH
-- =========================================

CREATE OR REPLACE VIEW vw_booking_per_month AS
SELECT
    DATE_TRUNC('month', booking_date) AS booking_month,
    COUNT(*) AS total_bookings
FROM fact_booking
GROUP BY DATE_TRUNC('month', booking_date);


-- =========================================
-- 5. REVENUE PER PACKAGE
-- =========================================

CREATE OR REPLACE VIEW vw_revenue_per_package AS
SELECT
    dp.package_name,
    SUM(fp.amount) AS total_revenue
FROM fact_payment fp
JOIN fact_booking fb
    ON fp.booking_key = fb.booking_key
JOIN dim_package dp
    ON fb.package_key = dp.package_key
WHERE fp.status = 'Paid'
GROUP BY dp.package_name;


-- =========================================
-- 6. PACKAGE POPULARITY
-- =========================================

CREATE OR REPLACE VIEW vw_package_popularity AS
SELECT
    dp.package_name,
    COUNT(*) AS total_bookings
FROM fact_booking fb
JOIN dim_package dp
    ON fb.package_key = dp.package_key
GROUP BY dp.package_name;


-- =========================================
-- 7. PHOTOGRAPHER PERFORMANCE
-- =========================================

CREATE OR REPLACE VIEW vw_photographer_performance AS
SELECT
    dph.name AS photographer_name,
    COUNT(fb.booking_key) AS total_bookings
FROM fact_booking fb
JOIN dim_photographer dph
    ON fb.photographer_key = dph.photographer_key
GROUP BY dph.name;


-- =========================================
-- 8. REPEAT CLIENT
-- =========================================

CREATE OR REPLACE VIEW vw_repeat_client AS
SELECT
    dc.name AS client_name,
    COUNT(fb.booking_key) AS total_bookings
FROM fact_booking fb
JOIN dim_client dc
    ON fb.client_key = dc.client_key
GROUP BY dc.name
HAVING COUNT(fb.booking_key) > 1;


-- =========================================
-- 9. PAYMENT SUMMARY PER BOOKING
-- =========================================

CREATE OR REPLACE VIEW vw_payment_summary AS
SELECT
    fb.booking_id,
    dc.name AS client_name,
    dp.package_name,
    fb.status AS booking_status,

    COALESCE(
        SUM(
            CASE
                WHEN fp.status = 'Paid'
                THEN fp.amount
                ELSE 0
            END
        ),
        0
    ) AS total_paid

FROM fact_booking fb

JOIN dim_client dc
    ON fb.client_key = dc.client_key

JOIN dim_package dp
    ON fb.package_key = dp.package_key

LEFT JOIN fact_payment fp
    ON fb.booking_key = fp.booking_key

GROUP BY
    fb.booking_id,
    dc.name,
    dp.package_name,
    fb.status;