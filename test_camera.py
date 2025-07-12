#!/usr/bin/env python3
"""
Basic camera test script for Arducam IMX477 on Raspberry Pi
"""

import os
import time
from datetime import datetime

try:
    from picamera2 import Picamera2, Preview
    from picamera2.encoders import JpegEncoder
    from picamera2.outputs import FileOutput
except ImportError:
    print("Error: picamera2 not found. Please run setup_camera.sh first.")
    print("If you're not on a Raspberry Pi, this script won't work.")
    exit(1)

def test_camera():
    """Test basic camera functionality"""
    print("Initializing Arducam IMX477 camera...")
    
    try:
        # Create camera instance
        picam2 = Picamera2()
        
        # Print camera properties
        print("\nCamera properties:")
        print(f"Camera model: {picam2.camera_properties.get('Model', 'Unknown')}")
        print(f"Sensor modes available: {len(picam2.sensor_modes)}")
        
        # Configure camera for high quality still images
        config = picam2.create_still_configuration(
            main={"size": (4056, 3040)},  # Full resolution for IMX477
            lores={"size": (1012, 760)},   # Low res for preview
            display="lores"
        )
        
        picam2.configure(config)
        
        print("\nCamera configured successfully!")
        print(f"Main stream resolution: {config['main']['size']}")
        print(f"Preview stream resolution: {config['lores']['size']}")
        
        # Start camera
        picam2.start()
        print("\nCamera started. Warming up for 2 seconds...")
        time.sleep(2)
        
        # Take a test photo
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"test_photo_{timestamp}.jpg"
        
        print(f"\nCapturing test photo: {filename}")
        picam2.capture_file(filename)
        
        # Get file info
        if os.path.exists(filename):
            file_size = os.path.getsize(filename) / (1024 * 1024)  # MB
            print(f"Photo saved successfully!")
            print(f"File size: {file_size:.2f} MB")
            print(f"Location: {os.path.abspath(filename)}")
        else:
            print("Error: Photo file not created")
        
        # Stop camera
        picam2.stop()
        picam2.close()
        print("\nCamera test completed successfully!")
        
    except Exception as e:
        print(f"\nError during camera test: {str(e)}")
        print("\nTroubleshooting tips:")
        print("1. Ensure camera is properly connected to CSI port")
        print("2. Run 'sudo raspi-config' and enable camera interface")
        print("3. Reboot after enabling camera")
        print("4. Check camera with 'libcamera-hello' command")
        return False
    
    return True

if __name__ == "__main__":
    print("Arducam IMX477 Camera Test")
    print("=" * 30)
    
    success = test_camera()
    
    if success:
        print("\n✓ Camera test passed! Ready for next phase.")
    else:
        print("\n✗ Camera test failed. Please check the troubleshooting tips.")
        exit(1)