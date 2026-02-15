# 📖 Decoy Service - Complete Index

## 🎯 Start Here

1. **[START_HERE.txt](START_HERE.txt)** - Visual summary with commands
2. **[QUICKSTART.md](QUICKSTART.md)** - 5-minute setup guide
3. **[README.md](README.md)** - Full documentation

## 📚 Documentation

| File | Purpose | Read When |
|------|---------|-----------|
| [QUICKSTART.md](QUICKSTART.md) | 5-minute setup & common tasks | First time setup |
| [README.md](README.md) | Complete documentation & guide | Need detailed info |
| [REFERENCE.md](REFERENCE.md) | Command/config quick reference | Need quick lookup |
| [STRUCTURE.md](STRUCTURE.md) | File organization guide | Need to understand structure |
| [BUILD_SUMMARY.md](BUILD_SUMMARY.md) | What was built & features | Want overview of project |
| [TROUBLESHOOTING.md](TROUBLESHOOTING.md) | Common issues & solutions | Having problems |

## 🛠️ Core Service Code

### Main Service
- **[decoy_service/decoy_service.py](decoy_service/decoy_service.py)** - Main orchestrator (520 lines)
  - `DecoyService` class - Coordinates all activity
  - Activity generation (website visits, clicks, searches)
  - Session management

### Browser Automation  
- **[decoy_service/browser_agent.py](decoy_service/browser_agent.py)** - Browser control (390 lines)
  - `BrowserAgent` - Abstract base class
  - `SeleniumAgent` - Selenium WebDriver implementation
  - `PlaywrightAgent` - Playwright implementation
  - Website navigation, clicking, scrolling, form filling

### Scheduling
- **[decoy_service/scheduler.py](decoy_service/scheduler.py)** - Background scheduling (180 lines)
  - `DecoyScheduler` class
  - Schedule sessions hourly, daily, or at intervals
  - Background daemon mode

### Utilities
- **[decoy_service/utils.py](decoy_service/utils.py)** - Helper functions (340 lines)
  - `Logger` - Logging setup
  - `ConfigManager` - Load YAML configs
  - `ActivityTracker` - Track and report activity
  - `RandomnessGenerator` - Generate realistic randomness

### Examples
- **[decoy_service/examples.py](decoy_service/examples.py)** - Usage examples (250 lines)
  - Simple one-time session
  - Scheduled sessions
  - Custom configuration
  - Activity tracking
  - Background mode

### Package Init
- **[decoy_service/__init__.py](decoy_service/__init__.py)** - Package initialization
  - Module exports
  - Version info

## ⚙️ Configuration Files

### Settings
- **[decoy_service/config/settings.yaml](decoy_service/config/settings.yaml)** - Behavior settings
  - Browser configuration (type, headless, user-agents)
  - Activity timing (click intervals, dwell time)
  - Clicking behavior (number of clicks, scrolling)
  - Request patterns (proxies, randomization)
  - Logging configuration

### Websites
- **[decoy_service/config/websites.yaml](decoy_service/config/websites.yaml)** - Content lists
  - Website categories (news, tech, education, entertainment, lifestyle)
  - Search queries
  - Fully customizable

### Environment
- **[decoy_service/config/.env.example](decoy_service/config/.env.example)** - Environment template
  - Proxy settings
  - Browser settings
  - API endpoints
  - Feature flags

## 📋 Dependencies & Setup

- **[decoy_service/requirements.txt](decoy_service/requirements.txt)** - Python dependencies
  - selenium (4.15+)
  - playwright (1.40+)
  - pyyaml (6.0+)
  - requests, beautifulsoup4, schedule, faker, python-dotenv

- **[setup.sh](setup.sh)** - Automated setup script
  - Creates virtual environment
  - Installs dependencies
  - Sets up configuration

## 📄 License & Meta

- **[LICENSE](LICENSE)** - MIT License with disclaimer
- **[INDEX.md](INDEX.md)** - This file

## 🗂️ Full Directory Structure

```
Claude/
├── INDEX.md                          ← You are here
├── START_HERE.txt                    ← Visual summary
├── QUICKSTART.md                     ← 5-min setup
├── README.md                         ← Full docs
├── REFERENCE.md                      ← Quick reference
├── STRUCTURE.md                      ← File organization
├── BUILD_SUMMARY.md                  ← What was built
├── TROUBLESHOOTING.md                ← Common issues
├── LICENSE                           ← MIT License
├── setup.sh                          ← Auto setup
│
└── decoy_service/
    ├── __init__.py                   ← Package init
    ├── decoy_service.py              ← Main service
    ├── browser_agent.py              ← Browser control
    ├── scheduler.py                  ← Scheduling
    ├── utils.py                      ← Utilities
    ├── examples.py                   ← Examples
    ├── requirements.txt              ← Dependencies
    │
    ├── config/
    │   ├── settings.yaml             ← Behavior config
    │   ├── websites.yaml             ← Website lists
    │   └── .env.example              ← Env template
    │
    └── logs/                         ← Activity logs
        └── decoy_service.log
```

