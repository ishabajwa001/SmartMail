import imaplib
import email
import re
import smtplib
import mimetypes
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders


# ── HTML → clean plain text ────────────────────────────────────────────────────

def _html_to_text(html: str) -> str:
    """
    Convert HTML email body to clean readable plain text.
    Strips <style>, <script>, all tags, decodes entities, normalises whitespace.
    """
    # 1. Remove <style> blocks entirely (prevents CSS leaking into visible body)
    html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL | re.IGNORECASE)
    # 2. Remove <script> blocks
    html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)
    # 3. Remove HTML comments
    html = re.sub(r'<!--.*?-->', '', html, flags=re.DOTALL)
    # 4. Block-level tags → newlines so paragraphs are preserved
    for tag in ['p', 'br', 'div', 'tr', 'li', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'blockquote']:
        html = re.sub(rf'</?{tag}[^>]*>', '\n', html, flags=re.IGNORECASE)
    # 5. Strip ALL remaining tags
    html = re.sub(r'<[^>]+>', '', html)
    # 6. Decode HTML entities
    html = html.replace('&nbsp;', ' ')
    html = html.replace('&amp;',  '&')
    html = html.replace('&lt;',   '<')
    html = html.replace('&gt;',   '>')
    html = html.replace('&quot;', '"')
    html = html.replace('&#39;',  "'")
    html = html.replace('&apos;', "'")
    html = re.sub(r'&#(\d+);',            lambda m: chr(int(m.group(1))), html)
    html = re.sub(r'&#x([0-9a-fA-F]+);', lambda m: chr(int(m.group(1), 16)), html)
    # 7. Normalise whitespace
    html = re.sub(r'[ \t]+',  ' ',    html)   # collapse spaces/tabs
    html = re.sub(r' *\n *',  '\n',   html)   # trim around newlines
    html = re.sub(r'\n{3,}',  '\n\n', html)   # max one blank line
    return html.strip()


def _decode_body(raw: bytes) -> str:
    for enc in ("utf-8", "latin-1", "ascii", "windows-1252"):
        try:
            return raw.decode(enc)
        except Exception:
            continue
    return raw.decode("utf-8", errors="replace")


def _decode_header(value: str) -> str:
    if not value:
        return ""
    parts = email.header.decode_header(value)
    out = []
    for part, charset in parts:
        if isinstance(part, bytes):
            out.append(part.decode(charset or "utf-8", errors="replace"))
        else:
            out.append(part)
    return "".join(out)


def _parse_message(msg) -> dict:
    """
    Extract clean plain-text body and attachments.
    Prefers text/plain; falls back to stripping text/html properly.
    Never lets raw HTML, CSS or JS leak into the body string.
    """
    plain_body = ""
    html_body  = ""
    attachments = []

    if msg.is_multipart():
        for part in msg.walk():
            ct = part.get_content_type()
            cd = str(part.get("Content-Disposition", ""))

            if ct.startswith("multipart/"):
                continue

            if "attachment" in cd:
                raw = part.get_payload(decode=True)
                if raw:
                    filename = part.get_filename()
                    filename = (_decode_header(filename) if filename
                                else f"file{mimetypes.guess_extension(ct) or '.bin'}")
                    attachments.append({
                        "filename":     filename,
                        "content_type": ct,
                        "data":         raw,
                        "size":         len(raw),
                    })
            elif ct == "text/plain" and not plain_body:
                raw = part.get_payload(decode=True)
                if raw:
                    plain_body = _decode_body(raw)
            elif ct == "text/html" and not html_body:
                raw = part.get_payload(decode=True)
                if raw:
                    html_body = _decode_body(raw)
    else:
        ct  = msg.get_content_type()
        raw = msg.get_payload(decode=True)
        if raw:
            if ct == "text/html":
                html_body  = _decode_body(raw)
            else:
                plain_body = _decode_body(raw)

    # Prefer plain text; fall back to HTML-stripped
    if plain_body.strip():
        body = plain_body
    elif html_body.strip():
        body = _html_to_text(html_body)
    else:
        body = ""

    # Safety pass: if plain text still contains HTML tags, strip them too
    if body and re.search(r'<[a-zA-Z][^>]*>', body):
        body = _html_to_text(body)

    return {"body": body.strip(), "attachments": attachments}


# ── Fetch ──────────────────────────────────────────────────────────────────────

def fetch_emails(email_addr: str, app_password: str, limit: int = 20) -> list[dict]:
    """Fetch unread emails via IMAP without marking them as read (BODY.PEEK)."""
    import socket
    socket.setdefaulttimeout(30)

    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    try:
        mail.login(email_addr, app_password)
        mail.select("inbox", readonly=False)

        status, msgs = mail.search(None, "UNSEEN")
        if status != "OK" or not msgs[0]:
            return []

        ids = msgs[0].split()[-limit:]
        results = []
        for eid in ids:
            try:
                _, data = mail.fetch(eid, "(BODY.PEEK[])")
                for part in data:
                    if isinstance(part, tuple):
                        msg = email.message_from_bytes(part[1])
                        parsed = _parse_message(msg)
                        results.append({
                            "id":          eid,
                            "from":        _decode_header(msg.get("from", "Unknown")),
                            "subject":     _decode_header(msg.get("subject", "(No Subject)")),
                            "date":        msg.get("date", ""),
                            "body":        parsed["body"],
                            "attachments": parsed["attachments"],
                        })
            except Exception:
                continue

        return results
    finally:
        try:
            mail.logout()
        except Exception:
            pass


# ── Send ───────────────────────────────────────────────────────────────────────

def delete_email(email_addr: str, app_password: str, email_id: bytes) -> bool:
    """Permanently delete an email from Gmail by its IMAP ID."""
    import socket
    socket.setdefaulttimeout(20)
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(email_addr, app_password)
        mail.select("inbox", readonly=False)
        # Mark as deleted then expunge
        mail.store(email_id, "+FLAGS", "\\Deleted")
        mail.expunge()
        mail.logout()
        return True
    except Exception:
        return False



def send_email(
    from_addr: str,
    app_password: str,
    to_addr: str,
    subject: str,
    body: str,
    attachments=None,
) -> None:
    msg = MIMEMultipart("mixed")
    msg["Subject"] = subject
    msg["From"]    = from_addr
    msg["To"]      = to_addr
    msg.attach(MIMEText(body, "plain", "utf-8"))

    if attachments:
        for att in attachments:
            if hasattr(att, "read"):
                att.seek(0)
                file_data    = att.read()
                filename     = att.name
                content_type = att.type or "application/octet-stream"
            else:
                file_data    = att["data"]
                filename     = att["filename"]
                content_type = att.get("content_type", "application/octet-stream")

            main, sub = (content_type.split("/", 1) if "/" in content_type
                         else ("application", "octet-stream"))
            part = MIMEBase(main, sub)
            part.set_payload(file_data)
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", "attachment", filename=filename)
            msg.attach(part)

    recipients = [a.strip() for a in to_addr.split(",") if a.strip()]
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(from_addr, app_password)
        server.sendmail(from_addr, recipients, msg.as_string())


def format_size(n: int) -> str:
    if n < 1024:       return f"{n} B"
    if n < 1024 ** 2:  return f"{n / 1024:.1f} KB"
    return f"{n / 1024 ** 2:.1f} MB"
