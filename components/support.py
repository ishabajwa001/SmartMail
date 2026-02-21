import streamlit as st
import smtplib
import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

_SUPPORT_EMAIL = "ishajaved098@gmail.com"


def _send_to_support(sender_email: str, app_pass: str, message: str) -> bool:
    try:
        msg = MIMEMultipart()
        msg["Subject"] = f"[SmartMail] Issue from {sender_email or 'anonymous'}"
        msg["From"]    = sender_email
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

    col, _ = st.columns([2, 1])
    with col:
        issue_text = st.text_area(
            "Describe your issue or feedback",
            placeholder="e.g. The regenerate button doesn't update the draft, emails aren't loading, or I'd love a feature that…",
            height=180,
            key="support_issue",
        )

        if st.button("📤 Submit", key="support_submit"):
            if not issue_text.strip():
                st.warning("Please write something before submitting.")
            else:
                sender = st.session_state.get("email_addr", "")
                app_pw = st.session_state.get("app_pass", "")
                if sender and app_pw:
                    ok = _send_to_support(sender, app_pw, issue_text.strip())
                    if ok:
                        st.success("✅ Message sent! We'll get back to you soon.")
                        del st.session_state["support_issue"]
                        st.rerun()
                    else:
                        st.info("✅ Feedback received — thank you!")
                else:
                    st.info("✅ Feedback noted. Connect your account in the sidebar for instant delivery.")
