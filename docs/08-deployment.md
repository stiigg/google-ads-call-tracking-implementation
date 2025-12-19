# Deployment Guide

Complete guide for deploying the Google Ads conversion tracking automation to production.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Testing](#testing)
5. [Cron Job Setup](#cron-job-setup)
6. [Monitoring](#monitoring)
7. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### System Requirements
- Linux/Unix server (Ubuntu, CentOS, macOS)
- Python 3.8 or higher
- pip package manager
- Cron (for scheduling)
- Write access to log directory

### Account Requirements
- Google Ads account with API access
- CallRail account with API enabled
- Access to create cron jobs on server

---

## Installation

### 1. Clone the Repository

```bash
# Clone to your server
git clone https://github.com/stiigg/google-ads-call-tracking-implementation.git
cd google-ads-call-tracking-implementation
```

### 2. Install Python Dependencies

```bash
# Install required packages
pip3 install -r code-templates/api-integrations/google-ads-api/requirements.txt
```

### 3. Make Scripts Executable

```bash
# Make the bash script executable
chmod +x code-templates/automation/scheduled-batch-upload.sh
```

---

## Configuration

### 1. Set Up Environment Variables

```bash
# Copy example file
cp .env.example .env

# Edit with your credentials
nano .env
```

**Required variables:**
```bash
# Google Ads Configuration
GOOGLE_ADS_CUSTOMER_ID=1234567890          # Your 10-digit customer ID (no dashes)
GOOGLE_ADS_CONVERSION_ACTION_ID=987654321  # Your conversion action ID

# CallRail Configuration
CALLRAIL_API_KEY=your-api-key-here         # From CallRail Settings > API Keys
CALLRAIL_ACCOUNT_ID=ACC1234567             # From CallRail URL
```

### 2. Configure Google Ads API Authentication

Create `google-ads.yaml` in the repository root:

```yaml
developer_token: YOUR_DEVELOPER_TOKEN
client_id: YOUR_CLIENT_ID.apps.googleusercontent.com
client_secret: YOUR_CLIENT_SECRET
refresh_token: YOUR_REFRESH_TOKEN
use_proto_plus: True
```

**See:** [Google Ads API Setup Guide](https://developers.google.com/google-ads/api/docs/first-call/overview)

### 3. Verify Configuration

```bash
# Test CallRail connection
python3 code-templates/api-integrations/callrail/fetch-conversions.py

# Test Google Ads upload (dry run with sample data)
python3 code-templates/api-integrations/google-ads-api/upload-conversions.py
```

---

## Testing

### Manual Test Run

```bash
# Navigate to repository root
cd /path/to/google-ads-call-tracking-implementation

# Run the script manually
./code-templates/automation/scheduled-batch-upload.sh
```

**Expected output:**
```
Fetching conversions from last 360 minutes...
✓ Fetched 5 conversions from CallRail
✓ Successfully uploaded conversion:
  GCLID: ABC123XYZ
  Conversion Time: 2025-12-19 10:30:00+0000
  Value: $150

=== Upload Summary ===
Total conversions: 5
Successful: 5
Failed: 0
✓ Saved last sync timestamp
```

### Check Logs

```bash
# View today's log file
tail -f logs/conversions_$(date +%Y%m%d).log
```

---

## Cron Job Setup

### 1. Choose Your Schedule

See `deployment/crontab.example` for options:
- **Every 6 hours** (recommended): `0 */6 * * *`
- **Every 4 hours**: `0 */4 * * *`
- **Business hours only**: `0 9-17/2 * * 1-5`

### 2. Install Cron Job

```bash
# Open crontab editor
crontab -e
```

**Add this line (update the path):**
```bash
# Google Ads Conversion Upload - Every 6 hours
0 */6 * * * cd /path/to/google-ads-call-tracking-implementation && ./code-templates/automation/scheduled-batch-upload.sh >> /var/log/google-ads-uploads.log 2>&1
```

### 3. Verify Cron Installation

```bash
# List installed cron jobs
crontab -l

# Check if cron service is running
sudo systemctl status cron
```

### 4. Monitor First Execution

```bash
# Watch the log file (wait for next scheduled time)
tail -f /var/log/google-ads-uploads.log
```

---

## Monitoring

### Daily Checks

**1. Check upload success rate:**
```bash
grep "Upload Summary" /var/log/google-ads-uploads.log | tail -5
```

**2. Check for errors:**
```bash
grep -i "error\|failed" /var/log/google-ads-uploads.log | tail -10
```

**3. Verify last sync time:**
```bash
cat .last_sync
```

### Set Up Email Alerts (Optional)

Add to crontab:
```bash
# Daily error report at 9am
0 9 * * * grep -i "error\|failed" /var/log/google-ads-uploads.log | mail -s "Google Ads Upload Errors" your-email@example.com
```

### Log Rotation

Add to crontab:
```bash
# Weekly cleanup - keep last 30 days
0 3 * * 0 find /path/to/google-ads-call-tracking-implementation/logs -name "*.log" -mtime +30 -delete
```

---

## Troubleshooting

### Common Issues

**1. "ModuleNotFoundError: No module named 'dotenv'"**
```bash
# Install missing dependency
pip3 install python-dotenv
```

**2. "Missing required environment variables"**
```bash
# Check .env file exists and has correct variables
cat .env | grep GOOGLE_ADS_CUSTOMER_ID
```

**3. "Permission denied" when running script**
```bash
# Make script executable
chmod +x code-templates/automation/scheduled-batch-upload.sh
```

**4. Cron job not running**
```bash
# Check cron service status
sudo systemctl status cron

# View cron logs
sudo grep CRON /var/log/syslog | tail -20
```

**5. No conversions found**
- Check CallRail has qualified calls with GCLID
- Verify time range: default is 6 hours
- Test CallRail API manually:
  ```bash
  python3 code-templates/api-integrations/callrail/fetch-conversions.py
  ```

### Debug Mode

Run with verbose output:
```bash
# Set debug environment variable
export PYTHONUNBUFFERED=1
./code-templates/automation/scheduled-batch-upload.sh
```

### Get Support

- Check logs: `logs/conversions_YYYYMMDD.log`
- Review error messages in `/var/log/google-ads-uploads.log`
- Open issue: [GitHub Issues](https://github.com/stiigg/google-ads-call-tracking-implementation/issues)

---

## Security Best Practices

1. **Protect credentials:**
   ```bash
   chmod 600 .env
   chmod 600 google-ads.yaml
   ```

2. **Never commit credentials:**
   - `.env` and `google-ads.yaml` are in `.gitignore`
   - Verify before pushing: `git status`

3. **Restrict file permissions:**
   ```bash
   chmod 700 code-templates/automation/scheduled-batch-upload.sh
   ```

4. **Use service account** (recommended for production):
   - Create dedicated service account for cron
   - Limit permissions to only what's needed

---

## Next Steps

- ✅ Verify cron job runs successfully
- ✅ Monitor conversions in Google Ads after 24-48 hours
- ✅ Set up email alerts for errors
- ✅ Document any custom modifications
- ✅ Schedule regular log reviews

**Related Documentation:**
- [Testing Procedures](05-testing-procedures.md)
- [Troubleshooting Guide](07-troubleshooting.md)
- [Project Overview](01-project-overview.md)
