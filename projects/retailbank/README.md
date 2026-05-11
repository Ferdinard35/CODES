# RetailBank Ghana — Lending & Credit Risk Database

A MySQL database project that models how a Ghanaian retail bank manages its loans — from the moment someone walks in to apply, all the way to the last repayment or, in the worst case, a default.

I built this to have something real and finance-focused to show on my CV. Not a todo app. Not a student management system. Something that reflects how actual banking data works.

---

## What it does

The database simulates a retail bank (think Ecobank or Fidelity Bank Ghana) that offers four loan products:

- **Personal loans** — for salaried employees who need quick cash
- **Mortgages** — long-term property financing
- **SME loans** — working capital for small businesses
- **Student loans** — low-interest loans with a grace period while studying

It tracks the full lifecycle of every loan: application → approval → disbursement → repayment → closure (or default). Student loans are handled differently — money is released semester by semester, and repayments don't start until after graduation.

---

## Tech stack

- MySQL 8.0
- Python 3 (for generating the seed data)
- MySQL Workbench

---

## The database — 11 tables

I organised the schema into four phases, each representing a stage in the lending process:

```
customers              who is borrowing
credit_scores          their risk score history over time
universities           the 5 institutions supported for student loans
student_profiles       links a student customer to their university and programme

loan_products          the bank's 4 loan products and their rules
loan_applications      every application — approved, rejected, pending, withdrawn

loans                  only approved applications become loans
loan_disbursements     tracks fund releases (semester tranches for student loans)

repayment_schedule     the full payment plan generated upfront for each loan
repayments             actual payments received
audit_log              automatic event log written by triggers, never manually
```

A few design decisions worth mentioning:

- Credit scores are stored as history, not just the latest value. This means you can track whether a borrower's risk profile is improving or getting worse over time.
- Student loan repayment schedules are generated upfront for the full tenure, but rows within the grace period are marked `deferred` from day one. The bank can see future cash flows immediately even before repayments start.
- The `audit_log` table is never written to by hand. Two triggers handle it automatically — one fires on every repayment, one fires when a loan defaults.

---

## The queries

Eight analytical queries that answer real questions a bank analyst would ask:

| # | Question | Main concepts |
|---|---|---|
| 1 | What does each customer still owe? | Aggregation, ratio |
| 2 | Which loans are overdue and by how many days? | DATEDIFF, CASE WHEN |
| 3 | How much has the bank lent out by product type? | GROUP BY, default rate |
| 4 | Which customers are at risk of defaulting? | Correlated subquery, multi-condition logic |
| 5 | What is the monthly repayment collection rate? | DATE_FORMAT, conditional SUM |
| 6 | Which universities have the highest student loan default rates? | Multi-table JOIN |
| 7 | How much has been disbursed vs approved per student? | LEFT JOIN, tranche tracking |
| 8 | Which students are still in grace period vs actively repaying? | CASE, date comparison |

---

## Views

Three reusable views that make reporting much simpler:

- `vw_loan_summary` — a clean snapshot of every loan with balances and status
- `vw_overdue_loans` — the collections watchlist with Bank of Ghana risk classifications (Watch / Substandard / Doubtful / Loss)
- `vw_customer_risk_profile` — full picture of each customer: credit score, debt, missed payments, and an auto-calculated risk label

---

## Triggers

Two automated triggers that write to the audit log without any manual input:

- `trg_after_repayment_insert` — fires every time a payment is recorded. Logs the amount, payment method, and whether it was late.
- `trg_loan_status_change` — fires when a loan is marked as defaulted. Flags the customer automatically and records the outstanding balance at the time of default.

The audit log existing purely from triggers (not manual inserts) means the record can't be accidentally skipped or manipulated by application code.

---

## How to run it

**What you need:**
- MySQL 8.0+ installed locally
- MySQL Workbench
- Python 3.8+

**Step 1 — Create the schema**

Open `schema.sql` in MySQL Workbench and run it. This creates the database and all 11 tables.

**Step 2 — Install the Python dependency**

```bash
pip install mysql-connector-python
```

**Step 3 — Update your credentials**

Open `seed_data.py` and change line 17 to your MySQL root password:

```python
"password": "yourpassword",
```

**Step 4 — Run the seed script**

```bash
python seed_data.py
```

This fills the database with 25 Ghanaian customers, 20 loan applications, disbursements, repayment schedules, and actual payment records.

**Step 5 — Run views, triggers, and queries**

In MySQL Workbench, run in this order:
1. `views.sql`
2. `triggers.sql`
3. `queries.sql` — run each query one at a time to see the results

---

## What the data looks like

- 25 customers with Ghanaian names, Ghana Card numbers, and GHS incomes
- 5 universities: UG, KNUST, Ashesi, UCC, GCTU
- 20 loan applications across all four product types
- 13 approved loans with full repayment histories going back to 2022
- Around 300+ repayment schedule rows — mix of paid, overdue, deferred, and pending
- 80% of past payments on time, 20% late — to make the queries interesting

---

## What I learned building this

Designing the schema took longer than writing any of the queries. Getting the relationships right — especially the student loan grace period logic and the tranche disbursements — required thinking through real banking processes rather than just writing tables.

The triggers were the most satisfying part. Once they were in place, inserting a repayment and watching the audit log update automatically felt like the database was actually alive.

If I were to extend this, I'd add a `staff` table for loan officers, a `collateral` table for secured loans, and stored procedures for automating the monthly overdue status updates.

---

## CV bullet point

> **Retail Banking Loan & Credit Risk Database** · MySQL · Python  
> Designed an 11-table relational database modelling a Ghanaian retail bank's full loan lifecycle across personal, mortgage, SME, and student loan products. Implemented semester-tranche disbursements, deferred repayment schedules for student grace periods, and automated credit risk triggers. Built 8 analytical queries covering portfolio exposure, collection rates, and default risk scoring, alongside 3 reporting views and 2 audit triggers.
