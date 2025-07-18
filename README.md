# Traffic Camera System

Modern traffic camera system for Raspberry Pi 3B+ with IMX477 camera using Bookworm OS.

## 🎯 **Current Status: Phases 1-2 Complete**

✅ **Phase 1**: Basic camera functionality with picamera2  
✅ **Phase 2**: Docker FileBrowser web interface  
🚧 **Phase 3**: Codebase cleanup (in progress)

## 📁 **Project Components**

### Core Scripts:
- **setup_camera.sh** - Automated setup for Bookworm/picamera2
- **test_camera.py** - Comprehensive camera testing
- **camera_capture.py** - Production photo capture 
- **camera_diagnostics.py** - System health checks
- **docker-compose.yml** - FileBrowser web interface

### Directories:
- **photos/** - Captured images storage
- **data/** - FileBrowser data
- **venv/** - Python virtual environment (created by setup)

## 🚀 **Quick Start**

### 1. Setup System
```bash
git clone https://github.com/csantosscott/TrafficCamera.git
cd TrafficCamera
./setup_camera.sh
```

### 2. Test Camera
```bash
# Test with virtual environment
source venv/bin/activate
python3 test_camera.py

# Or test without venv (system python)
python3 test_camera.py
```

### 3. Start Web Interface
```bash
docker-compose up -d
```
Access FileBrowser at: `http://<pi-ip>:8080` (admin/admin)

### 4. Capture Photos
```bash
# Single photo capture
python3 camera_capture.py

# View photos in web browser at http://<pi-ip>:8080
```

## 🔧 **System Requirements**

- Raspberry Pi 3B+ with Bookworm OS
- IMX477 camera connected to CSI port  
- Camera interface enabled in raspi-config
- Docker installed
- 128MB+ GPU memory (handled by setup script)

## 🔍 **Troubleshooting**

### Run Diagnostics
```bash
python3 camera_diagnostics.py
```
This checks libcamera, picamera2, GPU memory, Docker status, and project setup.

### Common Issues

**Camera not detected:**
- Enable camera: `sudo raspi-config` → Interface Options → Camera
- Check ribbon cable connection to CSI port
- Reboot after enabling camera
- Test with: `libcamera-hello`

**FileBrowser not accessible:**
- Start container: `docker-compose up -d`
- Check container: `docker ps`
- Find Pi IP: `hostname -I`
- Access: `http://<pi-ip>:8080`

**Import errors in venv:**
- picamera2 needs system packages: use `python3` directly or recreate venv with `--system-site-packages`

### For Help:
- Check logs: `docker logs traffic_camera_filebrowser`
- Run diagnostics: `python3 camera_diagnostics.py`  
- Test camera: `python3 test_camera.py`

## 📋 **Development Status**

See `projectplan.md` for detailed development phases and progress tracking.