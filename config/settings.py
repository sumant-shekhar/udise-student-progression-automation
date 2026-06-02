"""
Configuration settings for UDISE+ Student Progression Automation
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Credentials
USERNAME = os.getenv("UDISE_USERNAME", "10140806703")
PASSWORD = os.getenv("UDISE_PASSWORD", "Pankaj@123.123")

# Application URLs
LOGIN_URL = "https://sdms.udiseplus.gov.in/p0/v1/login?state-id=110"
DASHBOARD_URL = "https://sdms.udiseplus.gov.in/dashboard"

# Playwright settings
HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"
BROWSER_TYPE = os.getenv("BROWSER_TYPE", "chromium")  # chromium, firefox, webkit
VIEWPORT = {"width": 1920, "height": 1080}

# Timeouts (in milliseconds)
WAIT_TIMEOUT = 15000  # 15 seconds
ELEMENT_TIMEOUT = 5000  # 5 seconds
NAVIGATION_TIMEOUT = 30000  # 30 seconds

# Retry configuration
MAX_RETRIES = 3
RETRY_DELAY = 0.5  # seconds

# Loop settings
LOOP_CHECK_INTERVAL = 10  # seconds between checking for new classes
