import os
from dotenv import load_dotenv
load_dotenv()

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from database import init_db, save_expense, get_expenses, get_monthly_expenses
from agent import parse_expense, generate_insight

app = Flask(__name__, static_folder='.')
CORS(app)

init_db()

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '')
    goal = data.get('goal', 5000)
    conversation_history = data.get('conversation_history', [])
    
    expense = parse_expense(user_message)
    
    if expense:
        save_expense(expense['amount'], expense['category'], expense['description'])
        expenses = get_monthly_expenses()
        insight = generate_insight(expenses, goal, user_message, conversation_history)
        return jsonify({
            'type': 'expense',
            'message': f"✅ Recorded ₹{expense['amount']} under {expense['category']}. {insight}",
            'expense': expense
        })
    else:
        expenses = get_monthly_expenses()
        insight = generate_insight(expenses, goal, user_message, conversation_history)
        return jsonify({
            'type': 'insight',
            'message': insight
        })

@app.route('/expenses', methods=['GET'])
def expenses():
    data = get_monthly_expenses()
    return jsonify(data)

@app.route('/set-goal', methods=['POST'])
def set_goal():
    data = request.json
    goal = data.get('goal', 5000)
    return jsonify({'goal': goal})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
