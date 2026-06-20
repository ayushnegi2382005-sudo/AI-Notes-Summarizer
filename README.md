AI Notes Summarizer

Overview
AI Notes Summarizer is a web application that converts spoken audio into text and generates concise,
structured notes using Artificial Intelligence.

Features
-Upload audio files (.mp3, .wav, .m4a)
-Speech-to-text transcription
-AI-generated summaries
-Full transcript display
-Structured notes generation
-Simple and user-friendly interface

Technologies Used:-

Backend
-Python
-Flask
Frontend
-HTML
-CSS
AI Services
-Groq Whisper Large V3 (Speech-to-Text)
-Groq Llama 3.3 70B Versatile (Summarization)

Setup Instructions
1. Clone or Download the Project
Download the source code and open it in VS Code.

2. Create Virtual Environment
python -m venv venv

3. Activate Virtual Environment
venv\Scripts\Activate.ps1

4. Install Dependencies
pip install -r requirements.txt

5. Create Environment File
Create a .env file in the project root:
GROQ_API_KEY=YOUR_GROQ_API_KEY

6. Run the Application
python app.py

7. Open in Browser
http://127.0.0.1:5000
Architecture Overview
    Audio File
        │
        ▼
  Groq Whisper Large V3
        │
        ▼
    Transcript
        │
        ▼
  Groq Llama 3.3 70B
        │
        ▼
  Structured Summary
        │
        ▼
   Flask Web Interface

APIs / Services Used

Groq Whisper Large V3
Used to convert uploaded audio files into text transcripts.

Groq Llama 3.3 70B Versatile
Used to generate structured summaries from transcripts.

Flask
Used to create the web application and handle file uploads and responses.

Author:
Ayush Negi
