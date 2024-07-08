import os
from groq import Groq
from openai import OpenAI
import pyaudio
import wave
from dotenv import load_dotenv
import speech_recognition as sr
import time
from faster_whisper import WhisperModel
import threading
import numpy as np
import webrtcvad

wake_words = ['hey jarvis', 'jarvis']
CONVERSATION_TIMEOUT = 10
SAMPLE_RATE = 16000
CHUNK_DURATION_MS = 30  # supports 10, 20 and 30 (ms)
CHUNK_SIZE = int(SAMPLE_RATE * CHUNK_DURATION_MS / 1000)
VAD_MODE = 3

r = sr.Recognizer()

dotenv_path = os.path.join(os.path.dirname(__file__), './.env')
load_dotenv(dotenv_path=dotenv_path)

api_keys = {
    "openai": os.getenv('OPENAI_API_SECRET_KEY'),
    "groq": os.getenv('GROQ_API_SECRET_KEY'),
}

groq_client = Groq(api_key=api_keys['groq'])
openai_client = OpenAI(api_key=api_keys['openai'])

sys_msg = (
    'You are an AI voice assistant named Jarvis. Generate the most useful and factual response possible, carefully considering all previous generated text in your response before adding new tokens to the response. Make your response clear and concise, avoiding any verbosity.'
)

convo = [{'role': 'system', 'content': sys_msg}]

num_cores = os.cpu_count()
whisper_size = 'base'
whisper_model = WhisperModel(
    whisper_size,
    device='cpu',
    compute_type='int8',
    cpu_threads=num_cores//2,
    num_workers=num_cores//2
)

is_active = False
last_interaction_time = time.time()
processing_lock = threading.Lock()
is_speaking = False
vad = webrtcvad.Vad(VAD_MODE)

def groq_prompt(prompt):
    convo.append({'role': 'user', 'content': prompt})
    chat_completion = groq_client.chat.completions.create(messages=convo, model='llama3-70b-8192')
    response = chat_completion.choices[0].message
    convo.append(response)
    return response.content

def speak(text):
    global is_speaking, last_interaction_time
    is_speaking = True
    last_interaction_time = time.time()
    player_stream = pyaudio.PyAudio().open(format=pyaudio.paInt16, channels=1, rate=24000, output=True)
    stream_start = False

    with openai_client.audio.speech.with_streaming_response.create(
        model='tts-1',
        voice='fable',
        response_format='pcm',
        input=text,
    ) as response:
        silence_threshold = 0.01
        for chunk in response.iter_bytes(chunk_size=1024):
            if stream_start:
                player_stream.write(chunk)
            else:
                if max(chunk) > silence_threshold:
                    player_stream.write(chunk)
                    stream_start = True
    player_stream.stop_stream()
    player_stream.close()
    is_speaking = False
    last_interaction_time = time.time()
    time.sleep(0.5)

def check_conversation_timeout():
    global is_active
    while True:
        if is_active and not is_speaking and time.time() - last_interaction_time > CONVERSATION_TIMEOUT:
            print("Conversation timed out. Going back to inactive mode.")
            is_active = False
        time.sleep(1)

def wav_to_text(audio_path):
    segments, _ = whisper_model.transcribe(audio_path)
    text = ''.join(segment.text for segment in segments)
    return text

def is_speech(audio_frame):
    return vad.is_speech(audio_frame, SAMPLE_RATE)

def process_audio(audio):
    global is_active, last_interaction_time
    
    if is_speaking:
        return

    with processing_lock:
        try:
            prompt_audio_path = 'prompt.wav'
            with open(prompt_audio_path, 'wb') as f:
                f.write(audio.get_wav_data())
            
            prompt_text = wav_to_text(prompt_audio_path)
            print(f"Heard: {prompt_text}")

            if not is_active:
                if any(wake_word.lower() in prompt_text.lower() for wake_word in wake_words):
                    is_active = True
                    speak("Hello, how can I assist you?")
                    last_interaction_time = time.time()
            elif prompt_text.strip():
                print(f'USER: {prompt_text}')
                response = groq_prompt(prompt=prompt_text)
                print(f'JARVIS: {response}')
                speak(response)
                last_interaction_time = time.time()

        except Exception as e:
            print(f"An error occurred: {e}")

def listen_for_speech():
    global is_active
    
    print("Jarvis is listening. Say 'Hey Jarvis' or 'Jarvis' to start a conversation.")
    
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=SAMPLE_RATE, input=True, frames_per_buffer=CHUNK_SIZE)
    
    audio_buffer = []
    silence_chunks = 0
    
    while True:
        try:
            frame = stream.read(CHUNK_SIZE)
            is_speech_frame = is_speech(frame)
            
            if is_speech_frame:
                audio_buffer.append(frame)
                silence_chunks = 0
            else:
                silence_chunks += 1

            if len(audio_buffer) > 0 and (silence_chunks > 10 or len(audio_buffer) > 300):
                audio_data = b''.join(audio_buffer)
                audio = sr.AudioData(audio_data, SAMPLE_RATE, 2)
                if not is_speaking:
                    threading.Thread(target=process_audio, args=(audio,)).start()
                audio_buffer = []
                silence_chunks = 0

        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"An error occurred while listening: {e}")

    stream.stop_stream()
    stream.close()
    p.terminate()

if __name__ == "__main__":
    threading.Thread(target=check_conversation_timeout, daemon=True).start()
    listen_for_speech()