"""
Google Ads Offline Conversion Upload Script
Uses GCLID to upload call conversions and revenue to Google Ads
Now with CallRail integration and environment variable configuration
"""

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
import csv
import os
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add parent directories to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))

try:
    from automation.utils.logging_config import setup_logging
    from automation.utils.state_manager import get_minutes_since_last_sync, save_last_sync_time
    from callrail.fetch_conversions import fetch_new_conversions
    IMPORTS_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Some imports not available: {e}")
    IMPORTS_AVAILABLE = False

# Configuration from environment variables
CUSTOMER_ID = os.getenv('GOOGLE_ADS_CUSTOMER_ID')
CONVERSION_ACTION_ID = os.getenv('GOOGLE_ADS_CONVERSION_ACTION_ID')
GOOGLE_ADS_YAML_PATH = os.getenv('GOOGLE_ADS_YAML_PATH', 'google-ads.yaml')

# Validate required variables
if not CUSTOMER_ID or not CONVERSION_ACTION_ID:
    print("⚠️  ERROR: Missing required environment variables")
    print("Please set GOOGLE_ADS_CUSTOMER_ID and GOOGLE_ADS_CONVERSION_ACTION_ID in your .env file")
    print("Example:")
    print("  GOOGLE_ADS_CUSTOMER_ID=1234567890")
    print("  GOOGLE_ADS_CONVERSION_ACTION_ID=987654321")
    sys.exit(1)


def upload_click_conversion(client, customer_id, conversion_action_id, gclid, conversion_date_time, conversion_value=None, logger=None):
    """
    Upload a single click conversion to Google Ads

    Args:
        client: GoogleAdsClient instance
        customer_id: Google Ads customer ID
        conversion_action_id: ID of the conversion action
        gclid: Google Click Identifier
        conversion_date_time: Conversion timestamp (YYYY-MM-DD HH:MM:SS+TZ)
        conversion_value: Optional conversion value (for revenue tracking)
        logger: Optional logger instance
    
    Returns:
        True if successful, False otherwise
    """
    conversion_upload_service = client.get_service("ConversionUploadService")

    # Create the conversion
    click_conversion = client.get_type("ClickConversion")
    click_conversion.gclid = gclid
    click_conversion.conversion_action = client.get_service("GoogleAdsService").conversion_action_path(
        customer_id, conversion_action_id
    )
    click_conversion.conversion_date_time = conversion_date_time

    if conversion_value:
        click_conversion.conversion_value = float(conversion_value)

    try:
        # Upload the conversion
        request = client.get_type("UploadClickConversionsRequest")
        request.customer_id = customer_id
        request.conversions.append(click_conversion)
        request.partial_failure = True  # Continue even if some conversions fail

        response = conversion_upload_service.upload_click_conversions(
            request=request
        )

        # Check for partial failures
        if response.partial_failure_error:
            msg = f"Partial failure occurred: {response.partial_failure_error}"
            if logger:
                logger.warning(msg)
            else:
                print(msg)

        # Print results
        success_msg = [
            "✓ Successfully uploaded conversion:",
            f"  GCLID: {gclid}",
            f"  Conversion Time: {conversion_date_time}"
        ]
        if conversion_value:
            success_msg.append(f"  Value: ${conversion_value}")
        
        msg = "\n".join(success_msg)
        if logger:
            logger.info(msg)
        else:
            print(msg)

        return True

    except GoogleAdsException as ex:
        error_msg = [
            "✗ Failed to upload conversion:",
            f"  GCLID: {gclid}",
            f"  Error: {ex}"
        ]
        
        for error in ex.failure.errors:
            error_msg.append(f"  Error code: {error.error_code}")
            error_msg.append(f"  Message: {error.message}")
        
        msg = "\n".join(error_msg)
        if logger:
            logger.error(msg)
        else:
            print(msg)

        return False


