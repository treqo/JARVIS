import os
from dotenv import load_dotenv
from core.speech_recognition import listen_for_speech
from core.ai_client import check_conversation_timeout
import threading

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    dotenv_path = os.path.join(current_dir, '..', '.env')
    load_dotenv(dotenv_path)
    
    threading.Thread(target=check_conversation_timeout, daemon=True).start()
    listen_for_speech()