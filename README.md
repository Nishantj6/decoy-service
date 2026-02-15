# Decoy Service

A privacy-enhancing tool that generates random browsing activity to confuse behavioral advertisers and profilers. By creating a "decoy" signal through automated visits to diverse websites and random searches, this service obscures your actual browsing interests and habits.

## How It Works

The Decoy Service:
- **Visits random websites** from various categories (news, tech, education, entertainment, etc.)
- **Performs random clicks** on page elements to simulate genuine user interaction
- **Conducts random searches** on search engines
- **Adds realistic delays** between actions to mimic human behavior
- **Rotates user agents** to appear as different browsers/devices
- **Generates confusing signals** to advertisers and tracking services

## Privacy Benefits

- **Behavioral Obfuscation**: Advertisers can't build accurate profiles of your interests
- **Click Fraud Prevention**: Prevents targeted ad targeting based on your real behavior
- **Tracking Confusion**: Makes tracking networks uncertain about your preferences
- **Signal Noise**: Adds noise to behavioral data collection

## Installation

### Prerequisites
- Python 3.8+
- Chrome/Chromium browser (for Selenium) OR Firefox/Chromium (for Playwright)

### Setup

1. Clone or download the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Download WebDriver:
   - For Selenium with Chrome: [ChromeDriver](https://chromedriver.chromium.org/)
   - For Playwright: `playwright install`

4. Copy configuration:
```bash
cp config/.env.example config/.env
```

## Configuration

Edit `config/settings.yaml` to customize behavior:

- **Activity timing**: Click intervals, page dwell time, session duration
- **Browser settings**: Headless mode, user agent rotation
- **Clicking behavior**: Number of clicks per page, scrolling enabled
- **Logging**: Log level, output files

Edit `config/websites.yaml` to customize:
- Website categories and URLs to visit
- Search queries to use
- Domain lists for various interests

## Usage

### Daemon Mode (Recommended - Auto-Start)

The daemon approach runs the service as a background process that auto-starts on system boot. This is ideal for continuous, hands-free operation.

**Setup:**

1. Install dependencies:
```bash
pip install -r decoy_service/requirements.txt
playwright install
```

2. Install and configure the daemon:
```bash
chmod +x setup-daemon.sh
./setup-daemon.sh
```

This will:
- Create the runtime directory at `~/.decoy-service/`
- Install a LaunchAgent (macOS) or systemd service (Linux)
- Configure auto-start on user login
- Start the daemon immediately

**Control the daemon:**

```bash
# Using the control script (macOS)
./daemonctl.sh install   # Install and start daemon
./daemonctl.sh start     # Start daemon
./daemonctl.sh stop      # Stop daemon
./daemonctl.sh restart   # Restart daemon
./daemonctl.sh status    # Check daemon status
./daemonctl.sh logs      # View daemon logs
./daemonctl.sh uninstall # Remove daemon

# On Linux with systemd
systemctl --user start decoy-daemon.service
systemctl --user stop decoy-daemon.service
systemctl --user status decoy-daemon.service
```

**Using the Python client:**

```python
from decoy_service.daemon_client import DaemonClient

client = DaemonClient()

# Start the service
result = client.start()
print(result)

# Check status
status = client.status()
print(status)

# Stop the service
result = client.stop()
print(result)
```

**Using the Firefox extension:**

Install the Firefox extension from the `firefox-extension/` directory to control the daemon via a browser popup UI.

**Note**: The daemon communicates via Unix domain socket at `~/.decoy-service/daemon.sock`. For Firefox extension compatibility, you'll also need to run `api_server.py` as a fallback HTTP bridge:
```bash
python3 api_server.py
```

See [DAEMON_APPROACH.md](DAEMON_APPROACH.md) for detailed architecture documentation.

---

### One-time Session (Manual Mode)

Run a single decoy session:
```bash
python decoy_service.py
```

Or with custom config directory:
```bash
python decoy_service.py /path/to/config
```

### Scheduled Sessions (Legacy)

Run decoy activity at regular intervals:
```bash
python scheduler.py
```

Edit `scheduler.py` to customize schedule. Example schedules:
```python
# Run every 3 hours for 15 minutes
scheduler.schedule_interval(minutes=180, duration_minutes=15)

# Run daily at 2 PM for 30 minutes
scheduler.schedule_daily(hour=14, minute=0, duration_minutes=30)

# Run every hour for 10 minutes
scheduler.schedule_hourly(minute=0, duration_minutes=10)
```

## Advanced Configuration

### Using Proxies

Add proxies to `config/settings.yaml`:
```yaml
requests:
  proxies:
    - "http://proxy1.example.com:8080"
    - "http://proxy2.example.com:8080"
```

### Custom Website Lists

Create themed website lists in `config/websites.yaml`:
```yaml
categories:
  my_category:
    - "https://example1.com"
    - "https://example2.com"
```

### Environment Variables

Create `.env` file in config directory for sensitive settings:
```
PROXY_LIST_FILE=/path/to/proxies.txt
DEBUG_MODE=false
```

## Logging

Logs are saved to `logs/decoy_service.log`

View real-time logs:
```bash
tail -f logs/decoy_service.log
```

Change log level in `settings.yaml`:
- `DEBUG`: Very detailed information
- `INFO`: General activity information
- `WARNING`: Only warnings and errors
- `ERROR`: Only errors

## Safety & Ethics

### Important Notes

- **Only use for your own browsing**: Don't use this to generate traffic for websites or services you don't own
- **Respect website ToS**: Many sites prohibit automated access; use appropriate delays and user agents
- **Legal compliance**: Ensure you comply with local laws regarding automation and privacy tools
- **Resource considerate**: Use reasonable scheduling to avoid overloading servers
- **Disclosure**: Be aware of CFAA and similar laws in your jurisdiction

### Best Practices

1. Use realistic delays between actions
2. Mix in legitimate manual browsing
3. Rotate proxies if using them
4. Monitor website responses and respect 429 (Too Many Requests) errors
5. Use headless mode to avoid visual distraction
6. Run during off-peak hours to reduce server load

## Architecture

```
decoy_service/
├── decoy_service.py      # Main service orchestrator
├── browser_agent.py      # Selenium/Playwright integration
├── scheduler.py          # Scheduling and daemon mode
├── utils.py              # Utilities and helpers
├── requirements.txt      # Python dependencies
├── config/
│   ├── settings.yaml     # Main configuration
│   ├── websites.yaml     # Website lists and queries
│   └── .env.example      # Environment variables template
└── logs/                 # Activity logs
```

## Browser Support

### Selenium (Recommended for compatibility)
- Chrome/Chromium
- Firefox
- Safari

### Playwright (Modern alternative)
- Chromium
- Firefox
- WebKit

Change browser in `config/settings.yaml`:
```yaml
browser:
  type: "playwright"  # or "selenium"
  headless: true
```

## Troubleshooting

### Chrome/ChromeDriver not found
```bash
# Install Chrome/Chromium via Homebrew (macOS)
brew install chromium

# Download ChromeDriver matching your Chrome version
# https://chromedriver.chromium.org/
```

### Playwright browser not installed
```bash
playwright install
```

### Connection refused errors
- Check website URLs are accessible
- Verify no firewall/proxy blocking
- Add reasonable delays between requests

### Too many clicks/interactions detected
- Increase `click_interval_min` and `click_interval_max`
- Decrease number of clicks per page
- Add random delays

## Performance Considerations

- **Memory**: Headless mode uses ~100-150MB per browser instance
- **CPU**: Moderate load; scheduling helps distribute impact
- **Network**: Consider bandwidth with large parallel sessions
- **Duration**: Sessions can run for hours; use scheduled approach for continuous operation

## Contributing & Customization

Extend the service by:

1. **Add custom website sources**:
   - Modify `config/websites.yaml`
   - Add API integrations in `utils.py`

2. **Create custom browser behaviors**:
   - Extend `BrowserAgent` class
   - Add new interaction methods

3. **Add analytics**:
   - Extend `ActivityTracker` class
   - Export stats to database/API

## Legal Disclaimer

This tool is provided for educational and privacy protection purposes. Users are responsible for:
- Complying with terms of service of visited websites
- Respecting robots.txt and legal automation restrictions
- Following applicable laws in their jurisdiction
- Ensuring ethical use

See LICENSE file for full terms.

## Related Tools

- **AdNauseam**: Browser extension that clicks ads to confuse profilers
- **Privacy Badger**: Blocks third-party tracking
- **uBlock Origin**: Ad and tracker blocker
- **Tor Browser**: Anonymous browsing

## License

MIT License - See LICENSE file for details
