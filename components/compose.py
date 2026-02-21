import streamlit as st
from utils.email_utils import send_email
from utils.ai_utils import ai_compose, parse_draft


def render_compose(email_addr: str, app_pass: str) -> None:
    st.markdown(
        "<div class='page-title'>Compose <span>Email</span></div>"
        "<div class='page-sub'>Write manually or generate a draft with AI assistance.</div>",
        unsafe_allow_html=True,
    )

    col_form, col_ai = st.columns([3, 2], gap="large")

    # ── LEFT: Email form ──────────────────────────────────────────────────────
    with col_form:
        st.markdown("#### 📧 New Email")

        to_val  = st.text_input("To",      value=st.session_state.compose_to,  placeholder="recipient@example.com")
        sub_val = st.text_input("Subject", value=st.session_state.compose_sub, placeholder="Subject line…")

        body_key = f"compose_body_{st.session_state.compose_gen}"
        body_val = st.text_area(
            "Body",
            value=st.session_state.compose_body,
            placeholder="Write your message here…",
            height=260,
            key=body_key,
        )

        st.session_state.compose_body = body_val
        st.session_state.compose_to   = to_val
        st.session_state.compose_sub  = sub_val

        # ── Attachments ────────────────────────────────────────────────────────
        st.markdown("<div style='margin-top:0.6rem;'></div>", unsafe_allow_html=True)
        uploaded_files = st.file_uploader(
            "📎 Attach files — drag & drop or click to browse",
            accept_multiple_files=True,
            key="compose_attachments",
        )

        if uploaded_files:
            _ext_icon = {
                "pdf":"📄","doc":"📝","docx":"📝","xls":"📊","xlsx":"📊",
                "ppt":"📋","pptx":"📋","zip":"🗜️","rar":"🗜️","7z":"🗜️",
                "jpg":"🖼️","jpeg":"🖼️","png":"🖼️","gif":"🖼️","svg":"🖼️","webp":"🖼️",
                "mp4":"🎬","mov":"🎬","avi":"🎬","mkv":"🎬",
                "mp3":"🎵","wav":"🎵","flac":"🎵",
                "txt":"📃","csv":"📊","json":"🔧","py":"🐍","js":"⚡","html":"🌐","css":"🎨",
            }
            total_kb  = round(sum(f.size for f in uploaded_files) / 1024, 1)
            total_str = f"{total_kb} KB" if total_kb < 1024 else f"{round(total_kb/1024,1)} MB"
            rows_html = ""
            for f in uploaded_files:
                ext       = f.name.rsplit(".", 1)[-1].lower() if "." in f.name else ""
                icon      = _ext_icon.get(ext, "📎")
                size      = f"{round(f.size/1024,1)} KB" if f.size < 1048576 else f"{round(f.size/1048576,1)} MB"
                name      = f.name if len(f.name) <= 36 else f.name[:34] + "…"
                ext_label = ext.upper() if ext else "FILE"
                rows_html += f"""
                <div style='display:flex;align-items:center;gap:10px;
                            padding:0.55rem 0.8rem;border-bottom:1px solid var(--b1);'>
                    <span style='font-size:1.3rem;flex-shrink:0;'>{icon}</span>
                    <div style='flex:1;min-width:0;'>
                        <div style='font-family:"Outfit",sans-serif;font-size:0.84rem;
                                    font-weight:500;color:var(--t1);
                                    white-space:nowrap;overflow:hidden;text-overflow:ellipsis;'>{name}</div>
                        <div style='font-family:"JetBrains Mono",monospace;font-size:0.63rem;
                                    color:var(--t3);margin-top:1px;'>{size}</div>
                    </div>
                    <span style='background:rgba(91,141,239,0.12);border:1px solid rgba(91,141,239,0.25);
                                 border-radius:5px;padding:2px 8px;font-family:"JetBrains Mono",monospace;
                                 font-size:0.58rem;font-weight:700;color:var(--blue2);
                                 flex-shrink:0;'>{ext_label}</span>
                </div>"""
            st.markdown(f"""
            <div style='background:var(--bg3);border:1px solid var(--b2);
                        border-radius:10px;overflow:hidden;margin-top:0.2rem;'>
                <div style='display:flex;justify-content:space-between;align-items:center;
                            padding:0.55rem 0.9rem;background:var(--bg4);
                            border-bottom:1px solid var(--b1);'>
                    <span style='font-family:"Outfit",sans-serif;font-size:0.68rem;font-weight:700;
                                 color:var(--t2);text-transform:uppercase;letter-spacing:0.09em;'>
                        📎 {len(uploaded_files)} file{'s' if len(uploaded_files)!=1 else ''} ready
                    </span>
                    <span style='font-family:"JetBrains Mono",monospace;font-size:0.68rem;
                                 color:var(--blue2);font-weight:600;'>{total_str}</span>
                </div>
                {rows_html}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style='background:var(--bg3);border:2px dashed var(--b1);border-radius:10px;
                        padding:1.2rem;text-align:center;margin-top:0.2rem;'>
                <div style='font-size:1.4rem;margin-bottom:4px;opacity:0.5;'>📎</div>
                <div style='font-family:"Outfit",sans-serif;font-size:0.80rem;color:var(--t3);'>
                    No files attached yet
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='margin-top:0.6rem;'></div>", unsafe_allow_html=True)
        c_send, c_clear = st.columns([3, 2])
        with c_send:
            if st.button("📤 Send Email", key="compose_send"):
                _handle_send(email_addr, app_pass, to_val, sub_val, body_val,
                             attachments=uploaded_files or None)
        with c_clear:
            if st.button("🗑️ Clear", key="compose_clear"):
                st.session_state.compose_to   = ""
                st.session_state.compose_sub  = ""
                st.session_state.compose_body = ""
                st.session_state.compose_gen += 1
                st.rerun()

    # ── RIGHT: AI panel ───────────────────────────────────────────────────────
    with col_ai:
        st.markdown("""
        <div class='ai-panel'>
            <div class='ai-title'>✦ AI Drafting Assistant</div>
            <div class='ai-sub'>
                Describe what you want to write in plain English.
                AI will generate the subject and body — review it, then click
                <em>Use This Draft</em> to load it into the form.
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<div style='height:0.7rem'></div>", unsafe_allow_html=True)

        brief = st.text_area("Your brief", placeholder="", height=100, key="ai_brief_input")

        if st.button("✦ Generate Draft", key="ai_generate", use_container_width=True):
            if not st.session_state.credentials_ok:
                st.error("Connect your account in the sidebar first.")
            elif not brief.strip():
                st.warning("Write a brief above first.")
            else:
                with st.spinner("Drafting…"):
                    raw = ai_compose(brief)
                if raw.startswith("[quota]"):
                    st.warning("⏳ " + raw[7:].strip())
                elif raw.startswith("[error]"):
                    st.error("❌ " + raw[7:].strip())
                else:
                    st.session_state.ai_draft_text = raw

        # ── Draft preview box ─────────────────────────────────────────────────
        if st.session_state.ai_draft_text:
            st.markdown("<div style='height:0.4rem'></div>", unsafe_allow_html=True)
            st.markdown("<div class='chip'>✦ Generated Draft — review &amp; edit below</div>",
                        unsafe_allow_html=True)

            draft_edit_key = f"ai_draft_edit_{st.session_state.compose_gen}"
            edited = st.text_area(
                "",
                value=st.session_state.ai_draft_text,
                height=220,
                key=draft_edit_key,
                label_visibility="collapsed",
            )
            st.session_state.ai_draft_text = edited

            bu, br = st.columns(2, gap="small")
            with bu:
                if st.button("📋 Use This Draft", key="ai_use_draft", use_container_width=True):
                    subject, body = parse_draft(edited)
                    if subject:
                        st.session_state.compose_sub = subject
                    st.session_state.compose_body      = body
                    st.session_state.ai_draft_text     = ""
                    st.session_state.compose_gen      += 1
                    st.rerun()
            with br:
                if st.button("🔄 Regenerate", key="ai_regen", use_container_width=True):
                    if brief.strip():
                        with st.spinner("Regenerating…"):
                            raw = ai_compose(brief)
                        if raw.startswith("[quota]"):
                            st.warning("⏳ " + raw[7:].strip())
                        elif raw.startswith("[error]"):
                            st.error("❌ " + raw[7:].strip())
                        else:
                            st.session_state.ai_draft_text = raw
                            st.rerun()
                    else:
                        st.warning("Write a brief above first.")

        st.markdown("<div style='height:0.8rem'></div>", unsafe_allow_html=True)
        st.markdown("""
        <div style='background:var(--bg3);border:1px solid var(--b1);border-radius:9px;
                    padding:1rem 1.1rem;font-size:0.8rem;color:var(--t2);line-height:1.85;'>
            <div style='color:var(--em);font-weight:700;font-size:0.68rem;
                        text-transform:uppercase;letter-spacing:0.09em;margin-bottom:0.5rem;'>
                💡 How it works
            </div>
            1. Describe your email in the brief box<br>
            2. Click <strong style='color:var(--t1);'>✦ Generate Draft</strong><br>
            3. Review and edit in the draft box<br>
            4. Click <strong style='color:var(--t1);'>📋 Use This Draft</strong> to load it<br>
            5. Hit <strong style='color:var(--t1);'>📤 Send Email</strong>
        </div>
        """, unsafe_allow_html=True)


def _handle_send(email_addr, app_pass, to, sub, body, attachments=None):
    if not st.session_state.credentials_ok:
        st.error("Connect your account in the sidebar first.")
    elif not to.strip():
        st.warning("Please enter a recipient address.")
    elif not sub.strip():
        st.warning("Please enter a subject line.")
    elif not body.strip():
        st.warning("Please write a message body.")
    else:
        try:
            send_email(email_addr, app_pass, to, sub, body, attachments=attachments)
            n    = len(attachments) if attachments else 0
            note = f" with {n} attachment{'s' if n != 1 else ''}" if n else ""
            st.success(f"✅ Email sent to **{to}**{note}!")
            st.session_state.compose_to   = ""
            st.session_state.compose_sub  = ""
            st.session_state.compose_body = ""
            st.session_state.compose_gen += 1
            st.rerun()
        except Exception as e:
            st.error(f"Failed to send: {e}")
