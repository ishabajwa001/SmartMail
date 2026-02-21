# ✉ SmartMail — AI-Powered Email Agent

> **Developed by Isha Javed**

SmartMail is a local, privacy-first email client built with **Streamlit** and powered by **Google Gemini**. It connects to your Gmail via IMAP, automatically categorises and summarises every unread email, and drafts intelligent replies — all in a clean dark UI that runs entirely on your machine.

---

## 🚀 Live Demo

> 🔗 **[Click here to try SmartMail live](https://smartmail-xxgnibyhhxyqj6yqckraqs.streamlit.app/)**

---

## ✨ Features

| Feature | Details |
|---|---|
| 📬 **Fetch & Read** | Pulls unread Gmail via IMAP without marking emails as read |
| 🤖 **AI Analysis** | Gemini 2.5 Flash categorises, summarises, and drafts replies |
| ✏️ **Draft Replies** | Editable AI-generated replies, regenerate any time |
| 📤 **Send Email** | Send replies or new emails directly from the app |
| 🗑️ **Delete** | Permanently removes emails from Gmail via IMAP expunge |
| 🔍 **Search & Filter** | Search by sender, subject, or body; sort and group by category/date |
| 📎 **Attachments** | View received attachments, attach files to replies and new emails |
| ✓ **Read Tracking** | Opened emails are visually marked as read |
| 💬 **Support** | Built-in feedback form that emails the developer |

---

## 🗂 Project Structure

```
SmartMail/
├── agent.py                  # Entry point — Streamlit app config & page routing
├── app.py                    # Backwards-compat launcher
├── .env.example              # Template for credentials
│
├── components/
│   ├── sidebar.py            # Account credentials, navigation, stats
│   ├── inbox.py              # Email list, cards, expander, reply panel
│   ├── compose.py            # New email form + AI drafting assistant
│   ├── settings.py           # Setup guide & how-it-works
│   └── support.py            # Feedback form (sends to developer)
│
├── utils/
│   ├── email_utils.py        # IMAP fetch, SMTP send, IMAP delete
│   ├── ai_utils.py           # Gemini prompt, parse category/summary/draft
│   └── state.py              # Streamlit session state initialisation
│
└── config/
    └── theme.py              # Full CSS theme (grey-black, custom fonts)
```

---

## ⚡ Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/username/smartmail.git
cd smartmail
```

### 2. Install dependencies

```bash
pip install streamlit google-generativeai python-dotenv
```

### 3. Set up credentials

Create a `.env` file in the project root:

```env
EMAIL=you@gmail.com
APP_PASSWORD=xxxx xxxx xxxx xxxx
GEMINI_API_KEY=AIzaXXXXXXXXXXXXXXXX
```

### 4. Run

```bash
streamlit run agent.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## 🔐 Gmail App Password Setup

SmartMail uses Gmail's IMAP/SMTP with an **App Password** — not your regular Gmail password.

1. Enable **2-Step Verification** → [myaccount.google.com/security](https://myaccount.google.com/security)
2. Go to **App Passwords** → [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)
3. Choose **Mail → Other device**, name it `SmartMail`
4. Copy the 16-character password into `.env` or the sidebar

Also enable **IMAP** in Gmail:
> Settings → See all settings → Forwarding and POP/IMAP → Enable IMAP

---

## ✦ Gemini API Key

SmartMail uses **Gemini 2.5 Flash** for all AI features. The free tier is sufficient for personal use.

1. Visit [aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)
2. Click **Create API Key**
3. Paste the key into `.env` or the sidebar

---

## 🧠 How It Works

```
Fetch (IMAP)  →  AI Analysis (Gemini)  →  Display + Draft
     ↓                   ↓                       ↓
  UNSEEN emails    Category + Summary      Editable reply
  BODY.PEEK[]      + Draft reply           Send via SMTP
  (stay unread)    per email
```

1. **Fetch** — Connects to Gmail via IMAP SSL. Uses `BODY.PEEK[]` so emails remain unread in Gmail after fetching.
2. **Analyse** — Sends each email to Gemini with strict prompts: category (Important / Promotions / Updates / Others), a 2-sentence summary of only what's actually written, and a draft reply from the recipient's perspective.
3. **Display** — Emails shown as cards with category colour-coding. Opening a card marks it as read locally and shows the full email, AI summary, and editable draft.
4. **Send / Delete** — Replies go via Gmail SMTP. Deletes use IMAP `store +FLAGS \Deleted` + `expunge` to permanently remove from Gmail.

---

## 🖥 Pages

| Page | Description |
|---|---|
| **📬 Inbox** | Fetch, read, reply, and delete emails. Search, sort, and group by category or date. |
| **✍️ Compose** | Write new emails manually or generate a full draft with AI from a brief description. |
| **⚙️ Settings** | Setup instructions, `.env` guide, and how-it-works pipeline explanation. |
| **💬 Support** | Report issues or send feedback directly to the developer. |

---

## 🔒 Privacy

- **Nothing is stored** outside your local Streamlit session. Emails live in memory only for the duration of the session.
- Credentials are never logged or transmitted anywhere except directly to Google (IMAP/SMTP) and Google AI Studio (Gemini API).
- The app runs entirely on your own machine.

---

## 🐛 Troubleshooting

| Problem | Fix |
|---|---|
| `Connection failed` | Check App Password is correct and IMAP is enabled in Gmail |
| Emails not appearing | Click **Fetch Emails** — make sure emails are unread in Gmail |
| AI error | Verify your Gemini API key is valid and has quota remaining |
| Send fails | Confirm SMTP is not blocked by your network or firewall |
| Delete not working | Ensure IMAP is enabled; some networks block port 993 |

---

## 📦 Dependencies

```
streamlit
google-generativeai
python-dotenv
```

Standard library only beyond these: `imaplib`, `smtplib`, `email`, `re`, `datetime`.

---

## 👩‍💻 Developer

<sup>Isha Javed | BSCS</sup>
---

## 📄 License

MIT — use freely, modify as needed.
