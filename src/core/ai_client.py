from imports import get_llm_model, get_stt_model, get_tts_model
import time
import threading

llm_model = get_llm_model()
stt_model = get_stt_model()
tts_model = get_tts_model()

is_active = False
last_interaction_time = time.time()
processing_lock = threading.Lock()
is_speaking = False

CONVERSATION_TIMEOUT = 10
wake_words = ['hey jarvis', 'jarvis']

def check_conversation_timeout():
    global is_active
    while True:
        if is_active and not is_speaking and time.time() - last_interaction_time > CONVERSATION_TIMEOUT:
            print("Conversation timed out. Going back to inactive mode.")
            is_active = False
        time.sleep(1)

def process_audio(audio):
    global is_active, last_interaction_time, is_speaking
    
    if is_speaking:
        return

    with processing_lock:
        try:
            prompt_audio_path = 'prompt.wav'
            with open(prompt_audio_path, 'wb') as f:
                f.write(audio.get_wav_data())
            
            prompt_text = stt_model.transcribe(prompt_audio_path)
            print(f"Heard: {prompt_text}")

            if not is_active:
                if any(wake_word.lower() in prompt_text.lower() for wake_word in wake_words):
                    is_active = True
                    tts_model.speak("Hello, how can I assist you?")
                    last_interaction_time = time.time()
            elif prompt_text.strip():
                print(f'USER: {prompt_text}')
                response = llm_model.prompt(prompt_text)
                print(f'JARVIS: {response}')
                is_speaking = True
                tts_model.speak(response)
                is_speaking = False
                last_interaction_time = time.time()

        except Exception as e:
            print(f"An error occurred: {e}")