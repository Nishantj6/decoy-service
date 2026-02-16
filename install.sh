#!/bin/bash
# =============================================================
# Decoy Service - One-Command Installer
# =============================================================
# This script does everything:
#   1. Creates a Python virtual environment & installs dependencies
#   2. Installs Selenium WebDriver
#   3. Copies daemon files to a safe location (~/.decoy-service/app/)
#   4. Installs & starts the LaunchAgent (macOS) or systemd service (Linux)
#
# After running this script, just load the Firefox extension and click Start.
# =============================================================

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
DAEMON_DIR="$HOME/.decoy-service"
APP_DIR="$DAEMON_DIR/app"
LAUNCH_AGENTS_DIR="$HOME/Library/LaunchAgents"
INSTALLED_PLIST="$LAUNCH_AGENTS_DIR/com.decoy-service.daemon.plist"

echo ""
echo "============================================"
echo "  Decoy Service - Installer"
echo "============================================"
echo ""

# --------------------------------------------------
# Step 1: Python virtual environment & dependencies
# --------------------------------------------------
echo "[1/4] Setting up Python environment..."

if [ ! -d "$SCRIPT_DIR/.venv" ]; then
    python3 -m venv "$SCRIPT_DIR/.venv"
    echo "  Created virtual environment at .venv/"
else
    echo "  Virtual environment already exists"
fi

source "$SCRIPT_DIR/.venv/bin/activate"
pip install --upgrade pip -q
pip install -r "$SCRIPT_DIR/requirements.txt" -q
echo "  Dependencies installed"

# --------------------------------------------------
# Step 2: Install Selenium WebDriver (ChromeDriver)
# --------------------------------------------------
echo ""
echo "[2/4] Checking browser driver..."

if command -v chromedriver &>/dev/null; then
    echo "  ChromeDriver already installed: $(chromedriver --version 2>&1 | head -1)"
elif [ -x "$SCRIPT_DIR/install-chromedriver.sh" ]; then
    echo "  Installing ChromeDriver..."
    bash "$SCRIPT_DIR/install-chromedriver.sh" || echo "  Warning: ChromeDriver install failed. You may need to install it manually."
else
    echo "  Warning: ChromeDriver not found. Install it manually or run install-chromedriver.sh"
fi

# --------------------------------------------------
# Step 3: Copy daemon files to TCC-safe location
# --------------------------------------------------
echo ""
echo "[3/4] Setting up daemon..."

# macOS TCC (Transparency, Consent, and Control) blocks LaunchAgents
# from reading files in ~/Documents/, ~/Desktop/, ~/Downloads/.
# We copy everything to ~/.decoy-service/app/ which is not restricted.

mkdir -p "$DAEMON_DIR"
mkdir -p "$APP_DIR"

# Copy daemon and service module
cp "$SCRIPT_DIR/daemon.py" "$APP_DIR/daemon.py"
rm -rf "$APP_DIR/decoy_service"
cp -R "$SCRIPT_DIR/decoy_service" "$APP_DIR/decoy_service"

# Remove nested directory artifact from cp -R
rm -rf "$APP_DIR/decoy_service/decoy_service" 2>/dev/null

# Copy venv site-packages so daemon can find dependencies
if [ -d "$SCRIPT_DIR/.venv/lib" ]; then
    mkdir -p "$APP_DIR/lib"
    SITE_PKG=$(find "$SCRIPT_DIR/.venv/lib" -type d -name "site-packages" | head -1)
    if [ -n "$SITE_PKG" ]; then
        rm -rf "$APP_DIR/lib/site-packages"
        cp -R "$SITE_PKG" "$APP_DIR/lib/site-packages"
    fi
fi

PYTHONPATH_VALUE="$APP_DIR/lib/site-packages:$APP_DIR"
echo "  Daemon files copied to $APP_DIR"

# --------------------------------------------------
# Step 4: Install and start the daemon service
# --------------------------------------------------
echo ""
echo "[4/4] Installing auto-start service..."

if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS LaunchAgent
    mkdir -p "$LAUNCH_AGENTS_DIR"

    cat > "$INSTALLED_PLIST" << PLIST
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.decoy-service.daemon</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>$APP_DIR/daemon.py</string>
    </array>
    <key>WorkingDirectory</key>
    <string>$APP_DIR</string>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>$DAEMON_DIR/daemon-stdout.log</string>
    <key>StandardErrorPath</key>
    <string>$DAEMON_DIR/daemon-stderr.log</string>
    <key>EnvironmentVariables</key>
    <dict>
        <key>PATH</key>
        <string>/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin</string>
        <key>PYTHONUNBUFFERED</key>
        <string>1</string>
        <key>PYTHONPATH</key>
        <string>$PYTHONPATH_VALUE</string>
    </dict>
</dict>
</plist>
PLIST

    chmod 644 "$INSTALLED_PLIST"
    launchctl unload "$INSTALLED_PLIST" 2>/dev/null || true
    launchctl load "$INSTALLED_PLIST"
    echo "  LaunchAgent installed (auto-starts on boot)"

elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux systemd
    SYSTEMD_DIR="$HOME/.config/systemd/user"
    mkdir -p "$SYSTEMD_DIR"

    cat > "$SYSTEMD_DIR/decoy-daemon.service" << EOF
[Unit]
Description=Decoy Service Daemon
After=network.target

[Service]
Type=simple
ExecStart=/usr/bin/python3 $APP_DIR/daemon.py
WorkingDirectory=$APP_DIR
Environment=PYTHONPATH=$PYTHONPATH_VALUE
Restart=always
RestartSec=5

[Install]
WantedBy=default.target
EOF

    systemctl --user daemon-reload
    systemctl --user enable decoy-daemon.service
    systemctl --user start decoy-daemon.service
    echo "  Systemd service installed (auto-starts on boot)"

else
    echo "  Unsupported OS: $OSTYPE"
    exit 1
fi

# --------------------------------------------------
# Verify daemon is running
# --------------------------------------------------
echo ""
echo "Verifying daemon..."
sleep 2

if curl -s http://localhost:9999/api/health | grep -q "healthy"; then
    echo "  Daemon is running on localhost:9999"
else
    echo "  Warning: Daemon not responding yet. It may take a few seconds."
    echo "  Check logs: tail -f ~/.decoy-service/daemon-stderr.log"
fi

# --------------------------------------------------
# Done
# --------------------------------------------------
echo ""
echo "============================================"
echo "  Setup complete!"
echo "============================================"
echo ""
echo "Next step: Install the Firefox extension"
echo ""
echo "  1. Open Firefox"
echo "  2. Go to: about:debugging#/runtime/this-firefox"
echo "  3. Click 'Load Temporary Add-on'"
echo "  4. Select: $SCRIPT_DIR/firefox-extension/manifest.json"
echo "  5. Click the Decoy Service icon and press Start"
echo ""
echo "The daemon runs automatically on every boot."
echo "You never need to run this script again."
echo ""
