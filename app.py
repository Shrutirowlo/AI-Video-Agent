import streamlit as st
import time
from dotenv import load_dotenv

from utils.audio_processor import process_input
from core.transcriber import transcribe_all
from core.summaries import summarize, generate_title
from core.extractor import (
    extract_action_items,
    extract_key_decisions,
    extract_questions,
)
from core.rag_engine import (
    build_rag_chain,
    ask_question,
)

load_dotenv()

# ─── Page Config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Video Assistant",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');
@import url('https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@latest/tabler-icons.min.css');

/* ── Root Variables ── */
:root {
    --bg:           #F7F4EF;
    --surface:      #FFFFFF;
    --surface-2:    #F2EDE5;
    --border:       rgba(0,0,0,0.09);
    --border-strong: rgba(0,0,0,0.15);
    --accent:       #C47A52;
    --accent-dark:  #A85E3A;
    --accent-bg:    #F5EDE5;
    --accent-border:#DDAB8C;
    --accent-text:  #8B4A2A;
    --accent-deep:  #4A2010;
    --teal-bg:      #E1F5EE;
    --teal-border:  #5DCAA5;
    --teal-text:    #0F6E56;
    --blue-bg:      #E6F1FB;
    --blue-border:  #85B7EB;
    --blue-text:    #185FA5;
    --blue-deep:    #0C447C;
    --green:        #3B8A5A;
    --text:         #1A1A18;
    --text-sec:     #4A4A42;
    --text-muted:   #888880;
    --radius:       8px;
}

/* ── Global Reset ── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
    background-color: var(--bg) !important;
    color: var(--text) !important;
}

.stApp { background: var(--bg) !important; }

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stToolbar"] { display: none; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 0.5px solid var(--border-strong) !important;
}
[data-testid="stSidebar"] > div:first-child {
    padding-top: 1.5rem !important;
    padding-left: 1.25rem !important;
    padding-right: 1.25rem !important;
}
[data-testid="stSidebar"] * { color: var(--text) !important; }

/* ── Headings ── */
h1, h2, h3, h4 {
    font-family: 'Inter', sans-serif !important;
    font-weight: 500 !important;
    color: var(--text) !important;
}

/* ── Brand block ── */
.brand-block {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 1.25rem;
}
.brand-icon {
    width: 36px; height: 36px;
    border-radius: 10px;
    background: var(--accent);
    display: flex; align-items: center; justify-content: center;
    color: #fff; font-size: 18px;
    flex-shrink: 0;
}
.brand-name { font-size: 15px; font-weight: 500; color: var(--text); }
.brand-sub  { font-size: 11px; color: var(--text-muted); margin-top: 1px; }

/* ── Inputs ── */
.stTextInput > div > div > input {
    background: var(--surface-2) !important;
    border: 0.5px solid var(--border-strong) !important;
    border-radius: var(--radius) !important;
    color: var(--text) !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 13px !important;
}
.stTextInput > div > div > input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 2px rgba(196,122,82,0.15) !important;
}
.stTextInput > label {
    font-size: 11px !important;
    color: var(--text-muted) !important;
    font-weight: 400 !important;
}

/* ── Selectbox ── */
.stSelectbox > div > div {
    background: var(--surface-2) !important;
    border: 0.5px solid var(--border-strong) !important;
    border-radius: var(--radius) !important;
    color: var(--text) !important;
    font-size: 13px !important;
}
.stSelectbox > label {
    font-size: 11px !important;
    color: var(--text-muted) !important;
    font-weight: 400 !important;
}

/* ── Primary Button (Analyse) ── */
.stButton > button {
    background: var(--accent) !important;
    color: #fff !important;
    border: none !important;
    border-radius: var(--radius) !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 500 !important;
    font-size: 13px !important;
    padding: 0.55rem 1.25rem !important;
    transition: background 0.15s !important;
}
.stButton > button:hover {
    background: var(--accent-dark) !important;
    box-shadow: none !important;
    transform: none !important;
}

/* ── Secondary / ghost button ── */
.stButton > button[kind="secondary"] {
    background: var(--surface-2) !important;
    color: var(--text-sec) !important;
    border: 0.5px solid var(--border-strong) !important;
}

/* ── Page header ── */
.page-title {
    font-size: 22px;
    font-weight: 500;
    color: var(--text);
    margin-bottom: 4px;
}
.page-sub {
    font-size: 13px;
    color: var(--text-muted);
    margin-bottom: 10px;
}
.badge-row { display: flex; gap: 6px; flex-wrap: wrap; margin-bottom: 1rem; }
.badge {
    display: inline-block;
    font-size: 11px;
    font-weight: 500;
    padding: 3px 9px;
    border-radius: 99px;
}
.badge-warm  { background: var(--accent-bg);  color: var(--accent-text);  border: 0.5px solid var(--accent-border); }
.badge-teal  { background: var(--teal-bg);    color: var(--teal-text);    border: 0.5px solid var(--teal-border); }
.badge-blue  { background: var(--blue-bg);    color: var(--blue-text);    border: 0.5px solid var(--blue-border); }

