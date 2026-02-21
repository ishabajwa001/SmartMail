from __future__ import annotations
import re
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime

import streamlit as st
from utils.email_utils import fetch_emails, send_email, delete_email, format_size
from utils.ai_utils import ai_analyze_email
from utils.read_state import mark_read, bulk_read_ids

SORT_OPTIONS  = ["Newest First", "Oldest First", "Sender A→Z", "Sender Z→A", "Subject A→Z", "Has Attachments"]
GROUP_OPTIONS = ["None", "Category", "Sender", "Date"]

_CARD_CLS  = {"Important": "c-imp", "Promotions": "c-pro", "Updates": "c-upd", "Others": "c-oth"}
_PILL_CLS  = {"Important": "cp-imp", "Promotions": "cp-pro", "Updates": "cp-upd", "Others": "cp-oth"}
_CAT_ICON  = {"Important": "🔴", "Promotions": "🔵", "Updates": "🟢", "Others": "🟡"}
_CAT_COLOR = {
    "Important": "var(--coral)",  "Promotions": "var(--blue)",
    "Updates":   "var(--cyan)",   "Others":     "var(--violet)",
}
_ATT_ICONS = {
    "image": "🖼️", "application/pdf": "📄",
    "application/zip": "🗜️", "text": "📝",
    "audio": "🎵", "video": "🎬",
}


# ── Helpers ────────────────────────────────────────────────────────────────────

def _att_icon(ct: str) -> str:
    for k, v in _ATT_ICONS.items():
        if ct.startswith(k):
            return v
    return "📎"


def _pill(cat: str) -> str:
    return f"<span class='cpill {_PILL_CLS.get(cat, 'cp-oth')}'>{_CAT_ICON.get(cat,'•')} {cat}</span>"


def _parse_date(ds: str) -> datetime:
    try:
        return parsedate_to_datetime(ds).astimezone(timezone.utc)
    except Exception:
        return datetime(1970, 1, 1, tzinfo=timezone.utc)


def _sender_name(f: str) -> str:
    m = re.match(r'^"?([^<"]+)"?\s*<', f)
    if m:
        return m.group(1).strip()
    m = re.match(r'^([^@\s]+)', f)
    return m.group(1).strip() if m else f.strip()


def _date_bucket(ds: str) -> str:
    try:
        delta = (datetime.now(timezone.utc) - _parse_date(ds)).days
        if delta == 0:  return "Today"
        if delta == 1:  return "Yesterday"
        if delta <= 7:  return "This Week"
        if delta <= 30: return "This Month"
        return "Older"
    except Exception:
        return "Older"


def _apply_sort(items, sort_by):
    if sort_by == "Newest First":
        return sorted(items, key=lambda x: _parse_date(x[1].get("date", "")), reverse=True)
    if sort_by == "Oldest First":
        return sorted(items, key=lambda x: _parse_date(x[1].get("date", "")))
    if sort_by == "Sender A→Z":
        return sorted(items, key=lambda x: _sender_name(x[1].get("from", "")).lower())
    if sort_by == "Sender Z→A":
        return sorted(items, key=lambda x: _sender_name(x[1].get("from", "")).lower(), reverse=True)
    if sort_by == "Subject A→Z":
        return sorted(items, key=lambda x: (x[1].get("subject") or "").lower())
    if sort_by == "Has Attachments":
        return sorted(items, key=lambda x: len(x[1].get("attachments", [])), reverse=True)
    return items


def _apply_search(items, query):
    if not query.strip():
        return items
    q = query.lower()
    return [(i, em) for i, em in items
            if q in (em.get("subject") or "").lower()
            or q in (em.get("from") or "").lower()
            or q in (em.get("body") or "").lower()]


def _group_emails(items, group_by, categories):
    if group_by == "Category":
        order = ["Important", "Promotions", "Updates", "Others"]
        groups = {k: [] for k in order}
        for i, em in items:
            groups.setdefault(categories.get(i, "Others"), []).append((i, em))
        return {k: v for k, v in groups.items() if v}

    if group_by == "Sender":
        groups: dict = {}
        for i, em in items:
            groups.setdefault(_sender_name(em.get("from", "Unknown")), []).append((i, em))
        return dict(sorted(groups.items(), key=lambda x: x[0].lower()))

    if group_by == "Date":
        order_map = {"Today": 0, "Yesterday": 1, "This Week": 2, "This Month": 3, "Older": 4}
        groups: dict = {}
        for i, em in items:
            groups.setdefault(_date_bucket(em.get("date", "")), []).append((i, em))
        return dict(sorted(groups.items(), key=lambda x: order_map.get(x[0], 9)))

    return {"": items}


