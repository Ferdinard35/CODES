-- Test trigger 1: insert one repayment
use retailbank_ghana;
INSERT INTO repayments 
  (loan_id, schedule_id, amount_paid, payment_date, payment_mode, is_late, days_late, recorded_by)
VALUES 
  (1, NULL, 500.00, CURRENT_DATE, 'mobile_money', 0, 0, 'Kofi Mensah');

-- Now check audit_log
SELECT * FROM audit_log;