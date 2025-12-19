"""
Google Ads Offline Conversion Upload Script
Uses GCLID to upload call conversions and revenue to Google Ads
"""

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
import csv

# Configuration
GOOGLE_ADS_YAML_PATH = 'google-ads.yaml'  # Path to your credentials file
CUSTOMER_ID = '1234567890'  # Your Google Ads customer ID (without hyphens)
CONVERSION_ACTION_ID = '987654321'  # Your conversion action ID

def upload_click_conversion(client, customer_id, conversion_action_id, gclid, conversion_date_time, conversion_value=None):
    """
    Upload a single click conversion to Google Ads

    Args:
        client: GoogleAdsClient instance
        customer_id: Google Ads customer ID
        conversion_action_id: ID of the conversion action
        gclid: Google Click Identifier
        conversion_date_time: Conversion timestamp (YYYY-MM-DD HH:MM:SS+TZ)
        conversion_value: Optional conversion value (for revenue tracking)
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
            print(f"Partial failure occurred: {response.partial_failure_error}")

        # Print results
        for result in response.results:
            print("✓ Successfully uploaded conversion:")
            print(f"  GCLID: {gclid}")
            print(f"  Conversion Time: {conversion_date_time}")
            if conversion_value:
                print(f"  Value: ${conversion_value}")

        return True

    except GoogleAdsException as ex:
        print("✗ Failed to upload conversion:")
        print(f"  GCLID: {gclid}")
        print(f"  Error: {ex}")

        for error in ex.failure.errors:
            print(f"  Error code: {error.error_code}")
            print(f"  Message: {error.message}")

        return False


def upload_conversions_from_csv(csv_file_path):
    """
    Bulk upload conversions from a CSV file

    CSV Format:
    gclid,conversion_action_id,conversion_date_time,conversion_value
    ABC123XYZ,987654321,2025-12-19 10:30:00-08:00,0
    DEF456UVW,987654322,2025-12-19 14:00:00-08:00,4500
    """
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
                conv_value
            )

            if success:
                successful += 1
            else:
                failed += 1

    print("\n=== Upload Summary ===")
    print(f"Total rows: {successful + failed}")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")


if __name__ == "__main__":
    # Example: Upload from CSV file
    csv_path = "../../data-templates/sample-conversion-upload.csv"
    upload_conversions_from_csv(csv_path)

    # Example: Upload single conversion
    # client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML_PATH)
    # upload_click_conversion(
    #     client,
    #     CUSTOMER_ID,
    #     CONVERSION_ACTION_ID,
    #     gclid="CjwKCAiA1KL3BRA8EiwAzCfbQxyz123abc",
    #     conversion_date_time="2025-12-19 10:30:00-08:00",
    #     conversion_value=4500.00
    # )
