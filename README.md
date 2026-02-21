# ✉ SmartMail

AI-powered Gmail client built with **Streamlit** and **Google Gemini**.  

SmartMail connects to your Gmail inbox, categorizes emails using AI, generates concise summaries, drafts replies, and helps compose new emails in different tones — all from a minimal web interface.

🌐 **Live Demo:** [Open SmartMail]
(https://smartmail-xxgnibyhhxyqj6yqckraqs.streamlit.app/)  

> ⚠️ This version runs on Streamlit Community Cloud.  
> Read-state resets when the app restarts due to local JSON storage.  

---

## 🚀 Overview

SmartMail is designed as a **personal AI email assistant** focused on usability, efficiency, and operating within free-tier API limits.  

This project is intended for **single-user deployment** and **learning purposes**.

---

## ✨ Features

### 📬 Smart Inbox
- Fetch unread emails using Gmail IMAP  
- AI categorizes emails into:
  - Important  
  - Promotions  
  - Updates  
  - Others  
- Generates:
  - Concise AI summary  
  - Ready-to-edit draft reply  
- Persistent read-state (local JSON storage)  
- Search, filter, and sort emails  
- Bulk delete support  
- Attachment download  

### ✍️ AI Compose
- Describe your email in plain English  
- Automatic tone detection  
- Draft preview before sending  
- Manual editing before send  
- File attachment support  

### ⚙️ Smart Model Selection
- Calls `list_models()` on connect  
- Automatically selects the highest free-tier model available  
- Falls back silently if quota is exceeded  
- Prevents crashes or hanging when limits are reached  

---

## 🧠 Architecture


User → Streamlit UI → Email Utils (IMAP/SMTP) → AI Utils (Gemini API) → Local Read State (JSON)


**Project separation:**
- `components/` → UI  
- `utils/` → Business logic & integrations  
- `config/` → Styling & configuration  

---

## 📂 Project Structure


SmartMail/
├── agent.py # Main Streamlit app
├── requirements.txt # Python dependencies
├── .env.example # Example environment variables
├── components/ # Streamlit UI components
│ ├── inbox.py
│ ├── compose.py
│ └── ...
├── utils/ # Logic & integrations
│ ├── email_utils.py
│ ├── ai_utils.py
│ └── ...
├── config/ # Styling & configuration
│ ├── style.py
│ └── settings.py
└── .streamlit/ # Streamlit app configuration
└── config.toml


---

## 🛠 Tech Stack
- Python 3.10+  
- Streamlit  
- Google Gemini (`google-generativeai`)  
- Gmail IMAP (fetch emails)  
- Gmail SMTP (send emails)  
- python-dotenv  
- Local JSON persistence  

---

## 🔐 Authentication

SmartMail uses:  
- Gmail **App Password** (IMAP + SMTP)  
- Google **Gemini API Key**  

> ⚠️ OAuth is not implemented in this version due to cloud billing requirements.  
> Do **not commit** `.env` or credentials to GitHub.  

---

## ⚠️ Limitations
- Designed for single-user use  
- No OAuth authentication  
- Free-tier Gemini rate limits apply  
- Local JSON read-state resets on Streamlit Cloud restart  
- Not optimized for very large inboxes  
- Credentials are stored locally via `.env` or Streamlit secrets  

---

## 🧪 Resource Optimization
- Email body truncation before AI analysis  
- Model fallback logic  
- Controlled email fetch size  
- Draft regeneration only when requested  

---

## ▶️ Setup

### 1️⃣ Clone repository
```bash
git clone https://github.com/your-username/SmartMail.git
cd SmartMail
2️⃣ Install dependencies
pip install -r requirements.txt
3️⃣ Configure environment (Local / Optional)

Create a .env file:

EMAIL=your_email@gmail.com
APP_PASSWORD=your_gmail_app_password
GEMINI_API_KEY=your_gemini_api_key

For Streamlit deployment, use Streamlit Secrets instead of .env.

4️⃣ Run locally
streamlit run agent.py

Open in browser: http://localhost:8501

🌍 Deployment (Streamlit Community Cloud)

Push project to GitHub (public repository)

Go to Streamlit Share

Click New app → select repository → main file: agent.py

Open Secrets tab and add credentials in TOML format:

EMAIL = "your_email@gmail.com"
APP_PASSWORD = "your_app_password"
GEMINI_API_KEY = "your_api_key"

Click Deploy

The app now runs safely without exposing credentials in your repository.

👩‍💻 Developed By

Isha Javed
BS Computer Science Student, Pakistan

📜 License

MIT License — Free to use, modify, and distribute.