import streamlit as st
import google.generativeai as genai
import time

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="FinBot – AI Finance Assistant",
    page_icon="💰",
    layout="wide"
)

# =========================
# CUSTOM CSS
# =========================
st.markdown("""
<style>
    .main {
        padding: 2rem;
    }
    h1 {
        font-weight: 700;
    }
    .stChatMessage {
        padding: 1rem;
        border-radius: 12px;
    }
    .stChatMessage[data-testid="stChatMessage-user"] {
        background-color: #f0f2f6;
    }
    .stChatMessage[data-testid="stChatMessage-assistant"] {
        background-color: #e8f5e9;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# =========================
# API CONFIG
# =========================
GOOGLE_API_KEY = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-3-flash-preview")

# =========================
# SYSTEM PROMPT
# =========================
FINANCE_CONTEXT = """
You are FinBot, a professional and friendly financial education assistant.
You explain finance topics in simple, structured language.

You can help with:
- Budgeting & savings
- Stock market basics
- Mutual funds & SIPs
- Taxes (high-level overview)

Rules:
- Be concise and clear
- Use bullet points where useful
- ALWAYS include a disclaimer:
  "This is for educational purposes only, not professional financial advice."
"""
OUTRO_CONTEXT = """
Based on the user's question, suggest 3 short, relevant follow-up questions
the user might want to ask next.

Rules:
- Suggestions must be directly related to the user's question
- Keep them short (max 8–10 words each)
- Do NOT repeat the original question
- Do NOT give advice, only topics/questions
- Format strictly as bullet points
"""

# =========================
# SIDEBAR
# =========================
with st.sidebar:
    st.header("⚙️ FinBot Settings")
    st.markdown("Customize your guidance experience.")

    risk_level = st.selectbox(
        "Risk Preference",
        ["Conservative", "Balanced", "Aggressive"]
    )

    expertise = st.radio(
        "Knowledge Level",
        ["Beginner", "Intermediate", "Advanced"]
    )

    st.divider()
    st.caption("⚠️ Educational use only")

# =========================
# HEADER
# =========================
st.markdown("""
<h1>💰 FinBot</h1>
<p style="color: gray; margin-top: -10px;">
Smart finance insights, explained simply.
</p>
""", unsafe_allow_html=True)

with st.expander("🤖 How FinBot Works"):
    st.markdown("""
    FinBot provides educational insights on personal finance and markets.

    • No real-time financial data  
    • No personalized investment advice  

    ⚠️ **This is not professional financial advice.**
    """)

# =========================
# SESSION STATE
# =========================
if "messages" not in st.session_state:
    st.session_state.messages = []

# =========================
# EMPTY STATE
# =========================
if not st.session_state.messages:
    st.info("💡 Ask about savings, SIPs, stocks, budgeting, or tax basics.")

# =========================
# CHAT HISTORY
# =========================
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# =========================
# CHAT INPUT
# =========================
if prompt := st.chat_input("Ask about stocks, savings, or taxes..."):
    # User message
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )
    with st.chat_message("user"):
        st.markdown(prompt)

    # Build conversation context (last 5 messages)
    conversation = ""
    for m in st.session_state.messages[-5:]:
        conversation += f"{m['role']}: {m['content']}\n"

    # Assistant response
    with st.chat_message("assistant"):
        try:
            with st.spinner("Analyzing your question..."):
                time.sleep(0.5)
                full_prompt = f"""
                {FINANCE_CONTEXT}

                User profile:
                Risk preference: {risk_level}
                Knowledge level: {expertise}

                Conversation so far:
                {conversation}

                User question:
                {prompt}
                """

                response = model.generate_content(full_prompt)
                reply = response.text

            st.markdown(reply)
            st.session_state.messages.append(
                {"role": "assistant", "content": reply}
            )

        except Exception:
            st.error("⚠️ Something went wrong. Please try again.")
