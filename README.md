# CLIENT-SERVER & CLOUD SIMULATION FOR UNDERGRADUATES

You need to have nodejs (checked with v20.5.1) and npm (checked with v9.8.0) installed.

## Installation

### Ubuntu

(Only for server side)
```bash
sudo apt update
sudo apt upgrade
sudo apt install -y curl
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs
mkdir uploads
npm install socket.io express multer cors
```

To solve overwrite problems:

```bash
sudo dpkg --remove --force-remove-reinstreq libnode-dev
sudo dpkg --remove --force-remove-reinstreq libnode72:amd64
```
## Configuration

Configurate the maximum storage of your simulated server and the server ip at [config.json](config.json).

```

```

## Execution

### Server

```bash
node server.js
```
then just connect to the server UI opening a browser and browsing

```
http://localhost:3000/
```

### Client

Open the [client.html](client.html) in a browser.

