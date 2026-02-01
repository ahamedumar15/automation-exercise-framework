
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from utilities.wait_helper import WaitHelper
from utilities.logger import get_logger
from utilities.screenshot import ScreenshotHelper

logger = get_logger(__name__)


class BasePage:
    """Base class for all page objects"""

    def __init__(self, driver):
        self.driver = driver
        self.wait_helper = WaitHelper(driver)
        self.actions = ActionChains(driver)

    def open_url(self, url):
        """Navigate to a specific URL"""
        try:
            self.driver.get(url)
            logger.info(f"Navigated to: {url}")
        except Exception as e:
            logger.error(f"Failed to navigate to {url}: {e}")
            raise

    def get_current_url(self):
        """Get current page URL"""
        return self.driver.current_url

    def get_page_title(self):
        """Get current page title"""
        return self.driver.title

    def find_element(self, locator):
        """Find a single element"""
        try:
            element = self.wait_helper.wait_for_element_visible(locator)
            logger.debug(f"Element found: {locator}")
            return element
        except Exception as e:
            logger.error(f"Element not found: {locator}")
            raise

    def find_elements(self, locator):
        """Find multiple elements"""
        try:
            elements = self.wait_helper.wait_for_elements_visible(locator)
            logger.debug(f"Found {len(elements)} elements: {locator}")
            return elements
        except Exception as e:
            logger.debug(f"No elements found: {locator} - returning empty list")
            return []

    def click(self, locator):
        """Click on an element"""
        try:
            element = self.wait_helper.wait_for_element_clickable(locator)
            element.click()
            logger.info(f"Clicked on element: {locator}")
        except Exception as e:
            logger.warning(f"Normal click failed: {e}, trying JavaScript click")
            try:
                # Fallback to JavaScript click
                element = self.find_element(locator)
                self.driver.execute_script("arguments[0].click();", element)
                logger.info(f"Clicked on element using JavaScript: {locator}")
            except Exception as e2:
                logger.error(f"Failed to click element: {locator}")
                raise

    def send_keys(self, locator, text):
        """Send text to an input field"""
        try:
            element = self.wait_helper.wait_for_element_visible(locator)
            element.clear()
            element.send_keys(text)
            logger.info(f"Entered text in element: {locator}")
        except Exception as e:
            logger.error(f"Failed to enter text: {locator}")
            raise

    def get_text(self, locator):
        """Get text from an element"""
        try:
            element = self.wait_helper.wait_for_element_visible(locator)
            text = element.text
            logger.debug(f"Got text from element: {locator}")
            return text
        except Exception as e:
            logger.error(f"Failed to get text: {locator}")
            raise

    def get_attribute(self, locator, attribute):
        """Get attribute value from an element"""
        try:
            element = self.find_element(locator)
            value = element.get_attribute(attribute)
            logger.debug(f"Got attribute '{attribute}' from element: {locator}")
            return value
        except Exception as e:
            logger.error(f"Failed to get attribute: {locator}")
            raise

    def is_element_visible(self, locator, timeout=5):
        """Check if element is visible"""
        try:
            self.wait_helper.wait_for_element_visible(locator, timeout)
            return True
        except (NoSuchElementException, TimeoutException):
            return False

    def is_element_present(self, locator, timeout=5):
        """Check if element is present in DOM"""
        try:
            self.wait_helper.wait_for_element_present(locator, timeout)
            return True
        except (NoSuchElementException, TimeoutException):
            return False

    def select_dropdown_by_text(self, locator, text):
        """Select dropdown option by visible text"""
        try:
            element = self.find_element(locator)
            select = Select(element)
            select.select_by_visible_text(text)
            logger.info(f"Selected '{text}' from dropdown: {locator}")
        except Exception as e:
            logger.error(f"Failed to select from dropdown: {locator}")
            raise

    def select_dropdown_by_value(self, locator, value):
        """Select dropdown option by value"""
        try:
            element = self.find_element(locator)
            select = Select(element)
            select.select_by_value(value)
            logger.info(f"Selected value '{value}' from dropdown: {locator}")
        except Exception as e:
            logger.error(f"Failed to select from dropdown: {locator}")
            raise

    def hover_over_element(self, locator):
        """Hover mouse over an element"""
        try:
            element = self.find_element(locator)
            self.actions.move_to_element(element).perform()
            logger.info(f"Hovered over element: {locator}")
        except Exception as e:
            logger.error(f"Failed to hover over element: {locator}")
            raise

    def scroll_to_element(self, locator):
        """Scroll to make element visible"""
        try:
            element = self.find_element(locator)
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            logger.info(f"Scrolled to element: {locator}")
        except Exception as e:
            logger.error(f"Failed to scroll to element: {locator}")
            raise

    def scroll_to_bottom(self):
        """Scroll to bottom of page"""
        try:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            logger.info("Scrolled to bottom of page")
        except Exception as e:
            logger.error(f"Failed to scroll to bottom: {e}")
            raise

    def switch_to_alert(self):
        """Switch to alert and return alert object"""
        try:
            alert = self.wait_helper.wait_for_alert()
            logger.info("Switched to alert")
            return alert
        except Exception as e:
            logger.error(f"Failed to switch to alert: {e}")
            raise

    def accept_alert(self):
        """Accept alert"""
        try:
            alert = self.switch_to_alert()
            alert.accept()
            logger.info("Alert accepted")
        except Exception as e:
            logger.error(f"Failed to accept alert: {e}")
            raise

    def get_alert_text(self):
        """Get text from alert"""
        try:
            alert = self.switch_to_alert()
            text = alert.text
            logger.info(f"Alert text: {text}")
            return text
        except Exception as e:
            logger.error(f"Failed to get alert text: {e}")
            raise

    def take_screenshot(self, name):
        """Take screenshot with custom name"""
        return ScreenshotHelper.take_screenshot(self.driver, name)

    def refresh_page(self):
        """Refresh current page"""
        try:
            self.driver.refresh()
            logger.info("Page refreshed")
        except Exception as e:
            logger.error(f"Failed to refresh page: {e}")
            raise

    def go_back(self):
        """Navigate back"""
        try:
            self.driver.back()
            logger.info("Navigated back")
        except Exception as e:
            logger.error(f"Failed to navigate back: {e}")
            raise

    def switch_to_frame(self, locator):
        """Switch to iframe"""
        try:
            frame = self.find_element(locator)
            self.driver.switch_to.frame(frame)
            logger.info(f"Switched to frame: {locator}")
        except Exception as e:
            logger.error(f"Failed to switch to frame: {locator}")
            raise

    def switch_to_default_content(self):
        """Switch back to default content"""
        try:
            self.driver.switch_to.default_content()
            logger.info("Switched to default content")
        except Exception as e:
            logger.error(f"Failed to switch to default content: {e}")
            raise