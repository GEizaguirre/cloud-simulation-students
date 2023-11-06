const express = require('express');
const http = require('http');
const socketIo = require('socket.io');
const multer = require('multer');
const path = require('path');
const cors = require('cors');
const fs = require('fs');
const app = express();
const server = http.createServer(app);
const io = socketIo(server);
const port = 3000;
const upload = multer({ dest: 'uploads/' });

const configFile = 'config.json';
const configData = JSON.parse(fs.readFileSync(configFile));
const totalSpaceMB = configData.totalSpaceMB;

const receivedFiles = [];

let usedSpaceMB = 0;

app.use(cors()); // Enable CORS for all routes

app.use(express.static(path.join(__dirname, 'public')));


app.post('/upload', upload.array('file'), (req, res) => {
  const uploadedFiles = req.files;
  const clientName = req.body.clientName


  if (uploadedFiles) {
    const fileData = uploadedFiles.map((file) => {
        
        const sizeMB = (file.size / 1024 / 1024).toFixed(2);
        usedSpaceMB += parseFloat(sizeMB);
        let usedPercentage = (usedSpaceMB / totalSpaceMB) * 100;
        usedPercentage = usedPercentage.toFixed(2);

        return {
        client: clientName,
        title: file.originalname,
        sizeMB: sizeMB, // Calculate file size in MB,
        space: usedPercentage
        }
    });
    console.log('Received files:', fileData);

    receivedFiles.push(...fileData); // Add file data to the receivedFiles array
    io.sockets.emit('updateFiles', receivedFiles); // Send the whole array to all connected clients
    res.json({ message: 'Files uploaded successfully', fileData });
  } else {
    res.status(400).json({ message: 'No files received' });
  }
});

io.on('connection', (socket) => {
  console.log('A client connected.');
  socket.emit('updateFiles', receivedFiles); // Send the existing file data to the connected client

  socket.on('disconnect', () => {
    console.log('A client disconnected.');
  });
});

server.listen(port, () => {
  console.log(`Server is listening on port ${port}`);
});
