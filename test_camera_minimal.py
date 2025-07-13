#!/usr/bin/env python3
"""
Minimal camera test with memory-efficient settings for Raspberry Pi
"""

import os
import time
from datetime import datetime

try:
    import picamera
    from picamera import PiCamera
except ImportError:
    print("Error: picamera not found. Please run setup_camera.sh first.")
    exit(1)

def test_camera_minimal():
    """Test camera with minimal memory usage"""
    print("Starting minimal camera test...")
    print("This uses lower resolution to avoid memory issues")
    
    camera = None
    try:
        # Create camera instance
        camera = PiCamera()
        
        # Use lower resolution initially to avoid memory issues
        camera.resolution = (1920, 1080)  # 1080p instead of full 12MP
        camera.framerate = 15  # Lower framerate
        
        print("\nCamera initialized with reduced settings:")
        print("Resolution: {}".format(camera.resolution))
        print("Framerate: {}".format(camera.framerate))
        
        # Skip preview to save memory
        print("\nWarming up camera (no preview to save memory)...")
        time.sleep(2)
        
        # Take a test photo
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = "test_minimal_{}.jpg".format(timestamp)
        
        print("\nCapturing test photo: {}".format(filename))
        camera.capture(filename, quality=85)  # Slightly lower quality to save space
        
        # Get file info
        if os.path.exists(filename):
            file_size = os.path.getsize(filename) / 1024  # KB
            print("Photo saved successfully!")
            print("File size: {:.1f} KB".format(file_size))
            print("Location: {}".format(os.path.abspath(filename)))
        else:
            print("Error: Photo file not created")
            return False
            
        print("\nMinimal camera test completed successfully!")
        return True
        
    except Exception as e:
        print("\nError during camera test: {}".format(str(e)))
        
        if "Out of resources" in str(e) or "ENOSPC" in str(e):
            print("\nMemory issue detected! Try these fixes:")
            print("1. Increase GPU memory split:")
            print("   sudo nano /boot/config.txt")
            print("   Add: gpu_mem=128")
            print("   Then reboot")
            print("\n2. Close other applications using the camera")
            print("\n3. Try even lower resolution (640x480)")
        
        return False
    
    finally:
        if camera:
            camera.close()
            print("\nCamera closed")

def check_gpu_split():
    """Quick check of GPU memory"""
    import subprocess
    try:
        result = subprocess.check_output("vcgencmd get_mem gpu", shell=True)
        gpu_mem = result.decode('utf-8').strip()
        print("\nCurrent {}".format(gpu_mem))
        
        if "gpu=" in gpu_mem:
            mem_value = int(gpu_mem.split('=')[1].replace('M', ''))
            if mem_value < 128:
                print("WARNING: GPU memory is low. Recommended: 128 MB or higher")
    except:
        pass

if __name__ == "__main__":
    print("Minimal Camera Test for Raspberry Pi")
    print("=" * 40)
    
    check_gpu_split()
    
    success = test_camera_minimal()
    
    if success:
        print("\n✓ Camera test passed!")
    else:
        print("\n✗ Camera test failed.")
        print("\nRun ./camera_diagnostics.py for detailed diagnostics")
        exit(1)