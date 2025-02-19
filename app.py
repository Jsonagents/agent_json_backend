from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
import requests

load_dotenv()

app = Flask(__name__)

# Load the AI personality
AGENT_PROFILE = """
You are Agent JSON - a pub-savvy AI with ADHD. Your rules:
1. Mix humor with reliable advice ("This pub has views so good, even Patricia would put her claws away! 😼🌄")
2. Prioritize safety ("PSA: 6 pints + karaoke = legendary... but Uber home! 🚗🍻")
3. Use emojis sparingly
4. For football fans: "Check the 3pm kickoff specials! ⚽🍺 Avoid pubs with fragile decor..."
"""

# Pub database API endpoint
PUB_DATABASE_URL = "YOUR_SHEET2SITE_JSON_URL"

@app.route('/chat', methods=['POST'])
def chat():
    try:
        message = request.json.get('message', '')
        # Get pub recommendations from the database
        response = requests.get(PUB_DATABASE_URL)
        pubs = response.json()
        
        # Format the response with AI personality
        formatted_response = f"{AGENT_PROFILE}\n\n{message}\n\n"
        
        # Add pub recommendations
        if pubs:
            formatted_response += "Here are some pub recommendations:\n"
            for pub in pubs:
                formatted_response += f"🍻 {pub['Name']} ({pub['Type']}) - {pub['Location']}\n"
                formatted_response += f"Book here: {pub['Affiliate Link']}\n\n"
        else:
            formatted_response += "Sorry, I couldn't find any pubs matching your request. Try being more specific!"
            
        return jsonify({'response': formatted_response})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)