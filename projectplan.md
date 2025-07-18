# Traffic Camera System - Project Plan (Revised)

## Project Overview
Build a basic traffic camera system on Raspberry Pi 3B+ with Bookworm OS and IMX477 camera. Start with fundamental camera functionality, then add Docker frontend, and finally implement license plate detection features.

## Current Status Analysis
### Existing Components ✅
- ✅ Raspberry Pi 3B+ with Bookworm OS
- ✅ IMX477 camera detected (libcamera-hello working)
- ✅ Basic Docker setup with FileBrowser container
- ✅ Camera diagnostics and memory optimization tools
- ✅ Photo storage directory structure

### Technology Stack
- **Hardware**: Raspberry Pi 3B+, IMX477 Camera  
- **OS**: Raspberry Pi OS Bookworm
- **Camera Library**: picamera2 (Bookworm compatible)
- **Container**: Docker with FileBrowser
- **Storage**: Local filesystem with photos/ directory
- **Web Interface**: FileBrowser for image browsing

## Implementation Plan - REVISED (Basics First)

### Phase 1: Basic Camera Functionality ⭐ START HERE
#### Todo Items:
- [ ] **1.1** Update setup script for Bookworm compatibility
  - Modify `setup_camera.sh` to install picamera2 instead of picamera
  - Update system dependencies for Bookworm
  - Test installation process

- [ ] **1.2** Create simple camera test
  - Update `test_camera.py` to use picamera2 library
  - Test basic photo capture functionality
  - Verify photos are saved correctly to photos/ directory

- [ ] **1.3** Verify camera capture works reliably
  - Test different resolutions and settings
  - Ensure memory issues are resolved
  - Confirm photos are accessible via filesystem

### Phase 2: Docker Frontend Integration
#### Todo Items:
- [ ] **2.1** Get Docker FileBrowser working
  - Ensure Docker is installed and running
  - Test FileBrowser container startup
  - Verify photos/ directory is accessible via web interface

- [ ] **2.2** Configure FileBrowser for image viewing
  - Test image preview functionality in browser
  - Configure proper permissions for photo access
  - Set up basic authentication (change default credentials)

- [ ] **2.3** Integration testing
  - Capture photos with camera script
  - Verify images appear in FileBrowser interface
  - Test end-to-end workflow

### Phase 3: Enhanced Camera Features
#### Todo Items:
- [ ] **3.1** Improve camera capture system
  - Add timestamp to photo filenames
  - Implement burst capture mode
  - Add basic image quality settings

- [ ] **3.2** File organization
  - Create organized directory structure by date
  - Add basic metadata tracking
  - Implement simple cleanup routines

### Phase 4: License Plate Detection (Future)
#### Todo Items:
- [ ] **4.1** Research OCR integration
  - Evaluate tesseract-ocr for text detection
  - Test basic text extraction from sample images
  - Determine processing requirements

- [ ] **4.2** Implement basic detection
  - Add simple license plate region detection
  - Integrate text extraction
  - Store detected text with images

## Technical Requirements

### System Dependencies
```bash
# Camera and imaging
sudo apt-get install python3-picamera2 libcamera-apps
sudo apt-get install tesseract-ocr tesseract-ocr-eng
sudo apt-get install python3-opencv

# Docker (already configured)
docker-compose version 3.8+
FileBrowser container
```

### Python Dependencies (requirements.txt update needed)
```
picamera2
opencv-python
pytesseract
numpy
Pillow
```

### Hardware Configuration
- GPU memory: 128MB minimum (already configured via fix_camera_memory.sh)
- Camera interface: Enabled in raspi-config
- Docker: Installed and configured

## File Structure Plan
```
TrafficCamera/
├── src/
│   ├── camera_service.py          # Main camera service
│   ├── license_plate_detector.py  # OCR and detection logic
│   ├── image_processor.py         # Image preprocessing
│   └── file_organizer.py          # File management
├── docker/
│   ├── Dockerfile.camera          # Camera service container
│   └── docker-compose.yml         # Updated with camera service
├── photos/
│   ├── raw/                       # Original captures
│   ├── processed/                 # Enhanced images
│   └── thumbnails/                # Quick preview images
├── config/
│   ├── camera_config.json         # Camera settings
│   └── detection_config.json     # Detection parameters
└── logs/                          # System logs
```

## Implementation Approach
1. **Incremental Development**: Build on existing camera capture functionality
2. **Minimal Complexity**: Keep each change simple and focused
3. **Docker-First**: Containerize new components for easy deployment
4. **Local Storage**: Use filesystem storage (no external databases)
5. **Web Interface**: Leverage FileBrowser for image management

## Success Criteria
- [ ] System automatically captures images when motion/triggers detected
- [ ] License plates are detected and extracted from images
- [ ] Images are organized with meaningful filenames including detected text
- [ ] Web interface allows easy browsing and viewing of captured images
- [ ] System runs reliably in Docker containers
- [ ] Storage is efficiently managed with automatic cleanup

## Risk Mitigation
- **Camera Memory Issues**: Already addressed with GPU memory fixes
- **Processing Performance**: Use lightweight libraries, process images async
- **Storage Limitations**: Implement automatic cleanup and compression
- **Detection Accuracy**: Start with basic OCR, can enhance later

## Review Section
*This section will be updated as implementation progresses*

---

**Next Steps**: 
1. Confirm this plan meets project requirements
2. Begin with Phase 1.1 - updating camera system for picamera2
3. Test basic license plate detection capabilities
4. Integrate with existing Docker setup