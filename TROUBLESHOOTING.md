# Troubleshooting Guide

## Installation Issues

### "pip: command not found"
**Solution**: Install Python or use `python3 -m pip`
```bash
# Check Python version
python3 --version

# Use python3 instead
python3 -m pip install -r requirements.txt
```

### "ModuleNotFoundError: No module named 'selenium'"
**Solution**: Install requirements
```bash
pip install -r decoy_service/requirements.txt
```

### "ModuleNotFoundError: No module named 'playwright'"
**Solution**: Install Playwright and browsers
```bash
pip install playwright
playwright install
```

---

## Browser Issues

### "Chrome not found" or "chromedriver not found"

**For Selenium with Chrome:**
```bash
# macOS
brew install chromium

# Then download ChromeDriver matching your Chrome version:
# https://chromedriver.chromium.org/

# Check Chrome version
/Applications/Chromium.app/Contents/MacOS/Chromium --version

# Verify ChromeDriver works
chromedriver --version
```

**For Playwright (recommended):**
```bash
playwright install
# Change browser type in config/settings.yaml to "playwright"
```

### Browser window not appearing

This is normal! The browser runs in **headless mode** by default (hidden).

To see it, edit `config/settings.yaml`:
```yaml
browser:
  headless: false  # Set to false to see browser window
```

### "Timeout waiting for element"

Website takes too long to load. Increase timeout:
```yaml
# In config/settings.yaml
browser:
  timeout: 30  # Increase from default 10
```

---

## Website Access Issues

### "Connection refused" or "Connection timed out"

Website is unreachable. Solutions:
```yaml
# 1. Check internet connection
ping google.com

# 2. Website might be down - try other sites
# 3. Website might block automated access
# 4. Add different websites to config/websites.yaml
```

### "403 Forbidden" errors

Website blocks automated access. Solution:
- Remove that website from `config/websites.yaml`
- Add different websites instead
- Some sites like LinkedIn actively block automation

### Website not loading elements properly

Some dynamic websites need JavaScript to load content.
Use Playwright instead of Selenium:
```yaml
# In config/settings.yaml
browser:
  type: "playwright"
```

---

## Performance Issues

### "Too many requests" errors

Website is detecting automated traffic. Solutions:
```yaml
# In config/settings.yaml
activity:
  click_interval_min: 5  # Increase delays
  click_interval_max: 15
  requests_per_hour: 10  # Reduce request rate

clicking:
  clicks_per_page_max: 2  # Fewer clicks
```

### Browser using too much memory

Multiple browser instances or long sessions. Solutions:
```yaml
service:
  parallel_agents: 1  # Only 1 browser at a time
  session_duration: 30  # Limit to 30 minutes
```

Then restart periodically:
```bash
python scheduler.py  # Will restart sessions automatically
```

### High CPU usage

Reduce activity and increase delays:
```yaml
activity:
  click_interval_min: 10
  click_interval_max: 30
  page_dwell_min: 10

clicking:
  clicks_per_page_max: 1
  enable_scrolling: false
```

---

## Configuration Issues

### "No such file or directory: config/settings.yaml"

Make sure you're in the right directory:
```bash
cd /Users/iot_lab/Documents/Automation/Decoy/Claude
python decoy_service/decoy_service.py
```

Or provide config path:
```bash
python decoy_service/decoy_service.py config
```

### Invalid YAML syntax error

YAML is whitespace-sensitive. Check:
- Use spaces, not tabs
- Consistent indentation (2 spaces per level)
- Colons followed by spaces

**Wrong:**
```yaml
browser:
	headless: true  # TAB instead of space
```

**Correct:**
```yaml
browser:
  headless: true  # 2 spaces
```

### Settings not taking effect

1. Make sure you edited the correct file
2. YAML syntax errors prevent loading
3. Service must be restarted
4. Check logs for errors

```bash
tail -f logs/decoy_service.log
# Look for "Loaded config" or "Error loading"
```

---

## Logging Issues

### "Permission denied: logs/decoy_service.log"

Fix directory permissions:
```bash
chmod 755 logs/
touch logs/decoy_service.log
chmod 644 logs/decoy_service.log
```

Or create logs directory:
```bash
mkdir -p logs
```

### Not seeing log output

1. Check logging is enabled:
```yaml
logging:
  level: "INFO"  # Not ERROR
```

2. Check log file location:
```bash
ls -la logs/
```

3. Increase log level:
```yaml
logging:
  level: "DEBUG"  # More verbose
```

4. View logs in real-time:
```bash
tail -f logs/decoy_service.log
```

---

## Scheduling Issues

### Scheduler not running sessions

1. Check if scheduler is still running:
```bash
ps aux | grep scheduler
```

