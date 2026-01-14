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

Exemplifies a simple client-server architecture.

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

Simulates an scalable object storage system.

Do the same, but with the files in the [storage_service](storage_service/) directory. Use the port 3000 instead.

## Execution - AI inference

We need a Hugging Face account for this. We will set up a Hugging Face Space that serves a simple Sentiment Analysis API. It includes:

- Student View (/): A simple interface to send text.

- Teacher View (/admin): A real-time dashboard showing all student requests.

### Create the Space
1. Log in to [Hugging Face](https://huggingface.co/).
2. Click New Space.
3. Name: class-ai-server (or whatever).
4. License: MIT.
5. SDK: Select Docker > Blank.
6. Click Create Space.

### Add the Files

You need to copy [Dockerfile](Dockerfile), [app.py](app.py) and [requirements.txt](requirements.txt) into the Space.

### Run & Usage

Wait for the Space to build (Green "Running" badge).

Student URL: https://huggingface.co/spaces/YOUR_USERNAME/SPACE_NAME

Share this link with students.

### IMPORTANT: How to open the Teacher/Admin Page

The standard Hugging Face URL (huggingface.co/spaces/...) is a wrapper (iframe). If you try to add /admin to it, you will get a 404 Error. You must use the Direct Link.

How to get the Direct Link:

1. Go to your main Space page.
2. Click the three dot in the upper right corner.
3. Select "Embed This Space".
4. Copy the link there. It will look like: https://username-spacename.hf.space.

Add /admin to the end of that URL.
