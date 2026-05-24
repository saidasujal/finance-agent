import os
import json
from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = os.environ.get('GEMINI_API_KEY', '')
client = genai.Client(api_key=API_KEY)

MODEL_NAME = 'gemini-2.5-flash'

def parse_expense(user_message):
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
        response = client.models.generate_content(model=MODEL_NAME, contents=prompt)
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
    total_spent = sum(e['amount'] for e in expenses)
    remaining = goal - total_spent
    pct = round((total_spent / goal * 100) if goal > 0 else 0, 1)

    system_prompt = f"""
You are a smart Personal Finance AI Agent. Be direct, specific, and use clean text only.

CURRENT DATA:
- Monthly Savings Goal: Rs {goal}
- Total Spent This Month: Rs {total_spent}
- Remaining Budget: Rs {remaining}
- Budget Used: {pct}%
- Expense Details: {expenses}

STRICT RULES:
- DO NOT say "Recorded" or repeat what was just logged — that is already shown to the user
- Always write amounts as "Rs X" not with symbols
- Never use LaTeX or math formatting
- Give specific actionable advice based on actual numbers
- If budget used is under 50% say they are on track
- If budget used is over 80% warn them to slow down
- Mention their top spending category by name
- Keep replies under 4 sentences
- Be conversational, not robotic
- Start directly with the insight, never with a confirmation of the expense
"""
    try:
        context_prompt = f"{system_prompt}\n\nPast Conversation:\n"
        for msg in conversation_history:
            context_prompt += f"{msg['role'].capitalize()}: {msg['content']}\n"
        context_prompt += f"\nUser: {user_message}\nAI:"

        response = client.models.generate_content(model=MODEL_NAME, contents=context_prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Error generating insight: {e}")
        return "I'm having trouble connecting to my AI brain right now. Please try again later."
