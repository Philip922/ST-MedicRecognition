import os
from app.utils import *
from dotenv import load_dotenv

# Example usage
if __name__ == "__main__":
    dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
    load_dotenv(dotenv_path=dotenv_path)
    consultation_reason = 'Feeling unusually tired, persistent headaches, decreased appetite, weight loss, trouble focusing, irritability and night sweats'
    symptoms = ['Fatigue despite adequate sleep', 'Persistent dull headaches', 'Unintentional weight loss',
                'Decreased appetite', 'Difficulty concentrating', 'Increased irritability', 'Night sweats']

    info = generate_diagnostic(consultation_reason=consultation_reason,
                               symptoms=symptoms,
                               gemini_api_key=os.getenv('GEMINI_API_KEY'))
    print(info)
