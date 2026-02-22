from __future__ import annotations
import re
import html as html_module
import html as _html          # top-level so _render_card doesn't re-import on every card
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime


def _strip_html(text: str) -> str:
    """Remove HTML tags and unescape HTML entities for clean plain-text display."""
    if not text:
        return text
    # Remove style/script blocks entirely
    text = re.sub(r'<(style|script)[^>]*>.*?</(style|script)>', '', text, flags=re.DOTALL | re.IGNORECASE)
    # Remove all remaining HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    # Unescape HTML entities (e.g. &amp; → &, &lt; → <)
    text = html_module.unescape(text)
    # Collapse excessive whitespace/blank lines
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()

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

    # Show persistent flash messages (reply sent, inbox-zero, etc.) that survive rerun
    if st.session_state.get("inbox_reply_sent_msg"):
        st.success(st.session_state.inbox_reply_sent_msg)
        st.session_state.inbox_reply_sent_msg = ""
    if st.session_state.get("inbox_flash_msg"):
        st.info(st.session_state.inbox_flash_msg)
        st.session_state.inbox_flash_msg = ""

    if fetch_clicked:
        if not st.session_state.credentials_ok:
            st.error("Connect your account in the sidebar first.")
        else:
            with st.spinner("Connecting to Gmail…"):
                try:
                    emails = fetch_emails(email_addr, app_pass)
                    st.session_state.update({
                        "emails":              emails,
                        "fetched":             True,
                        "categories":          {},
                        "summaries":           {},
                        "drafts":              {},
                        "sent_flags":          {},
                        "reply_att_gen":       {},
                        "deleted_indices":     set(),
                        "bulk_delete_confirm": False,
                    })
                    # Restore persistent read flags using stable email IDs
                    persisted_read = bulk_read_ids()   # set[str]
                    for k in list(st.session_state.keys()):
                        if k.startswith("read_"):
                            del st.session_state[k]
                    for i, em in enumerate(emails):
                        raw_id = em.get("id", b"")
                        # em["id"] comes from IMAP as bytes; persisted_read stores strings
                        str_id = raw_id.decode("utf-8", errors="replace") if isinstance(raw_id, bytes) else str(raw_id)
                        if str_id in persisted_read:
                            st.session_state[f"read_{i}"] = True
                    if not emails:
                        st.session_state.inbox_flash_msg = "🎉 Inbox zero — no unread emails found! Click Fetch Emails again to check for new mail."
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
                    msg = str(e).lower()
                    if "auth" in msg or "login" in msg or "password" in msg or "credentials" in msg:
                        st.error("Failed to fetch emails: Authentication error. Please check your Gmail address and App Password.")
                    elif "timeout" in msg or "connect" in msg or "network" in msg:
                        st.error("Failed to fetch emails: Connection timed out. Please check your internet connection.")
                    else:
                        st.error("Failed to fetch emails. Please verify your credentials and that IMAP is enabled in Gmail.")

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

    # Six equal stat columns — all same height, same padding, same font sizes
    sc = st.columns(6)
    stat_data = [
        ("📬", str(nvis),  "Total",      "var(--blue2)",   "var(--blue)",   "var(--b1)"),
        ("🔴", str(n_imp), "Important",  "var(--coral2)",  "var(--coral)",  "var(--coral)"),
        ("🔵", str(n_pro), "Promotions", "var(--blue2)",   "var(--blue)",   "var(--blue)"),
        ("🟢", str(n_upd), "Updates",    "var(--cyan2)",   "var(--cyan)",   "var(--cyan)"),
        ("🟡", str(n_oth), "Others",     "var(--violet2)", "var(--violet)", "var(--violet)"),
        ("🗑️", str(ndel),  "Deleted",    "var(--coral2)",  "var(--coral)",  "var(--coral)"),
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
            # Reset both the shadow vars AND the widget keys so the UI visually clears
            st.session_state.inbox_search  = ""
            st.session_state.inbox_sort    = "Newest First"
            st.session_state.inbox_group   = "None"
            st.session_state.search_input  = ""
            st.session_state.sort_select   = "Newest First"
            st.session_state.group_select  = "None"
            st.rerun()

    st.markdown("<div style='height:0.4rem'></div>", unsafe_allow_html=True)

    # ── Bulk action bar — always visible when emails are loaded ───────────────
    # IMPORTANT: checkboxes are keyed as "{tab_id}_chk_{idx}" (e.g. "all_chk_0").
    # We must read from those keys directly — NOT from bare "chk_{i}" which is
    # always one render behind. An email is "selected" if it is checked in ANY tab.
    _ALL_TAB_IDS = ["all", "imp", "pro", "upd", "oth"]
    selected = {
        i for i in range(n)
        if i not in st.session_state.deleted_indices
        and any(st.session_state.get(f"{tid}_chk_{i}", False) for tid in _ALL_TAB_IDS)
    }

    has_deleted = bool(st.session_state.deleted_indices)
    n_visible   = n - len(st.session_state.deleted_indices)

    # Always render the action bar so users can discover Select All
    bar_cols = st.columns([2.2, 1.6, 1.6, 1.6, 1.6, 1.4])

    with bar_cols[0]:
        # Selection count badge — shows how many are ticked
        if selected:
            st.markdown(f"""
            <div style="background:rgba(224,92,108,0.10); border:1px solid rgba(224,92,108,0.30);
                        border-radius:8px; padding:0.45rem 0.9rem;
                        font-family:'Outfit',sans-serif; font-size:0.83rem;
                        color:var(--coral2); display:flex; align-items:center; gap:7px; height:38px;">
                ☑️ <strong>{len(selected)}</strong>&nbsp;of&nbsp;{n_visible}&nbsp;selected
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="background:var(--bg2); border:1px solid var(--b1);
                        border-radius:8px; padding:0.45rem 0.9rem;
                        font-family:'Outfit',sans-serif; font-size:0.83rem;
                        color:var(--t3); display:flex; align-items:center; gap:7px; height:38px;">
                ☐ &nbsp;{n_visible}&nbsp;email{"s" if n_visible != 1 else ""}
            </div>""", unsafe_allow_html=True)

    with bar_cols[1]:
        if st.button("☑ Select All", key="btn_select_all", use_container_width=True,
                     help="Select all visible emails"):
            for tid in _ALL_TAB_IDS:
                for i in range(n):
                    if i not in st.session_state.deleted_indices:
                        st.session_state[f"{tid}_chk_{i}"] = True
            st.session_state.bulk_delete_confirm = False
            st.rerun()

    with bar_cols[2]:
        if st.button("☐ Deselect All", key="btn_deselect_all", use_container_width=True,
                     help="Clear all selections", disabled=not selected):
            for tid in _ALL_TAB_IDS:
                for i in range(n):
                    st.session_state.pop(f"{tid}_chk_{i}", None)
            st.session_state.bulk_delete_confirm = False
            st.rerun()

    with bar_cols[3]:
        if not st.session_state.bulk_delete_confirm:
            # First click: arm the confirm step
            if st.button(f"🗑️ Delete ({len(selected)})", key="btn_delete_arm",
                         use_container_width=True, disabled=not selected,
                         help="Delete selected emails"):
                st.session_state.bulk_delete_confirm = True
                st.rerun()
        else:
            # Second click: actually delete
            if st.button(f"⚠️ Confirm ({len(selected)})", key="btn_delete_confirm",
                         use_container_width=True, type="primary",
                         help="Click again to permanently delete"):
                with st.spinner(f"Deleting {len(selected)} email(s) from Gmail…"):
                    for i in selected:
                        em = st.session_state.emails[i]
                        delete_email(email_addr, app_pass, em["id"])
                st.session_state.deleted_indices |= selected
                for i in selected:
                    for tid in _ALL_TAB_IDS:
                        st.session_state.pop(f"{tid}_chk_{i}", None)
                st.session_state.bulk_delete_confirm = False
                st.session_state.inbox_flash_msg = (
                    f"🗑️ {len(selected)} email{'s' if len(selected) != 1 else ''} deleted."
                )
                st.rerun()

    with bar_cols[4]:
        if st.session_state.bulk_delete_confirm and selected:
            if st.button("✕ Cancel", key="btn_delete_cancel", use_container_width=True):
                st.session_state.bulk_delete_confirm = False
                st.rerun()
        elif has_deleted:
            if st.button("↩ Restore View", key="btn_restore", use_container_width=True,
                         help="Restore soft-deleted emails to view"):
                st.session_state.deleted_indices = set()
                st.session_state.bulk_delete_confirm = False
                st.rerun()

    with bar_cols[5]:
        if has_deleted:
            nd = len(st.session_state.deleted_indices)
            st.markdown(f"""
            <div style="font-family:'Outfit',sans-serif; font-size:0.75rem;
                        color:var(--t3); padding-top:0.55rem; text-align:right;">
                {nd} deleted
            </div>""", unsafe_allow_html=True)

    # Warn user they're about to delete while confirm is armed
    if st.session_state.bulk_delete_confirm and selected:
        st.warning(
            f"⚠️ About to permanently delete **{len(selected)}** email(s) from Gmail. "
            f"Click **⚠️ Confirm** to proceed or **✕ Cancel** to abort."
        )

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
        q_esc = _html.escape(q)
        msg = f"No emails match &ldquo;{q_esc}&rdquo;." if q else "No emails in this category."
        st.markdown(
            f"<div style='text-align:center;padding:2.5rem;color:var(--t3);font-size:0.88rem;'>{msg}</div>",
            unsafe_allow_html=True,
        )
        return

    # ── Per-tab Select All / Deselect Tab row ─────────────────────────────────
    _ALL_TAB_IDS = ["all", "imp", "pro", "upd", "oth"]
    tab_indices  = [i for i, _ in items]
    # An email counts as checked if it is ticked in ANY tab
    tab_checked  = [
        any(st.session_state.get(f"{tid}_chk_{i}", False) for tid in _ALL_TAB_IDS)
        for i in tab_indices
    ]
    all_checked  = bool(tab_checked) and all(tab_checked)

    sel_a, sel_b, sel_spacer = st.columns([1.4, 1.6, 7])
    with sel_a:
        label = "☑ All in tab" if not all_checked else "☐ None in tab"
        if st.button(label, key=f"{tab_id}_sel_all", use_container_width=True,
                     help="Select or deselect all emails in this tab"):
            new_val = not all_checked
            for i in tab_indices:
                for tid in _ALL_TAB_IDS:
                    if new_val:
                        st.session_state[f"{tid}_chk_{i}"] = True
                    else:
                        st.session_state.pop(f"{tid}_chk_{i}", None)
            st.session_state.bulk_delete_confirm = False
            st.rerun()
    with sel_b:
        n_tab_sel = sum(tab_checked)
        if n_tab_sel:
            st.markdown(f"""
            <div style="font-family:'Outfit',sans-serif; font-size:0.78rem;
                        color:var(--coral2); padding-top:0.52rem;">
                {n_tab_sel} / {len(items)} checked in this tab
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="font-family:'Outfit',sans-serif; font-size:0.78rem;
                        color:var(--t3); padding-top:0.52rem;">
                {len(items)} email{"s" if len(items) != 1 else ""} — tick to select
            </div>""", unsafe_allow_html=True)

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

    # ── SECURITY: HTML-escape all user-controlled strings before injecting into HTML ──
    sbj_esc = _html.escape(sbj)
    sdr_esc = _html.escape(sdr)
    dt_esc  = _html.escape(dt)

    att_badge = ""
    if atts:
        n_imgs  = sum(1 for a in atts if a["content_type"].startswith("image/"))
        n_files = len(atts) - n_imgs
        parts = []
        if n_imgs:
            parts.append(f"🖼️ {n_imgs}")
        if n_files:
            parts.append(f"📎 {n_files}")
        att_badge = f"<span style='font-size:0.7rem;color:var(--blue);margin-left:6px;'>{' '.join(parts)}</span>"


    is_read    = st.session_state.get(f"read_{idx}", False)
    read_badge = "<span style='font-size:0.65rem; color:var(--t3); margin-left:6px;'>✓ read</span>" if is_read else ""
    card_opacity = "opacity:0.72;" if is_read else ""
    subject_weight = "font-weight:500; color:var(--t2);" if is_read else "font-weight:600; color:var(--t1);"

    query = st.session_state.inbox_search.strip()
    sbj_display = sbj_esc  # always start from the escaped version
    if query:
        # escape the query too before embedding in regex replacement
        query_esc = _html.escape(query)
        sbj_display = re.compile(re.escape(query_esc), re.IGNORECASE).sub(
            lambda m: f"<mark>{m.group()}</mark>", sbj_esc
        )

    # ── Card row: checkbox + card ──────────────────────────────────────────────
    chk_col, card_col = st.columns([0.3, 9.7])
    with chk_col:
        st.markdown("<div style='padding-top:0.85rem;'></div>", unsafe_allow_html=True)
        # The checkbox key IS the source of truth — read initial value from the key itself
        # (which may have been set by Select All or a previous interaction).
        # We no longer sync back to a bare "chk_{idx}" key — that caused the one-render lag.
        current_val = st.session_state.get(f"{tab_id}_chk_{idx}", False)
        st.checkbox(
            "", value=current_val,
            key=f"{tab_id}_chk_{idx}",
            label_visibility="collapsed",
        )

    with card_col:
        st.markdown(f"""
        <div class='ecard {_CARD_CLS.get(cat,"c-oth")} fade-in' style='{card_opacity}'>
            <div class='ecard-from'>{sdr_esc}</div>
            <div class='ecard-subject' style='{subject_weight}'>{sbj_display}</div>
            <div style='display:flex;align-items:center;gap:8px;flex-wrap:wrap;'>
                {_pill(cat)}<span class='ecard-date'>{dt_esc}</span>{att_badge}{read_badge}
            </div>
        </div>
        """, unsafe_allow_html=True)

        with st.expander(f"↳  {sbj[:60]}"):
            summary = st.session_state.summaries.get(idx, "")

            # ── Original Email body ────────────────────────────────────────────
            body_txt = _strip_html((em.get("body") or "").strip())

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
                            color:var(--t1); line-height:1.78;'>{_html.escape(summary) if summary else "No summary available."}</div>
            </div>
            """, unsafe_allow_html=True)

            # ── Attachments ────────────────────────────────────────────────────
            if atts:
                # Split into images (render inline) and files (download cards)
                img_atts  = [a for a in atts if a["content_type"].startswith("image/")]
                file_atts = [a for a in atts if not a["content_type"].startswith("image/")]

                # ── Inline image viewer ────────────────────────────────────────
                if img_atts:
                    st.markdown("""
                    <div style='font-family:"Outfit",sans-serif; font-size:0.60rem; font-weight:800;
                                color:var(--t3); text-transform:uppercase; letter-spacing:0.12em;
                                margin-bottom:0.65rem;'>🖼️ IMAGES</div>
                    """, unsafe_allow_html=True)

                    # Show up to 3 images per row
                    for row_start in range(0, len(img_atts), 3):
                        row = img_atts[row_start:row_start + 3]
                        img_cols = st.columns(len(row))
                        for ci, att in enumerate(row):
                            with img_cols[ci]:
                                fname     = att["filename"]
                                fname_esc = _html.escape(fname[:30] + ("…" if len(fname) > 30 else ""))
                                size      = format_size(att["size"])

                                # Render the image itself
                                try:
                                    st.image(
                                        att["data"],
                                        caption=None,
                                        use_container_width=True,
                                    )
                                except Exception:
                                    # Corrupt / unsupported format — fall back to icon
                                    st.markdown(
                                        "<div style='text-align:center;font-size:2.5rem;padding:1rem;'>🖼️</div>",
                                        unsafe_allow_html=True,
                                    )

                                # Filename + size pill below image
                                st.markdown(f"""
                                <div style='text-align:center; margin-top:4px; margin-bottom:4px;'>
                                    <div style='font-family:"Outfit",sans-serif; font-size:0.75rem;
                                                color:var(--t2); font-weight:500;
                                                white-space:nowrap; overflow:hidden;
                                                text-overflow:ellipsis;'>{fname_esc}</div>
                                    <div style='font-family:"JetBrains Mono",monospace;
                                                font-size:0.62rem; color:var(--t3);'>{size}</div>
                                </div>
                                """, unsafe_allow_html=True)

                                st.download_button(
                                    "⬇ Download",
                                    data=att["data"],
                                    file_name=att["filename"],
                                    mime=att["content_type"],
                                    key=f"{tab_id}_dl_{idx}_img_{row_start + ci}",
                                    use_container_width=True,
                                )

                # ── Non-image file attachments ─────────────────────────────────
                if file_atts:
                    st.markdown("""
                    <div style='font-family:"Outfit",sans-serif; font-size:0.60rem; font-weight:800;
                                color:var(--t3); text-transform:uppercase; letter-spacing:0.12em;
                                margin-top:0.5rem; margin-bottom:0.65rem;'>📎 ATTACHMENTS</div>
                    """, unsafe_allow_html=True)
                    acols = st.columns(min(len(file_atts), 4))
                    for ai, att in enumerate(file_atts):
                        with acols[ai % 4]:
                            icon  = _att_icon(att["content_type"])
                            size  = format_size(att["size"])
                            fname = att["filename"]
                            ext   = fname.rsplit(".", 1)[-1].upper() if "." in fname else "FILE"
                            fname_esc   = _html.escape(fname)
                            ext_esc     = _html.escape(ext)
                            fname_short = _html.escape(fname[:24]) + ("…" if len(fname) > 24 else "")
                            st.markdown(f"""
                            <div style='background:var(--bg2); border:1px solid var(--b1);
                                        border-radius:11px; padding:1rem 0.9rem 0.7rem;
                                        text-align:center; margin-bottom:0.5rem;'>
                                <div style='font-size:2rem; margin-bottom:6px;'>{icon}</div>
                                <div style='display:inline-block; background:rgba(91,141,239,0.10);
                                            border:1px solid rgba(91,141,239,0.22); border-radius:4px;
                                            padding:1px 7px; font-family:"JetBrains Mono",monospace;
                                            font-size:0.60rem; font-weight:600; color:var(--blue2);
                                            margin-bottom:7px;'>{ext_esc}</div>
                                <div style='font-size:0.78rem; color:var(--t2); font-weight:500;
                                            word-break:break-all; margin-bottom:3px;
                                            font-family:"Outfit",sans-serif; line-height:1.4;'>
                                    {fname_short}</div>
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
                key=f"{tab_id}_reply_att_{idx}_{st.session_state.reply_att_gen.get(idx, 0)}",
            )

            if reply_files:
                _ext_icon = {
                    "pdf":"📄","doc":"📝","docx":"📝","xls":"📊","xlsx":"📊",
                    "ppt":"📋","pptx":"📋","zip":"🗜️","rar":"🗜️",
                    "jpg":"🖼️","jpeg":"🖼️","png":"🖼️","gif":"🖼️","webp":"🖼️",
                    "mp4":"🎬","mov":"🎬","mp3":"🎵","wav":"🎵",
                    "txt":"📃","csv":"📊","py":"🐍","js":"⚡",
                }
                n_rf      = len(reply_files)
                total_kb  = round(sum(f.size for f in reply_files) / 1024, 1)
                total_str = f"{total_kb} KB" if total_kb < 1024 else f"{round(total_kb/1024,1)} MB"

                # Header
                st.markdown(
                    f"<div style='background:var(--bg4);border:1px solid var(--b2);"
                    f"border-radius:9px 9px 0 0;padding:0.4rem 0.8rem;"
                    f"display:flex;justify-content:space-between;align-items:center;'>"
                    f"<span style='font-family:Outfit,sans-serif;font-size:0.64rem;font-weight:700;"
                    f"color:var(--t2);text-transform:uppercase;letter-spacing:0.08em;'>"
                    f"📎 {n_rf} attached</span>"
                    f"<span style='font-family:JetBrains Mono,monospace;font-size:0.64rem;"
                    f"color:var(--blue2);'>{total_str}</span>"
                    f"</div>",
                    unsafe_allow_html=True,
                )

                # One row per file
                for f in reply_files:
                    ext  = f.name.rsplit(".", 1)[-1].lower() if "." in f.name else ""
                    icon = _ext_icon.get(ext, "📎")
                    size = f"{round(f.size/1024,1)} KB" if f.size < 1048576 else f"{round(f.size/1048576,1)} MB"
                    name = f.name if len(f.name) <= 30 else f.name[:28] + "…"

                    ri_ic, ri_nm, ri_sz = st.columns([0.5, 6.5, 2])
                    with ri_ic:
                        st.markdown(
                            f"<div style='font-size:1.1rem;padding-top:5px;text-align:center;'>{icon}</div>",
                            unsafe_allow_html=True,
                        )
                    with ri_nm:
                        st.markdown(
                            f"<div style='font-family:Outfit,sans-serif;font-size:0.82rem;"
                            f"font-weight:500;color:var(--t1);padding-top:3px;"
                            f"white-space:nowrap;overflow:hidden;text-overflow:ellipsis;'>"
                            f"{_html.escape(name)}</div>",
                            unsafe_allow_html=True,
                        )
                    with ri_sz:
                        st.markdown(
                            f"<div style='font-family:JetBrains Mono,monospace;font-size:0.62rem;"
                            f"color:var(--t3);padding-top:5px;text-align:right;'>{size}</div>",
                            unsafe_allow_html=True,
                        )

                # Bottom cap
                st.markdown(
                    "<div style='border:1px solid var(--b2);border-top:none;"
                    "border-radius:0 0 9px 9px;height:4px;background:var(--bg3);'></div>",
                    unsafe_allow_html=True,
                )

            # Action buttons row
            st.markdown("<div style='height:0.4rem'></div>", unsafe_allow_html=True)
            b1, b2, b3, b4 = st.columns(4)
            with b1:
                if st.button("🔄", key=f"{tab_id}_regen_{idx}", help="Regenerate draft"):
                    with st.spinner("Regenerating…"):
                        result = ai_analyze_email(em["subject"], em["body"], regenerate=True)
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
                    _MAX_ATT = 25 * 1024 * 1024  # 25 MB — Gmail hard limit
                    oversized = [f.name for f in (reply_files or []) if f.size > _MAX_ATT]
                    if oversized:
                        st.error(f"Attachment(s) exceed the 25 MB limit: {', '.join(oversized)}")
                    else:
                        try:
                            send_email(
                                from_addr=email_addr, app_password=app_pass,
                                to_addr=em["from"],
                                subject=f"Re: {em['subject']}",
                                body=st.session_state.drafts[idx],
                                attachments=reply_files if reply_files else None,
                            )
                            st.session_state.sent_flags[idx] = True
                            st.session_state.reply_att_gen[idx] = st.session_state.reply_att_gen.get(idx, 0) + 1
                            st.session_state.inbox_reply_sent_msg = "✅ Reply sent!"
                            st.rerun()
                        except Exception as e:
                            msg = str(e).lower()
                            if "size" in msg or "large" in msg or "too big" in msg:
                                st.error(f"Failed to send: {e}")
                            elif "auth" in msg or "login" in msg or "password" in msg:
                                st.error("Failed to send: Authentication error. Please reconnect your account.")
                            else:
                                st.error("Failed to send reply. Please check your connection and try again.")
            with b3:
                if st.button("✍️", key=f"{tab_id}_fwd_{idx}", help="Open in Compose"):
                    st.session_state.compose_to   = em["from"]
                    st.session_state.compose_sub  = f"Re: {em['subject']}"
                    st.session_state.compose_body = st.session_state.drafts[idx]
                    st.session_state.current_page = "compose"
                    st.rerun()
            with b4:
                if st.button("🗑️ Delete", key=f"{tab_id}_del_{idx}", help="Delete this email",
                             use_container_width=True):
                    with st.spinner("Deleting…"):
                        delete_email(email_addr, app_pass, em["id"])
                    st.session_state.deleted_indices.add(idx)
                    _ALL_TAB_IDS_CARD = ["all", "imp", "pro", "upd", "oth"]
                    for _tid in _ALL_TAB_IDS_CARD:
                        st.session_state.pop(f"{_tid}_chk_{idx}", None)
                    st.rerun()
