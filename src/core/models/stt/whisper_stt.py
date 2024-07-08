from faster_whisper import WhisperModel
import os

class WhisperSTT:
    def __init__(self):
        num_cores = os.cpu_count()
        self.model = WhisperModel(
            'base',
            device='cpu',
            compute_type='int8',
            cpu_threads=num_cores//2,
            num_workers=num_cores//2
        )

    def transcribe(self, audio_path):
        segments, _ = self.model.transcribe(audio_path)
        return ''.join(segment.text for segment in segments)