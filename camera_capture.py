#!/usr/bin/env python3
"""
Camera capture module for license plate photography
"""

import os
import time
from datetime import datetime
from pathlib import Path

try:
    from picamera2 import Picamera2
    from picamera2.encoders import JpegEncoder
    from picamera2.outputs import FileOutput
except ImportError:
    print("Error: picamera2 not found. Please run setup_camera.sh first.")
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
            self.camera = Picamera2()
            
            # Configure for high quality capture optimized for license plates
            # Using 2028x1520 for balance between quality and file size
            config = self.camera.create_still_configuration(
                main={"size": (2028, 1520)},
                lores={"size": (640, 480)},
                display="lores"
            )
            
            self.camera.configure(config)
            self.camera.start()
            
            # Allow camera to warm up
            time.sleep(2)
            
            self.is_initialized = True
            print("Camera initialized successfully")
            return True
            
        except Exception as e:
            print(f"Failed to initialize camera: {str(e)}")
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
            filename = f"{filename_prefix}_{timestamp}.jpg"
            filepath = self.photo_dir / filename
            
            # Capture the photo
            self.camera.capture_file(str(filepath))
            
            # Verify file was created
            if filepath.exists():
                file_size_kb = filepath.stat().st_size / 1024
                print(f"Photo captured: {filename} ({file_size_kb:.1f} KB)")
                return filepath
            else:
                print("Error: Photo file not created")
                return None
                
        except Exception as e:
            print(f"Error capturing photo: {str(e)}")
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
        print(f"Capturing {count} photos with {delay}s delay...")
        
        for i in range(count):
            photo_path = self.capture_photo(f"{filename_prefix}_{i+1}")
            if photo_path:
                captured_photos.append(photo_path)
            
            if i < count - 1:  # Don't delay after last photo
                time.sleep(delay)
        
        print(f"Burst capture complete. Captured {len(captured_photos)} photos.")
        return captured_photos
    
    def cleanup(self):
        """Clean up camera resources"""
        if self.camera and self.is_initialized:
            try:
                self.camera.stop()
                self.camera.close()
                self.is_initialized = False
                print("Camera cleaned up")
            except Exception as e:
                print(f"Error during cleanup: {str(e)}")

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
            print(f"Photo saved to: {photo_path}")
        
        # Wait a moment
        time.sleep(1)
        
        # Burst capture
        print("\nTesting burst capture...")
        burst_photos = camera.capture_burst(count=3, delay=0.5)
        print(f"Burst photos saved: {len(burst_photos)} files")
        
    finally:
        # Always cleanup
        camera.cleanup()

if __name__ == "__main__":
    main()