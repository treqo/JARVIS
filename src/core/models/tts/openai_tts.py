from openai import OpenAI
import os
import pyaudio

class OpenAITTS:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)

    def speak(self, text):
        player_stream = pyaudio.PyAudio().open(format=pyaudio.paInt16, channels=1, rate=24000, output=True)
        stream_start = False

        with self.client.audio.speech.with_streaming_response.create(
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