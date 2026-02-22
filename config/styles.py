GLOBAL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Fraunces:ital,opsz,wght@0,9..144,300;0,9..144,600;1,9..144,400&family=JetBrains+Mono:wght@400;500&display=swap');

/* ══════════════════════════════════════════════
   CSS VARIABLES — change palette here
══════════════════════════════════════════════ */
:root {
    --bg:        #0d0f18;
    --bg2:       #141620;
    --bg3:       #1b1e2e;
    --border:    #252840;
    --border2:   #2e3350;
    --text:      #e8eaf6;
    --text2:     #a8adc8;
    --text3:     #6b7099;
    --blue:      #5b8def;
    --blue2:     #7aa3f5;
    --teal:      #2dd4bf;
    --teal2:     #5eead4;
    --red:       #f87171;
    --amber:     #fbbf24;
    --purple:    #a78bfa;
}

*, *::before, *::after { box-sizing: border-box; }

html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'Inter', sans-serif;
}

/* Subtle mesh background */
[data-testid="stAppViewContainer"]::after {
    content: '';
    position: fixed; inset: 0; pointer-events: none; z-index: 0;
    background:
        radial-gradient(ellipse 70% 50% at 5%  0%,  rgba(91,141,239,0.09) 0%, transparent 60%),
        radial-gradient(ellipse 50% 40% at 95% 100%, rgba(45,212,191,0.07) 0%, transparent 60%),
        radial-gradient(ellipse 40% 30% at 50% 50%,  rgba(167,139,250,0.04) 0%, transparent 70%);
}

/* ═══════════════════════════
   HIDE CHROME
═══════════════════════════ */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stMain"] { padding: 0 !important; }
.block-container { padding: 2rem 2.5rem !important; max-width: 1440px !important; }
[data-testid="InputInstructions"] { display: none !important; }

/* ═══════════════════════════
   SIDEBAR
═══════════════════════════ */
[data-testid="stSidebar"] {
    background: #0a0c14 !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] > div { padding: 0 !important; }

[data-testid="stSidebar"] .stTextInput input {
    background: var(--bg3) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text) !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.84rem !important;
    padding: 0.45rem 0.75rem !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
}
[data-testid="stSidebar"] .stTextInput input:focus {
    border-color: var(--blue) !important;
    box-shadow: 0 0 0 3px rgba(91,141,239,0.15) !important;
    outline: none !important;
}
[data-testid="stSidebar"] .stTextInput label {
    color: var(--text3) !important;
    font-size: 0.69rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.09em !important;
    text-transform: uppercase !important;
}

/* ═══════════════════════════
   MAIN INPUTS
═══════════════════════════ */
.stTextInput input, .stTextArea textarea {
    background: var(--bg2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text) !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.9rem !important;
    transition: all 0.2s ease !important;
}
.stTextInput input:focus, .stTextArea textarea:focus {
    border-color: var(--blue) !important;
    box-shadow: 0 0 0 3px rgba(91,141,239,0.14) !important;
    background: #161828 !important;
}
.stTextInput label, .stTextArea label {
    color: var(--text2) !important;
    font-size: 0.73rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
}

