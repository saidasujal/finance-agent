import sqlite3
from datetime import datetime

DB_PATH = 'finance.db'

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_connection()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        amount REAL NOT NULL,
        category TEXT NOT NULL,
        description TEXT,
        date TEXT NOT NULL
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS chat_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        role TEXT NOT NULL,
        message TEXT NOT NULL,
        timestamp TEXT NOT NULL
    )''')
    conn.commit()
    conn.close()

def save_expense(amount, category, description, date):
    conn = get_connection()
    c = conn.cursor()
    c.execute('INSERT INTO expenses (amount, category, description, date) VALUES (?, ?, ?, ?)',
              (amount, category, description, date))
    conn.commit()
    conn.close()

def get_expenses(month, year):
    conn = get_connection()
    c = conn.cursor()
    c.execute('''SELECT amount, category, description, date FROM expenses
                 WHERE strftime('%m', date) = ? AND strftime('%Y', date) = ?
                 ORDER BY date DESC''',
              (f'{month:02d}', str(year)))
    rows = c.fetchall()
    conn.close()
    return [{'amount': r[0], 'category': r[1], 'description': r[2], 'date': r[3]} for r in rows]

def save_chat_message(date, role, message):
    conn = get_connection()
    c = conn.cursor()
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    c.execute('INSERT INTO chat_history (date, role, message, timestamp) VALUES (?, ?, ?, ?)',
              (date, role, message, timestamp))
    conn.commit()
    conn.close()

def get_chat_dates():
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT DISTINCT date FROM chat_history ORDER BY date DESC')
    rows = c.fetchall()
    conn.close()
    return [r[0] for r in rows]

def get_chat_by_date(date):
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT role, message, timestamp FROM chat_history WHERE date = ? ORDER BY timestamp ASC', (date,))
    rows = c.fetchall()
    conn.close()
    return [{'role': r[0], 'message': r[1], 'timestamp': r[2]} for r in rows]

def save_goal(month, year, amount):
    conn = get_connection()
    c = conn.cursor()
    conn.commit()
    conn.close()

def get_goal(month, year):
    return None

def get_spending_by_category(month, year):
    conn = get_connection()
    c = conn.cursor()
    c.execute('''SELECT category, SUM(amount) FROM expenses
                 WHERE strftime('%m', date) = ? AND strftime('%Y', date) = ?
                 GROUP BY category''',
              (f'{month:02d}', str(year)))
    rows = c.fetchall()
    conn.close()
    return {r[0]: r[1] for r in rows}

def get_daily_spending(month, year):
    conn = get_connection()
    c = conn.cursor()
    c.execute('''SELECT strftime('%Y-%m-%d', date), SUM(amount) FROM expenses
                 WHERE strftime('%m', date) = ? AND strftime('%Y', date) = ?
                 GROUP BY strftime('%Y-%m-%d', date)''',
              (f'{month:02d}', str(year)))
    rows = c.fetchall()
    conn.close()
    return {r[0]: r[1] for r in rows}

def export_to_csv(month, year):
    pass
