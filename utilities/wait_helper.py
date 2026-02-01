
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from config.config import EXPLICIT_WAIT
from utilities.logger import get_logger

logger = get_logger(__name__)


class WaitHelper:
    """Helper class for wait operations"""

    def __init__(self, driver, timeout=EXPLICIT_WAIT):
        self.driver = driver
        self.timeout = timeout
        self.wait = WebDriverWait(driver, timeout)

    def wait_for_element_visible(self, locator, timeout=None):
        """
        Wait for element to be visible

        Args:
            locator (tuple): Locator tuple (By.ID, "element_id")
            timeout (int): Custom timeout in seconds

        Returns:
            WebElement: The visible element
        """
        try:
            wait_time = timeout or self.timeout
            element = WebDriverWait(self.driver, wait_time).until(
                EC.visibility_of_element_located(locator)
            )
            logger.debug(f"Element visible: {locator}")
            return element
        except TimeoutException:
            logger.error(f"Element not visible within {wait_time}s: {locator}")
            raise

    def wait_for_element_clickable(self, locator, timeout=None):
        """
        Wait for element to be clickable

        Args:
            locator (tuple): Locator tuple (By.ID, "element_id")
            timeout (int): Custom timeout in seconds

        Returns:
            WebElement: The clickable element
        """
        try:
            wait_time = timeout or self.timeout
            # First, wait for element to be present
            WebDriverWait(self.driver, wait_time).until(
                EC.presence_of_element_located(locator)
            )
            # Then wait for it to be clickable
            element = WebDriverWait(self.driver, wait_time).until(
                EC.element_to_be_clickable(locator)
            )
            logger.debug(f"Element clickable: {locator}")
            return element
        except TimeoutException:
            logger.error(f"Element not clickable within {wait_time}s: {locator}")
            # Try to return the element anyway if it exists
            try:
                element = self.driver.find_element(*locator)
                if element:
                    logger.warning(f"Element exists but not clickable, returning anyway: {locator}")
                    return element
            except:
                pass
            raise

    def wait_for_element_present(self, locator, timeout=None):
        """
        Wait for element to be present in DOM

        Args:
            locator (tuple): Locator tuple
            timeout (int): Custom timeout in seconds

        Returns:
            WebElement: The present element
        """
        try:
            wait_time = timeout or self.timeout
            element = WebDriverWait(self.driver, wait_time).until(
                EC.presence_of_element_located(locator)
            )
            logger.debug(f"Element present: {locator}")
            return element
        except TimeoutException:
            logger.error(f"Element not present within {wait_time}s: {locator}")
            raise

    def wait_for_elements_visible(self, locator, timeout=None):
        """Wait for multiple elements to be visible"""
        try:
            wait_time = timeout or self.timeout
            elements = WebDriverWait(self.driver, wait_time).until(
                EC.visibility_of_all_elements_located(locator)
            )
            logger.debug(f"Elements visible: {locator}")
            return elements
        except TimeoutException:
            logger.error(f"Elements not visible within {wait_time}s: {locator}")
            raise

    def wait_for_text_in_element(self, locator, text, timeout=None):
        """Wait for specific text to appear in element"""
        try:
            wait_time = timeout or self.timeout
            result = WebDriverWait(self.driver, wait_time).until(
                EC.text_to_be_present_in_element(locator, text)
            )
            logger.debug(f"Text '{text}' present in element: {locator}")
            return result
        except TimeoutException:
            logger.error(f"Text '{text}' not found in element within {wait_time}s")
            raise

    def wait_for_element_invisible(self, locator, timeout=None):
        """Wait for element to become invisible"""
        try:
            wait_time = timeout or self.timeout
            result = WebDriverWait(self.driver, wait_time).until(
                EC.invisibility_of_element_located(locator)
            )
            logger.debug(f"Element invisible: {locator}")
            return result
        except TimeoutException:
            logger.error(f"Element still visible after {wait_time}s: {locator}")
            raise

    def wait_for_url_contains(self, url_fragment, timeout=None):
        """Wait for URL to contain specific text"""
        try:
            wait_time = timeout or self.timeout
            result = WebDriverWait(self.driver, wait_time).until(
                EC.url_contains(url_fragment)
            )
            logger.debug(f"URL contains: {url_fragment}")
            return result
        except TimeoutException:
            logger.error(f"URL doesn't contain '{url_fragment}' within {wait_time}s")
            raise

    def wait_for_alert(self, timeout=None):
        """Wait for alert to be present"""
        try:
            wait_time = timeout or self.timeout
            alert = WebDriverWait(self.driver, wait_time).until(
                EC.alert_is_present()
            )
            logger.debug("Alert present")
            return alert
        except TimeoutException:
            logger.error(f"Alert not present within {wait_time}s")
            raise