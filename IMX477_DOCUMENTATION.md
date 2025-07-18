# IMX477 Camera Sensor Documentation

## 📷 **Sensor Overview**

The Sony IMX477 is a high-quality 12-megapixel sensor used in the Raspberry Pi High Quality Camera and various third-party camera modules.

### Key Specifications:
- **Resolution**: 4056 x 3040 pixels (12.3 MP)
- **Sensor Size**: 7.9mm diagonal (1/2.3")
- **Pixel Size**: 1.55μm x 1.55μm
- **Color Filter**: RGGB Bayer pattern
- **Bit Depth**: 12-bit RAW output
- **Frame Rates**: Up to 120 fps at reduced resolution

## 🔧 **Available Modes** (from libcamera detection)

Based on your system detection:

```
Available cameras:
0 : imx477 [4056x3040 12-bit RGGB] (/base/soc/i2c0mux/i2c@1/imx477@1a)
    Modes: 
    'SRGGB10_CSI2P' : 1332x990 [120.05 fps - (696, 528)/2664x1980 crop]
    'SRGGB12_CSI2P' : 2028x1080 [50.03 fps - (0, 440)/4056x2160 crop]
                      2028x1520 [40.01 fps - (0, 760)/4056x2160 crop]
                      4056x3040 [10.00 fps - (0, 0)/4056x3040 crop]
```

### Mode Analysis:

| Resolution | FPS | Crop Region | Use Case |
|------------|-----|-------------|----------|
| 1332x990   | 120 | Center crop | High-speed capture, motion detection |
| 2028x1080  | 50  | Wide crop   | **Recommended for traffic/license plates** |
| 2028x1520  | 40  | Medium crop | Balanced quality/speed |
| 4056x3040  | 10  | Full sensor | Maximum quality, slow capture |

## 🎯 **Optimal Settings for Traffic Camera**

### For License Plate Capture:
```python
# Recommended configuration
still_config = picam2.create_still_configuration(
    main={"size": (2028, 1520)},  # Good balance of quality/speed
    raw={"size": (4056, 3040)}    # Full resolution RAW for processing
)
```

### Quality Settings:
- **Resolution**: 2028x1520 (3:2 aspect ratio)
- **Format**: JPEG for storage efficiency
- **Quality**: 95% JPEG compression
- **Frame Rate**: 40 fps capability
- **ISO**: 100-400 (low noise)
- **Exposure**: Auto with bias adjustment for lighting conditions

## ⚙️ **picamera2 Configuration Options**

### Basic Still Configuration:
```python
from picamera2 import Picamera2

picam2 = Picamera2()

# High quality setup
config = picam2.create_still_configuration(
    main={
        "size": (2028, 1520),    # Optimal for license plates
        "format": "RGB888"        # Full color depth
    },
    raw={"size": (4056, 3040)},  # Full sensor for best quality
    buffer_count=2                # Reduce memory usage
)

picam2.configure(config)
```

### Advanced Controls:
```python
# Set camera controls for optimal image quality
controls = {
    "ExposureTime": 10000,           # 10ms exposure (adjust for lighting)
    "AnalogueGain": 1.0,            # Start with 1x gain
    "DigitalGain": 1.0,             # Avoid digital gain if possible
    "Brightness": 0.0,              # Neutral brightness
    "Contrast": 1.0,                # Standard contrast
    "Saturation": 1.0,              # Standard color saturation
    "Sharpness": 1.0,               # Slight sharpening for text
    "NoiseReductionMode": 1,        # Minimal noise reduction
}

picam2.set_controls(controls)
```

## 🌟 **Optimization for License Plates**

### Image Quality Factors:
1. **Sharpness**: Critical for text readability
2. **Contrast**: Important for character distinction
3. **Exposure**: Balanced to avoid over/under-exposure
4. **Focus**: Should be set to license plate distance
5. **ISO**: Keep low (100-400) to minimize noise

### Lighting Considerations:
- **Daylight**: Use lower ISO (100-200), faster shutter
- **Overcast**: Increase exposure time slightly
- **Night/Low Light**: Higher ISO (400-800), longer exposure
- **Backlit Plates**: Use exposure compensation

### Distance and Angle:
- **Optimal Distance**: 3-10 meters from license plate
- **Angle**: Perpendicular to plate (minimize skew)
- **Height**: Camera at plate level when possible

## 📊 **Performance Characteristics**

### Memory Usage:
- **1920x1080**: ~6MB per frame
- **2028x1520**: ~9MB per frame  
- **4056x3040**: ~37MB per frame

### Processing Speed:
- **Capture Time**: 100-500ms depending on resolution
- **File Write**: 50-200ms depending on JPEG quality
- **Total Time**: ~300-700ms per photo

### Storage Requirements:
- **JPEG 95% Quality**: 
  - 1920x1080: ~100-200KB per image
  - 2028x1520: ~150-300KB per image
  - 4056x3040: ~800KB-2MB per image

## 🔧 **Recommended Configurations**

### Production Traffic Camera:
```python
# Balanced quality and performance
production_config = {
    "main": {"size": (2028, 1520), "format": "RGB888"},
    "buffer_count": 2,
    "queue": True
}

controls = {
    "ExposureTime": 8000,     # 8ms - good for moving vehicles
    "AnalogueGain": 1.5,      # Slight gain for better sensitivity
    "Sharpness": 1.2,         # Enhanced sharpness for text
    "Contrast": 1.1,          # Slightly increased contrast
    "NoiseReductionMode": 1   # Minimal noise reduction
}
```

### High Quality Archive:
```python
# Maximum quality for evidence/archival
archive_config = {
    "main": {"size": (4056, 3040), "format": "RGB888"},
    "raw": {"size": (4056, 3040)},
    "buffer_count": 1
}

controls = {
    "ExposureTime": 15000,    # Longer exposure for max quality
    "AnalogueGain": 1.0,      # Minimal gain
    "Sharpness": 1.0,         # Natural sharpness
    "NoiseReductionMode": 2   # Higher quality noise reduction
}
```

### Fast Capture Mode:
```python
# For high-speed or burst capture
fast_config = {
    "main": {"size": (1920, 1080), "format": "RGB888"},
    "buffer_count": 3,
    "queue": True
}

controls = {
    "ExposureTime": 5000,     # Fast shutter
    "AnalogueGain": 2.0,      # Higher gain for speed
    "NoiseReductionMode": 0   # No noise reduction for speed
}
```

## 🚨 **Common Issues & Solutions**

### Multiple Capture Failures:
- **Issue**: Camera state errors between captures
- **Solution**: Properly stop/restart camera between captures
- **Workaround**: Use single camera instance with multiple capture_file() calls

### Memory Issues:
- **Issue**: Out of memory with high resolutions
- **Solution**: Ensure GPU memory ≥128MB, use buffer_count=1-2
- **Monitor**: Check `vcgencmd get_mem gpu`

### Image Quality Issues:
- **Blurry Images**: Check focus, increase sharpness setting
- **Noisy Images**: Lower ISO, increase exposure time
- **Over/Under Exposed**: Adjust ExposureTime or use auto-exposure

### Performance Issues:
- **Slow Capture**: Use lower resolution or reduce JPEG quality
- **High CPU**: Enable hardware JPEG encoding if available

## 📚 **References**

- [picamera2 Documentation](https://datasheets.raspberrypi.com/camera/picamera2-manual.pdf)
- [IMX477 Datasheet](https://www.sony-semicon.co.jp/files/62/pdf/p-11_IMX477_Flyer.pdf)
- [libcamera Controls](https://libcamera.org/api-html/controls_8h.html)
- [Raspberry Pi Camera Guide](https://www.raspberrypi.org/documentation/accessories/camera.html)

---

**Last Updated**: Phase 4 Implementation
**Compatible With**: Raspberry Pi OS Bookworm, picamera2, libcamera