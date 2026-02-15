# Firefox Extension - Quick Start

## 🚀 Setup (5 minutes)

### 1. Install API Dependencies
```bash
cd /Users/iot_lab/Documents/Automation/Decoy/Claude
pip install flask flask-cors
```

### 2. Start the API Server
```bash
python3 api_server.py
```

Keep this running! You'll see:
```
Starting Decoy Service API on http://localhost:9999
API endpoints:
  POST   /api/start       - Start the service
  POST   /api/stop        - Stop the service
  GET    /api/status      - Get service status
  ...
```

Optional (macOS daemon mode):
```bash
./daemonctl.sh install
./daemonctl.sh status
```

### 3. Load Extension in Firefox

1. Open Firefox
2. Press `Ctrl+Shift+A` (or `Cmd+Shift+A` on Mac) to open Add-ons
3. Click the ⚙️ gear icon → "Debug Add-ons"
4. Or go to: `about:debugging#/runtime/this-firefox`
5. Click "Load Temporary Add-on"
6. Navigate to: `/Users/iot_lab/Documents/Automation/Decoy/Claude/firefox-extension/`
7. Select `manifest.json`

✅ Done! You'll see the Decoy Service icon in your toolbar.

### 4. Create Extension Icons (Optional)

The extension needs 3 icon files. You can:

**Option A**: Use online favicon generator
- Go to: https://favicon-generator.org/
- Download as PNG (16x16, 48x48, 128x128)
- Save to `firefox-extension/icons/`

**Option B**: Create with Python
```bash
pip install pillow
python3 << 'EOF'
from PIL import Image, ImageDraw

for size in [16, 48, 128]:
    img = Image.new('RGB', (size, size), '#2563eb')
    draw = ImageDraw.Draw(img)
    draw.rectangle([(2, 2), (size-2, size-2)], outline='white', width=1)
    img.save(f'firefox-extension/icons/icon-{size}.png')
EOF
```

**Option C**: Skip icons for now (use as-is for testing)

## 📖 Usage

### Basic Controls
1. Click Decoy Service icon in Firefox toolbar
2. **Start Service** - Begin generating activity
3. **Stop Service** - Stop the service
4. Watch stats update in real-time

### View Settings
- Click the ⚙️ Settings button in the popup
- Customize intensity, intervals, categories, etc.
- Changes save automatically

### Monitor Activity
The popup shows:
- 🟢 Status indicator (green = running, red = stopped)
- ⏱️ Session timer
- 🌐 Sites visited
- 🖱️ Clicks made
- 🔍 Searches performed

## 🔧 Customization

### Change Activity Intensity
1. Click Settings ⚙️
2. Select "Low", "Medium", or "High"
3. Adjust click interval (2-20 seconds)
4. Adjust session duration (5-120 minutes)
5. Changes save automatically

### Select Website Categories
1. Open Settings
2. Check/uncheck categories:
   - News
   - Technology
   - Education
   - Entertainment
   - Lifestyle
3. Service will only visit checked categories

### Browser Settings
**Run in Headless Mode** (hidden browser - recommended)
**Rotate User Agents** (appear as different browsers)
**Enable Page Scrolling** (simulate reading)

## ⚠️ Common Issues

### "Cannot connect to server"
**Problem**: Extension shows "cannot connect" error
**Solution**: 
- Verify API server is running (see Step 2 above)
- Check server is on `localhost:9999`
- No firewall blocking localhost

### Icons don't show
**Problem**: Extension icon is missing or broken
**Solution**:
- Create PNG icon files (see Step 4 above)
- Or reload extension after creating icons
- Or temporarily ignore (works fine without icons)

### Service doesn't start
**Problem**: Start button does nothing
**Solution**:
1. Check API server console for errors
2. Open Firefox Developer Tools (F12)
3. Check Console tab for JavaScript errors
4. Try reloading the extension
5. Restart the API server

### Settings don't save
**Problem**: Settings revert when you reload
**Solution**:
- Check Firefox allows storage for the extension
- Try using a different browser profile
- Clear browser storage and reload

## 🎓 Architecture

```
User Interface
└── Firefox Extension Popup
    ├── popup.html (UI)
    ├── popup.js (Logic)
    └── background.js (Message handler)
        │
        └─→ HTTP Request
            │
            └─→ localhost:9999 (Flask API)
                │
                └─→ DecoyService (Python)
                    ├── Browser Agent (Selenium/Playwright)
                    ├── Activity Tracker
                    └── Statistics
```

## 📁 Extension Files

| File | Purpose |
|------|---------|
| `manifest.json` | Extension configuration |
| `popup.html` | Main UI (what user sees) |
| `popup.css` | Styling for popup |
| `popup.js` | Button click handlers |
| `background.js` | Message handling |
| `pages/options.html` | Settings page UI |
| `pages/options.js` | Settings logic |
| `icons/` | App icons (16x48x128px) |

## 🔐 Security Notes

✅ **Safe**:
- All communication is local (localhost:9999)
- No data sent to external servers
- Settings stored in browser only
- No telemetry or tracking

⚠️ **Important**:
- Keep API server on localhost only
- Don't expose port 9999 to internet
- Use firewall to block external access
- Only use for personal privacy protection

## 📚 More Information

- [Full Firefox Extension Guide](../FIREFOX_EXTENSION.md)
- [API Documentation](../GITHUB_DEPLOY.md)
- [Main README](../README.md)
- [Troubleshooting Guide](../TROUBLESHOOTING.md)

## 🆘 Getting Help

1. Check logs at: `decoy_service/logs/decoy_service.log`
2. Enable debug mode in extension settings
3. Check browser console (F12) for errors
4. Review API server output for HTTP errors
5. Read TROUBLESHOOTING.md for common issues

---

**Ready?** Start the API server and load the extension! 🚀
