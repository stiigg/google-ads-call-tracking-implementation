const http = require('http');

const server = http.createServer((req, res) => {
  if (req.method !== 'POST') {
    res.writeHead(405);
    res.end('Method Not Allowed');
    return;
  }

  let body = '';
  req.on('data', (chunk) => {
    body += chunk.toString();
  });

  req.on('end', () => {
    console.log('Received CallRail webhook:', body);
    res.writeHead(200);
    res.end('OK');
  });
});

server.listen(3000, () => {
  console.log('Webhook handler listening on port 3000');
});
