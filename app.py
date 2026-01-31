import streamlit as st
import google.generativeai as genai

# --- CONFIGURATION ---
# Replace with your API key from https://aistudio.google.com/
GOOGLE_API_KEY = "AIzaSyCff2Wr8sDn8RnBqD0NQIewz9VqQGKACI0" 
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-3-flash-preview')

# --- PAGE SETUP ---
st.set_page_config(page_title="FinBot: Your Finance Expert", page_icon="💰")
st.title("💰 FinBot AI")
st.caption("Professional Financial Guidance & Market Insights")

# --- SYSTEM PROMPT ---
FINANCE_CONTEXT = (
    "You are a helpful and professional financial advisor chatbot. "
    "Provide clear, concise information on budgeting, investing, and markets. "
    "Always include a disclaimer that this is not professional financial advice."
)

# --- SESSION STATE ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- CHAT LOGIC ---
if prompt := st.chat_input("Ask me about stocks, savings, or taxes..."):
    # User message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Bot response
    with st.chat_message("assistant"):
        full_prompt = f"{FINANCE_CONTEXT}\n\nUser: {prompt}"
        response = model.generate_content(full_prompt)
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
