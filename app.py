import streamlit as st
from Common import take_speech, get_chatgroq_model, get_openai_model, response
import time

st.set_page_config(page_title="VoiceBot", page_icon="🎙️", layout="wide")

st.sidebar.page_link("pages/settings.py", label="⚙️ Settings", icon="⚙️")

st.title("🎙️ VoiceBot")

# Ensure settings are available
if "selected_provider" not in st.session_state or not st.session_state.selected_provider:
    st.warning("⚠️ Please set up your API provider in the ⚙️ Settings page.")
    st.stop()

# Prevent users from proceeding if no API key is entered
if st.session_state.selected_provider == "Groq" and not st.session_state.groq_api_key:
    st.warning("⚠️ Please enter a Groq API Key in Settings.")
    st.stop()
elif st.session_state.selected_provider == "OpenAI" and not st.session_state.openai_api_key:
    st.warning("⚠️ Please enter an OpenAI API Key in Settings.")
    st.stop()

# Chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.markdown("### 🗨️ Conversation")
for chat in st.session_state.chat_history:
    if chat["role"] == "user":
        st.markdown(f"🗣️ **You:** {chat['content']}")
    else:
        st.markdown(f"💬 **Bot:** {chat['content']}")

# **Voice Input Button**
if st.button("🎤 Speak", use_container_width=True):
    with st.spinner("Listening... 🎧"):
        time.sleep(1)  
        speech_text = take_speech()

    if speech_text:
        st.session_state.chat_history.append({"role": "user", "content": speech_text})

        with st.spinner("Thinking... 💭"):
            if st.session_state.selected_provider == "Groq":
                model = get_chatgroq_model(groq_api_key=st.session_state.groq_api_key)
                bot_response = response(model, speech_text)
            else:  # OpenAI
                chat_with_model = get_openai_model(api_key=st.session_state.openai_api_key)
                bot_response = chat_with_model(speech_text)

        st.session_state.chat_history.append({"role": "bot", "content": bot_response})
        st.rerun()

# **Clear Chat Button**
if st.button("🗑️ Clear Chat", use_container_width=True):
    st.session_state.chat_history = []
    st.success("Chat history cleared!")
    st.rerun()
