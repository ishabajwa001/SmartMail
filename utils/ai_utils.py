import streamlit as st
import google.generativeai as genai

CATEGORIES = ["Important", "Promotions", "Updates", "Others"]


def _call(prompt: str) -> str:
    """Call the current model, auto-falling back through available models on quota errors."""
    model = st.session_state.get("model")
    if not model:
        return "[error] No model connected. Please click Connect Account in the sidebar."

    try:
        return model.generate_content(prompt).text.strip()
    except Exception as e:
        msg = str(e)
        if "429" not in msg and "quota" not in msg.lower() and "rate" not in msg.lower():
            return f"[error] {msg}"

    # Quota hit — try next model in fallback list
    fallbacks = st.session_state.get("model_fallbacks", [])
    current   = st.session_state.get("gemini_model_name", "")
    remaining = fallbacks[fallbacks.index(current) + 1:] if current in fallbacks else []

    for next_model in remaining:
        try:
            m = genai.GenerativeModel(next_model)
            result = m.generate_content(prompt).text.strip()
            # Promote this model as the new active one
            st.session_state.model = m
            st.session_state.gemini_model_name = next_model
            return result
        except Exception as e2:
            if "429" in str(e2) or "quota" in str(e2).lower():
                continue   # this one is also exhausted, try next
            return f"[error] {e2}"

    return "[quota] All available models have hit their daily limit. Please use a new API key."


def ai_analyze_email(subject: str, body: str) -> dict:
    """
    Single API call → returns category, summary, and draft reply.
    """
    prompt = f"""You are an email assistant helping the RECIPIENT of the email below.

IMPORTANT RULES:
- The SUMMARY must ONLY describe what is literally written in the email. Do NOT invent, assume, or infer anything not explicitly stated (e.g. do not mention attachments, links, or resumes unless they are explicitly mentioned in the email text).
- The DRAFT is a reply written BY the recipient (the person reading this email), responding TO the sender. Do not confuse the roles.
- The DRAFT must use proper paragraphs with blank lines between them. Use **bold** only for key labels if needed. Start with "Hi [Sender's Name]," and end with "Best regards,\\n[Your Name]".
- Output EXACTLY this format, no extra text:

CATEGORY: <one of: Important, Promotions, Updates, Others>
SUMMARY: <2 sentences describing only what the email explicitly says>
DRAFT: <the recipient's reply to the sender>

---
Subject: {subject}
Body:
{body[:1500]}
"""
    raw = _call(prompt)
    return _parse_analysis(raw)


def _parse_analysis(raw: str) -> dict:
    result = {"category": "Others", "summary": "", "draft": ""}
    if not raw:
        return result

    lines = raw.strip().splitlines()
    draft_lines = []
    in_draft = False

    for line in lines:
        if line.startswith("CATEGORY:"):
            val = line.split(":", 1)[1].strip()
            result["category"] = val if val in CATEGORIES else "Others"

        elif line.startswith("SUMMARY:"):
            result["summary"] = line.split(":", 1)[1].strip()

        elif line.startswith("DRAFT:"):
            draft_lines.append(line.split(":", 1)[1].strip())
            in_draft = True

        elif in_draft:
            draft_lines.append(line)

    result["draft"] = "\n".join(draft_lines).strip()
    return result


def ai_compose(brief: str) -> str:
    """Compose a full email from a short brief."""
    return _call(
        f"You are an expert email writer. Read the brief carefully and write the email.\n"
        f"\n"
        f"TONE DETECTION — read the brief and decide the tone automatically:\n"
        f"- If the brief mentions casual words, friends, family, informal context → write casually, like texting a friend\n"
        f"- If the brief mentions work, job, client, professor, manager, formal context → write professionally and formally\n"
        f"- If the brief specifies a tone explicitly (e.g. 'friendly', 'professional', 'urgent') → follow it exactly\n"
        f"\n"
        f"CRITICAL RULES:\n"
        f"- Follow the brief EXACTLY — if they say 5 lines, write 5 lines. If they say short, write short.\n"
        f"- NO placeholders like [Name] or [Company] — if a detail is missing, make a natural assumption.\n"
        f"- NO markdown, bullet points, asterisks, or formatting symbols.\n"
        f"- Casual tone: relaxed language, contractions (I'm, I'll, it's), warm and natural.\n"
        f"- Formal tone: polished language, full sentences, respectful but not stiff.\n"
        f"- Sign-off must match the tone — casual: 'Talk soon,' / 'Cheers,' / 'See you,' — formal: 'Kind regards,' / 'Sincerely,' / 'Looking forward to hearing from you,'\n"
        f"- NEVER reference, quote, or imply any previous emails or conversations unless the brief explicitly mentions them. Treat every email as the first contact unless told otherwise.\n"
        f"- First line must be: Subject: <subject>\n"
        f"- Then a blank line, then the email body.\n"
        f"\n"
        f"Brief: {brief[:800]}"
    )


def parse_draft(draft_text: str) -> tuple[str, str]:
    """Split AI-composed email into (subject, body).
    Handles markdown fences, missing blank lines, and empty bodies.
    """
    if not draft_text or not draft_text.strip():
        return "", ""

    text = draft_text.strip()

    # Strip markdown code fences if Gemini wrapped output
    if text.startswith("```"):
        lines_raw = text.splitlines()
        # Remove opening fence
        lines_raw = lines_raw[1:]
        # Remove closing fence
        if lines_raw and lines_raw[-1].strip().startswith("```"):
            lines_raw = lines_raw[:-1]
        text = "\n".join(lines_raw).strip()

    lines = text.splitlines()
    subject = ""
    body_start = 0
    found_subject = False

    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.lower().startswith("subject:"):
            subject = stripped.split(":", 1)[1].strip()
            body_start = i + 1
            found_subject = True
            break

    if not found_subject:
        # No subject line found — return everything as body
        return "", text

    # Skip any blank lines between subject and body
    while body_start < len(lines) and not lines[body_start].strip():
        body_start += 1

    body = "\n".join(lines[body_start:]).strip()

    # Fallback: if body somehow empty but we have text after subject, grab raw remainder
    if not body and body_start < len(lines):
        body = "\n".join(lines[body_start:])

    return subject, body
