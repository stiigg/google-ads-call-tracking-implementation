# Customer Journey Funnel

## Overview

This document details the complete customer journey from ad click to conversion upload, covering all three call source pathways that CallRail tracks automatically.

---

## Three Call Source Pathways

### Pathway 1: Call-Only Ads / Call Extensions
**User taps phone number directly in the ad itself**

```
User searches → Google Ad displays with phone number → User taps call button
                                                                ↓
                                                    Google automatically captures GCLID
                                                                ↓
                                                    Call forwarded to your business
                                                                ↓
                                        CallRail receives call with GCLID pre-associated
                                                                ↓
                                                    Staff answers and qualifies
                                                                ↓
                                                    Tag in CallRail → Sent to Google Ads
```

**Configuration Required:**
- Google Ads Call Extensions or Call-Only Ads enabled
- CallRail configured as call forwarding destination
- Call Details Forwarding (CDF) enabled in Google Ads

**Technical Notes:**
- GCLID is passed automatically via Google's call forwarding system
- Easiest to implement - minimal website changes needed
- Works even if user never visits your website
- Immediate attribution, no DNI required

---

### Pathway 2: Click-to-Call (Mobile Website)
**User clicks Google ad, lands on website, then clicks phone number**

```
Step 1: Ad Click
┌────────────────────────────────────────────────────┐
│ User clicks Google Ad                                      │
│ URL: yoursite.com/?gclid=CjwKCAiA9ZyGBhBhEiwA...        │
└────────────────────────────────────────────────────┘
                    ↓
                    
Step 2: Page Load & GCLID Capture
┌────────────────────────────────────────────────────┐
│ CallRail JavaScript Executes:                           │
│ 1. Reads GCLID from URL                                 │
│ 2. Stores in visitor session (90-day cookie)           │
│ 3. Assigns tracking number from DNI pool               │
│    Example: (555) 123-4567                             │
│ 4. Swaps displayed phone number on page                │
└────────────────────────────────────────────────────┘
                    ↓
                    
Step 3: User Sees Dynamic Number
┌────────────────────────────────────────────────────┐
│ Website displays: 📞 (555) 123-4567                   │
│ [This is a clickable link on mobile]                   │
└────────────────────────────────────────────────────┘
                    ↓
                    
Step 4: User Taps to Call
┌────────────────────────────────────────────────────┐
│ CallRail Receives Incoming Call:                        │
│ - Tracking number: (555) 123-4567                      │
│ - Looks up: "Which visitor has this number?"           │
│ - Finds: GCLID=CjwKCAiA9ZyGBhBhEiwA...                │
│ - Forwards call to your real business number           │
└────────────────────────────────────────────────────┘
                    ↓
                    
Step 5: Qualification & Tagging
┌────────────────────────────────────────────────────┐
│ Staff answers call, qualifies lead                      │
│ Tags in CallRail:                                       │
│ - ☑️ Appointment_Booked                                │
│ - $ Value: $500                                         │
└────────────────────────────────────────────────────┘
                    ↓
                    
Step 6: Automatic Upload to Google Ads
┌────────────────────────────────────────────────────┐
│ CallRail sends to Google Ads API:                       │
│ {                                                        │
│   "gclid": "CjwKCAiA9ZyGBhBhEiwA...",                  │
│   "conversion_name": "Phone Call",                      │
│   "conversion_value": 500.00,                           │
│   "conversion_time": "2025-12-19T15:15:00"              │
│ }                                                        │
└────────────────────────────────────────────────────┘
                    ↓
                    
Step 7: Attribution in Google Ads
┌────────────────────────────────────────────────────┐
│ Google Ads matches GCLID to original click:             │
│ Campaign: LA Audiology                                  │
│ Keyword: "audiologist near me"                         │
│ Cost: $45.00                                            │
│ Revenue: $500.00                                        │
│ ROAS: 11.1x                                             │
└────────────────────────────────────────────────────┘
```

**Configuration Required:**
- CallRail JavaScript snippet in website footer
- DNI number pool configured (minimum 5-10 numbers)
- Auto-tagging enabled in Google Ads
- Tracking numbers formatted as clickable links (`<a href="tel:+15551234567">`)

**Technical Notes:**
- GCLID captured via URL parameter parsing
- Session stored in first-party cookie (90-day expiration)
- Works for mobile click-to-call scenarios
- Requires sufficient DNI pool for concurrent visitors

---

### Pathway 3: Manual Dial (User Reads DNI Number)
**User visits website, writes down number, calls later**

```
Step 1-2: Same as Pathway 2
(Ad click → Website load → GCLID captured → DNI number assigned)

                    ↓
                    
Step 3: User Sees Number But Doesn't Call Yet
┌────────────────────────────────────────────────────┐
│ User writes down: (555) 123-4567                        │
│ Closes browser, goes about their day                   │
│                                                          │
│ CallRail session persists for 90 days:                 │
│ - Visitor ID: vis_12345                                 │
│ - GCLID: CjwKCAiA9ZyGBhBhEiwA...                       │
│ - Assigned number: (555) 123-4567                      │
└────────────────────────────────────────────────────┘
                    ↓
           [Time passes: 2 hours later...]
                    ↓
                    
Step 4: User Manually Dials
┌────────────────────────────────────────────────────┐
│ User dials (555) 123-4567 from their phone keypad      │
│                                                          │
│ CallRail receives call:                                 │
│ - Incoming on: (555) 123-4567                          │
│ - Looks up session database                            │
│ - Finds: Visitor vis_12345                             │
│ - Retrieves: GCLID CjwKCAiA9ZyGBhBhEiwA...            │
│ - Associates call with original ad click               │
└────────────────────────────────────────────────────┘
                    ↓
                    
Step 5-7: Same as Pathway 2
(Qualification → Tagging → Upload → Attribution)
```

