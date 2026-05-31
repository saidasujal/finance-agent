# NexFi — AI Personal Finance Agent

<div align="center">

<img src="bg-finance.png" alt="NexFi Banner" width="350"/>

**A conversational AI finance tracker that understands plain English, logs your expenses, and gives real-time budget insights.**

[![Live Demo](https://img.shields.io/badge/Live%20Demo-finance--agent--wybs.onrender.com-6366f1?style=for-the-badge)](https://finance-agent-wybs.onrender.com)
[![Python](https://img.shields.io/badge/Python-3.14-3776AB?style=for-the-badge&logo=python)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.x-000000?style=for-the-badge&logo=flask)](https://flask.palletsprojects.com)
[![Gemini](https://img.shields.io/badge/Gemini-2.5%20Flash-4285F4?style=for-the-badge&logo=google)](https://ai.google.dev)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-18-336791?style=for-the-badge&logo=postgresql)](https://postgresql.org)

</div>

---

## What Is This?

NexFi is a personal finance AI agent you talk to like a chat app. Instead of filling forms or clicking buttons to log expenses, you just say:

> *"I spent ₹150 on food today"*

The AI parses your message, extracts the amount and category, saves it to the database, and responds with a personalized budget insight — all in one step.

Each user gets a persistent, isolated session via browser localStorage. No login required, no data mixing between users.

---

## Features

- **Conversational expense logging** — type naturally, AI extracts structured data
- **Real-time budget tracking** — live ring chart showing % of monthly goal used
- **AI-powered insights** — Gemini 2.5 Flash analyzes your spending and gives specific advice
- **Category breakdown** — Food, Transport, Entertainment, Shopping, Health, Education, Other
- **Chat history** — browse past conversations by date
- **Monthly goal** — set and persist your budget goal per user per month
- **Multi-user support** — isolated data per browser using UUID identity
- **CSV export** — download your expense data
- **Dark UI** — glassmorphism design with animated background

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | HTML, CSS, JavaScript (Vanilla) |
| Backend | Python, Flask, Flask-CORS |
| AI Model | Google Gemini 2.5 Flash (`google-genai`) |
| Database | PostgreSQL (hosted on Render) |
| DB Driver | psycopg2-binary |
| Deployment | Render (Web Service + PostgreSQL) |

---

## Project Structure

```
finance-agent/
├── app.py              # Flask routes and API endpoints
├── agent.py            # Gemini AI integration (parse + insight)
├── database.py         # PostgreSQL operations (all DB logic)
├── index.html          # Single-page frontend (UI + JS)
├── requirements.txt    # Python dependencies
├── bg-finance.png      # Background asset
├── background.png      # UI asset
├── verify_html.py      # HTML validation script
├── verify_js.js        # JS syntax validation script
└── .gitignore
```

---

## Architecture

```
Browser (index.html)
    │
    │  fetch() with X-User-ID header
    ▼
Flask Backend (app.py)
    │
    ├── agent.py  ──► Google Gemini 2.5 Flash API
    │                   ├── parse_expense()     → extract amount/category
    │                   └── generate_insight()  → budget advice
    │
    └── database.py ──► PostgreSQL (Render)
                          ├── expenses table
                          ├── chat_history table
                          └── goals table
```

### Multi-User Identity Flow

No login system required. Each browser generates a UUID on first visit:

```
First visit → crypto.randomUUID() → saved to localStorage
Every request → sends X-User-ID header → backend filters all DB queries by user_id
Return visit → same UUID from localStorage → same data
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/chat` | Send message, get AI response |
| `GET` | `/expenses` | Get current month expenses |
| `POST` | `/set-goal` | Save monthly budget goal |
| `GET` | `/get-goal` | Fetch saved goal for current month |
| `GET` | `/chat-history` | Get list of past chat dates |
| `GET` | `/chat-history/<date>` | Get messages for a specific date |

All endpoints read `X-User-ID` from request headers to isolate user data.

---

## Database Schema

```sql
CREATE TABLE expenses (
    id SERIAL PRIMARY KEY,
    user_id TEXT,
    amount REAL NOT NULL,
    category TEXT NOT NULL,
    description TEXT,
    date TEXT NOT NULL
);

CREATE TABLE chat_history (
    id SERIAL PRIMARY KEY,
    user_id TEXT,
    date TEXT NOT NULL,
    role TEXT NOT NULL,
    message TEXT NOT NULL,
    timestamp TEXT NOT NULL
);

CREATE TABLE goals (
    id SERIAL PRIMARY KEY,
    user_id TEXT NOT NULL,
    month INT NOT NULL,
    year INT NOT NULL,
    amount REAL NOT NULL
);
```

---

## How the AI Works

Two-step pipeline on every chat message:

**Step 1 — `parse_expense()`**
Sends user message to Gemini. Extracts structured JSON:
```json
{
  "is_expense": true,
  "amount": 150.0,
  "category": "Food",
  "description": "lunch"
}
```

**Step 2 — `generate_insight()`**
If it's an expense, sends full expense history + budget goal to Gemini.
Returns a 2–4 sentence personalized insight like:
> *"You've used 34% of your budget. Food is your top category this month at ₹1,200. You're on track — ₹3,800 still available."*

---

## Local Setup

### Prerequisites
- Python 3.10+
- PostgreSQL (local or hosted)
- Google Gemini API key — [get one here](https://ai.google.dev)

### Steps

```bash
# 1. Clone the repo
git clone https://github.com/SaidaSujal/finance-agent.git
cd finance-agent

# 2. Install dependencies
pip install -r requirements.txt

# 3. Create .env file
touch .env
```

Add to `.env`:
```
GEMINI_API_KEY=your_gemini_api_key_here
DATABASE_URL=postgresql://user:password@host/dbname
```

```bash
# 4. Run the app
python3 app.py
```

Open `http://localhost:5000` in your browser.

### Database Setup

If using a fresh PostgreSQL database, the tables are created automatically on first run via `init_db()`.

If migrating an existing database without `user_id` columns:
```sql
ALTER TABLE expenses ADD COLUMN IF NOT EXISTS user_id TEXT;
ALTER TABLE chat_history ADD COLUMN IF NOT EXISTS user_id TEXT;
```

---

## Deployment (Render)

1. Push code to GitHub
2. Create a new **Web Service** on [Render](https://render.com)
3. Connect your GitHub repo
4. Set environment variables: `GEMINI_API_KEY`, `DATABASE_URL`
5. Build command: *(leave empty)*
6. Start command: `python app.py`
7. Create a **PostgreSQL** instance on Render and link the URL

---

## Expense Categories

| Category | Examples |
|----------|---------|
| Food | Lunch, groceries, coffee |
| Transport | Uber, bus, petrol |
| Entertainment | Movies, games, Netflix |
| Shopping | Clothes, electronics |
| Health | Medicine, gym, doctor |
| Education | Books, courses, stationery |
| Other | Anything else |

---

## Known Limitations

- No authentication — uses localStorage UUID (data tied to browser, not account)
- Clearing browser data resets user identity
- Render free PostgreSQL expires after 90 days
- Single-worker Flask server (not production-grade for high traffic)

---

## Author

**Sujal Saida** — 3rd Year Diploma Student  
Built as a portfolio project exploring AI agent architecture, full-stack development, and conversational UI design.

[![GitHub](https://img.shields.io/badge/GitHub-SaidaSujal-181717?style=flat&logo=github)](https://github.com/SaidaSujal)

---

## License

MIT License — free to use, modify, and distribute.
