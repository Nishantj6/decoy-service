#!/bin/bash
# Quick test script for Decoy Service installation
# Run this to verify everything is working

echo "🧪 Testing Decoy Service Installation..."
echo ""

# Check Python
echo "1. Checking Python..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo "   ✅ $PYTHON_VERSION"
else
    echo "   ❌ Python 3 not found"
    exit 1
fi

# Check Chrome
echo "2. Checking Chrome..."
if [ -d "/Applications/Google Chrome.app" ] || [ -d "/Applications/Chromium.app" ] || command -v google-chrome &> /dev/null || command -v chromium &> /dev/null; then
    echo "   ✅ Chrome/Chromium found"
else
    echo "   ⚠️  Chrome/Chromium not found (required for automation)"
fi

# Check Selenium
echo "3. Checking Selenium..."
if python3 -c "import selenium" 2>/dev/null; then
    echo "   ✅ Selenium installed"
else
    echo "   ❌ Selenium not installed"
    echo "   Install with: pip3 install selenium"
    exit 1
fi

# Check ChromeDriver
echo "4. Checking ChromeDriver..."
if command -v chromedriver &> /dev/null; then
    echo "   ✅ ChromeDriver found"
else
    echo "   ⚠️  ChromeDriver not found"
    echo "   Install with: brew install chromedriver (macOS)"
fi

# Check if daemon is running
echo "5. Checking daemon..."
if curl -s http://localhost:9999/api/health > /dev/null 2>&1; then
    echo "   ✅ Daemon is running"
    HEALTH=$(curl -s http://localhost:9999/api/health)
    echo "   Response: $HEALTH"
else
    echo "   ❌ Daemon not running"
    echo "   Start with: python3 daemon.py &"
    echo ""
    echo "   Would you like to start the daemon now? (y/n)"
    read -r response
    if [[ "$response" =~ ^[Yy]$ ]]; then
        echo "   Starting daemon..."
        python3 daemon.py > /dev/null 2>&1 &
        sleep 2
        if curl -s http://localhost:9999/api/health > /dev/null 2>&1; then
            echo "   ✅ Daemon started successfully"
        else
            echo "   ❌ Failed to start daemon"
            exit 1
        fi
    fi
fi

# Check Firefox extension (can't fully verify, but check Firefox)
echo "6. Checking Firefox..."
if [ -d "/Applications/Firefox.app" ] || command -v firefox &> /dev/null; then
    echo "   ✅ Firefox found"
else
    echo "   ⚠️  Firefox not found"
fi

echo ""
echo "✅ Installation check complete!"
echo ""
echo "Next steps:"
echo "1. Install the Firefox extension (.xpi file)"
echo "2. Click the extension icon"
echo "3. Click 'Start Service'"
echo "4. Verify timer is counting"
echo ""
echo "📖 Full guide: firefox-extension/DISTRIBUTION_GUIDE.md"
