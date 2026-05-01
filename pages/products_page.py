
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from config.config import PRODUCTS_URL
from utilities.logger import get_logger

logger = get_logger(__name__)


class ProductsPage(BasePage):
    """Products page locators and methods"""

    # Page Elements
    ALL_PRODUCTS_HEADING = (By.CSS_SELECTOR, ".features_items h2")
    PRODUCTS_LIST = (By.CSS_SELECTOR, ".features_items")
    PRODUCT_ITEMS = (By.CSS_SELECTOR, ".single-products")

    # Search
    SEARCH_INPUT = (By.ID, "search_product")
    SEARCH_BUTTON = (By.ID, "submit_search")
    SEARCHED_PRODUCTS_HEADING = (By.CSS_SELECTOR, ".features_items h2")

    # Product Details
    PRODUCT_NAME = (By.CSS_SELECTOR, ".productinfo p")
    PRODUCT_PRICE = (By.CSS_SELECTOR, ".productinfo h2")
    VIEW_PRODUCT_BUTTONS = (By.CSS_SELECTOR, ".choose a")
    ADD_TO_CART_BUTTONS = (By.CSS_SELECTOR, ".product-overlay .add-to-cart")

    # Product Detail Page
    PRODUCT_DETAIL_NAME = (By.CSS_SELECTOR, ".product-information h2")
    PRODUCT_DETAIL_CATEGORY = (By.CSS_SELECTOR, ".product-information p:nth-child(3)")
    PRODUCT_DETAIL_PRICE = (By.CSS_SELECTOR, ".product-information span span")
    PRODUCT_DETAIL_AVAILABILITY = (By.CSS_SELECTOR, ".product-information p:nth-child(6)")
    PRODUCT_DETAIL_CONDITION = (By.CSS_SELECTOR, ".product-information p:nth-child(7)")
    PRODUCT_DETAIL_BRAND = (By.CSS_SELECTOR, ".product-information p:nth-child(8)")
    QUANTITY_INPUT = (By.ID, "quantity")
    ADD_TO_CART_DETAIL = (By.CSS_SELECTOR, ".product-information button")

    # Modal
    CONTINUE_SHOPPING_BUTTON = (By.CSS_SELECTOR, "button.btn-success")
    VIEW_CART_MODAL = (By.CSS_SELECTOR, "u")

    # Brands
    BRANDS_PANEL = (By.CSS_SELECTOR, ".brands_products")
    BRAND_LINKS = (By.CSS_SELECTOR, ".brands-name a")

    # Categories
    CATEGORY_PANEL = (By.CSS_SELECTOR, ".left-sidebar")
    WOMEN_CATEGORY = (By.XPATH, "//a[normalize-space()='Women']")
    DRESS_SUBCATEGORY = (By.XPATH, "//div[@id='Women']//a[contains(text(),'Dress')]")

    def __init__(self, driver):
        super().__init__(driver)

    def open(self):
        """Open products page"""
        self.open_url(PRODUCTS_URL)
        logger.info("Products page opened")

    def is_products_page_loaded(self):
        """Check if products page is loaded"""
        return self.is_element_visible(self.ALL_PRODUCTS_HEADING)

    def get_all_products_heading_text(self):
        """Get the heading text"""
        return self.get_text(self.ALL_PRODUCTS_HEADING)

    def get_products_count(self):
        """Get count of products displayed"""
        try:
            products = self.find_elements(self.PRODUCT_ITEMS)
            count = len(products)
            logger.info(f"Total products: {count}")
            return count
        except Exception as e:
            logger.info("No products found (possibly empty search results)")
            return 0

    def is_products_list_visible(self):
        """Check if products list is visible"""
        return self.is_element_visible(self.PRODUCTS_LIST)

    def click_view_product(self, index=0):
        """Click on View Product button for a specific product"""
        view_buttons = self.find_elements(self.VIEW_PRODUCT_BUTTONS)
        if index < len(view_buttons):
            view_buttons[index].click()
            logger.info(f"Clicked on View Product for product at index {index}")
        else:
            logger.error(f"Product index {index} out of range")
            raise IndexError(f"Product index {index} out of range")

    def is_product_detail_page_loaded(self):
        """Check if product detail page is loaded"""
        return (
            self.is_element_visible(self.PRODUCT_DETAIL_NAME, timeout=10)
            and self.is_element_visible(self.PRODUCT_DETAIL_CATEGORY, timeout=10)
            and self.is_element_visible(self.PRODUCT_DETAIL_PRICE, timeout=10)
            and self.is_element_visible(self.PRODUCT_DETAIL_AVAILABILITY, timeout=10)
            and self.is_element_visible(self.PRODUCT_DETAIL_CONDITION, timeout=10)
            and self.is_element_visible(self.PRODUCT_DETAIL_BRAND, timeout=10)
        )

    def get_product_detail_info(self):
        """Get product detail information"""
        return {
            'name': self.get_text(self.PRODUCT_DETAIL_NAME),
            'category': self.get_text(self.PRODUCT_DETAIL_CATEGORY),
            'price': self.get_text(self.PRODUCT_DETAIL_PRICE),
            'availability': self.get_text(self.PRODUCT_DETAIL_AVAILABILITY),
            'condition': self.get_text(self.PRODUCT_DETAIL_CONDITION),
            'brand': self.get_text(self.PRODUCT_DETAIL_BRAND)
        }

    def search_product(self, product_name):
        """Search for a product"""
        self.send_keys(self.SEARCH_INPUT, product_name)
        self.click(self.SEARCH_BUTTON)
        logger.info(f"Searched for product: {product_name}")

    def is_search_results_visible(self):
        """Check if search results are visible"""
        return self.is_element_visible(self.SEARCHED_PRODUCTS_HEADING)

    def get_searched_products_heading(self):
        """Get searched products heading text"""
        return self.get_text(self.SEARCHED_PRODUCTS_HEADING)

    def get_search_results_count(self):
        """Get count of search results"""
        return self.get_products_count()

    def verify_searched_products_visible(self):
        """Verify searched products are visible"""
        return self.is_search_results_visible()

    def has_search_results(self):
        """Check if search returned any results"""
        return self.get_search_results_count() > 0

    def add_product_to_cart(self, index=0):
        """Add a product to cart by index"""
        products = self.find_elements(self.PRODUCT_ITEMS)
        if index < len(products):
            product = products[index]
            # Hover over product to make Add to Cart visible
            self.actions.move_to_element(product).perform()
            add_cart_btn = product.find_element(By.CSS_SELECTOR, ".add-to-cart")
            add_cart_btn.click()
            logger.info(f"Added product at index {index} to cart")
        else:
            logger.error(f"Product index {index} out of range")
            raise IndexError(f"Product index {index} out of range")

    def click_continue_shopping(self):
        """Click Continue Shopping button in modal"""
        self.click(self.CONTINUE_SHOPPING_BUTTON)
        logger.info("Clicked Continue Shopping")

    def click_view_cart_modal(self):
        """Click View Cart link in modal"""
        self.click(self.VIEW_CART_MODAL)
        logger.info("Clicked View Cart from modal")

    def set_product_quantity(self, quantity):
        """Set product quantity on detail page"""
        quantity_input = self.wait_helper.wait_for_element_visible(self.QUANTITY_INPUT, timeout=15)
        quantity_input.clear()
        self.send_keys(self.QUANTITY_INPUT, str(quantity))
        logger.info(f"Set product quantity to: {quantity}")

    def add_to_cart_from_detail_page(self):
        """Add product to cart from detail page"""
        self.click(self.ADD_TO_CART_DETAIL)
        logger.info("Added product to cart from detail page")

    def click_brand(self, brand_name):
        """Click on a specific brand"""
        brand_locator = (
            By.XPATH,
            f"//div[contains(@class, 'brands_products')]//a[normalize-space()='{brand_name}']",
        )
        self.scroll_to_element(self.BRANDS_PANEL)
        self.click(brand_locator)
        logger.info(f"Clicked on brand: {brand_name}")

    def is_brands_panel_visible(self):
        """Check if brands panel is visible"""
        return self.is_element_visible(self.BRANDS_PANEL)

    def get_all_brand_names(self):
        """Get all brand names"""
        brands = self.find_elements(self.BRAND_LINKS)
        brand_names = [brand.text for brand in brands]
        logger.info(f"Found brands: {brand_names}")
        return brand_names

    def click_category_subcategory(self, category, subcategory):
        """Click on category and then subcategory"""
        category_locator = (By.LINK_TEXT, category)
        subcategory_locator = (By.LINK_TEXT, subcategory)

        self.scroll_to_element(self.CATEGORY_PANEL)
        self.click(category_locator)
        self.click(subcategory_locator)
        logger.info(f"Clicked on {category} > {subcategory}")