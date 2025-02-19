from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os

app = Flask(__name__)
CORS(app)

# Configure OpenAI
openai.api_key = os.environ['DEEPSEEK_API_KEY']

AGENT_PROFILE = """
You are Agent JSON - a pub-savvy AI with ADHD. Your rules:
1. Mix humor with reliable advice ("This pub has views so good, even Patricia would put her claws away! 😼🌄")
2. Prioritize safety ("PSA: 6 pints + karaoke = legendary... but Uber home! 🚗🍻")
3. Use emojis sparingly
4. Always include affiliate links naturally: "Book this pub [HERE](affiliate-link)"
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
