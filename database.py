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
        user_id TEXT,
        amount REAL NOT NULL,
        category TEXT NOT NULL,
        description TEXT,
        date TEXT NOT NULL
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS chat_history (
        id SERIAL PRIMARY KEY,
        user_id TEXT,
        date TEXT NOT NULL,
        role TEXT NOT NULL,
        message TEXT NOT NULL,
        timestamp TEXT NOT NULL
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS goals (
        id SERIAL PRIMARY KEY,
        user_id TEXT NOT NULL,
        month INT NOT NULL,
        year INT NOT NULL,
        amount REAL NOT NULL
    )''')
    conn.commit()
    conn.close()

def save_expense(user_id, amount, category, description, date):
    conn = get_connection()
    c = conn.cursor()
    c.execute('INSERT INTO expenses (user_id, amount, category, description, date) VALUES (%s, %s, %s, %s, %s)',
              (user_id, amount, category, description, date))
    conn.commit()
    conn.close()

def get_expenses(user_id, month, year):
    conn = get_connection()
    c = conn.cursor()
    c.execute('''SELECT amount, category, description, date FROM expenses
                 WHERE user_id = %s
                 AND EXTRACT(MONTH FROM date::timestamp) = %s
                 AND EXTRACT(YEAR FROM date::timestamp) = %s
                 ORDER BY date DESC''',
              (user_id, month, year))
    rows = c.fetchall()
    conn.close()
    return [{'amount': r[0], 'category': r[1], 'description': r[2], 'date': r[3]} for r in rows]

def save_chat_message(user_id, date, role, message):
    conn = get_connection()
    c = conn.cursor()
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    c.execute('INSERT INTO chat_history (user_id, date, role, message, timestamp) VALUES (%s, %s, %s, %s, %s)',
              (user_id, date, role, message, timestamp))
    conn.commit()
    conn.close()

def get_chat_dates(user_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT DISTINCT date FROM chat_history WHERE user_id = %s ORDER BY date DESC', (user_id,))
    rows = c.fetchall()
    conn.close()
    return [r[0] for r in rows]

def get_chat_by_date(user_id, date):
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT role, message, timestamp FROM chat_history WHERE user_id = %s AND date = %s ORDER BY timestamp ASC', (user_id, date))
    rows = c.fetchall()
    conn.close()
    return [{'role': r[0], 'message': r[1], 'timestamp': r[2]} for r in rows]

def save_goal(user_id, month, year, amount):
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT id FROM goals WHERE user_id = %s AND month = %s AND year = %s', (user_id, month, year))
    row = c.fetchone()
    if row:
        c.execute('UPDATE goals SET amount = %s WHERE id = %s', (amount, row[0]))
    else:
        c.execute('INSERT INTO goals (user_id, month, year, amount) VALUES (%s, %s, %s, %s)', (user_id, month, year, amount))
    conn.commit()
    conn.close()

def get_goal(user_id, month, year):
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT amount FROM goals WHERE user_id = %s AND month = %s AND year = %s', (user_id, month, year))
    row = c.fetchone()
    conn.close()
    if row:
        return row[0]
    return 5000

def get_spending_by_category(user_id, month, year):
    conn = get_connection()
    c = conn.cursor()
    c.execute('''SELECT category, SUM(amount) FROM expenses
                 WHERE user_id = %s
                 AND EXTRACT(MONTH FROM date::timestamp) = %s
                 AND EXTRACT(YEAR FROM date::timestamp) = %s
                 GROUP BY category''',
              (user_id, month, year))
    rows = c.fetchall()
    conn.close()
    return {r[0]: r[1] for r in rows}

def get_daily_spending(user_id, month, year):
    conn = get_connection()
    c = conn.cursor()
    c.execute('''SELECT DATE(date::timestamp), SUM(amount) FROM expenses
                 WHERE user_id = %s
                 AND EXTRACT(MONTH FROM date::timestamp) = %s
                 AND EXTRACT(YEAR FROM date::timestamp) = %s
                 GROUP BY DATE(date::timestamp)''',
              (user_id, month, year))
    rows = c.fetchall()
    conn.close()
    return {str(r[0]): r[1] for r in rows}

def export_to_csv(month, year):
    pass
