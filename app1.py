import streamlit as st
from Common import get_chatgroq_model, get_openai_model, response
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

# JavaScript for Browser Speech Recognition
js_code = """
<script>
    function startDictation() {
        if (window.hasOwnProperty('webkitSpeechRecognition')) {
            var recognition = new webkitSpeechRecognition();
            recognition.continuous = false;
            recognition.interimResults = false;
            recognition.lang = "en-US";
            recognition.start();

            recognition.onresult = function (e) {
                document.getElementById('input_text').value = e.results[0][0].transcript;
                document.getElementById('submit_button').click();
            };

            recognition.onerror = function (e) {
                console.error("Speech Recognition Error:", e);
            };
        } else {
            alert("Speech recognition is not supported in this browser.");
        }
    }
</script>
"""

st.components.v1.html(js_code, height=0)

# Voice Input Button
st.markdown('<button onclick="startDictation()">🎤 Speak</button>', unsafe_allow_html=True)

# Hidden input field for speech-to-text result
user_input = st.text_input("Your message:", key="input_text")

# Submit button (auto-clicked by JavaScript)
if st.button("Submit", key="submit_button"):
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    with st.spinner("Thinking... 💭"):
        if st.session_state.selected_provider == "Groq":
            model = get_chatgroq_model(groq_api_key=st.session_state.groq_api_key)
            bot_response = response(model, user_input)
        else:  # OpenAI
            chat_with_model = get_openai_model(api_key=st.session_state.openai_api_key)
            bot_response = chat_with_model(user_input)

    st.session_state.chat_history.append({"role": "bot", "content": bot_response})
    st.rerun()

# Clear Chat Button
if st.button("🗑️ Clear Chat", use_container_width=True):
    st.session_state.chat_history = []
    st.success("Chat history cleared!")
    st.rerun()
