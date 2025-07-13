#!/usr/bin/env python3
"""
Camera diagnostics script to check system resources and camera configuration
"""

import subprocess
import os

def run_command(cmd):
    """Run a shell command and return output"""
    try:
        result = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
        return result.decode('utf-8').strip()
    except subprocess.CalledProcessError as e:
        return "Error: {}".format(e.output.decode('utf-8'))

def check_gpu_memory():
    """Check GPU memory split"""
    print("\n=== GPU Memory Split ===")
    gpu_mem = run_command("vcgencmd get_mem gpu")
    print(gpu_mem)
    
    # Check if GPU memory is sufficient
    if "gpu=" in gpu_mem:
        mem_value = int(gpu_mem.split('=')[1].replace('M', ''))
        if mem_value < 128:
            print("WARNING: GPU memory is {} MB. Recommended: 128 MB or higher".format(mem_value))
            print("To fix: Add 'gpu_mem=128' to /boot/config.txt and reboot")
    
def check_camera_status():
    """Check camera detection status"""
    print("\n=== Camera Status ===")
    cam_status = run_command("vcgencmd get_camera")
    print(cam_status)
    
def check_memory():
    """Check system memory"""
    print("\n=== System Memory ===")
    mem_info = run_command("free -h")
    print(mem_info)
    
def check_processes():
    """Check for processes using camera"""
    print("\n=== Camera Processes ===")
    processes = run_command("ps aux | grep -E 'camera|raspistill|raspivid' | grep -v grep")
    if processes:
        print("Active camera processes:")
        print(processes)
    else:
        print("No active camera processes found")

def test_basic_capture():
    """Test basic capture with minimal settings"""
    print("\n=== Testing Basic Capture ===")
    print("Attempting capture with reduced resolution...")
    
    # Try progressively smaller resolutions
    resolutions = [
        ("640x480", "raspistill -w 640 -h 480 -o test_640x480.jpg"),
        ("1024x768", "raspistill -w 1024 -h 768 -o test_1024x768.jpg"),
        ("1920x1080", "raspistill -w 1920 -h 1080 -o test_1920x1080.jpg")
    ]
    
    for res, cmd in resolutions:
        print("\nTrying resolution {}...".format(res))
        result = run_command(cmd)
        if "Failed" not in result and os.path.exists("test_{}.jpg".format(res.replace('x', 'x'))):
            print("Success! Captured at {}".format(res))
            file_size = os.path.getsize("test_{}.jpg".format(res.replace('x', 'x'))) / 1024
            print("File size: {:.1f} KB".format(file_size))
        else:
            print("Failed at {}".format(res))
            print(result[:200])  # First 200 chars of error

def suggest_fixes():
    """Suggest fixes based on diagnostics"""
    print("\n=== Recommended Fixes ===")
    print("1. Increase GPU memory split:")
    print("   sudo nano /boot/config.txt")
    print("   Add or modify: gpu_mem=128")
    print("   Then reboot: sudo reboot")
    print("\n2. Ensure camera cable is properly connected")
    print("\n3. Update firmware:")
    print("   sudo apt update")
    print("   sudo apt full-upgrade")
    print("   sudo rpi-update")
    print("\n4. Enable camera interface:")
    print("   sudo raspi-config")
    print("   Navigate to: Interface Options > Camera > Enable")

def main():
    print("Raspberry Pi Camera Diagnostics")
    print("=" * 40)
    
    check_camera_status()
    check_gpu_memory()
    check_memory()
    check_processes()
    test_basic_capture()
    suggest_fixes()

if __name__ == "__main__":
    main()