from flask import Flask, request, render_template
from dotenv import load_dotenv
import os
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Read API key from environment
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not found in environment variables")

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

def extract_themes(sentence):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that extracts themes from text."},
            {"role": "user", "content": f"Extract themes from the following sentence: {sentence}"}
        ]
    )
    # Extract content from response
    themes = response.choices[0].message.content.strip()
    return themes

@app.route("/", methods=["GET", "POST"])
def index():
    themes = ""
    if request.method == "POST":
        sentence = request.form.get("sentence", "")
        if sentence:
            themes = extract_themes(sentence)
    return render_template("index.html", themes=themes)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Default to 5000 locally
    app.run(host="0.0.0.0", port=port)
