
--  RetailBank Ghana — Reporting Views
--  3 reusable views for dashboards and reporting


USE retailbank_ghana;

-- VIEW 1 
-- vw_loan_summary
-- Live snapshot of every loan: approved, disbursed, collected, remaining

CREATE OR REPLACE VIEW vw_loan_summary AS
SELECT
    l.loan_id,
    c.full_name                                     AS customer_name,
    c.employment_status,
    lp.product_name,
    lp.product_type,
    l.approved_amount,
    COALESCE(SUM(ld.amount), 0)                     AS total_disbursed_GHS,
    ROUND(l.approved_amount - l.outstanding_balance, 2)
                                                    AS total_repaid_GHS,
    l.outstanding_balance,
    l.interest_rate_pct,
    l.tenure_months,
    l.disbursement_date,
    l.maturity_date,
    l.grace_period_end,
    l.status                                        AS loan_status,
    DATEDIFF(l.maturity_date, CURRENT_DATE)         AS days_to_maturity
FROM loans l
JOIN customers     c  ON l.customer_id = c.customer_id
JOIN loan_products lp ON l.product_id  = lp.product_id
LEFT JOIN loan_disbursements ld ON l.loan_id = ld.loan_id
GROUP BY
    l.loan_id, c.full_name, c.employment_status,
    lp.product_name, lp.product_type, l.approved_amount,
    l.outstanding_balance, l.interest_rate_pct, l.tenure_months,
    l.disbursement_date, l.maturity_date, l.grace_period_end, l.status;


-- VIEW 2 
-- vw_overdue_loans
-- All loans with at least one overdue installment — the collections watchlist

CREATE OR REPLACE VIEW vw_overdue_loans AS
SELECT
    l.loan_id,
    c.full_name                                     AS customer_name,
    c.phone,
    c.email,
    c.region,
    lp.product_type,
    lp.product_name,
    COUNT(rs.schedule_id)                           AS overdue_installments,
    SUM(rs.total_due)                               AS total_overdue_GHS,
    MIN(rs.due_date)                                AS earliest_missed_date,
    DATEDIFF(CURRENT_DATE, MIN(rs.due_date))        AS days_since_first_miss,
    l.outstanding_balance,
    CASE
        WHEN DATEDIFF(CURRENT_DATE, MIN(rs.due_date)) <= 30  THEN 'Watch'
        WHEN DATEDIFF(CURRENT_DATE, MIN(rs.due_date)) <= 60  THEN 'Substandard'
        WHEN DATEDIFF(CURRENT_DATE, MIN(rs.due_date)) <= 90  THEN 'Doubtful'
        ELSE 'Loss'
    END                                             AS classification
FROM repayment_schedule rs
JOIN loans         l  ON rs.loan_id    = l.loan_id
JOIN customers     c  ON l.customer_id = c.customer_id
JOIN loan_products lp ON l.product_id  = lp.product_id
WHERE rs.status = 'overdue'
GROUP BY
    l.loan_id, c.full_name, c.phone, c.email, c.region,
    lp.product_type, lp.product_name, l.outstanding_balance;


--  VIEW 3 
-- vw_customer_risk_profile
-- Full customer picture: credit score + active loans + risk flag

CREATE OR REPLACE VIEW vw_customer_risk_profile AS
SELECT
    c.customer_id,
    c.full_name,
    c.employment_status,
    c.monthly_income,
    c.region,
    cs.score                                        AS latest_credit_score,
    cs.rating                                       AS credit_rating,
    cs.assessed_date                                AS score_date,
    COUNT(DISTINCT l.loan_id)                       AS total_active_loans,
    COALESCE(SUM(l.outstanding_balance), 0)         AS total_debt_GHS,
    ROUND(
        COALESCE(SUM(l.outstanding_balance), 0) /
        NULLIF(c.monthly_income * 12, 0) * 100, 2
    )                                               AS debt_to_income_pct,
    COUNT(DISTINCT CASE WHEN rs.status = 'overdue' THEN rs.schedule_id END)
                                                    AS missed_payments,
    c.is_flagged,
    CASE
        WHEN c.is_flagged = 1                       THEN 'FLAGGED'
        WHEN cs.score < 580
          OR COUNT(DISTINCT CASE WHEN rs.status = 'overdue'
                                 THEN rs.schedule_id END) >= 3
        THEN 'HIGH RISK'
        WHEN cs.score BETWEEN 580 AND 669
          OR COUNT(DISTINCT CASE WHEN rs.status = 'overdue'
                                 THEN rs.schedule_id END) BETWEEN 1 AND 2
        THEN 'MEDIUM RISK'
        ELSE 'LOW RISK'
    END                                             AS risk_profile
FROM customers c
LEFT JOIN loans l ON c.customer_id = l.customer_id AND l.status = 'active'
LEFT JOIN repayment_schedule rs ON l.loan_id = rs.loan_id
LEFT JOIN (
    SELECT cs1.customer_id, cs1.score, cs1.rating, cs1.assessed_date
    FROM credit_scores cs1
    WHERE cs1.assessed_date = (
        SELECT MAX(cs2.assessed_date)
        FROM credit_scores cs2
        WHERE cs2.customer_id = cs1.customer_id
    )
) cs ON c.customer_id = cs.customer_id
GROUP BY
    c.customer_id, c.full_name, c.employment_status,
    c.monthly_income, c.region, cs.score, cs.rating,
    cs.assessed_date, c.is_flagged;
