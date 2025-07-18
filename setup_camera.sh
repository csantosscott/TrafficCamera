#!/bin/bash
# Setup script for Raspberry Pi camera - Bookworm Compatible

echo "Camera Setup Script for Raspberry Pi Bookworm"
echo "=============================================="

# Check if running on Raspberry Pi
if [ ! -f /proc/device-tree/model ]; then
    echo "Warning: This doesn't appear to be a Raspberry Pi"
else
    echo "Detected: $(cat /proc/device-tree/model)"
fi

echo ""
echo "Please ensure you have:"
echo "1. Enabled the camera interface using 'sudo raspi-config'"
echo "2. Connected the IMX477 camera to the CSI port"
echo "3. Rebooted after enabling the camera"
echo "4. Verified camera detection with 'libcamera-hello'"
echo ""

# Install system dependencies for Bookworm first
echo "Installing system dependencies for Bookworm..."
sudo apt-get update
sudo apt-get install -y python3-pip python3-venv python3-picamera2 libcamera-apps libcamera-dev libcap-dev

# Create photos directory
echo "Creating photos directory..."
mkdir -p photos

# Create Python virtual environment with system site packages
echo "Creating Python virtual environment with system packages access..."
python3 -m venv venv --system-site-packages
source venv/bin/activate

# Install Python packages
echo "Installing Python packages..."
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "Setup complete! 🎉"
echo ""

# Test camera detection now that dependencies are installed
echo "Testing camera detection..."
if command -v libcamera-hello >/dev/null 2>&1; then
    echo "✅ libcamera tools found"
    if ls /dev/video* >/dev/null 2>&1; then
        echo "✅ Camera devices detected"
        echo "Camera should be ready for use!"
    else
        echo "⚠️  Camera devices not found - check connections and raspi-config"
    fi
else
    echo "⚠️  libcamera tools not found after installation"
fi

echo ""
echo "To test the camera:"
echo "1. source venv/bin/activate"
echo "2. python3 test_camera.py"
echo ""
echo "If camera test fails, try 'libcamera-hello' to verify camera works."