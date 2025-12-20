# CRM Integrations (OPTIONAL)

⚠️ **These integrations are NOT required for basic call tracking setup.**

## When You DON'T Need This

CallRail handles offline conversion tracking **completely standalone**:
- ✅ GCLID capture and storage
- ✅ Call tagging and conversion classification  
- ✅ Automatic upload to Google Ads API
- ✅ Revenue attribution

**Skip this directory if you're doing:**
- Healthcare appointments (audiology, dental, medical)
- Professional services consultations (legal, financial)
- Home services quotes (HVAC, plumbing, roofing)
- Any business with short sales cycles (< 7 days)

## When You MIGHT Need This

Use CRM integrations only if you need:
- 📊 Sales pipeline management across weeks/months
- 🔄 Multi-touch attribution across 5+ channels
- 👥 Team collaboration on complex deals
- 📈 Advanced lead scoring and nurturing

## Available Templates

### HubSpot Webhook Handler
Receives webhooks from HubSpot when deals close, then uploads conversions to Google Ads.

**Use case:** B2B SaaS with 30+ day sales cycles

### Salesforce GCLID Capture
Apex code to store GCLID values on Lead/Contact records in Salesforce.

**Use case:** Enterprise sales teams already using Salesforce

### Zapier Workflow
No-code automation connecting CallRail → CRM → Google Ads.

**Use case:** Non-technical users who need CRM sync

## Before Using These

Ask yourself:
1. Does CallRail's built-in conversion tagging solve my problem? (Usually yes)
2. Do I have a sales cycle longer than 14 days? (If no, skip CRM)
3. Do I already use a CRM for other purposes? (If no, don't add complexity)

**Most businesses should ignore this directory entirely.**

## Decision Tree

```
START: Do you already use a CRM (HubSpot/Salesforce/etc)?
  ├─ NO → ✅ USE CALLRAIL STANDALONE (Recommended)
  │        └─ Skip this directory entirely
  │
  └─ YES → Is your sales cycle longer than 14 days?
           ├─ NO → ✅ USE CALLRAIL STANDALONE
           │        └─ CRM adds unnecessary complexity
           │
           └─ YES → Do you need multi-touch attribution?
                    ├─ NO → ✅ USE CALLRAIL STANDALONE
                    │        └─ Tag conversions in CallRail only
                    │
                    └─ YES → ⚠️ Consider CRM integration
                             └─ Read the specific template docs below
```

## Getting Started Without CRM

If you're reading this and thinking "I'm not sure if I need CRM integration," you probably don't.

**Instead, follow the simple setup:**
1. Read [docs/09-callrail-simple-setup.md](../../../docs/09-callrail-simple-setup.md)
2. Set up CallRail direct integration (10 minutes)
3. Start tracking conversions immediately

**You can always add CRM integration later if your business requirements change.**

---

## Template Documentation

### 1. HubSpot Webhook Handler (`hubspot-webhook-handler.js`)

**What it does:** Receives webhooks from HubSpot when a deal is marked as "Closed Won," extracts the GCLID and revenue data, then uploads the conversion to Google Ads.

**Requirements:**
- Node.js server to run the webhook endpoint
- HubSpot Professional or Enterprise plan (webhooks feature)
- Custom GCLID field configured in HubSpot
- Google Ads API credentials

**Setup complexity:** High (requires server hosting and webhook configuration)

**When to use:** B2B businesses with complex sales cycles where deals are managed entirely in HubSpot and CallRail is not used for conversion tagging.

### 2. Salesforce GCLID Capture (`salesforce-gclid-capture.apex`)

**What it does:** Stores the GCLID value on Lead or Contact records in Salesforce, enabling later conversion uploads when deals close.

**Requirements:**
- Salesforce org (any edition)
- Custom field `GCLID__c` created on Lead object
- Apex deployment permissions
- Web-to-Lead form or custom integration to capture GCLID

**Setup complexity:** Medium (requires Salesforce admin access and custom field creation)

**When to use:** Enterprise sales teams already using Salesforce for pipeline management who need to track offline conversions from initial ad click through to closed deals.

### 3. Zapier Workflow (`zapier-workflow.json`)

**What it does:** No-code automation that connects CallRail (or web forms) to Google Sheets or other CRM systems, capturing GCLID and conversion data.

**Requirements:**
- Zapier account (Starter plan minimum)
- CallRail account with webhook support
- Destination CRM or Google Sheets

**Setup complexity:** Low (point-and-click configuration)

**When to use:** Non-technical users who need to sync call data to multiple systems but don't want to write code.

**Note:** This is the easiest option if you absolutely must have CRM sync, but CallRail's native Google Ads integration is still simpler and more reliable.

---

## Maintenance & Support

These templates are provided as starting points and may require customization for your specific business needs. They are not actively maintained as part of the core repository.

**For help with:**
- **CallRail setup** → See [docs/09-callrail-simple-setup.md](../../../docs/09-callrail-simple-setup.md)
- **Google Ads integration** → See [docs/04-implementation-guide.md](../../../docs/04-implementation-guide.md)
- **CRM-specific questions** → Consult your CRM provider's documentation

**Remember:** The vast majority of businesses tracking offline conversions do NOT need CRM integration. Start simple with CallRail standalone.
