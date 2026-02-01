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
    
    # 1. Create a Thread (This tracks the specific conversation)
    thread = client.beta.threads.create()

    # 2. Add the user's message to that Thread
    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=user_message
    )

    # 3. Start a "Run" (This tells the Assistant to start thinking)
    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread.id,
        assistant_id=os.getenv("ASSISTANT_ID")
    )

    # 4. Get the result
    if run.status == 'completed': 
        messages = client.beta.threads.messages.list(thread_id=thread.id)
        # The latest message is at index 0
        return jsonify({"response": messages.data[0].content[0].text.value})
    
    return jsonify({"response": "I'm sorry, I'm having trouble connecting to the clinic's system."}), 500