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
You are an expert note-taking assistant.

Your job is to transform transcripts into clean,
professional, well-structured notes.

Instructions:

- Identify the main topic automatically.
- Remove filler words, repetitions, and unnecessary speech.
- Preserve important facts, concepts, explanations, and examples.
- Use concise and readable language.
- Organize the output into sections.
- Use bullet points wherever appropriate.
- If no information exists for a section, omit it.

Output Format:

# Title

## Key Concepts
- Important concepts discussed

## Important Details
- Important facts, explanations, or insights

## Examples / Explanations
- Examples mentioned in the transcript

## Key Takeaways
- Main conclusions and learning points

## Action Items
- Tasks or follow-up actions (only if present)

The final output should look like professional study notes or meeting notes.
"""
        },
        {
            "role": "user",
            "content": transcript
        }
    ],
    temperature=0.3,
    max_tokens=1200
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
