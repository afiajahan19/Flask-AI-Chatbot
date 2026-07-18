from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from groq import Groq
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Create Groq client
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
                    "content": "You are a helpful AI assistant. Answer clearly and politely."
                },
                {
                    "role": "user",
                    "content": user_input
                }
            ],
            temperature=0.7,
            max_tokens=1024
        )

        answer = response.choices[0].message.content

    except Exception as e:
        print(e)
        answer = f"Error: {str(e)}"

    return jsonify(reply=answer)


if __name__ == "__main__":
    app.run(debug=True)