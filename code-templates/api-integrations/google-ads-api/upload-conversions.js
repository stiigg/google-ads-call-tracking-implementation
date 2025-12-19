/**
 * Google Ads Offline Conversion Upload Script (Node.js)
 * Uses GCLID to upload call conversions and revenue to Google Ads
 */

const { GoogleAdsApi } = require('google-ads-api');
const fs = require('fs');
const csv = require('csv-parser');

// Configuration - Update these values or use environment variables
const CUSTOMER_ID = process.env.GOOGLE_ADS_CUSTOMER_ID || '1234567890'; // Without hyphens
const CONVERSION_ACTION_ID = process.env.CONVERSION_ACTION_ID || '987654321';

// Initialize Google Ads API client
const client = new GoogleAdsApi({
  client_id: process.env.GOOGLE_ADS_CLIENT_ID,
  client_secret: process.env.GOOGLE_ADS_CLIENT_SECRET,
  developer_token: process.env.GOOGLE_ADS_DEVELOPER_TOKEN,
});

/**
 * Upload a single click conversion to Google Ads
 * 
 * @param {Object} row - Conversion data from CSV
 * @param {string} row.gclid - Google Click Identifier
 * @param {string} row.conversion_date_time - Conversion timestamp (YYYY-MM-DD HH:MM:SS+TZ)
 * @param {string} [row.conversion_value] - Optional conversion value for revenue tracking
 * @param {string} [row.conversion_action_id] - Optional conversion action ID
 * @param {string} [row.currency_code] - Optional currency code (default: USD)
 * @returns {Promise<boolean>} Success status
 */
async function uploadClickConversion(row) {
  try {
    // Initialize customer
    const customer = client.Customer({
      customer_id: CUSTOMER_ID,
      refresh_token: process.env.GOOGLE_ADS_REFRESH_TOKEN,
    });

    // Build conversion action resource name
    const conversionActionId = row.conversion_action_id || CONVERSION_ACTION_ID;
    const conversionActionResourceName = `customers/${CUSTOMER_ID}/conversionActions/${conversionActionId}`;

    // Create the conversion object
    const clickConversion = {
      gclid: row.gclid,
      conversion_action: conversionActionResourceName,
      conversion_date_time: row.conversion_date_time,
    };

    // Add optional conversion value if provided
    if (row.conversion_value) {
      clickConversion.conversion_value = parseFloat(row.conversion_value);
      clickConversion.currency_code = row.currency_code || 'USD';
    }

    // Upload the conversion
    const response = await customer.conversionUploads.uploadClickConversions({
      conversions: [clickConversion],
      partial_failure: true, // Continue even if some conversions fail
    });

    console.log('✓ Successfully uploaded conversion:');
    console.log(`  GCLID: ${row.gclid}`);
    console.log(`  Conversion Time: ${row.conversion_date_time}`);
    if (row.conversion_value) {
      console.log(`  Value: $${row.conversion_value}`);
    }

    return true;
  } catch (error) {
    console.error('✗ Failed to upload conversion:');
    console.error(`  GCLID: ${row.gclid}`);
    console.error(`  Error: ${error.message}`);
    
    // Log detailed error information if available
    if (error.errors) {
      error.errors.forEach((err) => {
        console.error(`  Error code: ${err.error_code}`);
        console.error(`  Message: ${err.message}`);
      });
    }

    return false;
  }
}

/**
 * Bulk upload conversions from a CSV file
 * 
 * CSV Format:
 * gclid,conversion_action_id,conversion_date_time,conversion_value,currency_code
 * ABC123XYZ,987654321,2025-12-19 10:30:00-08:00,0,USD
 * DEF456UVW,987654322,2025-12-19 14:00:00-08:00,4500,USD
 * 
 * @param {string} csvPath - Path to CSV file
 * @returns {Promise<void>}
 */
async function uploadConversionsFromCsv(csvPath) {
  let successful = 0;
  let failed = 0;
  const conversions = [];

  return new Promise((resolve, reject) => {
    fs.createReadStream(csvPath)
      .pipe(csv())
      .on('data', (row) => {
        conversions.push(row);
      })
      .on('end', async () => {
        console.log(`\nProcessing ${conversions.length} conversions...\n`);

        // Process conversions sequentially
        for (const row of conversions) {
          const success = await uploadClickConversion(row);
          if (success) {
            successful++;
          } else {
            failed++;
          }
          console.log(''); // Empty line between conversions
        }

        console.log('=== Upload Summary ===');
        console.log(`Total rows: ${successful + failed}`);
        console.log(`Successful: ${successful}`);
        console.log(`Failed: ${failed}`);

        resolve();
      })
      .on('error', (error) => {
        console.error('Error reading CSV file:', error.message);
        reject(error);
      });
  });
}

// Main execution
if (require.main === module) {
  // Check if required environment variables are set
  const requiredEnvVars = [
    'GOOGLE_ADS_CLIENT_ID',
    'GOOGLE_ADS_CLIENT_SECRET',
    'GOOGLE_ADS_DEVELOPER_TOKEN',
    'GOOGLE_ADS_REFRESH_TOKEN',
  ];

  const missingVars = requiredEnvVars.filter((varName) => !process.env[varName]);

  if (missingVars.length > 0) {
    console.error('Error: Missing required environment variables:');
    missingVars.forEach((varName) => console.error(`  - ${varName}`));
    console.error('\nPlease set these variables before running the script.');
    console.error('See README.md for setup instructions.');
    process.exit(1);
  }

  // Example: Upload from CSV file
  const csvPath = process.argv[2] || '../../data-templates/sample-conversion-upload.csv';
  
  console.log('Google Ads Offline Conversion Upload');
  console.log('=====================================\n');
  console.log(`Customer ID: ${CUSTOMER_ID}`);
  console.log(`CSV File: ${csvPath}\n`);

  uploadConversionsFromCsv(csvPath)
    .then(() => {
      console.log('\nUpload process completed.');
      process.exit(0);
    })
    .catch((error) => {
      console.error('\nFatal error:', error.message);
      process.exit(1);
    });
}

module.exports = {
  uploadClickConversion,
  uploadConversionsFromCsv,
};
