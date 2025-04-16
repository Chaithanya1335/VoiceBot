import streamlit as st
from Common import take_input, get_chatgroq_model, get_openai_model, response

# -----------------------------
# **App Configuration**
# -----------------------------
st.set_page_config(page_title="🎙️ VoiceBot", page_icon="🎤", layout="wide")
st.title("🎤 VoiceBot - Talk to AI")

# -----------------------------
# **Check API Key Before Proceeding**
# -----------------------------
selected_provider = st.session_state.get("selected_provider", None)
groq_api_key = st.session_state.get("groq_api_key", "")
openai_api_key = st.session_state.get("openai_api_key", "")

if selected_provider not in ["Groq", "OpenAI"] or (
    selected_provider == "Groq" and not groq_api_key
) or (selected_provider == "OpenAI" and not openai_api_key):
    st.warning("⚠️ Please go to **Settings** and enter a valid API key to continue.")
    st.stop()

# -----------------------------
# **Chat History Display**
# -----------------------------
st.subheader("💬 Conversation History")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Show chat history
for role, text in st.session_state.messages:
    if role == "user":
        st.markdown(f"🧑‍💻 **You:** {text}")
    else:
        st.markdown(f"🤖 **Bot:** {text}")

# -----------------------------
# **Voice & Text Input Tabs**
# -----------------------------
st.subheader("📝 Interact with the AI")

tab1, tab2 = st.tabs(["🎙️ Voice Input", "⌨️ Text Input"])

with tab1:
    if st.button("🎙️ Start Listening"):
        with st.spinner("🎤 Listening... Please speak clearly"):
            speech_text = take_input()

        if speech_text and speech_text.strip():
            st.success(f"✅ **You said:** {speech_text}")

            with st.spinner("🤖 Thinking... Generating response, please wait"):
                try:
                    if selected_provider == "Groq":
                        model = get_chatgroq_model(groq_api_key)
                        bot_response = response(model, speech_text)
                    else:
                        chat_with_model = get_openai_model(openai_api_key)
                        bot_response = chat_with_model(speech_text)

                    # Store messages
                    st.session_state.messages.append(("user", speech_text))
                    st.session_state.messages.append(("bot", bot_response))

                    st.success(f"🤖 **Bot:** {bot_response}")

                except Exception as e:
                    st.error(f"⚠️ Error: {str(e)}")

            st.rerun()

        else:
            st.error("❌ No speech detected. Please try again.")

with tab2:
    user_input = st.text_input("Type your message here:", key="text_input")

    if st.button("📨 Send"):
        if user_input and user_input.strip():
            st.success(f"✅ **You said:** {user_input}")

            with st.spinner("🤖 Thinking... Generating response, please wait"):
                try:
                    if selected_provider == "Groq":
                        model = get_chatgroq_model(groq_api_key)
                        bot_response = response(model, user_input)
                    else:
                        chat_with_model = get_openai_model(openai_api_key)
                        bot_response = chat_with_model(user_input)

                    # Store messages
                    st.session_state.messages.append(("user", user_input))
                    st.session_state.messages.append(("bot", bot_response))

                    st.success(f"🤖 **Bot:** {bot_response}")

                except Exception as e:
                    st.error(f"⚠️ Error: {str(e)}")

            st.rerun()

        else:
            st.error("❌ Please enter a message before sending.")

# -----------------------------
# **Clear Chat Button**
# -----------------------------
if st.button("🗑️ Clear Chat", use_container_width=True):
    st.session_state.messages = []
    st.success("🧹 Chat history cleared!")
    st.rerun()
