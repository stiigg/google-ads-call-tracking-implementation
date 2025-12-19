"""
GCLID Validator - Verify GCLID format and validity
"""

import re
from datetime import datetime, timedelta


def is_valid_gclid_format(gclid):
    """
    Check if GCLID matches expected format

    Valid GCLID format:
    - Starts with 'Cj' or 'EAIa'
    - Contains only alphanumeric characters, hyphens, and underscores
    - Typically 50-100 characters long
    """
    if not gclid:
        return False, "GCLID is empty"

    if len(gclid) < 20:
        return False, f"GCLID too short ({len(gclid)} chars), expected 20+"

    if len(gclid) > 200:
        return False, f"GCLID too long ({len(gclid)} chars), expected <200"

    pattern = r'^[A-Za-z0-9_-]+$'
    if not re.match(pattern, gclid):
        return False, "GCLID contains invalid characters"

    return True, "Valid GCLID format"


def check_gclid_age(click_timestamp, current_timestamp=None):
    """
    Check if GCLID is within the 90-day conversion window
    """
    if current_timestamp is None:
        current_timestamp = datetime.now()

    age = current_timestamp - click_timestamp
    max_age = timedelta(days=90)

    if age > max_age:
        return False, f"GCLID is {age.days} days old (max: 90 days)"

    return True, f"GCLID is {age.days} days old (within window)"


def validate_gclid_batch(gclids):
    """
    Validate a list of GCLIDs and return results
    """
    results = []

    for gclid in gclids:
        is_valid, message = is_valid_gclid_format(gclid)
        results.append({
            'gclid': gclid,
            'valid': is_valid,
            'message': message
        })

    return results


if __name__ == "__main__":
    # Example usage
    test_gclids = [
        "CjwKCAiA1KL3BRA8EiwAzCfbQxyz123abc",  # Valid
        "EAIaIQobChMI...",  # Valid
        "abc123",  # Invalid - too short
        "Cj@#$%^&*()",  # Invalid - special characters
    ]

    for gclid in test_gclids:
        is_valid, message = is_valid_gclid_format(gclid)
        print(f"GCLID: {gclid[:30]}...")
        print(f"  Status: {'✓ VALID' if is_valid else '✗ INVALID'}")
        print(f"  Message: {message}\n")
