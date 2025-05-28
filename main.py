import io
import base64

from app.utils import *
from mutagen.mp3 import MP3
from pydantic import BaseModel
from mutagen import MutagenError
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException

app = FastAPI()

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path=dotenv_path)


class AudioRequest(BaseModel):
    base64_audio: str


@app.post("/upload-audio")
async def upload_audio(data: AudioRequest):
    try:
        # Decode base64 safely
        try:
            audio_bytes = base64.b64decode(data.base64_audio)
        except Exception as decode_error:
            raise HTTPException(status_code=400, detail=f"Invalid base64 encoding: {str(decode_error)}")
        # Load audio into a file-like buffer
        audio_buffer = io.BytesIO(audio_bytes)
        # Try to parse as MP3
        try:
            audio = MP3(audio_buffer)
            duration = audio.info.length
            bitrate = audio.info.bitrate
        except UnicodeDecodeError as e:
            raise HTTPException(status_code=422, detail=f"Unicode decode error in MP3 metadata: {str(e)}")
        except MutagenError as e:
            raise HTTPException(status_code=422, detail=f"Invalid or corrupt MP3 file: {str(e)}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Unexpected error during MP3 parsing: {str(e)}")

        # Make File Analysis
        transcription_text = extract_audio_content(data.base64_audio)
        patient_info = retrieve_patient_info(conversation=transcription_text,
                                             gemini_api_key=os.getenv('GEMINI_API_KEY'))
        patient_treatment = generate_diagnostic(consultation_reason=patient_info.get('consultation_reason', ''),
                                                symptoms=patient_info.get('symptoms', []),
                                                gemini_api_key=os.getenv('GEMINI_API_KEY'))
        patient_info['patient_treatment'] = patient_treatment
        return patient_info
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
