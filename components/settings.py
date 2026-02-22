import streamlit as st


def render_settings():
    st.markdown(
        "<div class='page-title'>Settings <span>&amp; Help</span></div>"
        "<div class='page-sub'>Everything you need to get SmartMail running in minutes.</div>",
        unsafe_allow_html=True,
    )

    # Row 1
    c1, c2 = st.columns(2, gap="large")
    with c1:
        st.markdown("""
        <div class='set-card'>
            <h4>🔐 Gmail App Password</h4>
            <p>You need an <strong>App Password</strong>, not your regular Gmail password.
               Requires 2-Step Verification to be enabled on your Google account.</p>
            <ol>
                <li>Enable <strong>2-Step Verification</strong> at
                    <a href='https://myaccount.google.com/security' target='_blank'>myaccount.google.com/security</a></li>
                <li>Go to
                    <a href='https://myaccount.google.com/apppasswords' target='_blank'>myaccount.google.com/apppasswords</a></li>
                <li>Choose <em>Mail → Other device</em> — name it <code>SmartMail</code></li>
                <li>Copy the 16-character password → paste into the sidebar</li>
            </ol>
            <p style="margin-top:0.85rem; padding:0.7rem 0.9rem;
                      background:rgba(0,217,255,0.06); border:1px solid rgba(0,217,255,0.20);
                      border-radius:8px; font-size:0.86rem; color:var(--t2);">
                💡 Also enable <strong>IMAP</strong> in Gmail:
                <em>Settings → See all settings → Forwarding and POP/IMAP → Enable IMAP</em>
            </p>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class='set-card'>
            <h4>✦ Gemini API Key</h4>
            <p>Use Google's <strong>Gemini</strong> models — generous free tier, great for personal use.</p>
            <ol>
                <li>Visit <a href='https://aistudio.google.com/app/apikey' target='_blank'>aistudio.google.com/app/apikey</a></li>
                <li>Click <strong>Create API Key</strong></li>
                <li>Select or create a Google Cloud project</li>
                <li>Copy the key → paste into the sidebar under <em>Gemini API Key</em></li>
            </ol>
            <p style="margin-top:0.85rem; padding:0.7rem 0.9rem;
                      background:rgba(155,109,255,0.06); border:1px solid rgba(155,109,255,0.20);
                      border-radius:8px; font-size:0.86rem; color:var(--t2);">
                💡 The <strong>free tier</strong> includes generous limits — no billing required to start.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

    # Row 2
    c3, c4 = st.columns(2, gap="large")
    with c3:
        st.markdown("""
        <div class='set-card'>
            <h4>📄 Optional .env File</h4>
            <p>Create a <code>.env</code> file next to <code>agent.py</code> to auto-fill your
               credentials at startup — no typing each session.</p>
            <div class='code-block'><span class='cb-comment'># .env — place next to agent.py</span>
<span class='cb-key'>EMAIL</span>=<span class='cb-value'>you@gmail.com</span>
<span class='cb-key'>APP_PASSWORD</span>=<span class='cb-value'>xxxx xxxx xxxx xxxx</span>
<span class='cb-key'>GEMINI_API_KEY</span>=<span class='cb-value'>AIzaXXXXXXXXXXXXXXXX</span></div>
        </div>
        """, unsafe_allow_html=True)

    with c4:
        st.markdown("""
        <div class='set-card'>
            <h4>🚀 Running SmartMail</h4>
            <p>Install the required packages and launch from your terminal.
               Requires <strong>Python 3.10+</strong>.</p>
            <div class='code-block'><span class='cb-comment'># Step 1 — Install dependencies</span>
<span class='cb-cmd'>pip install</span> <span class='cb-flag'>streamlit google-generativeai python-dotenv</span>

<span class='cb-comment'># Step 2 — Launch the app</span>
<span class='cb-cmd'>streamlit run</span> <span class='cb-flag'>agent.py</span></div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:0.6rem'></div>", unsafe_allow_html=True)
    st.divider()

    # How It Works
    st.markdown("""
    <div style='margin-bottom:1.4rem;'>
        <div style='font-family:"Outfit",sans-serif; font-size:0.68rem; font-weight:700;
                    color:var(--t2); text-transform:uppercase; letter-spacing:0.15em;
                    margin-bottom:0.4rem;'>✦ Agent Pipeline</div>
        <div style='font-family:"Beiruti",sans-serif; font-size:1.9rem; font-weight:800;
                    color:var(--t1); line-height:1.1;'>Three steps from inbox to insight</div>
    </div>
    """, unsafe_allow_html=True)

    s1, s2, s3 = st.columns(3, gap="medium")
    with s1:
        st.markdown("""
        <div class='step-card s-blue'>
            <div class='step-num' style='color:var(--blue2);'>01 — Fetch</div>
            <div class='step-title' style='color:var(--blue2);'>Connect &amp; Retrieve</div>
            <div class='step-body'>Connects to Gmail via IMAP using your App Password and retrieves
                all unread emails securely. Nothing is stored outside your session.</div>
        </div>
        """, unsafe_allow_html=True)

    with s2:
        st.markdown("""
        <div class='step-card s-cyan'>
            <div class='step-num' style='color:var(--cyan2);'>02 — Analyse</div>
            <div class='step-title' style='color:var(--cyan2);'>Categorise &amp; Summarise</div>
            <div class='step-body'>Gemini 2.5 Flash classifies each email into Important, Promotions,
                Updates, or Others — and writes a sharp 2-sentence summary instantly.</div>
        </div>
        """, unsafe_allow_html=True)

    with s3:
        st.markdown("""
        <div class='step-card s-violet'>
            <div class='step-num' style='color:var(--violet2);'>03 — Draft</div>
            <div class='step-title' style='color:var(--violet2);'>Review &amp; Send</div>
            <div class='step-body'>A polished reply draft is generated for each email. Edit it freely,
                then choose to send — you remain in full control at every step.</div>
        </div>
        """, unsafe_allow_html=True)
