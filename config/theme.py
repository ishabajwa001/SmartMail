CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Beiruti:wght@300;400;500;600;700;800;900&family=Outfit:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

/* ══════════════════════════════════════════════════
   SMARTMAIL · GREY-BLACK THEME
   Beiruti Display · Outfit Body · JetBrains Mono
   ══════════════════════════════════════════════════ */
:root {
    /* ── Backgrounds — grey-black palette ── */
    --bg:     #0e0e0e;
    --bg2:    #161616;
    --bg3:    #1e1e1e;
    --bg4:    #262626;

    /* ── Borders ── */
    --b1:     #2e2e2e;
    --b2:     #3a3a3a;

    /* ── Text ── */
    --t1:     #f0f0f0;
    --t2:     #a0a0a0;
    --t3:     #606060;

    /* ── Accents — muted but distinct ── */
    --blue:   #5b8def;
    --blue2:  #8ab0f5;
    --violet: #9b6dff;
    --violet2:#c4a0ff;
    --coral:  #e05c6c;
    --coral2: #f09aaa;
    --cyan:   #3ac0d8;
    --cyan2:  #7dd8eb;
    --mint:   #3dd68c;
    --gold:   #d4a017;
    --gold2:  #e8c566;

    /* ── Legacy aliases ── */
    --em:     var(--blue);
    --em2:    var(--blue2);
    --am:     var(--violet);
    --am2:    var(--violet2);
    --co:     var(--coral);
    --co2:    var(--coral2);
    --sky:    var(--cyan);
    --sky2:   var(--cyan2);
    --text:   var(--t1);

    /* ── Glow — subtle ── */
    --glow-blue:   rgba(91,141,239,0.18);
    --glow-violet: rgba(155,109,255,0.14);
    --glow-coral:  rgba(224,92,108,0.16);
    --glow-cyan:   rgba(58,192,216,0.14);
}

/* ── Reset & Base ────────────────────────────────── */
*, *::before, *::after { box-sizing: border-box; }

html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg) !important;
    color: var(--t1) !important;
    font-family: 'Outfit', sans-serif;
}

/* ── Subtle Grey Ambient Background ─────────────── */
[data-testid="stAppViewContainer"]::before {
    content: '';
    position: fixed; inset: 0; pointer-events: none; z-index: 0;
    background:
        radial-gradient(ellipse 70% 50% at -10%  -5%,  rgba(91,141,239,0.07) 0%, transparent 60%),
        radial-gradient(ellipse 50% 45% at 110% 105%,  rgba(155,109,255,0.05) 0%, transparent 60%);
}

/* ── SVG Grain Texture ───────────────────────────── */
[data-testid="stAppViewContainer"]::after {
    content: '';
    position: fixed; inset: 0; pointer-events: none; z-index: 1; opacity: 0.018;
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 512 512' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.75' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
    background-size: 200px 200px;
}

/* ── Chrome ──────────────────────────────────────── */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stMain"] { padding: 0 !important; }
.block-container { padding: 2rem 3rem !important; max-width: 1440px !important; }
[data-testid="InputInstructions"] { display: none !important; }

/* ══════════════════════════════════════════════════
   SIDEBAR
   ══════════════════════════════════════════════════ */
[data-testid="stSidebar"] {
    background: #0a0a0a !important;
    border-right: 1px solid var(--b1) !important;
}
[data-testid="stSidebar"] > div { padding: 0 !important; }

[data-testid="stSidebar"] .stTextInput input {
    background: var(--bg3) !important;
    border: 1px solid var(--b1) !important;
    border-radius: 8px !important;
    color: var(--t1) !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 0.88rem !important;
    padding: 0.45rem 0.78rem !important;
    transition: border-color 0.25s, box-shadow 0.25s, background 0.25s !important;
}
[data-testid="stSidebar"] .stTextInput input:focus {
    border-color: var(--blue) !important;
    box-shadow: 0 0 0 3px rgba(61,142,255,0.20) !important;
    background: var(--bg4) !important;
    outline: none !important;
}
[data-testid="stSidebar"] .stTextInput label {
    color: var(--t2) !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 0.68rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.10em !important;
    text-transform: uppercase !important;
}

/* ══════════════════════════════════════════════════
   MAIN INPUTS — consistent height & style everywhere
   ══════════════════════════════════════════════════ */

