decoy_service/
├── 📄 README.md                          # Full documentation
├── 📄 QUICKSTART.md                      # Quick start guide  
├── 📄 LICENSE                            # MIT License
├── 📄 setup.sh                           # Automated setup script
│
├── decoy_service/                        # Main package
│   ├── __init__.py                       # Package init (auto-created)
│   ├── decoy_service.py                  # Main service orchestrator
│   ├── browser_agent.py                  # Browser automation (Selenium/Playwright)
│   ├── scheduler.py                      # Schedule recurring sessions
│   ├── utils.py                          # Utilities (logging, config, tracking)
│   ├── examples.py                       # Example usage scenarios
│   └── requirements.txt                  # Python dependencies
│
├── config/                               # Configuration files
│   ├── settings.yaml                     # Behavior settings (timing, clicks, etc)
│   ├── websites.yaml                     # Website categories and queries
│   └── .env.example                      # Environment variables template
│
└── logs/                                 # Activity logs (auto-created)
    └── decoy_service.log                 # Main activity log


FILE DESCRIPTIONS:

DOCUMENTATION:
  README.md          - Complete guide with architecture, usage, troubleshooting
  QUICKSTART.md      - 5-minute setup and common tasks
  LICENSE            - MIT License with disclaimer

MAIN CODE:
  decoy_service.py   - Orchestrates browser visits, searches, interactions
  browser_agent.py   - Selenium and Playwright browser automation
  scheduler.py       - Schedule sessions at regular intervals
  utils.py           - Logging, config loading, activity tracking
  examples.py        - Example usage patterns

CONFIGURATION:
  settings.yaml      - Timing, clicking behavior, browser settings
  websites.yaml      - Website lists by category, search queries
  .env.example       - Template for environment variables


SETUP:
1. pip install -r decoy_service/requirements.txt
2. python decoy_service/decoy_service.py

For scheduling:
3. python decoy_service/scheduler.py
