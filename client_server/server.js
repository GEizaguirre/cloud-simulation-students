const cors = require('cors');
const express = require('express');
const http = require('http');
const WebSocket = require('ws');

const app = express();
const server = http.createServer(app);
const wss = new WebSocket.Server({ server });

app.use(cors()); // Enable CORS for all routes

const port = 3000;

app.use(express.json());

// Serve static files, including the HTML file, from the 'public' directory
app.use(express.static('public'));

// Initialize an array to store the connected WebSocket clients
const clients = [];

wss.on('connection', (ws) => {
  clients.push(ws);
  console.log(`WebSocket client connected. Total clients: ${clients.length}`);

  // Handle WebSocket client disconnection
  ws.on('close', () => {
    const index = clients.indexOf(ws);
    if (index > -1) {
      clients.splice(index, 1);
      console.log(`WebSocket client disconnected. Total clients: ${clients.length}`);
    }
  });
});

app.get('/greeting', (req, res) => {
  const userName = req.query.name || 'Anonymous';
  console.log(`Greeting request from user: ${userName}`);
  const message = `Hello, ${userName}!`;
  res.json({ message });

  // Broadcast the message to all connected clients
  clients.forEach((client) => {
    if (client.readyState === WebSocket.OPEN) {
      client.send(JSON.stringify({ message }));
    }
  });
});

app.get('/current-hour', (req, res) => {
    const userName = req.query.name || 'Anonymous';
    console.log(`Current hour request from user: ${userName}`);
    const currentHour = new Date().getHours().toString();
    res.json({ userName, hour: currentHour });
  
    // Broadcast the message to all connected clients
    clients.forEach((client) => {
      if (client.readyState === WebSocket.OPEN) {
        client.send(JSON.stringify({ userName, hour: currentHour }));
      }
    });
  });

app.get('/random-number', (req, res) => {
  const userName = req.query.name || 'Anonymous';
  console.log(`Random number request from user: ${userName}`);
  const randomNumber = Math.random();
  res.json({ userName, number: randomNumber });

  // Broadcast the message to all connected clients
  clients.forEach((client) => {
    if (client.readyState === WebSocket.OPEN) {
      client.send(JSON.stringify({ userName, number: randomNumber }));
    }
  });
});

server.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
