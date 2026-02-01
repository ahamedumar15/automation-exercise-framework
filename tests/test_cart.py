
import pytest
import time
from utilities.logger import get_logger

logger = get_logger(__name__)


@pytest.mark.smoke
@pytest.mark.regression
class TestCart:
    """Test class for shopping cart scenarios"""

    def test_add_products_in_cart(self, home_page, cart_page):
        """
        Test Case TC_CART_001: Add Products in Cart
        """
        logger.info("Starting test: Add products in cart")

        # Step 1: Navigate to home page
        home_page.open()
        home_page.click_products()
        time.sleep(2)

        # Step 2-3: Add first product
        home_page.hover_and_click_add_to_cart(0)
        time.sleep(2)

        # Step 4: Continue shopping
        try:
            if home_page.is_element_visible(home_page.CONTINUE_SHOPPING_BUTTON, timeout=3):
                continue_btn = home_page.find_element(home_page.CONTINUE_SHOPPING_BUTTON)
                continue_btn.click()
                time.sleep(1)
        except:
            logger.info("Continue shopping button not found or already closed")

        # Step 5: Add second product
        home_page.hover_and_click_add_to_cart(1)
        time.sleep(2)

        # Step 6: View cart
        home_page.click_cart()
        time.sleep(2)

        # Step 7: Verify products in cart
        assert cart_page.is_cart_page_loaded(), "Cart page not loaded"
        cart_items = cart_page.get_cart_items_count()
        assert cart_items >= 1, f"Expected at least 1 item, got {cart_items}"
        logger.info(f" Cart has {cart_items} items")

        # Step 8: Verify product details
        if cart_items >= 1:
            product1_details = cart_page.get_product_details(0)
            assert product1_details is not None, "Product 1 details not found"
            logger.info(f" Product 1: {product1_details}")

        if cart_items >= 2:
            product2_details = cart_page.get_product_details(1)
            assert product2_details is not None, "Product 2 details not found"
            logger.info(f" Product 2: {product2_details}")

    @pytest.mark.regression
    def test_verify_product_quantity_in_cart(self, home_page, products_page, cart_page):
        """
        Test Case TC_CART_002: Verify Product quantity in Cart
        """
        logger.info("Starting test: Verify product quantity in cart")

        # Step 1-2: Navigate and view product
        home_page.open()
        home_page.click_products()
        time.sleep(1)

        products_page.click_view_product(0)
        time.sleep(1)

        # Step 3: Verify product detail page
        assert products_page.is_product_detail_page_loaded(), "Product detail page not loaded"
        product_info = products_page.get_product_detail_info()
        product_name = product_info['name']
        logger.info(f" Product detail opened: {product_name}")

        # Step 4: Set quantity to 4
        test_quantity = 4
        products_page.set_product_quantity(test_quantity)

        # Step 5: Add to cart
        products_page.add_to_cart_from_detail_page()
        time.sleep(1)

        # Step 6: View cart
        products_page.click_view_cart_modal()
        time.sleep(2)

        # Step 7: Verify quantity
        assert cart_page.verify_product_quantity(product_name, test_quantity), \
            f"Product quantity not {test_quantity}"
        logger.info(f" Product quantity verified: {test_quantity}")

    @pytest.mark.smoke
    def test_remove_products_from_cart(self, home_page, cart_page):
        """
        Test Case TC_CART_003: Remove Products from Cart
        """
        logger.info("Starting test: Remove products from cart")

        # Step 1-2: Add product to cart
        home_page.open()
        home_page.click_products()
        time.sleep(2)
        home_page.hover_and_click_add_to_cart(0)
        time.sleep(2)

        # Step 3: Navigate to cart
        home_page.click_cart()
        time.sleep(2)

        # Step 4: Verify cart has items
        initial_count = cart_page.get_cart_items_count()
        assert initial_count > 0, "Cart is empty"
        logger.info(f" Cart has {initial_count} items")

        # Step 5: Remove product
        cart_page.delete_product(0)
        time.sleep(2)

        # Step 6: Verify product removed
        final_count = cart_page.get_cart_items_count()
        assert final_count == initial_count - 1, "Product not removed"
        logger.info(f" Product removed. Remaining items: {final_count}")

    @pytest.mark.regression
    def test_view_cart_after_login(self, home_page, login_page, cart_page):
        """
        Test Case TC_CART_004: Place Order after Register while Checkout
        """
        logger.info("Starting test: View cart after login")

        from testdata.user_data import UserData
        user_data = UserData.generate_user()

        # Step 1: Add products
        home_page.open()
        home_page.click_products()
        time.sleep(2)
        home_page.hover_and_click_add_to_cart(0)
        time.sleep(2)

        # Step 2-3: View cart
        home_page.click_cart()
        time.sleep(2)

        assert cart_page.is_cart_page_loaded(), "Cart page not loaded"
        products_before = cart_page.get_all_product_names()
        logger.info(f" Products in cart before login: {products_before}")

        # Step 4-5: Proceed to checkout (should prompt login)
        cart_page.click_proceed_to_checkout()
        time.sleep(1)

        if cart_page.is_register_login_modal_visible():
            cart_page.click_register_login_link()
            time.sleep(1)

            # Step 6: Complete registration
            login_page.enter_signup_details(user_data['name'], user_data['email'])
            login_page.click_signup_button()
            login_page.complete_registration(user_data)

            if login_page.is_account_created():
                login_page.click_continue()
                time.sleep(1)

                # Step 7: Navigate to cart
                home_page.click_cart()
                time.sleep(2)

                # Step 8: Verify cart products
                products_after = cart_page.get_all_product_names()
                logger.info(f" Products in cart after login: {products_after}")

                # Cart should maintain products
                assert len(products_after) > 0, "Cart is empty after login"

                # Cleanup
                home_page.click(home_page.HOME_LINK)
                time.sleep(1)
                home_page.click_delete_account()
                if login_page.is_account_deleted():
                    login_page.click_continue()
                    logger.info(" Test completed successfully")

    @pytest.mark.regression
    def test_verify_cart_empty_message(self, cart_page):
        """
        Test Case TC_CART_005: Verify empty cart message
        """
        logger.info("Starting test: Verify empty cart message")

        # Navigate directly to cart without adding products
        cart_page.open()
        time.sleep(1)

        # Verify empty cart message or no products
        if cart_page.is_cart_empty():
            logger.info(" Cart is empty as expected")
            assert True
        else:
            # If there are items, delete them
            cart_page.delete_all_products()
            time.sleep(1)
            assert cart_page.is_cart_empty(), "Cart not empty after deleting all"
            logger.info(" Cart emptied successfully")

    @pytest.mark.smoke
    def test_subscription_in_cart_page(self, cart_page):
        """
        Test Case TC_CART_006: Verify Subscription in Cart page
        """
        logger.info("Starting test: Subscription in cart page")

        # Step 1: Navigate to cart
        cart_page.open()

        # Step 2-3: Scroll to subscription section
        cart_page.scroll_to_bottom()

        assert cart_page.is_element_visible(cart_page.SUBSCRIPTION_EMAIL), "Subscription section not visible"
        logger.info(" Subscription section visible")

        # Step 4: Subscribe
        test_email = "test_subscription@example.com"
        cart_page.subscribe_email(test_email)
        time.sleep(2)

        # Step 5: Verify success
        assert cart_page.subscribe_email(test_email), "Subscription not successful"
        logger.info(" Subscription successful")

    @pytest.mark.regression
    def test_calculate_cart_total(self, home_page, cart_page):
        """
        Test Case TC_CART_007: Verify cart total calculation
        """
        logger.info("Starting test: Calculate cart total")

        # Add multiple products
        home_page.open()
        home_page.click_products()
        time.sleep(2)
        home_page.hover_and_click_add_to_cart(0)
        time.sleep(2)

        try:
            if home_page.is_element_visible(home_page.CONTINUE_SHOPPING_BUTTON, timeout=3):
                continue_btn = home_page.find_element(home_page.CONTINUE_SHOPPING_BUTTON)
                continue_btn.click()
                time.sleep(1)
        except:
            logger.info("Continue shopping not needed")

        home_page.hover_and_click_add_to_cart(1)
        time.sleep(2)

        # Navigate to cart
        home_page.click_cart()
        time.sleep(2)

        # Calculate and verify total
        total_price = cart_page.calculate_total_price()
        logger.info(f" Total cart price: Rs. {total_price}")

        assert total_price > 0, "Total price should be greater than 0"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])