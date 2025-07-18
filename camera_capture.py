#!/usr/bin/env python3
"""
Camera capture module for traffic monitoring - Bookworm/picamera2 compatible
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
    print("Please run setup_camera.sh first or install with: sudo apt install python3-picamera2")
    exit(1)

class CameraController:
    """Controller for IMX477 camera operations using picamera2"""
    
    def __init__(self, photo_dir="photos"):
        """Initialize camera controller
        
        Args:
            photo_dir: Directory to save captured photos
        """
        self.photo_dir = Path(photo_dir)
        self.photo_dir.mkdir(exist_ok=True)
        self.picam2 = None
        self.is_initialized = False
        
    def initialize(self):
        """Initialize and configure the camera"""
        try:
            print("Initializing camera with picamera2...")
            self.picam2 = Picamera2()
            
            # Configure for high quality still capture
            still_config = self.picam2.create_still_configuration(
                main={"size": (1920, 1080)}  # 1080p for good quality and performance
            )
            self.picam2.configure(still_config)
            
            print("Starting camera...")
            self.picam2.start()
            
            # Allow camera to warm up
            print("Camera warming up...")
            time.sleep(2)
            
            self.is_initialized = True
            print("Camera initialized successfully")
            print("Configuration: {}".format(still_config))
            return True
            
        except Exception as e:
            print("Failed to initialize camera: {}".format(str(e)))
            self.is_initialized = False
            return False
    
    def capture_photo(self, filename_prefix="capture"):
        """Capture a photo and save to disk
        
        Args:
            filename_prefix: Prefix for the filename
            
        Returns:
            Path to saved photo or None if failed
        """
        if not self.is_initialized:
            print("Camera not initialized. Call initialize() first.")
            return None
            
        try:
            # Generate filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]  # Include milliseconds
            filename = "{}_{}.jpg".format(filename_prefix, timestamp)
            filepath = self.photo_dir / filename
            
            # Capture the photo using picamera2
            self.picam2.capture_file(str(filepath))
            
            # Verify file was created
            if filepath.exists():
                file_size_kb = filepath.stat().st_size / 1024
                print("Photo captured: {} ({:.1f} KB)".format(filename, file_size_kb))
                return filepath
            else:
                print("Error: Photo file not created")
                return None
                
        except Exception as e:
            print("Error capturing photo: {}".format(str(e)))
            return None
    
    def capture_burst(self, count=3, delay=0.5, filename_prefix="burst"):
        """Capture multiple photos in quick succession
        
        Args:
            count: Number of photos to capture
            delay: Delay between captures in seconds
            filename_prefix: Prefix for filenames
            
        Returns:
            List of paths to saved photos
        """
        if not self.is_initialized:
            print("Camera not initialized. Call initialize() first.")
            return []
            
        captured_photos = []
        print("Capturing {} photos with {}s delay...".format(count, delay))
        
        for i in range(count):
            photo_path = self.capture_photo("{}_{}".format(filename_prefix, i+1))
            if photo_path:
                captured_photos.append(photo_path)
            
            if i < count - 1:  # Don't delay after last photo
                time.sleep(delay)
        
        print("Burst capture complete. Captured {} photos.".format(len(captured_photos)))
        return captured_photos
    
    def cleanup(self):
        """Clean up camera resources"""
        if self.picam2 and self.is_initialized:
            try:
                self.picam2.stop()
                self.is_initialized = False
                print("Camera cleaned up")
            except Exception as e:
                print("Error during cleanup: {}".format(str(e)))

def main():
    """Simple single photo capture for production use"""
    camera = CameraController()
    
    try:
        # Initialize camera
        if not camera.initialize():
            print("Failed to initialize camera")
            return
        
        # Single photo capture
        print("\nCapturing photo...")
        photo_path = camera.capture_photo("traffic_camera")
        if photo_path:
            print("Photo saved to: {}".format(photo_path))
            print("View in FileBrowser at: http://<pi-ip>:8080")
        else:
            print("Photo capture failed")
        
    finally:
        # Always cleanup
        camera.cleanup()

if __name__ == "__main__":
    main()