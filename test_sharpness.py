#!/usr/bin/env python3
"""
Sharpness test script to diagnose blur issues
Tests different exposure times and settings
"""

import time
from datetime import datetime
from pathlib import Path

try:
    from picamera2 import Picamera2
    print("✅ Successfully imported picamera2")
except ImportError as e:
    print(f"❌ Error importing picamera2: {e}")
    exit(1)

def test_sharpness_settings():
    """Test different camera settings to find optimal sharpness"""
    
    photos_dir = Path("photos/sharpness_tests")
    photos_dir.mkdir(parents=True, exist_ok=True)
    
    # Different test configurations
    test_configs = [
        {
            "name": "very_fast_shutter",
            "exposure": 1000,      # 1ms - very fast
            "gain": 2.0,
            "description": "1ms exposure, high gain"
        },
        {
            "name": "fast_shutter", 
            "exposure": 3000,      # 3ms - fast
            "gain": 1.5,
            "description": "3ms exposure, medium gain"
        },
        {
            "name": "medium_shutter",
            "exposure": 5000,      # 5ms - medium
            "gain": 1.2,
            "description": "5ms exposure, low gain"
        },
        {
            "name": "current_production",
            "exposure": 8000,      # 8ms - current setting
            "gain": 1.5,
            "description": "Current production settings"
        }
    ]
    
    picam2 = None
    try:
        print("🔬 Sharpness Test - Testing different exposure settings")
        print("=" * 60)
        
        picam2 = Picamera2()
        
        for i, config in enumerate(test_configs):
            print(f"\n📸 Test {i+1}/4: {config['name']}")
            print(f"   Settings: {config['description']}")
            
            # Configure camera for this test
            still_config = picam2.create_still_configuration(
                main={"size": (2028, 1520), "format": "RGB888"}
            )
            picam2.configure(still_config)
            
            # Start camera
            picam2.start()
            time.sleep(1)  # Brief warmup
            
            # Set test controls
            controls = {
                "ExposureTime": config["exposure"],
                "AnalogueGain": config["gain"],
                "Sharpness": 1.5,         # Higher sharpness for testing
                "Contrast": 1.2,          # Higher contrast
                "NoiseReductionMode": 0   # No noise reduction for max sharpness
            }
            
            picam2.set_controls(controls)
            time.sleep(0.5)  # Allow settings to apply
            
            # Capture test image
            timestamp = datetime.now().strftime("%H%M%S")
            filename = f"{config['name']}_{timestamp}.jpg"
            filepath = photos_dir / filename
            
            print(f"   Capturing: {filename}")
            picam2.capture_file(str(filepath))
            
            if filepath.exists():
                file_size_kb = filepath.stat().st_size / 1024
                print(f"   ✅ Saved: {file_size_kb:.1f} KB")
            else:
                print(f"   ❌ Failed to save")
            
            picam2.stop()
            time.sleep(0.5)  # Brief pause between tests
        
        print("\n" + "=" * 60)
        print("🎯 Sharpness Test Complete!")
        print(f"📁 Test images saved to: {photos_dir}")
        print("\n📋 Next Steps:")
        print("1. View images in FileBrowser to compare sharpness")
        print("2. Find the sharpest image and note its settings")
        print("3. The best settings will be used to update camera_capture.py")
        print("\n🔍 Look for:")
        print("- Sharpest text/details")
        print("- Least motion blur") 
        print("- Good contrast and clarity")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
    finally:
        if picam2:
            try:
                picam2.stop()
            except:
                pass

if __name__ == "__main__":
    test_sharpness_settings()