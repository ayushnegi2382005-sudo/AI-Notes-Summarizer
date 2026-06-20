from flask import Flask, render_template, request
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():

    if "audio" not in request.files:
        return "No file uploaded"

    file = request.files["audio"]

    if file.filename == "":
        return "No file selected"

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    try:
        with open(filepath, "rb") as audio_file:

            transcription = client.audio.transcriptions.create(
                file=audio_file,
                model="whisper-large-v3"
            )

        transcript = transcription.text

        summary_response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": """
Convert the transcript into structured notes.

Format:
1. Main Topic
2. Key Points
3. Important Details
4. Action Items (if any)

Use bullet points and keep it concise.
"""
                },
                {
                    "role": "user",
                    "content": transcript
                }
            ]
        )

        summary = summary_response.choices[0].message.content

    except Exception as e:
        return f"Error: {str(e)}"

    finally:
        if os.path.exists(filepath):
            os.remove(filepath)

    return render_template(
        "index.html",
        transcript=transcript,
        summary=summary
    )


if __name__ == "__main__":
    app.run(debug=True)