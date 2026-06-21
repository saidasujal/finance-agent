import os
from dotenv import load_dotenv
load_dotenv()

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from database import (
    init_db,
    save_expense,
    get_expenses,
    save_chat_message,
    get_chat_dates,
    get_chat_by_date,
    save_goal,
    get_goal
)
from agent import parse_expense, generate_insight
from datetime import datetime
import time

app = Flask(__name__, static_folder='.')
CORS(app)

init_db()

@app.route('/')
def index():
    user_id = request.headers.get('X-User-ID', 'anonymous')
    return send_from_directory('.', 'index.html')

@app.route('/<path:filename>')
def serve_asset(filename):
    """Serve static assets (images, CSS, JS) from project directory."""
    user_id = request.headers.get('X-User-ID', 'anonymous')
    allowed_ext = ('.png', '.jpg', '.jpeg', '.gif', '.svg', '.ico', '.css', '.js', '.woff', '.woff2')
    if filename.endswith(allowed_ext):
        return send_from_directory('.', filename)
    return '', 404

@app.route('/chat', methods=['POST'])
def chat():
    user_id = request.headers.get('X-User-ID', 'anonymous')
    data = request.json
    user_message = data.get('message', '')
    goal = data.get('goal', 5000)
    conversation_history = data.get('conversation_history', [])

    now = datetime.now()
    today = now.strftime('%Y-%m-%d')

    # Save user message to history
    save_chat_message(user_id, today, 'user', user_message)

    # Parse expense FIRST — before any DB write
    expense = parse_expense(user_message)

    # Normalize category aliases the AI might return
    CATEGORY_ALIASES = {
        'travel': 'Transport',
        'groceries': 'Food',
        'canteen': 'Food',
        'medicine': 'Health',
        'medical': 'Health',
    }
    if expense and expense.get('category'):
        raw_cat = expense['category'].strip()
        normalized = CATEGORY_ALIASES.get(raw_cat.lower(), raw_cat)
        # Ensure it's in the supported list
        ALLOWED_CATEGORIES = {'Food', 'Transport', 'Entertainment', 'Shopping', 'Health', 'Education', 'Other'}
        expense['category'] = normalized if normalized in ALLOWED_CATEGORIES else 'Other'

    if expense and expense.get('is_expense') and expense.get('amount'):
        # Generate insight BEFORE saving expense
        # This prevents double-save if insight fails
        expenses_before = get_expenses(user_id, now.month, now.year)

        # Retry insight up to 3 times
        insight = None
        for attempt in range(3):
            try:
                # Temporarily add this expense to the list for accurate insight
                temp_expenses = expenses_before + [{
                    'amount': expense['amount'],
                    'category': expense['category'],
                    'description': expense['description'],
                    'date': now.strftime('%Y-%m-%d %H:%M:%S')
                }]
                insight = generate_insight(temp_expenses, goal, user_message, conversation_history)
                if 'trouble connecting' not in insight:
                    break
                if attempt < 2:
                    time.sleep(2)
            except Exception as e:
                print(f"Insight attempt {attempt+1} failed: {e}")
                if attempt < 2:
                    time.sleep(2)

        # Now save the expense (only once, after insight succeeds or all retries done)
        save_expense(
            user_id,
            expense['amount'],
            expense['category'],
            expense['description'],
            now.strftime('%Y-%m-%d %H:%M:%S')
        )

        # Get fresh total after saving
        expenses_after = get_expenses(user_id, now.month, now.year)
        total_spent = sum(e['amount'] for e in expenses_after)

        if insight and 'trouble connecting' not in insight:
            reply = f"✅ Recorded ₹{expense['amount']} under {expense['category']}. {insight}"
        else:
            remaining = goal - total_spent
            pct = round((total_spent / goal * 100) if goal > 0 else 0, 1)
            reply = f"✅ Recorded ₹{expense['amount']} under {expense['category']}. You've spent Rs {total_spent} this month ({pct}% of your Rs {goal} goal). Rs {remaining} remaining."

        save_chat_message(user_id, today, 'ai', reply)
        return jsonify({
            'type': 'expense',
            'message': reply,
            'expense': expense,
            'total_spent': total_spent
        })
    else:
        # Not an expense — generate insight with retry
        expenses = get_expenses(user_id, now.month, now.year)
        insight = None
        for attempt in range(3):
            insight = generate_insight(expenses, goal, user_message, conversation_history)
            if 'trouble connecting' not in insight:
                break
            if attempt < 2:
                time.sleep(2)

        save_chat_message(user_id, today, 'ai', insight)
        return jsonify({'type': 'insight', 'message': insight})

@app.route('/expenses', methods=['GET'])
def expenses():
    user_id = request.headers.get('X-User-ID', 'anonymous')
    now = datetime.now()
    data = get_expenses(user_id, now.month, now.year)
    return jsonify(data)

@app.route('/chat-history', methods=['GET'])
def chat_history():
    user_id = request.headers.get('X-User-ID', 'anonymous')
    dates = get_chat_dates(user_id)
    return jsonify(dates)

@app.route('/chat-history/<date>', methods=['GET'])
def chat_history_by_date(date):
    user_id = request.headers.get('X-User-ID', 'anonymous')
    messages = get_chat_by_date(user_id, date)
    return jsonify(messages)

@app.route('/set-goal', methods=['POST'])
def set_goal():
    user_id = request.headers.get('X-User-ID', 'anonymous')
    data = request.json
    goal = data.get('goal', 5000)
    amount = data.get('amount', goal)
    now = datetime.now()
    save_goal(user_id, now.month, now.year, amount)
    return jsonify({'goal': goal})

@app.route('/get-goal', methods=['GET'])
def get_goal_route():
    user_id = request.headers.get('X-User-ID', 'anonymous')
    now = datetime.now()
    amount = get_goal(user_id, now.month, now.year)
    return jsonify({'goal': amount})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
