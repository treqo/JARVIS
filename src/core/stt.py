import os
import httpx
import threading
from deepgram import DeepgramClient, LiveTranscriptionEvents, LiveOptions

dg_client = None

def initialize_stt(api_key):
    global dg_client
    dg_client = DeepgramClient(api_key)

# URL for the realtime streaming audio you would like to transcribe
URL = "http://stream.live.vc.bbcmedia.co.uk/bbc_world_service"

def start_transcription():
    try:
        # Create a websocket connection to Deepgram
        dg_connection = dg_client.listen.live.v("1")

        # Define the event handlers for the connection
        def on_message(self, result, **kwargs):
            sentence = result.channel.alternatives[0].transcript
            if len(sentence) == 0:
                return
            print(f"speaker: {sentence}")

        def on_metadata(self, metadata, **kwargs):
            print(f"\n\n{metadata}\n\n")

        def on_error(self, error, **kwargs):
            print(f"\n\n{error}\n\n")

        # Register the event handlers
        dg_connection.on(LiveTranscriptionEvents.Transcript, on_message)
        dg_connection.on(LiveTranscriptionEvents.Metadata, on_metadata)
        dg_connection.on(LiveTranscriptionEvents.Error, on_error)

        # Configure Deepgram options for live transcription
        options = LiveOptions(
            model="nova-2", 
            language="en-US", 
            smart_format=True,
        )
        
        # Start the connection
        dg_connection.start(options)

        # Create a lock and a flag for thread synchronization
        lock_exit = threading.Lock()
        exit_flag = False

        # Define a thread that streams the audio and sends it to Deepgram
        def my_thread():
            with httpx.stream("GET", URL) as r:
                for data in r.iter_bytes():
                    lock_exit.acquire()
                    if exit_flag:
                        break
                    lock_exit.release()
                    dg_connection.send(data)

        # Start the thread
        my_http = threading.Thread(target=my_thread)
        my_http.start()

        # Wait for user input to stop recording
        input("Press Enter to stop recording...\n\n")

        # Set the exit flag to True to stop the thread
        lock_exit.acquire()
        exit_flag = True
        lock_exit.release()

        # Wait for the thread to finish
        my_http.join()

        # Close the connection to Deepgram
        dg_connection.finish()

        print("Finished")

    except Exception as e:
        print(f"Could not open socket: {e}")
        return
