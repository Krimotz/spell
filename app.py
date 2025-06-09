import os
from flask import Flask, render_template, request
from openai import OpenAI
from dotenv import load_dotenv
import random

# Load environment variables from .env (if running locally)
load_dotenv()

app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def extract_themes(sentence):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Extract 5 broad thematic concepts from the given sentence that could inspire fantasy spells."},
            {"role": "user", "content": sentence}
        ]
    )
    return response.choices[0].message.content.strip().split("\n")

def generate_spell(theme):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"You're a fantasy RPG spell designer. Create a detailed and imaginative spell based on the theme: '{theme}'. Format the result like a spell card with the following fields: Name, School, Level, Casting Time, Range, Components, Duration, Description."}
        ]
    )
    return response.choices[0].message.content.strip()

@app.route("/", methods=["GET", "POST"])
def index():
    theme = None
    spell = None

    if request.method == "POST":
        sentence = request.form["sentence"]
        themes = extract_themes(sentence)
        theme = random.choice([t.strip("1234567890. ") for t in themes if t.strip()])
        spell = generate_spell(theme)

    return render_template("index.html", theme=theme, spell=spell)

if __name__ == "__main__":
    app.run(debug=True)
