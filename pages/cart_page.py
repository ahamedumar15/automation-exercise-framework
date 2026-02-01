
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from config.config import CART_URL
from utilities.logger import get_logger
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logger = get_logger(__name__)


class CartPage(BasePage):
    """Cart page locators and methods"""

    # Cart Elements
    CART_INFO_TABLE = (By.XPATH, "//div[@id='cart_info']")
    CART_ITEMS = (By.CSS_SELECTOR, "#cart_info_table tbody tr")
    PRODUCT_NAMES = (By.CSS_SELECTOR, ".cart_description h4 a")
    PRODUCT_PRICES = (By.CSS_SELECTOR, ".cart_price p")
    PRODUCT_QUANTITIES = (By.CSS_SELECTOR, ".cart_quantity button")
    PRODUCT_TOTALS = (By.CSS_SELECTOR, ".cart_total_price")
    DELETE_BUTTONS = (By.CSS_SELECTOR, ".cart_quantity_delete")

    # Empty Cart
    EMPTY_CART_TEXT = (By.XPATH, "//b[contains(text(), 'Cart is empty')]")

    # Checkout
    PROCEED_TO_CHECKOUT_BUTTON = (By.CSS_SELECTOR, ".btn.btn-default.check_out")
    REGISTER_LOGIN_LINK = (By.XPATH, "//u[contains(text(), 'Register / Login')]")

    # Subscription (footer)
    SUBSCRIPTION_EMAIL = (By.ID, "susbscribe_email")
    SUBSCRIPTION_BUTTON = (By.ID, "subscribe")
    SUCCESS_SUBSCRIBE_ALERT = (By.XPATH, "//*[contains(@class, 'alert-success') and normalize-space(text()) = 'You have been successfully subscribed!']")

    def __init__(self, driver):
        super().__init__(driver)

    def open(self):
        """Open cart page"""
        self.open_url(CART_URL)
        logger.info("Cart page opened")

    def is_cart_page_loaded(self):
        """Check if cart page is loaded"""
        return self.is_element_visible(self.CART_INFO_TABLE) or self.is_element_visible(self.EMPTY_CART_TEXT)

    def is_cart_empty(self):
        """Check if cart is empty"""
        return self.is_element_visible(self.EMPTY_CART_TEXT, timeout=3)

    def get_cart_items_count(self):
        """Get number of items in cart"""
        if self.is_cart_empty():
            return 0
        cart_items = self.find_elements(self.CART_ITEMS)
        count = len(cart_items)
        logger.info(f"Cart items count: {count}")
        return count

    def get_all_product_names(self):
        """Get names of all products in cart"""
        if self.is_cart_empty():
            return []
        products = self.find_elements(self.PRODUCT_NAMES)
        names = [product.text for product in products]
        logger.info(f"Products in cart: {names}")
        return names

    def get_product_details(self, index=0):
        """
        Get details of a specific product in cart

        Args:
            index (int): Index of the product (0-based)

        Returns:
            dict: Product details
        """
        if self.is_cart_empty():
            return None

        cart_items = self.find_elements(self.CART_ITEMS)
        if index >= len(cart_items):
            logger.error(f"Product index {index} out of range")
            return None

        item = cart_items[index]

        name = item.find_element(By.CSS_SELECTOR, ".cart_description h4 a").text
        price_text = item.find_element(By.CSS_SELECTOR, ".cart_price p").text
        quantity_text = item.find_element(By.CSS_SELECTOR, ".cart_quantity button").text
        total_text = item.find_element(By.CSS_SELECTOR, ".cart_total_price").text

        details = {
            'name': name,
            'price': price_text,
            'quantity': int(quantity_text),
            'total': total_text
        }

        logger.info(f"Product {index} details: {details}")
        return details

    def verify_product_in_cart(self, product_name):
        """
        Verify if a product is in cart

        Args:
            product_name (str): Name of the product

        Returns:
            bool: True if product found, False otherwise
        """
        products = self.get_all_product_names()
        is_present = product_name in products
        logger.info(f"Product '{product_name}' in cart: {is_present}")
        return is_present

    def delete_product(self, index=0):
        """
        Delete a product from cart by index

        Args:
            index (int): Index of the product to delete
        """
        delete_buttons = self.find_elements(self.DELETE_BUTTONS)
        if index < len(delete_buttons):
            delete_buttons[index].click()
            logger.info(f"Deleted product at index {index}")
        else:
            logger.error(f"Delete button index {index} out of range")

    def delete_all_products(self):
        """Delete all products from cart"""
        while not self.is_cart_empty():
            self.delete_product(0)
        logger.info("Deleted all products from cart")

    def click_proceed_to_checkout(self):
        """Click Proceed to Checkout button"""
        self.scroll_to_element(self.PROCEED_TO_CHECKOUT_BUTTON)
        self.click(self.PROCEED_TO_CHECKOUT_BUTTON)
        logger.info("Clicked Proceed to Checkout")

    def is_register_login_modal_visible(self):
        """Check if Register/Login modal is visible"""
        return self.is_element_visible(self.REGISTER_LOGIN_LINK, timeout=5)

    def click_register_login_link(self):
        """Click on Register/Login link in checkout modal"""
        self.click(self.REGISTER_LOGIN_LINK)
        logger.info("Clicked Register/Login link")

    def verify_product_quantity(self, product_name, expected_quantity):
        """
        Verify quantity of a specific product

        Args:
            product_name (str): Name of the product
            expected_quantity (int): Expected quantity

        Returns:
            bool: True if quantity matches, False otherwise
        """
        products = self.get_all_product_names()
        if product_name not in products:
            logger.error(f"Product '{product_name}' not found in cart")
            return False

        index = products.index(product_name)
        details = self.get_product_details(index)

        if details and details['quantity'] == expected_quantity:
            logger.info(f"Quantity verified for '{product_name}': {expected_quantity}")
            return True
        else:
            logger.error(
                f"Quantity mismatch for '{product_name}'. Expected: {expected_quantity}, Got: {details['quantity']}")
            return False

    def subscribe_email(self, email):
        """Subscribe and verify success in one step"""
        self.scroll_to_bottom()
        self.send_keys(self.SUBSCRIPTION_EMAIL, email)
        self.click(self.SUBSCRIPTION_BUTTON)
        logger.info(f"Subscribed with email: {email}")

        # Update your locator to something reliable
        success_locator = (By.XPATH,"//*[contains(@class, 'alert-success') and contains(text(), 'successfully subscribed')]")

        try:
            alert = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(success_locator)
            )
            success_text = alert.text.strip()
            logger.info(f"Success message: {success_text}")
            return True
        except:
            logger.error("Subscription success alert did not appear")
            return False


    def calculate_total_price(self):
        """Calculate total price of all items in cart"""
        if self.is_cart_empty():
            return 0

        totals = self.find_elements(self.PRODUCT_TOTALS)
        total_price = 0

        for total_element in totals:
            # Extract numeric value from "Rs. 500" format
            price_text = total_element.text.replace("Rs. ", "").replace(",", "")
            total_price += int(price_text)

        logger.info(f"Total cart price: Rs. {total_price}")
        return total_price