import sqlite3
from decimal import Decimal

from refresh import refresh_manager

DB_NAME = "finance_tracker.db"


# CONNECT TO DATABASE


def connect_db():
    return sqlite3.connect(DB_NAME)


# CREATE TRANSACTIONS TABLE

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

# CREATE BUDGET TABLE


def create_budget_table():

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS budgets (
        month TEXT PRIMARY KEY,
        amount_cents INTEGER NOT NULL
    )
    """)

    conn.commit()
    conn.close()



# ADD TRANSACTION

def add_transaction(date, category, description, amount, trans_type):

    conn = connect_db()
    cursor = conn.cursor()

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

    refresh_manager.data_changed.emit()



# GET ALL TRANSACTIONS


def get_transactions():

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM transactions
    ORDER BY date DESC, id DESC
    """)

    rows = cursor.fetchall()

    conn.close()

    return rows

# GET CURRENT BALANCE


def get_balance():

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT SUM(amount_cents)
    FROM transactions
    WHERE type = 'Income'
    """)

    income = cursor.fetchone()[0]

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

    refresh_manager.data_changed.emit()


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



# UPDATE TRANSACTION


def update_transaction(
    transaction_id,
    date,
    category,
    description,
    amount,
    trans_type
):

    conn = connect_db()
    cursor = conn.cursor()

    amount_cents = int(Decimal(str(amount)) * 100)

    cursor.execute("""
    UPDATE transactions
    SET date = ?,
        category = ?,
        description = ?,
        amount_cents = ?,
        type = ?
    WHERE id = ?
    """, (
        date,
        category,
        description,
        amount_cents,
        trans_type,
        transaction_id
    ))

    conn.commit()
    conn.close()

    refresh_manager.data_changed.emit()



# SEARCH TRANSACTIONS


def search_transactions(search_text="", trans_type="All"):

    conn = connect_db()
    cursor = conn.cursor()

    query = """
    SELECT *
    FROM transactions
    WHERE 1=1
    """

    params = []

    if search_text:

        query += """
        AND (
            category LIKE ?
            OR description LIKE ?
        )
        """

        params.extend([
            f"%{search_text}%",
            f"%{search_text}%"
        ])

    if trans_type != "All":

        query += " AND type = ?"
        params.append(trans_type)

    query += " ORDER BY date DESC"

    cursor.execute(query, params)

    rows = cursor.fetchall()

    conn.close()

    return rows



# EXPORT DATA


def get_all_transactions_for_export():

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        date,
        category,
        description,
        amount_cents,
        type
    FROM transactions
    ORDER BY date DESC
    """)

    rows = cursor.fetchall()

    conn.close()

    return rows

# MONTHLY SUMMARY


def get_monthly_summary():

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        substr(date, 1, 7) AS month,

        SUM(
            CASE
                WHEN type='Income'
                THEN amount_cents
                ELSE 0
            END
        ),

        SUM(
            CASE
                WHEN type='Expense'
                THEN amount_cents
                ELSE 0
            END
        )

    FROM transactions

    GROUP BY month

    ORDER BY month
    """)

    rows = cursor.fetchall()

    conn.close()

    return rows



# SETTINGS


def set_setting(key, value):

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS settings (
        key TEXT PRIMARY KEY,
        value TEXT
    )
    """)

    cursor.execute("""
    INSERT INTO settings (key, value)
    VALUES (?, ?)
    ON CONFLICT(key)
    DO UPDATE SET value=excluded.value
    """, (key, value))

    conn.commit()
    conn.close()


def get_setting(key, default=None):

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS settings (
        key TEXT PRIMARY KEY,
        value TEXT
    )
    """)

    cursor.execute("""
    SELECT value
    FROM settings
    WHERE key=?
    """, (key,))

    row = cursor.fetchone()

    conn.close()

    return row[0] if row else default



# SET BUDGET


def set_budget(month, amount):

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS budgets (
        month TEXT PRIMARY KEY,
        amount_cents INTEGER NOT NULL
    )
    """)

    amount_cents = int(float(amount) * 100)

    cursor.execute("""
    INSERT INTO budgets (month, amount_cents)
    VALUES (?, ?)
    ON CONFLICT(month)
    DO UPDATE SET amount_cents=excluded.amount_cents
    """, (month, amount_cents))

    conn.commit()
    conn.close()

# GET BUDGET


def get_budget(month):

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS budgets (
        month TEXT PRIMARY KEY,
        amount_cents INTEGER NOT NULL
    )
    """)

    cursor.execute("""
    SELECT amount_cents
    FROM budgets
    WHERE month = ?
    """, (month,))

    row = cursor.fetchone()

    conn.close()

    return row[0] if row else 0


# GET MONTH EXPENSES

def get_month_expenses(month):

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT SUM(amount_cents)
    FROM transactions
    WHERE type = 'Expense'
    AND substr(date, 1, 7) = ?
    """, (month,))

    result = cursor.fetchone()[0]

    conn.close()

    return result or 0



# INITIALIZE DATABASE


create_table()
create_budget_table()