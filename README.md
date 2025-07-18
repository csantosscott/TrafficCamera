# Traffic Camera System

Modern traffic camera system for Raspberry Pi 3B+ with IMX477 camera using Bookworm OS.

## 🎯 **Current Status: Phases 1-3 Complete**

✅ **Phase 1**: Basic camera functionality with picamera2  
✅ **Phase 2**: Docker FileBrowser web interface  
✅ **Phase 3**: Codebase cleanup and modernization  
🚀 **Ready for**: Enhanced features and license plate detection

## 📁 **Project Architecture**

### Core Scripts:
- **setup_camera.sh** - Automated setup for Bookworm/picamera2
- **test_camera.py** - Comprehensive camera testing with diagnostics
- **camera_capture.py** - Production single photo capture 
- **camera_diagnostics.py** - Complete system health checks
- **docker-compose.yml** - FileBrowser web interface configuration

### Technology Stack:
- **Hardware**: Raspberry Pi 3B+ + IMX477 Camera
- **OS**: Raspberry Pi OS Bookworm (libcamera native)
- **Camera API**: picamera2 (modern Bookworm-compatible library)
- **Backend**: Python 3.11+ with system-wide picamera2
- **Frontend**: FileBrowser Docker container
- **Storage**: Local filesystem (photos/ directory)
- **Interface**: Web browser access on port 8080

### Directory Structure:
```
TrafficCamera/
├── photos/              # 📸 All captured images
├── data/                # 💾 FileBrowser application data  
├── venv/                # 🐍 Python virtual environment
├── setup_camera.sh      # 🔧 One-time system setup
├── test_camera.py       # ✅ Testing & validation
├── camera_capture.py    # 📷 Production photo capture
├── camera_diagnostics.py # 🔍 System health checks
├── docker-compose.yml   # 🐳 Web interface config
└── README.md           # 📚 This documentation
```

### How It Works:
1. **Setup**: `setup_camera.sh` installs picamera2, creates venv, sets up directories
2. **Capture**: `camera_capture.py` takes timestamped photos → saves to `photos/`
3. **View**: FileBrowser container serves `photos/` via web interface
4. **Monitor**: `camera_diagnostics.py` checks all system components

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

- **Hardware**: Raspberry Pi 3B+ with IMX477 camera
- **OS**: Raspberry Pi OS Bookworm (64-bit recommended)
- **Camera**: IMX477 connected to CSI port, enabled in raspi-config
- **Software**: Docker and Docker Compose
- **Memory**: 128MB+ GPU memory (increase from default 76MB)
- **Network**: For FileBrowser web interface access

### Prerequisites Check:
```bash
# Verify camera detection
libcamera-hello --list-cameras

# Check GPU memory (should be 128MB+)
vcgencmd get_mem gpu

# Verify Docker is installed
docker --version && docker-compose --version
```

## 🔍 **Troubleshooting & Diagnostics**

### Complete System Check
```bash
python3 camera_diagnostics.py
```
**What it checks:**
- ✅ libcamera tools and camera detection
- ✅ picamera2 library availability 
- ✅ GPU memory allocation
- ✅ System memory status
- ✅ Docker container status
- ✅ Project setup verification
- ✅ Quick photo capture test

### Common Issues & Solutions

#### 🔴 **Camera not detected**
```bash
# Enable camera interface
sudo raspi-config  # → Interface Options → Camera → Enable

# Check physical connection
# Ensure ribbon cable firmly connected to CSI port

# Test detection
libcamera-hello --list-cameras

# Reboot after changes
sudo reboot
```

#### 🔴 **Low GPU Memory (76MB → 128MB)**
```bash
# Edit boot configuration
sudo nano /boot/firmware/config.txt

# Add or modify this line:
gpu_mem=128

# Save and reboot
sudo reboot

# Verify change
vcgencmd get_mem gpu
```

#### 🔴 **FileBrowser not accessible**
```bash
# Start container
docker-compose up -d

# Check container status
docker ps

# Find Pi IP address
hostname -I

# Access web interface
# http://<pi-ip>:8080 (admin/admin)

# Check logs if issues
docker logs traffic_camera_filebrowser
```

#### 🔴 **picamera2 import errors**
```bash
# picamera2 is installed system-wide, not in venv
# Use system python directly:
python3 test_camera.py

# Or recreate venv with system packages:
rm -rf venv
python3 -m venv venv --system-site-packages
source venv/bin/activate
```

#### 🔴 **Multiple capture test fails**
This is a known issue with the test script and doesn't affect single photo capture functionality. Use `camera_capture.py` for production photo taking.

### 🔧 **Manual Fixes**

#### Increase GPU Memory
```bash
sudo nano /boot/firmware/config.txt
# Add: gpu_mem=128
sudo reboot
```

#### Reset Docker Containers
```bash
docker-compose down
docker-compose up -d
```

#### Complete System Reset
```bash
./setup_camera.sh  # Re-run setup if needed
```

### 📞 **Getting Help**

**First, run diagnostics:**
```bash
python3 camera_diagnostics.py
```

**Test individual components:**
```bash
libcamera-hello                    # Test camera hardware
python3 test_camera.py             # Test picamera2 integration  
python3 camera_capture.py          # Test photo capture
docker ps                          # Check containers
```

**Check system status:**
```bash
vcgencmd get_mem gpu               # GPU memory
free -h                            # System memory  
docker logs traffic_camera_filebrowser  # Container logs
```

## 📋 **Development Status**

See `projectplan.md` for detailed development phases and progress tracking.