# Traffic Camera Project Plan

## Project Overview
Create a Docker container application for Raspberry Pi (Buster Release 10) with Arducam IMX477 12.3MP camera to capture license plate photos triggered by noise threshold.

## Hardware
- Raspberry Pi running Buster Release 10
- Arducam for Raspberry Pi Camera 12.3MP IMX477

## Project Phases

### Phase 1: Camera Setup and Basic Photo Capture ✓

#### TODO Items:
- [x] Verify camera hardware connection and enable camera interface on Raspberry Pi
- [x] Install necessary camera libraries and dependencies
- [x] Create basic Python script to test camera functionality
- [x] Implement photo capture and save functionality
- [x] Test photo quality and adjust camera settings

### Phase 2: Docker Environment Setup

#### TODO Items:
- [ ] Use the filebowser docker image for the application
- [ ] Configure Docker to access camera hardware (privileged mode/device mapping)
- [ ] Create docker-compose.yml for easy deployment
- [ ] Test camera access from within Docker container
- [ ] Assign a local storage directory in the pi for the Docker container to use

### Phase 3: Application Structure

#### TODO Items:
- [ ] Test the filebrowser UI container with the camera.(Check with me on this step)
- [ ] Implement camera module with configurable settings
- [ ] Create photo storage management (file naming, directory structure)
- [ ] Add basic logging functionality
- [ ] Implement configuration file support

### Phase 4: Noise Threshold Trigger (Final Checkpoint)

#### TODO Items:
- [ ] Research and select appropriate audio library for Raspberry Pi
- [ ] Implement noise level monitoring
- [ ] Create configurable noise threshold system
- [ ] Integrate noise trigger with camera capture
- [ ] Add debouncing to prevent excessive captures
- [ ] Test complete system with various noise levels

## Technical Considerations

### Camera Requirements:
- Use libcamera or picamera2 (depending on Buster compatibility)
- Implement proper camera initialization and cleanup
- Consider image format (JPEG for storage efficiency)
- Set appropriate resolution for license plate capture

### Docker Considerations:
- Base image: Consider using `balenalib/raspberry-pi-debian:buster`
- Required privileges for camera access
- Volume mounting for persistent photo storage
- Container restart policy for reliability

### File Structure:
```
traffic_camera/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── config/
│   └── config.yaml
├── src/
│   ├── main.py
│   ├── camera/
│   │   └── camera_controller.py
│   ├── audio/
│   │   └── noise_monitor.py
│   └── utils/
│       └── logger.py
└── photos/
    └── (captured images)
```

## Next Steps
1. Verify hardware setup and camera connection
2. Begin with Phase 1 implementation
3. Test each component before moving to the next phase

## Review Section
(To be completed after implementation)