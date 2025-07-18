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

# Test camera detection first
echo "Testing camera detection..."
if command -v libcamera-hello >/dev/null 2>&1; then
    echo "✅ libcamera tools found"
    echo "Testing camera detection (5 second test)..."
    timeout 5s libcamera-hello --nopreview 2>/dev/null
    if [ $? -eq 0 ] || [ $? -eq 124 ]; then
        echo "✅ Camera detected successfully"
    else
        echo "❌ Camera not detected. Please check connections and enable camera in raspi-config"
        exit 1
    fi
else
    echo "❌ libcamera tools not found. Installing..."
fi

# Install system dependencies for Bookworm
echo "Installing system dependencies for Bookworm..."
sudo apt-get update
sudo apt-get install -y python3-pip python3-venv python3-picamera2 libcamera-apps libcamera-dev

# Create photos directory
echo "Creating photos directory..."
mkdir -p photos

# Create Python virtual environment
echo "Creating Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install Python packages
echo "Installing Python packages..."
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "Setup complete! 🎉"
echo ""
echo "To test the camera:"
echo "1. source venv/bin/activate"
echo "2. python3 test_camera.py"
echo ""
echo "Camera should be accessible via picamera2 library."