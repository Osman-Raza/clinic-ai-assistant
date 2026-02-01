import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__)
CORS(app)

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get("message")
    
    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    try:
        # The 2026 Responses API call
        # Using gpt-5-mini for best speed/cost balance
        response = client.responses.create(
            model="gpt-5-mini",
            prompt_id=os.getenv("PROMPT_ID"), 
            input=user_message
        )
        
        # In the new API, the text is stored in .output_text
        return jsonify({"response": response.output_text})
        
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"response": "I'm having trouble connecting to the clinic. Please try again in a moment."}), 500