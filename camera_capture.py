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
        
    def initialize(self, quality_mode="production"):
        """Initialize and configure the camera
        
        Args:
            quality_mode: "production", "high_quality", or "fast"
        """
        try:
            print("Initializing camera with picamera2...")
            self.picam2 = Picamera2()
            
            # Configure based on quality mode
            if quality_mode == "high_quality":
                # Maximum quality for archival/evidence
                still_config = self.picam2.create_still_configuration(
                    main={"size": (4056, 3040), "format": "RGB888"},
                    raw={"size": (4056, 3040)},
                    buffer_count=1
                )
                controls = {
                    "ExposureTime": 15000,    # 15ms for max quality
                    "AnalogueGain": 1.0,      # Minimal gain
                    "Sharpness": 1.0,         # Natural sharpness
                    "NoiseReductionMode": 2   # High quality noise reduction
                    # Note: Focus must be set manually on lens for now
                }
                print("Mode: High Quality (4056x3040)")
                
            elif quality_mode == "fast":
                # Fast capture for high-speed scenarios
                still_config = self.picam2.create_still_configuration(
                    main={"size": (1920, 1080), "format": "RGB888"},
                    buffer_count=3
                )
                controls = {
                    "ExposureTime": 5000,     # 5ms fast shutter
                    "AnalogueGain": 2.0,      # Higher gain for speed
                    "NoiseReductionMode": 0   # No noise reduction for speed
                    # Note: Focus must be set manually on lens for now
                }
                print("Mode: Fast Capture (1920x1080)")
                
            else:  # production (default)
                # Balanced quality and performance for traffic camera
                still_config = self.picam2.create_still_configuration(
                    main={"size": (2028, 1520), "format": "RGB888"},
                    buffer_count=2
                )
                controls = {
                    "ExposureTime": 8000,     # 8ms - good for moving vehicles
                    "AnalogueGain": 1.5,      # Slight gain for sensitivity
                    "Sharpness": 1.2,         # Enhanced sharpness for text
                    "Contrast": 1.1,          # Slightly increased contrast
                    "NoiseReductionMode": 1   # Minimal noise reduction
                    # Note: Focus must be set manually on lens for now
                }
                print("Mode: Production (2028x1520) - Optimized for license plates")
            
            self.picam2.configure(still_config)
            
            print("Starting camera...")
            self.picam2.start()
            
            # Apply camera controls for optimal image quality
            print("Applying camera controls...")
            self.picam2.set_controls(controls)
            
            # Allow camera to warm up and stabilize
            print("Camera warming up and stabilizing...")
            time.sleep(2)
            
            # Camera is now ready (focus must be set manually on lens)
            print("⚠️  Focus: Please manually adjust lens focus ring for optimal sharpness")
            print("   Recommended: Set focus to 3-10 meters for license plate capture")
            time.sleep(1)  # Allow settings to stabilize
            
            self.is_initialized = True
            print("Camera initialized successfully - MANUAL FOCUS REQUIRED")
            print("Configuration: {}".format(still_config))
            print("Controls applied: {}".format(controls))
            return True
            
        except Exception as e:
            print("Failed to initialize camera: {}".format(str(e)))
            self.is_initialized = False
            return False
    
    def ensure_focus(self):
        """Remind user about manual focus (no software control available)"""
        if not self.is_initialized:
            return False
            
        try:
            # Manual focus must be set on lens itself
            print("📷 Focus: Manual lens adjustment required")
            time.sleep(0.1)  # Brief pause
            return True
        except Exception as e:
            print("⚠️  Focus check failed: {}".format(str(e)))
            return True  # Continue anyway
    
    def capture_photo(self, filename_prefix="traffic_camera", organize_by_date=True):
        """Capture a photo and save to disk with timestamp and optional date organization
        
        Args:
            filename_prefix: Prefix for the filename
            organize_by_date: Create date-based subdirectories
            
        Returns:
            Path to saved photo or None if failed
        """
        if not self.is_initialized:
            print("Camera not initialized. Call initialize() first.")
            return None
            
        try:
            # Generate timestamp
            now = datetime.now()
            timestamp = now.strftime("%Y%m%d_%H%M%S_%f")[:-3]  # Include milliseconds
            
            # Create year-based directory structure if requested
            if organize_by_date:
                year_dir = self.photo_dir / now.strftime("%Y")
                year_dir.mkdir(exist_ok=True)
                save_dir = year_dir
            else:
                save_dir = self.photo_dir
            
            # Generate filename with enhanced timestamp format
            # Format: prefix_YYYYMMDD_HHMMSS_mmm.jpg
            filename = "{}_{}_{}.jpg".format(
                filename_prefix,
                now.strftime("%Y%m%d"),
                now.strftime("%H%M%S_%f")[:-3]  # Include milliseconds
            )
            filepath = save_dir / filename
            
            # Ensure proper focus before capture
            print("Ensuring focus...")
            self.ensure_focus()
            
            # Capture the photo using picamera2
            print("Capturing: {}".format(filename))
            self.picam2.capture_file(str(filepath))
            
            # Verify file was created and get metadata
            if filepath.exists():
                file_size_kb = filepath.stat().st_size / 1024
                relative_path = filepath.relative_to(self.photo_dir)
                print("✅ Photo captured: {} ({:.1f} KB)".format(relative_path, file_size_kb))
                print("   Full path: {}".format(filepath))
                return filepath
            else:
                print("❌ Error: Photo file not created")
                return None
                
        except Exception as e:
            print("❌ Error capturing photo: {}".format(str(e)))
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
    """Enhanced single photo capture with quality options"""
    import sys
    
    # Check for quality mode argument
    quality_mode = "production"  # default
    if len(sys.argv) > 1:
        mode = sys.argv[1].lower()
        if mode in ["production", "high_quality", "fast"]:
            quality_mode = mode
        else:
            print("Usage: python3 camera_capture.py [production|high_quality|fast]")
            print("Defaulting to production mode...")
    
    camera = CameraController()
    
    try:
        # Initialize camera with specified quality mode
        print("=== Traffic Camera Enhanced Capture ===")
        if not camera.initialize(quality_mode=quality_mode):
            print("Failed to initialize camera")
            return
        
        # Single photo capture with date organization
        print("\nCapturing photo with enhanced settings...")
        photo_path = camera.capture_photo("traffic_camera", organize_by_date=True)
        
        if photo_path:
            print("\n🎉 Capture successful!")
            print("📁 View in FileBrowser at: http://<pi-ip>:8080")
            print("📋 Quality mode: {}".format(quality_mode))
            
            # Show directory structure
            relative_path = photo_path.relative_to(Path("photos"))
            print("📂 Organized path: photos/{}".format(relative_path))
            print("📅 Year-based organization with full datetime in filename")
        else:
            print("\n❌ Photo capture failed")
            return 1
        
    except KeyboardInterrupt:
        print("\n⏹️  Capture interrupted by user")
        return 1
    finally:
        # Always cleanup
        camera.cleanup()
    
    return 0

if __name__ == "__main__":
    exit(main())