#!/usr/bin/env python3
"""
Basic camera test script for Arducam IMX477 on Raspberry Pi (Python 3.7 compatible)
"""

import os
import time
from datetime import datetime

try:
    import picamera
    from picamera import PiCamera
except ImportError:
    print("Error: picamera not found. Please run setup_camera.sh first.")
    print("If you're not on a Raspberry Pi, this script won't work.")
    exit(1)

def test_camera():
    """Test basic camera functionality"""
    print("Initializing Arducam IMX477 camera...")
    
    camera = None
    try:
        # Create camera instance
        camera = PiCamera()
        
        # Set camera resolution for IMX477
        camera.resolution = (4056, 3040)  # Full resolution
        
        print("\nCamera initialized successfully!")
        print("Resolution: {}".format(camera.resolution))
        print("Framerate: {}".format(camera.framerate))
        
        # Allow camera to warm up
        print("\nWarming up camera for 2 seconds...")
        camera.start_preview()
        time.sleep(2)
        
        # Take a test photo
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = "test_photo_{}.jpg".format(timestamp)
        
        print("\nCapturing test photo: {}".format(filename))
        camera.capture(filename)
        camera.stop_preview()
        
        # Get file info
        if os.path.exists(filename):
            file_size = os.path.getsize(filename) / (1024 * 1024)  # MB
            print("Photo saved successfully!")
            print("File size: {:.2f} MB".format(file_size))
            print("Location: {}".format(os.path.abspath(filename)))
        else:
            print("Error: Photo file not created")
            return False
            
        print("\nCamera test completed successfully!")
        return True
        
    except Exception as e:
        print("\nError during camera test: {}".format(str(e)))
        print("\nTroubleshooting tips:")
        print("1. Ensure camera is properly connected to CSI port")
        print("2. Run 'sudo raspi-config' and enable camera interface")
        print("3. Reboot after enabling camera")
        print("4. Check camera with 'raspistill -o test.jpg' command")
        return False
    
    finally:
        if camera:
            camera.close()

if __name__ == "__main__":
    print("Arducam IMX477 Camera Test")
    print("=" * 30)
    
    success = test_camera()
    
    if success:
        print("\n✓ Camera test passed! Ready for next phase.")
    else:
        print("\n✗ Camera test failed. Please check the troubleshooting tips.")
        exit(1)