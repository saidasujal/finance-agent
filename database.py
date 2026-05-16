import sqlite3
import csv
import io

DB_NAME = 'finance.db'

def get_connection():
    return sqlite3.connect(DB_NAME)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            description TEXT,
            date TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS goals (
            month INTEGER NOT NULL,
            year INTEGER NOT NULL,
            amount REAL NOT NULL,
            PRIMARY KEY (month, year)
        )
    ''')
    conn.commit()
    conn.close()

def save_expense(amount, category, description, date):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO expenses (amount, category, description, date)
        VALUES (?, ?, ?, ?)
    ''', (amount, category, description, date))
    conn.commit()
    conn.close()

def get_expenses(month, year):
    conn = get_connection()
    cursor = conn.cursor()
    month_str = f"{year}-{month:02d}"
    cursor.execute('''
        SELECT id, amount, category, description, date
        FROM expenses
        WHERE date LIKE ?
    ''', (f"{month_str}%",))
    rows = cursor.fetchall()
    conn.close()
    return [{"id": r[0], "amount": r[1], "category": r[2], "description": r[3], "date": r[4]} for r in rows]

def save_goal(month, year, amount):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO goals (month, year, amount)
        VALUES (?, ?, ?)
    ''', (month, year, amount))
    conn.commit()
    conn.close()

def get_goal(month, year):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT amount FROM goals
        WHERE month = ? AND year = ?
    ''', (month, year))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else 0.0

def get_spending_by_category(month, year):
    conn = get_connection()
    cursor = conn.cursor()
    month_str = f"{year}-{month:02d}"
    cursor.execute('''
        SELECT category, SUM(amount)
        FROM expenses
        WHERE date LIKE ?
        GROUP BY category
    ''', (f"{month_str}%",))
    rows = cursor.fetchall()
    conn.close()
    return {r[0]: r[1] for r in rows}

def get_daily_spending(month, year):
    conn = get_connection()
    cursor = conn.cursor()
    month_str = f"{year}-{month:02d}"
    cursor.execute('''
        SELECT date, SUM(amount)
        FROM expenses
        WHERE date LIKE ?
        GROUP BY date
        ORDER BY date
    ''', (f"{month_str}%",))
    rows = cursor.fetchall()
    conn.close()
    return {r[0]: r[1] for r in rows}

def export_to_csv(month, year):
    expenses = get_expenses(month, year)
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=["id", "amount", "category", "description", "date"])
    writer.writeheader()
    writer.writerows(expenses)
    return output.getvalue()
