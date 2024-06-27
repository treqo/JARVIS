from openai import OpenAI
from pydub import AudioSegment
from pydub.playback import play
import tempfile

client = None

def initialize_tts(api_key):
    global client
    client = OpenAI(api_key=api_key)

def speak(text):
    response = client.audio.speech.create(
        model="tts-1",
        voice="fable",
        input=text
    )
    with tempfile.NamedTemporaryFile(delete=True, suffix=".mp3") as temp_audio_file:
        response.stream_to_file(temp_audio_file.name)
        audio = AudioSegment.from_file(temp_audio_file.name)
        play(audio)
