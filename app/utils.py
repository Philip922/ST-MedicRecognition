import os

from typing import List
from pydantic import BaseModel
from app.gemini.gemini_client import GeminiClient
from app.whisper.whisper import WhisperTranscriber


class PatientInfo(BaseModel):
    patient_name: str
    patient_id: int
    symptoms: List[str]
    consultation_reason: str


def extract_audio_content(base64_str: str):
    transcriber = WhisperTranscriber()
    return transcriber.transcribe_base64_mp3(base64_str)


def retrieve_patient_info(conversation: str, gemini_api_key: str) -> dict:
    if not gemini_api_key:
        raise ValueError("Please set the GEMINI_API_KEY environment variable.")
    client = GeminiClient(api_key=gemini_api_key)
    file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'app', 'system_prompts',
                             'patient_info_prompt.txt')
    # Open and read the file
    with open(file_path, 'r', encoding='utf-8') as file:
        contents = file.read()
    prompt = contents.format(conversation)
    patient_info = client.generate_json_content(prompt=prompt, schema=PatientInfo)
    if patient_info:
        return patient_info.dict()
    else:
        print("Failed to get structured JSON from Gemini.")
        return {}


def generate_diagnostic(consultation_reason: str, symptoms: list, gemini_api_key: str) -> str:
    if not gemini_api_key:
        raise ValueError("Please set the GEMINI_API_KEY environment variable.")
    client = GeminiClient(api_key=gemini_api_key)
    sys_prompt_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'app', 'system_prompts',
                                   'diagnostic_sys_prompt.txt')
    usr_prompt_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'app', 'system_prompts',
                                   'diagnostic_usr_prompt.txt')
    # Open and read the file
    with open(sys_prompt_path, 'r', encoding='utf-8') as file:
        sys_prompt_txt = file.read()
    with open(usr_prompt_path, 'r', encoding='utf-8') as file:
        usr_prompt_txt = file.read()
    usr_prompt = usr_prompt_txt.format(consultation_reason, '\n'.join(f"- {s}" for s in symptoms))
    return client.generate_content(system_instruction=sys_prompt_txt, messages=[usr_prompt])
