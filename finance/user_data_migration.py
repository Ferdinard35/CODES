"""
user_data_migration.py
======================
Ensures all transactions and budgets are correctly scoped to the
logged-in user.  Call migrate_to_per_user() once on app start-up
(safe to call repeatedly – it is idempotent).
"""

import database


def migrate_to_per_user():
    """Attach any orphaned rows to the first / current user."""
    database.migrate_database()

    user = database.get_logged_in_user()
    if not user:
        return

    uid = user["id"]

    with database.connect_db() as conn:
        # Transactions with no owner → current user
        conn.execute(
            "UPDATE transactions SET user_id = ? WHERE user_id IS NULL",
            (uid,)
        )
        # Budgets with no owner → current user
        conn.execute(
            "UPDATE budgets SET user_id = ? WHERE user_id IS NULL",
            (uid,)
        )


def get_user_transactions(user_id, search_text="", trans_type="All"):
    """Return transactions belonging only to user_id."""
    query  = "SELECT * FROM transactions WHERE user_id = ?"
    params = [user_id]

    if search_text:
        query  += " AND (category LIKE ? OR description LIKE ?)"
        params += [f"%{search_text}%", f"%{search_text}%"]

    if trans_type != "All":
        query  += " AND LOWER(type) = LOWER(?)"
        params += [trans_type]

    query += " ORDER BY date DESC, id DESC"

    with database.connect_db() as conn:
        return conn.execute(query, params).fetchall()


def get_user_balance(user_id):
    income   = _sum_by_type(user_id, "Income")
    expenses = _sum_by_type(user_id, "Expense")
    return (income - expenses) / 100


def get_user_total_income(user_id):
    return _sum_by_type(user_id, "Income") / 100


def get_user_total_expenses(user_id):
    return _sum_by_type(user_id, "Expense") / 100


def _sum_by_type(user_id, trans_type):
    with database.connect_db() as conn:
        result = conn.execute(
            "SELECT SUM(amount_cents) FROM transactions "
            "WHERE user_id = ? AND type = ?",
            (user_id, trans_type)
        ).fetchone()[0]
    return result or 0


def get_user_budget(user_id, month):
    with database.connect_db() as conn:
        row = conn.execute(
            "SELECT amount_cents FROM budgets WHERE user_id = ? AND month = ?",
            (user_id, month)
        ).fetchone()
    return row[0] if row else 0


def set_user_budget(user_id, month, amount):
    from decimal import Decimal
    cents = int(Decimal(str(amount)) * 100)
    with database.connect_db() as conn:
        conn.execute("""
            INSERT INTO budgets (user_id, month, amount_cents)
            VALUES (?, ?, ?)
            ON CONFLICT(user_id, month)
            DO UPDATE SET amount_cents = excluded.amount_cents
        """, (user_id, month, cents))


def get_user_month_expenses(user_id, month):
    with database.connect_db() as conn:
        result = conn.execute(
            "SELECT SUM(amount_cents) FROM transactions "
            "WHERE user_id = ? AND type = 'Expense' "
            "AND substr(date,1,7) = ?",
            (user_id, month)
        ).fetchone()[0]
    return result or 0
