"""
Configuration file for the automation framework
"""
import os
from pathlib import Path

# Base Directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Application URLs
BASE_URL = "https://automationexercise.com"
LOGIN_URL = f"{BASE_URL}/login"
PRODUCTS_URL = f"{BASE_URL}/products"
CART_URL = f"{BASE_URL}/view_cart"
CONTACT_URL = f"{BASE_URL}/contact_us"

# Browser Configuration
BROWSER = os.getenv("BROWSER", "firefox")
HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"
IMPLICIT_WAIT = 10
EXPLICIT_WAIT = 20
PAGE_LOAD_TIMEOUT = 30

# Directory Paths
REPORTS_DIR = BASE_DIR / "reports"
LOGS_DIR = BASE_DIR / "logs"
SCREENSHOTS_DIR = BASE_DIR / "screenshots"
TESTDATA_DIR = BASE_DIR / "testdata"

# Create directories if they don't exist
for directory in [REPORTS_DIR, LOGS_DIR, SCREENSHOTS_DIR]:
    directory.mkdir(exist_ok=True)

# Test Data
TEST_EMAIL_DOMAIN = "@automationtest.com"

# Logging Configuration
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Screenshot Configuration
SCREENSHOT_ON_FAILURE = True
SCREENSHOT_ON_SUCCESS = False

# Retry Configuration
MAX_RETRIES = 3
RETRY_DELAY = 2