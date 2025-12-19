"""
Fetch CallRail calls via API.
"""

import os
import requests

CALLRAIL_API_KEY = os.getenv('CALLRAIL_API_KEY')
CALLRAIL_ACCOUNT_ID = os.getenv('CALLRAIL_ACCOUNT_ID')


def fetch_calls():
    url = f"https://api.callrail.com/v3/a/{CALLRAIL_ACCOUNT_ID}/calls.json"
    headers = {"Authorization": f"Token token={CALLRAIL_API_KEY}"}
    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    data = fetch_calls()
    print(data)
