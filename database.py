import os
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime

DATABASE_URL = os.environ.get('DATABASE_URL', '')

def get_connection():
    return psycopg2.connect(DATABASE_URL)

def init_db():
    conn = get_connection()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS expenses (
        id SERIAL PRIMARY KEY,
        amount REAL NOT NULL,
        category TEXT NOT NULL,
        description TEXT,
        date TEXT NOT NULL
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS chat_history (
        id SERIAL PRIMARY KEY,
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
    c.execute('INSERT INTO expenses (amount, category, description, date) VALUES (%s, %s, %s, %s)',
              (amount, category, description, date))
    conn.commit()
    conn.close()

def get_expenses(month, year):
    conn = get_connection()
    c = conn.cursor()
    c.execute('''SELECT amount, category, description, date FROM expenses
                 WHERE EXTRACT(MONTH FROM date::timestamp) = %s
                 AND EXTRACT(YEAR FROM date::timestamp) = %s
                 ORDER BY date DESC''',
              (month, year))
    rows = c.fetchall()
    conn.close()
    return [{'amount': r[0], 'category': r[1], 'description': r[2], 'date': r[3]} for r in rows]

def save_chat_message(date, role, message):
    conn = get_connection()
    c = conn.cursor()
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    c.execute('INSERT INTO chat_history (date, role, message, timestamp) VALUES (%s, %s, %s, %s)',
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
    c.execute('SELECT role, message, timestamp FROM chat_history WHERE date = %s ORDER BY timestamp ASC', (date,))
    rows = c.fetchall()
    conn.close()
    return [{'role': r[0], 'message': r[1], 'timestamp': r[2]} for r in rows]

def save_goal(month, year, amount):
    pass

def get_goal(month, year):
    return None

def get_spending_by_category(month, year):
    conn = get_connection()
    c = conn.cursor()
    c.execute('''SELECT category, SUM(amount) FROM expenses
                 WHERE EXTRACT(MONTH FROM date::timestamp) = %s
                 AND EXTRACT(YEAR FROM date::timestamp) = %s
                 GROUP BY category''',
              (month, year))
    rows = c.fetchall()
    conn.close()
    return {r[0]: r[1] for r in rows}

def get_daily_spending(month, year):
    conn = get_connection()
    c = conn.cursor()
    c.execute('''SELECT DATE(date::timestamp), SUM(amount) FROM expenses
                 WHERE EXTRACT(MONTH FROM date::timestamp) = %s
                 AND EXTRACT(YEAR FROM date::timestamp) = %s
                 GROUP BY DATE(date::timestamp)''',
              (month, year))
    rows = c.fetchall()
    conn.close()
    return {str(r[0]): r[1] for r in rows}

def export_to_csv(month, year):
    pass
