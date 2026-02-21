"""
SmartMail — Entry Point
Supports local (.env) and Streamlit Cloud (st.secrets) deployment.
"""
import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

# Pull secrets from Streamlit Cloud if available, fall back to .env
def _secret(key: str) -> str:
    try:
        return st.secrets.get(key, os.getenv(key, ""))
    except Exception:
        return os.getenv(key, "")

os.environ.setdefault("EMAIL",          _secret("EMAIL"))
os.environ.setdefault("APP_PASSWORD",   _secret("APP_PASSWORD"))
os.environ.setdefault("GEMINI_API_KEY", _secret("GEMINI_API_KEY"))

st.set_page_config(
    page_title="SmartMail",
    page_icon="✉",
    layout="wide",
    initial_sidebar_state="expanded",
)

from config.theme import CSS
from utils.state import init_state
from components.sidebar import render_sidebar
from components.inbox import render_inbox
from components.compose import render_compose
from components.settings import render_settings
from components.support import render_support

st.markdown(CSS, unsafe_allow_html=True)
init_state()

email_addr, app_pass = render_sidebar()
page = st.session_state.current_page

if page == "inbox":
    render_inbox(email_addr, app_pass)
elif page == "compose":
    render_compose(email_addr, app_pass)
elif page == "settings":
    render_settings()
elif page == "support":
    render_support()
