import sqlite3

DB_NAME = "tracker.db"



# CONNECTION


def create_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row  # cleaner access
    return conn



# INIT DATABASE


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



# USER PROFILE


def save_user_profile(name, age, height):

    with create_connection() as conn:
        conn.execute("""
            INSERT INTO users (id, name, age, height)
            VALUES (1, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                name=excluded.name,
                age=excluded.age,
                height=excluded.height
        """, (name, age, height))


def get_user_profile():

    with create_connection() as conn:
        row = conn.execute("""
            SELECT name, age, height
            FROM users
            WHERE id = 1
        """).fetchone()

        if not row:
            return None

        return dict(row)


def get_user_height():

    user = get_user_profile()

    if not user or not user["height"]:
        return 0

    try:
        return float(user["height"])
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
        conn.execute("""
            INSERT OR REPLACE INTO entries
            (date, weight, waist, chest, arms, bmi)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (date, weight, waist, chest, arms, bmi))


def entry_exists(date):

    with create_connection() as conn:
        row = conn.execute("""
            SELECT 1 FROM entries
            WHERE date = ?
        """, (date,)).fetchone()

        return row is not None


def get_latest_entry():

    with create_connection() as conn:
        row = conn.execute("""
            SELECT weight, bmi
            FROM entries
            ORDER BY id DESC
            LIMIT 1
        """).fetchone()

        if not row:
            return None

        return float(row["weight"]), float(row["bmi"])


def get_latest_measurements():

    with create_connection() as conn:
        row = conn.execute("""
            SELECT waist, chest, arms
            FROM entries
            ORDER BY id DESC
            LIMIT 1
        """).fetchone()

        if not row:
            return None

        return float(row["waist"]), float(row["chest"]), float(row["arms"])


def get_all_entries():

    with create_connection() as conn:
        rows = conn.execute("""
            SELECT date, weight
            FROM entries
            ORDER BY date ASC
        """).fetchall()

        return [(r["date"], r["weight"]) for r in rows]


def get_all_history():

    with create_connection() as conn:
        rows = conn.execute("""
            SELECT id, date, weight, waist, chest, arms, bmi
            FROM entries
            ORDER BY id DESC
        """).fetchall()

        return [
            (
                row["id"],
                row["date"],
                row["weight"],
                row["waist"],
                row["chest"],
                row["arms"],
                row["bmi"]
            )
            for row in rows
        ]


def delete_entry(entry_id):

    with create_connection() as conn:
        conn.execute("""
            DELETE FROM entries
            WHERE id = ?
        """, (entry_id,))



# GOALS


def save_goals(weight, waist, chest):

    with create_connection() as conn:
        conn.execute("""
            INSERT INTO goals
            (id, target_weight, target_waist, target_chest)
            VALUES (1, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                target_weight=excluded.target_weight,
                target_waist=excluded.target_waist,
                target_chest=excluded.target_chest
        """, (weight, waist, chest))


def get_goals():

    with create_connection() as conn:
        row = conn.execute("""
            SELECT target_weight, target_waist, target_chest
            FROM goals
            WHERE id = 1
        """).fetchone()

        if not row:
            return None

        return dict(row)


def get_current_goal():

    return get_goals()