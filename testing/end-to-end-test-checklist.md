# End-to-End Testing Checklist

Complete verification that all components of the call tracking system are working correctly.

## ✅ Pre-Testing Setup

- [ ] Google Ads account has auto-tagging enabled
- [ ] Conversion actions created in Google Ads
- [ ] CallRail account configured
- [ ] DNI script installed on website
- [ ] CallRail-Google Ads integration connected
- [ ] Test budget allocated (minimum $20 for test clicks)

---

## TEST 1: GCLID Capture Verification

### Steps:
1. [ ] Clear browser cookies and cache
2. [ ] Click a Google Ad (note which campaign/keyword)
3. [ ] Land on website
4. [ ] Check URL contains `?gclid=...`
5. [ ] Open browser DevTools → Application → Cookies
6. [ ] Verify `_gcl_aw` cookie exists with GCLID value

### Expected Results:
- GCLID appears in URL immediately after clicking ad
- Cookie stores GCLID with 90-day expiration
- GCLID format: `CjwKCAiA...` (long alphanumeric string)

### Pass/Fail:
- [ ] PASS
- [ ] FAIL (document issue):

---

## TEST 2: DNI Number Swap

### Steps:
1. [ ] Click Google Ad and land on website
2. [ ] Note the phone number displayed
3. [ ] Open new incognito window
4. [ ] Visit website directly (type URL, don't click ad)
5. [ ] Compare phone numbers

### Expected Results:
- Ad click shows tracking number (from CallRail pool)
- Direct visit shows different number OR static number
- Number persists across multiple pages during same session

### Phone Numbers Observed:
- From ad click: ________________
- From direct visit: ________________

### Pass/Fail:
- [ ] PASS
- [ ] FAIL (document issue):

---

## TEST 3: Call Attribution - Scenario A (Direct from Ad)

### Steps:
1. [ ] On mobile device, search for your keyword
2. [ ] Click call extension or call-only ad
3. [ ] Complete call (talk for 60+ seconds)
4. [ ] Hang up
5. [ ] Wait 5 minutes
6. [ ] Check CallRail dashboard → Calls

### Expected Results:
- Call appears in CallRail within 5 minutes
- GCLID is populated
- Source shows "Google Ads"
- Campaign/keyword data visible
- Call duration accurate

### Actual Results:
- Call appeared: YES / NO
- GCLID captured: ________________
- Duration: ________ seconds

### Pass/Fail:
- [ ] PASS
- [ ] FAIL (document issue):

---

## TEST 4: Call Attribution - Scenario B (Website Click-to-Call)

### Steps:
1. [ ] Click Google Ad
2. [ ] Copy the GCLID from URL: ________________
3. [ ] Tap phone number on website
4. [ ] Complete call (60+ seconds)
5. [ ] Check CallRail dashboard

### Expected Results:
- Call shows same GCLID as copied from URL
- Attribution data matches ad click
- Landing page recorded correctly

### Actual Results:
- GCLID matches: YES / NO
- Expected: ________________
- Actual: ________________

### Pass/Fail:
- [ ] PASS
- [ ] FAIL (document issue):

---

## TEST 5: Call Attribution - Scenario C (Manual Dial Later)

### Steps:
1. [ ] Click Google Ad
2. [ ] Note tracking number shown: ________________
3. [ ] Note GCLID from URL: ________________
4. [ ] Close browser completely
5. [ ] Wait 10 minutes
6. [ ] Call the tracking number from different phone
7. [ ] Complete call (60+ seconds)
8. [ ] Check CallRail dashboard

### Expected Results:
- Call attributes to original GCLID even though calling from different device
- Session association preserved

### Actual Results:
- GCLID captured: ________________
- Matches original: YES / NO

### Pass/Fail:
- [ ] PASS
- [ ] FAIL (document issue):

---

## TEST 6: Call Qualification and Tagging

### Steps:
1. [ ] Make test call (any scenario)
2. [ ] Log into CallRail dashboard
3. [ ] Find the test call
4. [ ] Add tag: "Appointment_Booked"
5. [ ] Verify tag appears on call record

### Expected Results:
- Tag successfully applied
- Timestamp of tagging recorded
- Tag visible in call details

### Pass/Fail:
- [ ] PASS
- [ ] FAIL (document issue):

---

## TEST 7: Automatic Conversion Upload to Google Ads

### Steps:
1. [ ] Complete Test 6 (tagged call)
2. [ ] Wait 6-24 hours
3. [ ] Log into Google Ads
4. [ ] Navigate to: Campaigns → Campaigns
5. [ ] Check conversions column
6. [ ] Navigate to: Tools → Conversions
7. [ ] Filter by "Appointment_Booked"
8. [ ] Look for test conversion

### Expected Results:
- Conversion appears in Google Ads
- Attributed to correct campaign/keyword
- Conversion time matches call time

### Actual Results:
- Conversion visible: YES / NO
- Campaign: ________________
- Keyword: ________________
- Time delay: ________ hours

### Pass/Fail:
- [ ] PASS
- [ ] FAIL (document issue):

---

## TEST 8: Manual CSV Revenue Upload

### Steps:
1. [ ] Get GCLID from previous test call: ________________
2. [ ] Create CSV file:
```
Google Click ID,Conversion Name,Conversion Time,Conversion Value,Conversion Currency
[GCLID],Sale_Completed_Audiology,2025-12-19 15:00:00,100,USD
```
3. [ ] Upload to Google Ads → Tools → Conversions → Uploads
4. [ ] Wait 6-24 hours
5. [ ] Check Google Ads for revenue conversion

### Expected Results:
- Upload successful (no errors)
- Conversion appears with $100 value
- ROAS calculated correctly

### Actual Results:
- Upload status: SUCCESS / FAILED
- Error message (if any): ________________
- Conversion visible: YES / NO
- Value shown: $________

### Pass/Fail:
- [ ] PASS
- [ ] FAIL (document issue):

---

## TEST 9: ROAS Calculation Verification

### Steps:
1. [ ] In Google Ads, find the campaign used for testing
2. [ ] Note the cost of the test click: $________
3. [ ] Note the conversion value uploaded: $________
4. [ ] Calculate expected ROAS: (Value / Cost) × 100 = ________%
5. [ ] Check Google Ads displays correct ROAS

### Expected Results:
- Google Ads ROAS matches manual calculation
- Conversion value column shows correct amount

### Actual Results:
- Expected ROAS: ________%
- Google Ads ROAS: ________%
- Match: YES / NO

### Pass/Fail:
- [ ] PASS
- [ ] FAIL (document issue):

---

## TEST 10: Cross-Device Tracking

### Steps:
1. [ ] On Device A (desktop), click Google Ad
2. [ ] Note GCLID and tracking number
3. [ ] On Device B (mobile), call the tracking number
4. [ ] Verify CallRail attributes call to original desktop click

### Expected Results:
- Attribution maintained across devices
- GCLID links mobile call to desktop click

### Pass/Fail:
- [ ] PASS
- [ ] FAIL (document issue):

---

## FINAL VERIFICATION

### All Tests Passed?
- [ ] YES - System is fully operational
- [ ] NO - Review failed tests and troubleshoot

### Issues to Resolve:
1. ________________
2. ________________
3. ________________

### Date Testing Completed: ________________
### Tested By: ________________
### Sign-off: ________________

---

## POST-TESTING ACTIONS

- [ ] Document test results in project documentation
- [ ] Train staff on call tagging procedures
- [ ] Set up monitoring for ongoing data flow
- [ ] Schedule weekly review for first month
- [ ] Enable Smart Bidding once 30+ conversions collected
