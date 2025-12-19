# Implementation Guide

## 1. Google Ads Setup

- Enable auto-tagging.
- Create conversion actions for calls and revenue.
- Configure call extensions.

## 2. Call Tracking Platform Setup

- Create call tracking numbers and DNI pools.
- Connect Google Ads integration.
- Configure qualification rules.

## 3. Website Installation

- Add DNI script (see `code-templates/website/`).
- Verify GCLID capture and storage.

## 4. Conversion Uploads

- Use API scripts in `code-templates/api-integrations/google-ads-api/`.
- Schedule batch uploads for revenue conversions.

## 5. Validate

- Run tests in `testing/`.
- Confirm conversions in Google Ads.
