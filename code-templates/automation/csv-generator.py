"""Generate a sample conversion CSV for Google Ads uploads."""

import csv
from datetime import datetime


def generate_csv(output_path):
    rows = [
        {
            "gclid": "CjwKCAiA1KL3BRA8EiwAzCfbQxyz123abc",
            "conversion_action_id": "987654321",
            "conversion_date_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S-08:00'),
            "conversion_value": "0",
        }
    ]

    with open(output_path, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    generate_csv("../../data-templates/sample-conversion-upload.csv")
