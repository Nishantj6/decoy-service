#!/bin/bash
# Setup script for Decoy Daemon
# Configures auto-start on system boot

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PLIST_FILE="$SCRIPT_DIR/com.decoy-service.daemon.plist"
LAUNCH_AGENTS_DIR="$HOME/Library/LaunchAgents"
INSTALLED_PLIST="$LAUNCH_AGENTS_DIR/com.decoy-service.daemon.plist"
DAEMON_SOCKET_DIR="$HOME/.decoy-service"

echo "🔧 Setting up Decoy Service Daemon..."

# Create .decoy-service directory
mkdir -p "$DAEMON_SOCKET_DIR"
echo "✅ Created daemon directory: $DAEMON_SOCKET_DIR"

# Create LaunchAgents directory if it doesn't exist
mkdir -p "$LAUNCH_AGENTS_DIR"

# Prepare plist file with correct paths
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    echo "📱 Configuring for macOS..."
    
    # Replace placeholders in plist
    sed -e "s|{{DECOY_SERVICE_PATH}}|$SCRIPT_DIR|g" \
        -e "s|{{HOME}}|$HOME|g" \
        "$PLIST_FILE" > "$INSTALLED_PLIST"
    
    # Set correct permissions
    chmod 644 "$INSTALLED_PLIST"
    
    echo "✅ LaunchAgent installed to: $INSTALLED_PLIST"
    
    # Load the LaunchAgent
    echo "⚙️  Loading LaunchAgent..."
    launchctl unload "$INSTALLED_PLIST" 2>/dev/null || true
    launchctl load "$INSTALLED_PLIST"
    
    echo "✅ Daemon will auto-start on next boot"
    echo "✅ To start daemon now, run: launchctl load $INSTALLED_PLIST"

elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux (systemd)
    echo "🐧 Configuring for Linux..."
    
    SYSTEMD_DIR="$HOME/.config/systemd/user"
    SYSTEMD_SERVICE="$SYSTEMD_DIR/decoy-daemon.service"
    
    mkdir -p "$SYSTEMD_DIR"
    
    cat > "$SYSTEMD_SERVICE" << EOF
[Unit]
Description=Decoy Service Daemon
After=network.target

[Service]
Type=simple
ExecStart=/usr/bin/python3 $SCRIPT_DIR/daemon.py
WorkingDirectory=$SCRIPT_DIR
Restart=always
RestartSec=5

[Install]
WantedBy=default.target
EOF
    
    echo "✅ Systemd service installed to: $SYSTEMD_SERVICE"
    
    # Enable and start
    systemctl --user daemon-reload
    systemctl --user enable decoy-daemon.service
    systemctl --user start decoy-daemon.service
    
    echo "✅ Daemon will auto-start on next boot"
    echo "✅ To start daemon now, run: systemctl --user start decoy-daemon.service"

else
    echo "⚠️  Unsupported OS: $OSTYPE"
    echo "Manual setup required - see README"
    exit 1
fi

echo ""
echo "🎉 Daemon setup complete!"
echo ""
echo "Next steps:"
echo "1. Install dependencies: pip install -r requirements.txt"
echo "2. Install Playwright browsers: playwright install"
echo "3. Restart your computer (or manually start daemon)"
echo "4. Install Firefox extension from firefox-extension/"
echo ""
