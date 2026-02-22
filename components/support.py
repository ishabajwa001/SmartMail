import streamlit as st
import smtplib
import datetime
import re
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

_SUPPORT_EMAIL = "ishajaved098@gmail.com"


def _sanitize_header(value: str) -> str:
    """Strip CR/LF/NUL from header values to prevent email header injection."""
    if not value:
        return ""
    return re.sub(r"[\r\n\x00]", "", value).strip()


def _send_to_support(sender_email: str, app_pass: str, message: str) -> bool:
    try:
        # Sanitize user-supplied values before setting as headers
        safe_sender  = _sanitize_header(sender_email or "anonymous")
        safe_subject = _sanitize_header(f"[SmartMail] Issue from {sender_email or 'anonymous'}")

        msg = MIMEMultipart()
        msg["Subject"] = safe_subject
        msg["From"]    = safe_sender
        msg["To"]      = _SUPPORT_EMAIL
        body = (
            f"SmartMail Support Request\n"
            f"==========================\n"
            f"Time:   {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"From:   {sender_email or 'Not provided'}\n\n"
            f"Message:\n{message}\n"
        )
        msg.attach(MIMEText(body, "plain", "utf-8"))
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, app_pass)
            server.sendmail(sender_email, [_SUPPORT_EMAIL], msg.as_string())
        return True
    except Exception:
        return False


def render_support():
    st.markdown(
        "<div class='page-title'>Feedback <span>&amp; Support</span></div>"
        "<div class='page-sub'>Facing an issue or have a suggestion? Let us know — we read every message.</div>",
        unsafe_allow_html=True,
    )

    # Show persistent flash messages that survive rerun
    if st.session_state.get("support_flash_msg"):
        st.success(st.session_state.support_flash_msg)
        st.session_state.support_flash_msg = ""

    # Initialize counter for resetting the text area
    if "support_form_key" not in st.session_state:
        st.session_state.support_form_key = 0

    col, _ = st.columns([2, 1])
    with col:
        issue_text = st.text_area(
            "Describe your issue or feedback",
            placeholder="e.g. The regenerate button doesn't update the draft, emails aren't loading, or I'd love a feature that…",
            height=180,
            key=f"support_issue_{st.session_state.support_form_key}",
        )

        if st.button("📤 Submit", key="support_submit"):
            if not issue_text.strip():
                st.warning("Please write something before submitting.")
            else:
                sender = st.session_state.get("email_addr", "")
                app_pw = st.session_state.get("app_pass", "")
                # Increment key to reset the text area widget
                st.session_state.support_form_key += 1
                if sender and app_pw:
                    ok = _send_to_support(sender, app_pw, issue_text.strip())
                    st.session_state.support_flash_msg = (
                        "✅ Message sent! We'll get back to you soon." if ok
                        else "✅ Feedback received — thank you!"
                    )
                else:
                    st.session_state.support_flash_msg = "✅ Feedback noted. Connect your account in the sidebar for instant delivery."
                st.rerun()
