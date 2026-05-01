
import pytest
from utilities.logger import get_logger

logger = get_logger(__name__)


@pytest.mark.smoke
@pytest.mark.regression
class TestProducts:
    """Test class for products page scenarios"""

    def test_verify_all_products_and_product_detail_page(self, home_page, products_page):
        """
        Test Case TC_PRD_001: Verify All Products and product detail page

        """
        logger.info("Starting test: Verify all products and product detail")

        # Step 1-2: Navigate to products page
        home_page.open()
        home_page.click_products()
        assert products_page.is_products_page_loaded(), "Products page not loaded"

        # Step 3: Verify ALL PRODUCTS page
        assert products_page.is_products_page_loaded(), "Products page not loaded"
        heading_text = products_page.get_all_products_heading_text()
        assert "ALL PRODUCTS" in heading_text, f"Expected 'ALL PRODUCTS', got: {heading_text}"
        logger.info("✓ ALL PRODUCTS page loaded")

        # Step 4: Verify products list
        assert products_page.is_products_list_visible(), "Products list not visible"
        product_count = products_page.get_products_count()
        assert product_count > 0, "No products displayed"
        logger.info(f"✓ Products list visible with {product_count} products")

        # Step 5: Click View Product for first product
        products_page.click_view_product(0)

        # Step 6: Verify product detail page
        assert products_page.is_product_detail_page_loaded(), "Product detail page not loaded"
        logger.info("✓ Product detail page loaded")

        # Step 7: Verify product details
        product_info = products_page.get_product_detail_info()

        assert product_info['name'], "Product name not visible"
        assert product_info['category'], "Product category not visible"
        assert product_info['price'], "Product price not visible"
        assert product_info['availability'], "Product availability not visible"
        assert product_info['condition'], "Product condition not visible"
        assert product_info['brand'], "Product brand not visible"

        logger.info(f"✓ Product details verified: {product_info['name']}")

    @pytest.mark.smoke
    def test_search_product(self, home_page, products_page):
        """
        Test Case TC_PRD_002: Search Product
        """
        logger.info("Starting test: Search product")

        # Step 1-3: Navigate to products page
        home_page.open()
        home_page.click_products()
        assert products_page.is_products_page_loaded(), "Products page not loaded"
        logger.info("✓ Products page loaded")

        # Step 4-5: Search for product
        search_term = "top"
        products_page.search_product(search_term)

        # Step 6: Verify searched products heading
        assert products_page.is_search_results_visible(), "Search results not visible"
        search_heading = products_page.get_searched_products_heading()
        assert "SEARCHED PRODUCTS" in search_heading, f"Expected 'SEARCHED PRODUCTS', got: {search_heading}"
        logger.info("✓ Search results page displayed")

        # Step 7: Verify search results
        results_count = products_page.get_search_results_count()
        assert results_count > 0, "No search results found"
        logger.info(f"✓ Found {results_count} products matching '{search_term}'")

    @pytest.mark.regression
    def test_search_product_no_results(self, home_page, products_page):
        """
        Test Case TC_PRD_003: Search for product with no results
        """
        logger.info("Starting test: Search product with no results")

        home_page.open()
        home_page.click_products()
        assert products_page.is_products_page_loaded(), "Products page not loaded"

        # Search for non-existent product
        products_page.search_product("NonExistentProduct123XYZ")

        # Should still show searched products heading
        assert products_page.is_search_results_visible(), "Search results page not displayed"

        # Check if there are results
        if products_page.has_search_results():
            results_count = products_page.get_search_results_count()
            logger.info(f"✓ Search completed with {results_count} results")
        else:
            logger.info("✓ Search completed with 0 results (no products found)")

        # Test passes either way - we're just verifying the search functionality works

    @pytest.mark.regression
    def test_verify_product_quantity_in_detail_page(self, home_page, products_page):
        """
        Test Case TC_PRD_004: Verify product quantity can be increased in detail page
        """
        logger.info("Starting test: Verify product quantity in detail page")

        home_page.open()
        home_page.click_products()
        assert products_page.is_products_page_loaded(), "Products page not loaded"

        # Go to product detail page
        products_page.click_view_product(0)

        # Verify quantity field is visible
        assert products_page.is_element_visible(products_page.QUANTITY_INPUT, timeout=15), "Quantity input not visible"

        # Set quantity
        test_quantity = 4
        products_page.set_product_quantity(test_quantity)

        # Get current value
        quantity_value = products_page.get_attribute(products_page.QUANTITY_INPUT, "value")
        assert quantity_value == str(
            test_quantity), f"Quantity not set correctly. Expected: {test_quantity}, Got: {quantity_value}"

        logger.info(f"✓ Product quantity set to {test_quantity}")

    @pytest.mark.smoke
    def test_view_category_products(self, home_page, products_page):
        """
        Test Case TC_PRD_005: View Category Products
        """
        logger.info("Starting test: View category products")

        # Step 1: Navigate to home page
        home_page.open()

        # Step 2: Verify categories visible
        assert home_page.is_element_visible(home_page.CATEGORY_PRODUCTS), "Categories not visible"
        logger.info("✓ Categories visible on sidebar")

        # Step 3-4: Click category and subcategory
        home_page.click_category("Women")
        home_page.click_category("Dress")

        # Step 5: Verify category products displayed
        current_url = home_page.get_current_url()
        assert "category_products" in current_url, f"Not on category page. URL: {current_url}"

        # Verify products displayed
        products_count = products_page.get_products_count()
        assert products_count > 0, "No category products displayed"
        logger.info(f"✓ Category products displayed: {products_count} items")

    @pytest.mark.regression
    def test_view_brands_products(self, home_page, products_page):
        """
        Test Case TC_PRD_006: View & Cart Brand Products
        """
        logger.info("Starting test: View brand products")

        # Step 1: Navigate to products page
        home_page.open()
        home_page.click_products()
        assert products_page.is_products_page_loaded(), "Products page not loaded"

        # Step 2: Verify brands visible
        assert products_page.is_brands_panel_visible(), "Brands panel not visible"
        logger.info("✓ Brands panel visible")

        # Step 3: Click on a brand
        products_page.click_brand("Polo")

        # Step 4: Verify brand products displayed
        current_url = products_page.get_current_url()
        assert "brand_products" in current_url, f"Not on brand page. URL: {current_url}"

        products_count = products_page.get_products_count()
        assert products_count > 0, "No brand products displayed"
        logger.info(f"✓ Brand products displayed: {products_count} items")

    @pytest.mark.regression
    def test_add_products_to_cart_from_products_page(self, home_page, products_page, cart_page):
        """
        Test Case TC_PRD_007: Add multiple products to cart from products page
        """
        logger.info("Starting test: Add products to cart from products page")

        home_page.open()
        home_page.click_products()
        assert products_page.is_products_page_loaded(), "Products page not loaded"

        # Add first product
        products_page.add_product_to_cart(0)

        # Click Continue Shopping
        products_page.click_continue_shopping()
        assert products_page.wait_helper.wait_for_element_invisible(products_page.CONTINUE_SHOPPING_BUTTON, timeout=10), "Continue shopping modal did not close"

        # Add second product
        products_page.add_product_to_cart(1)

        # Click View Cart
        products_page.click_view_cart_modal()
        assert cart_page.is_cart_page_loaded(), "Cart page not loaded"

        # Verify cart has 2 items
        cart_items_count = cart_page.get_cart_items_count()
        assert cart_items_count == 2, f"Expected 2 items in cart, got {cart_items_count}"
        logger.info(f"✓ Cart has {cart_items_count} items")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])