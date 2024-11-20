#!/usr/bin/env python3

from PIL import Image, ExifTags
import argparse
import os
import time
from pathlib import Path

def compatible_exteision(img: str) -> bool:
    return img.lower().endswith((".jpg", ".jpeg", ".png", ".gif", ".bmp"))

def get_metadata(img: str) -> None:

    try:
        image_obj = Image.open(img)
        exif_data = image_obj._getexif()

        file = Path(img)
        creation_time = file.stat().st_ctime
        print(f"\nFile: {img}")
        print(f"Creation Time: {time.ctime(creation_time)}")
        file_size_in_bytes = file.stat().st_size
        file_size_in_mb = file_size_in_bytes / (1024 * 1024)

        print(f"Size: {file_size_in_mb:.2f} MB")
        # print(f"Size: {file.stat().st_size} bytes")

        if not exif_data:
            print(f"No metadata found in {img}\n")
            return
        
        print(f"Metadata for {img}:")
        for tag_id, value in exif_data.items():
            tag_name = ExifTags.TAGS.get(tag_id, tag_id)
            print(f"  {tag_name}: {value}")
        print("\n")

    except Exception as e:
        print(f"Error: processing failed {img}: {e}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("imgs", nargs="+", help="Image files to analyze")
    args = parser.parse_args()

    for img in args.imgs:
        if not compatible_exteision(img):
            print(f"Error: unsupported file: {img}")
            continue
        if os.path.exists(img):
            get_metadata(img)
        else:
            print(f"Error: file not found: {img}")

if __name__ == '__main__':
    main()