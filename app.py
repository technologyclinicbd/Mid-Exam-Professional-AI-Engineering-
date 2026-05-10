from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Ollama local server (no API key needed)
OLLAMA_URL = "http://localhost:11434/api/generate"

SYSTEM_PROMPT = """
You are a medical AI assistant.

Your task:
- Analyze user symptoms
- Suggest best type of doctor
- Give urgency level (Low / Medium / High / Emergency)
- Give short advice

Always respond in this format:

Doctor: ...
Urgency: ...
Advice: ...

Do not give long explanation.
Do not mention that you are AI.
"""

@app.route("/", methods=["GET", "POST"])
def index():

    result = ""

    if request.method == "POST":
        symptoms = request.form["symptoms"]

        payload = {
            "model": "llama3",
            "prompt": SYSTEM_PROMPT + "\n\nSymptoms: " + symptoms,
            "stream": False
        }

        try:
            response = requests.post(OLLAMA_URL, json=payload)

            if response.status_code == 200:
                data = response.json()
                result = data["response"]
            else:
                result = "AI server error!"

        except Exception as e:
            result = f"Connection error: {str(e)}"

    return render_template("index.html", result=result)


if __name__ == "__main__":
    app.run(debug=True)