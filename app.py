import streamlit as st
import google.generativeai as genai
import time

# =========================
# 1. ELITE PAGE CONFIG
# =========================
st.set_page_config(
    page_title="ArthaX – Smart Wealth AI",
    page_icon="💹",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================
# 2. PRO-LEVEL CUSTOM CSS
# =========================
st.markdown("""
<style>
    /* Main Background & Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Inter', sans-serif; }
    
    .stApp {
        background: linear-gradient(160deg, #0f172a 0%, #1e293b 100%);
        color: #f8fafc;
    }

    /* Sidebar Glassmorphism */
    section[data-testid="stSidebar"] {
        background-color: rgba(15, 23, 42, 0.8) !important;
        backdrop-filter: blur(15px);
        border-right: 1px solid rgba(255,255,255,0.1);
    }

    /* Chat Bubble Styling */
    .stChatMessage {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px !important;
        padding: 20px !important;
        margin-bottom: 20px !important;
    }

    /* Custom Header */
    .hero-text {
        background: linear-gradient(to right, #10b981, #3b82f6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 3.5rem;
    }

    /* Floating Metric Cards */
    .card {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 12px;
        padding: 20px;
        border: 1px solid rgba(255,255,255,0.1);
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# =========================
# 3. CORE LOGIC & API
# =========================
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    # Fixed model ID for stability
    model = genai.GenerativeModel("gemini-1.5-flash-latest")
except Exception as e:
    st.error("Connect your Gemini API Key in secrets to begin.")
    st.stop()

# =========================
# 4. INTERACTIVE SIDEBAR
# =========================
with st.sidebar:
    st.markdown("<h2 style='color:#10b981;'>⚙️ ArthaX Command</h2>", unsafe_allow_html=True)
    
    # Financial DNA Profile
    st.write("---")
    risk = st.select_slider("Risk Tolerance", ["Safe", "Moderate", "Aggressive"], value="Moderate")
    goal = st.selectbox("Primary Goal", ["Wealth Creation", "Tax Saving", "Retirement", "Debt Exit"])
    
    st.write("---")
    if st.button("🔄 Reset Terminal", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# =========================
# 5. DASHBOARD HEADER
# =========================
st.markdown("<div style='text-align:center;'><h1 class='hero-text'>ArthaX</h1><p style='color:#94a3b8; font-size:1.1rem;'>The Future of Financial Intelligence</p></div>", unsafe_allow_html=True)

# Real-time indicators based on user choice
c1, c2, c3 = st.columns(3)
with c1: st.markdown(f"<div class='card'><small>STRATEGY</small><br><b>{risk}</b></div>", unsafe_allow_html=True)
with c2: st.markdown(f"<div class='card'><small>GOAL</small><br><b>{goal}</b></div>", unsafe_allow_html=True)
with c3: st.markdown(f"<div class='card'><small>STATUS</small><br><b style='color:#10b981;'>System Online</b></div>", unsafe_allow_html=True)

st.write("<br>", unsafe_allow_html=True)

# =========================
# 6. INTELLIGENT CHAT
# =========================
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show history
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# User input with interaction feedback
if prompt := st.chat_input("Ask ArthaX anything about your money..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Interactive status message
        with st.status("🔍 Analyzing Market Data...", expanded=True) as status:
            try:
                # One-shot prompt for better speed
                full_query = f"User is profiling for {goal} with a {risk} risk. Answer this: {prompt}. Rule: Use bold text for numbers and end with 3 short follow-up questions."
                response = model.generate_content(full_query)
                
                # Simulate "typing" feel
                time.sleep(0.5)
                st.markdown(response.text)
                
                status.update(label="Analysis Complete", state="complete", expanded=False)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Error: {e}")
