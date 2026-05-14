import sqlite3
from decimal import Decimal

DB_NAME = "finance_tracker.db"



# CONNECT TO DATABASE

def connect_db():
    return sqlite3.connect(DB_NAME)


# CREATE TABLE

def create_table():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        category TEXT NOT NULL,
        description TEXT,
        amount_cents INTEGER NOT NULL,
        type TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()



# ADD TRANSACTION

def add_transaction(date, category, description, amount, trans_type):
    """
    amount should be entered like:
    12.50
    99.99
    """

    conn = connect_db()
    cursor = conn.cursor()

    # Convert to cents
    amount_cents = int(Decimal(str(amount)) * 100)

    cursor.execute("""
    INSERT INTO transactions
    (date, category, description, amount_cents, type)
    VALUES (?, ?, ?, ?, ?)
    """, (
        date,
        category,
        description,
        amount_cents,
        trans_type
    ))

    conn.commit()
    conn.close()



# GET ALL TRANSACTIONS

def get_transactions():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM transactions
    ORDER BY date DESC
    """)

    rows = cursor.fetchall()

    conn.close()

    return rows



# CALCULATE BALANCE

def get_balance():
    conn = connect_db()
    cursor = conn.cursor()

    # Total income
    cursor.execute("""
    SELECT SUM(amount_cents)
    FROM transactions
    WHERE type = 'Income'
    """)

    income = cursor.fetchone()[0]

    # Total expenses
    cursor.execute("""
    SELECT SUM(amount_cents)
    FROM transactions
    WHERE type = 'Expense'
    """)

    expenses = cursor.fetchone()[0]

    conn.close()

    income = income if income else 0
    expenses = expenses if expenses else 0

    balance_cents = income - expenses

    return balance_cents / 100



# DELETE TRANSACTION

def delete_transaction(transaction_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    DELETE FROM transactions
    WHERE id = ?
    """, (transaction_id,))

    conn.commit()
    conn.close()


# TOTAL INCOME

def get_total_income():

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT SUM(amount_cents)
    FROM transactions
    WHERE type = 'Income'
    """)

    result = cursor.fetchone()[0]

    conn.close()

    return (result or 0) / 100



# TOTAL EXPENSES

def get_total_expenses():

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT SUM(amount_cents)
    FROM transactions
    WHERE type = 'Expense'
    """)

    result = cursor.fetchone()[0]

    conn.close()

    return (result or 0) / 100



# RECENT TRANSACTIONS

def get_recent_transactions(limit=5):

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM transactions
    ORDER BY date DESC, id DESC
    LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()

    conn.close()

    return rows
# EXPENSES BY CATEGORY

def get_expenses_by_category():

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT category, SUM(amount_cents)
    FROM transactions
    WHERE type = 'Expense'
    GROUP BY category
    """)

    rows = cursor.fetchall()

    conn.close()

    return rows

# MONTHLY EXPENSES

def get_monthly_expenses():

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT substr(date, 1, 7) AS month,
           SUM(amount_cents)
    FROM transactions
    WHERE type = 'Expense'
    GROUP BY month
    ORDER BY month
    """)

    rows = cursor.fetchall()

    conn.close()

    return rows

# INITIALIZE DATABASE

create_table()