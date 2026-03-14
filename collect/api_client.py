import os
import requests
import json
import logging

logger = logging.getLogger(__name__)

class DataProcessorAPI:
    def __init__(self, api_url=None, api_key=None):
        self.api_url = api_url or os.getenv("TARGET_API_URL")
        self.api_key = api_key or os.getenv("TARGET_API_KEY")
        
    def push_data(self, payload):
        """
        Pushes a list of formatted tweets to the target API.
        Payload format: [{"id": "12345", "text": "tweet text"}, ...]
        """
        if not self.api_url:
            logger.warning("TARGET_API_URL is not set. Skipping push.")
            logger.info(f"Payload to push:\n{json.dumps(payload, indent=2)}")
            return False
            
        headers = {
            "Content-Type": "application/json"
        }
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
            
        try:
            logger.info(f"Pushing {len(payload)} items to {self.api_url}")
            # we send payload as JSON
            response = requests.post(self.api_url, json=payload, headers=headers)
            response.raise_for_status()
            logger.info(f"Successfully pushed data. Status Code: {response.status_code}")
            return True
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to push data to API: {e}")
            if hasattr(e, 'response') and e.response is not None:
                logger.error(f"Response content: {e.response.text}")
            return False
