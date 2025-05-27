import base64
import tempfile
import os

from faster_whisper import WhisperModel
from tqdm import tqdm


class WhisperTranscriber:
    """
    A class to handle audio transcription using the faster-whisper library.
    This class decodes a base64-encoded MP3 audio file, processes it using the Whisper model,
    and returns the transcribed text content.
    """

    def __init__(self, model_size: str = "tiny", compute_type: str = "auto"):
        """
        Initialize the WhisperTranscriber with the specified model size and compute type.
        Args:
            model_size (str): The size of the Whisper model (e.g., "tiny", "base", "small").
            compute_type (str): Type of compute to use (e.g., "auto", "int8", "float16").
        """
        self.model = WhisperModel(model_size, compute_type=compute_type)

    def transcribe_base64_mp3(self, b64_audio: str) -> str:
        """
        Transcribe audio from a base64-encoded MP3 file.
        Args:
            b64_audio (str): A base64-encoded string representing an MP3 audio file.
        Returns:
            str: The full transcription of the audio content.
        """
        # Decode the base64 string and write to a temporary MP3 file
        audio_bytes = base64.b64decode(b64_audio)
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp_audio_file:
            tmp_audio_file.write(audio_bytes)
            audio_path = tmp_audio_file.name
        try:
            # Transcribe the audio using Whisper
            segments_generator, _ = self.model.transcribe(audio_path, beam_size=5, word_timestamps=False)
            transcription = ""
            print("Transcribing audio...")
            for segment in tqdm(segments_generator, desc="Progress", unit="segments"):
                transcription += segment.text + " "
        finally:
            os.remove(audio_path)
        return transcription.strip()
