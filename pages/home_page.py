
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from config.config import BASE_URL
from utilities.logger import get_logger

logger = get_logger(__name__)


class HomePage(BasePage):
    """Home page locators and methods"""

    # Locators
    LOGO = (By.CSS_SELECTOR, "img[alt='Website for automation practice']")
    HOME_LINK = (By.XPATH, "//a[normalize-space()='Home']")
    PRODUCTS_LINK = (By.XPATH, "//a[@href='/products']")
    CART_LINK = (By.XPATH, "//a[normalize-space()='Cart']")
    SIGNUP_LOGIN_LINK = (By.XPATH, "//a[normalize-space()='Signup / Login']")
    LOGOUT_LINK = (By.LINK_TEXT, "Logout")
    DELETE_ACCOUNT_LINK = (By.LINK_TEXT, "Delete Account")
    CONTACT_US_LINK = (By.LINK_TEXT, "Contact us")
    TEST_CASES_LINK = (By.LINK_TEXT, "Test Cases")

    # Main content
    CAROUSEL = (By.ID, "slider-carousel")
    FEATURES_ITEMS = (By.CSS_SELECTOR, ".features_items")
    CATEGORY_PRODUCTS = (By.CSS_SELECTOR, ".left-sidebar")

    # Product items
    PRODUCT_ITEMS = (By.CSS_SELECTOR, ".single-products")
    ADD_TO_CART_BUTTONS = (By.CSS_SELECTOR, ".product-overlay .add-to-cart")
    VIEW_PRODUCT_LINKS = (By.CSS_SELECTOR, ".choose a")
    CONTINUE_SHOPPING_BUTTON = (By.CSS_SELECTOR, "button.btn-success")

    # Subscription
    SUBSCRIPTION_HEADING = (By.XPATH, "//h2[contains(text(), 'Subscription')]")
    SUBSCRIPTION_EMAIL = (By.ID, "susbscribe_email")
    SUBSCRIPTION_BUTTON = (By.ID, "subscribe")
    SUCCESS_SUBSCRIBE_ALERT = (By.CSS_SELECTOR, ".alert-success alert")

    # Categories
    WOMEN_CATEGORY = (By.XPATH, "//a[normalize-space()='Women']")
    MEN_CATEGORY = (By.XPATH, "//a[normalize-space()='Men']")
    KIDS_CATEGORY = (By.XPATH, "//a[normalize-space()='Kids']")

    # Logged in user
    LOGGED_IN_AS_TEXT = (By.XPATH, "//li[contains(., 'Logged in as')]")

    def __init__(self, driver):
        super().__init__(driver)

    def open(self):
        """Open home page"""
        self.open_url(BASE_URL)
        logger.info("Home page opened")

    def is_home_page_loaded(self):
        """Verify home page is loaded"""
        return self.is_element_visible(self.LOGO) and self.is_element_visible(self.CAROUSEL)

    def click_signup_login(self):
        """Click on Signup/Login link"""
        self.click(self.SIGNUP_LOGIN_LINK)
        logger.info("Clicked on Signup/Login")

    def click_products(self):
        """Click on Products link"""
        self.click(self.PRODUCTS_LINK)
        logger.info("Clicked on Products")

    def click_cart(self):
        """Click on Cart link"""
        self.click(self.CART_LINK)
        logger.info("Clicked on Cart")

    def click_logout(self):
        """Click on Logout link"""
        self.click(self.LOGOUT_LINK)
        logger.info("Clicked on Logout")

    def click_delete_account(self):
        """Click on Delete Account link"""
        self.click(self.DELETE_ACCOUNT_LINK)
        logger.info("Clicked on Delete Account")

    def click_contact_us(self):
        """Click on Contact Us link"""
        self.click(self.CONTACT_US_LINK)
        logger.info("Clicked on Contact Us")

    def is_logged_in(self):
        """Check if user is logged in"""
        return self.is_element_visible(self.LOGGED_IN_AS_TEXT, timeout=5)

    def get_logged_in_username(self):
        """Get logged in username"""
        if self.is_logged_in():
            text = self.get_text(self.LOGGED_IN_AS_TEXT)
            username = text.replace("Logged in as ", "").strip()
            logger.info(f"Logged in username: {username}")
            return username
        return None

    def is_logout_visible(self):
        """Check if logout link is visible"""
        return self.is_element_visible(self.LOGOUT_LINK, timeout=5)

    def get_product_count(self):
        """Get count of products displayed on home page"""
        products = self.find_elements(self.PRODUCT_ITEMS)
        count = len(products)
        logger.info(f"Product count on home page: {count}")
        return count

    def scroll_to_footer(self):
        """Scroll to footer section"""
        self.scroll_to_bottom()
        logger.info("Scrolled to footer")

    def subscribe_email(self, email):
        """Subscribe with email"""
        self.scroll_to_element(self.SUBSCRIPTION_EMAIL)
        self.send_keys(self.SUBSCRIPTION_EMAIL, email)
        self.click(self.SUBSCRIPTION_BUTTON)
        logger.info(f"Subscribed with email: {email}")

    def is_subscription_successful(self):
        """Check if subscription was successful"""
        return self.is_element_visible(self.SUCCESS_SUBSCRIBE_ALERT, timeout=10)

    def get_subscription_success_message(self):
        """Get subscription success message"""
        if self.is_subscription_successful():
            return self.get_text(self.SUCCESS_SUBSCRIBE_ALERT)
        return None

    def click_category(self, category_name):
        """Click on a category"""
        category_locator = (By.LINK_TEXT, category_name)
        self.scroll_to_element(category_locator)
        self.click(category_locator)
        logger.info(f"Clicked on category: {category_name}")

    def hover_and_click_add_to_cart(self, product_index=0):
        """Hover over product and click add to cart"""
        import time
        products = self.find_elements(self.PRODUCT_ITEMS)
        if product_index < len(products):
            product = products[product_index]

            # Scroll to product
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", product)
            time.sleep(0.5)

            # Hover over product
            self.actions.move_to_element(product).perform()
            time.sleep(0.5)  # Wait for overlay to appear

            # Find and click add to cart button
            try:
                add_to_cart_btn = product.find_element(By.CSS_SELECTOR, ".overlay-content .add-to-cart")
            except:
                try:
                    add_to_cart_btn = product.find_element(By.CSS_SELECTOR, ".product-overlay .add-to-cart")
                except:
                    add_to_cart_btn = product.find_element(By.CSS_SELECTOR, "a[data-product-id]")

            # Use JavaScript click as fallback
            try:
                add_to_cart_btn.click()
            except:
                self.driver.execute_script("arguments[0].click();", add_to_cart_btn)

            logger.info(f"Added product {product_index} to cart")
        else:
            logger.error(f"Product index {product_index} out of range")

    def verify_home_page_visible(self):
        """Verify home page is visible"""
        return self.is_element_visible(self.CAROUSEL) and self.is_element_visible(self.FEATURES_ITEMS)