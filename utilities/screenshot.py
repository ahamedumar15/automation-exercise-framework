
import os
from datetime import datetime
from pathlib import Path
from config.config import SCREENSHOTS_DIR
from utilities.logger import get_logger

logger = get_logger(__name__)


class ScreenshotHelper:
    """Helper class for taking screenshots"""

    @staticmethod
    def take_screenshot(driver, test_name):
        """
        Take a screenshot and save it with timestamp

        Args:
            driver: WebDriver instance
            test_name (str): Name of the test

        Returns:
            str: Path to the saved screenshot
        """
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{test_name}_{timestamp}.png"
            filepath = SCREENSHOTS_DIR / filename

            driver.save_screenshot(str(filepath))
            logger.info(f"Screenshot saved: {filepath}")
            return str(filepath)
        except Exception as e:
            logger.error(f"Failed to take screenshot: {e}")
            return None

    @staticmethod
    def take_element_screenshot(driver, element, test_name):
        """
        Take a screenshot of a specific element

        Args:
            driver: WebDriver instance
            element: WebElement to capture
            test_name (str): Name of the test

        Returns:
            str: Path to the saved screenshot
        """
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{test_name}_element_{timestamp}.png"
            filepath = SCREENSHOTS_DIR / filename

            element.screenshot(str(filepath))
            logger.info(f"Element screenshot saved: {filepath}")
            return str(filepath)
        except Exception as e:
            logger.error(f"Failed to take element screenshot: {e}")
            return None