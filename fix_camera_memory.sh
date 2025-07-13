#!/bin/bash
# Script to fix camera memory issues on Raspberry Pi

echo "Camera Memory Fix Script"
echo "======================="

# Check current GPU memory
echo -e "\nCurrent GPU memory allocation:"
vcgencmd get_mem gpu

# Check if we need to update
current_gpu=$(vcgencmd get_mem gpu | grep -oE '[0-9]+')
if [ "$current_gpu" -lt 128 ]; then
    echo -e "\nWARNING: GPU memory is only ${current_gpu}MB"
    echo "The IMX477 camera requires at least 128MB GPU memory"
    
    echo -e "\nTo fix this issue:"
    echo "1. Edit boot config: sudo nano /boot/config.txt"
    echo "2. Add or modify this line: gpu_mem=128"
    echo "3. Save and exit (Ctrl+X, Y, Enter)"
    echo "4. Reboot: sudo reboot"
    
    echo -e "\nWould you like to automatically update the config? (requires sudo)"
    read -p "Update GPU memory to 128MB? [y/N] " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        # Backup current config
        sudo cp /boot/config.txt /boot/config.txt.backup
        
        # Check if gpu_mem exists
        if grep -q "^gpu_mem=" /boot/config.txt; then
            # Update existing value
            sudo sed -i 's/^gpu_mem=.*/gpu_mem=128/' /boot/config.txt
            echo "Updated existing gpu_mem setting"
        else
            # Add new value
            echo -e "\n# Camera memory allocation\ngpu_mem=128" | sudo tee -a /boot/config.txt > /dev/null
            echo "Added gpu_mem=128 to config"
        fi
        
        echo -e "\nConfiguration updated! Please reboot for changes to take effect:"
        echo "sudo reboot"
    fi
else
    echo -e "\nGPU memory is ${current_gpu}MB - this should be sufficient"
fi

# Kill any existing camera processes
echo -e "\nChecking for camera processes..."
if pgrep -f "raspistill|raspivid|camera" > /dev/null; then
    echo "Found camera processes, terminating..."
    pkill -f "raspistill|raspivid|camera"
    sleep 1
fi

# Test camera
echo -e "\nTesting camera with minimal settings..."
raspistill -w 640 -h 480 -o test_minimal.jpg -t 1000

if [ -f test_minimal.jpg ]; then
    echo "✓ Camera test successful!"
    ls -lh test_minimal.jpg
else
    echo "✗ Camera test failed"
    echo "Please check the troubleshooting steps above"
fi