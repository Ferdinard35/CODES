import sqlite3

DB_NAME = "tracker.db"

def create_connection():
    return sqlite3.connect(DB_NAME)


def init_db():
    with create_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                name TEXT,
                age INTEGER,
                height REAL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                weight REAL,
                waist REAL,
                chest REAL,
                arms REAL,
                bmi REAL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS goals (
                id INTEGER PRIMARY KEY,
                target_weight REAL,
                target_waist REAL,
                target_chest REAL
            )
        """)


# USER
def save_user_profile(name, age, height):
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO users (id, name, age, height)
            VALUES (1, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                name=excluded.name,
                age=excluded.age,
                height=excluded.height
        """, (name, age, height))


def get_user_profile():
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name, age, height FROM users LIMIT 1")
        return cursor.fetchone()


def get_user_height():
    user = get_user_profile()
    return user[2] if user else 0


# ENTRIES
def add_weight_entry(date, weight, waist, chest, arms):
    height_cm = get_user_height()
    bmi = 0

    if height_cm > 0:
        height_m = height_cm / 100  #convert cm → meters
        bmi = round(weight / (height_m ** 2), 2)

    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO entries (date, weight, waist, chest, arms, bmi)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (date, weight, waist, chest, arms, bmi))

def get_latest_entry():
    with create_connection() as conn:
        cursor = conn.cursor()
        # Sort by ID instead of date to guarantee the absolute newest entry shows up
        cursor.execute("SELECT * FROM entries ORDER BY id DESC LIMIT 1")
        return cursor.fetchone()

def get_all_entries():
    """For charts - must be ASCENDING to draw the line correctly"""
    with create_connection() as conn:
        cursor = conn.cursor()
        # Sorting by ID ensures the chart draws from oldest to newest
        cursor.execute("SELECT date, weight FROM entries ORDER BY id ASC")
        return cursor.fetchall()


def get_all_history():
    """For table"""
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM entries ORDER BY date DESC")
        return cursor.fetchall()


def delete_entry(entry_id):
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM entries WHERE id=?", (entry_id,))


# GOALS 
def save_goals(weight, waist, chest):
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO goals (id, target_weight, target_waist, target_chest)
            VALUES (1, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                target_weight=excluded.target_weight,
                target_waist=excluded.target_waist,
                target_chest=excluded.target_chest
        """, (weight, waist, chest))


def get_goals():
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT target_weight, target_waist, target_chest FROM goals LIMIT 1")
        return cursor.fetchone()