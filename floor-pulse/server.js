const http = require('http');
const fs = require('fs');
const path = require('path');
const { WebSocketServer } = require('ws');

const PORT = process.env.PORT || 3000;
const PUBLIC = path.join(__dirname, 'public');

const MIME = {
  '.html': 'text/html',
  '.js':   'application/javascript',
  '.json': 'application/json',
  '.css':  'text/css',
};

const server = http.createServer((req, res) => {
  const filePath = req.url === '/' ? '/index.html' : req.url.split('?')[0];
  const abs = path.resolve(PUBLIC, '.' + filePath);

  if (!abs.startsWith(PUBLIC)) {
    res.writeHead(403);
    return res.end('Forbidden');
  }

  fs.readFile(abs, (err, data) => {
    if (err) { res.writeHead(404); return res.end('Not found'); }
    res.writeHead(200, { 'Content-Type': MIME[path.extname(abs)] || 'text/plain' });
    res.end(data);
  });
});

const wss = new WebSocketServer({ server });
const clients = new Set();

wss.on('connection', (ws) => {
  clients.add(ws);
  console.log(`+ client connected (${clients.size} total)`);

  ws.on('message', (data) => {
    // Broadcast to ALL clients including sender so your own tap shows locally
    const msg = data.toString();
    clients.forEach(client => {
      if (client.readyState === 1) client.send(msg);
    });
  });

  ws.on('close', () => {
    clients.delete(ws);
    console.log(`- client disconnected (${clients.size} total)`);
  });

  ws.on('error', () => clients.delete(ws));
});

server.listen(PORT, () => {
  console.log(`\nFloor Pulse — http://localhost:${PORT}`);
  console.log(`Open multiple tabs: ?tech=alpha  ?tech=bravo  ?tech=charlie\n`);
});
