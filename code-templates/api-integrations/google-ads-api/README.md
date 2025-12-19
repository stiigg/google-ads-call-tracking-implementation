# Google Ads API Integration - Node.js

Complete implementation for uploading offline conversions to Google Ads using the Google Ads API with Node.js.

## Features

- ✅ Upload single or batch conversions with GCLID
- ✅ Revenue tracking with conversion values
- ✅ Comprehensive error handling with detailed logging
- ✅ Partial failure support (continues processing on errors)
- ✅ Environment variable configuration
- ✅ CSV batch processing with streaming
- ✅ Production-ready with proper authentication

## Prerequisites

1. **Node.js** v14+ installed
2. **Google Ads account** with API access
3. **Google Cloud Project** with Google Ads API enabled
4. **OAuth2 credentials** (Client ID, Client Secret, Refresh Token)
5. **Developer Token** from Google Ads Manager account

## Installation

```bash
cd code-templates/api-integrations/google-ads-api
npm install
```

This will install:
- `google-ads-api` - Official Google Ads API client for Node.js
- `csv-parser` - CSV file processing

## Authentication Setup

### Step 1: Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable **Google Ads API**:
   - Navigate to "APIs & Services" → "Library"
   - Search for "Google Ads API"
   - Click "Enable"

### Step 2: Create OAuth2 Credentials

1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "OAuth client ID"
3. Choose "Desktop app" as application type
4. Download the JSON credentials file
5. Note your **Client ID** and **Client Secret**

### Step 3: Generate Refresh Token

**Option A: Using OAuth2 Playground**

1. Go to [OAuth2 Playground](https://developers.google.com/oauthplayground/)
2. Click settings icon (⚙️) → Check "Use your own OAuth credentials"
3. Enter your Client ID and Client Secret
4. In Step 1, add scope: `https://www.googleapis.com/auth/adwords`
5. Click "Authorize APIs" and sign in with your Google account
6. In Step 2, click "Exchange authorization code for tokens"
7. Copy the **Refresh Token**

**Option B: Programmatically (see Google Ads API docs)**

### Step 4: Get Developer Token

1. Sign in to your [Google Ads Manager account](https://ads.google.com/)
2. Click "Tools & Settings" → "API Center"
3. Apply for a Developer Token
4. Wait for approval (usually 1-5 business days)
5. Copy your **Developer Token** once approved

### Step 5: Set Environment Variables

Create a `.env` file or export environment variables:

```bash
export GOOGLE_ADS_CLIENT_ID="your_client_id.apps.googleusercontent.com"
export GOOGLE_ADS_CLIENT_SECRET="your_client_secret"
export GOOGLE_ADS_DEVELOPER_TOKEN="your_developer_token"
export GOOGLE_ADS_REFRESH_TOKEN="1//0your_refresh_token"
export GOOGLE_ADS_CUSTOMER_ID="1234567890"  # Without hyphens
export CONVERSION_ACTION_ID="987654321"     # Your conversion action ID
```

**For production, use a proper secrets management solution.**

## Usage

### CSV Format

Create a CSV file with the following columns:

```csv
gclid,conversion_action_id,conversion_date_time,conversion_value,currency_code
ABC123XYZ,987654321,2025-12-19 10:30:00-08:00,0,USD
DEF456UVW,987654321,2025-12-19 14:00:00-08:00,4500,USD
GHI789RST,987654322,2025-12-19 16:45:00-08:00,1200,USD
```

**Required columns:**
- `gclid` - Google Click Identifier
- `conversion_date_time` - Timestamp in format `YYYY-MM-DD HH:MM:SS+TZ`

**Optional columns:**
- `conversion_action_id` - Overrides default conversion action
- `conversion_value` - Revenue amount (omit or set to 0 for non-revenue conversions)
- `currency_code` - Currency (defaults to USD)

### Run the Script

```bash
# Upload from default CSV location
node upload-conversions.js

# Upload from custom CSV file
node upload-conversions.js /path/to/conversions.csv
```

### Example Output

```
Google Ads Offline Conversion Upload
=====================================

Customer ID: 1234567890
CSV File: conversions.csv

Processing 3 conversions...

✓ Successfully uploaded conversion:
  GCLID: ABC123XYZ
  Conversion Time: 2025-12-19 10:30:00-08:00

✓ Successfully uploaded conversion:
  GCLID: DEF456UVW
  Conversion Time: 2025-12-19 14:00:00-08:00
  Value: $4500

✗ Failed to upload conversion:
  GCLID: INVALID_GCLID
  Error: Invalid GCLID format

=== Upload Summary ===
Total rows: 3
Successful: 2
Failed: 1

Upload process completed.
```

## Programmatic Usage

You can also import and use the functions in your own code:

```javascript
const { uploadClickConversion, uploadConversionsFromCsv } = require('./upload-conversions');

// Upload single conversion
await uploadClickConversion({
  gclid: 'ABC123XYZ',
  conversion_date_time: '2025-12-19 10:30:00-08:00',
  conversion_value: '4500',
  currency_code: 'USD'
});

// Batch upload from CSV
await uploadConversionsFromCsv('./conversions.csv');
```

## Troubleshooting

### Common Errors

**"Missing required environment variables"**
- Ensure all 4 credential environment variables are set
- Check variable names match exactly

**"Invalid GCLID"**
- Verify GCLID format (should start with letters, contain alphanumeric characters)
- Ensure GCLID is from a recent click (typically within 90 days)

**"Authentication failed"**
- Verify your refresh token is still valid
- Regenerate refresh token if needed
- Check Client ID and Secret are correct

**"Developer token not approved"**
- Wait for Google to approve your token application
- Use test account for development

**"Conversion action not found"**
- Verify conversion action ID exists in your Google Ads account
- Check customer ID is correct (without hyphens)

### Debug Mode

For detailed API request/response logging, set:

```bash
export NODE_ENV=development
```

## Differences from Python Version

Both implementations provide the same functionality:

| Feature | Python | Node.js |
|---------|--------|---------|
| Google Ads API | ✅ v23.0.0 | ✅ v21.0.1 |
| CSV Processing | ✅ Built-in | ✅ csv-parser |
| Error Handling | ✅ | ✅ |
| Batch Upload | ✅ | ✅ |
| Authentication | YAML config | Environment variables |
| Async Processing | Sync | Async/await |

## Resources

- [Google Ads API Documentation](https://developers.google.com/google-ads/api/docs/start)
- [google-ads-api npm package](https://www.npmjs.com/package/google-ads-api)
- [OAuth2 Setup Guide](https://developers.google.com/google-ads/api/docs/oauth/overview)
- [Conversion Upload Guide](https://developers.google.com/google-ads/api/docs/conversions/upload-offline)

## Support

For issues or questions:
1. Check the [main repository documentation](../../../README.md)
2. Review [troubleshooting guide](../../../docs/07-troubleshooting.md)
3. Open an [issue](https://github.com/stiigg/google-ads-call-tracking-implementation/issues)

## License

MIT License - See main repository LICENSE file
