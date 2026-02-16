#!/bin/bash
# Setup script for Decoy Daemon
# Configures auto-start on system boot
#
# macOS TCC (Transparency, Consent, and Control) blocks LaunchAgents from
# reading files in ~/Documents/. To work around this, we copy the daemon
# files to ~/.decoy-service/app/ which is not TCC-protected.

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
LAUNCH_AGENTS_DIR="$HOME/Library/LaunchAgents"
INSTALLED_PLIST="$LAUNCH_AGENTS_DIR/com.decoy-service.daemon.plist"
DAEMON_DIR="$HOME/.decoy-service"
APP_DIR="$DAEMON_DIR/app"

echo "Setting up Decoy Service Daemon..."

# Create directories
mkdir -p "$DAEMON_DIR"
mkdir -p "$APP_DIR"
mkdir -p "$LAUNCH_AGENTS_DIR"

# Copy daemon files to TCC-safe location (~/.decoy-service/app/)
# macOS blocks LaunchAgents from reading ~/Documents/
echo "Copying daemon files to $APP_DIR ..."
cp "$SCRIPT_DIR/daemon.py" "$APP_DIR/daemon.py"
rm -rf "$APP_DIR/decoy_service"
cp -R "$SCRIPT_DIR/decoy_service" "$APP_DIR/decoy_service"

# Remove any nested decoy_service/decoy_service directory (cp -R artifact)
rm -rf "$APP_DIR/decoy_service/decoy_service" 2>/dev/null

# Copy venv site-packages so daemon can import dependencies
if [ -d "$SCRIPT_DIR/.venv/lib" ]; then
    echo "Copying Python packages..."
    mkdir -p "$APP_DIR/lib"
    SITE_PKG=$(find "$SCRIPT_DIR/.venv/lib" -type d -name "site-packages" | head -1)
    if [ -n "$SITE_PKG" ]; then
        rm -rf "$APP_DIR/lib/site-packages"
        cp -R "$SITE_PKG" "$APP_DIR/lib/site-packages"
    fi
fi

# Detect Python site-packages path for PYTHONPATH
PYTHON_VERSION=$(/usr/bin/python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')" 2>/dev/null || echo "3.9")
PYTHONPATH_VALUE="$APP_DIR/lib/site-packages:$APP_DIR"

echo "Files copied to: $APP_DIR"

if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS LaunchAgent
    echo "Configuring macOS LaunchAgent..."

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

    # Load the LaunchAgent
    launchctl unload "$INSTALLED_PLIST" 2>/dev/null || true
    launchctl load "$INSTALLED_PLIST"

    echo "LaunchAgent installed and loaded"
    echo "Daemon will auto-start on every boot"

elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux (systemd)
    echo "Configuring Linux systemd service..."

    SYSTEMD_DIR="$HOME/.config/systemd/user"
    SYSTEMD_SERVICE="$SYSTEMD_DIR/decoy-daemon.service"

    mkdir -p "$SYSTEMD_DIR"

    cat > "$SYSTEMD_SERVICE" << EOF
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

    echo "Systemd service installed and started"
    echo "Daemon will auto-start on every boot"

else
    echo "Unsupported OS: $OSTYPE"
    exit 1
fi

echo ""
echo "Setup complete!"
echo ""
echo "The daemon runs automatically on boot."
echo "Open Firefox and click Start in the Decoy Service extension."
echo ""
