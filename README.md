# Google Ads Call Tracking & Offline Conversion Implementation

Complete implementation guide for tracking phone calls from Google Ads through to revenue, enabling accurate ROAS measurement for businesses where conversions happen offline.

## 🎯 What This Solves

- **The Problem**: You spend money on Google Ads, people call you, but you can't tell which ads actually generate revenue
- **The Solution**: Track every call back to the specific ad, keyword, and campaign that generated it, then connect those calls to actual sales revenue

## 🏥 Perfect For

- Healthcare providers (audiology clinics, dental practices, medical specialists)
- Professional services (legal, financial, consulting)
- Home services (HVAC, plumbing, roofing)
- Any business where phone calls are the primary conversion

## 📊 Key Features

- ✅ GCLID-based attribution linking ads to calls
- ✅ Dynamic Number Insertion (DNI) for website visitors
- ✅ Three call source tracking: ad extensions, website clicks, manual dials
- ✅ **🆕 Automated conversion upload to Google Ads via cron jobs**
- ✅ **🆕 CallRail API integration for real-time data sync**
- ✅ **🆕 Smart state management to avoid duplicate uploads**
- ✅ Revenue tracking and ROAS calculation
- ✅ HIPAA-compliant configuration for healthcare
- ✅ Complete testing procedures
- ✅ **🆕 Production-ready deployment with logging and monitoring**

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Google Ads account with API access
- CallRail account (or other call tracking platform)
- Linux/Unix server for automation

### Installation

```bash
# Clone the repository
git clone https://github.com/stiigg/google-ads-call-tracking-implementation.git
cd google-ads-call-tracking-implementation

# Install dependencies
pip3 install -r code-templates/api-integrations/google-ads-api/requirements.txt

# Configure credentials
cp .env.example .env
nano .env  # Add your API keys and IDs

# Make script executable
chmod +x code-templates/automation/scheduled-batch-upload.sh

# Test the setup
python3 code-templates/api-integrations/callrail/fetch-conversions.py
```

### Deploy Automation

```bash
# Open crontab
crontab -e

# Add this line (update path):
0 */6 * * * cd /path/to/repo && ./code-templates/automation/scheduled-batch-upload.sh >> /var/log/google-ads-uploads.log 2>&1
```

**See: [Deployment Guide](docs/08-deployment.md) for complete setup instructions**

## 📚 Documentation

- [Project Overview](docs/01-project-overview.md) - Understand what this system does
- [Technical Architecture](docs/02-technical-architecture.md) - How all the pieces fit together
- [Customer Journey Funnel](docs/03-customer-journey-funnel.md) - Step-by-step user flow
- [Implementation Guide](docs/04-implementation-guide.md) - Detailed setup instructions
- [Testing Procedures](docs/05-testing-procedures.md) - Verify everything works
- [HIPAA Compliance](docs/06-hipaa-compliance.md) - Healthcare-specific requirements
- [Troubleshooting](docs/07-troubleshooting.md) - Common issues and solutions
- **🆕 [Deployment Guide](docs/08-deployment.md) - Production setup and automation**

## 🛠️ Technology Stack

- **Call Tracking**: CallRail (primary), CallTrackingMetrics, Ringba
- **Google Ads API**: v24+ for conversion uploads
- **Automation**: Bash scripts + Python + Cron
- **State Management**: File-based sync tracking
- **Logging**: Daily log files with rotation
- **Website**: HTML/JavaScript for DNI implementation
- **Optional**: Google Tag Manager, CRM integration

## 💻 Code Structure

```
code-templates/
├── api-integrations/
│   ├── google-ads-api/
│   │   ├── upload-conversions.py      # Main upload logic
│   │   └── requirements.txt           # Python dependencies
│   └── callrail/
│       └── fetch-conversions.py       # CallRail API integration
└── automation/
    ├── scheduled-batch-upload.sh  # Cron job wrapper
    └── utils/
        ├── logging_config.py      # Centralized logging
        └── state_manager.py       # Duplicate prevention

deployment/
└── crontab.example               # Scheduling examples
```

## 🔄 How It Works

1. **User clicks Google Ad** → GCLID attached to URL
2. **User calls tracking number** → GCLID captured by CallRail
3. **Call qualifies as lead** → Marked in CallRail with value
4. **Cron job runs (every 6 hours)** → Fetches new conversions
5. **Script uploads to Google Ads** → Links GCLID to conversion
6. **Google attributes conversion** → Campaign optimization happens automatically

## 📊 Expected Results

**Typical Implementation Outcomes:**
- Week 1-2: System fully operational, initial data flowing
- Week 3-4: 10-20% improvement in ROAS through initial optimizations
- Week 5-8: 30-50% improvement as Smart Bidding learns
- Week 9+: 50-100%+ improvement over baseline with mature optimization

## 🏆 Case Studies

- [Audiology Clinic Implementation](case-studies/audiology-clinic-implementation.md) - $4,500 avg sale, 375:1 ROAS
- [Dental Practice Setup](case-studies/dental-practice-setup.md) - Multi-location tracking
- [Results Analysis](case-studies/results-analysis.md) - Before/after metrics

## 🔧 Tools & Utilities

- [GCLID Validator](tools/gclid-validator.py) - Verify GCLID format
- [CSV Formatter](tools/csv-formatter.py) - Format data for Google Ads upload
- [ROAS Analyzer](tools/roas-analyzer.py) - Calculate and visualize return on ad spend

## 🔒 Security & Best Practices

- Environment variables for sensitive credentials
- `.gitignore` excludes all credential files
- File permissions restrict access to config files
- Daily log rotation with automatic cleanup
- State tracking prevents duplicate uploads
- Error logging and monitoring capabilities

## 🤝 Contributing

Contributions welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📝 License

MIT License - see [LICENSE](LICENSE) file

## 👤 Author

**Christian Baghai**
- GitHub: [@stiigg](https://github.com/stiigg)
- Specialization: Clinical statistical programming → Digital analytics (GA4/GTM)
- Location: Paris, France

## 🚀 Recent Updates

### Version 2.0 (December 2025)
- ✅ Added CallRail API integration
- ✅ Implemented smart state management
- ✅ Added comprehensive logging system
- ✅ Created production deployment guide
- ✅ Fixed path resolution in automation scripts
- ✅ Added environment variable configuration
- ✅ Included cron job examples and monitoring

## 🙏 Acknowledgments

- Google Ads API documentation
- CallRail developer resources
- Healthcare compliance best practices

## 📞 Support

- Open an [Issue](https://github.com/stiigg/google-ads-call-tracking-implementation/issues)
- Read the [Deployment Guide](docs/08-deployment.md)
- Check [Troubleshooting](docs/07-troubleshooting.md)
- Start a [Discussion](https://github.com/stiigg/google-ads-call-tracking-implementation/discussions)

---

**Ready to track every dollar spent on Google Ads?** 💰

Start with the [Deployment Guide](docs/08-deployment.md) →
