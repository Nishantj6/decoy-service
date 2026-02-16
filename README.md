# Decoy Service

A privacy tool that generates random browsing activity to confuse advertisers and trackers. It visits random websites, performs searches, and clicks on pages — creating noise that makes it impossible to build an accurate profile of your real browsing habits.

## What It Does

- Visits random websites across categories (news, tech, education, shopping, etc.)
- Performs random searches on search engines
- Clicks on page elements to simulate real user behavior
- Adds realistic delays between actions to mimic human browsing
- Runs silently in the background with no interaction needed

## Quick Start

### 1. Clone and install

```bash
git clone https://github.com/Nishantj6/decoy-service.git
cd decoy-service
chmod +x install.sh
./install.sh
```

This single command:
- Creates a Python virtual environment and installs dependencies
- Copies daemon files to a safe system location
- Installs an auto-start service (LaunchAgent on macOS, systemd on Linux)
- Starts the daemon immediately

### 2. Install the Firefox extension

Open `firefox-extension/dist/signed/decoy-service-1.1.0-signed.xpi` in Firefox:

- **Double-click** the `.xpi` file, or
- **Drag and drop** it into a Firefox window, or
- In Firefox: `about:addons` → gear icon → **Install Add-on From File** → select the `.xpi`

Click **Add** when Firefox prompts you. The extension is now permanently installed and survives Firefox restarts.

### 3. Start

Click the Decoy Service icon in the Firefox toolbar and press **Start**.

That's it. The daemon runs automatically on every boot. The extension stays installed permanently.

## How It Works

```
Firefox Extension (popup UI)
        │
        │ HTTP (localhost:9999)
        ▼
   Python Daemon (auto-starts on boot)
        │
        ▼
   DecoyService (headless browser automation)
        │
        ▼
   Random websites, searches, clicks
```

The Python daemon runs as a background service that starts automatically when you log in. The Firefox extension is just a control panel — it sends start/stop commands to the daemon over HTTP.

## Configuration

Edit `decoy_service/config/settings.yaml` to customize:

- **Session duration** — how long each decoy session runs
- **Click intervals** — time between actions
- **Headless mode** — run browser visibly or in background
- **User agent rotation** — appear as different browsers

Edit `decoy_service/config/websites.yaml` to customize:

- Website categories and URLs to visit
- Search queries to use

## Troubleshooting

### Extension shows "network error failed to fetch"

The daemon isn't running. Fix it:

```bash
# Check if daemon is running
launchctl list | grep decoy    # macOS
systemctl --user status decoy-daemon    # Linux

# Reinstall (fixes most issues)
./install.sh
```

### Check daemon logs

```bash
tail -f ~/.decoy-service/daemon-stderr.log
```

### Manually restart the daemon

```bash
# macOS
launchctl unload ~/Library/LaunchAgents/com.decoy-service.daemon.plist
launchctl load ~/Library/LaunchAgents/com.decoy-service.daemon.plist

# Linux
systemctl --user restart decoy-daemon
```

### Uninstall

```bash
# macOS
launchctl unload ~/Library/LaunchAgents/com.decoy-service.daemon.plist
rm ~/Library/LaunchAgents/com.decoy-service.daemon.plist
rm -rf ~/.decoy-service

# Linux
systemctl --user stop decoy-daemon
systemctl --user disable decoy-daemon
rm ~/.config/systemd/user/decoy-daemon.service
rm -rf ~/.decoy-service
```

## Project Structure

```
├── install.sh                  # One-command installer (run this first)
├── daemon.py                   # Background daemon with HTTP API
├── requirements.txt            # Python dependencies
├── decoy_service/
│   ├── decoy_service.py        # Main service orchestrator
│   ├── browser_agent.py        # Browser automation (Selenium)
│   ├── utils.py                # Activity tracking & utilities
│   └── config/
│       ├── settings.yaml       # Behavior settings
│       └── websites.yaml       # Website & search lists
└── firefox-extension/
    ├── manifest.json           # Extension manifest
    ├── popup.html/js/css       # Extension popup UI
    ├── background.js           # Background daemon communication
    ├── daemon-client.js        # API client
    └── dist/signed/
        └── decoy-service-1.1.0-signed.xpi  # Signed extension (install this)
```

## Legal Disclaimer

This tool is for personal privacy protection. Users are responsible for complying with applicable laws and website terms of service.

## License

MIT License — see LICENSE file for details.
