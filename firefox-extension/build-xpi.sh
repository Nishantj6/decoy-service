#!/bin/bash
# Build script for Decoy Service Firefox Extension
# Creates a .xpi file ready for Mozilla signing

set -e

EXTENSION_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BUILD_DIR="${EXTENSION_DIR}/build"
DIST_DIR="${EXTENSION_DIR}/dist"
EXTENSION_NAME="decoy-service"

# Read version from manifest.json
VERSION=$(grep '"version"' "${EXTENSION_DIR}/manifest.json" | sed -E 's/.*"version": "([^"]+)".*/\1/')

echo "🔨 Building Decoy Service Extension v${VERSION}"

# Clean previous builds
rm -rf "${BUILD_DIR}" "${DIST_DIR}"
mkdir -p "${BUILD_DIR}" "${DIST_DIR}"

# Copy extension files to build directory
echo "📦 Copying extension files..."
cp "${EXTENSION_DIR}/manifest.json" "${BUILD_DIR}/"
cp "${EXTENSION_DIR}/background.js" "${BUILD_DIR}/"
cp "${EXTENSION_DIR}/daemon-client.js" "${BUILD_DIR}/"
cp "${EXTENSION_DIR}/popup.html" "${BUILD_DIR}/"
cp "${EXTENSION_DIR}/popup.js" "${BUILD_DIR}/"
cp "${EXTENSION_DIR}/popup.css" "${BUILD_DIR}/"
cp -r "${EXTENSION_DIR}/icons" "${BUILD_DIR}/"
cp -r "${EXTENSION_DIR}/pages" "${BUILD_DIR}/"

# Create .xpi file (which is just a zip file)
echo "🗜️  Creating .xpi package..."
cd "${BUILD_DIR}"
XPI_FILE="${DIST_DIR}/${EXTENSION_NAME}-${VERSION}.xpi"
zip -r -FS "${XPI_FILE}" * -x "*.DS_Store"

cd "${EXTENSION_DIR}"
echo "✅ Build complete!"
echo ""
echo "📦 Extension package: ${XPI_FILE}"
echo "📊 Package size: $(du -h "${XPI_FILE}" | cut -f1)"
echo ""
echo "Next steps:"
echo "1. Go to https://addons.mozilla.org/developers/"
echo "2. Click 'Submit a New Add-on'"
echo "3. Upload ${EXTENSION_NAME}-${VERSION}.xpi"
echo "4. Choose 'Self-distributed' for unlisted distribution"
echo "5. Download the signed .xpi file"
echo ""
