require('dotenv').config();
const fs = require('fs');
const { parse } = require('csv-parse/sync');
const { GoogleAdsApi } = require('google-ads-api');

/**
 * Upload offline revenue conversions to Google Ads from a CSV file.
 * 
 * CSV Format Required:
 * gclid,conversion_time,revenue,currency_code
 * abc123xyz,2025-12-19 10:30:00+00:00,50.00,EUR
 * 
 * @param {string} csvPath - Path to the CSV file containing conversion data
 */
async function scheduleRevenueUpload(csvPath) {
  // Validate CSV file exists
  if (!fs.existsSync(csvPath)) {
    console.error('❌ CSV file not found:', csvPath);
    return;
  }

  console.log('📂 Reading conversions from:', csvPath);

  try {
    // Initialize Google Ads API client
    const client = new GoogleAdsApi({
      client_id: process.env.GOOGLE_ADS_CLIENT_ID,
      client_secret: process.env.GOOGLE_ADS_CLIENT_SECRET,
      developer_token: process.env.GOOGLE_ADS_DEVELOPER_TOKEN,
    });

    const customer = client.Customer({
      customer_id: process.env.GOOGLE_ADS_CUSTOMER_ID,
      refresh_token: process.env.GOOGLE_ADS_REFRESH_TOKEN,
    });

    // Parse CSV file
    const csvContent = fs.readFileSync(csvPath, 'utf-8');
    const records = parse(csvContent, {
      columns: true,
      skip_empty_lines: true,
      trim: true,
    });

    console.log(`📊 Found ${records.length} conversion(s) to upload`);

    // Map CSV rows to Google Ads conversion format
    const conversions = records.map((row, index) => {
      // Validate required fields
      if (!row.gclid || !row.conversion_time || !row.revenue) {
        throw new Error(`Row ${index + 1}: Missing required fields (gclid, conversion_time, revenue)`);
      }

      return {
        gclid: row.gclid.trim(),
        conversion_action: `customers/${process.env.GOOGLE_ADS_CUSTOMER_ID}/conversionActions/${process.env.GOOGLE_ADS_CONVERSION_ACTION_ID}`,
        conversion_date_time: row.conversion_time.trim(),
        conversion_value: parseFloat(row.revenue),
        currency_code: row.currency_code?.trim() || 'EUR',
      };
    });

    // Upload conversions to Google Ads
    console.log('⬆️  Uploading conversions to Google Ads...');
    const response = await customer.conversionUploads.uploadClickConversions({
      conversions: conversions,
      partial_failure: true, // Continue even if some conversions fail
    });

    // Handle response
    if (response.partial_failure_error) {
      console.warn('⚠️  Some conversions failed to upload:');
      console.warn(response.partial_failure_error);
    }

    console.log(`✅ Successfully uploaded ${conversions.length} conversion(s)`);
    console.log('📈 Results:', JSON.stringify(response.results, null, 2));

  } catch (error) {
    console.error('❌ Upload failed:', error.message);
    
    // Provide helpful error messages
    if (error.message.includes('authentication')) {
      console.error('\n💡 Check your OAuth credentials in .env file');
    } else if (error.message.includes('conversion_action')) {
      console.error('\n💡 Verify your GOOGLE_ADS_CONVERSION_ACTION_ID is correct');
    } else if (error.message.includes('Missing required fields')) {
      console.error('\n💡 Ensure your CSV has columns: gclid, conversion_time, revenue, currency_code');
    }
    
    throw error;
  }
}

// Run directly from command line
if (require.main === module) {
  const csvPath = process.argv[2] || '../../data-templates/sample-conversion-upload.csv';
  
  scheduleRevenueUpload(csvPath)
    .then(() => {
      console.log('\n🎉 Upload completed successfully');
      process.exit(0);
    })
    .catch((error) => {
      console.error('\n💥 Upload failed:', error.message);
      process.exit(1);
    });
}

module.exports = { scheduleRevenueUpload };
