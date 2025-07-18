#!/usr/bin/env python3
"""
Basic camera test script for IMX477 - Bookworm Compatible
"""

import os
import time
from datetime import datetime
from pathlib import Path

try:
    from picamera2 import Picamera2
    print("✅ Successfully imported picamera2")
except ImportError as e:
    print(f"❌ Error importing picamera2: {e}")
    print("Please run setup_camera.sh first.")
    print("If you're not on a Raspberry Pi, this script won't work.")
    exit(1)

def test_camera():
    """Test basic camera functionality with picamera2"""
    print("Initializing IMX477 camera with picamera2...")
    
    picam2 = None
    try:
        # Create photos directory if it doesn't exist
        photos_dir = Path("photos")
        photos_dir.mkdir(exist_ok=True)
        
        # Initialize picamera2
        picam2 = Picamera2()
        
        # Configure camera for still capture (start with 1080p for testing)
        still_config = picam2.create_still_configuration(main={"size": (1920, 1080)})
        picam2.configure(still_config)
        
        print("\nCamera initialized successfully!")
        print("Configuration: {}".format(still_config))
        
        # Start camera
        print("\nStarting camera...")
        picam2.start()
        
        # Camera warm-up time
        print("Warming up camera for 2 seconds...")
        time.sleep(2)
        
        # Take a test photo
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = "test_photo_{}.jpg".format(timestamp)
        filepath = photos_dir / filename
        
        print("\nCapturing test photo: {}".format(filename))
        picam2.capture_file(str(filepath))
        
        # Verify file was created
        if filepath.exists():
            file_size_kb = filepath.stat().st_size / 1024
            print("Photo saved successfully!")
            print("File size: {:.1f} KB".format(file_size_kb))
            print("Location: {}".format(filepath.absolute()))
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
        print("4. Check camera with 'libcamera-hello --nopreview' command")
        print("5. Ensure libcamera-apps is installed")
        return False
    
    finally:
        if picam2:
            picam2.stop()

def test_multiple_captures():
    """Test multiple photo captures"""
    print("\n" + "=" * 40)
    print("Testing multiple captures...")
    
    picam2 = None
    try:
        photos_dir = Path("photos")
        photos_dir.mkdir(exist_ok=True)
        
        picam2 = Picamera2()
        still_config = picam2.create_still_configuration(main={"size": (1920, 1080)})
        picam2.configure(still_config)
        picam2.start()
        
        time.sleep(3)  # Longer warm up for multiple captures
        
        for i in range(3):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
            filename = "multi_test_{:02d}_{}.jpg".format(i+1, timestamp)
            filepath = photos_dir / filename
            
            print("Capture {}/3: {}".format(i+1, filename))
            picam2.capture_file(str(filepath))
            
            if filepath.exists():
                file_size_kb = filepath.stat().st_size / 1024
                print("  ✅ Saved - {:.1f} KB".format(file_size_kb))
            else:
                print("  ❌ Failed to save")
                return False
            
            if i < 2:  # Don't sleep after last capture
                time.sleep(1)
        
        print("✅ Multiple capture test successful!")
        return True
        
    except Exception as e:
        print("❌ Multiple capture test failed: {}".format(str(e)))
        return False
    
    finally:
        if picam2:
            picam2.stop()

if __name__ == "__main__":
    print("IMX477 Camera Test - Bookworm/picamera2")
    print("=" * 40)
    
    # Test basic capture
    success = test_camera()
    
    if success:
        print("\n🎉 Basic camera test passed!")
        
        # Test multiple captures
        multi_success = test_multiple_captures()
        
        if multi_success:
            print("\n🎉 All camera tests passed!")
            print("\nNext steps:")
            print("1. Check photos/ directory for captured images")
            print("2. Run Docker FileBrowser to view images via web interface")
            print("3. Continue with Phase 2 of project plan")
        else:
            print("\n⚠️  Basic test passed but multiple capture test failed")
    else:
        print("\n💥 Camera test failed. Check troubleshooting tips above.")
        exit(1)