# Simple CallRail Setup Guide (No Code Required)

**Time Required**: 10-15 minutes  
**Difficulty**: Easy - No technical knowledge needed  
**Cost**: $45-95/month CallRail subscription

## What You'll Accomplish

By the end of this guide:
- ✅ Every call from Google Ads will be tracked
- ✅ You'll know which specific ads drive revenue
- ✅ Google Ads will automatically optimize based on your sales data
- ✅ No CRM needed, no code to write

## Before You Start

### Requirements
- ☑️ Active Google Ads account
- ☑️ Website where you can add one line of code to the footer
- ☑️ CallRail account (sign up at [callrail.com](https://www.callrail.com))
- ☑️ 15 minutes of uninterrupted time

### What You DON'T Need
- ❌ A developer or programmer
- ❌ A CRM like Salesforce or HubSpot
- ❌ Any coding knowledge
- ❌ Custom APIs or scripts

---

## Step 1: Connect CallRail to Google Ads (5 minutes)

### 1.1 Log into CallRail

1. Go to [app.callrail.com](https://app.callrail.com)
2. Click **Settings** (gear icon) in the left sidebar
3. Click **Integrations**

### 1.2 Authorize Google Ads Connection

1. Find **Google Ads** in the integrations list
2. Click **Connect** or **Authorize**
3. A Google login window will pop up
4. Select your Google account (the one with Google Ads access)
5. Click **Allow** to give CallRail permission

**What just happened?**  
You gave CallRail a digital key to send conversion data to your Google Ads account automatically. This is like connecting your Spotify to Facebook - one click, no passwords to remember.

### 1.3 Select Your Google Ads Account

1. CallRail will show a list of Google Ads accounts you have access to
2. Select the account you want to track
3. Click **Save**

### 1.4 Configure Conversion Settings

**CallRail will ask:**

**"What should we name the conversion in Google Ads?"**  
- Default: "Phone Call" (recommended)
- Or customize: "Lead Call" or "Appointment Call"

**"How should we count conversions?"**  
- Select: **Every conversion** (count every qualified call)
- Or: **One per click** (count only the first call from each person)

**"Track first-time vs. repeat callers separately?"**  
- Select: **No** (simpler) 
- Or: **Yes** (if you want to see new vs. returning customer metrics)

**"Minimum call duration to count as conversion?"**  
- Recommended: **60 seconds** (filters out wrong numbers)
- Adjust based on your business (30-120 seconds typical)

Click **Save Settings**

---

## Step 2: Add CallRail Tracking to Your Website (5 minutes)

### 2.1 Get Your Tracking Code

1. In CallRail, go to **Settings** → **Tracking Numbers**
2. Click on your main tracking number
3. Click **Get Snippet** or **JavaScript Snippet**
4. Copy the code (looks like this):

```html
<script>
  (function(){var w=window;var ic=w.Callrail||{};if(typeof ic.ready!=="undefined"){ic.ready(function(){ic.target="YOUR_NUMBER_HERE";})}else{var d=document;var c=d.createElement("script");c.type="text/javascript";c.async=true;c.src="https://cdn.callrail.com/companies/123456789/TARGET_ID.js";var s=d.getElementsByTagName("script")[0];s.parentNode.insertBefore(c,s);}})()
</script>
```

### 2.2 Add Code to Your Website Footer

**If you use WordPress:**
1. Go to **Appearance** → **Theme File Editor**
2. Find `footer.php` in the right sidebar
3. Paste the CallRail code just before `</body>`
4. Click **Update File**

**If you use Shopify:**
1. Go to **Online Store** → **Themes**
2. Click **Actions** → **Edit Code**
3. Find `theme.liquid`
4. Paste the CallRail code just before `</body>`
5. Click **Save**

**If you use another platform:**  
Google: "how to add code to [your platform] footer" or contact your web developer (5-minute task).

### 2.3 Verify It's Working

1. Visit your website in a new browser tab
2. Right-click → **Inspect** (or press F12)
3. Click **Console** tab
4. Look for "CallRail" in the messages (means it's working!)
5. Check your website - the phone number should now be a tracking number

---

## Step 3: Enable Auto-Tagging in Google Ads (2 minutes)

### 3.1 Turn On Auto-Tagging

1. Log into [ads.google.com](https://ads.google.com)
2. Click **Tools** (wrench icon) → **Settings** → **Account settings**
3. Scroll to **Auto-tagging**
4. Check the box: **Tag the URL that people click through from my ad**
5. Click **Save**

**What is auto-tagging?**  
This adds a tracking code (GCLID) to every ad click automatically. It's like putting a receipt number on every customer who walks in. CallRail reads this receipt number to know which ad brought them.

### 3.2 Verify Conversion Action Was Created

1. In Google Ads, go to **Tools** → **Measurement** → **Conversions**
2. You should see: **"Phone Call"** (or your custom name)
3. Source should say: **"Import from clicks"**
4. Status should say: **"Enabled"**

If you see this, everything is connected! ✅

---

## Step 4: Tag Your First Call (3 minutes)

### 4.1 Generate a Test Call

1. Click one of your Google Ads (from a mobile device is easiest)
2. Call the number shown on your website
3. Stay on the line for at least 60 seconds (or whatever minimum you set)
4. Hang up

### 4.2 Tag the Call in CallRail

1. Log into CallRail
2. Go to **Activity** → **Calls**
3. You should see your test call (might take 1-2 minutes to appear)
4. Click on the call
5. Click **Add Tag**
6. Type a tag name:
   - "Appointment_Booked" for scheduled appointments
   - "Sale_Completed" for closed deals
   - "Qualified_Lead" for good prospects
   - "Not_Qualified" for wrong numbers / spam
7. If it's a revenue-generating call, enter the dollar amount: `$500`
8. Click **Save**

### 4.3 Check Google Ads (3 Hours Later)

1. Wait 2-3 hours for data to sync
2. Log into Google Ads
3. Go to **Campaigns** → Select your campaign
4. Look at the **Conversions** column
5. You should see `1` conversion with value `$500`

If you see this, you're done! 🎉

---

## Daily Workflow (30 Seconds Per Call)

### Every Time You Get a Call:

1. Answer the call
2. Qualify the lead (is it a real customer?)
3. After the call, open CallRail
4. Find the call in **Activity** → **Calls**
5. Tag it:
   - **Appointment_Booked** + dollar value if they scheduled
   - **Not_Qualified** if wrong number / spam
6. Done!

CallRail automatically sends this to Google Ads within minutes.

---

## Understanding the Data Flow

```
Customer Journey:

1. Customer searches "hearing aids Los Angeles"
         ↓
2. Clicks your Google Ad
         ↓ (Google adds GCLID tracking code to URL)
         
3. Lands on your website
         ↓ (CallRail captures GCLID, shows tracking number)
         
4. Calls tracking number: (555) 123-4567
         ↓ (CallRail forwards to your real number)
         
5. You answer, book appointment for $500
         ↓
         
6. You tag call in CallRail: "Appointment - $500"
         ↓ (CallRail sends to Google Ads automatically)
         
7. Google Ads shows:
   - Campaign: Los Angeles Hearing Aids
   - Keyword: hearing aids los angeles
   - Cost: $45
   - Revenue: $500
   - ROAS: 11x (you made $11 for every $1 spent)
         ↓
         
8. Google's Smart Bidding automatically:
   - Bids MORE on profitable keywords
   - Bids LESS on unprofitable keywords
   - Optimizes your budget automatically
```

---

## What You See in CallRail

### Call Details Page Shows:

- ☑️ **Caller ID**: Who called
- ☑️ **Duration**: How long they talked
- ☑️ **Source**: Google Ads (shows campaign/keyword)
- ☑️ **GCLID**: The tracking code (long string of letters/numbers)
- ☑️ **Landing Page**: What page they visited
- ☑️ **Device**: Mobile, desktop, tablet
- ☑️ **Location**: City/state of caller
- ☑️ **Tags**: Your custom labels
- ☑️ **Value**: Revenue amount

### Reports You Can Run:

- Calls by campaign
- Calls by keyword
- Calls by time of day
- Conversion rate by source
- Revenue by campaign
- Average call duration
- First-time vs. repeat callers

---

## HIPAA Compliance (Healthcare Only)

### If You're in Healthcare:

**⚠️ You MUST disable call recording to comply with HIPAA:**

1. CallRail → **Settings** → **Call Recording**
2. Toggle: **OFF** (or set to "Disabled")
3. **Save**

CallRail will still track:
- ✅ Call duration
- ✅ Caller ID (hashed)
- ✅ Source / GCLID
- ✅ Tags
- ✅ Revenue

CallRail will NOT record:
- ❌ Actual conversation audio
- ❌ Patient medical information
- ❌ Any PHI (Protected Health Information)

**See full guide**: [HIPAA Compliance Documentation](06-hipaa-compliance.md)

---

## Troubleshooting

### Problem: Calls appear in CallRail but not Google Ads

**Check:**
1. Did you wait 2-3 hours? (Data sync delay)
2. Is auto-tagging enabled in Google Ads?
3. Did you tag the call in CallRail?
4. Does the call show "Google Ads" as the source?
5. Is call duration above minimum threshold?

### Problem: Phone number on website isn't changing

**Check:**
1. Did you paste the JavaScript snippet correctly?
2. Did you paste it just before `</body>` tag?
3. Clear your browser cache and reload
4. Check browser console for errors (F12 → Console tab)

### Problem: Conversion value is $0 in Google Ads

**Check:**
1. Did you enter a dollar amount when tagging in CallRail?
2. The value field can't be left blank
3. Re-tag the call with a value

### Problem: Google Ads shows "GCLID Not Found" error

**Check:**
1. Auto-tagging must be enabled BEFORE the ad click
2. If you just enabled it, test with a new click
3. Old clicks won't have GCLID

---

## Cost Breakdown

### CallRail Pricing (As of Dec 2025)

**Basic Plan**: $45/month
- 50 tracking numbers
- Unlimited calls
- Google Ads integration
- Basic reporting

**Pro Plan**: $95/month  
- Everything in Basic
- Call recording (disable for HIPAA)
- Form tracking
- Conversation Intelligence (AI)

**Start with Basic** - You can always upgrade later.

### Other Costs

- **Google Ads spend**: Variable (your existing budget)
- **Website hosting**: No change (you already have this)
- **CRM**: $0 (not needed!)
- **Developer**: $0 (you just did it yourself!)

**Total: $45-95/month**

---

## Next Steps

### Week 1: Monitor and Learn
- Tag every call that comes in
- Watch the data flow into Google Ads
- Identify which campaigns drive conversions

### Week 2-4: Initial Optimizations
- Pause keywords with 0 conversions
- Increase bids on profitable keywords
- Adjust ad copy based on what works

### Week 5-8: Enable Smart Bidding
- Switch to Target ROAS or Target CPA bidding
- Let Google's algorithms optimize automatically
- Watch ROAS improve 30-50%

### Week 9+: Scale What Works
- Expand successful campaigns
- Test new keywords similar to winners
- Expect 50-100%+ ROAS improvement over baseline

---

## Advanced Options (Later)

### If You Want More Automation:
- Explore this repo's [Advanced Deployment Guide](08-deployment.md)
- Set up automated conversion uploads via API
- Implement custom tagging logic

### If You Want CRM Integration:
- Connect CallRail to Salesforce, HubSpot, or Zoho
- Automate conversion tagging from deal closures
- Track longer sales cycles (weeks/months)

### If You Want Multi-Location Tracking:
- See [Dental Practice Case Study](../case-studies/dental-practice-setup.md)
- Use separate tracking numbers per location
- Compare performance across offices

---

## Support Resources

### CallRail Help:
- CallRail Support: [support.callrail.com](https://support.callrail.com)
- Live Chat: Available in CallRail dashboard
- Phone: Listed in your account settings

### Google Ads Help:
- Google Ads Support: [support.google.com/google-ads](https://support.google.com/google-ads)
- Community Forum: [support.google.com/google-ads/community](https://support.google.com/google-ads/community)

### This Repository:
- [GitHub Issues](https://github.com/stiigg/google-ads-call-tracking-implementation/issues)
- [Troubleshooting Guide](07-troubleshooting.md)
- [GitHub Discussions](https://github.com/stiigg/google-ads-call-tracking-implementation/discussions)

---

## Congratulations! 🎉

You now have a complete call tracking system that:

- ✅ Tracks every call from Google Ads
- ✅ Links calls to specific keywords and campaigns  
- ✅ Reports revenue back to Google Ads automatically
- ✅ Enables Smart Bidding optimization
- ✅ Gives you data-driven insights
- ✅ Requires zero technical maintenance

**All in 15 minutes, with no code, and no CRM needed.**

Welcome to data-driven marketing! 🚀

---

## Questions?

Open an issue or discussion in this repository, and we'll help you troubleshoot!