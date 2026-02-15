# Firefox Extension Guide

A complete Firefox extension for controlling the Decoy Service directly from your browser!

## Features

✨ **Simple Toggle Interface**
- One-click enable/disable of decoy service
- Real-time status indicator
- Activity statistics display

⚙️ **Customizable Settings**
- Activity intensity (low, medium, high)
- Click intervals and session duration
- Browser behavior (headless, user agents)
- Website categories and preferences

📊 **Live Monitoring**
- Session timer
- Sites visited counter
- Clicks made tracker
- Search queries performed

🚀 **Quick Access**
- Extension popup in toolbar
- Settings page for advanced configuration
- Documentation links

## Installation

### Step 1: Load Extension in Firefox

1. Open Firefox
2. Go to `about:debugging#/runtime/this-firefox`
3. Click "Load Temporary Add-on"
4. Navigate to `/firefox-extension/` folder
5. Select `manifest.json`

Your extension will now appear in Firefox toolbar!

### Step 2: Start the API Server

The extension needs the Python API server to control the service:

```bash
cd /Users/iot_lab/Documents/Automation/Decoy/Claude

# Install Flask dependency
pip install flask flask-cors

# Start the API server
python3 api_server.py
```

The server will run on `http://localhost:9999`

Optional (macOS daemon mode):
```bash
./daemonctl.sh install
./daemonctl.sh status
```

### Step 3: Use the Extension

1. Click the Decoy Service icon in Firefox toolbar
2. Click "Start Service" button
3. Watch the activity statistics update in real-time
4. Click "Stop Service" when done

## Extension Files

```
firefox-extension/
├── manifest.json           # Extension configuration
├── popup.html             # Main popup interface
├── popup.css              # Popup styling
├── popup.js               # Popup logic
├── background.js          # Background worker
│
├── pages/
│   ├── options.html       # Settings page
│   ├── options.css        # Settings styling
│   └── options.js         # Settings logic
│
└── icons/                 # Extension icons
    ├── icon-16.png
    ├── icon-48.png
    └── icon-128.png
```

## How It Works

### Architecture Flow

```
Firefox Extension UI
        ↓
    popup.html (User sees this)
        ↓
    popup.js (Handles clicks)
        ↓
    chrome.runtime.sendMessage()
        ↓
    background.js (Listens for messages)
        ↓
    HTTP Request to localhost:9999
        ↓
    api_server.py (Python Flask server)
        ↓
    DecoyService (Python service)
        ↓
    Browser Automation (visits sites, clicks, etc)
```

### Communication Flow

1. **User clicks Start** in popup
2. Popup sends message to background script
3. Background script makes HTTP request to Python API
4. API server starts DecoyService
5. Service runs in background visiting random sites
6. Extension displays live stats from API
7. User can stop anytime with Stop button

## Settings

### Activity Settings

**Intensity**: Controls how aggressive the clicking is
- **Low**: 1-2 clicks per page (subtle)
- **Medium**: 3-5 clicks per page (balanced)
- **High**: 6-10 clicks per page (aggressive)

**Click Interval**: Time between actions (1-20 seconds)
- Shorter = more aggressive
- Longer = more human-like

**Session Duration**: How long to run (5-120 minutes)
- 0 = Run indefinitely
- Set a limit to save resources

### Browser Settings

**Headless Mode**: Run browser hidden (recommended)

**Rotate User Agents**: Switch between different browser identities

**Page Scrolling**: Simulate reading pages

### Content Preferences

Select which website categories to visit:
- News
- Technology
- Education
- Entertainment
- Lifestyle

### Advanced

**Auto-start**: Automatically start service when Firefox launches

**Log Level**: Control verbosity
- Error: Only show problems
- Warning: Show warnings too
- Info: Standard information
- Debug: Very detailed (for troubleshooting)

## API Endpoints

The extension communicates with these endpoints:

### POST /api/start
Start the decoy service
```bash
curl -X POST http://localhost:9999/api/start
```

### POST /api/stop
Stop the service
```bash
curl -X POST http://localhost:9999/api/stop
```

### GET /api/status
Get current status and statistics
```bash
curl http://localhost:9999/api/status
```

### GET /api/config
Get current configuration
```bash
curl http://localhost:9999/api/config
```

### POST /api/config
Update configuration
```bash
curl -X POST http://localhost:9999/api/config \
  -H "Content-Type: application/json" \
  -d '{"intensity": "high"}'
```

### POST /api/schedule
Schedule service at intervals
```bash
curl -X POST http://localhost:9999/api/schedule \
  -H "Content-Type: application/json" \
  -d '{"interval": 180, "duration": 15}'
```

### GET /api/health
Health check
```bash
curl http://localhost:9999/api/health
```

## Troubleshooting

### "Popup not responding"
- Check if API server is running: `python3 api_server.py`
- Verify localhost:9999 is accessible
- Check browser console for errors (F12)

### "Cannot connect to server"
- API server not running
- Wrong port (should be 9999)
- Firewall blocking localhost

### Service doesn't start
- Ensure all Python dependencies are installed
- Check that ChromeDriver is available
- Look at logs in `decoy_service/logs/`

### Stats not updating
- API server may be slow
- Try stopping and restarting service
- Check network tab in DevTools (F12)

## Development

### Modify the Popup

Edit `popup.html` to change the UI
Edit `popup.css` to change styling
Edit `popup.js` to change behavior

### Add New API Endpoints

Edit `api_server.py` to add routes

### Create Icons

Create 16x16, 48x48, 128x128 PNG files and place in `icons/`

### Debug the Extension

1. Open Firefox DevTools (F12)
2. Go to Storage > Extensions
3. Look for stored settings
4. Check Console tab for errors

## Future Enhancements

Possible improvements:
- [ ] Notifications when service starts/stops
- [ ] Multiple profiles/schedules
- [ ] Activity history and analytics
- [ ] Website blacklist/whitelist
- [ ] Proxy rotation
- [ ] Cloud sync settings
- [ ] Statistics export

## Safety & Privacy

✅ **What this extension does:**
- Communicates with local Python service only
- No data sent to external servers
- Stores settings locally in browser
- Uses CORS for secure API access

⚠️ **Important Notes:**
- Keep API server running on localhost only
- Don't expose port 9999 to the internet
- Only use for personal privacy protection
- Respect website terms of service

## Support

For issues:
1. Check logs at `decoy_service/logs/decoy_service.log`
2. Enable debug mode in extension settings
3. Check API server console for errors
4. Review documentation in main README.md
