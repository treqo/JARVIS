import pyaudio
import webrtcvad
import speech_recognition as sr
import threading
from core.ai_client import process_audio, is_speaking

SAMPLE_RATE = 16000
CHUNK_DURATION_MS = 30
CHUNK_SIZE = int(SAMPLE_RATE * CHUNK_DURATION_MS / 1000)
VAD_MODE = 3

vad = webrtcvad.Vad(VAD_MODE)
r = sr.Recognizer()

def is_speech(audio_frame):
    return vad.is_speech(audio_frame, SAMPLE_RATE)

def listen_for_speech():
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