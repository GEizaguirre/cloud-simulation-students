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
then just connect to the server UI opening a browser and browsing

```
http://localhost:3001/
```

### Client

In client.html, subsitute "localhost" by the server private ip. It can be running the following command in the server 
```
ip a
```
Open the [client1.html](client_server/client1.html) in a browser.

## Execution - storage mode ([storage_service](storage_service/) directory)

### Server

```bash
node server.js
```
then just connect to the server UI opening a browser and browsing

```
http://localhost:3000/
```

### Client

In client.html, subsitute "localhost" by the server private ip. It can be running the following command in the server 
```
ip a
```
Open the [client2.html](storage_service/client2.html) in a browser.
