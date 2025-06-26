import streamlit as st
import requests

st.set_page_config(page_title="💬 LLM Chat App", layout="centered")

# Sidebar config
with st.sidebar:
    st.title("🧠 LLM Chat Settings")
    model_name = st.selectbox("Select Model", ["llama3", "mistral"], index=0)
    if st.button("🔄 Clear Chat"):
        st.session_state.messages = []
        st.session_state.user_input = ""  # Clear input manually

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "user_input" not in st.session_state:
    st.session_state.user_input = ""

# Page header
st.markdown("<h2 style='text-align:center;'>🤖 Local LLM Chatbot</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Powered by Ollama + FastAPI + Streamlit</p>", unsafe_allow_html=True)
st.markdown("---")

# Chat input form
with st.form(key="chat_form", clear_on_submit=True):  # This clears input box
    user_input = st.text_input(
        "Your Message",
        placeholder="Ask me anything...",
        value=st.session_state.user_input,
        key="chat_input"
    )
    submit = st.form_submit_button("Send")

# Handle submit
if submit and user_input.strip():
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.session_state.user_input = ""  # Clear manually just in case

    try:
        response = requests.post(
            "http://localhost:8000/chat",
            json={
                "model": model_name,
                "messages": st.session_state.messages
            }
        )
        if response.status_code == 200 and "message" in response.json():
            assistant_reply = response.json()["message"]["content"]
            st.session_state.messages.append({"role": "assistant", "content": assistant_reply})
        else:
            st.error("❌ Error from FastAPI/Ollama: " + str(response.json()))
    except Exception as e:
        st.error(f"❌ Could not reach FastAPI backend: {e}")

# Display messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

st.markdown("---")
st.caption("Created with ❤️ using Streamlit, FastAPI, and Ollama")

