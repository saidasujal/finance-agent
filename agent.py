import os
import json
from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = os.environ.get('GEMINI_API_KEY', '')
client = genai.Client(api_key=API_KEY)

MODEL_NAME = 'gemini-2.5-flash'

def parse_expense(user_message):
    """Extracts amount, category, and description from a user message."""
    prompt = f"""
You are a helpful personal finance assistant.
Analyze the following user input and extract any expense information.
Categories must strictly be one of: Food, Transport, Entertainment, Shopping, Health, Education, Other.
Return ONLY a valid JSON object with the following keys:
- is_expense: boolean (true if it's an expense entry, false otherwise)
- amount: float (the amount spent, or null if not an expense)
- category: string (one of the allowed categories, or null)
- description: string (a short description, or null)

User Input: "{user_message}"
"""
    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )
        text = response.text.strip()
        if text.startswith("```json"):
            text = text[7:]
        if text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
        data = json.loads(text.strip())
        return data
    except Exception as e:
        print(f"Error parsing expense: {e}")
        return {"is_expense": False, "amount": None, "category": None, "description": None}

def generate_insight(expenses, goal, user_message, conversation_history):
    """Generate personalized financial advice with memory of past conversation."""
    system_prompt = f"""
You are a friendly and expert Personal Finance AI Agent.
Your job is to provide helpful, personalized financial advice, answer questions about spending, and offer insights.

Current Month Data:
- Monthly Savings Goal: {goal}
- Total Expenses: {sum(e['amount'] for e in expenses)}
- Details: {expenses}

Conversation Rules:
- Be concise and actionable.
- Reference their spending data or goal when appropriate.
- If they ask about their budget, use the provided numbers.
"""
    try:
        context_prompt = f"{system_prompt}\n\nPast Conversation:\n"
        for msg in conversation_history:
            context_prompt += f"{msg['role'].capitalize()}: {msg['content']}\n"
        context_prompt += f"\nUser: {user_message}\nAI:"

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=context_prompt
        )
        return response.text
    except Exception as e:
        print(f"Error generating insight: {e}")
        return "I'm having trouble connecting to my AI brain right now. Please try again later."