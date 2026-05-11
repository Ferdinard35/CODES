
--  RetailBank Ghana — Business Queries
--  8 Real-world analytical questions a credit analyst would ask


USE retailbank_ghana;

--  QUERY 1 
-- What is each customer's total outstanding loan balance?
-- Use case: Daily portfolio exposure report
SELECT
    c.customer_id,
    c.full_name,
    c.employment_status,
    COUNT(l.loan_id)                        AS active_loans,
    SUM(l.outstanding_balance)              AS total_outstanding_GHS,
    SUM(l.approved_amount)                  AS total_approved_GHS,
    ROUND(
        SUM(l.outstanding_balance) /
        NULLIF(SUM(l.approved_amount), 0) * 100, 2
    )                                       AS pct_still_owed
FROM customers c
JOIN loans l ON c.customer_id = l.customer_id
WHERE l.status = 'active'
GROUP BY c.customer_id, c.full_name, c.employment_status
ORDER BY total_outstanding_GHS DESC;


--  QUERY 2
-- Which loans are overdue and by how many days?
-- Use case: Collections team daily watchlist
SELECT
    l.loan_id,
    c.full_name,
    c.phone,
    lp.product_name,
    lp.product_type,
    rs.due_date,
    DATEDIFF(CURRENT_DATE, rs.due_date)     AS days_overdue,
    rs.total_due                            AS amount_overdue_GHS,
    l.outstanding_balance,
    CASE
        WHEN DATEDIFF(CURRENT_DATE, rs.due_date) BETWEEN 1  AND 30  THEN '1–30 days (Watch)'
        WHEN DATEDIFF(CURRENT_DATE, rs.due_date) BETWEEN 31 AND 60  THEN '31–60 days (Substandard)'
        WHEN DATEDIFF(CURRENT_DATE, rs.due_date) BETWEEN 61 AND 90  THEN '61–90 days (Doubtful)'
        WHEN DATEDIFF(CURRENT_DATE, rs.due_date) > 90               THEN '90+ days (Loss)'
    END                                     AS risk_classification
FROM repayment_schedule rs
JOIN loans    l  ON rs.loan_id     = l.loan_id
JOIN customers c ON l.customer_id  = c.customer_id
JOIN loan_products lp ON l.product_id = lp.product_id
WHERE rs.status = 'overdue'
ORDER BY days_overdue DESC;


--  QUERY 3 
-- What is the bank's total loan book exposure by product type?
-- Use case: Executive portfolio summary

SELECT
    lp.product_type,
    lp.product_name,
    COUNT(l.loan_id)                        AS total_loans,
    SUM(l.approved_amount)                  AS total_approved_GHS,
    SUM(l.outstanding_balance)              AS total_outstanding_GHS,
    SUM(l.approved_amount - l.outstanding_balance)
                                            AS total_collected_GHS,
    ROUND(AVG(l.interest_rate_pct), 2)      AS avg_interest_rate_pct,
    SUM(CASE WHEN l.status = 'defaulted' THEN 1 ELSE 0 END)
                                            AS defaulted_loans,
    ROUND(
        SUM(CASE WHEN l.status = 'defaulted' THEN 1 ELSE 0 END) /
        COUNT(l.loan_id) * 100, 2
    )                                       AS default_rate_pct
FROM loans l
JOIN loan_products lp ON l.product_id = lp.product_id
GROUP BY lp.product_type, lp.product_name
ORDER BY total_outstanding_GHS DESC;


--  QUERY 4 
-- Which customers are at highest risk of default?
-- Use case: Credit risk team — early warning system

SELECT
    c.customer_id,
    c.full_name,
    c.employment_status,
    c.monthly_income,
    cs.score                                AS latest_credit_score,
    cs.rating                               AS credit_rating,
    COUNT(DISTINCT l.loan_id)               AS active_loans,
    SUM(l.outstanding_balance)              AS total_debt_GHS,
    ROUND(
        SUM(l.outstanding_balance) /
        NULLIF(c.monthly_income * 12, 0) * 100, 2
    )                                       AS debt_to_annual_income_pct,
    COUNT(DISTINCT CASE WHEN rs.status = 'overdue' THEN rs.schedule_id END)
                                            AS missed_payments,
    CASE
        WHEN cs.score < 580
          OR COUNT(DISTINCT CASE WHEN rs.status = 'overdue' THEN rs.schedule_id END) >= 3
          OR ROUND(SUM(l.outstanding_balance) / NULLIF(c.monthly_income * 12,0) * 100,2) > 60
        THEN 'HIGH RISK'
        WHEN cs.score BETWEEN 580 AND 669
          OR COUNT(DISTINCT CASE WHEN rs.status = 'overdue' THEN rs.schedule_id END) BETWEEN 1 AND 2
        THEN 'MEDIUM RISK'
        ELSE 'LOW RISK'
    END                                     AS risk_flag
FROM customers c
JOIN loans l ON c.customer_id = l.customer_id
JOIN repayment_schedule rs ON l.loan_id = rs.loan_id
JOIN (
    -- Latest credit score per customer
    SELECT cs1.customer_id, cs1.score, cs1.rating
    FROM credit_scores cs1
    WHERE cs1.assessed_date = (
        SELECT MAX(cs2.assessed_date)
        FROM credit_scores cs2
        WHERE cs2.customer_id = cs1.customer_id
    )
) cs ON c.customer_id = cs.customer_id
WHERE l.status = 'active'
GROUP BY c.customer_id, c.full_name, c.employment_status,
         c.monthly_income, cs.score, cs.rating
ORDER BY missed_payments DESC, cs.score ASC;

--  QUERY 5 
-- What is the monthly repayment collection rate?
-- Use case: Finance team — monthly performance report

