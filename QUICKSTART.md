# Quick Start Guide

## Installation (5 minutes)

### 1. Install Python Dependencies
```bash
cd decoy_service
pip install -r requirements.txt
```

### 2. Install Browser Driver
Choose one option:

**Option A: Chrome/Selenium (Recommended)**
```bash
# macOS
brew install chromium

# Then download ChromeDriver matching your Chrome version
# https://chromedriver.chromium.org/
# Place it in your PATH or decoy_service directory
```

**Option B: Playwright**
```bash
playwright install
```

### 3. First Run
```bash
python decoy_service.py
```

The browser will open and start generating decoy activity!

## Configuration Quickstart

### Edit Website Lists
Open `config/websites.yaml` and add your own websites:
```yaml
categories:
  my_interests:
    - "https://example1.com"
    - "https://example2.com"
```

### Customize Behavior
Edit `config/settings.yaml`:
- Change `clicks_per_page_max` for more/fewer clicks
- Adjust `page_dwell_min/max` for longer/shorter page views
- Set `headless: false` to see the browser in action
- Change `session_duration` to limit how long it runs

## Common Tasks

### Run Continuously Every 3 Hours
Edit `decoy_service/scheduler.py`, find the `main()` function, and use:
```python
scheduler.schedule_interval(minutes=180, duration_minutes=15)
```

Then run:
```bash
python decoy_service/scheduler.py
```

### Run in Headless Mode (Hidden)
```yaml
# In config/settings.yaml
browser:
  headless: true  # True = hidden, False = visible
```

### Increase Activity Intensity
```yaml
activity:
  requests_per_hour: 50  # More requests
  
clicking:
  clicks_per_page_min: 3
  clicks_per_page_max: 10  # More clicks
```

### Check What's Happening
```bash
# View live logs
tail -f logs/decoy_service.log

# Increase logging detail
# In config/settings.yaml, set: level: "DEBUG"
```

### Run API Server as a macOS Daemon (for Firefox Extension)
```bash
# From project root
./daemonctl.sh install

# Verify daemon + API health
./daemonctl.sh status

# View daemon logs
./daemonctl.sh logs
```

The extension API is available at `http://localhost:9999`.

## What It Does

1. **Opens a browser** in headless mode
2. **Visits random websites** from your configured list
3. **Clicks randomly** on page elements
4. **Scrolls pages** to simulate reading
5. **Performs searches** on search engines
6. **Waits with random delays** to appear human-like
7. **Logs all activity** to see what happened

## Privacy Benefits

- ✅ Confuses behavioral tracking
- ✅ Pollutes advertising profiles
- ✅ Adds noise to profiling data
- ✅ Makes targeted ads less accurate
- ✅ Helps prevent filter bubbles

## Next Steps

1. **Customize websites**: Edit `config/websites.yaml`
2. **Adjust timing**: Edit `config/settings.yaml`
3. **Schedule sessions**: Use `scheduler.py` for regular runs
4. **Monitor logs**: Watch `logs/decoy_service.log`

## Troubleshooting

**"Chrome not found"**
- Install Chromium: `brew install chromium`
- Or set Chrome path in `settings.yaml`

**"Too many requests detected"**
- Increase delays in `settings.yaml`
- Reduce `requests_per_hour`

**"Website not loading"**
- Check internet connection
- Website might block automated access
- Try adding different websites

**See logs for more details:**
```bash
tail -f logs/decoy_service.log
```

## Important Notes

- ⚠️ **Legal**: Use responsibly and within laws of your jurisdiction
- ⚠️ **Ethics**: Don't use for malicious purposes (DDoS, fraud, etc.)
- ⚠️ **Respect**: Follow website terms of service
- ⚠️ **Reasonable**: Use realistic delays, don't overload servers

## Need Help?

1. Check `logs/decoy_service.log` for errors
2. Read full documentation in `README.md`
3. Look at examples in `decoy_service/examples.py`
4. Increase logging level to DEBUG

Happy privacy protecting! 🔒
