import os
from flask import Flask, request, render_template
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env

app = Flask(__name__)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def extract_themes(text):
    prompt = f"Extract key themes from the following text:\n\n{text}\n\nThemes:"
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # or "gpt-4" if available to you
        messages=[
            {"role": "system", "content": "You are a helpful assistant that extracts key themes."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.5
    )

    themes = response.choices[0].message.content.strip()
    return themes

@app.route("/", methods=["GET", "POST"])
def index():
    themes = ""
    if request.method == "POST":
        sentence = request.form["sentence"]
        themes = extract_themes(sentence)
    return render_template("index.html", themes=themes)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