def upload_conversions_from_csv(csv_file_path, logger=None):
    """
    Bulk upload conversions from a CSV file

    CSV Format:
    gclid,conversion_action_id,conversion_date_time,conversion_value
    ABC123XYZ,987654321,2025-12-19 10:30:00-08:00,0
    DEF456UVW,987654322,2025-12-19 14:00:00-08:00,4500
    """
    if logger:
        logger.info(f"Uploading conversions from CSV: {csv_file_path}")
    else:
        print(f"Uploading conversions from CSV: {csv_file_path}")
    
    # Initialize Google Ads client
    client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML_PATH)

    successful = 0
    failed = 0

    with open(csv_file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            gclid = row['gclid']
            conv_action_id = row.get('conversion_action_id', CONVERSION_ACTION_ID)
            conv_date_time = row['conversion_date_time']
            conv_value = row.get('conversion_value', None)

            success = upload_click_conversion(
                client,
                CUSTOMER_ID,
                conv_action_id,
                gclid,
                conv_date_time,
                conv_value,
                logger
            )

            if success:
                successful += 1
            else:
                failed += 1

    summary = [
        "",
        "=== Upload Summary ===",
        f"Total rows: {successful + failed}",
        f"Successful: {successful}",
        f"Failed: {failed}"
    ]
    msg = "\n".join(summary)
    if logger:
        logger.info(msg)
    else:
        print(msg)
    
    return successful, failed


def upload_conversions_from_callrail(since_minutes=None, logger=None):
    """
    Fetch conversions from CallRail and upload to Google Ads
    
    Args:
        since_minutes: Fetch conversions from last N minutes (None = auto-detect from last sync)
        logger: Optional logger instance
    
    Returns:
        Tuple of (successful_count, failed_count)
    """
    if not IMPORTS_AVAILABLE:
        msg = "⚠️  Cannot use CallRail integration - missing required modules"
        if logger:
            logger.error(msg)
        else:
            print(msg)
        return 0, 0
    
    # Determine time window
    if since_minutes is None:
        since_minutes = get_minutes_since_last_sync(default_minutes=360)
    
    if logger:
        logger.info(f"=== Starting Conversion Upload ===")
        logger.info(f"Fetching conversions from last {since_minutes} minutes...")
    else:
        print("=== Starting Conversion Upload ===")
        print(f"Fetching conversions from last {since_minutes} minutes...")
    
    # Fetch from CallRail
    conversions = fetch_new_conversions(since_minutes)
    
    if not conversions:
        msg = "No conversions to upload"
        if logger:
            logger.info(msg)
        else:
            print(msg)
        return 0, 0
    
    # Initialize Google Ads client
    client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML_PATH)
    
    successful = 0
    failed = 0
    
    for conv in conversions:
        success = upload_click_conversion(
            client,
            CUSTOMER_ID,
            CONVERSION_ACTION_ID,
            conv['gclid'],
            conv['conversion_date_time'],
            conv['conversion_value'],
            logger
        )
        
        if success:
            successful += 1
        else:
            failed += 1
    
    summary = [
        "",
        "=== Upload Summary ===",
        f"Total conversions: {len(conversions)}",
        f"Successful: {successful}",
        f"Failed: {failed}"
    ]
    msg = "\n".join(summary)
    if logger:
        logger.info(msg)
    else:
        print(msg)
    
    # Save sync timestamp if any uploads succeeded
    if successful > 0:
        save_last_sync_time()
    
    return successful, failed


if __name__ == "__main__":
    # Setup logging if available
    logger = None
    if IMPORTS_AVAILABLE:
        logger = setup_logging()
    
    # Choose upload method based on available integrations
    if IMPORTS_AVAILABLE:
        # Primary: Upload from CallRail with automatic time tracking
        logger.info("Using CallRail integration for conversion upload")
        upload_conversions_from_callrail(logger=logger)
    else:
        # Fallback: Upload from CSV file for testing
        print("\nFalling back to CSV upload (CallRail integration not available)")
        csv_path = "../../data-templates/sample-conversion-upload.csv"
        if os.path.exists(csv_path):
            upload_conversions_from_csv(csv_path)
        else:
            print(f"Error: CSV file not found: {csv_path}")
    
    # Example: Upload single conversion (commented out)
    # client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML_PATH)
    # upload_click_conversion(
    #     client,
    #     CUSTOMER_ID,
    #     CONVERSION_ACTION_ID,
    #     gclid="CjwKCAiA1KL3BRA8EiwAzCfbQxyz123abc",
    #     conversion_date_time="2025-12-19 10:30:00-08:00",
    #     conversion_value=4500.00,
    #     logger=logger
    # )
