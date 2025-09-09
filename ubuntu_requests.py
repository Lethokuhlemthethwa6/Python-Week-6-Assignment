"""
Ubuntu Image Fetcher
A mindful tool for collecting and organizing shared images from the web.

Ubuntu principles applied:
- Community: Connecting to the web’s shared resources
- Respect: Handling errors gracefully
- Sharing: Saving images in an organized folder
- Practicality: Useful for reusing images later

Author: Lethokuhle Mthethwa
"""

import os
import requests
from urllib.parse import urlparse
import hashlib

SAVE_DIR = "Fetched_Images"

def is_safe_response(response):
    """
    Check important HTTP headers to ensure safe download.
    """
    content_type = response.headers.get("Content-Type", "")
    content_length = response.headers.get("Content-Length")

    # Only allow image types
    if not content_type.startswith("image/"):
        print("✗ Not an image, skipping download.")
        return False
    
    # Optional: Prevent extremely large downloads
    if content_length and int(content_length) > 10_000_000:  # 10MB
        print("✗ File too large, skipping download.")
        return False

    return True

def generate_hash(content):
    """
    Generate a hash of the file content to prevent duplicates.
    """
    return hashlib.md5(content).hexdigest()

def fetch_image(url, downloaded_hashes):
    """
    Fetch and save a single image.
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        if not is_safe_response(response):
            return

        # Check for duplicate content
        file_hash = generate_hash(response.content)
        if file_hash in downloaded_hashes:
            print(f"⚠️ Duplicate detected, skipping: {url}")
            return
        downloaded_hashes.add(file_hash)

        # Extract filename from URL or generate one
        parsed_url = urlparse(url)
        filename = os.path.basename(parsed_url.path) or "downloaded_image.jpg"
        filepath = os.path.join(SAVE_DIR, filename)

        # Prevent overwriting by renaming
        base, ext = os.path.splitext(filename)
        counter = 1
        while os.path.exists(filepath):
            filename = f"{base}_{counter}{ext}"
            filepath = os.path.join(SAVE_DIR, filename)
            counter += 1

        # Save image in binary mode
        with open(filepath, "wb") as f:
            f.write(response.content)

        print(f"✓ Successfully fetched: {filename}")
        print(f"✓ Image saved to {filepath}")

    except requests.exceptions.RequestException as e:
        print(f"✗ Connection error: {e}")
    except Exception as e:
        print(f"✗ An unexpected error occurred: {e}")

def main():
    print("🌍 Welcome to the Ubuntu Image Fetcher")
    print("A tool for mindfully collecting images from the web\n")

    # Create directory if not exists
    os.makedirs(SAVE_DIR, exist_ok=True)

    # Get multiple URLs from user (comma-separated)
    urls = input("Please enter one or more image URLs (separated by commas): ").split(",")

    downloaded_hashes = set()
    for url in [u.strip() for u in urls if u.strip()]:
        fetch_image(url, downloaded_hashes)

    print("\nConnection strengthened. Community enriched. 🫶")

if __name__ == "__main__":
    main()
