import sqlite3

DB_NAME = "tracker.db"



# CONNECTION
def create_connection():
    return sqlite3.connect(DB_NAME)



# INIT DB

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
                date TEXT UNIQUE,
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

        conn.commit()



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

        conn.commit()


def get_user_profile():
    with create_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT name, age, height FROM users LIMIT 1")
        return cursor.fetchone()


def get_user_height():
    user = get_user_profile()

    try:
        return float(user[2]) if user and user[2] else 0
    except:
        return 0



# ENTRIES

def add_weight_entry(date, weight, waist, chest, arms):
    height_cm = get_user_height()
    bmi = 0

    if height_cm > 0:
        height_m = height_cm / 100
        bmi = round(weight / (height_m ** 2), 2)

    with create_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
            INSERT OR REPLACE INTO entries
            (date, weight, waist, chest, arms, bmi)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (date, weight, waist, chest, arms, bmi))

        conn.commit()


def entry_exists(date):
    with create_connection() as conn:
        cursor = conn.cursor()

        cursor.execute(
            "SELECT 1 FROM entries WHERE date = ? LIMIT 1",
            (date,)
        )

        return cursor.fetchone() is not None


def get_latest_entry():
    with create_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT weight, bmi
            FROM entries
            ORDER BY id DESC
            LIMIT 1
        """)

        return cursor.fetchone()


def get_latest_measurements():
    with create_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT waist, chest, arms
            FROM entries
            ORDER BY id DESC
            LIMIT 1
        """)

        return cursor.fetchone()


def get_all_entries():
    with create_connection() as conn:
        cursor = conn.cursor()

        # FIX: order by date instead of id (IMPORTANT FOR CHART)
        cursor.execute("""
            SELECT date, weight
            FROM entries
            ORDER BY date ASC
        """)

        return cursor.fetchall()


def get_all_history():
    with create_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM entries
            ORDER BY id DESC
        """)

        return cursor.fetchall()


def delete_entry(entry_id):
    with create_connection() as conn:
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM entries WHERE id=?",
            (entry_id,)
        )

        conn.commit()



# GOALS

def save_goals(weight, waist, chest):
    with create_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO goals
            (id, target_weight, target_waist, target_chest)
            VALUES (1, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                target_weight=excluded.target_weight,
                target_waist=excluded.target_waist,
                target_chest=excluded.target_chest
        """, (weight, waist, chest))

        conn.commit()


def get_goals():
    with create_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT target_weight, target_waist, target_chest
            FROM goals
            LIMIT 1
        """)

        return cursor.fetchone()


# FIXED: consistent return (VERY IMPORTANT)
def get_current_goal():
    goals = get_goals()

    if not goals:
        return None

    return {
        "weight": goals[0],
        "waist": goals[1],
        "chest": goals[2]
    }