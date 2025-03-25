# 🎙️ VoiceBot

VoiceBot is a Streamlit-based AI-powered chatbot that allows users to have voice-based conversations with either **Groq** or **OpenAI** models.

## 🚀 Features
- Supports **Groq** and **OpenAI** models
- Voice input using **speech-to-text**
- Interactive chatbot experience
- Persistent chat history
- API provider selection via a separate settings page

---

## 📌 Prerequisites
Ensure you have the following installed:
- **Python 3.8+**
- **pip** (Python package manager)

---

## 📥 Installation

1. **Clone the repository**
```sh
 git clone https://github.com/your-repo/voicebot.git
 cd voicebot
```

2. **Create a virtual environment (Optional but recommended)**
```sh
python -m venv venv  # Windows/Linux/Mac
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate  # Windows
```

3. **Install required dependencies**
```sh
pip install -r requirements.txt
```

---

## 🔑 Obtaining API Keys

To use the chatbot, you need API keys for **Groq** or **OpenAI**.

### **Groq API Key**
1. Go to [Groq API](https://groq.com/)
2. Sign in or create an account
3. Navigate to **API Keys** and generate a new key

### **OpenAI API Key**
1. Go to [OpenAI API](https://platform.openai.com/)
2. Sign in or create an account
3. Navigate to **API Keys** and generate a new key

---

## 🛠️ Running the App

1. **Run the Streamlit app**
```sh
streamlit run app.py
```

2. **Configure API Provider:**
   - Open the **Settings** page (⚙️)
   - Select either **Groq** or **OpenAI**
   - Enter the respective **API Key**

3. **Start Chatting!** 🎤
   - Click the **"🎤 Speak"** button to start a conversation
   - View the chat history dynamically updated in the UI

---

## 🗑️ Clearing Chat History
If you want to clear the conversation history, simply click the **"🗑️ Clear Chat"** button.

---

## 👥 Contributors
- **Mangammagari Gnana Chaithanya**



