import streamlit as st


def init_state():
    defaults = {
        "credentials_ok": False,
        "model":          None,

        "emails":           [],
        "fetched":          False,
        "categories":       {},
        "summaries":        {},
        "drafts":           {},
        "sent_flags":       {},
        "reply_att_gen":    {},   # per-email counter — incremented on send to reset file uploader
        "deleted_indices":  set(),   # soft-deleted email indices

        "current_page": "inbox",

        "compose_to":    "",
        "compose_sub":   "",
        "compose_body":  "",
        "ai_draft_text": "",
        "compose_gen":   0,   # incremented on each AI generate to force widget refresh
        "gemini_model_name": "",
        "model_fallbacks":   [],

        "inbox_sort":   "Newest First",
        "inbox_search": "",
        "inbox_group":  "None",

        # Compose: persist success/error messages across rerun
        "compose_sent_msg":  "",
        "compose_error_msg": "",

        # Inbox: persist reply-sent and inbox-zero flash messages across rerun
        "inbox_reply_sent_msg": "",
        "inbox_flash_msg":      "",
        # Inbox: two-step bulk delete confirmation flag
        "bulk_delete_confirm":  False,

        # Support: counter to reset text area widget
        "support_form_key": 0,
        # Support: persist feedback message across rerun
        "support_flash_msg": "",
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val
