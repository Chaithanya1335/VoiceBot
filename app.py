import streamlit as st
import speech_recognition as sr
from Common import get_chatgroq_model, get_openai_model, response

st.set_page_config(page_title="VoiceBot", page_icon="🎙️", layout="wide")

st.title("🎙️ VoiceBot")

# -----------------------------
# **API Key Validation**
# -----------------------------
selected_provider = st.session_state.get("selected_provider", None)
groq_api_key = st.session_state.get("groq_api_key", "")
openai_api_key = st.session_state.get("openai_api_key", "")

if selected_provider not in ["Groq", "OpenAI"] or (
    selected_provider == "Groq" and not groq_api_key
) or (selected_provider == "OpenAI" and not openai_api_key):
    st.warning("⚠️ Please go to Settings and enter an API key first.")
    st.stop()

# -----------------------------
# **Speech Recognition Setup**
# -----------------------------
recognizer = sr.Recognizer()

# Automatically Selects Default Microphone
def get_default_microphone():
    mic_list = sr.Microphone.list_microphone_names()
    for i, mic in enumerate(mic_list):
        if "bluetooth" in mic.lower():
            return sr.Microphone(device_index=i)
    return sr.Microphone() if mic_list else None  # Default system microphone

mic = get_default_microphone()
if mic is None:
    st.error("⚠️ No microphone detected. Please check your audio settings.")
    st.stop()

# -----------------------------
# **Chat History Section**
# -----------------------------
st.subheader("💬 Conversation")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Chat History
for role, text in st.session_state.messages:
    if role == "user":
        st.markdown(f"🧑‍💻 **You:** {text}")
    else:
        st.markdown(f"🤖 **Bot:** {text}")

# -----------------------------
# **Speech Recognition & Chat Processing**
# -----------------------------
if st.button("🎙️ Start Listening"):
    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        st.info("🎤 Listening...")

        try:
            audio = recognizer.listen(source, timeout=5)
            st.success("✅ Stopped Listening...")
            query = recognizer.recognize_google(audio)
            st.session_state.messages.append(("user", query))  # Store user input

        except sr.UnknownValueError:
            st.error("⚠️ Could not recognize speech. Please try again.")
            st.rerun()
        except sr.RequestError:
            st.error("⚠️ Error with speech recognition service.")
            st.rerun()

    # **Generate AI Response**
    if query:
        with st.spinner("🤖 Thinking..."):
            if selected_provider == "Groq":
                model = get_chatgroq_model(groq_api_key)
                bot_response = response(model, query)
            else:
                chat_with_model = get_openai_model(openai_api_key)
                bot_response = chat_with_model(query)

            
            st.session_state.messages.append(("bot", bot_response))  # Store bot response

        st.rerun()  # Refresh UI to display output

# **Clear Chat Button**
if st.button("🗑️ Clear Chat", use_container_width=True):
    st.session_state.messages = []
    st.success("Chat history cleared!")
    st.rerun()
