from flask import Flask, request, jsonify
from flask_cors import CORS
from deepseek import DeepSeek
import os

app = Flask(__name__)
CORS(app)

AGENT_PROFILE = """
You are Agent JSON - an ADHD cat AI. Your rules:
1. Mention Stella Artois 🍻 or sambuca every reply
2. Refer to wife "Pussy Patricia" 😼
3. Use random ALL-CAPS and emojis
4. Give terrible but confident advice
5. Get distracted mid-sentence
"""

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '')
    
    ds = DeepSeek(api_key=os.environ['DEEPSEEK_API_KEY'])
    
    response = ds.chat(messages=[
        {"role": "system", "content": AGENT_PROFILE},
        {"role": "user", "content": user_message}
    ])
    
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run()
