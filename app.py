import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import os
from dotenv import load_dotenv

import database
import agent

# Read secrets from .env (NEVER HARDCODE)
load_dotenv()

# Initialize Database
database.init_db()

st.set_page_config(page_title="Personal Finance Agent", page_icon="💰", layout="wide")

# Initialize session state for memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# Main UI Header
st.title("💰 Personal Finance Agent with Memory")

current_date = datetime.now()
current_month = current_date.month
current_year = current_date.year
current_date_str = current_date.strftime("%Y-%m-%d")

# === Sidebar Configuration ===
st.sidebar.header("Monthly Overview")

# Set Monthly Savings Goal
goal_amount = database.get_goal(current_month, current_year)
new_goal = st.sidebar.number_input("Set Monthly Savings Goal (₹)", min_value=0.0, value=goal_amount, step=100.0)
if new_goal != goal_amount:
    database.save_goal(current_month, current_year, new_goal)
    st.sidebar.success("Goal updated!")
    goal_amount = new_goal

# Summary Data
expenses = database.get_expenses(current_month, current_year)
total_spent = sum(e["amount"] for e in expenses)
remaining_budget = goal_amount - total_spent
percentage_used = (total_spent / goal_amount * 100) if goal_amount > 0 else 0

st.sidebar.subheader("Summary")
st.sidebar.metric("Total Spent", f"₹{total_spent:,.2f}")
st.sidebar.metric("Goal", f"₹{goal_amount:,.2f}")
st.sidebar.metric("Remaining Budget", f"₹{remaining_budget:,.2f}")

# Warning if > 80% budget used
if percentage_used > 80:
    st.sidebar.warning(f"⚠️ You have used {percentage_used:.1f}% of your monthly budget!")
else:
    st.sidebar.info(f"Budget used: {percentage_used:.1f}%")

# Export CSV Button
csv_data = database.export_to_csv(current_month, current_year)
st.sidebar.download_button(
    label="Download Expenses as CSV",
    data=csv_data,
    file_name=f"expenses_{current_year}_{current_month:02d}.csv",
    mime="text/csv"
)

# === Main Layout Dashboard ===
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Spending by Category")
    cat_spending = database.get_spending_by_category(current_month, current_year)
    if cat_spending:
        fig_pie = px.pie(
            values=list(cat_spending.values()), 
            names=list(cat_spending.keys()),
            hole=0.4
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    else:
        st.info("No expenses recorded yet for this month.")

with col2:
    st.subheader("Daily Spending Trend")
    daily_spending = database.get_daily_spending(current_month, current_year)
    if daily_spending:
        df_daily = pd.DataFrame(list(daily_spending.items()), columns=["Date", "Amount"])
        fig_line = px.bar(df_daily, x="Date", y="Amount")
        st.plotly_chart(fig_line, use_container_width=True)
    else:
        st.info("No expenses recorded yet for this month.")

st.divider()

# === Chat Interface ===
st.subheader("Chat with your Finance Agent")

# Render Conversation History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("Type your expense (e.g. 'Spent 500 on Food') or ask a question..."):
    # Render user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Process interaction with Agent
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            # Attempt to parse expense
            parsed_data = agent.parse_expense(prompt)
            
            if parsed_data.get("is_expense") and parsed_data.get("amount") is not None and parsed_data.get("category") is not None:
                amt = parsed_data["amount"]
                cat = parsed_data["category"]
                desc = parsed_data.get("description", "")
                
                # Automatically save expense
                database.save_expense(amt, cat, desc, current_date_str)
                
                response_text = f"✅ Recorded ₹{amt} under {cat} ({desc})."
                st.markdown(response_text)
                st.session_state.messages.append({"role": "assistant", "content": response_text})
                # Refresh page to show updated charts
                st.rerun()
            else:
                # Provide personalized insight / memory processing
                response_text = agent.generate_insight(
                    expenses=database.get_expenses(current_month, current_year),
                    goal=goal_amount,
                    user_message=prompt,
                    conversation_history=st.session_state.messages[:-1]
                )
                st.markdown(response_text)
                st.session_state.messages.append({"role": "assistant", "content": response_text})
