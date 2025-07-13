#!/usr/bin/env python3
"""
Camera capture module for license plate photography (Python 3.7 compatible)
"""

import os
import time
from datetime import datetime
from pathlib import Path

try:
    import picamera
    from picamera import PiCamera
except ImportError:
    print("Error: picamera not found. Please run setup_camera.sh first.")
    exit(1)

class CameraController:
    """Controller for Arducam IMX477 camera operations"""
    
    def __init__(self, photo_dir="photos"):
        """Initialize camera controller
        
        Args:
            photo_dir: Directory to save captured photos
        """
        self.photo_dir = Path(photo_dir)
        self.photo_dir.mkdir(exist_ok=True)
        self.camera = None
        self.is_initialized = False
        
    def initialize(self):
        """Initialize and configure the camera"""
        try:
            print("Initializing camera...")
            self.camera = PiCamera()
            
            # Configure for high quality capture optimized for license plates
            # Start with lower resolution to avoid memory issues
            # Can be increased if system has enough GPU memory
            self.camera.resolution = (1920, 1080)  # 1080p for memory efficiency
            
            # Set additional camera properties for better image quality
            self.camera.iso = 100  # Low ISO for less noise
            self.camera.sharpness = 0
            self.camera.contrast = 0
            self.camera.brightness = 50
            self.camera.saturation = 0
            
            # Skip preview on systems with limited memory
            # Uncomment if you have enough GPU memory (128MB+)
            # self.camera.start_preview()
            
            # Allow camera to warm up
            time.sleep(2)
            
            self.is_initialized = True
            print("Camera initialized successfully")
            print("Resolution: {}".format(self.camera.resolution))
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
            
            # Capture the photo
            self.camera.capture(str(filepath), quality=95)  # High quality JPEG
            
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
        if self.camera and self.is_initialized:
            try:
                self.camera.stop_preview()
                self.camera.close()
                self.is_initialized = False
                print("Camera cleaned up")
            except Exception as e:
                print("Error during cleanup: {}".format(str(e)))

def main():
    """Test the camera capture functionality"""
    camera = CameraController()
    
    try:
        # Initialize camera
        if not camera.initialize():
            print("Failed to initialize camera")
            return
        
        # Single photo capture
        print("\nTesting single photo capture...")
        photo_path = camera.capture_photo("license_plate")
        if photo_path:
            print("Photo saved to: {}".format(photo_path))
        
        # Wait a moment
        time.sleep(1)
        
        # Burst capture
        print("\nTesting burst capture...")
        burst_photos = camera.capture_burst(count=3, delay=0.5)
        print("Burst photos saved: {} files".format(len(burst_photos)))
        
    finally:
        # Always cleanup
        camera.cleanup()

if __name__ == "__main__":
    main()