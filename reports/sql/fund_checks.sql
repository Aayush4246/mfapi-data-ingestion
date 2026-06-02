-- Verify unique AMFI codes
SELECT amfi_code, COUNT(*) AS occurrences
FROM fund_master
GROUP BY amfi_code
HAVING COUNT(*) > 1;

-- Check NAV date range per fund
SELECT amfi_code, MIN(nav_date) AS start_date, MAX(nav_date) AS end_date
FROM nav_history
GROUP BY amfi_code;

-- Validate NAV values are positive
SELECT amfi_code, nav_date, nav_value
FROM nav_history
WHERE nav_value <= 0;
