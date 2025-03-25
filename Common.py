import speech_recognition
import pyttsx3
from langchain_groq.chat_models import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage

def take_speech():

    """
    
    This function takes user input from the microphone 
    and returns the query as a string.

    """

    sr = speech_recognition().Recognizer()

    with speech_recognition.Microphone() as source:
        
        print("Please Say Something......")

        sr.pause_threshold = 1
        audio = sr.listen(source)

        try:
            query = sr.recognize_google(audio)
        except Exception as e:
            print("Sorry, I didn't catch that.")
            return None
    return query

        

def text_to_voice(text:str):
    """
    This function takes a string as input and converts it into speech.
    """
    # initializing the voice to speak
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)

    engine.say(text)
    engine.runAndWait()

    engine.save_to_file(text=text,filename='speech.mp4')

    return 'speech.mp4'



def get_llm_model(groq_api_key):
    """
    This function takes a Groq API key as input and returns a LLM model.
    """
    # initializing the LLM model

    llm_model = ChatGroq(
    model='llama3-8b-8192',  
    temperature=0.7,  # Make responses more natural and engaging
    api_key=groq_api_key
    )

    

    return llm_model



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



