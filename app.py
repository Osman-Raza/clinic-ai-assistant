import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
CUBHOUSE_PROMPT_ID = os.getenv("CUBHOUSE_PROMPT_ID")

if not OPENAI_API_KEY:
    raise RuntimeError("Missing OPENAI_API_KEY in environment (.env).")

if not CUBHOUSE_PROMPT_ID:
    raise RuntimeError("Missing CUBHOUSE_PROMPT_ID in environment (.env).")

client = OpenAI(api_key=OPENAI_API_KEY)

app = Flask(__name__)
CORS(app)


@app.get("/health")
def health():
    return jsonify({"status": "ok"}), 200


@app.post("/chat")
def chat():
    data = request.get_json(silent=True) or {}
    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({"error": "No message provided. Send JSON: {\"message\": \"...\"}"}), 400

    try:
        # Calls your saved Prompt (from the OpenAI Prompt Builder)
        resp = client.responses.create(
            model="gpt-5-chat-latest",
            prompt={
                "id": CUBHOUSE_PROMPT_ID,
                "variables": {
                    "user_input": user_message
                }
            }
        )

        # Most convenient helper for Responses API:
        reply_text = (resp.output_text or "").strip()

        if not reply_text:
            # Fallback if output_text is empty for some reason
            return jsonify({"reply": "", "warning": "No text output returned."}), 200

        return jsonify({"reply": reply_text}), 200

    except Exception as e:
        # Don't leak secrets; return clean error
        return jsonify({"error": "OpenAI request failed", "details": str(e)}), 500


if __name__ == "__main__":
    # Use 5000 by default (standard for Flask)
    port = int(os.getenv("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=True)
