# Traffic Camera System Project Plan

## Project Overview
Build a basic traffic camera system on Raspberry Pi 3B+ with Bookworm OS and IMX477 camera. Start with fundamental camera functionality, then add Docker frontend, and finally implement license plate detection features.

## Architecture
- **Hardware**: Raspberry Pi 3B+ with IMX477 Camera
- **OS**: Raspberry Pi OS Bookworm
- **Camera Library**: picamera2 (Bookworm compatible)
- **Container**: Docker with FileBrowser
- **Storage**: Local filesystem with photos/ directory
- **Web Interface**: FileBrowser for image browsing

## Security Group Reference
- Use sg-01c9d9f9004c3949a (Open_SecurityGroup)

## Project Structure
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

## Todo List

### Phase 1: Basic Camera Functionality
- [x] Update setup script for Bookworm compatibility
- [x] Create simple camera test using picamera2 library
- [x] Verify camera capture works reliably
- [x] Test different resolutions and settings
- [x] Ensure photos save correctly to photos/ directory

### Phase 2: Docker Frontend Integration
- [x] Get Docker FileBrowser working
- [x] Configure FileBrowser for image viewing
- [x] Test image preview functionality in browser
- [x] Integration testing - photos appear in FileBrowser interface
- [x] Verify FileBrowser accessible at http://pi-ip:8080

### Phase 3: Codebase Cleanup and Core Functionality
- [x] Update camera_diagnostics.py for Bookworm/picamera2
- [x] Update camera_capture.py for production use
- [x] Remove obsolete scripts and legacy configuration files
- [x] Update documentation with current workflow
- [x] Document FileBrowser access and usage

### Phase 4: Enhanced Camera Features
- [x] Create comprehensive IMX477 documentation with optimal settings
- [x] Add 3 quality modes: production, high_quality, fast
- [x] Implement enhanced timestamped filenames with milliseconds
- [x] Fix multiple capture issue in test_camera.py
- [x] Implement date-based directory structure (YYYY/MM/DD)
- [x] Add command line quality mode selection

### Phase 5: License Plate Detection (Future)
- [ ] Research OCR integration with tesseract-ocr
- [ ] Test basic text extraction from sample images
- [ ] Determine processing requirements
- [ ] Add simple license plate region detection
- [ ] Integrate text extraction
- [ ] Store detected text with images

## Technical Requirements

### System Dependencies
- python3-picamera2 and libcamera-apps
- tesseract-ocr and tesseract-ocr-eng
- python3-opencv
- Docker and docker-compose version 3.8+

### Python Dependencies
- picamera2
- opencv-python
- pytesseract
- numpy
- Pillow

### Environment Variables Needed
- Camera interface: Enabled in raspi-config
- GPU memory: 128MB minimum configured
- Docker: Installed and configured

## Deployment Strategy
1. Incremental development building on existing camera functionality
2. Keep each change simple and focused (minimal complexity)
3. Containerize new components for easy deployment
4. Use filesystem storage (no external databases)
5. Leverage FileBrowser for image management

## Success Criteria
- [ ] System automatically captures images when motion/triggers detected
- [ ] License plates are detected and extracted from images
- [ ] Images organized with meaningful filenames including detected text
- [ ] Web interface allows easy browsing and viewing of captured images
- [ ] System runs reliably in Docker containers
- [ ] Storage efficiently managed with automatic cleanup

## Review Section
*[To be completed after implementation]*

### Changes Made
*[Summary of actual changes implemented]*
- ✅ Camera fully functional with picamera2, photos saving to photos/ directory
- ✅ FileBrowser accessible at http://pi-ip:8080, photos visible in web interface  
- ✅ Codebase cleaned and modernized for Bookworm/picamera2/Docker stack
- ✅ Camera system enhanced with professional-grade features and IMX477 optimization

### Key Learnings
*[Any important discoveries or decisions made during development]*
- Camera memory issues addressed with GPU memory fixes
- Processing performance uses lightweight libraries for async image processing
- Storage limitations handled with automatic cleanup and compression
- Detection accuracy starts with basic OCR, can be enhanced later

### Future Enhancements
*[Potential improvements or features for future iterations]*
- Motion detection triggers for automatic capture
- Advanced license plate recognition algorithms
- Real-time processing and alerts
- Cloud storage integration