/* Labels — identical across all input types */
.stTextInput label,
.stTextArea label,
.stSelectbox label {
    color: var(--t2) !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 0.68rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.09em !important;
    text-transform: uppercase !important;
    margin-bottom: 4px !important;
}

/* Text input */
.stTextInput input {
    background: var(--bg2) !important;
    border: 1px solid var(--b1) !important;
    border-radius: 9px !important;
    color: var(--t1) !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 0.88rem !important;
    height: 42px !important;
    padding: 0 0.9rem !important;
    transition: border-color 0.22s, box-shadow 0.22s, background 0.22s !important;
}
.stTextInput input:focus {
    border-color: var(--blue) !important;
    box-shadow: 0 0 0 2px rgba(91,141,239,0.18) !important;
    background: var(--bg3) !important;
    outline: none !important;
}

/* Selectbox — same height as text input */
.stSelectbox [data-baseweb="select"] > div {
    background: var(--bg2) !important;
    border: 1px solid var(--b1) !important;
    border-radius: 9px !important;
    color: var(--t1) !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 0.88rem !important;
    min-height: 42px !important;
    transition: border-color 0.22s, box-shadow 0.22s !important;
}
.stSelectbox [data-baseweb="select"] > div:hover { border-color: var(--b2) !important; }
.stSelectbox [data-baseweb="select"] > div:focus-within {
    border-color: var(--blue) !important;
    box-shadow: 0 0 0 2px rgba(91,141,239,0.16) !important;
}

/* Textarea — draft/compose areas */
.stTextArea textarea {
    background: var(--bg3) !important;
    border: 1px solid var(--b1) !important;
    border-left: 3px solid var(--blue) !important;
    border-radius: 9px !important;
    color: var(--t1) !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 0.88rem !important;
    line-height: 1.72 !important;
    padding: 0.85rem 1rem !important;
    transition: border-color 0.22s, box-shadow 0.22s !important;
}
.stTextArea textarea:focus {
    border-color: var(--blue) !important;
    box-shadow: 0 0 0 2px rgba(91,141,239,0.16) !important;
    outline: none !important;
}

/* Dropdown popover list */
[data-baseweb="popover"] [role="listbox"] {
    background: var(--bg3) !important;
    border: 1px solid var(--b2) !important;
    border-radius: 11px !important;
    box-shadow: 0 12px 40px rgba(0,0,0,0.55) !important;
}
[data-baseweb="popover"] [role="option"] {
    background: transparent !important;
    color: var(--t2) !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 0.86rem !important;
    padding: 0.5rem 0.95rem !important;
    transition: background 0.14s !important;
}
[data-baseweb="popover"] [role="option"]:hover { background: rgba(91,141,239,0.10) !important; color: var(--t1) !important; }
[data-baseweb="popover"] [aria-selected="true"] { background: rgba(91,141,239,0.16) !important; color: var(--blue2) !important; }

/* Tighten column gaps in toolbar rows */
[data-testid="stHorizontalBlock"] { gap: 0.6rem !important; align-items: flex-start !important; }

/* ══════════════════════════════════════════════════
   BUTTONS — grey-black with blue accent
   ══════════════════════════════════════════════════ */
