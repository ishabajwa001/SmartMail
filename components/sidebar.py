import os
import streamlit as st
import google.generativeai as genai


_GEMINI_PREFERRED = [
    "gemini-2.0-flash-lite",
    "gemini-2.0-flash",
    "gemini-1.5-flash",
    "gemini-1.5-flash-latest",
    "gemini-1.5-flash-8b",
    "gemini-1.5-pro",
    "gemini-pro",
    "gemini-2.5-flash",
]


def render_sidebar() -> tuple[str, str]:
    with st.sidebar:

        # ── Logo
        st.markdown("""
        <div style="padding:1.6rem 1.3rem 1.2rem; border-bottom:1px solid var(--b1);
                    background:linear-gradient(180deg, rgba(61,142,255,0.06), transparent);">
            <div style="display:flex; align-items:center; gap:12px;">
                <div style="width:40px; height:40px; border-radius:10px;
                            background:linear-gradient(135deg,#1b3d85,#0f2260);
                            border:1px solid rgba(61,142,255,0.35);
                            display:flex; align-items:center; justify-content:center;
                            font-size:1.1rem; box-shadow:0 4px 18px rgba(61,142,255,0.22);">
                    ✉
                </div>
                <div>
                    <div style="font-family:'Beiruti',sans-serif; font-size:1.3rem; font-weight:900;
                                color:var(--t1); line-height:1; letter-spacing:-0.02em;">
                        SmartMail
                    </div>
                    <div style="font-family:'Outfit',sans-serif; font-size:0.58rem; font-weight:700;
                                color:var(--t3); letter-spacing:0.16em; text-transform:uppercase; margin-top:3px;">
                        AI Agent
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ── Account Credentials
        st.markdown("<div class='slbl'>Account</div>", unsafe_allow_html=True)

        email_addr = st.text_input("Gmail Address",
                                   value=os.getenv("EMAIL", ""),
                                   placeholder="you@gmail.com",
                                   key="sb_email")
        app_pass   = st.text_input("App Password",
                                   value=os.getenv("APP_PASSWORD", ""),
                                   placeholder="xxxx xxxx xxxx xxxx",
                                   type="password", key="sb_pass")
        gemini_key = st.text_input("Gemini API Key",
                                   value=os.getenv("GEMINI_API_KEY", ""),
                                   placeholder="AIza…",
                                   type="password", key="sb_gem")

        # ── Connection status badge
        if st.session_state.credentials_ok:
            import html as _html
            model_name = _html.escape(st.session_state.get("gemini_model_name", "gemini"))
            st.markdown(
                f"<div class='badge-ok'><span class='dot'></span> Connected &amp; Ready"
                f"<div style='font-size:0.58rem;color:var(--t3);margin-top:2px;'>model: {model_name}</div></div>",
                unsafe_allow_html=True)
        else:
            st.markdown("<div class='badge-err'>○ Not connected yet</div>",
                        unsafe_allow_html=True)

        # ── Connect button
        if st.button("⚡ Connect Account", key="btn_connect"):
            if email_addr and app_pass and gemini_key:
                try:
                    st.session_state.model          = None
                    st.session_state.credentials_ok = False
                    genai.configure(api_key=gemini_key)

                    available = {
                        m.name.split("/")[-1]: m.name
                        for m in genai.list_models()
                        if "generateContent" in getattr(m, "supported_generation_methods", [])
                        and "tts"       not in m.name.lower()
                        and "vision"    not in m.name.lower()
                        and "embedding" not in m.name.lower()
                        and "aqa"       not in m.name.lower()
                        and "preview"   not in m.name.lower()
                    }

                    ordered  = [n for n in _GEMINI_PREFERRED if n in available]
                    ordered += [n for n in available if n not in ordered]

                    if not ordered:
                        st.error("No supported Gemini models found for this API key.")
                    else:
                        chosen = ordered[0]
                        st.session_state.model             = genai.GenerativeModel(chosen)
                        st.session_state.model_fallbacks   = ordered
                        st.session_state.credentials_ok    = True
                        st.session_state.email_addr        = email_addr
                        st.session_state.app_pass          = app_pass
                        st.session_state.gemini_model_name = chosen
                        st.rerun()

                except Exception as e:
                    msg = str(e).lower()
                    if "credentials" in msg or "password" in msg or "auth" in msg:
                        st.error("Connection failed: Invalid credentials. Please check your email address and App Password.")
                    elif "api" in msg or "key" in msg or "quota" in msg:
                        st.error("Connection failed: API key error. Please check your Gemini API key.")
                    elif "network" in msg or "connect" in msg or "timeout" in msg:
                        st.error("Connection failed: Network error. Please check your internet connection.")
                    else:
                        st.error("Connection failed. Please verify your credentials and try again.")
            else:
                st.warning("Please fill in all three fields.")

        # ── Navigation
        st.markdown("<div class='slbl'>Navigate</div>", unsafe_allow_html=True)

        pages  = {
            "📬  Inbox":    "inbox",
            "✍️  Compose":  "compose",
            "⚙️  Settings": "settings",
            "💬  Support":  "support",
        }
        labels = list(pages.keys())
        cur    = st.session_state.current_page
        idx    = list(pages.values()).index(cur) if cur in pages.values() else 0

        selected = st.radio("", labels, index=idx,
                            label_visibility="collapsed", key="nav_radio")
        if pages[selected] != st.session_state.current_page:
            st.session_state.current_page = pages[selected]
            st.rerun()

        # ── Stats (shown after fetch)
        if st.session_state.fetched and st.session_state.emails:
            st.markdown("<div class='slbl'>Stats</div>", unsafe_allow_html=True)

            n    = len(st.session_state.emails)
            cats = list(st.session_state.categories.values())

            st.markdown(f"""
            <div style="margin:0 1rem 0.9rem;
                        background:linear-gradient(135deg, rgba(61,142,255,0.10), rgba(0,217,255,0.06));
                        border:1px solid rgba(61,142,255,0.22);
                        border-radius:10px; padding:0.85rem 1rem; text-align:center;">
                <div style="font-family:'Beiruti',sans-serif; font-size:2.2rem; font-weight:900;
                            color:var(--blue2); line-height:1;">{n}</div>
                <div style="font-family:'Outfit',sans-serif; font-size:0.60rem; font-weight:700;
                            color:var(--t3); text-transform:uppercase; letter-spacing:0.13em; margin-top:4px;">
                    Unread Emails
                </div>
            </div>
            """, unsafe_allow_html=True)

            rows = [
                ("Important",  "var(--coral2)", cats.count("Important")),
                ("Promotions", "var(--blue2)",  cats.count("Promotions")),
                ("Updates",    "var(--cyan2)",  cats.count("Updates")),
                ("Others",     "var(--violet2)",cats.count("Others")),
            ]
            for cat, color, count in rows:
                if count:
                    pct = int(count / n * 100)
                    st.markdown(f"""
                    <div style="padding:4px 1rem 3px;">
                        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;">
                            <span style="font-family:'Outfit',sans-serif; font-size:0.78rem; color:{color}; font-weight:600;">● {cat}</span>
                            <span style="font-family:'JetBrains Mono',monospace; font-size:0.74rem; color:var(--t2); font-weight:500;">{count}</span>
                        </div>
                        <div style="height:3px; background:var(--bg3); border-radius:2px;">
                            <div style="height:3px; width:{pct}%; background:{color}; border-radius:2px; opacity:0.7; transition:width 0.4s ease;"></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

    return email_addr, app_pass
