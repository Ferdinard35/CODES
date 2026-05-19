import sqlite3
from decimal import Decimal
import hashlib
import os

from refresh import refresh_manager

# =====================
# FIXED DB PATH (VERY IMPORTANT)
# =====================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(BASE_DIR, "finance_tracker.db")


def connect_db():
    return sqlite3.connect(DB_NAME)


# =====================
# INIT TABLES
# =====================
def create_table():
    with connect_db() as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            date TEXT NOT NULL,
            category TEXT NOT NULL,
            description TEXT,
            amount_cents INTEGER NOT NULL,
            type TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
        """)


def create_budget_table():
    with connect_db() as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS budgets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            month TEXT NOT NULL,
            amount_cents INTEGER NOT NULL,
            UNIQUE(user_id, month),
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
        """)


def create_users_table():
    with connect_db() as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
        """)


def create_settings_table():
    with connect_db() as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT
        )
        """)


def column_exists(conn, table_name, column_name):
    columns = conn.execute(f"PRAGMA table_info({table_name})").fetchall()
    return any(column[1] == column_name for column in columns)


def get_first_user_id(conn):
    row = conn.execute("SELECT id FROM users ORDER BY id LIMIT 1").fetchone()
    return row[0] if row else None


def migrate_database():
    with connect_db() as conn:
        if not column_exists(conn, "transactions", "user_id"):
            conn.execute("ALTER TABLE transactions ADD COLUMN user_id INTEGER")
            first_user_id = get_first_user_id(conn)
            if first_user_id:
                conn.execute(
                    "UPDATE transactions SET user_id=? WHERE user_id IS NULL",
                    (first_user_id,)
                )

        if not column_exists(conn, "budgets", "user_id"):
            first_user_id = get_first_user_id(conn)
            conn.execute("ALTER TABLE budgets RENAME TO budgets_old")
            conn.execute("""
            CREATE TABLE budgets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                month TEXT NOT NULL,
                amount_cents INTEGER NOT NULL,
                UNIQUE(user_id, month),
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
            """)
            conn.execute("""
            INSERT INTO budgets (user_id, month, amount_cents)
            SELECT ?, month, amount_cents
            FROM budgets_old
            """, (first_user_id,))
            conn.execute("DROP TABLE budgets_old")


# =====================
# USERS
# =====================
def hash_password(password):
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def register_user(username, password):
    password_hash = hash_password(password)

    try:
        with connect_db() as conn:
            conn.execute("""
            INSERT INTO users (username, password)
            VALUES (?, ?)
            """, (username, password_hash))
        return True
    except sqlite3.IntegrityError:
        return False


def authenticate_user(username, password):
    password_hash = hash_password(password)

    with connect_db() as conn:
        user = conn.execute("""
        SELECT id FROM users
        WHERE username=? AND password=?
        """, (username, password_hash)).fetchone()

    return user is not None


def login_user(username, password):
    password_hash = hash_password(password)

    with connect_db() as conn:
        user = conn.execute("""
        SELECT id, username FROM users
        WHERE username=? AND password=?
        """, (username, password_hash)).fetchone()

    if not user:
        return None

    set_setting("current_user_id", str(user[0]))
    set_setting("current_username", user[1])
    attach_legacy_data_to_user(user[0])
    return {"id": user[0], "username": user[1]}


def get_logged_in_user():
    user_id = get_setting("current_user_id")
    username = get_setting("current_username")

    if not user_id or not username:
        return None

    with connect_db() as conn:
        user = conn.execute("""
        SELECT id, username FROM users
        WHERE id=? AND username=?
        """, (user_id, username)).fetchone()

    if not user:
        logout_user()
        return None

    return {"id": user[0], "username": user[1]}


def is_authenticated():
    return get_logged_in_user() is not None


def logout_user():
    set_setting("current_user_id", "")
    set_setting("current_username", "")


def get_current_user_id():
    user = get_logged_in_user()
    if not user:
        raise PermissionError("Authentication required")
    return user["id"]


def attach_legacy_data_to_user(user_id):
    with connect_db() as conn:
        if column_exists(conn, "transactions", "user_id"):
            conn.execute(
                "UPDATE transactions SET user_id=? WHERE user_id IS NULL",
                (user_id,)
            )

        if column_exists(conn, "budgets", "user_id"):
            conn.execute(
                "UPDATE budgets SET user_id=? WHERE user_id IS NULL",
                (user_id,)
            )


# =====================
# TRANSACTIONS
# =====================
def add_transaction(date, category, description, amount, trans_type):

    amount_cents = int(Decimal(str(amount)) * 100)

    with connect_db() as conn:
        conn.execute("""
        INSERT INTO transactions
        (date, category, description, amount_cents, type)
        VALUES (?, ?, ?, ?, ?)
        """, (date, category, description, amount_cents, trans_type))

    refresh_manager.data_changed.emit()


