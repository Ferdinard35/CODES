
--  RetailBank Ghana — Triggers
--  2 automated audit triggers

USE retailbank_ghana;

-- Change delimiter so MySQL doesn't break on semicolons inside trigger body
DELIMITER $$

-- ── TRIGGER 1 ──────────────────────────────────────────────────
-- trg_after_repayment_insert
-- Fires AFTER every repayment row is inserted.
-- Logs the event to audit_log automatically.
-- ──────────────────────────────────────────────────────────────
DROP TRIGGER IF EXISTS trg_after_repayment_insert$$

CREATE TRIGGER trg_after_repayment_insert
AFTER INSERT ON repayments
FOR EACH ROW
BEGIN
    DECLARE v_customer_id INT;

    -- Look up the customer who owns this loan
    SELECT customer_id INTO v_customer_id
    FROM loans
    WHERE loan_id = NEW.loan_id;

    -- Write to audit log
    INSERT INTO audit_log (
        event_type,
        table_name,
        record_id,
        customer_id,
        loan_id,
        description,
        event_time
    ) VALUES (
        'REPAYMENT_RECEIVED',
        'repayments',
        NEW.repayment_id,
        v_customer_id,
        NEW.loan_id,
        CONCAT(
            'Payment of GHS ', FORMAT(NEW.amount_paid, 2),
            ' received on ', NEW.payment_date,
            ' via ', NEW.payment_mode,
            IF(NEW.is_late = 1,
               CONCAT(' — LATE by ', NEW.days_late, ' day(s)'),
               ' — On time')
        ),
        NOW()
    );
END$$


-- ── TRIGGER 2 ──────────────────────────────────────────────────
-- trg_loan_status_change
-- Fires AFTER a loan row is updated.
-- When status flips to 'defaulted':
--   1. Stamps the defaulted_at timestamp on the loan
--   2. Flags the customer (is_flagged = 1)
--   3. Logs the event to audit_log
-- ──────────────────────────────────────────────────────────────
DROP TRIGGER IF EXISTS trg_loan_status_change$$

CREATE TRIGGER trg_loan_status_change
AFTER UPDATE ON loans
FOR EACH ROW
BEGIN
    -- Only act when status changes TO 'defaulted'
    IF NEW.status = 'defaulted' AND OLD.status != 'defaulted' THEN

        -- 1. Stamp defaulted_at (UPDATE — we're in AFTER trigger so we log, not re-update)
        --    Note: defaulted_at should be set in the UPDATE statement itself.
        --    Here we flag the customer and audit the event.

        -- 2. Flag the customer as high risk
        UPDATE customers
        SET is_flagged = 1
        WHERE customer_id = NEW.customer_id;

        -- 3. Log to audit trail
        INSERT INTO audit_log (
            event_type,
            table_name,
            record_id,
            customer_id,
            loan_id,
            description,
            event_time
        ) VALUES (
            'LOAN_DEFAULTED',
            'loans',
            NEW.loan_id,
            NEW.customer_id,
            NEW.loan_id,
            CONCAT(
                'Loan #', NEW.loan_id,
                ' (GHS ', FORMAT(NEW.approved_amount, 2), ' approved) ',
                'has been marked as DEFAULTED. ',
                'Outstanding balance: GHS ', FORMAT(NEW.outstanding_balance, 2), '. ',
                'Customer flagged for risk review.'
            ),
            NOW()
        );

    END IF;
END$$

DELIMITER ;

