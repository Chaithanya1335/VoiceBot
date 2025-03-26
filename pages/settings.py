import streamlit as st
import time

st.set_page_config(page_title="Settings", page_icon="⚙️", layout="wide")

st.title("⚙️ API Settings")

# Instructions for API Key
st.markdown("""
### **Groq API Key**
1. Go to [Groq API](https://groq.com/)
2. Sign in or create an account
3. Navigate to **API Keys** and generate a new key

### **OpenAI API Key**
1. Go to [OpenAI API](https://platform.openai.com/)
2. Sign in or create an account
3. Navigate to **API Keys** and generate a new key
""")

# **Initialize session state if not set**
if "selected_provider" not in st.session_state:
    st.session_state["selected_provider"] = "Groq"
if "groq_api_key" not in st.session_state:
    st.session_state["groq_api_key"] = ""
if "openai_api_key" not in st.session_state:
    st.session_state["openai_api_key"] = ""

# **Select API Provider**
provider = st.radio("🔍 Select API Provider:", ["Groq", "OpenAI"], index=0)

# **Enter API Key**
if provider == "Groq":
    api_key = st.text_input("🔑 Enter Groq API Key:", type="password", value=st.session_state["groq_api_key"])
elif provider == "OpenAI":
    api_key = st.text_input("🔑 Enter OpenAI API Key:", type="password", value=st.session_state["openai_api_key"])

# **Save API Key Button**
if api_key and st.button("✅ Save & Continue to Chat"):
    st.session_state["selected_provider"] = provider
    if provider == "Groq":
        st.session_state["groq_api_key"] = api_key
    else:
        st.session_state["openai_api_key"] = api_key

    st.success("✅ API Key saved! Redirecting to chat...")
    time.sleep(1)  # **Short delay before navigation**
    st.switch_page("app1.py")  # **Navigate to the chat page**
    st.stop()

# **If No API Key is Entered**
if not api_key:
    st.warning("⚠️ Please enter your API key to continue.")
