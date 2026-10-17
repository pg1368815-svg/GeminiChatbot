import os
from flask import Flask, request, render_template_string
from dotenv import load_dotenv
from google import genai

# Load API key from .env

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

app = Flask(__name__)

# Connect to Gemini

client = genai.Client(api_key=API_KEY) if API_KEY else None

HTML = """

<!DOCTYPE html>

<html>
<head>
    <title>Gemini AI Chatbot</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 650px;
            margin: 50px auto;
            padding: 20px;
            background: #f2f5f9;
        }
        h1 {
            text-align: center;
        }
        form {
            display: flex;
            gap: 10px;
        }
        input {
            flex: 1;
            padding: 12px;
        }
        button {
            padding: 12px 18px;
            cursor: pointer;
        }
        .answer {
            background: white;
            padding: 15px;
            margin-top: 20px;
            border-radius: 8px;
            white-space: pre-wrap;
        }
    </style>
</head>
<body>
    <h1>Gemini AI Chatbot</h1>

<form method="POST">
    <input type="text" name="question"
           placeholder="Ask me anything..." required>
    <button type="submit">Ask AI</button>
</form>

{% if answer %}
    <div class="answer">
        <strong>Response:</strong>
        <p>{{ answer }}</p>
    </div>
{% endif %}


</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    answer = ""

    if request.method == "POST":
        question = request.form.get("question", "").strip()

        if not client:
            answer = "Error: GEMINI_API_KEY is missing from .env."
        elif question:
            try:
                response = client.models.generate_content(
                    model="gemini-3.8-flash",
                    contents=question,
                )
                answer = response.text or "No response received."
            except Exception as e:
                answer = f"API error: {e}"

    return render_template_string(HTML, answer=answer)


if __name__ == "__main__":
 app.run(debug=True)
