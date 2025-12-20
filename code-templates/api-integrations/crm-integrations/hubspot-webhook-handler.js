/**
 * ⚠️ OPTIONAL INTEGRATION - NOT REQUIRED FOR BASIC SETUP
 * 
 * This code is only needed if:
 * 1. You already use HubSpot CRM for sales pipeline management
 * 2. You have sales cycles longer than 14 days
 * 3. You need multi-touch attribution across many channels
 * 
 * CallRail handles offline conversion tracking standalone without this.
 * See: docs/09-callrail-simple-setup.md for the recommended basic setup.
 * 
 * Most businesses should NOT use this file.
 * Read code-templates/api-integrations/crm-integrations/README.md first.
 */

const express = require('express');

const app = express();
app.use(express.json());

app.post('/hubspot/webhook', (req, res) => {
  console.log('HubSpot webhook payload', req.body);
  res.status(200).send('OK');
});

app.listen(4000, () => {
  console.log('HubSpot webhook handler running on port 4000');
});
