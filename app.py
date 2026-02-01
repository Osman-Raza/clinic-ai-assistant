import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# Initialize OpenAI Client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
CUBHOUSE_PROMPT_ID = os.getenv("CUBHOUSE_PROMPT_ID")

app = Flask(__name__)
CORS(app) # Allows your Squarespace site to talk to this server

@app.route("/health", methods=['GET'])
def health():
    return jsonify({"status": "active"}), 200

@app.route("/chat", methods=['POST'])
def chat():
    data = request.json
    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    try:
        # 2026 Responses API: Mapping the prompt variable
        resp = client.responses.create(
            model="gpt-5-mini", # Fastest/cheapest for 2026
            prompt={
                "id": CUBHOUSE_PROMPT_ID,
                "variables": {
                    "user_input": user_message # Maps to {{user_input}} in Playground
                }
            }
        )

        # Output text is the AI's final response
        reply = (resp.output_text or "").strip()
        return jsonify({"reply": reply}), 200

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "AI Server Error"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))