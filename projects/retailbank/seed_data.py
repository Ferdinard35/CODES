
from decimal import Decimal
from datetime import date, timedelta
import random
import mysql.connector
import sys
sys.stdout.reconfigure(encoding="utf-8")
"""
RetailBank Ghana — Seed Data Generator
=======================================
Generates and inserts realistic Ghanaian banking data into MySQL.

Requirements:
    pip install mysql-connector-python

Usage:
    1. Make sure MySQL is running locally
    2. Run schema.sql first in MySQL Workbench
    3. Update DB_CONFIG below with your credentials
    4. Run: python seed_data.py
"""


# ── DB CONNECTION ──────────────────────────────────────────────
DB_CONFIG = {
    "host":     "localhost",
    "user":     "root",          # change if different
<<<<<<< HEAD
    "password": "2006Ferdinand?",  
=======
    "password": "2006Ferdinand?",  # ← update this
>>>>>>> 3ccfd545651cc21aeac90d1ec8e347bdb21bf1e6
    "database": "retailbank_ghana"
}

random.seed(42)

# ── GHANAIAN DATA POOLS ────────────────────────────────────────
FIRST_NAMES = [
    "Kwame", "Ama", "Kofi", "Akosua", "Yaw", "Abena", "Kweku", "Efua",
    "Nana", "Adjoa", "Kojo", "Adwoa", "Kwabena", "Afia", "Fiifi", "Maame",
    "Yaa", "Kwasi", "Akua", "Mensah", "Ofori", "Boateng", "Asante", "Darko"
]
LAST_NAMES = [
    "Mensah", "Asante", "Boateng", "Ofori", "Darko", "Owusu", "Amoah",
    "Appiah", "Frimpong", "Acheampong", "Adjei", "Tetteh", "Nkrumah",
    "Quaye", "Ankrah", "Laryea", "Dankwa", "Amponsah", "Kyei", "Bonsu"
]
REGIONS = [
    "Greater Accra", "Ashanti", "Western", "Eastern", "Central",
    "Brong-Ahafo", "Northern", "Volta", "Upper East", "Upper West"
]
EMPLOYERS = [
    "Ghana Health Service", "Cocobod", "Ghana Revenue Authority",
    "Ecobank Ghana", "MTN Ghana", "Vodafone Ghana", "Anglogold Ashanti",
    "Ghana Commercial Bank", "Tullow Oil Ghana", "Stanbic Bank Ghana",
    "Ghana Education Service", "Electricity Company of Ghana",
    "Ghana Water Company", "Bank of Ghana", "Accra Metropolitan Assembly"
]
PROGRAMMES = [
    "BSc Computer Science", "BSc Economics", "BA Accounting",
    "BSc Civil Engineering", "BSc Medicine & Surgery", "BA Law",
    "BSc Business Administration", "BSc Electrical Engineering",
    "BA Communication Studies", "BSc Agriculture"
]
LOAN_PURPOSES = {
    "personal": ["Medical expenses", "Home renovation", "Wedding expenses",
                 "Education support", "Vehicle purchase", "Debt consolidation"],
    "mortgage": ["Purchase of residential property", "Construction of family home",
                 "Renovation of existing property"],
    "sme":      ["Business expansion", "Working capital", "Equipment purchase",
                 "Stock/inventory financing", "Office renovation"],
    "student":  ["Tuition fees and academic expenses"]
}

TODAY = date.today()


def random_date(start: date, end: date) -> date:
    delta = (end - start).days
    if delta <= 0:
        return start
    return start + timedelta(days=random.randint(0, delta))


# Guaranteed unique Ghana Card numbers
_ghana_cards = random.sample(range(100000000, 999999999), 100)
_ghana_card_index = 0


def ghana_card() -> str:
    global _ghana_card_index
    n = _ghana_cards[_ghana_card_index]
    _ghana_card_index += 1
    return f"GHA-{n}-{random.randint(0,9)}"


# Guaranteed unique phone numbers
_phones_used = set()


def phone() -> str:
    prefixes = ["024", "054", "055", "059", "020", "050", "026", "056"]
    while True:
        n = f"{random.choice(prefixes)}{random.randint(1000000,9999999)}"
        if n not in _phones_used:
            _phones_used.add(n)
            return n


def score_to_rating(s):
    if s < 580:
        return "poor"
    if s < 670:
        return "fair"
    if s < 740:
        return "good"
    if s < 800:
        return "very_good"
    return "excellent"