/* ── Session card ── */
.session-card {
    background: var(--surface);
    border: 0.5px solid var(--border-strong);
    border-left: 3px solid var(--accent);
    border-radius: 12px;
    padding: 0.875rem 1.25rem;
    margin-bottom: 1rem;
}
.session-eyebrow {
    font-size: 10px;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--text-muted);
    margin-bottom: 4px;
}
.session-title {
    font-size: 17px;
    font-weight: 500;
    color: var(--text);
}

/* ── Content cards ── */
.card {
    background: var(--surface);
    border: 0.5px solid var(--border-strong);
    border-radius: 12px;
    padding: 1rem 1.25rem;
    height: 100%;
}
.card-head {
    font-size: 10px;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: var(--text-muted);
    margin-bottom: 8px;
}
.card-body {
    font-size: 13px;
    color: var(--text-sec);
    line-height: 1.65;
}

/* ── Transcript box ── */
.transcript-box {
    background: var(--surface-2);
    border: 0.5px solid var(--border-strong);
    border-radius: 8px;
    padding: 10px 12px;
    font-size: 12px;
    color: var(--text-muted);
    line-height: 1.7;
    max-height: 220px;
    overflow-y: auto;
    font-family: 'JetBrains Mono', monospace;
    white-space: pre-wrap;
    word-break: break-word;
}

/* ── List items inside cards ── */
.list-item {
    display: flex;
    gap: 7px;
    align-items: flex-start;
    margin-bottom: 7px;
    font-size: 13px;
    color: var(--text-sec);
    line-height: 1.5;
}
.list-icon-green  { color: var(--green); font-size: 14px; margin-top: 1px; flex-shrink: 0; }
.list-icon-warm   { color: var(--accent); font-size: 14px; margin-top: 1px; flex-shrink: 0; }
.list-icon-blue   { color: var(--blue-text); font-size: 14px; margin-top: 1px; flex-shrink: 0; }

/* ── Pipeline status ── */
.pipeline-label {
    font-size: 11px;
    color: var(--text-muted);
    margin-bottom: 8px;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    font-weight: 500;
}
.step-row {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 5px 8px;
    border-radius: var(--radius);
    margin-bottom: 2px;
}
.step-dot {
    width: 7px; height: 7px;
    border-radius: 50%;
    flex-shrink: 0;
}
.dot-done    { background: var(--green); }
.dot-active  { background: var(--accent); animation: blink 1.2s ease infinite; }
.dot-pending { background: var(--border-strong); }
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:0.3} }
.step-text { font-size: 12px; color: var(--text-sec); }

/* ── Chat ── */
.chat-head {
    font-size: 14px;
    font-weight: 500;
    color: var(--text);
    margin-bottom: 8px;
}
.chat-log {
    background: var(--surface-2);
    border: 0.5px solid var(--border-strong);
    border-radius: 12px;
    padding: 1rem;
    max-height: 380px;
    overflow-y: auto;
    margin-bottom: 0.75rem;
}
.chat-msg { margin-bottom: 12px; display: flex; flex-direction: column; gap: 3px; }
.chat-label { font-size: 10px; font-weight: 500; letter-spacing: 0.08em; text-transform: uppercase; }
.chat-label.user { color: var(--accent); }
.chat-label.bot  { color: var(--blue-text); }
.chat-bubble {
    display: inline-block;
    padding: 8px 12px;
    border-radius: 10px;
    font-size: 13px;
    line-height: 1.55;
    max-width: 88%;
}
.bubble-user {
    background: var(--accent-bg);
    color: var(--accent-deep);
    border: 0.5px solid var(--accent-border);
    align-self: flex-end;
}
.bubble-bot {
    background: var(--blue-bg);
    color: var(--blue-deep);
    border: 0.5px solid var(--blue-border);
    align-self: flex-start;
}

/* ── Empty state ── */
.empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 5rem 2rem;
    text-align: center;
}
.empty-icon {
    width: 60px; height: 60px;
    border-radius: 16px;
    background: var(--accent-bg);
    border: 0.5px solid var(--accent-border);
    display: flex; align-items: center; justify-content: center;
    font-size: 28px;
    margin-bottom: 1rem;
}
.empty-title { font-size: 18px; font-weight: 500; color: var(--text); margin-bottom: 6px; }
.empty-body  { font-size: 13px; color: var(--text-muted); max-width: 320px; line-height: 1.6; }

