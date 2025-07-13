# TrafficCamera

Traffic Camera project for Raspberry Pi with Arducam IMX477

## Phase 1 Summary

Phase 1 has been completed with the following components:

### Files Created:
1. **setup_camera.sh** - Automated setup script for Raspberry Pi
2. **requirements.txt** - Python dependencies (picamera2, numpy, Pillow)
3. **test_camera.py** - Basic camera test script
4. **camera_capture.py** - Full camera controller with capture functionality
5. **photos/** - Directory for storing captured images

### Setup Instructions:

1. Clone this repository to your Raspberry Pi:
   ```bash
   git clone https://github.com/csantosscott/TrafficCamera.git
   cd TrafficCamera
   ```

2. Run the setup script:
   ```bash
   ./setup_camera.sh
   ```

3. Activate the virtual environment:
   ```bash
   source venv/bin/activate
   ```

4. Test the camera:
   ```bash
   python3 test_camera.py
   ```

5. Test photo capture functionality:
   ```bash
   python3 camera_capture.py
   ```

### Features Implemented:
- Camera initialization for Arducam IMX477
- Single photo capture with timestamp
- Burst photo capture (multiple photos in succession)
- Optimized resolution for license plate capture (2028x1520)
- Organized photo storage in photos/ directory

### Next Steps:
Phase 2 will implement Docker containerization for the application.

## Troubleshooting:

### Camera Memory Issues (ENOSPC):
If you get "ENOSPC" or "Out of resources" errors:

1. **Run the fix script**:
   ```bash
   ./fix_camera_memory.sh
   ```

2. **Or manually increase GPU memory**:
   ```bash
   sudo nano /boot/config.txt
   # Add or modify: gpu_mem=128
   sudo reboot
   ```

3. **Run diagnostics**:
   ```bash
   ./camera_diagnostics.py
   ```

4. **Test with minimal settings**:
   ```bash
   ./test_camera_minimal.py
   ```

### General Issues:
- Ensure camera is enabled in raspi-config
- Check camera connection to CSI port
- Verify with `raspistill -o test.jpg`
- Reboot after any camera configuration changes