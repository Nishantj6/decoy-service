# Decoy Service - Reference Card

## 📋 File Reference

| File | Purpose | Lines |
|------|---------|-------|
| `decoy_service.py` | Main service orchestrator | ~520 |
| `browser_agent.py` | Selenium & Playwright wrappers | ~390 |
| `scheduler.py` | Schedule recurring sessions | ~180 |
| `utils.py` | Logging, config, tracking | ~340 |
| `examples.py` | Usage examples | ~250 |

## 🎮 Command Reference

```bash
# One-time session
python decoy_service/decoy_service.py

# Scheduled sessions (background)
python decoy_service/scheduler.py

# Run examples
python decoy_service/examples.py 1    # Simple session
python decoy_service/examples.py 2    # Scheduled
python decoy_service/examples.py 3    # Custom config
python decoy_service/examples.py 4    # Tracking
python decoy_service/examples.py 5    # Headless mode

# Watch logs
tail -f logs/decoy_service.log

# Setup (one time)
bash setup.sh
```

## ⚙️ Configuration Quick Reference

### settings.yaml - Activity Timing
```yaml
activity:
  click_interval_min: 2          # Seconds between actions
  click_interval_max: 8
  page_dwell_min: 5              # Seconds on each page
  page_dwell_max: 30
  session_duration: 0            # 0 = infinite
```

### settings.yaml - Clicking Behavior
```yaml
clicking:
  clicks_per_page_min: 1
  clicks_per_page_max: 5
  enable_scrolling: true
  enable_form_interaction: false
```

### settings.yaml - Browser
```yaml
browser:
  type: "chrome"                 # chrome, firefox, safari, playwright
  headless: true                 # true = hidden, false = visible
  rotate_user_agents: true
```

### settings.yaml - Logging
```yaml
logging:
  level: "INFO"                  # DEBUG, INFO, WARNING, ERROR
  log_file: "logs/decoy_service.log"
```

## 🌐 websites.yaml Structure

```yaml
categories:
  news:
    - "https://news.ycombinator.com"
    - "https://bbc.com"
    # Add more...
    
  tech:
    - "https://github.com"
    # Add more...
    
search_queries:
  - "machine learning trends"
  - "privacy protection"
  # Add more...
```

## 🔑 Key Classes

### DecoyService
```python
service = DecoyService('config')
service.start_session()
service.tracker.print_summary()
```

### DecoyScheduler
```python
scheduler = DecoyScheduler('config', logger)
scheduler.schedule_interval(minutes=180, duration_minutes=15)
scheduler.start()
scheduler.stop()
```

### Browser Agents
```python
from browser_agent import create_agent
agent = create_agent(logger, config)
agent.open_browser()
agent.visit_url("https://example.com")
agent.random_click()
agent.scroll_page(500)
agent.close_browser()
```

### Activity Tracker
```python
tracker.record_website_visit(url)
tracker.record_click("element description")
tracker.record_search("query")
summary = tracker.get_summary()
tracker.print_summary()
```

## 🎯 Common Tweaks

### More Aggressive
```yaml
# settings.yaml
activity:
  click_interval_min: 1
  click_interval_max: 4
  requests_per_hour: 100
clicking:
  clicks_per_page_max: 10
```

### More Subtle
```yaml
# settings.yaml
activity:
  click_interval_min: 5
  click_interval_max: 15
  requests_per_hour: 10
clicking:
  clicks_per_page_max: 2
```

### Headless (Background)
```yaml
# settings.yaml
browser:
  headless: true
logging:
  level: "WARNING"
```

### Debug Mode
```yaml
# settings.yaml
browser:
  headless: false
logging:
  level: "DEBUG"
```

## 🔍 Log Levels

| Level | Use Case | Examples |
|-------|----------|----------|
| `DEBUG` | Detailed troubleshooting | Click events, element details |
| `INFO` | General activity | Sites visited, searches performed |
| `WARNING` | Potential issues | Failed connections, missing elements |
| `ERROR` | Problems | Browser crashes, config errors |

View logs:
```bash
tail -f logs/decoy_service.log
grep "ERROR" logs/decoy_service.log
grep "Visited" logs/decoy_service.log
```

## 📊 Metrics

After a session, check:
```
session_duration_minutes: Total time
websites_visited: Number of sites
total_clicks: Total clicks made
search_queries: Number of searches
forms_filled: Number of forms
```

Calculate your own:
- Clicks per minute = total_clicks / duration
- Sites per hour = (websites_visited / duration) * 60
- Avg. dwell time = duration / websites_visited

## 🚨 Common Issues

| Problem | Solution |
|---------|----------|
| Chrome not found | `brew install chromium` |
| ChromeDriver mismatch | Download matching version |
| Playwright not installed | `playwright install` |
| Timeout errors | Increase `browser.timeout` in settings |
| Too many requests detected | Increase `click_interval_min/max` |
| Website blocks access | Add different websites to config |
| Permission denied on logs | Check `logs/` directory permissions |

## 📚 Documentation

- **README.md** - Full documentation and architecture
- **QUICKSTART.md** - 5-minute setup guide
- **examples.py** - Code examples
- **BUILD_SUMMARY.md** - What was built
- **STRUCTURE.md** - File organization

## 🔐 Security & Ethics

✅ **Safe to use for:**
- Personal privacy protection
- Preventing ad targeting
- Research and testing

❌ **NOT safe for:**
- DDoS attacks or abuse
- Fraud or malicious activity
- Unauthorized automation

⚠️ **Always:**
- Use reasonable delays
- Follow website ToS
- Respect robots.txt
- Comply with local laws

## 💡 Tips & Tricks

1. **Mix with manual browsing** - Combine with real browsing for better results
2. **Use proxies** - Add proxy rotation for better anonymity
3. **Customize websites** - Add sites you actually read
4. **Monitor logs** - Check what the service is doing
5. **Test first** - Run with headless=false to see behavior
6. **Schedule wisely** - Off-peak hours are more respectful
7. **Start slow** - Begin with conservative settings

## 📞 Support

1. Check logs: `tail -f logs/decoy_service.log`
2. Read README.md for detailed info
3. Look at examples.py for code patterns
4. Set `logging.level: DEBUG` for detailed output
5. Run with `headless: false` to see what's happening

---

Last updated: February 15, 2026
Version: 1.0.0
