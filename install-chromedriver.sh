#!/bin/bash
# Auto-install ChromeDriver for Decoy Service
# Works on macOS and Linux without Homebrew

set -e

echo "🔧 Installing ChromeDriver..."
echo ""

# Detect OS
OS=$(uname -s)
ARCH=$(uname -m)

# Detect Chrome version
if [ "$OS" = "Darwin" ]; then
    # macOS
    if [ -d "/Applications/Google Chrome.app" ]; then
        CHROME_VERSION=$(/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --version | awk '{print $3}' | cut -d'.' -f1)
        echo "Detected Chrome version: $CHROME_VERSION"
    else
        echo "⚠️  Google Chrome not found in /Applications/"
        echo "Please install Chrome first: https://www.google.com/chrome/"
        exit 1
    fi
elif [ "$OS" = "Linux" ]; then
    # Linux
    if command -v google-chrome &> /dev/null; then
        CHROME_VERSION=$(google-chrome --version | awk '{print $3}' | cut -d'.' -f1)
        echo "Detected Chrome version: $CHROME_VERSION"
    elif command -v chromium-browser &> /dev/null; then
        CHROME_VERSION=$(chromium-browser --version | awk '{print $2}' | cut -d'.' -f1)
        echo "Detected Chromium version: $CHROME_VERSION"
    else
        echo "⚠️  Chrome/Chromium not found"
        echo "Install with: sudo apt-get install chromium-browser"
        exit 1
    fi
else
    echo "❌ Unsupported OS: $OS"
    exit 1
fi

# Check if chromedriver already exists
if command -v chromedriver &> /dev/null; then
    EXISTING_VERSION=$(chromedriver --version | awk '{print $2}' | cut -d'.' -f1)
    echo "✅ ChromeDriver already installed (version $EXISTING_VERSION)"
    exit 0
fi

# Download ChromeDriver
echo "📥 Downloading ChromeDriver..."

if [ "$OS" = "Darwin" ]; then
    # macOS
    if [ "$ARCH" = "arm64" ]; then
        URL="https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_mac_arm64.zip"
    else
        URL="https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_mac64.zip"
    fi

    curl -L -o /tmp/chromedriver.zip "$URL"
    unzip -o /tmp/chromedriver.zip -d /tmp/

    # Install
    echo "📦 Installing ChromeDriver..."
    sudo mv /tmp/chromedriver /usr/local/bin/

    # Fix macOS security
    echo "🔐 Removing quarantine attribute..."
    sudo xattr -d com.apple.quarantine /usr/local/bin/chromedriver 2>/dev/null || true
    sudo chmod +x /usr/local/bin/chromedriver

elif [ "$OS" = "Linux" ]; then
    # Linux
    URL="https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip"

    curl -L -o /tmp/chromedriver.zip "$URL"
    unzip -o /tmp/chromedriver.zip -d /tmp/

    # Install
    echo "📦 Installing ChromeDriver..."
    sudo mv /tmp/chromedriver /usr/local/bin/
    sudo chmod +x /usr/local/bin/chromedriver
fi

# Cleanup
rm -f /tmp/chromedriver.zip

# Verify
echo ""
echo "✅ ChromeDriver installed successfully!"
chromedriver --version
echo ""
echo "Next step: python3 daemon.py &"
