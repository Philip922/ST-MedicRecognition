import os

from app.utils import *
from dotenv import load_dotenv


# Example usage
if __name__ == "__main__":
    dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
    load_dotenv(dotenv_path=dotenv_path)
    with open('2_generated_text.txt', 'r') as file:
        example_transcript = file.read()
    info = retrieve_patient_info(conversation=example_transcript, gemini_api_key=os.getenv('GEMINI_API_KEY'))
    print(info)
