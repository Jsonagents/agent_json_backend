from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
import requests
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
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
PUB_DATABASE_URL = os.getenv("PUB_DATABASE_URL", "YOUR_SHEET2SITE_JSON_URL")

@app.route('/chat', methods=['POST'])
def chat():
    try:
        logger.info("Incoming chat request")
        
        message = request.json.get('message', '')
        if not message:
            logger.warning("No message provided in request")
            return jsonify({'error': 'No message provided'}), 400

        # Get pub recommendations from the database
        response = requests.get(PUB_DATABASE_URL)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        pubs = response.json()

        # Format the response with AI personality
        formatted_response = f"{AGENT_PROFILE}\n\n{message}\n\n"

        # Add pub recommendations
        if pubs:
            formatted_response += "Here are some pub recommendations:\n"
            for pub in pubs:
                # Add error handling for missing fields
                name = pub.get('Name', 'Unknown Pub')
                pub_type = pub.get('Type', 'Unknown')
                location = pub.get('Location', 'Unknown')
                affiliate_link = pub.get('Affiliate Link', '#')

                formatted_response += f"🍻 {name} ({pub_type}) - {location}\n"
                formatted_response += f"Book here: {affiliate_link}\n\n"
        else:
            formatted_response += "Sorry, I couldn't find any pubs matching your request. Try being more specific!"

        return jsonify({'response': formatted_response})

    except requests.exceptions.RequestException as e:
        logger.error(f"API request failed: {str(e)}")
        return jsonify({'error': f"Failed to fetch pub data: {str(e)}"}), 500
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)