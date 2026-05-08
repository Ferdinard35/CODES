-- Test trigger 2: mark a loan as defaulted
use retailbank_ghana;
UPDATE loans 
SET status = 'defaulted', defaulted_at = NOW() 
WHERE loan_id = 3;

-- Check audit_log again
SELECT * FROM audit_log;

-- Check that the customer got flagged automatically
SELECT customer_id, full_name, is_flagged 
FROM customers 
WHERE customer_id = (SELECT customer_id FROM loans WHERE loan_id = 3);