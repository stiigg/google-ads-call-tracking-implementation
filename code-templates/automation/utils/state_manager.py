"""
State Manager: Track last successful sync to avoid duplicate uploads
"""

import os
from datetime import datetime

STATE_FILE = os.path.join(os.path.dirname(__file__), '../../../.last_sync')


def get_last_sync_time():
    """
    Get timestamp of last successful sync
    
    Returns:
        datetime object or None if never synced
    """
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, 'r') as f:
                timestamp_str = f.read().strip()
                return datetime.fromisoformat(timestamp_str)
        except (ValueError, IOError) as e:
            print(f"Warning: Could not read last sync time: {e}")
            return None
    return None


def save_last_sync_time():
    """
    Save current timestamp as last successful sync
    """
    try:
        with open(STATE_FILE, 'w') as f:
            f.write(datetime.utcnow().isoformat())
        print(f"✓ Saved last sync timestamp")
    except IOError as e:
        print(f"Warning: Could not save last sync time: {e}")


def get_minutes_since_last_sync(default_minutes=360):
    """
    Calculate minutes since last sync
    
    Args:
        default_minutes: Default value if never synced (default 6 hours)
    
    Returns:
        Number of minutes since last sync
    """
    last_sync = get_last_sync_time()
    if last_sync:
        delta = datetime.utcnow() - last_sync
        minutes = int(delta.total_seconds() / 60)
        print(f"Last sync was {minutes} minutes ago")
        return minutes
    else:
        print(f"No previous sync found, using default: {default_minutes} minutes")
        return default_minutes


if __name__ == "__main__":
    # Test the state manager
    print("Testing state manager...")
    
    minutes = get_minutes_since_last_sync()
    print(f"Minutes since last sync: {minutes}")
    
    print("\nSaving current time...")
    save_last_sync_time()
    
    print("\nChecking again...")
    minutes = get_minutes_since_last_sync()
    print(f"Minutes since last sync: {minutes}")
