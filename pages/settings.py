import streamlit as st

st.set_page_config(page_title="Settings", page_icon="⚙️", layout="wide")

st.title("⚙️ Settings")

"""
### **Groq API Key**
1. Go to [Groq API](https://groq.com/)
2. Sign in or create an account
3. Navigate to **API Keys** and generate a new key

### **OpenAI API Key**
1. Go to [OpenAI API](https://platform.openai.com/)
2. Sign in or create an account
3. Navigate to **API Keys** and generate a new key
"""

# Initialize session state variables if not already set
if "selected_provider" not in st.session_state:
    st.session_state.selected_provider = None
if "groq_api_key" not in st.session_state:
    st.session_state.groq_api_key = ""
if "openai_api_key" not in st.session_state:
    st.session_state.openai_api_key = ""

# Select API Provider
st.session_state.selected_provider = st.radio("🔍 provide API key:", ["Groq", "OpenAI"], index=0)

# Enter API Keys
if st.session_state.selected_provider == "Groq":
    st.session_state.groq_api_key = st.text_input("🔑 Enter Groq API Key:", type="password", value=st.session_state.groq_api_key)
elif st.session_state.selected_provider == "OpenAI":
    st.session_state.openai_api_key = st.text_input("🔑 Enter OpenAI API Key:", type="password", value=st.session_state.openai_api_key)

st.success("✅ Settings saved! Go back to the chat page.")
