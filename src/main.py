from dotenv import load_dotenv
import os
from core import initialize_tts, speak, listen, get_client, get_ai_response, initialize_stt, start_transcription

# Load environment variables from .env file
dotenv_path = os.path.join(os.path.dirname(__file__), '../.env')
load_dotenv(dotenv_path=dotenv_path)

# Retrieve API keys from environment variables
api_keys = {
    "openai": os.getenv('OPENAI_API_SECRET_KEY'),
    "deepgram": os.getenv('DEEPGRAM_API_SECRET_KEY')
}

# Check if API keys are available
if not api_keys["openai"] or api_keys["openai"] == "":
    raise ValueError("No OpenAI API key found in .env file")

if not api_keys["deepgram"] or api_keys["deepgram"] == "":
    raise ValueError("No Deepgram API key found in .env file")

def main():
    openai_api_key = api_keys["openai"]
    deepgram_api_key = api_keys["deepgram"]

    client = get_client(openai_api_key)
    initialize_tts(openai_api_key)
    initialize_stt(deepgram_api_key)

    conversation = [{"role": "system", "content": "You are a helpful AI assistant named JARVIS."}]
    
    speak("Hello, I'm JARVIS. How can I assist you today?")

    while True:
        user_input = listen()
        if user_input:
            conversation.append({"role": "user", "content": user_input})
            ai_response = get_ai_response(client, conversation)
            conversation.append({"role": "assistant", "content": ai_response})
            speak(ai_response)

        if user_input and "transcribe" in user_input.lower():
            start_transcription()

        if user_input and "goodbye" in user_input.lower():
            speak("Goodbye! Have a great day.")
            break

if __name__ == "__main__":
    main()