# ══════════════════════════════════════════════════════════════
def seed():
    conn = mysql.connector.connect(**DB_CONFIG)
    cur = conn.cursor()
    print("[OK] Connected to retailbank_ghana\n")

    # ── SAFETY: clear all tables before inserting ──────────────
    print("  [CLEARING] Clearing existing data...")
    cur.execute("SET FOREIGN_KEY_CHECKS = 0")
    for tbl in ["audit_log", "repayments", "repayment_schedule",
                "loan_disbursements", "loans", "loan_applications",
                "loan_products", "student_profiles", "credit_scores",
                "customers", "universities"]:
        cur.execute(f"TRUNCATE TABLE {tbl}")
    cur.execute("SET FOREIGN_KEY_CHECKS = 1")
    conn.commit()
    print("  [DONE] Tables cleared -- starting fresh\n")

    # ── 1. UNIVERSITIES ───────────────────────────────────────
    universities = [
        ("University of Ghana",                  "UG",
         "Legon, Accra",  "Greater Accra"),
        ("Kwame Nkrumah University of Science",
         "KNUST", "Kumasi",        "Ashanti"),
        ("Ashesi University",                    "AU",    "Berekuso",      "Eastern"),
        ("University of Cape Coast",
         "UCC",   "Cape Coast",    "Central"),
        ("Ghana Communication Technology Univ",
         "GCTU",  "Tesano, Accra", "Greater Accra"),
    ]
    cur.executemany(
        "INSERT INTO universities (university_name,abbreviation,location,region) VALUES (%s,%s,%s,%s)",
        universities
    )
    conn.commit()
    print(f"  [OK] Inserted {len(universities)} universities")

    # ── 2. LOAN PRODUCTS ──────────────────────────────────────
    products = [
        ("Salary Advance Personal Loan", "personal", 500,    50000,  3,  60, 24.50,  0,
         "Quick personal loans for salaried employees"),
        ("Home Mortgage Loan",          "mortgage", 50000, 800000, 60, 240, 18.75,  0,
         "Long-term mortgage for property purchase or construction"),
        ("SME Business Loan",           "sme",       2000, 200000,  6,  60, 26.00,  0,
         "Working capital and expansion loans for small businesses"),
        ("Student Education Loan",      "student",   1000,  30000, 12,  96, 12.50, 12,
         "Low-interest student loans with 12-month grace period after graduation"),
    ]
    cur.executemany(
        """INSERT INTO loan_products
           (product_name,product_type,min_amount,max_amount,
            min_tenure_months,max_tenure_months,interest_rate_pct,
            grace_period_months,description)
           VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
        products
    )
    conn.commit()
    cur.execute(
        "SELECT product_id,product_type,interest_rate_pct,grace_period_months FROM loan_products")
    product_rows = cur.fetchall()
    prod_lookup = {ptype: (pid, rate, grace)
                   for pid, ptype, rate, grace in product_rows}
    print(f"  [OK] Inserted {len(products)} loan products")

    # ── 3. CUSTOMERS (25) ─────────────────────────────────────
    emp_pool = (["employed"]*10 + ["self_employed"] *
                7 + ["student"]*6 + ["unemployed"]*2)
    customer_ids = []
    student_customer_ids = []

    for i in range(25):
        emp = emp_pool[i]
        dob = random_date(date(1970, 1, 1), date(2003, 12, 31))
        income = (round(random.uniform(800,  8000), 2) if emp == "employed" else
                  round(random.uniform(500,  5000), 2) if emp == "self_employed" else
                  round(random.uniform(0,     500), 2) if emp == "student" else 0.00)
        employer = (random.choice(EMPLOYERS) if emp == "employed" else
                    "Self-employed" if emp == "self_employed" else None)
        name = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
        cur.execute(
            """INSERT INTO customers
               (full_name,national_id,date_of_birth,gender,phone,email,
                region,employment_status,employer_name,monthly_income)
               VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
            (name, ghana_card(), dob,
             random.choice(["male", "female"]),
             phone(),
             f"{name.lower().replace(' ','.')}{random.randint(1,99)}@gmail.com",
             random.choice(REGIONS), emp, employer, income)
        )
        cid = cur.lastrowid
        customer_ids.append(cid)
        if emp == "student":
            student_customer_ids.append(cid)

    conn.commit()
    print(
        f"  [OK] Inserted 25 customers  ({len(student_customer_ids)} students)")

    # ── 4. CREDIT SCORES ──────────────────────────────────────
    for cid in customer_ids:
        for _ in range(random.randint(1, 3)):
            score = random.randint(320, 820)
            cur.execute(
                """INSERT INTO credit_scores
                   (customer_id,score,rating,assessed_date,assessed_by)
                   VALUES (%s,%s,%s,%s,%s)""",
                (cid, score, score_to_rating(score),
                 random_date(date(2022, 1, 1), date(2024, 6, 1)),
                 "Automated Credit Bureau Pull")
            )
    conn.commit()
    print("  [OK] Inserted credit score records")

    # ── 5. STUDENT PROFILES ───────────────────────────────────
    cur.execute("SELECT university_id FROM universities")
    uni_ids = [r[0] for r in cur.fetchall()]

    for cid in student_customer_ids:
        grad = random_date(date(2025, 6, 1), date(2028, 6, 30))
        cur.execute(
            """INSERT INTO student_profiles
               (customer_id,university_id,programme,level,
                year_of_study,expected_grad_date,student_id_number)
               VALUES (%s,%s,%s,%s,%s,%s,%s)""",
            (cid, random.choice(uni_ids),
             random.choice(PROGRAMMES), "undergraduate",
             random.randint(1, 4), grad,
             f"STU{random.randint(10000,99999)}")
        )
    conn.commit()
    print(f"  [OK] Inserted {len(student_customer_ids)} student profiles")

    # ── 6. LOAN APPLICATIONS & LOANS ─────────────────────────
    # All loans disbursed between 2 and 3 years ago so schedule rows
    # are well in the past and will be marked paid/overdue correctly.
    LOAN_START = date(2022, 1, 1)
    LOAN_END = date(2023, 6, 30)

    statuses = (["approved"]*13 + ["rejected"] *
                4 + ["pending"]*2 + ["withdrawn"]*1)
    random.shuffle(statuses)

    student_loan_customers = set()
    loan_ids = []
    app_count = 0

    for i, status in enumerate(statuses):
        cid = customer_ids[i % len(customer_ids)]
        cur.execute(
            "SELECT employment_status FROM customers WHERE customer_id=%s", (cid,))
        emp_status = cur.fetchone()[0]

        # Pick product type
        if emp_status == "student" and cid not in student_loan_customers:
            ptype = "student"
            student_loan_customers.add(cid)
        elif emp_status in ("employed", "self_employed") and random.random() < 0.25:
            ptype = "sme"
        elif emp_status == "employed" and random.random() < 0.15:
            ptype = "mortgage"
        else:
            ptype = "personal"

        pid, rate, grace = prod_lookup[ptype]

        amount_ranges = {
            "personal": (1000,  40000),
            "mortgage": (60000, 600000),
            "sme":      (5000, 150000),
            "student":  (2000,  25000),
        }
        tenure_ranges = {
            "personal": (12, 36),
            "mortgage": (60, 120),
            "sme":      (12, 36),
            "student":  (24, 60),
        }
        amt = round(random.uniform(*amount_ranges[ptype]), 2)
        tenure = random.randint(*tenure_ranges[ptype])

        applied_date = random_date(LOAN_START, LOAN_END)

        # decided_date always set for non-pending apps
        if status == "pending":
            decided_date = None
            officer = None
        else:
            decided_date = applied_date + timedelta(days=random.randint(3, 14))
            officer = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"

        rejection_reason = (
            random.choice(["Insufficient income", "Poor credit score",
                           "Incomplete documentation", "High debt-to-income ratio"])
            if status == "rejected" else None
        )
        purpose = random.choice(LOAN_PURPOSES[ptype])

        cur.execute(
            """INSERT INTO loan_applications
               (customer_id,product_id,applied_amount,tenure_months,
                purpose,status,applied_date,decided_date,decided_by,rejection_reason)
               VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
            (cid, pid, amt, tenure, purpose, status,
             applied_date, decided_date, officer, rejection_reason)
        )
        app_id = cur.lastrowid
        app_count += 1

        if status == "approved":
            disb_date = decided_date + timedelta(days=random.randint(1, 5))
            mat_date = disb_date + timedelta(days=tenure * 30)
            grace_end = (disb_date + timedelta(days=grace * 30)
                         ) if grace > 0 else None

            cur.execute(
                """INSERT INTO loans
                   (application_id,customer_id,product_id,approved_amount,
                    outstanding_balance,interest_rate_pct,tenure_months,
                    disbursement_date,maturity_date,grace_period_end,status)
                   VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                (app_id, cid, pid, amt, amt, rate, tenure,
                 disb_date, mat_date, grace_end,
                 random.choice(["active", "active", "active", "closed", "defaulted"]))
            )
            loan_id = cur.lastrowid
            loan_ids.append((loan_id, cid, pid, ptype, amt, rate, tenure,
                             disb_date, mat_date, grace_end, grace))

    conn.commit()
    print(
        f"  [OK] Inserted {app_count} loan applications  ({len(loan_ids)} approved → loans)")

    # ── 7. LOAN DISBURSEMENTS ─────────────────────────────────
    modes = ["bank_transfer", "mobile_money", "cheque"]
    for (loan_id, cid, pid, ptype, amt, rate, tenure,
         disb_date, mat_date, grace_end, grace) in loan_ids:

        if ptype == "student":
            num_tranches = random.randint(2, 4)
            tranche_amt = round(amt / num_tranches, 2)
            for t in range(num_tranches):
                t_date = disb_date + timedelta(days=t * 180)
                cur.execute(
                    """INSERT INTO loan_disbursements
                       (loan_id,tranche_number,amount,disbursement_date,
                        disbursement_mode,reference,notes)
                       VALUES (%s,%s,%s,%s,%s,%s,%s)""",
                    (loan_id, t+1, tranche_amt, t_date,
                     random.choice(modes),
                     f"TXN{random.randint(1000000,9999999)}",
                     f"Semester {t+1} disbursement")
                )
        elif ptype == "mortgage" and amt > 200000:
            for t in range(2):
                cur.execute(
                    """INSERT INTO loan_disbursements
                       (loan_id,tranche_number,amount,disbursement_date,
                        disbursement_mode,reference,notes)
                       VALUES (%s,%s,%s,%s,%s,%s,%s)""",
                    (loan_id, t+1, round(amt/2, 2),
                     disb_date + timedelta(days=t*90),
                     "bank_transfer",
                     f"TXN{random.randint(1000000,9999999)}",
                     f"Mortgage tranche {t+1}")
                )
        else:
            cur.execute(
                """INSERT INTO loan_disbursements
                   (loan_id,tranche_number,amount,disbursement_date,
                    disbursement_mode,reference)
                   VALUES (%s,%s,%s,%s,%s,%s)""",
                (loan_id, 1, amt, disb_date,
                 random.choice(modes),
                 f"TXN{random.randint(1000000,9999999)}")
            )
    conn.commit()
    print("  [OK] Inserted disbursement records")

    # ── 8. REPAYMENT SCHEDULES ────────────────────────────────
    schedule_count = 0
    for (loan_id, cid, pid, ptype, amt, rate, tenure,
         disb_date, mat_date, grace_end, grace) in loan_ids:

        monthly_rate = Decimal(str(rate)) / Decimal("100") / Decimal("12")
        d_amt = Decimal(str(amt))

        if monthly_rate == 0:
            emi = d_amt / tenure
        else:
            emi = d_amt * monthly_rate / (1 - (1 + monthly_rate) ** -tenure)
        emi = emi.quantize(Decimal("0.01"))

        for i in range(1, tenure + 1):
            due_date = disb_date + timedelta(days=i * 30)

            interest = (d_amt * monthly_rate).quantize(Decimal("0.01"))
            principal = (emi - interest).quantize(Decimal("0.01"))
            if d_amt - principal < 0:
                principal = d_amt
            d_amt -= principal

            # Determine status
            in_grace = grace_end and due_date <= grace_end

            if in_grace:
                sched_status = "deferred"
            elif due_date < TODAY:
                # Past due dates: 85% paid, 15% overdue — gives rich query results
                sched_status = "paid" if random.random() < 0.85 else "overdue"
            elif due_date <= TODAY + timedelta(days=30):
                sched_status = "pending"
            else:
                sched_status = "pending"

            cur.execute(
                """INSERT INTO repayment_schedule
                   (loan_id,installment_number,due_date,
                    principal_due,interest_due,total_due,status)
                   VALUES (%s,%s,%s,%s,%s,%s,%s)""",
                (loan_id, i, due_date,
                 max(principal, Decimal("0")),
                 max(interest,  Decimal("0")),
                 max(emi,       Decimal("0")),
                 sched_status)
            )
            schedule_count += 1

    conn.commit()
    print(f"  [OK] Inserted {schedule_count} repayment schedule rows")

    # ── 9. REPAYMENTS (actual payments received) ──────────────
    cur.execute(
        """SELECT schedule_id, loan_id, due_date, total_due
           FROM repayment_schedule WHERE status = 'paid'"""
    )
    paid_schedules = cur.fetchall()

    for (sched_id, loan_id, due_date, total_due) in paid_schedules:
        is_late = random.random() < 0.2
        days_late = random.randint(1, 30) if is_late else 0
        pay_date = due_date + timedelta(days=days_late)
        # Keep pay_date in the past
        if pay_date > TODAY:
            pay_date = TODAY

        cur.execute(
            """INSERT INTO repayments
               (loan_id,schedule_id,amount_paid,payment_date,
                payment_mode,reference,is_late,days_late,recorded_by)
               VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
            (loan_id, sched_id, total_due, pay_date,
             random.choice(["bank_transfer", "mobile_money", "cash"]),
             f"PAY{random.randint(1000000,9999999)}",
             int(is_late), days_late,
             f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}")
        )
    conn.commit()
    print(f"  [OK] Inserted {len(paid_schedules)} repayment records")

    cur.close()
    conn.close()
    print("\n[DONE] Seed complete! Your database is ready to query.")
    print("   → Open MySQL Workbench and connect to 'retailbank_ghana'")
    print("   → Run queries.sql to explore your data")


if __name__ == "__main__":
    seed()
