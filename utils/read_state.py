"""
Persistent read-state store.

Saves read email IDs to a local JSON file so the "read" badge
survives page reloads and new browser sessions.

Storage: .smartmail_read.json  (next to agent.py / working dir)
"""
from __future__ import annotations
import json
import os

_STORE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".smartmail_read.json")


def _load() -> set[str]:
    try:
        with open(_STORE_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, list):
            return set(data)
    except (FileNotFoundError, json.JSONDecodeError):
        pass
    return set()


def _save(ids: set[str]) -> None:
    try:
        with open(_STORE_PATH, "w", encoding="utf-8") as f:
            json.dump(sorted(ids), f)
    except OSError:
        pass  # read-only filesystem — degrade silently


def _normalise(email_id) -> str:
    if isinstance(email_id, bytes):
        email_id = email_id.decode("utf-8", errors="replace")
    return str(email_id)


def is_read(email_id) -> bool:
    """Return True if this email ID has been marked read in any previous session."""
    return _normalise(email_id) in _load()


def mark_read(email_id) -> None:
    """Persist this email ID as read."""
    email_id = _normalise(email_id)
    ids = _load()
    if email_id not in ids:
        ids.add(email_id)
        _save(ids)


def mark_unread(email_id) -> None:
    """Remove read flag for this email ID."""
    email_id = _normalise(email_id)
    ids = _load()
    if email_id in ids:
        ids.discard(email_id)
        _save(ids)


def bulk_read_ids() -> set[str]:
    """Return the full set of read email IDs (for bulk checks at render time)."""
    return _load()
