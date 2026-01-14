# CLIENT-SERVER & CLOUD SIMULATION FOR UNDERGRADUATES

You need to have nodejs (checked with v20.5.1) and npm (checked with v9.8.0) installed.

## Installation

### Ubuntu

(Only for server side)
```bash
sudo apt update
sudo apt upgrade
sudo apt install -y curl
sudo apt-get install -y lsb-release
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs
npm install socket.io express multer cors ws
```

Storage service
```bash
mkdir uploads
```

To solve overwrite problems:

```bash
sudo dpkg --remove --force-remove-reinstreq libnode-dev
sudo dpkg --remove --force-remove-reinstreq libnode72:amd64
```

## Execution - client service mode ([client_server](client_server/) directory)

### Server

```bash
node server.js
```

then, get the server's local IP

**Linux:**
```bash
ip a
```

**macOS:**
```bash
ifconfig | grep "inet "
```

open the server interface at:

```
localhost:3001/server.html
```

then, ask the students to connect to the Client browsing:

```
http://<SERVER_IP>:3001/
```

### Client

In client.html, subsitute "localhost" by the server private ip. It can be running the following command in the server 
```
ip a
```
Open the [client1.html](client_server/client1.html) in a browser.

## Execution - storage mode ([storage_service](storage_service/) directory)

Do the same, but with the files in the [storage_service](storage_service/) directory. Use the port 3000 instead.
