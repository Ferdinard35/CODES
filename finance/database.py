import sqlite3
from decimal import Decimal

def create_db():
    conn = sqlite3.connect("finance_tracker.db")
    cursor = conn.cursor()
    
    # creating a transactions table to track every Cedi moving in or out
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            category TEXT NOT NULL,
            description TEXT,
            amount INTEGER NOT NULL,  -- Stored in Pesewas (Amount * 100)
            type TEXT NOT NULL        -- 'Income' or 'Expense'
        )
    ''')
    
    conn.commit()
    conn.close()

def add_transaction(date, category, description, amount, trans_type):
    """
    Saves a transaction. 
    Note: Convert Decimal 'GHS' to Integer 'Pesewas' before saving.
    """
    # Convert GHS (e.g. 50.75) to Pesewas (5075) to avoid floating point errors
    pesewas = int(Decimal(str(amount)) * 100)
    
    conn = sqlite3.connect("finance_tracker.db")
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO transactions (date, category, description, amount, type)
        VALUES (?, ?, ?, ?, ?)
    ''', (date, category, description, pesewas, trans_type))
    conn.commit()
    conn.close()

