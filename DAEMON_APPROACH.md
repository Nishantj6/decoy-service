# Decoy Service - Daemon Approach

> **Experimental Branch**: This branch implements a daemon-based architecture instead of the HTTP server approach.

## Overview

Instead of running a Flask HTTP server on port 9999, the daemon approach uses:
- **Unix Domain Sockets (IPC)** for communication between extension and service
- **Background daemon process** that auto-starts on system boot
- **No manual server launch** required for end users
- **Lightweight** - no HTTP overhead

## Architecture

```
Firefox Extension
       ↓
   IPC Socket
  (~/.decoy-service/daemon.sock)
       ↓
  Daemon Process (daemon.py)
       ↓
  Selenium/Playwright
       ↓
   Browser Automation
```

## Installation

### macOS

```bash
# 1. Install dependencies
pip install -r decoy_service/requirements.txt
playwright install

# 2. Setup daemon (auto-start on boot)
chmod +x setup-daemon.sh
./setup-daemon.sh

# 3. Restart or manually start
launchctl load ~/Library/LaunchAgents/com.decoy-service.daemon.plist

# 4. Load Firefox extension from firefox-extension/
```

### Linux (systemd)

```bash
# 1. Install dependencies
pip install -r decoy_service/requirements.txt
playwright install

# 2. Setup daemon
chmod +x setup-daemon.sh
./setup-daemon.sh

# 3. Start daemon
systemctl --user start decoy-daemon.service

# 4. Load Firefox extension
```

### Windows

Manual setup required - convert `setup-daemon.sh` to PowerShell script or use Task Scheduler

## How It Works

### Daemon Startup Flow

1. User installs Decoy Service
2. Runs `./setup-daemon.sh`
3. LaunchAgent/Systemd is configured
4. **Next system boot**: Daemon auto-starts
5. Firefox extension loads and connects to daemon socket

### Communication Flow

1. Extension sends JSON command via Unix socket:
   ```json
   {"command": "start"}
   ```

2. Daemon receives, processes, returns response:
   ```json
   {"success": true, "status": "running"}
   ```

3. Extension updates UI accordingly

## Commands

The daemon accepts these commands:

| Command | Description |
|---------|-------------|
| `start` | Start browsing service |
| `stop` | Stop browsing service |
| `status` | Get current status |
| `activity-log` | Get activity log |
| `shutdown` | Shutdown daemon |

## Testing Daemon

### Manual Testing

```bash
# Start daemon manually
python3 daemon.py &

# Test with client in another terminal
python3 -c "from decoy_service.daemon_client import DaemonClient; c = DaemonClient(); print(c.status())"
```

### Check Daemon Status

```bash
# macOS
launchctl list | grep decoy-service

# Linux
systemctl --user status decoy-daemon.service

# Check logs
tail -f ~/.decoy-service/daemon.log
```

### Stop Daemon

```bash
# macOS
launchctl unload ~/Library/LaunchAgents/com.decoy-service.daemon.plist

# Linux
systemctl --user stop decoy-daemon.service
```

## File Structure (Daemon Branch)

```
.
├── daemon.py                          # Main daemon process (NEW)
├── com.decoy-service.daemon.plist     # macOS LaunchAgent config (NEW)
├── setup-daemon.sh                    # Installation script (NEW)
├── decoy_service/
│   ├── daemon_client.py               # IPC client library (NEW)
│   ├── decoy_service.py
│   ├── browser_agent.py
│   └── ...
├── firefox-extension/                 # Needs update for IPC
└── ...
```

## Advantages vs HTTP Server

| Aspect | HTTP Server | Daemon + IPC |
|--------|-------------|--------------|
| **Manual launch** | Required | Not needed (auto-start) |
| **User experience** | Good | Better |
| **Port conflicts** | Possible | None |
| **Network overhead** | More | Less |
| **Debugging** | Easy (visible) | Medium (logs) |
| **Complexity** | Lower | Higher |
| **Security** | Good | Better (local only) |

## Known Issues / TODO

### Completed ✅
- [x] Socket timeout handling - Added 5s timeout in daemon_client.py
- [x] Fix plist log paths to use HOME directory
- [x] Fix working directory handling in daemon.py
- [x] Update documentation with daemon usage

### In Progress
- [ ] Update Firefox extension to use daemon_client instead of HTTP calls
  - Currently uses HTTP fallback due to browser sandbox limitations
  - Firefox extension requires both daemon.py and api_server.py running
- [ ] Test on Linux with systemd
- [ ] Test on Windows (need Task Scheduler script)

### Future Enhancements
- [ ] Add daemon restart/crash recovery
- [ ] Add daemon health checks
- [ ] Multi-user support
- [ ] Native messaging bridge for Firefox extension

### Known Deployment Issues

**macOS Documents Folder Permissions**

If the project is located in the Documents folder, LaunchAgent may fail with "Operation not permitted" due to macOS security protections.

**Solutions**:
1. Move project to `/usr/local/decoy-service/` or `~/Applications/`
2. Use Homebrew Python instead of system Python
3. Grant Full Disk Access (not recommended for security)

See README Troubleshooting section for detailed instructions.

## Comparing Branches

```bash
# Switch to HTTP server version
git checkout main

# Switch back to daemon version
git checkout daemon-approach

# See differences
git diff main daemon-approach
```

## Questions?

This is an experimental branch. Use `main` for the stable HTTP server version.
