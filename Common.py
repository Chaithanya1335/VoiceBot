import speech_recognition
import openai
from langchain_groq.chat_models import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
import os
from dotenv import load_dotenv
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import speech_recognition as sr

load_dotenv()

groq_api_key = os.getenv('GROQ_API_KEY')



def take_input():
    """
    Captures user speech using sounddevice, saves it, and converts it to text using Google Web Speech API.
    """

    recognizer = sr.Recognizer()
    samplerate = 44100  # Standard sampling rate
    duration = 5  # Record for 5 seconds

    print("Please say something...")

    # Record audio with sounddevice
    audio_data = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=1, dtype=np.int16)
    sd.wait()  # Wait for recording to complete

    # Save as WAV file
    wav.write("input_audio.wav", samplerate, audio_data)

    # Process audio with speech recognition
    with sr.AudioFile("input_audio.wav") as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.record(source)

        try:
            query = recognizer.recognize_google(audio)
            return query
        except sr.UnknownValueError:
            print("Sorry, I didn't catch that.")
            return None
        except sr.RequestError:
            print("Could not connect to the speech recognition service.")
            return None








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



