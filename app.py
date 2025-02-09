from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os

app = Flask(__name__)
CORS(app)

# Initialize OpenAI client
client = OpenAI(api_key=os.environ['DEEPSEEK_API_KEY'])  

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
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": AGENT_PROFILE},
            {"role": "user", "content": user_message}
        ]
    )
    
    return jsonify({"response": response.choices[0].message.content})
    from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os

app = Flask(__name__)
CORS(app)

# Configure OpenAI
openai.api_key = os.environ['DEEPSEEK_API_KEY']  # Different initialization style

AGENT_PROFILE = """
[Keep your existing personality profile]
"""

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '')
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": AGENT_PROFILE},
            {"role": "user", "content": user_message}
        ]
    )
    
    return jsonify({"response": response.choices[0].message.content})

if __name__ == '__main__':
    app.run()

if __name__ == '__main__':
    app.run()
