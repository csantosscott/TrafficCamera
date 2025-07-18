#!/usr/bin/env python3
"""
Photo directory structure cleanup script
Moves photos from nested YYYY/MM/DD structure to simplified YYYY/ structure
"""

import os
import shutil
from pathlib import Path

def cleanup_photo_structure():
    """Move photos from nested structure to simplified year-only structure"""
    photos_dir = Path("photos")
    
    if not photos_dir.exists():
        print("❌ Photos directory not found")
        return
    
    print("🧹 Cleaning up photo directory structure...")
    print("Moving from: photos/YYYY/MM/DD/filename.jpg")
    print("         to: photos/YYYY/filename.jpg")
    print()
    
    moved_count = 0
    
    # Look for year directories
    for year_dir in photos_dir.iterdir():
        if not year_dir.is_dir() or not year_dir.name.isdigit():
            continue
            
        print(f"📅 Processing year: {year_dir.name}")
        
        # Look for month directories within year
        for month_dir in year_dir.iterdir():
            if not month_dir.is_dir() or not month_dir.name.isdigit():
                continue
                
            print(f"  📂 Found month: {month_dir.name}")
            
            # Look for day directories within month
            for day_dir in month_dir.iterdir():
                if not day_dir.is_dir() or not day_dir.name.isdigit():
                    continue
                    
                print(f"    📂 Found day: {day_dir.name}")
                
                # Move all JPG files from day directory to year directory
                for photo_file in day_dir.glob("*.jpg"):
                    destination = year_dir / photo_file.name
                    
                    # Handle filename conflicts
                    counter = 1
                    original_destination = destination
                    while destination.exists():
                        name_parts = original_destination.stem, counter, original_destination.suffix
                        destination = year_dir / f"{name_parts[0]}_{name_parts[1]:03d}{name_parts[2]}"
                        counter += 1
                    
                    try:
                        shutil.move(str(photo_file), str(destination))
                        print(f"      ✅ Moved: {photo_file.name} → {destination.relative_to(photos_dir)}")
                        moved_count += 1
                    except Exception as e:
                        print(f"      ❌ Failed to move {photo_file.name}: {e}")
    
    print()
    print("🗂️  Removing empty nested directories...")
    
    # Remove empty month/day directories
    for year_dir in photos_dir.iterdir():
        if not year_dir.is_dir() or not year_dir.name.isdigit():
            continue
            
        for month_dir in list(year_dir.iterdir()):
            if not month_dir.is_dir() or not month_dir.name.isdigit():
                continue
                
            # Remove empty day directories
            for day_dir in list(month_dir.iterdir()):
                if day_dir.is_dir() and not any(day_dir.iterdir()):
                    try:
                        day_dir.rmdir()
                        print(f"  🗑️  Removed empty directory: {day_dir.relative_to(photos_dir)}")
                    except Exception as e:
                        print(f"  ❌ Failed to remove {day_dir.relative_to(photos_dir)}: {e}")
            
            # Remove empty month directories
            if not any(month_dir.iterdir()):
                try:
                    month_dir.rmdir()
                    print(f"  🗑️  Removed empty directory: {month_dir.relative_to(photos_dir)}")
                except Exception as e:
                    print(f"  ❌ Failed to remove {month_dir.relative_to(photos_dir)}: {e}")
    
    print()
    print("📊 Cleanup Summary:")
    print(f"   📸 Photos moved: {moved_count}")
    
    # Show final structure
    print()
    print("📁 Final directory structure:")
    for year_dir in sorted(photos_dir.iterdir()):
        if year_dir.is_dir() and year_dir.name.isdigit():
            photo_count = len(list(year_dir.glob("*.jpg")))
            print(f"  📅 {year_dir.name}/ ({photo_count} photos)")
            
            # Show first few files as examples
            photos = list(year_dir.glob("*.jpg"))[:3]
            for photo in photos:
                print(f"    📸 {photo.name}")
            if len(photos) < len(list(year_dir.glob("*.jpg"))):
                remaining = len(list(year_dir.glob("*.jpg"))) - len(photos)
                print(f"    ... and {remaining} more")
    
    print()
    print("✅ Cleanup complete! Photos are now organized as:")
    print("   photos/YYYY/filename_YYYYMMDD_HHMMSS_mmm.jpg")

def main():
    """Main function with safety checks"""
    print("🧹 Photo Directory Structure Cleanup")
    print("=" * 40)
    
    photos_dir = Path("photos")
    
    if not photos_dir.exists():
        print("❌ No photos directory found. Nothing to clean up.")
        return
    
    # Count current nested structure
    nested_photos = 0
    for year_dir in photos_dir.iterdir():
        if year_dir.is_dir() and year_dir.name.isdigit():
            for month_dir in year_dir.iterdir():
                if month_dir.is_dir() and month_dir.name.isdigit():
                    for day_dir in month_dir.iterdir():
                        if day_dir.is_dir() and day_dir.name.isdigit():
                            nested_photos += len(list(day_dir.glob("*.jpg")))
    
    if nested_photos == 0:
        print("✅ No nested photo structure found. Directory is already clean!")
        
        # Show current structure
        print("\n📁 Current structure:")
        for year_dir in sorted(photos_dir.iterdir()):
            if year_dir.is_dir() and year_dir.name.isdigit():
                photo_count = len(list(year_dir.glob("*.jpg")))
                print(f"  📅 {year_dir.name}/ ({photo_count} photos)")
        return
    
    print(f"🔍 Found {nested_photos} photos in nested directories")
    
    # Ask for confirmation
    response = input("\n❓ Proceed with cleanup? (y/N): ").lower().strip()
    if response not in ['y', 'yes']:
        print("❌ Cleanup cancelled.")
        return
    
    # Perform cleanup
    cleanup_photo_structure()
    print("\n🎉 All done! You can now test the new capture system:")
    print("   python3 camera_capture.py")

if __name__ == "__main__":
    main()