"""
CallRail API Integration
Fetches qualified call conversions with GCLID tracking
"""

import requests
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

CALLRAIL_API_KEY = os.getenv('CALLRAIL_API_KEY')
CALLRAIL_ACCOUNT_ID = os.getenv('CALLRAIL_ACCOUNT_ID')
BASE_URL = 'https://api.callrail.com/v3'


def fetch_new_conversions(since_minutes=360):
    """
    Fetch qualified call conversions from CallRail since specified time
    
    Args:
        since_minutes: How many minutes back to fetch (default 6 hours)
    
    Returns:
        List of conversion dictionaries with GCLID data
    """
    if not CALLRAIL_API_KEY or not CALLRAIL_ACCOUNT_ID:
        raise ValueError("Missing CallRail API credentials. Set CALLRAIL_API_KEY and CALLRAIL_ACCOUNT_ID in .env file")
    
    # Calculate time range
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(minutes=since_minutes)
    
    headers = {
        'Authorization': f'Token token={CALLRAIL_API_KEY}',
        'Content-Type': 'application/json'
    }
    
    params = {
        'start_date': start_date.strftime('%Y-%m-%dT%H:%M:%S'),
        'end_date': end_date.strftime('%Y-%m-%dT%H:%M:%S'),
        'fields': 'id,start_time,duration,tracking_phone_number,customer_phone_number,qualifying,value,tags,gclid',
        'qualifying': 'true'  # Only fetch qualified leads
    }
    
    url = f'{BASE_URL}/a/{CALLRAIL_ACCOUNT_ID}/calls.json'
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        
        calls_data = response.json()
        conversions = []
        
        for call in calls_data.get('calls', []):
            # Only include calls with GCLID tracking
            if call.get('gclid'):
                conversion = {
                    'gclid': call['gclid'],
                    'conversion_date_time': format_timestamp(call['start_time']),
                    'conversion_value': call.get('value', 0),
                    'call_id': call['id'],
                    'duration': call.get('duration', 0),
                    'phone_number': call.get('customer_phone_number', '')
                }
                conversions.append(conversion)
        
        print(f"✓ Fetched {len(conversions)} conversions from CallRail")
        return conversions
        
    except requests.exceptions.RequestException as e:
        print(f"✗ Error fetching from CallRail API: {e}")
        return []


def format_timestamp(callrail_timestamp):
    """
    Convert CallRail timestamp to Google Ads format
    
    Args:
        callrail_timestamp: ISO format timestamp from CallRail
    
    Returns:
        Formatted timestamp: YYYY-MM-DD HH:MM:SS+TZ
    """
    # Handle both with and without timezone
    if callrail_timestamp.endswith('Z'):
        callrail_timestamp = callrail_timestamp.replace('Z', '+00:00')
    
    dt = datetime.fromisoformat(callrail_timestamp)
    return dt.strftime('%Y-%m-%d %H:%M:%S%z')


if __name__ == "__main__":
    # Test the integration
    print("Testing CallRail API integration...")
    print(f"API Key configured: {'Yes' if CALLRAIL_API_KEY else 'No'}")
    print(f"Account ID configured: {'Yes' if CALLRAIL_ACCOUNT_ID else 'No'}")
    print()
    
    if CALLRAIL_API_KEY and CALLRAIL_ACCOUNT_ID:
        conversions = fetch_new_conversions(since_minutes=1440)  # Last 24 hours
        
        print(f"\nFound {len(conversions)} conversions:")
        for conv in conversions[:5]:  # Show first 5
            print(f"  GCLID: {conv['gclid']}")
            print(f"  Time: {conv['conversion_date_time']}")
            print(f"  Value: ${conv['conversion_value']}")
            print(f"  Duration: {conv['duration']}s")
            print()
    else:
        print("⚠️  Please configure CALLRAIL_API_KEY and CALLRAIL_ACCOUNT_ID in your .env file")