/* ── Expander ── */
[data-testid="stExpander"] {
    background: var(--surface) !important;
    border: 0.5px solid var(--border-strong) !important;
    border-radius: 12px !important;
}
[data-testid="stExpander"] summary {
    font-size: 13px !important;
    color: var(--text-sec) !important;
}

/* ── Progress bar ── */
.stProgress > div > div > div { background: var(--accent) !important; }
.stSpinner > div { border-top-color: var(--accent) !important; }

/* ── Alert / info ── */
[data-testid="stAlert"] {
    background: var(--accent-bg) !important;
    border: 0.5px solid var(--accent-border) !important;
    border-radius: 10px !important;
    color: var(--accent-text) !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--border-strong); border-radius: 2px; }
::-webkit-scrollbar-thumb:hover { background: var(--accent); }

/* ── Markdown text ── */
[data-testid="stMarkdownContainer"] p { color: var(--text-sec) !important; font-size: 13px !important; }
label { color: var(--text-muted) !important; }
</style>
""", unsafe_allow_html=True)

# ─── Session State ───────────────────────────────────────────────────────────────
for key, default in {
    "result": None,
    "chat_history": [],
    "processing": False,
    "pipeline_done": False,
    "pipeline_steps": {},
}.items():
    if key not in st.session_state:
        st.session_state[key] = default


# ─── Helpers ────────────────────────────────────────────────────────────────────
def dot_class(key: str) -> str:
    s = st.session_state.pipeline_steps.get(key, "pending")
    return {"active": "dot-active", "done": "dot-done"}.get(s, "dot-pending")

def render_step(icon: str, label: str, key: str):
    st.markdown(f"""
    <div class="step-row">
        <div class="step-dot {dot_class(key)}"></div>
        <span class="step-text">{icon} {label}</span>
    </div>""", unsafe_allow_html=True)

def update_step(key, state):
    st.session_state.pipeline_steps[key] = state


# ─── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="brand-block">
        <div class="brand-icon">🎬</div>
        <div>
            <div class="brand-name">AI Video</div>
            <div class="brand-sub">Meeting intelligence</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    source = st.text_input(
        "YouTube URL or file path",
        placeholder="https://youtube.com/watch?v=… or /path/to/file.mp4"
    )
    language = st.selectbox("Language", ["english", "hinglish"], index=0)

    run_btn = st.button("⚡ Analyse", use_container_width=True)

    if st.session_state.pipeline_done or st.session_state.pipeline_steps:
        st.markdown("---")
        st.markdown('<div class="pipeline-label">Pipeline status</div>', unsafe_allow_html=True)
        render_step("🔊", "Audio processing", "audio")
        render_step("📝", "Transcription",    "transcript")
        render_step("🏷️", "Title generation", "title")
        render_step("📋", "Summarisation",    "summary")
        render_step("🔍", "Extraction",       "extract")
        render_step("🧠", "RAG engine",       "rag")


# ─── Main ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="page-title">AI Video Assistant</div>
<div class="page-sub">Transcribe · Summarise · Chat with your meetings</div>
<div class="badge-row">
    <span class="badge badge-warm">Transcription</span>
    <span class="badge badge-teal">Summarisation</span>
    <span class="badge badge-blue">RAG chat</span>
</div>
""", unsafe_allow_html=True)

st.markdown("---")


# ─── Run Pipeline ───────────────────────────────────────────────────────────────
if run_btn:
    if not source.strip():
        st.error("Please enter a YouTube URL or file path.")
    else:
        st.session_state.pipeline_done = False
        st.session_state.result = None
        st.session_state.chat_history = []
        st.session_state.pipeline_steps = {}

        progress_ph = st.empty()

        try:
            progress_ph.info("⚙️ Pipeline running — see sidebar for live status…")

            # ── Audio ──
            update_step("audio", "active")
            st.rerun() if False else None   # sidebar re-render hint (rerun only at end)
            # chunks = process_input(source)
            chunks = process_input(source)   # remove when real function is wired
            update_step("audio", "done")

            # ── Transcription ──
            update_step("transcript", "active")

            transcript = transcribe_all(chunks, language)

            update_step("transcript", "done")

            # ── Title ──
            update_step("title", "active")
            # title = generate_title(transcript)
            title = generate_title(transcript)
            update_step("title", "done")

            # ── Summary ──
            update_step("summary", "active")
            # summary = summarize(transcript)
            summary = summarize(transcript)
            update_step("summary", "done")

            # ── Extraction ──
            update_step("extract", "active")
            action_items = extract_action_items(transcript)
            decisions = extract_key_decisions(transcript)
            questions = extract_questions(transcript)
            update_step("extract", "done")

            # ── RAG ──
            update_step("rag", "active")
            # rag_chain = build_rag_chain(transcript)
            rag_chain = build_rag_chain(transcript)  
            update_step("rag", "done")

            st.session_state.result = {
                "title":          title,
                "transcript":     transcript,
                "summary":        summary,
                "action_items":   action_items,
                "key_decisions":  decisions,
                "open_questions": questions,
                "rag_chain":      rag_chain,
            }
            st.session_state.pipeline_done = True
            progress_ph.success("✅ Analysis complete!")
            
            progress_ph.empty()
            st.rerun()

        except Exception as e:
            for k in ["audio", "transcript", "title", "summary", "extract", "rag"]:
                if st.session_state.pipeline_steps.get(k) == "active":
                    st.session_state.pipeline_steps[k] = "pending"
            progress_ph.error(f"❌ Error: {e}")


