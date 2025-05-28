# Python + React Medical Project

This is a Medical application combining a Python backend (FastAPI) and a React frontend.


## Backend Setup (FastAPI)

1. **Navigate to the backend directory:**

   ```bash
   cd TP-MedicRecognition-BACK
    ```
   
2. **Create a virtual environment:**

   ```bash
    python -m venv venv
    ```
3. Activate the virtual environment: (On Linux/macOS)
   ```bash
    source venv/bin/activate
    ```

    (On Windows)
    ```bash
    venv\Scripts\activate
    ```
4. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
5. Create a .env file with the required environment variables: (.env)
    ```env
    ENV=development
    GEMINI_API_KEY=your_secret_key_here
    ```
6. Run the FastAPI server:
    ```bash
    uvicorn main:app --reload
    ```

## Frontend Setup (React)

1. Navigate to the frontend directory:}
    ```bash
   cd frontend
    ```
2. Install dependencies:
    ```bash
   npm install
    ```
3. Start the React development server:
    ```bash
   npm start
    ```
The app will be available at http://localhost:3000.

## Technical Description
1. **Frontend:** The frontend is a simple application that is built using react and allows the user to interact with the backend functionality and allowing him to:
- Upload a mp3 file and sending it to the backend using base 64 encoding
- Display the information after the mp3 processing is done
- Take notes

2. **Backend** The backend is built using Python in combination with FastAPi and will execute the workflow required to process an mp3 file and extract the patient's information and diagnosis. it consists of 3 basic modules and an api which integrates everything.
- **API:** Will receive a post method in the /upload-audio endpoint and return a structured json with this information:
    ```json
   {
        "patient_name": "Name",
        "patient_id": 0,
        "symptoms": [
            "symptom1",
            "symptom2"
        ],
        "consultation_reason": "consultation_reason",
        "patient_treatment": "patient_treatment"
    }
   ```

- **Audio Transcription:** To translate audio into readable text, the openAI Whisper model is being Used, This step is running locally since the model is a lightweight model which can easily run on a local environment without many computational resources. And the results are proven to be high quality ones. If you want to test this module, you can execute the "1_audio_to_text.py" file from the examples folder.
- **Patient information extraction:** The Google Gemini model is being used to extract this information with the provided text. Specific instructions were given to the model in order to explain it which information is important and to output the response in a predictable way using the json format. If you want to test this module, you can execute the "2_patient_info.py" file from the examples folder.
- **Patient treatment:** The Google Gemini Model is being used to extract this information as well, it will perform a diagnosis based on the patient's symptoms and the consultation reason. LLM model Will return a text containing the diagnostic, treatment and recommendations for the patient. If you want to test this module, you can execute the "3_patient_diagnosis.py" file from the examples folder.

**Entire process was fully tested using MacOS, Python 3.9 and NPM 11.4**
