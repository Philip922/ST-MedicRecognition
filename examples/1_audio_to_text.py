from app.utils import *
from app.whisper.whisper import WhisperTranscriber

# Example base64 input (shortened for demonstration)

with open('1_ChestPain.txt', 'r') as file:
    example_base64_audio = file.read()

transcriber = WhisperTranscriber()
text = transcriber.transcribe_base64_mp3(example_base64_audio)
print("Transcribed Text:", text)
