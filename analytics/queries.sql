-- =========================================
-- 1. TOTAL REVENUE
-- =========================================

SELECT
    SUM(amount) AS total_revenue
FROM fact_payment
WHERE status = 'Paid';


-- =========================================
-- 2. TOTAL BOOKINGS
-- =========================================

SELECT
    COUNT(*) AS total_bookings
FROM fact_booking;


-- =========================================
-- 3. MONTHLY REVENUE
-- =========================================

SELECT
    DATE_TRUNC('month', payment_date) AS revenue_month,
    SUM(amount) AS total_revenue
FROM fact_payment
WHERE status = 'Paid'
GROUP BY DATE_TRUNC('month', payment_date)
ORDER BY revenue_month;


-- =========================================
-- 4. BOOKINGS PER MONTH
-- =========================================

SELECT
    DATE_TRUNC('month', booking_date) AS booking_month,
    COUNT(*) AS total_bookings
FROM fact_booking
GROUP BY DATE_TRUNC('month', booking_date)
ORDER BY booking_month;


-- =========================================
-- 5. REVENUE PER PACKAGE
-- =========================================

SELECT
    dp.package_name,
    SUM(fp.amount) AS total_revenue
FROM fact_payment fp
JOIN fact_booking fb
    ON fp.booking_key = fb.booking_key
JOIN dim_package dp
    ON fb.package_key = dp.package_key
WHERE fp.status = 'Paid'
GROUP BY dp.package_name
ORDER BY total_revenue DESC;


-- =========================================
-- 6. PACKAGE POPULARITY
-- =========================================

SELECT
    dp.package_name,
    COUNT(*) AS total_bookings
FROM fact_booking fb
JOIN dim_package dp
    ON fb.package_key = dp.package_key
GROUP BY dp.package_name
ORDER BY total_bookings DESC;


-- =========================================
-- 7. PHOTOGRAPHER PERFORMANCE
-- =========================================

SELECT
    dph.name AS photographer_name,
    COUNT(fb.booking_key) AS total_bookings
FROM fact_booking fb
JOIN dim_photographer dph
    ON fb.photographer_key = dph.photographer_key
GROUP BY dph.name
ORDER BY total_bookings DESC;


-- =========================================
-- 8. REPEAT CLIENT
-- =========================================

SELECT
    dc.name AS client_name,
    COUNT(fb.booking_key) AS total_bookings
FROM fact_booking fb
JOIN dim_client dc
    ON fb.client_key = dc.client_key
GROUP BY dc.name
HAVING COUNT(fb.booking_key) > 1
ORDER BY total_bookings DESC;


-- =========================================
-- 9. OUTSTANDING / UNPAID BOOKINGS
-- =========================================

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
    fb.status
ORDER BY fb.booking_id;