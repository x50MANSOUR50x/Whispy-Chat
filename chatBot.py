import streamlit as st
import google.genai as genai
import time
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Retrieve the Gemini API key
GEN_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEN_API_KEY:
    st.error("❌ Gemini API key not found. Please add it to your .env file.")
    st.stop()

# Initialize the Gemini client
client = genai.Client(api_key=GEN_API_KEY)

# Streamlit page setup
st.set_page_config(page_title="WhispyChat 💬", page_icon="🤖")
st.title("🤖 WhispyChat (Gemini)")
st.markdown("Ask me anything!")

# Initialize chat session
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
user_input = st.chat_input("💬 Type your question here...")

if user_input:
    # Save user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate response from Gemini
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=user_input
        )
        assistant_reply = response.text.strip()
    except Exception as e:
        assistant_reply = f"⚠️ Error: {str(e)}"

    st.session_state.messages.append({"role": "assistant", "content": assistant_reply})

    # Display response with typing animation
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        response_text = ""
        for char in assistant_reply:
            response_text += char
            response_placeholder.markdown(response_text + "▌")
            time.sleep(0.003)
        response_placeholder.markdown(response_text)