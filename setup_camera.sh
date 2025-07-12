#!/bin/bash
# Setup script for Raspberry Pi camera

echo "Camera Setup Script for Raspberry Pi"
echo "===================================="

# Check if running on Raspberry Pi
if [ ! -f /proc/device-tree/model ]; then
    echo "Warning: This doesn't appear to be a Raspberry Pi"
else
    echo "Detected: $(cat /proc/device-tree/model)"
fi

echo ""
echo "Please ensure you have:"
echo "1. Enabled the camera interface using 'sudo raspi-config'"
echo "2. Connected the Arducam IMX477 camera to the CSI port"
echo "3. Rebooted after enabling the camera"
echo ""

# Install system dependencies
echo "Installing system dependencies..."
sudo apt-get update
sudo apt-get install -y python3-pip python3-venv libcamera-dev python3-libcamera python3-kms++

# Create Python virtual environment
echo "Creating Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install Python packages
echo "Installing Python packages..."
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "Setup complete! To test the camera, run:"
echo "source venv/bin/activate"
echo "python3 test_camera.py"