# ── Main render ────────────────────────────────────────────────────────────────

def render_inbox(email_addr: str, app_pass: str) -> None:
    col_h, col_b = st.columns([5, 1])
    with col_h:
        st.markdown(
            "<div class='page-title'>Your <span>Inbox</span></div>"
            "<div class='page-sub'>AI-powered email management — categorised, summarised, and ready to reply.</div>",
            unsafe_allow_html=True,
        )
    with col_b:
        st.markdown("<div style='margin-top:1.1rem'></div>", unsafe_allow_html=True)
        fetch_clicked = st.button("📬 Fetch Emails", key="btn_fetch")

    if fetch_clicked:
        if not st.session_state.credentials_ok:
            st.error("Connect your account in the sidebar first.")
        else:
            with st.spinner("Connecting to Gmail…"):
                try:
                    emails = fetch_emails(email_addr, app_pass)
                    st.session_state.update({
                        "emails":          emails,
                        "fetched":         True,
                        "categories":      {},
                        "summaries":       {},
                        "drafts":          {},
                        "sent_flags":      {},
                        "deleted_indices": set(),
                    })
                    # Restore persistent read flags using stable email IDs
                    persisted_read = bulk_read_ids()
                    for k in list(st.session_state.keys()):
                        if k.startswith("read_"):
                            del st.session_state[k]
                    for i, em in enumerate(emails):
                        if em.get("id") in persisted_read:
                            st.session_state[f"read_{i}"] = True
                    if not emails:
                        st.info("🎉 Inbox zero — no unread emails found! Click Fetch Emails again to check for new mail.")
                        st.rerun()
                    else:
                        st.success(f"Found **{len(emails)}** unread email(s). Running AI analysis…")
                        bar = st.progress(0)
                        for i, em in enumerate(emails):
                            result = ai_analyze_email(em["subject"], em["body"])
                            st.session_state.categories[i] = result["category"]
                            st.session_state.summaries[i]  = result["summary"]
                            st.session_state.drafts[i]     = result["draft"]
                            bar.progress((i + 1) / len(emails))
                        bar.empty()
                        st.rerun()
                except Exception as e:
                    st.error(f"Failed to fetch emails: {e}")

    if not (st.session_state.fetched and st.session_state.emails):
        if not st.session_state.fetched:
            st.markdown("""
            <div class='empty'>
                <div class='empty-icon'>📬</div>
                <div class='empty-title'>Ready when you are</div>
                <div class='empty-sub'>
                    Connect your credentials in the sidebar,<br>
                    then click <strong style='color:var(--blue);'>Fetch Emails</strong> above.
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Fetched but no emails — show a friendly empty state
            st.markdown("""
            <div class='empty'>
                <div class='empty-icon'>✅</div>
                <div class='empty-title'>Inbox Zero!</div>
                <div class='empty-sub'>
                    No unread emails right now.<br>
                    Click <strong style='color:var(--blue);'>Fetch Emails</strong> again to check for new arrivals.
                </div>
            </div>
            """, unsafe_allow_html=True)
        return

    # ── Ensure deleted_indices exists (backwards compat) ──────────────────────
    if "deleted_indices" not in st.session_state:
        st.session_state.deleted_indices = set()

    cats = list(st.session_state.categories.values())
    n    = len(st.session_state.emails)
    ndel = len(st.session_state.deleted_indices)
    nvis = n - ndel

    # ── Stats + Toolbar — fully unified layout ────────────────────────────────
    vis_cats = [
        st.session_state.categories.get(i, "Others")
        for i in range(n)
        if i not in st.session_state.deleted_indices
    ]
    n_imp = vis_cats.count("Important")
    n_pro = vis_cats.count("Promotions")
    n_upd = vis_cats.count("Updates")
    n_oth = vis_cats.count("Others")

    # Five equal stat columns — all same height, same padding, same font sizes
    sc = st.columns(5)
    stat_data = [
        ("📬", str(nvis),  "Total",      "var(--blue2)",   "var(--blue)",   "var(--b1)"),
        ("🔴", str(n_imp), "Important",  "var(--coral2)",  "var(--coral)",  "var(--coral)"),
        ("🔵", str(n_pro), "Promotions", "var(--blue2)",   "var(--blue)",   "var(--blue)"),
        ("🟢", str(n_upd), "Updates",    "var(--cyan2)",   "var(--cyan)",   "var(--cyan)"),
        ("🟡", str(n_oth), "Others",     "var(--violet2)", "var(--violet)", "var(--violet)"),
    ]
    for col, (icon, count, label, txt_color, accent, bdr) in zip(sc, stat_data):
        with col:
            st.markdown(f"""
            <div style="background:var(--bg2); border:1px solid var(--b1);
                        border-top:3px solid {accent}; border-radius:10px;
                        padding:0.85rem 1rem 0.75rem; text-align:center;
                        height:80px; display:flex; flex-direction:column;
                        align-items:center; justify-content:center; gap:2px;">
                <div style="font-family:'Beiruti',sans-serif; font-size:1.55rem;
                            font-weight:800; color:{txt_color}; line-height:1;">{count}</div>
                <div style="font-family:'Outfit',sans-serif; font-size:0.58rem; font-weight:700;
                            color:var(--t3); text-transform:uppercase; letter-spacing:0.11em;">
                    {icon} {label}
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div style='height:0.75rem'></div>", unsafe_allow_html=True)

    # Search + Sort + Group + Clear — all in one consistent row with matching heights
    tc1, tc2, tc3, tc4 = st.columns([4, 2, 2, 1])
    with tc1:
        search_val = st.text_input(
            "🔍 Search",
            value=st.session_state.inbox_search,
            placeholder="Search subject, sender, or body…",
            key="search_input",
        )
        st.session_state.inbox_search = search_val
    with tc2:
        sort_val = st.selectbox(
            "↕ Sort",
            SORT_OPTIONS,
            index=SORT_OPTIONS.index(st.session_state.inbox_sort),
            key="sort_select",
        )
        st.session_state.inbox_sort = sort_val
    with tc3:
        group_val = st.selectbox(
            "⊞ Group",
            GROUP_OPTIONS,
            index=GROUP_OPTIONS.index(st.session_state.inbox_group),
            key="group_select",
        )
        st.session_state.inbox_group = group_val
    with tc4:
        st.markdown("<div style='height:1.9rem'></div>", unsafe_allow_html=True)
        if st.button("✕", key="clear_filters", help="Clear all filters"):
            st.session_state.inbox_search = ""
            st.session_state.inbox_sort   = "Newest First"
            st.session_state.inbox_group  = "None"
            st.rerun()

    st.markdown("<div style='height:0.4rem'></div>", unsafe_allow_html=True)

    # ── Bulk selection / delete / restore row ──────────────────────────────────
    selected = {
        i for i in range(n)
        if i not in st.session_state.deleted_indices
        and st.session_state.get(f"chk_{i}", False)
    }

    has_deleted = bool(st.session_state.deleted_indices)
    if selected or has_deleted:
        action_cols = st.columns([3, 2, 2, 3])
        with action_cols[0]:
            if selected:
                st.markdown(f"""
                <div style="background:rgba(224,92,108,0.07); border:1px solid rgba(224,92,108,0.25);
                            border-radius:8px; padding:0.45rem 0.85rem;
                            font-family:'Outfit',sans-serif; font-size:0.82rem;
                            color:var(--coral2); display:flex; align-items:center; gap:7px;
                            height:38px;">
                    🗑️ <strong>{len(selected)}</strong>&nbsp;selected
                </div>""", unsafe_allow_html=True)
        with action_cols[1]:
            if selected:
                if st.button(f"🗑️ Delete ({len(selected)})", key="btn_delete_selected"):
                    with st.spinner("Deleting from Gmail…"):
                        for i in selected:
                            em = st.session_state.emails[i]
                            delete_email(email_addr, app_pass, em["id"])
                    st.session_state.deleted_indices |= selected
                    for i in selected:
                        st.session_state.pop(f"chk_{i}", None)
                    st.rerun()
        with action_cols[2]:
            if has_deleted:
                if st.button("↩ Restore View", key="btn_restore"):
                    st.session_state.deleted_indices = set()
                    st.rerun()
        with action_cols[3]:
            if has_deleted:
                nd = len(st.session_state.deleted_indices)
                st.markdown(f"""
                <div style="font-family:'Outfit',sans-serif; font-size:0.78rem;
                            color:var(--t3); padding-top:0.5rem;">
                    {nd} email{"s" if nd != 1 else ""} deleted
                </div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:0.2rem'></div>", unsafe_allow_html=True)

    # ── Category tabs ──────────────────────────────────────────────────────────
    # Each tab gets a unique tab_id so widget keys never collide across tabs
    tab_labels = ["All", "🔴 Important", "🔵 Promotions", "🟢 Updates", "🟡 Others"]
    tab_ids    = ["all", "imp", "pro", "upd", "oth"]
    tab_filters = [None, "Important", "Promotions", "Updates", "Others"]

    tabs = st.tabs(tab_labels)
    for tab, tab_id, filt in zip(tabs, tab_ids, tab_filters):
        with tab:
            _render_tab(tab_id, filt, email_addr, app_pass)


# ── Tab renderer ───────────────────────────────────────────────────────────────

def _render_tab(tab_id: str, cat_filter, email_addr: str, app_pass: str) -> None:
    deleted = st.session_state.deleted_indices

    items = [
        (i, em) for i, em in enumerate(st.session_state.emails)
        if i not in deleted
        and (not cat_filter or st.session_state.categories.get(i, "Others") == cat_filter)
    ]
    items = _apply_search(items, st.session_state.inbox_search)
    items = _apply_sort(items, st.session_state.inbox_sort)

    if not items:
        q = st.session_state.inbox_search
        msg = f"No emails match &ldquo;{q}&rdquo;." if q else "No emails in this category."
        st.markdown(
            f"<div style='text-align:center;padding:2.5rem;color:var(--t3);font-size:0.88rem;'>{msg}</div>",
            unsafe_allow_html=True,
        )
        return

    groups = _group_emails(items, st.session_state.inbox_group, st.session_state.categories)

    for label, group_items in groups.items():
        if label:
            color = _CAT_COLOR.get(label, "var(--t2)")
            st.markdown(f"""
            <div class='group-hdr'>
                <span class='group-hdr-label' style='color:{color};'>
                    {_CAT_ICON.get(label,'')} {label}
                </span>
                <span class='group-hdr-count'>{len(group_items)}</span>
            </div>
            """, unsafe_allow_html=True)

        for idx, em in group_items:
            _render_card(tab_id, idx, em, email_addr, app_pass)



# ── Card renderer ──────────────────────────────────────────────────────────────

def _render_card(tab_id: str, idx: int, em: dict, email_addr: str, app_pass: str) -> None:
    """
    tab_id is prepended to every widget key so the same email rendered
    in multiple tabs never produces duplicate keys.
    """
    cat  = st.session_state.categories.get(idx, "Others")
    sbj  = (em["subject"] or "(No Subject)")[:90]
    sdr  = em["from"][:65]
    dt   = em.get("date", "")
    atts = em.get("attachments", [])

    att_badge = (
        f"<span style='font-size:0.7rem;color:var(--blue);margin-left:6px;'>📎 {len(atts)}</span>"
        if atts else ""
    )

    is_read    = st.session_state.get(f"read_{idx}", False)
    read_badge = "<span style='font-size:0.65rem; color:var(--t3); margin-left:6px;'>✓ read</span>" if is_read else ""
    card_opacity = "opacity:0.72;" if is_read else ""
    subject_weight = "font-weight:500; color:var(--t2);" if is_read else "font-weight:600; color:var(--t1);"

    query = st.session_state.inbox_search.strip()
    sbj_display = sbj
    if query:
        sbj_display = re.compile(re.escape(query), re.IGNORECASE).sub(
            lambda m: f"<mark>{m.group()}</mark>", sbj
        )

    # ── Card row: checkbox + card ──────────────────────────────────────────────
    chk_col, card_col = st.columns([0.3, 9.7])
    with chk_col:
        st.markdown("<div style='padding-top:0.85rem;'></div>", unsafe_allow_html=True)
        checked = st.checkbox(
            "", value=st.session_state.get(f"chk_{idx}", False),
            key=f"{tab_id}_chk_{idx}",
            label_visibility="collapsed",
        )
        st.session_state[f"chk_{idx}"] = checked

    with card_col:
        st.markdown(f"""
        <div class='ecard {_CARD_CLS.get(cat,"c-oth")} fade-in' style='{card_opacity}'>
            <div class='ecard-from'>{sdr}</div>
            <div class='ecard-subject' style='{subject_weight}'>{sbj_display}</div>
            <div style='display:flex;align-items:center;gap:8px;flex-wrap:wrap;'>
                {_pill(cat)}<span class='ecard-date'>{dt}</span>{att_badge}{read_badge}
            </div>
        </div>
        """, unsafe_allow_html=True)

        with st.expander(f"↳  {sbj[:60]}"):
            summary = st.session_state.summaries.get(idx, "")

            # ── Original Email body ────────────────────────────────────────────
            body_txt = (em.get("body") or "").strip()

            # Track read state — use persistent store via email ID
            read_key   = f"read_{idx}"
            email_id   = em.get("id", "")
            already_read = st.session_state.get(read_key, False)

            if body_txt:
                # Normalise whitespace — strip all blank/whitespace-only lines
                body_lines = body_txt.splitlines()
                body_lines = [ln.strip() for ln in body_lines]
                # Remove consecutive empty lines, keep at most one
                collapsed = []
                prev_empty = False
                for ln in body_lines:
                    if ln == "":
                        if not prev_empty:
                            collapsed.append(ln)
                        prev_empty = True
                    else:
                        collapsed.append(ln)
                        prev_empty = False
                body_clean = "\n".join(collapsed).strip()

                # HTML-escape
                body_safe = (
                    body_clean
                    .replace("&", "&amp;")
                    .replace("<", "&lt;")
                    .replace(">", "&gt;")
                    .replace('"', "&quot;")
                )
                # Single newline → <br>, blank line → small spacer
                body_safe = body_safe.replace("\n\n", "<br>").replace("\n", "<br>")

                st.markdown(f"""
                <div style='margin-bottom:1rem;'>
                    <div style='font-family:"Outfit",sans-serif; font-size:0.60rem; font-weight:800;
                                color:var(--t3); text-transform:uppercase; letter-spacing:0.12em;
                                margin-bottom:0.5rem;'>📧 ORIGINAL EMAIL</div>
                    <div style='background:var(--bg3); border:1px solid var(--b1);
                                border-left:3px solid var(--b2); border-radius:10px;
                                padding:0.75rem 1.1rem;
                                font-family:"Outfit",sans-serif; font-size:0.85rem;
                                color:var(--t1); line-height:1.55; word-break:break-word;
                                max-height:280px; overflow-y:auto;'>
                        {body_safe}
                    </div>
                </div>
                """, unsafe_allow_html=True)

            # Mark as read — persist to disk so it survives future sessions
            if not already_read and email_id:
                mark_read(email_id)
                st.session_state[read_key] = True

            # ── AI Summary — highlighted blue ──────────────────────────────────
            st.markdown(f"""
            <div style='background:linear-gradient(135deg, rgba(91,141,239,0.10) 0%, rgba(91,141,239,0.04) 100%);
                        border:1px solid rgba(91,141,239,0.35);
                        border-left:4px solid var(--blue);
                        border-radius:11px; padding:1rem 1.3rem; margin-bottom:1rem;
                        box-shadow:0 2px 16px rgba(91,141,239,0.08);'>
                <div style='font-family:"Outfit",sans-serif; font-size:0.60rem; font-weight:800;
                            color:var(--blue2); text-transform:uppercase; letter-spacing:0.14em;
                            margin-bottom:0.5rem; display:flex; align-items:center; gap:6px;'>
                    <span style='background:var(--blue); color:#fff; border-radius:4px;
                                 padding:1px 8px; font-size:0.58rem;'>✦ AI</span>
                    SUMMARY
                </div>
                <div style='font-family:"Outfit",sans-serif; font-size:0.90rem;
                            color:var(--t1); line-height:1.78;'>{summary or "No summary available."}</div>
            </div>
            """, unsafe_allow_html=True)

            # ── Attachments ────────────────────────────────────────────────────
            if atts:
                st.markdown("""
                <div style='font-family:"Outfit",sans-serif; font-size:0.60rem; font-weight:800;
                            color:var(--t3); text-transform:uppercase; letter-spacing:0.12em;
                            margin-bottom:0.65rem;'>📎 ATTACHMENTS</div>
                """, unsafe_allow_html=True)
                acols = st.columns(min(len(atts), 4))
                for ai, att in enumerate(atts):
                    with acols[ai % 4]:
                        icon = _att_icon(att["content_type"])
                        size = format_size(att["size"])
                        fname = att['filename']
                        ext = fname.rsplit('.', 1)[-1].upper() if '.' in fname else 'FILE'
                        st.markdown(f"""
                        <div style='background:var(--bg2); border:1px solid var(--b1);
                                    border-radius:11px; padding:1rem 0.9rem 0.7rem;
                                    text-align:center; margin-bottom:0.5rem;
                                    transition:border-color 0.22s, box-shadow 0.22s, transform 0.22s;'
                             onmouseover="this.style.borderColor='rgba(91,141,239,0.45)';this.style.transform='translateY(-2px)'"
                             onmouseout="this.style.borderColor='var(--b1)';this.style.transform='translateY(0)'">
                            <div style='font-size:2rem; margin-bottom:6px;'>{icon}</div>
                            <div style='display:inline-block; background:rgba(91,141,239,0.10);
                                        border:1px solid rgba(91,141,239,0.22); border-radius:4px;
                                        padding:1px 7px; font-family:"JetBrains Mono",monospace;
                                        font-size:0.60rem; font-weight:600; color:var(--blue2);
                                        margin-bottom:7px;'>{ext}</div>
                            <div style='font-size:0.78rem; color:var(--t2); font-weight:500;
                                        word-break:break-all; margin-bottom:3px;
                                        font-family:"Outfit",sans-serif; line-height:1.4;'>
                                {fname[:24]}{"…" if len(fname) > 24 else ""}</div>
                            <div style='font-size:0.70rem; color:var(--t3);
                                        font-family:"JetBrains Mono",monospace;'>{size}</div>
                        </div>
                        """, unsafe_allow_html=True)
                        st.download_button(
                            "⬇ Download", data=att["data"],
                            file_name=att["filename"], mime=att["content_type"],
                            key=f"{tab_id}_dl_{idx}_{ai}",
                            use_container_width=True,
                        )

            # ── Draft Reply — highlighted violet, single editable area ─────────
            draft_widget_key = f"{tab_id}_draft_{idx}"
            draft_val = st.session_state.drafts.get(idx, "")

            st.markdown("""
            <div style='background:linear-gradient(135deg, rgba(155,109,255,0.09) 0%, rgba(155,109,255,0.03) 100%);
                        border:1px solid rgba(155,109,255,0.30);
                        border-left:4px solid var(--violet);
                        border-radius:11px; padding:0.8rem 1.2rem 0.4rem 1.2rem;
                        margin-top:0.5rem; margin-bottom:0.5rem;
                        box-shadow:0 2px 12px rgba(155,109,255,0.06);'>
                <div style='font-family:"Outfit",sans-serif; font-size:0.60rem; font-weight:800;
                            color:var(--violet2); text-transform:uppercase; letter-spacing:0.14em;
                            margin-bottom:0.4rem; display:flex; align-items:center; gap:6px;'>
                    <span style='background:var(--violet); color:#fff; border-radius:4px;
                                 padding:1px 8px; font-size:0.58rem;'>✏️</span>
                    DRAFT REPLY — edit &amp; send
                </div>
            </div>
            """, unsafe_allow_html=True)

            edited = st.text_area(
                "reply",
                value=draft_val,
                height=250,
                key=draft_widget_key,
                label_visibility="collapsed",
                placeholder="Your AI-generated reply will appear here. Edit freely before sending.",
            )
            st.session_state.drafts[idx] = edited

            # Attachment uploader — styled
            reply_files = st.file_uploader(
                "📎 Attach files to reply",
                accept_multiple_files=True,
                key=f"{tab_id}_reply_att_{idx}",
            )

            if reply_files:
                _ext_icon = {
                    "pdf":"📄","doc":"📝","docx":"📝","xls":"📊","xlsx":"📊",
                    "ppt":"📋","pptx":"📋","zip":"🗜️","rar":"🗜️",
                    "jpg":"🖼️","jpeg":"🖼️","png":"🖼️","gif":"🖼️","webp":"🖼️",
                    "mp4":"🎬","mov":"🎬","mp3":"🎵","wav":"🎵",
                    "txt":"📃","csv":"📊","py":"🐍","js":"⚡",
                }
                total_kb = round(sum(f.size for f in reply_files) / 1024, 1)
                total_str = f"{total_kb} KB" if total_kb < 1024 else f"{round(total_kb/1024,1)} MB"
                rows_html = ""
                for f in reply_files:
                    ext  = f.name.rsplit(".", 1)[-1].lower() if "." in f.name else ""
                    icon = _ext_icon.get(ext, "📎")
                    size = f"{round(f.size/1024,1)} KB" if f.size < 1048576 else f"{round(f.size/1048576,1)} MB"
                    name = f.name if len(f.name) <= 30 else f.name[:28] + "…"
                    rows_html += f"""
                    <div style='display:flex; align-items:center; gap:8px;
                                padding:0.45rem 0.75rem; border-bottom:1px solid var(--b1);'>
                        <span style='font-size:1.1rem; flex-shrink:0;'>{icon}</span>
                        <div style='flex:1; min-width:0; font-family:"Outfit",sans-serif;
                                    font-size:0.82rem; color:var(--t1); font-weight:500;
                                    white-space:nowrap; overflow:hidden; text-overflow:ellipsis;'>{name}</div>
                        <span style='font-family:"JetBrains Mono",monospace; font-size:0.62rem;
                                     color:var(--t3); flex-shrink:0;'>{size}</span>
                    </div>"""
                st.markdown(f"""
                <div style='background:var(--bg3); border:1px solid var(--b2);
                            border-radius:9px; overflow:hidden; margin-top:0.3rem;'>
                    <div style='display:flex; justify-content:space-between; align-items:center;
                                padding:0.45rem 0.8rem; background:var(--bg4);
                                border-bottom:1px solid var(--b1);'>
                        <span style='font-family:"Outfit",sans-serif; font-size:0.64rem; font-weight:700;
                                     color:var(--t2); text-transform:uppercase; letter-spacing:0.08em;'>
                            📎 {len(reply_files)} attached
                        </span>
                        <span style='font-family:"JetBrains Mono",monospace; font-size:0.64rem;
                                     color:var(--blue2);'>{total_str}</span>
                    </div>
                    {rows_html}
                </div>
                """, unsafe_allow_html=True)

            # Action buttons row
            st.markdown("<div style='height:0.4rem'></div>", unsafe_allow_html=True)
            b1, b2, b3, b4 = st.columns(4)
            with b1:
                if st.button("🔄", key=f"{tab_id}_regen_{idx}", help="Regenerate draft"):
                    with st.spinner("Regenerating…"):
                        result = ai_analyze_email(em["subject"], em["body"])
                        new_draft = result["draft"]
                    # Delete widget key so Streamlit re-renders with new value
                    st.session_state.drafts[idx] = new_draft
                    if draft_widget_key in st.session_state:
                        del st.session_state[draft_widget_key]
                    st.rerun()
            with b2:
                already_sent = st.session_state.sent_flags.get(idx, False)
                if st.button(
                    "✅" if already_sent else "📤",
                    key=f"{tab_id}_send_{idx}",
                    disabled=already_sent,
                    help="Send reply" if not already_sent else "Already sent",
                ):
                    try:
                        send_email(
                            from_addr=email_addr, app_password=app_pass,
                            to_addr=em["from"],
                            subject=f"Re: {em['subject']}",
                            body=st.session_state.drafts[idx],
                            attachments=reply_files if reply_files else None,
                        )
                        st.session_state.sent_flags[idx] = True
                        st.success("✅ Reply sent!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Failed to send: {e}")
            with b3:
                if st.button("✍️", key=f"{tab_id}_fwd_{idx}", help="Open in Compose"):
                    st.session_state.compose_to   = em["from"]
                    st.session_state.compose_sub  = f"Re: {em['subject']}"
                    st.session_state.compose_body = st.session_state.drafts[idx]
                    st.session_state.current_page = "compose"
                    st.rerun()
            with b4:
                if st.button("🗑️", key=f"{tab_id}_del_{idx}", help="Delete email"):
                    with st.spinner("Deleting…"):
                        delete_email(email_addr, app_pass, em["id"])
                    st.session_state.deleted_indices.add(idx)
                    st.session_state.pop(f"chk_{idx}", None)
                    st.rerun()
