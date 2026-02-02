import streamlit as st
import google.generativeai as genai
import time

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="ArthaX – AI Finance Assistant",
    page_icon="💹",
    layout="wide"
)

# =========================
# API CONFIG (Optimized)
# =========================
try:
    # Use 1.5-flash for speed and stability
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
   model = genai.GenerativeModel("gemini-1.5-flash-latest")
except Exception as e:
    st.error("API Key missing or invalid. Please check your secrets.")
    st.stop()

# =========================
# ADVANCED CUSTOM CSS
# =========================
st.markdown("""
<style>
    /* Main Background */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: rgba(255, 255, 255, 0.8) !important;
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(0,0,0,0.05);
    }

    /* Chat Bubbles Customization */
    .stChatMessage {
        border-radius: 20px !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        margin-bottom: 15px;
        border: 1px solid rgba(255,255,255,0.3);
    }
    
    /* Header Animation */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .header-container {
        animation: fadeIn 0.8s ease-out;
        text-align: center;
        padding: 20px;
    }

    /* Custom Metric Cards */
    .metric-card {
        background: white;
        padding: 15px;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.02);
    }
</style>
""", unsafe_allow_html=True)

# =========================
# SIDEBAR & DASHBOARD
# =========================
with st.sidebar:
    # Optional: If you saved your logo as logo.png
    # st.image("logo.png", width=150)
    st.markdown("## ⚙️ Personalization")
    
    risk_level = st.select_slider(
        "Risk Appetite",
        options=["Conservative", "Balanced", "Aggressive"],
        value="Balanced"
    )

    expertise = st.radio(
        "Financial Literacy",
        ["Beginner", "Intermediate", "Advanced"],
        horizontal=True
    )

    st.divider()
    if st.button("🗑️ Clear Conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    
    st.markdown("---")
    st.caption("🔒 Secured by Gemini 1.5 Flash")

# =========================
# INTERACTIVE HEADER
# =========================
st.markdown("""
<div class="header-container">
    <h1 style='font-size: 3rem; color: #1E3A8A;'>Artha<span style='color: #10B981;'>X</span></h1>
    <p style='font-size: 1.2rem; color: #4B5563;'>Your Intelligent Path to Wealth</p>
</div>
""", unsafe_allow_html=True)

# Mini Dashboard for context
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f"<div class='metric-card'><b>Mode</b><br>🎓 Education</div>", unsafe_allow_html=True)
with col2:
    st.markdown(f"<div class='metric-card'><b>Risk</b><br>🎯 {risk_level}</div>", unsafe_allow_html=True)
with col3:
    st.markdown(f"<div class='metric-card'><b>Level</b><br>🧠 {expertise}</div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# =========================
# CHAT ENGINE
# =========================
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history with nice avatars
for msg in st.session_state.messages:
    avatar = "👤" if msg["role"] == "user" else "🤖"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ask about SIPs, Gold, or Tax planning..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="🤖"):
        try:
            # We combine both requirements into ONE call to make it faster/cheaper
            full_prompt = f"""
            System: You are ArthaX, a finance expert. 
            Context: User has a {risk_level} risk level and {expertise} expertise.
            
            Answer this query concisely with bullet points: {prompt}
            
            Rule: End with '---' then suggest 3 follow-up questions (max 8 words each).
            Disclaimer: ALWAYS include "Educational purposes only, not advice."
            """
            
            with st.status("ArthaX is analyzing markets...", expanded=True) as status:
                response = model.generate_content(full_prompt)
                st.write(response.text)
                status.update(label="Analysis Complete!", state="complete", expanded=False)

            st.session_state.messages.append({"role": "assistant", "content": response.text})

        except Exception as e:
            st.error(f"Error: {e}")
