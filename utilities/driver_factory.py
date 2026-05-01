
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from config.config import BROWSER, HEADLESS, IMPLICIT_WAIT, PAGE_LOAD_TIMEOUT
from utilities.logger import get_logger

logger = get_logger(__name__)

class DriverFactory:
    """Factory class to create WebDriver instances"""

    @staticmethod
    def get_driver(browser=None):
        """ Create and return a WebDriver instance based on browser type
        Args:
            browser (str): Browser name (chrome, firefox, edge)
        Returns:
            WebDriver: Configured WebDriver instance
        """
        browser = browser or BROWSER
        browser = browser.lower()
        logger.info(f"Initializing {browser} browser")
        if browser == "chrome":
            driver = DriverFactory._get_chrome_driver()
        elif browser == "firefox":
            driver = DriverFactory._get_firefox_driver()
        elif browser == "edge":
            driver = DriverFactory._get_edge_driver()
        else:
            raise ValueError(f"Unsupported browser: {browser}")

        # Set timeouts
        driver.implicitly_wait(IMPLICIT_WAIT)
        driver.set_page_load_timeout(PAGE_LOAD_TIMEOUT)
        driver.maximize_window()
        logger.info(f"{browser.capitalize()} browser initialized successfully")
        return driver

    @staticmethod
    def _get_chrome_driver():
        """Create Chrome WebDriver"""
        options = webdriver.ChromeOptions()
        # Chrome options for stability
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-gpu")
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        if HEADLESS:
            options.add_argument("--headless=new")
            options.add_argument("--window-size=1920,1080")

        service = ChromeService(ChromeDriverManager().install())
        return webdriver.Chrome(service=service, options=options)

    @staticmethod
    def _get_firefox_driver():
        """Create Firefox WebDriver"""
        options = webdriver.FirefoxOptions()
        options.add_argument("-private")  # Enable private browsing mode
        if HEADLESS:
            options.add_argument("--headless")
        service = FirefoxService(GeckoDriverManager().install())
        return webdriver.Firefox(service=service, options=options)

    @staticmethod
    def _get_edge_driver():
        """Create Edge WebDriver"""
        options = webdriver.EdgeOptions()
        options.add_argument("--disable-blink-features=AutomationControlled")
        if HEADLESS:
            options.add_argument("--headless")
        service = EdgeService(EdgeChromiumDriverManager().install())
        return webdriver.Edge(service=service, options=options)

    @staticmethod
    def quit_driver(driver):
        """ Safely quit the WebDriver instance
        Args:
            driver: WebDriver instance to quit
        """
        if driver:
            try:
                driver.quit()
                logger.info("Browser closed successfully")
            except Exception as e:
                logger.error(f"Error closing browser: {e}")