## 🚀 Quick Commands

### Installation & First Run
```bash
cd decoy_service
pip install -r requirements.txt
python decoy_service.py
```

### With Playwright
```bash
pip install -r requirements.txt
playwright install
python decoy_service.py
```

### Scheduling
```bash
python scheduler.py
```

### Examples
```bash
python examples.py 1    # Simple session
python examples.py 2    # Scheduled sessions
python examples.py 3    # Custom config
python examples.py 4    # Tracking
python examples.py 5    # Headless mode
```

### Monitoring
```bash
tail -f logs/decoy_service.log
```

## 📊 Code Statistics

| Component | Lines | Purpose |
|-----------|-------|---------|
| decoy_service.py | 520 | Main orchestrator |
| browser_agent.py | 390 | Browser control |
| utils.py | 340 | Utilities |
| examples.py | 250 | Usage examples |
| scheduler.py | 180 | Scheduling |
| **Total** | **~1,680** | **Complete service** |

## 🎯 Use Cases

### Simple One-Time Privacy Boost
1. Read [QUICKSTART.md](QUICKSTART.md)
2. Run: `python decoy_service.py`
3. Let it run for 10-30 minutes

### Regular Privacy Protection
1. Read [REFERENCE.md](REFERENCE.md)
2. Edit `scheduler.py` to schedule
3. Run: `python scheduler.py`
4. Monitor: `tail -f logs/decoy_service.log`

### Custom Configuration
1. Read [README.md](README.md)
2. Edit `config/settings.yaml`
3. Edit `config/websites.yaml`
4. Run: `python decoy_service.py`

### Troubleshooting
1. Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
2. Enable DEBUG logging in settings
3. Run with `headless: false`
4. Check `logs/decoy_service.log`

## 🔑 Key Concepts

### DecoyService
Main class that orchestrates all activity. Creates browser agents, generates random patterns, tracks activity.

```python
service = DecoyService('config')
service.start_session()
service.tracker.print_summary()
```

### BrowserAgent
Abstract interface for different browser implementations. Handles navigation, clicking, scrolling.

```python
agent = create_agent(logger, config)
agent.open_browser()
agent.visit_url("https://example.com")
agent.random_click()
```

### DecoyScheduler
Runs sessions at scheduled intervals. Supports hourly, daily, custom schedules.

```python
scheduler = DecoyScheduler('config', logger)
scheduler.schedule_interval(minutes=180, duration_minutes=15)
scheduler.start()
```

### ActivityTracker
Tracks statistics and metrics from sessions.

```python
tracker.record_website_visit(url)
summary = tracker.get_summary()
```

## 💡 Tips for Success

1. **Start Simple** - Run once with default config first
2. **Customize Carefully** - Edit one setting at a time
3. **Monitor Logs** - Check `logs/decoy_service.log` for errors
4. **Test First** - Run with `headless: false` to see behavior
5. **Schedule Wisely** - Use off-peak hours for background sessions
6. **Mix In Reality** - Combine with real browsing for best results

## ⚠️ Important Reminders

- Use only for personal privacy protection
- Respect website terms of service
- Follow applicable laws and regulations
- Use reasonable delays to avoid overloading servers
- Don't use for malicious purposes (DDoS, fraud, etc.)

## 🎓 Learning Resources

The code demonstrates:
- Object-oriented Python design patterns
- Configuration management with YAML
- Browser automation (Selenium & Playwright)
- Logging and monitoring
- Scheduling and threading
- Error handling and recovery

## 📞 Getting Help

### If You Get an Error:
1. Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
2. Enable DEBUG logging in `settings.yaml`
3. Run with `headless: false` in `settings.yaml`
4. Check `logs/decoy_service.log`

### For Configuration Questions:
1. Check [REFERENCE.md](REFERENCE.md)
2. Read [README.md](README.md)
3. Look at `examples.py`
4. Check comments in `settings.yaml` and `websites.yaml`

### For Usage Questions:
1. Read [QUICKSTART.md](QUICKSTART.md)
2. See examples in `examples.py`
3. Check [README.md](README.md)

## 🎉 Ready to Start?

**Choose your path:**

- **⚡ Quick Start**: Go to [QUICKSTART.md](QUICKSTART.md)
- **📖 Learn More**: Read [README.md](README.md)
- **🔍 Quick Ref**: Use [REFERENCE.md](REFERENCE.md)
- **🐛 Debugging**: Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- **💻 Code**: See `decoy_service/decoy_service.py`

---

**Version**: 1.0.0  
**License**: MIT  
**Created**: February 15, 2026  
**Status**: ✅ Complete and Ready to Use

Happy privacy protecting! 🔒
