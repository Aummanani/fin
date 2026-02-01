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
# PROMPTS
# =========================
FINANCE_CONTEXT = """
You are FinBot, a professional and friendly financial education assistant.
You explain finance topics in simple, structured language.

Rules:
- Be concise
- Use bullet points
- ALWAYS include:
"This is for educational purposes only, not professional financial advice."
"""

OUTRO_CONTEXT = """
Suggest 3 short follow-up questions related to the user's query.

Rules:
- Max 8 words each
- Bullet points only
- No advice
- No repetition
"""

# =========================
# SIDEBAR
# =========================
with st.sidebar:
    st.header("⚙️ FinBot Settings")

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
<p style="color:gray;margin-top:-10px;">
Smart finance insights, explained simply.
</p>
""", unsafe_allow_html=True)

# =========================
# SESSION STATE
# =========================
if "messages" not in st.session_state:
    st.session_state.messages = []

if not st.session_state.messages:
    st.info("💡 Ask about savings, SIPs, stocks, or taxes.")

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
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    conversation = ""
    for m in st.session_state.messages[-5:]:
        conversation += f"{m['role']}: {m['content']}\n"

    # =========================
    # ASSISTANT RESPONSE
    # =========================
    with st.chat_message("assistant"):
        try:
            with st.spinner("Analyzing your question..."):
                time.sleep(0.4)

                full_prompt = f"""
{FINANCE_CONTEXT}

User profile:
Risk: {risk_level}
Level: {expertise}

Conversation:
{conversation}

User question:
{prompt}
"""

                main_response = model.generate_content(full_prompt).text

                outro_prompt = f"""
{OUTRO_CONTEXT}

User question:
{prompt}

Answer:
{main_response}
"""

                outro_response = model.generate_content(outro_prompt).text

                reply = f"""
{main_response}

---
### 🔎 You might also explore:
{outro_response}
"""

            st.markdown(reply)
            st.session_state.messages.append(
                {"role": "assistant", "content": reply}
            )

        except Exception as e:
            st.error("⚠️ Something went wrong. Please try again.")
