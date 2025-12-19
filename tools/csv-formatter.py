"""Format a CSV file for Google Ads conversion uploads."""

import csv


def format_csv(input_path, output_path):
    with open(input_path, 'r') as infile, open(output_path, 'w', newline='') as outfile:
        reader = csv.DictReader(infile)
        fieldnames = ['gclid', 'conversion_action_id', 'conversion_date_time', 'conversion_value']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in reader:
            writer.writerow({key: row.get(key, '') for key in fieldnames})


if __name__ == '__main__':
    format_csv('../data-templates/sample-crm-export.csv', '../data-templates/sample-conversion-upload.csv')
