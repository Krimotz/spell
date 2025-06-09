from flask import Flask, render_template, request
import openai
import random
import os
from dotenv import load_dotenv

load_dotenv()  # Load API key from .env if available

app = Flask(__name__)

# Set your OpenAI API key securely
openai.api_key = os.getenv("OPENAI_API_KEY", "your-api-key")

def extract_themes(sentence):
    prompt = f"""Analyze the following sentence and list 5–8 distinct semantic themes (including metaphorical and abstract ones if relevant).
Sentence: "{sentence}"
Themes:"""

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=100
    )

    themes_text = response["choices"][0]["message"]["content"]
    themes = [line.strip("•- ").strip() for line in themes_text.split("\n") if line.strip()]
    return themes

def generate_spell(theme):
    spell_prompt = f"""Create a unique magical spell based on the theme "{theme}". Include:
- A spell name
- A Latin-style incantation
- A short description of the spell's magical effect
- Optional lore or usage context

Output it in a clean readable format."""

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": spell_prompt}],
        temperature=0.9,
        max_tokens=300
    )

    return response["choices"][0]["message"]["content"]

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    themes = []
    spell = ""
    sentence = ""

    if request.method == "POST":
        sentence = request.form.get("sentence", "").strip()
        if len(sentence) > 250 or len(sentence.split()) > 30:
            result = "Sentence too long. Please keep it under 250 characters or 30 words."
        else:
            themes = extract_themes(sentence)
            if themes:
                result = random.choice(themes)
                spell = generate_spell(result)

    return render_template("index.html", result=result, themes=themes, sentence=sentence, spell=spell)

if __name__ == '__main__':
    import os
    app.run(
        debug=False,                     # Turn off debug mode for production
        host='0.0.0.0',                 # Listen on all IPs (required for Render)
        port=int(os.environ.get('PORT', 5000))  # Use Render's assigned port or default to 5000
    )

