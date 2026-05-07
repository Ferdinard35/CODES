-- ============================================================
--  RetailBank Ghana — Lending & Credit Risk Database
--  Schema: 11 Tables
--  Database: MySQL 8.0+
--  Currency: GHS (Ghanaian Cedi)
--  Author: Portfolio Project
-- ============================================================

DROP DATABASE IF EXISTS retailbank_ghana;
CREATE DATABASE retailbank_ghana CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE retailbank_ghana;



-- 1. CUSTOMERS
--    Core borrower profile. Every loan traces back here.
CREATE TABLE customers (
    customer_id       INT AUTO_INCREMENT PRIMARY KEY,
    full_name         VARCHAR(150)    NOT NULL,
    national_id       VARCHAR(20)     UNIQUE NOT NULL,          -- Ghana Card number
    date_of_birth     DATE            NOT NULL,
    gender            ENUM('male','female','other') NOT NULL,
    phone             VARCHAR(15)     NOT NULL,
    email             VARCHAR(150)    UNIQUE,
    region            VARCHAR(50)     NOT NULL,                 -- e.g. Greater Accra, Ashanti
    employment_status ENUM('employed','self_employed','student','unemployed') NOT NULL,
    employer_name     VARCHAR(150),
    monthly_income    DECIMAL(15,2)   NOT NULL DEFAULT 0.00,    -- GHS
    is_flagged        TINYINT(1)      NOT NULL DEFAULT 0,       -- 1 = flagged for risk
    created_at        DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at        DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 2. CREDIT SCORES
--    Score history over time — one record per assessment per customer.
--    Allows tracking how a customer's risk profile changes.
CREATE TABLE credit_scores (
    score_id       INT AUTO_INCREMENT PRIMARY KEY,
    customer_id    INT             NOT NULL,
    score          SMALLINT        NOT NULL,                    -- 300–850 range
    rating         ENUM('poor','fair','good','very_good','excellent') NOT NULL,
    assessed_date  DATE            NOT NULL,
    assessed_by    VARCHAR(100),                               -- officer or system
    notes          TEXT,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE CASCADE,
    INDEX idx_customer_score (customer_id, assessed_date)
);

-- 3. UNIVERSITIES
--    Referenced by student_profiles. Kept separate for clean normalisation.
CREATE TABLE universities (
    university_id   INT AUTO_INCREMENT PRIMARY KEY,
    university_name VARCHAR(200) NOT NULL,
    abbreviation    VARCHAR(20),                               -- e.g. UG, KNUST
    location        VARCHAR(100),
    region          VARCHAR(50)
);

-- 4. STUDENT PROFILES
--    Extra details for customers who are students applying for student loans.
--    One-to-one with customers where applicable.
CREATE TABLE student_profiles (
    profile_id          INT AUTO_INCREMENT PRIMARY KEY,
    customer_id         INT          NOT NULL UNIQUE,
    university_id       INT          NOT NULL,
    programme           VARCHAR(150) NOT NULL,                 -- e.g. BSc Computer Science
    level               ENUM('undergraduate','postgraduate','diploma') NOT NULL,
    year_of_study       TINYINT      NOT NULL,                 -- 1, 2, 3, 4...
    expected_grad_date  DATE         NOT NULL,
    student_id_number   VARCHAR(50),
    FOREIGN KEY (customer_id)   REFERENCES customers(customer_id)   ON DELETE CASCADE,
    FOREIGN KEY (university_id) REFERENCES universities(university_id)
);




-- 5. LOAN PRODUCTS
--    The bank's loan catalogue. Each product has its own rules.
CREATE TABLE loan_products (
    product_id          INT AUTO_INCREMENT PRIMARY KEY,
    product_name        VARCHAR(100)  NOT NULL,
    product_type        ENUM('personal','mortgage','sme','student') NOT NULL,
    min_amount          DECIMAL(15,2) NOT NULL,                -- GHS
    max_amount          DECIMAL(15,2) NOT NULL,                -- GHS
    min_tenure_months   INT           NOT NULL,
    max_tenure_months   INT           NOT NULL,
    interest_rate_pct   DECIMAL(5,2)  NOT NULL,                -- annual %
    grace_period_months INT           NOT NULL DEFAULT 0,      -- student loans > 0
    is_active           TINYINT(1)    NOT NULL DEFAULT 1,
    description         TEXT
);

-- 6. LOAN APPLICATIONS
--    Every application, approved or not. Includes the deciding officer.
CREATE TABLE loan_applications (
    application_id   INT AUTO_INCREMENT PRIMARY KEY,
    customer_id      INT           NOT NULL,
    product_id       INT           NOT NULL,
    applied_amount   DECIMAL(15,2) NOT NULL,                   -- GHS
    tenure_months    INT           NOT NULL,
    purpose          VARCHAR(255),
    status           ENUM('pending','approved','rejected','withdrawn') NOT NULL DEFAULT 'pending',
    applied_date     DATE          NOT NULL,
    decided_date     DATE,
    decided_by       VARCHAR(100),                             -- loan officer name
    rejection_reason VARCHAR(255),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (product_id)  REFERENCES loan_products(product_id),
    INDEX idx_application_status (status),
    INDEX idx_application_customer (customer_id)
);




-- 7. LOANS
--    Only approved applications become loans.
--    Tracks the full lifecycle: active → closed / defaulted.
CREATE TABLE loans (
    loan_id              INT AUTO_INCREMENT PRIMARY KEY,
    application_id       INT           NOT NULL UNIQUE,
    customer_id          INT           NOT NULL,
    product_id           INT           NOT NULL,
    approved_amount      DECIMAL(15,2) NOT NULL,               -- GHS
    outstanding_balance  DECIMAL(15,2) NOT NULL,               -- GHS — updated on repayment
    interest_rate_pct    DECIMAL(5,2)  NOT NULL,               -- locked at approval
    tenure_months        INT           NOT NULL,
    disbursement_date    DATE          NOT NULL,
    maturity_date        DATE          NOT NULL,
    grace_period_end     DATE,                                 -- NULL for non-student loans
    status               ENUM('active','closed','defaulted','deferred') NOT NULL DEFAULT 'active',
    defaulted_at         DATETIME,                             -- set by trigger
    created_at           DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (application_id) REFERENCES loan_applications(application_id),
    FOREIGN KEY (customer_id)    REFERENCES customers(customer_id),
    FOREIGN KEY (product_id)     REFERENCES loan_products(product_id),
    INDEX idx_loan_status   (status),
    INDEX idx_loan_customer (customer_id)
);

-- 8. LOAN DISBURSEMENTS
--    Tracks individual fund releases. For student loans: one per semester.
--    For other loans: typically one lump sum, but supports staged releases (e.g. construction mortgages).
CREATE TABLE loan_disbursements (
    disbursement_id    INT AUTO_INCREMENT PRIMARY KEY,
    loan_id            INT           NOT NULL,
    tranche_number     TINYINT       NOT NULL DEFAULT 1,        -- 1 = first release
    amount             DECIMAL(15,2) NOT NULL,                  -- GHS
    disbursement_date  DATE          NOT NULL,
    disbursement_mode  ENUM('bank_transfer','mobile_money','cheque') NOT NULL DEFAULT 'bank_transfer',
    reference          VARCHAR(100),                            -- bank transaction ref
    notes              VARCHAR(255),
    FOREIGN KEY (loan_id) REFERENCES loans(loan_id) ON DELETE CASCADE,
    INDEX idx_disbursement_loan (loan_id)
);




-- 9. REPAYMENT SCHEDULE
--    Generated upfront for the full loan tenure.
--    Student loan rows within the grace period are marked 'deferred'.
CREATE TABLE repayment_schedule (
    schedule_id        INT AUTO_INCREMENT PRIMARY KEY,
    loan_id            INT           NOT NULL,
    installment_number INT           NOT NULL,                  -- 1, 2, 3...
    due_date           DATE          NOT NULL,
    principal_due      DECIMAL(15,2) NOT NULL,                  -- GHS
    interest_due       DECIMAL(15,2) NOT NULL,                  -- GHS
    total_due          DECIMAL(15,2) NOT NULL,                  -- principal + interest
    status             ENUM('pending','paid','deferred','overdue','waived') NOT NULL DEFAULT 'pending',
    FOREIGN KEY (loan_id) REFERENCES loans(loan_id) ON DELETE CASCADE,
    UNIQUE KEY uq_loan_installment (loan_id, installment_number),
    INDEX idx_schedule_due_date (due_date),
    INDEX idx_schedule_status   (status)
);

-- 10. REPAYMENTS
--     Actual payments received from borrowers.
--     Each payment links to a schedule row and triggers the audit log.
CREATE TABLE repayments (
    repayment_id      INT AUTO_INCREMENT PRIMARY KEY,
    loan_id           INT           NOT NULL,
    schedule_id       INT,                                      -- NULL if unscheduled/early payment
    amount_paid       DECIMAL(15,2) NOT NULL,                   -- GHS
    payment_date      DATE          NOT NULL,
    payment_mode      ENUM('bank_transfer','mobile_money','cash','cheque') NOT NULL,
    reference         VARCHAR(100),
    is_late           TINYINT(1)    NOT NULL DEFAULT 0,         -- 1 = paid after due_date
    days_late         INT           NOT NULL DEFAULT 0,
    recorded_by       VARCHAR(100),
    FOREIGN KEY (loan_id)     REFERENCES loans(loan_id),
    FOREIGN KEY (schedule_id) REFERENCES repayment_schedule(schedule_id),
    INDEX idx_repayment_loan (loan_id),
    INDEX idx_repayment_date (payment_date)
);

-- 11. AUDIT LOG
--     Trigger-powered. Records sensitive events automatically.
--     No manual inserts — everything written by triggers.
CREATE TABLE audit_log (
    log_id        INT AUTO_INCREMENT PRIMARY KEY,
    event_type    VARCHAR(50)  NOT NULL,                        -- e.g. REPAYMENT_RECEIVED, LOAN_DEFAULTED
    table_name    VARCHAR(50)  NOT NULL,
    record_id     INT          NOT NULL,                        -- ID of the affected row
    customer_id   INT,
    loan_id       INT,
    description   TEXT,
    event_time    DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_audit_customer (customer_id),
    INDEX idx_audit_loan     (loan_id),
    INDEX idx_audit_event    (event_type)
);
