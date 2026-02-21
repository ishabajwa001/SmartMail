# ✉️ SmartMail

AI-powered Gmail client built with **Streamlit** and **Google Gemini**.

SmartMail connects to your Gmail inbox, categorizes emails using AI, generates concise summaries, drafts replies, and helps compose new emails — all from a minimal web interface.

---

## 🚀 Overview

SmartMail is a personal AI email assistant designed for:

- Learning AI integrations
- Practicing API usage
- Demonstrating clean project architecture
- Operating within free-tier limits

This project is intended for **single-user deployment**.

---

## ✨ Features

### 📬 Smart Inbox
- Fetch unread emails via Gmail IMAP
- AI categorization:
  - Important
  - Promotions
  - Updates
  - Others
- AI-generated summaries
- Draft reply suggestions
- Search & filter support
- Bulk delete support
- Attachment download

### ✍️ AI Compose
- Describe email in plain English
- Automatic tone detection
- Draft preview
- Manual editing before sending
- Attachment support

### 🧠 Smart Model Handling
- Auto-detects available Gemini models
- Falls back on quota errors
- Prevents crashes on rate limits

---

## 🧠 Architecture


User → Streamlit UI → Email Utils (IMAP/SMTP) → AI Utils (Gemini API) → Local JSON Storage


Project separation:

- `components/` → UI
- `utils/` → Business logic & integrations
- `.streamlit/` → App configuration

---

## 📂 Project Structure

```text
SmartMail/
├── agent.py                  # Main Streamlit app
├── requirements.txt          # Python dependencies
├── .env.example              # Example environment variables
│
├── components/               # Streamlit UI components
│   ├── inbox.py
│   ├── compose.py
│   └── __init__.py
│
├── utils/                    # Logic & integrations
│   ├── email_utils.py
│   ├── ai_utils.py
│   └── __init__.py
│
├── config/                   # Styling & configuration
│   ├── style.py
│   ├── settings.py
│   └── __init__.py
│
├── data/                     # Local JSON read-state storage
│   └── read_state.json
│
├── .streamlit/               # Streamlit configuration
│   └── config.toml
│
└── README.md
🛠 Tech Stack

Python 3.10+

Streamlit

Google Gemini API (google-generativeai)

Gmail IMAP (fetch emails)

Gmail SMTP (send emails)

python-dotenv

Local JSON storage

🔐 Authentication

SmartMail requires:

Gmail App Password (for IMAP & SMTP)

Google Gemini API Key

⚠️ OAuth is not implemented in this version.

⚠️ Never commit .env or credentials to GitHub.

⚠️ Limitations

Single-user only

No OAuth authentication

Free-tier Gemini rate limits apply

Local JSON resets on cloud restart

Not optimized for large inboxes

🧪 Optimization Techniques

Email body truncation before AI analysis

Model fallback logic

Controlled fetch size

Draft generation on-demand only

▶️ Local Setup
1️⃣ Clone Repository
git clone https://github.com/your-username/SmartMail.git
cd SmartMail
2️⃣ Install Dependencies
pip install -r requirements.txt
3️⃣ Create .env File
EMAIL=your_email@gmail.com
APP_PASSWORD=your_gmail_app_password
GEMINI_API_KEY=your_gemini_api_key
4️⃣ Run App
streamlit run agent.py

Open in browser:

http://localhost:8501
🌍 Deployment (Streamlit Community Cloud)

Push project to GitHub (public repo)

Go to Streamlit Community Cloud

Click "New App"

Select repository

Main file: agent.py

Add credentials in Secrets tab:

EMAIL = "your_email@gmail.com"
APP_PASSWORD = "your_app_password"
GEMINI_API_KEY = "your_api_key"

Click Deploy

👩‍💻 Developed By

Isha Javed
BS Computer Science Student
Pakistan

📜 License

MIT License — Free to use