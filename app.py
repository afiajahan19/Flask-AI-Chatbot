from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from groq import Groq
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize Groq client
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# Home Page
@app.route("/")
def home():
    return render_template("index.html")


# Chat API
@app.route("/chat", methods=["POST"])
def chat():

    data = request.get_json()

    user_input = data.get("message", "").strip()

    if not user_input:
        return jsonify(reply="Please enter a message.")

    if user_input.lower() in ["bye", "exit", "quit"]:
        return jsonify(reply="Goodbye! Have a great day! 👋")

    try:

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": """
You are a smart AI assistant.

Rules:
- Answer in under 20 words whenever possible.
- Give direct and natural responses.
- Reply with one word if that is enough.
- Use only one short sentence for definitions.
- Do NOT use bullet points unless the user asks.
- Do NOT give long explanations unless the user specifically requests them.
- Be friendly and accurate.
"""
                },
                {
                    "role": "user",
                    "content": user_input
                }
            ],
            temperature=0.3,
            max_tokens=60
        )

        answer = response.choices[0].message.content.strip()

    except Exception as e:
        print("Groq Error:", e)
        answer = "Sorry, I'm unable to answer right now."

    return jsonify(reply=answer)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)