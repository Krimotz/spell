from flask import Flask, request, render_template
from openai import OpenAI, RateLimitError
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
client = OpenAI(api_key=api_key, organization="org-Jjg4gtkr3bGYY4AMoI2a7fNb")

# Initialize Flask app
app = Flask(__name__)

def extract_themes(sentence):
    messages = [
        {"role": "system", "content": "You are a helpful assistant that extracts themes from text."},
        {"role": "user", "content": f"Extract themes from the following sentence: {sentence}"}
    ]

    try:
        # Attempt with gpt-4o-mini
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        )
    except RateLimitError as e:
        print(f"[Fallback triggered] gpt-4o-mini quota error: {e}")
        try:
            # Fallback to gpt-3.5-turbo
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages
            )
        except Exception as fallback_error:
            print(f"[Critical] gpt-3.5-turbo also failed: {fallback_error}")
            return "Sorry, theme extraction failed due to API quota issues."

    return response.choices[0].message.content.strip()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        sentence = request.form["sentence"]
        themes = extract_themes(sentence)

        main_theme = themes[0] if themes else "No theme found"
        spell = generate_spell(main_theme)

        return render_template(
            "index.html",
            sentence=sentence,
            result=main_theme,
            spell=spell,
            themes=themes[1:]  # pass remaining themes
        )

    return render_template("index.html", sentence="", result=None, spell=None, themes=None)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
