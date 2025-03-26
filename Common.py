import speech_recognition
import openai
from langchain_groq.chat_models import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from streamlit_javascript import st_javascript
import os
from dotenv import load_dotenv

load_dotenv()

groq_api_key = os.getenv('GROQ_API_KEY')

import speech_recognition as sr

def take_input():
    """
    This function captures user speech and converts it to text using Google Web Speech API.
    """

    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Please say something...")

        recognizer.adjust_for_ambient_noise(source)  # Reduce background noise
        audio = recognizer.listen(source)

        try:
            query = recognizer.recognize_google(audio)  # Uses Google's online STT
            return query
        except sr.UnknownValueError:
            print("Sorry, I didn't catch that.")
            return None
        except sr.RequestError:
            print("Could not connect to the speech recognition service.")
            return None

import streamlit as st
from streamlit_javascript import st_javascript

import streamlit as st
from streamlit_javascript import st_javascript

import streamlit as st
from streamlit_javascript import st_javascript

import streamlit as st
from streamlit_js_eval import streamlit_js_eval
# Function to capture speech from browser
def take_input_from_browser():
    script = """
    async function getSpeech() {
        return new Promise((resolve) => {
            try {
                const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
                if (!SpeechRecognition) {
                    resolve("❌ Speech Recognition not supported in this browser.");
                    return;
                }

                const recognition = new SpeechRecognition();
                recognition.lang = "en-US";
                recognition.interimResults = false;
                recognition.maxAlternatives = 1;

                recognition.onresult = function(event) {
                    resolve(event.results[0][0].transcript);
                };

                recognition.onerror = function(event) {
                    resolve("❌ Error: " + event.error);
                };

                recognition.onspeechend = function() {
                    recognition.stop();
                };

                recognition.start();
            } catch (error) {
                resolve("❌ Speech Recognition failed.");
            }
        });
    }
    getSpeech();
    """

    # Run JavaScript and return output
    speech_text = streamlit_js_eval(script=script, key="speech_input")
    return speech_text if speech_text else "❌ No speech detected."









def get_chatgroq_model(groq_api_key):
    if not groq_api_key:
        raise ValueError("❌ Error: GROQ_API_KEY is missing. Please check your .env file.")
    
    
    llm_model = ChatGroq(
        model="llama3-8b-8192", 
        temperature=0.7, 
        api_key=groq_api_key
    )
    
    return llm_model

def get_openai_model(api_key, model="gpt-3.5-turbo"):
    """
    Initializes and returns an OpenAI LLM model.
    
    Parameters:
        api_key (str): OpenAI API key.
        model (str): The model to use (default: "gpt-4").

    Returns:
        function: A function that takes a prompt and returns a response.
    """
    openai.api_key = api_key

    def chat_with_model(prompt):
        """
        Generates a response from OpenAI's model.
        
        Parameters:
            prompt (str): The input prompt for the model.

        Returns:
            str: The generated response from the model.
        """
        try:
            response = openai.ChatCompletion.create(
                model=model,
                messages=[{"role": "system", "content": "You are a helpful assistant."},
                          {"role": "user", "content": prompt}]
            )
            return response["choices"][0]["message"]["content"]
        except Exception as e:
            return f"⚠️ Error: {e}"

    return chat_with_model


def response(llm_model,query):
    """
    This function takes a LLM model and a query as input and returns a response.
    """

    # System message to create a more human-like response style
    system_message = SystemMessage(
        content=(
            "You are an insightful, self-aware person with life experiences, emotions, and a unique personality. "
            "You do NOT mention being an AI. Instead, answer as if you are reflecting on your own life, passions, and growth. "
            "Be conversational, engaging, and thoughtful—like a person sharing their story."
        )
    )
    # Generate a response using the LLM model
    output = llm_model.invoke([system_message, HumanMessage(content=query)])

    return output.content



