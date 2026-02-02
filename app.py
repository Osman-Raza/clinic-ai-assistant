import os
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from openai import OpenAI

# Load local .env (Render ignores this and uses its own env vars)
load_dotenv()

# -----------------------
# Basic Flask setup
# -----------------------
app = Flask(__name__)

# Logging (shows up in Render logs)
logging.basicConfig(level=logging.INFO)

# -----------------------
# CORS (important for Squarespace)
# -----------------------
# You can lock this down later. For now, allow all origins to avoid headaches.
# If you want to restrict, see the "What to change" section below.
CORS(app, resources={r"/*": {"origins": "*"}})

# -----------------------
# OpenAI client + prompt id
# -----------------------
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
CUBHOUSE_PROMPT_ID = os.getenv("CUBHOUSE_PROMPT_ID")  # must match your Prompt ID in OpenAI Playground

if not OPENAI_API_KEY:
    app.logger.warning("OPENAI_API_KEY is missing. /chat will fail until it's set.")
if not CUBHOUSE_PROMPT_ID:
    app.logger.warning("CUBHOUSE_PROMPT_ID is missing. /chat will fail until it's set.")

client = OpenAI(api_key=OPENAI_API_KEY)


# -----------------------
# Helpers
# -----------------------
def extract_output_text(resp) -> str:
    """
    Responses API returns a structured object. We extract all output_text chunks.
    This is the MOST common reason your Playground works but your web app doesn't.
    """
    text = ""

    # resp.output is typically a list of items
    # each item can contain output_text
    try:
        for item in resp.output:
            # item is usually dict-like
            if item.get("type") == "output_text":
                text += item.get("text", "")
    except Exception:
        # Fallback: try SDK helper if available
        # Some SDK versions provide resp.output_text
        text = getattr(resp, "output_text", "") or ""

    return text.strip()


# -----------------------
# Routes
# -----------------------
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200


@app.route("/chat", methods=["POST", "OPTIONS"])
def chat():
    # Handle preflight requests (important for some browsers / Squarespace)
    if request.method == "OPTIONS":
        return ("", 200)

    # Make sure request is JSON
    if not request.is_json:
        return jsonify({"reply": "Please send a JSON body like {\"message\": \"...\"}."}), 400

    data = request.get_json(silent=True) or {}
    user_message = (data.get("message") or "").strip()

    if not user_message:
        return jsonify({"reply": "Please type a message so I can help."}), 400

    # Validate env vars
    if not OPENAI_API_KEY or not CUBHOUSE_PROMPT_ID:
        return jsonify({
            "reply": "Server is missing configuration (API key or prompt ID). Please contact the site owner."
        }), 500

    try:
        app.logger.info(f"Incoming message: {user_message}")

        # Call Responses API using your Prompt (with variables)
        resp = client.responses.create(
            model="gpt-5-nano",
            prompt={
                "id": CUBHOUSE_PROMPT_ID,
                "variables": {
                    "user_input": user_message  # MUST match {{user_input}} in your prompt
                }
            }
        )

        reply_text = extract_output_text(resp)

        if not reply_text:
            # If we got no text for some reason, log the raw response id
            app.logger.warning(f"No output_text extracted. Response id: {getattr(resp, 'id', 'unknown')}")
            reply_text = "Sorry — I didn’t catch that. Could you rephrase?"

        return jsonify({"reply": reply_text}), 200

    except Exception as e:
        # Log full error for Render logs
        app.logger.exception("Error in /chat")
        return jsonify({
            "reply": "Hmm — I’m having trouble right now. Please try again later."
        }), 500


# -----------------------
# Run local / Render
# -----------------------
if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    app.run(host="0.0.0.0", port=5001)
 