/* ═══════════════════════════
   BUTTONS — base
═══════════════════════════ */
.stButton > button {
    background: linear-gradient(135deg, #5b8def 0%, #7b5ef8 100%) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 9px !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    padding: 0.58rem 1.1rem !important;
    letter-spacing: 0.01em !important;
    width: 100% !important;
    transition: all 0.22s cubic-bezier(.4,0,.2,1) !important;
    box-shadow: 0 2px 12px rgba(91,141,239,0.3) !important;
    position: relative !important;
    overflow: hidden !important;
}
.stButton > button::after {
    content: '' !important;
    position: absolute !important; inset: 0 !important;
    background: linear-gradient(135deg,rgba(255,255,255,0.08),transparent) !important;
    opacity: 0 !important; transition: opacity 0.2s !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(91,141,239,0.45) !important;
}
.stButton > button:hover::after { opacity: 1 !important; }
.stButton > button:active  { transform: translateY(0) !important; }
.stButton > button:disabled {
    background: rgba(91,141,239,0.15) !important;
    color: rgba(255,255,255,0.28) !important;
    box-shadow: none !important; transform: none !important;
}

/* ═══════════════════════════
   ALERTS
═══════════════════════════ */
.stSuccess { background: rgba(45,212,191,0.1) !important; border:1px solid rgba(45,212,191,0.3) !important; border-radius:9px !important; }
.stError   { background: rgba(248,113,113,0.1) !important; border:1px solid rgba(248,113,113,0.3) !important; border-radius:9px !important; }
.stInfo    { background: rgba(91,141,239,0.1)  !important; border:1px solid rgba(91,141,239,0.3)  !important; border-radius:9px !important; }
.stWarning { background: rgba(251,191,36,0.1)  !important; border:1px solid rgba(251,191,36,0.3)  !important; border-radius:9px !important; }

/* ═══════════════════════════
   TABS
═══════════════════════════ */
.stTabs [role="tablist"] {
    background: var(--bg2);
    border: 1px solid var(--border);
    border-radius: 10px; padding: 4px; gap: 3px;
}
.stTabs [role="tab"] {
    background: transparent !important;
    color: var(--text3) !important;
    border-radius: 7px !important; border: none !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.82rem !important; font-weight: 500 !important;
    padding: 0.4rem 1rem !important; transition: all 0.18s !important;
}
.stTabs [role="tab"]:hover { color: var(--text2) !important; background: var(--bg3) !important; }
.stTabs [role="tab"][aria-selected="true"] {
    background: linear-gradient(135deg,rgba(91,141,239,0.2),rgba(123,94,248,0.15)) !important;
    color: var(--text) !important;
    box-shadow: inset 0 0 0 1px rgba(91,141,239,0.35) !important;
}
.stTabs [data-baseweb="tab-panel"] { padding-top: 1.4rem !important; }

/* ═══════════════════════════
   EXPANDER
═══════════════════════════ */
details {
    background: var(--bg2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    margin-bottom: 0.5rem !important;
    overflow: hidden !important;
    transition: border-color 0.2s !important;
}
details summary {
    color: var(--text2) !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.85rem !important; font-weight: 500 !important;
    padding: 0.75rem 1rem !important;
    cursor: pointer !important;
    transition: color 0.15s !important;
}
details summary:hover { color: var(--text) !important; }
details[open] { border-color: rgba(91,141,239,0.35) !important; }

/* ═══════════════════════════
   SIDEBAR NAV RADIO
═══════════════════════════ */
[data-testid="stSidebar"] .stRadio > label  { display: none !important; }
[data-testid="stSidebar"] .stRadio [role="radiogroup"] { gap: 2px !important; }
[data-testid="stSidebar"] .stRadio [data-baseweb="radio"] {
    background: transparent !important; border-radius: 8px !important;
    padding: 0.52rem 1.1rem !important; transition: all 0.18s !important;
    border-left: 2px solid transparent !important;
}
[data-testid="stSidebar"] .stRadio [data-baseweb="radio"]:hover {
    background: rgba(91,141,239,0.08) !important;
}
[data-testid="stSidebar"] .stRadio [data-baseweb="radio"][aria-checked="true"] {
    background: rgba(91,141,239,0.12) !important;
    border-left-color: var(--blue) !important;
}
[data-testid="stSidebar"] .stRadio label {
    color: var(--text3) !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.87rem !important; font-weight: 500 !important;
    text-transform: none !important; letter-spacing: 0 !important;
    transition: color 0.15s !important;
}
[data-testid="stSidebar"] .stRadio [aria-checked="true"] label {
    color: var(--text) !important; font-weight: 600 !important;
}

/* SIDEBAR connect button — teal */
[data-testid="stSidebar"] .stButton > button {
    background: linear-gradient(135deg, #2dd4bf 0%, #14b8a6 100%) !important;
    color: #042f2e !important; font-weight: 700 !important;
    box-shadow: 0 3px 14px rgba(45,212,191,0.3) !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background: linear-gradient(135deg, #5eead4 0%, #2dd4bf 100%) !important;
    box-shadow: 0 6px 22px rgba(45,212,191,0.45) !important;
    transform: translateY(-2px) !important;
}

/* ═══════════════════════════
   SCROLLBAR
═══════════════════════════ */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--border2); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #3d4466; }

/* ═══════════════════════════
   FILE UPLOADER
═══════════════════════════ */
[data-testid="stFileUploader"] {
    background: var(--bg2) !important;
    border: 2px dashed var(--border2) !important;
    border-radius: 10px !important;
    transition: border-color 0.2s, background 0.2s !important;
}
[data-testid="stFileUploader"]:hover {
    border-color: var(--blue) !important;
    background: rgba(91,141,239,0.04) !important;
}
[data-testid="stFileUploader"] label {
    color: var(--text2) !important;
    font-size: 0.72rem !important; font-weight: 600 !important;
    letter-spacing: 0.09em !important; text-transform: uppercase !important;
}
[data-testid="stFileUploader"] section {
    background: transparent !important; border: none !important; padding: 0.7rem !important;
}
[data-testid="stFileUploader"] small {
    color: var(--text3) !important; font-size: 0.73rem !important;
}

/* ═══════════════════════════
   DOWNLOAD BUTTON
═══════════════════════════ */
[data-testid="stDownloadButton"] > button {
    background: var(--bg3) !important;
    color: var(--blue2) !important;
    border: 1px solid rgba(91,141,239,0.28) !important;
    border-radius: 7px !important;
    font-size: 0.76rem !important; font-weight: 600 !important;
    padding: 0.35rem 0.6rem !important;
    box-shadow: none !important; transition: all 0.18s !important;
}
[data-testid="stDownloadButton"] > button:hover {
    background: rgba(91,141,239,0.12) !important;
    border-color: rgba(91,141,239,0.55) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 3px 10px rgba(91,141,239,0.2) !important;
}

/* ═══════════════════════════
   CHECKBOX
═══════════════════════════ */
.stCheckbox label span { color: var(--text2) !important; font-size: 0.85rem !important; font-weight: 500 !important; }

/* ═══════════════════════════
   PROGRESS BAR
═══════════════════════════ */
.stProgress > div > div {
    background: linear-gradient(90deg, var(--blue), var(--teal)) !important;
    border-radius: 4px !important;
}
.stProgress > div { background: var(--bg3) !important; border-radius: 4px !important; }

/* ═══════════════════════════
   CODE BLOCKS
═══════════════════════════ */
.stCodeBlock { background: var(--bg2) !important; border: 1px solid var(--border) !important; border-radius: 8px !important; }

/* ══════════════════════════════════════════════
   CUSTOM COMPONENT CLASSES
══════════════════════════════════════════════ */

/* Page heading */
.page-title {
    font-family: 'Fraunces', serif;
    font-size: 2.1rem; color: var(--text);
    line-height: 1.2; margin-bottom: 0.3rem;
}
.page-title span {
    background: linear-gradient(135deg, var(--blue), var(--teal));
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
}
/* ↑ FIX: was #404468 (near-invisible). Now clearly readable */
.page-sub { color: var(--text2); font-size: 0.88rem; margin-bottom: 1.5rem; }

/* ── EMAIL CARD ── */
.ecard {
    background: var(--bg2);
    border: 1px solid var(--border);
    border-left: 3px solid var(--border);
    border-radius: 10px;
    padding: 1.1rem 1.4rem; margin-bottom: 0.7rem;
    transition: transform 0.2s, box-shadow 0.2s, border-color 0.2s;
    cursor: default; position: relative; overflow: hidden;
}
.ecard::after {
    content: ''; position: absolute; inset: 0;
    background: linear-gradient(135deg,rgba(255,255,255,0.02),transparent);
    pointer-events: none;
}
.ecard:hover {
    transform: translateX(4px);
    box-shadow: 0 4px 28px rgba(0,0,0,0.3), -4px 0 12px rgba(91,141,239,0.06);
    border-color: var(--border2); border-left-color: inherit;
}
.ecard.c-imp { border-left-color: var(--red); }
.ecard.c-pro { border-left-color: var(--blue); }
.ecard.c-upd { border-left-color: var(--teal); }
.ecard.c-oth { border-left-color: var(--amber); }

.ecard-from    { font-family:'JetBrains Mono',monospace; font-size:0.72rem; color:var(--blue2); margin-bottom:4px; letter-spacing:0.01em; }
.ecard-subject { font-family:'Fraunces',serif; font-size:1.02rem; color:var(--text); margin-bottom:6px; font-weight:600; }
/* ↑ FIX: was #282b3e (near-invisible) */
.ecard-date    { font-size:0.71rem; color:var(--text3); }

/* ── CATEGORY PILL ── */
.cpill {
    display:inline-flex; align-items:center; gap:4px;
    padding: 2px 10px; border-radius: 20px;
    font-size: 0.67rem; font-weight: 700;
    letter-spacing: 0.07em; text-transform: uppercase;
}
.cp-imp { background:rgba(248,113,113,0.12); color:var(--red);    border:1px solid rgba(248,113,113,0.3); }
.cp-pro { background:rgba(91,141,239,0.12);  color:var(--blue2);  border:1px solid rgba(91,141,239,0.3); }
.cp-upd { background:rgba(45,212,191,0.12);  color:var(--teal2);  border:1px solid rgba(45,212,191,0.3); }
.cp-oth { background:rgba(251,191,36,0.12);  color:var(--amber);  border:1px solid rgba(251,191,36,0.3); }

/* ── CHIP LABEL ── */
.chip {
    display: inline-flex; align-items: center; gap: 5px;
    background: rgba(91,141,239,0.1);
    border: 1px solid rgba(91,141,239,0.25);
    border-radius: 6px; padding: 3px 10px;
    font-size: 0.69rem; font-weight: 700;
    /* ↑ FIX: was #7b96ff which was ok but border too faint */
    color: var(--blue2); letter-spacing: 0.07em; text-transform: uppercase;
    margin-bottom: 0.55rem; width: fit-content;
}

/* ── PANELS ── */
.panel {
    background: var(--bg2);
    border: 1px solid var(--border);
    border-radius: 12px; padding: 1.4rem;
}

/* ── STATUS BADGES ── */
.badge-ok  { display:flex; align-items:center; gap:7px; background:rgba(45,212,191,0.1); border:1px solid rgba(45,212,191,0.3); border-radius:8px; padding:0.5rem 0.9rem; font-size:0.82rem; color:var(--teal2); margin-top:0.4rem; }
.badge-err { display:flex; align-items:center; gap:7px; background:rgba(248,113,113,0.1); border:1px solid rgba(248,113,113,0.3); border-radius:8px; padding:0.5rem 0.9rem; font-size:0.82rem; color:var(--red); margin-top:0.4rem; }
.dot { width:7px; height:7px; border-radius:50%; background:var(--teal); box-shadow:0 0 7px var(--teal); display:inline-block; animation:blink 2s infinite; }
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:.25} }

/* ── SIDEBAR SECTION LABEL ── */
/* ↑ FIX: was #282b3e (near-invisible against sidebar bg) */
.slbl {
    font-size: 0.64rem; color: var(--text3);
    text-transform: uppercase; letter-spacing: 0.12em; font-weight: 700;
    padding: 0.9rem 1.1rem 0.3rem;
    display: flex; align-items: center; gap: 8px;
}
.slbl::after { content:''; flex:1; height:1px; background: linear-gradient(90deg,var(--border2),transparent); }

/* ── SIDEBAR STAT ROWS ── */
/* ↑ FIX: now using explicit readable color */
.sstat { display:flex; justify-content:space-between; align-items:center; padding:4px 1.1rem; font-size:0.8rem; }
.sstat-num { font-weight:700; color:var(--blue2); }

/* ── EMPTY STATE ── */
.empty { text-align:center; padding:5rem 2rem; animation: fadeUp 0.4s ease; }
.empty-icon { font-size:3.5rem; margin-bottom:0.8rem; }
.empty-title { font-family:'Fraunces',serif; font-size:1.7rem; color:var(--text); margin-bottom:0.5rem; }
/* ↑ FIX: was #404468 */
.empty-sub { color: var(--text2); font-size: 0.9rem; line-height: 1.7; }

/* ── AI PANEL ── */
.ai-panel {
    background: linear-gradient(160deg, #151828, #111422);
    border: 1px solid rgba(91,141,239,0.25);
    border-radius: 12px; padding: 1.4rem;
}
.ai-title { font-family:'Fraunces',serif; font-size:1.1rem; color:var(--blue2); margin-bottom:4px; font-weight:600; }
/* ↑ FIX: was #404468 */
.ai-sub { font-size: 0.82rem; color: var(--text2); margin-bottom: 1rem; line-height: 1.5; }

/* ── SETTINGS CARDS ── */
.set-card {
    background: var(--bg2);
    border: 1px solid var(--border);
    border-radius: 12px; padding: 1.5rem;
    transition: border-color 0.2s, box-shadow 0.2s;
}
.set-card:hover { border-color: var(--border2); box-shadow: 0 4px 20px rgba(0,0,0,0.2); }
.set-card h4 { font-family:'Fraunces',serif; color:var(--text); margin-bottom:0.8rem; font-size:1.05rem; }
.set-card p, .set-card li { color: var(--text2) !important; font-size: 0.88rem !important; line-height: 1.75 !important; }
.set-card a { color: var(--blue2) !important; text-decoration: none !important; }
.set-card a:hover { color: var(--teal2) !important; }

/* ── ANIMATIONS ── */
@keyframes fadeUp { from{opacity:0;transform:translateY(14px)} to{opacity:1;transform:translateY(0)} }
@keyframes fadeIn { from{opacity:0} to{opacity:1} }
.fade-in { animation: fadeIn 0.35s ease; }

/* ── DIVIDER ── */
hr { border-color: var(--border) !important; margin: 1.2rem 0 !important; }

/* ═══════════════════════════
   SELECTBOX (sort/group dropdowns)
═══════════════════════════ */
.stSelectbox > label {
    color: var(--text2) !important;
    font-size: 0.72rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
}
.stSelectbox [data-baseweb="select"] > div {
    background: var(--bg2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 9px !important;
    color: var(--text) !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.88rem !important;
    transition: border-color 0.2s !important;
}
.stSelectbox [data-baseweb="select"] > div:hover {
    border-color: var(--border2) !important;
}
.stSelectbox [data-baseweb="select"] > div:focus-within {
    border-color: var(--blue) !important;
    box-shadow: 0 0 0 3px rgba(91,141,239,0.13) !important;
}
/* Dropdown list */
[data-baseweb="popover"] [role="listbox"] {
    background: #1b1e2e !important;
    border: 1px solid var(--border2) !important;
    border-radius: 10px !important;
    box-shadow: 0 8px 30px rgba(0,0,0,0.4) !important;
}
[data-baseweb="popover"] [role="option"] {
    background: transparent !important;
    color: var(--text2) !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.86rem !important;
    padding: 0.5rem 0.9rem !important;
    transition: background 0.15s !important;
}
[data-baseweb="popover"] [role="option"]:hover {
    background: rgba(91,141,239,0.1) !important;
    color: var(--text) !important;
}
[data-baseweb="popover"] [aria-selected="true"] {
    background: rgba(91,141,239,0.18) !important;
    color: var(--blue2) !important;
}

/* ═══════════════════════════
   SEARCH HIGHLIGHT
═══════════════════════════ */
mark {
    background: rgba(91,141,239,0.3) !important;
    color: var(--text) !important;
    border-radius: 3px !important;
    padding: 0 2px !important;
}

/* ═══════════════════════════
   TOOLBAR BOX
═══════════════════════════ */
.toolbar {
    background: var(--bg2);
    border: 1px solid var(--border);
    border-radius: 11px;
    padding: 0.9rem 1.1rem;
    margin-bottom: 1rem;
}
.toolbar-label {
    font-size: 0.68rem; color: var(--text3);
    text-transform: uppercase; letter-spacing: 0.1em;
    font-weight: 700; margin-bottom: 0.55rem;
}

/* ═══════════════════════════
   GROUP HEADER DIVIDERS
═══════════════════════════ */
.group-hdr {
    display: flex; align-items: center; gap: 10px;
    margin: 1.1rem 0 0.5rem;
    padding-bottom: 0.4rem;
    border-bottom: 1px solid var(--border);
}
.group-hdr-label {
    font-size: 0.72rem; font-weight: 700;
    text-transform: uppercase; letter-spacing: 0.1em;
}
.group-hdr-count {
    font-size: 0.7rem; color: var(--text3);
    background: var(--bg3); border: 1px solid var(--border);
    border-radius: 10px; padding: 1px 8px;
}

/* ═══════════════════════════
   HIDE DEFAULT FILE UPLOADER LIST
   (we render our own custom attachment preview)
═══════════════════════════ */
[data-testid="stFileUploaderFile"],
[data-testid="stFileUploaderFileData"],
[data-testid="stFileUploaderDropzone"] + div > div > div > ul,
[data-testid="stFileUploader"] ul,
[data-testid="stFileUploader"] li,
section[data-testid="stFileUploader"] > div > div:nth-child(2),
[data-testid="stFileUploaderDropzone"] ~ div[style] {
    display: none !important;
}

/* ═══════════════════════════
   CLEAR FILTERS BUTTON override
═══════════════════════════ */
[data-testid="stButton"][key="clear_filters"] > button,
button[kind="secondary"] {
    background: var(--bg3) !important;
    color: var(--red) !important;
    border: 1px solid rgba(248,113,113,0.3) !important;
    box-shadow: none !important;
    font-size: 0.8rem !important;
}
button[kind="secondary"]:hover {
    background: rgba(248,113,113,0.08) !important;
    border-color: var(--red) !important;
}
</style>
"""