2. Edit `scheduler.py` to add schedule:
```python
def main():
    scheduler = DecoyScheduler('config', logger)
    scheduler.schedule_interval(minutes=180, duration_minutes=15)
    scheduler.start()
```

3. Run again:
```bash
python decoy_service/scheduler.py
```

### Sessions starting at wrong time

Check system time:
```bash
date
```

Scheduling uses system time. If off, fix system time or adjust schedule:
```python
# Currently scheduled at 2 PM
scheduler.schedule_daily(hour=14, minute=0, duration_minutes=30)

# Change to different time
scheduler.schedule_daily(hour=9, minute=0, duration_minutes=30)  # 9 AM instead
```

---

## Activity Issues

### Not visiting enough websites

Increase activity in settings:
```yaml
activity:
  click_interval_min: 1  # Shorter waits
  click_interval_max: 3
  requests_per_hour: 50  # More requests
```

### Too many clicks detected

Reduce clicking:
```yaml
clicking:
  clicks_per_page_min: 1
  clicks_per_page_max: 2

activity:
  click_interval_min: 10  # Longer delays
```

### Search queries not working

Some search engines require:
1. Accepting cookies first
2. JavaScript enabled
3. Matching CSS selectors

Try switching search engines or:
```yaml
clicking:
  enable_form_interaction: true  # Might need enabling
```

---

## Mac-Specific Issues

### "ChromeDriver cannot be opened because the developer cannot be verified"

```bash
# Allow it to run
xattr -d com.apple.quarantine /path/to/chromedriver

# Or download from official source
# https://chromedriver.chromium.org/
```

### "Permission denied" for setup.sh

```bash
chmod +x setup.sh
./setup.sh
```

---

## Linux-Specific Issues

### "No DISPLAY" error

You're on a headless server. Use headless mode (already default):
```yaml
browser:
  headless: true
```

Or use Playwright with no display:
```bash
pip install playwright
playwright install
```

### Missing dependencies

Install required libraries:
```bash
# Debian/Ubuntu
sudo apt-get install -y \
  python3 python3-pip \
  chromium-browser \
  libatk-bridge2.0-0 \
  libgconf-2-4 \
  libxss1

# Red Hat/CentOS
sudo yum install -y \
  python3 python3-pip \
  chromium \
  atk \
  at-spi2-atk
```

---

## Windows-Specific Issues

### "python" command not found

Use `python3` instead or add Python to PATH:
```cmd
python3 -m pip install -r requirements.txt
python3 decoy_service/decoy_service.py
```

### File path issues

Use forward slashes or double backslashes:
```yaml
# In config/settings.yaml
logging:
  log_file: "logs/decoy_service.log"  # OK
  # OR
  log_file: "logs\\decoy_service.log"  # Also OK
```

### Antivirus blocks ChromeDriver

Temporarily disable antivirus or add to exceptions, then:
```bash
pip install playwright
# Use Playwright instead
```

---

## Debugging Tips

### Enable debug logging

```yaml
# In config/settings.yaml
logging:
  level: "DEBUG"  # Maximum verbosity
```

Then check logs:
```bash
tail -f logs/decoy_service.log
```

### Test with visible browser

```yaml
# In config/settings.yaml
browser:
  headless: false  # See what's happening
```

### Test single website

Edit `examples.py` or create test script:
```python
from decoy_service import DecoyService

service = DecoyService('config')
service.agent = create_agent(service.logger, service.settings)
service.agent.open_browser()
service.agent.visit_url("https://example.com")
service.agent.random_click()
service.agent.close_browser()
```

### Check configuration is loaded

```bash
python -c "
from decoy_service import DecoyService
s = DecoyService('config')
print('Settings:', s.settings)
print('Websites:', s.websites_config)
"
```

---

## Getting More Help

1. **Check logs**: `tail -f logs/decoy_service.log`
2. **Enable debug**: Set `logging.level: DEBUG` in settings
3. **Run visible**: Set `browser.headless: false` in settings
4. **Read README**: Full documentation in README.md
5. **Check examples**: Code examples in examples.py

## Common Error Messages

| Error | Cause | Solution |
|-------|-------|----------|
| `ModuleNotFoundError` | Missing dependency | `pip install -r requirements.txt` |
| `Connection refused` | Website down or blocked | Remove from config, try others |
| `Timeout` | Website too slow | Increase timeout in settings |
| `Permission denied` | File permissions | `chmod 755 logs/` |
| `YAML error` | Invalid YAML syntax | Check indentation (spaces not tabs) |
| `ChromeDriver not found` | Driver not installed | Download from chromedriver.org |
| `Too many requests` | Rate limiting | Increase delays in settings |

---

Still having issues? Check the full README.md or create a minimal test case to debug.