.stButton > button {
    background: linear-gradient(135deg, #1c1c1c 0%, #242424 100%) !important;
    color: var(--blue2) !important;
    border: 1px solid rgba(91,141,239,0.35) !important;
    border-radius: 10px !important;
    font-family: 'Outfit', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.86rem !important;
    letter-spacing: 0.03em !important;
    padding: 0.6rem 1.2rem !important;
    width: 100% !important;
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
    box-shadow: 0 2px 10px rgba(91,141,239,0.14), inset 0 1px 0 rgba(255,255,255,0.04) !important;
    position: relative !important;
    overflow: hidden !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #262626 0%, #2e2e2e 100%) !important;
    border-color: rgba(91,141,239,0.60) !important;
    box-shadow: 0 0 0 1px rgba(91,141,239,0.25), 0 8px 24px rgba(91,141,239,0.25), inset 0 1px 0 rgba(255,255,255,0.06) !important;
    transform: translateY(-2px) !important;
    color: #fff !important;
}
.stButton > button:active { transform: translateY(0) scale(0.98) !important; }
.stButton > button:disabled {
    background: var(--bg3) !important;
    color: var(--t3) !important;
    border-color: var(--b1) !important;
    box-shadow: none !important;
    transform: none !important;
}

/* ══════════════════════════════════════════════════
   ALERTS
   ══════════════════════════════════════════════════ */
.stSuccess { background: rgba(0,255,176,0.07) !important; border: 1px solid rgba(0,255,176,0.28) !important; border-radius: 10px !important; color: #6effd9 !important; }
.stError   { background: rgba(255,61,107,0.07) !important; border: 1px solid rgba(255,61,107,0.28) !important; border-radius: 10px !important; }
.stInfo    { background: rgba(61,142,255,0.07) !important; border: 1px solid rgba(61,142,255,0.28) !important; border-radius: 10px !important; }
.stWarning { background: rgba(255,190,0,0.07)  !important; border: 1px solid rgba(255,190,0,0.28)  !important; border-radius: 10px !important; }

/* ══════════════════════════════════════════════════
   TABS — interactive with animated indicator
   ══════════════════════════════════════════════════ */
.stTabs [role="tablist"] {
    background: var(--bg2);
    border: 1px solid var(--b1);
    border-radius: 12px;
    padding: 5px;
    gap: 3px;
}
.stTabs [role="tab"] {
    background: transparent !important;
    color: var(--t3) !important;
    border-radius: 8px !important;
    border: none !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 0.82rem !important;
    font-weight: 600 !important;
    padding: 0.42rem 1.1rem !important;
    transition: all 0.20s ease !important;
    position: relative !important;
}
.stTabs [role="tab"]:hover {
    color: var(--t2) !important;
    background: rgba(255,255,255,0.04) !important;
}
.stTabs [role="tab"][aria-selected="true"] {
    background: linear-gradient(135deg, rgba(61,142,255,0.22), rgba(61,142,255,0.10)) !important;
    color: var(--blue2) !important;
    box-shadow: inset 0 0 0 1px rgba(61,142,255,0.38), 0 2px 10px rgba(61,142,255,0.15) !important;
}
.stTabs [data-baseweb="tab-panel"] { padding-top: 1.3rem !important; }

/* ══════════════════════════════════════════════════
   EXPANDERS
   ══════════════════════════════════════════════════ */
details {
    background: var(--bg2) !important;
    border: 1px solid var(--b1) !important;
    border-radius: 11px !important;
    margin-bottom: 0.55rem !important;
    overflow: hidden !important;
    transition: border-color 0.25s, box-shadow 0.25s !important;
}
details summary {
    color: var(--t2) !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 0.88rem !important;
    font-weight: 500 !important;
    padding: 0.78rem 1.1rem !important;
    cursor: pointer !important;
    transition: color 0.18s, background 0.18s !important;
}
details summary:hover {
    color: var(--t1) !important;
    background: rgba(255,255,255,0.02) !important;
}
details[open] {
    border-color: rgba(61,142,255,0.35) !important;
    box-shadow: 0 4px 20px rgba(61,142,255,0.08) !important;
}

/* ══════════════════════════════════════════════════
   SIDEBAR NAV
   ══════════════════════════════════════════════════ */
[data-testid="stSidebar"] .stRadio > label { display: none !important; }
[data-testid="stSidebar"] .stRadio [role="radiogroup"] { gap: 2px !important; }
[data-testid="stSidebar"] .stRadio [data-baseweb="radio"] {
    background: transparent !important;
    border-radius: 9px !important;
    padding: 0.55rem 1.1rem !important;
    transition: all 0.20s ease !important;
    border-left: 2px solid transparent !important;
}
[data-testid="stSidebar"] .stRadio [data-baseweb="radio"]:hover {
    background: rgba(61,142,255,0.09) !important;
}
[data-testid="stSidebar"] .stRadio [data-baseweb="radio"][aria-checked="true"] {
    background: linear-gradient(90deg, rgba(61,142,255,0.14), rgba(61,142,255,0.05)) !important;
    border-left-color: var(--blue) !important;
    box-shadow: inset 0 0 0 1px rgba(61,142,255,0.12) !important;
}
[data-testid="stSidebar"] .stRadio label {
    color: var(--t2) !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 0.90rem !important;
    font-weight: 500 !important;
    letter-spacing: 0 !important;
    text-transform: none !important;
    transition: color 0.18s !important;
}
[data-testid="stSidebar"] .stRadio [aria-checked="true"] label {
    color: var(--t1) !important;
    font-weight: 700 !important;
}

/* Sidebar Connect button — grey accent */
[data-testid="stSidebar"] .stButton > button {
    background: linear-gradient(135deg, #1e1e1e 0%, #2a2a2a 100%) !important;
    color: var(--blue2) !important;
    border: 1px solid rgba(91,141,239,0.35) !important;
    box-shadow: 0 2px 14px rgba(91,141,239,0.12) !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background: linear-gradient(135deg, #2a2a2a 0%, #363636 100%) !important;
    border-color: rgba(91,141,239,0.60) !important;
    box-shadow: 0 0 0 1px rgba(91,141,239,0.25), 0 8px 24px rgba(91,141,239,0.20) !important;
    color: #fff !important;
}

/* ══════════════════════════════════════════════════
   SCROLLBAR
   ══════════════════════════════════════════════════ */
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--b2); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #3a4a88; }

/* ══════════════════════════════════════════════════
   FILE UPLOADER
   ══════════════════════════════════════════════════ */
[data-testid="stFileUploader"] {
    background: var(--bg2) !important;
    border: 1px dashed var(--b2) !important;
    border-radius: 10px !important;
    transition: border-color 0.25s, background 0.25s, box-shadow 0.25s !important;
}
[data-testid="stFileUploader"]:hover {
    border-color: var(--blue) !important;
    background: rgba(61,142,255,0.04) !important;
    box-shadow: 0 0 20px rgba(61,142,255,0.10) !important;
}
[data-testid="stFileUploader"] label {
    color: var(--t2) !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 0.70rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.10em !important;
    text-transform: uppercase !important;
}
[data-testid="stFileUploader"] section { background: transparent !important; border: none !important; }
[data-testid="stFileUploader"] small { color: var(--t3) !important; }

/* ══════════════════════════════════════════════════
   DOWNLOAD BUTTON
   ══════════════════════════════════════════════════ */
[data-testid="stDownloadButton"] > button {
    background: var(--bg3) !important;
    color: var(--blue2) !important;
    border: 1px solid rgba(61,142,255,0.28) !important;
    border-radius: 8px !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 0.76rem !important;
    font-weight: 600 !important;
    padding: 0.32rem 0.70rem !important;
    box-shadow: none !important;
    transition: all 0.20s ease !important;
}
[data-testid="stDownloadButton"] > button:hover {
    background: rgba(61,142,255,0.10) !important;
    border-color: rgba(61,142,255,0.52) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 14px rgba(61,142,255,0.20) !important;
}

/* ══════════════════════════════════════════════════
   PROGRESS BAR
   ══════════════════════════════════════════════════ */
.stProgress > div > div {
    background: linear-gradient(90deg, var(--blue), var(--cyan)) !important;
    border-radius: 4px !important;
    box-shadow: 0 0 8px rgba(61,142,255,0.40) !important;
}
.stProgress > div { background: var(--bg3) !important; border-radius: 4px !important; }

/* ══════════════════════════════════════════════════
   MISC
   ══════════════════════════════════════════════════ */
.stCheckbox label span { color: var(--t2) !important; font-size: 0.88rem !important; font-weight: 500 !important; }
hr { border-color: var(--b1) !important; margin: 1.4rem 0 !important; }
mark {
    background: rgba(184,92,255,0.25) !important;
    color: var(--violet2) !important;
    border-radius: 3px !important;
    padding: 0 3px !important;
}
.stCodeBlock { background: var(--bg2) !important; border: 1px solid var(--b1) !important; border-radius: 10px !important; }

/* Reset <p> margins inside markdown blocks so email bodies don't double-space */
.stMarkdown p { margin: 0 !important; padding: 0 !important; }

/* ══════════════════════════════════════════════════
   COMPONENT CLASSES
   ══════════════════════════════════════════════════ */

/* Page Heading */
.page-title {
    font-family: 'Beiruti', sans-serif;
    font-size: 2.8rem;
    font-weight: 900;
    color: var(--t1);
    line-height: 1.1;
    margin-bottom: 0.4rem;
    letter-spacing: -0.02em;
}
.page-title span {
    background: linear-gradient(120deg, var(--blue) 0%, var(--cyan) 45%, var(--violet) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.page-sub {
    color: var(--t2);
    font-size: 0.93rem;
    margin-bottom: 1.8rem;
    line-height: 1.65;
    font-weight: 400;
}

/* ── Email Cards — lighter, tighter ──────────────────── */
.ecard {
    background: var(--bg2);
    border: 1px solid var(--b1);
    border-left: 3px solid transparent;
    border-radius: 9px;
    padding: 0.7rem 1.1rem;
    margin-bottom: 0.4rem;
    transition: border-color 0.18s ease, background 0.18s ease;
    cursor: default;
}
.ecard:hover {
    border-color: var(--b2);
    background: var(--bg3);
}
.ecard.c-imp { border-left-color: var(--coral);  }
.ecard.c-pro { border-left-color: var(--blue);   }
.ecard.c-upd { border-left-color: var(--cyan);   }
.ecard.c-oth { border-left-color: var(--violet); }

.ecard-from    { font-family: 'Outfit', sans-serif; font-size: 0.72rem; color: var(--t3); margin-bottom: 3px; }
.ecard-subject { font-family: 'Outfit', sans-serif; font-size: 0.95rem; color: var(--t1); margin-bottom: 5px; font-weight: 600; }
.ecard-date    { font-family: 'JetBrains Mono', monospace; font-size: 0.68rem; color: var(--t3); }

/* ── Category Pills ───────────────────────────────── */
.cpill {
    display: inline-flex; align-items: center; gap: 4px;
    padding: 2px 10px; border-radius: 20px;
    font-family: 'Outfit', sans-serif;
    font-size: 0.63rem; font-weight: 700;
    letter-spacing: 0.07em; text-transform: uppercase;
}
.cp-imp { background: rgba(255,61,107,0.10);  color: var(--coral2);  border: 1px solid rgba(255,61,107,0.28); }
.cp-pro { background: rgba(61,142,255,0.10);  color: var(--blue2);   border: 1px solid rgba(61,142,255,0.28); }
.cp-upd { background: rgba(0,217,255,0.10);   color: var(--cyan2);   border: 1px solid rgba(0,217,255,0.28); }
.cp-oth { background: rgba(184,92,255,0.10);  color: var(--violet2); border: 1px solid rgba(184,92,255,0.28); }

/* ── Chip Label ──────────────────────────────────── */
.chip {
    display: inline-flex; align-items: center; gap: 5px;
    background: rgba(61,142,255,0.08);
    border: 1px solid rgba(61,142,255,0.24);
    border-radius: 6px; padding: 3px 11px;
    font-family: 'Outfit', sans-serif;
    font-size: 0.65rem; font-weight: 700;
    color: var(--blue2); letter-spacing: 0.08em; text-transform: uppercase;
    margin-bottom: 0.55rem; width: fit-content;
}

/* ── Stat Cards ──────────────────────────────────── */
.stat-card {
    background: var(--bg2);
    border: 1px solid var(--b1);
    border-radius: 10px;
    padding: 0.75rem 1rem;
    text-align: center;
    margin-bottom: 0.8rem;
    transition: border-color 0.22s, box-shadow 0.22s, transform 0.22s;
}
.stat-card:hover {
    border-color: var(--b2);
    box-shadow: 0 4px 18px rgba(0,0,0,0.30);
    transform: translateY(-2px);
}
.stat-card-val {
    font-family: 'Beiruti', sans-serif;
    font-size: 0.92rem; font-weight: 700;
    letter-spacing: 0.02em;
}

/* ── Status Badges ───────────────────────────────── */
.badge-ok {
    display: flex; align-items: center; gap: 8px;
    background: rgba(0,255,176,0.08);
    border: 1px solid rgba(0,255,176,0.28);
    border-radius: 9px; padding: 0.50rem 0.95rem;
    font-size: 0.84rem; color: #6effd9;
    margin-top: 0.5rem;
    font-family: 'Outfit', sans-serif; font-weight: 500;
}
.badge-err {
    display: flex; align-items: center; gap: 8px;
    background: rgba(255,61,107,0.08);
    border: 1px solid rgba(255,61,107,0.28);
    border-radius: 9px; padding: 0.50rem 0.95rem;
    font-size: 0.84rem; color: var(--coral2);
    margin-top: 0.5rem;
    font-family: 'Outfit', sans-serif; font-weight: 500;
}
.dot {
    width: 7px; height: 7px; border-radius: 50%;
    background: var(--mint);
    box-shadow: 0 0 8px var(--mint);
    display: inline-block;
    animation: pulse-dot 2.2s infinite;
}
@keyframes pulse-dot {
    0%, 100% { opacity: 1; box-shadow: 0 0 8px var(--mint); }
    50%       { opacity: 0.2; box-shadow: 0 0 3px var(--mint); }
}

/* ── Sidebar Section Label ───────────────────────── */
.slbl {
    font-family: 'Outfit', sans-serif;
    font-size: 0.64rem;
    color: var(--t2);
    text-transform: uppercase;
    letter-spacing: 0.14em;
    font-weight: 700;
    padding: 1rem 1.1rem 0.38rem;
    display: flex; align-items: center; gap: 8px;
}
.slbl::after {
    content: ''; flex: 1; height: 1px;
    background: linear-gradient(90deg, var(--b2), transparent);
}

/* ── Empty State ─────────────────────────────────── */
.empty { text-align: center; padding: 5rem 2rem; animation: fadeUp 0.4s ease; }
.empty-icon { font-size: 3.2rem; margin-bottom: 0.8rem; }
.empty-title { font-family: 'Beiruti', sans-serif; font-size: 2.1rem; font-weight: 800; color: var(--t1); margin-bottom: 0.5rem; }
.empty-sub { color: var(--t2); font-size: 0.92rem; line-height: 1.7; }

/* ── AI Panel ────────────────────────────────────── */
.ai-panel {
    background: linear-gradient(145deg, #0f1730, #080d1e);
    border: 1px solid rgba(61,142,255,0.24);
    border-radius: 13px; padding: 1.4rem;
    box-shadow: inset 0 1px 0 rgba(61,142,255,0.10);
}
.ai-title {
    font-family: 'Beiruti', sans-serif;
    font-size: 1.3rem; font-weight: 800;
    color: var(--blue2); margin-bottom: 5px;
}
.ai-sub { font-size: 0.87rem; color: var(--t2); margin-bottom: 1rem; line-height: 1.6; }

/* ── Settings Cards ──────────────────────────────── */
.set-card {
    background: var(--bg2);
    border: 1px solid var(--b1);
    border-radius: 13px;
    padding: 1.6rem 1.7rem;
    transition: border-color 0.25s, box-shadow 0.25s, transform 0.25s;
    height: 100%;
}
.set-card:hover {
    border-color: rgba(61,142,255,0.30);
    box-shadow: 0 8px 32px rgba(0,0,0,0.35);
    transform: translateY(-2px);
}
.set-card h4 {
    font-family: 'Beiruti', sans-serif;
    font-weight: 800;
    color: var(--t1);
    margin: 0 0 0.8rem 0;
    font-size: 1.22rem;
}
.set-card p {
    color: var(--t2) !important;
    font-size: 0.90rem !important;
    line-height: 1.75 !important;
    margin-bottom: 0.8rem !important;
}
.set-card ol, .set-card ul {
    color: var(--t2) !important;
    font-size: 0.89rem !important;
    line-height: 1.9 !important;
    padding-left: 1.2rem !important;
    margin-bottom: 0 !important;
}
.set-card li { margin-bottom: 0.15rem !important; }
.set-card a {
    color: var(--blue2) !important;
    text-decoration: none !important;
    border-bottom: 1px solid rgba(61,142,255,0.32) !important;
    transition: color 0.18s, border-color 0.18s !important;
}
.set-card a:hover { color: var(--cyan2) !important; border-bottom-color: var(--cyan) !important; }
.set-card code {
    background: var(--bg3) !important;
    color: var(--violet2) !important;
    padding: 2px 7px !important;
    border-radius: 5px !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.82rem !important;
    border: 1px solid var(--b1) !important;
}
.set-card strong { color: var(--t1) !important; }
.set-card em { color: var(--cyan2) !important; font-style: italic !important; }

/* ── .env / code block inside cards ─────────────── */
.code-block {
    background: var(--bg3);
    border: 1px solid var(--b1);
    border-left: 3px solid var(--blue);
    border-radius: 10px;
    padding: 1rem 1.2rem;
    margin-top: 0.85rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.83rem;
    color: var(--violet2);
    line-height: 1.9;
    overflow-x: auto;
    white-space: pre;
}
.code-block .cb-key   { color: var(--blue2); }
.code-block .cb-value { color: var(--cyan2); }
.code-block .cb-cmd   { color: var(--mint); }
.code-block .cb-flag  { color: var(--gold2); }
.code-block .cb-comment { color: var(--t3); }

/* ── Step Cards (How it works) ───────────────────── */
.step-card {
    background: var(--bg2);
    border: 1px solid var(--b1);
    border-radius: 13px;
    padding: 1.4rem 1.5rem;
    height: 100%;
    transition: border-color 0.25s, box-shadow 0.25s, transform 0.25s;
    position: relative;
    overflow: hidden;
}
.step-card::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; height: 2px;
    border-radius: 13px 13px 0 0;
}
.step-card.s-blue::before   { background: linear-gradient(90deg, var(--blue), var(--cyan)); }
.step-card.s-cyan::before   { background: linear-gradient(90deg, var(--cyan), var(--mint)); }
.step-card.s-violet::before { background: linear-gradient(90deg, var(--violet), var(--coral)); }
.step-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 36px rgba(0,0,0,0.40);
}
.step-card.s-blue:hover   { border-color: rgba(61,142,255,0.38); box-shadow: 0 12px 36px rgba(61,142,255,0.12), 0 4px 20px rgba(0,0,0,0.35); }
.step-card.s-cyan:hover   { border-color: rgba(0,217,255,0.38);  box-shadow: 0 12px 36px rgba(0,217,255,0.12),  0 4px 20px rgba(0,0,0,0.35); }
.step-card.s-violet:hover { border-color: rgba(184,92,255,0.38); box-shadow: 0 12px 36px rgba(184,92,255,0.12), 0 4px 20px rgba(0,0,0,0.35); }

.step-num   { font-family: 'JetBrains Mono', monospace; font-size: 0.66rem; font-weight: 600; letter-spacing: 0.12em; text-transform: uppercase; margin-bottom: 9px; padding-top: 4px; }
.step-title { font-family: 'Beiruti', sans-serif; font-weight: 800; font-size: 1.12rem; margin-bottom: 8px; }
.step-body  { font-size: 0.88rem; color: var(--t2); line-height: 1.72; }

/* ── Group Headers ───────────────────────────────── */
.group-hdr {
    display: flex; align-items: center; gap: 10px;
    margin: 1.2rem 0 0.55rem;
    padding-bottom: 0.45rem;
    border-bottom: 1px solid var(--b1);
}
.group-hdr-label { font-family: 'Outfit', sans-serif; font-size: 0.70rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.10em; }
.group-hdr-count { font-size: 0.68rem; color: var(--t3); background: var(--bg3); border: 1px solid var(--b1); border-radius: 4px; padding: 1px 8px; font-family: 'JetBrains Mono', monospace; }

/* ── Animations ──────────────────────────────────── */
/* ── Checkbox styling (email select) ─────────────── */
.stCheckbox { margin-bottom: 0 !important; }
.stCheckbox > label > div:first-child {
    border-color: var(--b2) !important;
    border-radius: 5px !important;
    background: var(--bg3) !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
}
.stCheckbox > label > div:first-child:hover {
    border-color: var(--blue) !important;
    box-shadow: 0 0 0 2px rgba(61,142,255,0.18) !important;
}
.stCheckbox input:checked + div {
    background: var(--blue) !important;
    border-color: var(--blue) !important;
}

/* ── Delete pill button override ─────────────────── */
[data-testid="stButton"] button[kind="secondary"] {
    background: rgba(255,61,107,0.08) !important;
    color: var(--coral2) !important;
    border: 1px solid rgba(255,61,107,0.28) !important;
    box-shadow: none !important;
}
[data-testid="stButton"] button[kind="secondary"]:hover {
    background: rgba(255,61,107,0.14) !important;
    border-color: var(--coral) !important;
}

@keyframes fadeUp { from { opacity: 0; transform: translateY(14px); } to { opacity: 1; transform: translateY(0); } }
@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
@keyframes glow-pulse {
    0%, 100% { box-shadow: 0 0 8px rgba(61,142,255,0.20); }
    50%       { box-shadow: 0 0 20px rgba(61,142,255,0.45); }
}
.fade-in { animation: fadeIn 0.35s ease; }
.glow-pulse { animation: glow-pulse 2.5s ease-in-out infinite; }
</style>
"""
