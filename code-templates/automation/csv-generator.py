"""Generate conversion CSV for Google Ads uploads from CRM data or sample data.

This script can:
1. Read conversion data from an existing CRM export CSV file
2. Generate sample data for testing purposes
"""

import csv
import sys
from datetime import datetime


def generate_csv_from_crm_data(input_file, output_file, column_mapping=None):
    """
    Read conversion data from CRM export and format for Google Ads upload.
    
    Args:
        input_file: Path to your CRM export CSV file
        output_file: Path where Google Ads upload CSV will be saved
        column_mapping: Dict mapping your CSV columns to required fields
                       Example: {
                           'gclid_column': 'google_click_id',
                           'date_column': 'close_date',
                           'value_column': 'sale_amount',
                           'conversion_action_id': '987654321'
                       }
    """
    # Default column mapping if none provided
    if column_mapping is None:
        column_mapping = {
            'gclid_column': 'gclid',
            'date_column': 'conversion_date',
            'value_column': 'conversion_value',
            'conversion_action_id': '987654321'  # Replace with your actual ID
        }
    
    rows = []
    skipped_count = 0
    
    try:
        # Read input CSV file
        with open(input_file, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            
            # Validate required columns exist
            if column_mapping['gclid_column'] not in reader.fieldnames:
                raise ValueError(f"Column '{column_mapping['gclid_column']}' not found in input file")
            
            # Process each row
            for row_num, row in enumerate(reader, start=2):  # Start at 2 (after header)
                gclid_value = row.get(column_mapping['gclid_column'], '').strip()
                
                # Skip rows without GCLID
                if not gclid_value:
                    skipped_count += 1
                    continue
                
                # Build output row
                output_row = {
                    "gclid": gclid_value,
                    "conversion_action_id": str(column_mapping['conversion_action_id']),
                    "conversion_date_time": row.get(column_mapping['date_column'], '').strip(),
                    "conversion_value": row.get(column_mapping['value_column'], '0').strip()
                }
                
                rows.append(output_row)
        
        # Write Google Ads format CSV
        if rows:
            with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(
                    csvfile, 
                    fieldnames=['gclid', 'conversion_action_id', 'conversion_date_time', 'conversion_value']
                )
                writer.writeheader()
                writer.writerows(rows)
            
            print(f"✓ Successfully processed {len(rows)} conversions")
            if skipped_count > 0:
                print(f"⚠ Skipped {skipped_count} rows without GCLID")
            print(f"✓ Output saved to: {output_file}")
        else:
            print("⚠ No valid conversions found in input file")
            
    except FileNotFoundError:
        print(f"✗ Error: Input file '{input_file}' not found")
        sys.exit(1)
    except ValueError as e:
        print(f"✗ Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        sys.exit(1)


def generate_sample_csv(output_path):
    """
    Generate a sample conversion CSV with fake data for testing.
    
    Args:
        output_path: Path where sample CSV will be saved
    """
    rows = [
        {
            "gclid": "CjwKCAiA1KL3BRA8EiwAzCfbQxyz123abc",
            "conversion_action_id": "987654321",
            "conversion_date_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S-08:00'),
            "conversion_value": "0",
        }
    ]

    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    
    print(f"✓ Sample CSV generated: {output_path}")


if __name__ == "__main__":
    # Example 1: Generate sample data (original functionality)
    print("\n=== Generating Sample Data ===")
    generate_sample_csv("../../data-templates/sample-conversion-upload.csv")
    
    # Example 2: Process real CRM data (uncomment and customize to use)
    # print("\n=== Processing Real CRM Data ===")
    # column_mapping = {
    #     'gclid_column': 'google_click_id',      # Your CSV column name for GCLID
    #     'date_column': 'close_date',            # Your CSV column name for conversion date
    #     'value_column': 'sale_amount',          # Your CSV column name for conversion value
    #     'conversion_action_id': '987654321'     # Your Google Ads conversion action ID
    # }
    # generate_csv_from_crm_data(
    #     input_file="../../data-templates/crm-export.csv",
    #     output_file="../../data-templates/google-ads-upload.csv",
    #     column_mapping=column_mapping
    # )
