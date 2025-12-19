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
