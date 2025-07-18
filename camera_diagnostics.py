#!/usr/bin/env python3
"""
Camera diagnostics script for Bookworm with libcamera/picamera2
"""

import subprocess
import os
from pathlib import Path

def run_command(cmd):
    """Run a shell command and return output"""
    try:
        result = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
        return result.decode('utf-8').strip()
    except subprocess.CalledProcessError as e:
        return "Error: {}".format(e.output.decode('utf-8'))

def check_libcamera_status():
    """Check libcamera and camera detection"""
    print("\n=== libcamera Status ===")
    
    # Check if libcamera tools are available
    libcam_hello = run_command("which libcamera-hello")
    if "libcamera-hello" in libcam_hello:
        print("✅ libcamera-hello found: {}".format(libcam_hello))
    else:
        print("❌ libcamera-hello not found")
    
    # Check camera detection
    print("\nTesting camera detection...")
    cam_test = run_command("timeout 3s libcamera-hello --list-cameras 2>/dev/null || echo 'timeout'")
    if "Available cameras" in cam_test or "IMX477" in cam_test:
        print("✅ Camera detected successfully")
        print("Camera info:")
        print(cam_test[:300])  # First 300 chars
    else:
        print("❌ Camera not detected or timeout occurred")

def check_picamera2_status():
    """Check picamera2 library availability"""
    print("\n=== picamera2 Status ===")
    
    # Test picamera2 import
    test_import = run_command("python3 -c 'import picamera2; print(\"picamera2 version:\", picamera2.__version__)' 2>/dev/null || echo 'Import failed'")
    if "Import failed" not in test_import:
        print("✅ picamera2 library available")
        print(test_import)
    else:
        print("❌ picamera2 library not available")
        print("Install with: sudo apt install python3-picamera2")

def check_gpu_memory():
    """Check GPU memory split"""
    print("\n=== GPU Memory Split ===")
    gpu_mem = run_command("vcgencmd get_mem gpu")
    print("GPU Memory: {}".format(gpu_mem))
    
    # Check if GPU memory is sufficient
    if "gpu=" in gpu_mem:
        mem_value = int(gpu_mem.split('=')[1].replace('M', ''))
        if mem_value >= 128:
            print("✅ GPU memory sufficient ({} MB)".format(mem_value))
        else:
            print("⚠️  GPU memory low ({} MB). Recommended: 128 MB+".format(mem_value))
            print("To fix: Add 'gpu_mem=128' to /boot/firmware/config.txt and reboot")
    
def check_memory():
    """Check system memory"""
    print("\n=== System Memory ===")
    mem_info = run_command("free -h")
    print(mem_info)
    
def check_processes():
    """Check for processes using camera"""
    print("\n=== Camera Processes ===")
    processes = run_command("ps aux | grep -E 'libcamera|picamera|test_camera' | grep -v grep")
    if processes and "Error:" not in processes:
        print("Active camera-related processes:")
        print(processes)
    else:
        print("No active camera processes found")

def check_project_status():
    """Check project setup status"""
    print("\n=== Project Setup Status ===")
    
    # Check photos directory
    photos_dir = Path("photos")
    if photos_dir.exists():
        photo_count = len(list(photos_dir.glob("*.jpg")))
        print("✅ Photos directory exists ({} photos)".format(photo_count))
    else:
        print("❌ Photos directory missing")
    
    # Check venv
    venv_dir = Path("venv")
    if venv_dir.exists():
        print("✅ Virtual environment exists")
    else:
        print("❌ Virtual environment missing")
    
    # Check Docker status
    docker_status = run_command("docker ps --filter name=traffic_camera_filebrowser --format 'table {{.Names}}\t{{.Status}}'")
    if "traffic_camera_filebrowser" in docker_status:
        print("✅ FileBrowser container running")
        print("   Access at: http://<pi-ip>:8080")
    else:
        print("❌ FileBrowser container not running")
        print("   Start with: docker-compose up -d")

def test_quick_capture():
    """Test quick capture with libcamera"""
    print("\n=== Quick Capture Test ===")
    print("Testing libcamera-still capture...")
    
    test_file = "diagnostic_test.jpg"
    result = run_command("libcamera-still -o {} --timeout 2000 --nopreview 2>/dev/null || echo 'capture_failed'".format(test_file))
    
    if os.path.exists(test_file):
        file_size = os.path.getsize(test_file) / 1024
        print("✅ Capture successful: {} ({:.1f} KB)".format(test_file, file_size))
        # Clean up test file
        os.remove(test_file)
    else:
        print("❌ Capture failed")
        print("Try running: python3 test_camera.py")

def suggest_fixes():
    """Suggest fixes for common issues"""
    print("\n=== Troubleshooting Guide ===")
    print("If camera is not working:")
    print("1. Enable camera: sudo raspi-config -> Interface Options -> Camera")
    print("2. Check connection: Ensure ribbon cable is properly connected")
    print("3. Reboot after enabling camera")
    print("4. Run setup: ./setup_camera.sh")
    print("\nIf FileBrowser not accessible:")
    print("1. Start container: docker-compose up -d")
    print("2. Check IP: hostname -I")
    print("3. Access: http://<pi-ip>:8080 (admin/admin)")

def main():
    print("Traffic Camera System Diagnostics - Bookworm/libcamera")
    print("=" * 60)
    
    check_libcamera_status()
    check_picamera2_status()
    check_gpu_memory()
    check_memory()
    check_processes()
    check_project_status()
    test_quick_capture()
    suggest_fixes()

if __name__ == "__main__":
    main()