# ─── Results ────────────────────────────────────────────────────────────────────
if st.session_state.result:
    r = st.session_state.result

    # Session title
    st.markdown(f"""
    <div class="session-card">
        <div class="session-eyebrow">Session title</div>
        <div class="session-title">{r['title']}</div>
    </div>""", unsafe_allow_html=True)

    # Summary + Transcript
    col1, col2 = st.columns([3, 2], gap="medium")

    with col1:
        st.markdown(f"""
        <div class="card">
            <div class="card-head">📋 Summary</div>
            <div class="card-body">{r['summary']}</div>
        </div>""", unsafe_allow_html=True)

    with col2:
        with st.expander("📝 Full transcript", expanded=False):
            st.markdown(
                f'<div class="transcript-box">{r["transcript"]}</div>',
                unsafe_allow_html=True
            )

    st.markdown("<br>", unsafe_allow_html=True)

    # Action items / Decisions / Questions
    c1, c2, c3 = st.columns(3, gap="medium")

    with c1:
        st.markdown(f"""
        <div class="card">
            <div class="card-head">✅ Action items</div>
            <div class="card-body">
                <pre>{r['action_items']}</pre>
            </div>
        </div>""", unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="card">
            <div class="card-head">🔑 Key decisions</div>
            <div class="card-body">
            <pre>{r['key_decisions']}</pre>
            </div>
        </div>""", unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
    <div class="card">
        <div class="card-head">❓ Open questions</div>
        <div class="card-body">
            <pre>{r['open_questions']}</pre>
        </div>
    </div>""", unsafe_allow_html=True)

    st.markdown("---")

    # ── RAG Chat ──────────────────────────────────────────────────────────────
    st.markdown('<div class="chat-head">💬 Chat with your meeting</div>', unsafe_allow_html=True)

    # Chat history
    if st.session_state.chat_history:
        chat_html = '<div class="chat-log">'
        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                chat_html += f"""
                <div class="chat-msg" style="align-items:flex-end">
                    <span class="chat-label user">You</span>
                    <div class="chat-bubble bubble-user">{msg['content']}</div>
                </div>"""
            else:
                chat_html += f"""
                <div class="chat-msg" style="align-items:flex-start">
                    <span class="chat-label bot">Assistant</span>
                    <div class="chat-bubble bubble-bot">{msg['content']}</div>
                </div>"""
        chat_html += "</div>"
        st.markdown(chat_html, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="card" style="text-align:center;padding:2.5rem;margin-bottom:0.75rem">
            <div style="font-size:2rem;margin-bottom:0.5rem">💬</div>
            <div style="color:var(--text-muted);font-size:13px">Ask anything about your meeting transcript</div>
        </div>""", unsafe_allow_html=True)

    # Chat input row
    inp_col, btn_col = st.columns([5, 1], gap="small")
    with inp_col:
        user_input = st.text_input(
            "question",
            placeholder="What were the main decisions made?",
            label_visibility="collapsed",
            key="chat_input_field"
        )
    with btn_col:
        send_btn = st.button("Send →", use_container_width=True)

    if send_btn and user_input.strip():
        with st.spinner("Thinking..."):
            answer = ask_question(
                r["rag_chain"],
                user_input.strip()
        )
        st.session_state.chat_history.append({"role": "user",      "content": user_input.strip()})
        st.session_state.chat_history.append({"role": "assistant", "content": answer})
        st.rerun()

    if st.session_state.chat_history:
        if st.button("🗑️ Clear chat", type="secondary"):
            st.session_state.chat_history = []
            st.rerun()

else:
    # ── Empty state ──────────────────────────────────────────────────────────
    st.markdown("""
    <div class="empty-state">
        <div class="empty-icon">🎬</div>
        <div class="empty-title">Ready to analyse</div>
        <div class="empty-body">
            Paste a YouTube URL or local file path in the sidebar,
            choose your language, and hit <strong>Analyse</strong> to get started.
        </div>
        <div class="badge-row" style="margin-top:1.5rem;justify-content:center">
            <span class="badge badge-warm">Transcription</span>
            <span class="badge badge-teal">Summarisation</span>
            <span class="badge badge-blue">RAG chat</span>
        </div>
    </div>""", unsafe_allow_html=True)