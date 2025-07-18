# Docker Setup for Traffic Camera Project

## Overview
This Docker setup uses FileBrowser to provide a web-based file management interface for the traffic camera project.

## Getting Started

### Prerequisites
- Docker and Docker Compose installed on your Raspberry Pi
- Port 8080 available

### Installation
1. Install Docker on Raspberry Pi:
   ```bash
   curl -fsSL https://get.docker.com -o get-docker.sh
   sudo sh get-docker.sh
   sudo usermod -aG docker $USER
   # Log out and back in for group changes to take effect
   ```

2. Install Docker Compose:
   ```bash
   sudo apt-get install docker-compose
   ```

### Running the Container
1. Start the FileBrowser service:
   ```bash
   docker-compose up -d
   ```

2. Access FileBrowser at: http://<raspberry-pi-ip>:8080
   - Default username: admin
   - Default password: admin

### Directory Structure
- `/photos` - Camera captures will be stored here
- `/config` - Application configuration files
- `/src` - Source code directory

### Stopping the Service
```bash
docker-compose down
```

### Camera Support (Future)
The docker-compose.yml includes commented-out sections for camera device mapping. Once camera support is ready, uncomment the `devices` and `privileged` sections.

### Security Note
Remember to change the default username and password in production!