def get_transactions():
    with connect_db() as conn:
        return conn.execute("""
        SELECT * FROM transactions
        ORDER BY date DESC, id DESC
        """).fetchall()


def get_balance():
    income = _sum_transactions_by_type("Income")
    expenses = _sum_transactions_by_type("Expense")
    return (income - expenses) / 100


def get_total_income():
    return _sum_transactions_by_type("Income") / 100


def get_total_expenses():
    return _sum_transactions_by_type("Expense") / 100


def _sum_transactions_by_type(trans_type):
    with connect_db() as conn:
        result = conn.execute("""
        SELECT SUM(amount_cents)
        FROM transactions
        WHERE type=?
        """, (trans_type,)).fetchone()[0]

    return result or 0


def get_expenses_by_category():
    with connect_db() as conn:
        return conn.execute("""
        SELECT category, SUM(amount_cents)
        FROM transactions
        WHERE type='Expense'
        GROUP BY category
        """).fetchall()


def get_monthly_expenses():
    with connect_db() as conn:
        return conn.execute("""
        SELECT substr(date, 1, 7) AS month,
               SUM(amount_cents)
        FROM transactions
        WHERE type='Expense'
        GROUP BY month
        ORDER BY month
        """).fetchall()


def get_monthly_summary():
    with connect_db() as conn:
        return conn.execute("""
        SELECT
            substr(date, 1, 7) AS month,
            SUM(CASE WHEN type='Income' THEN amount_cents ELSE 0 END),
            SUM(CASE WHEN type='Expense' THEN amount_cents ELSE 0 END)
        FROM transactions
        GROUP BY month
        ORDER BY month
        """).fetchall()


def get_all_transactions_for_export():
    with connect_db() as conn:
        return conn.execute("""
        SELECT date, category, description, amount_cents, type
        FROM transactions
        ORDER BY date DESC, id DESC
        """).fetchall()


def update_transaction(
    transaction_id,
    date,
    category,
    description,
    amount,
    trans_type
):
    amount_cents = int(Decimal(str(amount)) * 100)

    with connect_db() as conn:
        conn.execute("""
        UPDATE transactions
        SET date=?,
            category=?,
            description=?,
            amount_cents=?,
            type=?
        WHERE id=?
        """, (
            date,
            category,
            description,
            amount_cents,
            trans_type,
            transaction_id
        ))

    refresh_manager.data_changed.emit()


# =====================
# FIXED SEARCH (IMPORTANT)
# =====================
def search_transactions(search_text="", trans_type="All"):

    query = "SELECT * FROM transactions WHERE 1=1"
    params = []

    if search_text:
        query += " AND (category LIKE ? OR description LIKE ?)"
        params.extend([f"%{search_text}%", f"%{search_text}%"])

    if trans_type != "All":
        query += " AND LOWER(type)=LOWER(?)"
        params.append(trans_type)

    query += " ORDER BY date DESC, id DESC"

    with connect_db() as conn:
        return conn.execute(query, params).fetchall()


def delete_transaction(transaction_id):
    with connect_db() as conn:
        conn.execute("DELETE FROM transactions WHERE id=?", (transaction_id,))

    refresh_manager.data_changed.emit()


def get_transaction_count():
    with connect_db() as conn:
        return conn.execute("SELECT COUNT(*) FROM transactions").fetchone()[0]


def clear_transactions():
    with connect_db() as conn:
        conn.execute("DELETE FROM transactions")

    refresh_manager.data_changed.emit()


# =====================
# SETTINGS
# =====================
def set_setting(key, value):
    with connect_db() as conn:
        conn.execute("""
        INSERT INTO settings (key, value)
        VALUES (?, ?)
        ON CONFLICT(key)
        DO UPDATE SET value=excluded.value
        """, (key, value))


def get_setting(key, default=None):
    with connect_db() as conn:
        row = conn.execute("""
        SELECT value
        FROM settings
        WHERE key=?
        """, (key,)).fetchone()

    return row[0] if row else default


# =====================
# BUDGETS
# =====================
def set_budget(month, amount):
    amount_cents = int(Decimal(str(amount)) * 100)

    with connect_db() as conn:
        conn.execute("""
        INSERT INTO budgets (month, amount_cents)
        VALUES (?, ?)
        ON CONFLICT(month)
        DO UPDATE SET amount_cents=excluded.amount_cents
        """, (month, amount_cents))


def get_budget(month):
    with connect_db() as conn:
        row = conn.execute("""
        SELECT amount_cents
        FROM budgets
        WHERE month=?
        """, (month,)).fetchone()

    return row[0] if row else 0


def get_month_expenses(month):
    with connect_db() as conn:
        result = conn.execute("""
        SELECT SUM(amount_cents)
        FROM transactions
        WHERE type='Expense'
        AND substr(date, 1, 7)=?
        """, (month,)).fetchone()[0]

    return result or 0


# =====================
# AUTO INIT
# =====================
create_table()
create_budget_table()
create_users_table()
create_settings_table()
