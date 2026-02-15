#!/usr/bin/env python3
"""
Build script for Firefox extension using Python's zipfile module
Ensures maximum compatibility with Mozilla's validation system
"""

import os
import json
import zipfile
from pathlib import Path

# Configuration
EXTENSION_DIR = Path(__file__).parent
DIST_DIR = EXTENSION_DIR / "dist"
EXTENSION_NAME = "decoy-service"

# Files to include in the extension
FILES_TO_INCLUDE = [
    "manifest.json",
    "background.js",
    "daemon-client.js",
    "popup.html",
    "popup.js",
    "popup.css",
    "icons/icon-16.svg",
    "icons/icon-48.svg",
    "icons/icon-128.svg",
    "pages/options.html",
    "pages/options.js",
    "pages/options.css",
]

def read_version():
    """Read version from manifest.json"""
    manifest_path = EXTENSION_DIR / "manifest.json"
    with open(manifest_path, 'r') as f:
        manifest = json.load(f)
    return manifest['version']

def create_xpi():
    """Create .xpi file with proper zip formatting"""
    version = read_version()

    print(f"🔨 Building Decoy Service Extension v{version}")

    # Create dist directory
    DIST_DIR.mkdir(exist_ok=True)

    # XPI output path
    xpi_path = DIST_DIR / f"{EXTENSION_NAME}-{version}.xpi"

    print("📦 Creating .xpi package...")

    # Create zip file with proper compression
    with zipfile.ZipFile(xpi_path, 'w', zipfile.ZIP_DEFLATED) as xpi:
        for file_path in FILES_TO_INCLUDE:
            full_path = EXTENSION_DIR / file_path
            if full_path.exists():
                # Add file to zip at the correct path
                xpi.write(full_path, file_path)
                print(f"  ✓ {file_path}")
            else:
                print(f"  ⚠️  Skipping missing file: {file_path}")

    # Get file size
    size_kb = xpi_path.stat().st_size // 1024

    print("✅ Build complete!")
    print()
    print(f"📦 Extension package: {xpi_path}")
    print(f"📊 Package size: {size_kb}KB")
    print()
    print("Next steps:")
    print("1. Go to https://addons.mozilla.org/developers/")
    print("2. Click 'Submit a New Add-on'")
    print(f"3. Upload {EXTENSION_NAME}-{version}.xpi")
    print("4. Choose 'Self-distributed' for unlisted distribution")
    print("5. Download the signed .xpi file")
    print()

if __name__ == "__main__":
    create_xpi()
