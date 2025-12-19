# Technical Architecture

## Core Systems

1. **Google Ads**: Generates GCLIDs and receives offline conversion uploads.
2. **Website**: Captures GCLID and triggers DNI number swaps.
3. **Call Tracking Platform**: Attributes calls to ads and records call outcomes.
4. **CRM/Booking System**: Stores qualified leads and revenue details.
5. **Integration Layer**: Uploads conversions via API or CSV.

## Data Flow Summary

- User clicks ad → GCLID appears in landing URL.
- GCLID is stored and passed to call tracking provider.
- Calls are qualified and tagged.
- Qualified calls are uploaded to Google Ads.