SELECT
    DATE_FORMAT(rs.due_date, '%Y-%m')       AS month,
    COUNT(rs.schedule_id)                   AS installments_due,
    SUM(rs.total_due)                       AS total_due_GHS,
    SUM(CASE WHEN rs.status = 'paid' THEN rs.total_due ELSE 0 END)
                                            AS total_collected_GHS,
    SUM(CASE WHEN rs.status = 'overdue' THEN rs.total_due ELSE 0 END)
                                            AS total_overdue_GHS,
    ROUND(
        SUM(CASE WHEN rs.status = 'paid' THEN rs.total_due ELSE 0 END) /
        NULLIF(SUM(rs.total_due), 0) * 100, 2
    )                                       AS collection_rate_pct
FROM repayment_schedule rs
WHERE rs.status != 'deferred'
GROUP BY month
ORDER BY month DESC;


--  QUERY 6 
-- Which universities have the highest student loan default rates?
-- Use case: Student loan product risk review

SELECT
    u.university_name,
    u.abbreviation,
    COUNT(DISTINCT l.loan_id)               AS total_student_loans,
    SUM(l.approved_amount)                  AS total_disbursed_GHS,
    SUM(CASE WHEN l.status = 'defaulted' THEN 1 ELSE 0 END)
                                            AS defaulted_loans,
    ROUND(
        SUM(CASE WHEN l.status = 'defaulted' THEN 1 ELSE 0 END) /
        NULLIF(COUNT(DISTINCT l.loan_id), 0) * 100, 2
    )                                       AS default_rate_pct,
    ROUND(AVG(cs.score), 0)                 AS avg_credit_score
FROM universities u
JOIN student_profiles sp ON u.university_id = sp.university_id
JOIN loans l  ON sp.customer_id = l.customer_id
JOIN loan_products lp ON l.product_id = lp.product_id AND lp.product_type = 'student'
LEFT JOIN (
    SELECT customer_id, AVG(score) AS score
    FROM credit_scores
    GROUP BY customer_id
) cs ON sp.customer_id = cs.customer_id
GROUP BY u.university_id, u.university_name, u.abbreviation
ORDER BY default_rate_pct DESC;


--  QUERY 7 
-- How much has been disbursed vs approved per student loan? (Tranche tracking)
-- Use case: Student loan disbursement control

SELECT
    c.full_name,
    sp.programme,
    u.abbreviation                          AS university,
    sp.expected_grad_date,
    l.loan_id,
    l.approved_amount,
    COUNT(ld.disbursement_id)               AS tranches_released,
    COALESCE(SUM(ld.amount), 0)             AS total_disbursed_GHS,
    ROUND(l.approved_amount -
          COALESCE(SUM(ld.amount), 0), 2)   AS remaining_to_disburse_GHS,
    ROUND(
        COALESCE(SUM(ld.amount), 0) /
        NULLIF(l.approved_amount, 0) * 100, 2
    )                                       AS pct_disbursed,
    CASE
        WHEN l.grace_period_end >= CURRENT_DATE THEN 'In Grace Period'
        WHEN l.grace_period_end <  CURRENT_DATE THEN 'Repaying'
        ELSE 'N/A'
    END                                     AS repayment_stage
FROM loans l
JOIN customers c        ON l.customer_id      = c.customer_id
JOIN student_profiles sp ON c.customer_id     = sp.customer_id
JOIN universities u      ON sp.university_id  = u.university_id
JOIN loan_products lp    ON l.product_id      = lp.product_id
LEFT JOIN loan_disbursements ld ON l.loan_id  = ld.loan_id
WHERE lp.product_type = 'student'
GROUP BY c.full_name, sp.programme, u.abbreviation,
         sp.expected_grad_date, l.loan_id,
         l.approved_amount, l.grace_period_end
ORDER BY pct_disbursed ASC;


-- QUERY 8 
-- Which students are in grace period vs actively repaying?
-- Use case: Student loan lifecycle monitoring

SELECT
    c.full_name,
    u.abbreviation                          AS university,
    sp.programme,
    sp.year_of_study,
    sp.expected_grad_date,
    l.loan_id,
    l.approved_amount,
    l.grace_period_end,
    CASE
        WHEN l.grace_period_end >= CURRENT_DATE
        THEN DATEDIFF(l.grace_period_end, CURRENT_DATE)
        ELSE 0
    END                                     AS days_left_in_grace,
    COUNT(CASE WHEN rs.status = 'deferred' THEN 1 END)
                                            AS deferred_installments,
    COUNT(CASE WHEN rs.status = 'paid'    THEN 1 END)
                                            AS paid_installments,
    COUNT(CASE WHEN rs.status = 'overdue' THEN 1 END)
                                            AS overdue_installments,
    CASE
        WHEN l.grace_period_end >= CURRENT_DATE THEN '📚 Grace Period'
        WHEN l.status = 'defaulted'             THEN '🔴 Defaulted'
        WHEN l.status = 'closed'                THEN '✅ Fully Repaid'
        ELSE '💳 Actively Repaying'
    END                                     AS loan_stage
FROM loans l
JOIN customers c         ON l.customer_id     = c.customer_id
JOIN student_profiles sp ON c.customer_id     = sp.customer_id
JOIN universities u       ON sp.university_id = u.university_id
JOIN loan_products lp     ON l.product_id     = lp.product_id
LEFT JOIN repayment_schedule rs ON l.loan_id  = rs.loan_id
WHERE lp.product_type = 'student'
GROUP BY c.full_name, u.abbreviation, sp.programme,
         sp.year_of_study, sp.expected_grad_date,
         l.loan_id, l.approved_amount, l.grace_period_end, l.status
ORDER BY days_left_in_grace DESC;
