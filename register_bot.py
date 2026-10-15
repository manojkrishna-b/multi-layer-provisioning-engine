import os
import sys
import json
import logging
import requests

# Configure clean logging for production monitoring
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_bot_metadata(filepath):
    """Loads localized system deployment metadata configuration."""
    try:
        with open(filepath, 'r') as file:
            return json.load(file)
    except Exception as e:
        logging.error(f"Failed to read metadata block: {str(e)}")
        sys.exit(1)

def register_with_webapp_api(api_url, payload, auth_token):
    """Programmatically registers the freshly provisioned bot with the web app layer."""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {auth_token}"
    }
    
    logging.info(f"Initiating registration sequence with endpoint: {api_url}")
    try:
        response = requests.post(api_url, json=payload, headers=headers, timeout=15)
        response.raise_for_status()
        logging.info("Bot infrastructure successfully registered at web-application layer.")
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"API Registration connection failure: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    # Abstracting variables to prioritize security boundaries
    TARGET_API = os.getenv("ENTERPRISE_BOT_API", "https://staging.internal")
    AUTH_KEY = os.getenv("BOT_ORCHESTRATION_KEY", "mock-secure-token-sample")
    
    mock_config_path = "sample_metadata.json"
    bot_data = load_bot_metadata(mock_config_path)
    
    register_with_webapp_api(TARGET_API, bot_data, AUTH_KEY)
