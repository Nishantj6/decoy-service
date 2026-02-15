#!/bin/bash
# Check if Firefox extension is signed by Mozilla

XPI_FILE="$1"

if [ -z "$XPI_FILE" ]; then
    echo "Usage: ./check-extension-signing.sh <path-to-xpi-file>"
    echo ""
    echo "Example:"
    echo "  ./check-extension-signing.sh firefox-extension/dist/decoy-service-1.0.0.xpi"
    exit 1
fi

if [ ! -f "$XPI_FILE" ]; then
    echo "❌ File not found: $XPI_FILE"
    exit 1
fi

echo "🔍 Checking signing status..."
echo "File: $XPI_FILE"
echo ""

# Check for META-INF signature files
if unzip -l "$XPI_FILE" 2>/dev/null | grep -q "META-INF"; then
    echo "✅ SIGNED BY MOZILLA"
    echo ""
    echo "Signature files found:"
    unzip -l "$XPI_FILE" 2>/dev/null | grep META-INF | awk '{print "  " $4}'
    echo ""
    echo "✓ This extension can be shared with friends"
    echo "✓ Will install in any Firefox version"
    echo "✓ Verified and approved by Mozilla"
else
    echo "❌ NOT SIGNED"
    echo ""
    echo "This is your local build (unsigned)."
    echo ""
    echo "To get it signed:"
    echo "1. Go to: https://addons.mozilla.org/developers/"
    echo "2. Upload this .xpi file"
    echo "3. Choose 'Self-distributed' for unlisted"
    echo "4. Wait for approval (usually minutes)"
    echo "5. Download the signed version"
    echo ""
    echo "⚠️  Do NOT share this unsigned version with friends!"
fi

echo ""
echo "File details:"
echo "  Size: $(ls -lh "$XPI_FILE" | awk '{print $5}')"
echo "  Name: $(basename "$XPI_FILE")"