**Configuration Required:**
- Same as Pathway 2
- Sufficient DNI pool size to avoid number recycling
- 90-day session persistence configured

**Technical Notes:**
- Most challenging to track (no digital click event)
- Relies on DNI number persistence
- Session must not expire before call
- Number can't be reassigned to different visitor
- Tracks calls that happen hours/days after website visit

---

## Complete Funnel Stages (All Pathways)

### Stage 1: Ad Click
- **What happens**: User clicks Google Ad
- **Data captured**: GCLID automatically appended to URL
- **Duration**: < 1 second
- **Success criteria**: Auto-tagging enabled in Google Ads

### Stage 2: Website Engagement  
- **What happens**: User lands on website, CallRail script executes
- **Data captured**: GCLID, visitor session, landing page, referrer, device
- **Duration**: 1-3 seconds
- **Success criteria**: JavaScript loads successfully, DNI number assigned

### Stage 3: Call Initiation
- **What happens**: User calls tracking number (immediate or delayed)
- **Data captured**: Caller ID, tracking number dialed, timestamp
- **Duration**: Varies (immediate to days later)
- **Success criteria**: Call duration > minimum threshold (typically 60s)

### Stage 4: Call Qualification
- **What happens**: Staff answers, qualifies lead, tags outcome
- **Data captured**: Call quality, tags, revenue value, notes
- **Duration**: 30 seconds per call (manual tagging)
- **Success criteria**: Proper tag applied, value entered if applicable

### Stage 5: Offline Conversion Upload
- **What happens**: CallRail sends conversion to Google Ads API
- **Data captured**: GCLID, conversion name, value, timestamp
- **Duration**: 5-10 seconds (automatic)
- **Success criteria**: Google Ads matches GCLID, conversion accepted

### Stage 6: Attribution & Optimization
- **What happens**: Google Ads attributes conversion, updates algorithms
- **Data captured**: Campaign, keyword, ad, device, location metrics
- **Duration**: 2-3 hours for reporting, ongoing for optimization
- **Success criteria**: Conversion visible in reports, Smart Bidding adjusts

---

## Technical Requirements by Pathway

| Requirement | Pathway 1 | Pathway 2 | Pathway 3 |
|------------|-----------|-----------|----------|
| CallRail JavaScript | Optional | ✅ Required | ✅ Required |
| DNI Configuration | Optional | ✅ Required | ✅ Required |
| Auto-tagging | ✅ Required | ✅ Required | ✅ Required |
| Call Forwarding | ✅ Required | ✅ Required | ✅ Required |
| Google Ads CDF | ✅ Required | Optional | Optional |
| Session Persistence | N/A | 90 days | 90 days |
| Number Pool Size | N/A | 5-10+ | 10-20+ |

---

## Conversion Window

All three pathways respect Google Ads conversion window settings:

- **Default**: 90 days from original click
- **Configurable**: 1-90 days (set in Google Ads)
- **CallRail alignment**: Automatically matches Google Ads setting

**Important**: Calls occurring >90 days after ad click will be rejected with `EXPIRED_GCLID` error.

---

## Data Flow Timing

### Real-Time Flow (CallRail Direct Integration)

```
Time 0:00 - Customer calls
Time 0:30 - Staff tags call in CallRail
Time 0:35 - CallRail sends to Google Ads API (5 seconds)
Time 3:00 - Conversion appears in Google Ads reports (3 hour delay)
Next Day - Smart Bidding begins optimization
```

### Batch Upload Flow (Using This Repo's Scripts)

```
Time 0:00 - Customer calls  
Time 0:30 - Staff tags call
Time 6:00 - Cron job runs (every 6 hours)
Time 6:02 - Script uploads to Google Ads (2 minutes)
Time 9:00 - Conversion visible in reports (3 hour delay)
Next Day - Smart Bidding optimization
```

---

## Success Metrics

### Tracking Health Indicators

- **GCLID Capture Rate**: >95% of ad clicks should have valid GCLID
- **DNI Assignment Rate**: 100% of website visitors should see tracking number
- **Call Attribution Rate**: >90% of calls should match to source
- **Upload Success Rate**: >98% of tagged calls should reach Google Ads
- **Reporting Latency**: <6 hours from call to conversion visibility

### Troubleshooting Thresholds

- **GCLID capture <85%**: Check auto-tagging settings
- **DNI not showing**: Verify JavaScript snippet placement
- **Calls not attributed**: Check DNI pool size, session persistence
- **Upload failures >5%**: Review API credentials, conversion action status
- **Reporting delays >12 hours**: Contact CallRail or Google Ads support

---

## Related Documentation

- [Simple CallRail Setup](09-callrail-simple-setup.md) - Step-by-step implementation
- [Technical Architecture](02-technical-architecture.md) - System design details
- [Troubleshooting](07-troubleshooting.md) - Common issues and solutions
- [Testing Procedures](05-testing-procedures.md) - Verify each pathway works