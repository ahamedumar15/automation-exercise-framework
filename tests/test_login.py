
import pytest
from testdata.user_data import UserData, LoginCredentials
from utilities.logger import get_logger

logger = get_logger(__name__)


@pytest.mark.smoke
@pytest.mark.regression
class TestLogin:
    """Test class for login scenarios"""

    def test_login_with_valid_credentials(self, home_page, login_page):
        """
        Test Case TC_LG_001: Login User with correct email and password
        """
        logger.info("Starting test: Login with valid credentials")

        # First, create a user to login with
        user_data = UserData.generate_user()

        # Step 1-2: Open home page
        home_page.open()
        assert home_page.is_home_page_loaded(), "Home page not loaded"

        # Register user first
        home_page.click_signup_login()
        login_page.enter_signup_details(user_data['name'], user_data['email'])
        login_page.click_signup_button()
        login_page.complete_registration(user_data)

        if login_page.is_account_created():
            login_page.click_continue()
            assert home_page.is_logged_in(), "User not logged in after continue"

            # Logout
            home_page.click_logout()
            assert login_page.is_login_form_visible(), "Login form not visible after logout"

            # Step 3-4: Navigate to login page
            assert login_page.is_login_form_visible(), "Login form not visible"
            logger.info("Login form is visible")

            # Step 5-6: Login with credentials
            login_page.login(user_data['email'], user_data['password'])

            # Step 7: Verify login successful
            assert home_page.is_logged_in(), "User not logged in"
            username = home_page.get_logged_in_username()
            assert username == user_data['name'], f"Username mismatch"
            logger.info(f"Successfully logged in as: {username}")

            # Cleanup: Delete account
            home_page.click_delete_account()
            if login_page.is_account_deleted():
                login_page.click_continue()
                logger.info("Test completed successfully")

    @pytest.mark.regression
    def test_login_with_invalid_credentials(self, home_page, login_page):
        """
        Test Case TC_LG_002: Login User with incorrect email and password
        """
        logger.info("Starting test: Login with invalid credentials")

        # Step 1-2: Navigate to login page
        home_page.open()
        home_page.click_signup_login()

        # Step 3: Verify login form
        assert login_page.is_login_form_visible(), "Login form not visible"
        logger.info("Login form is visible")

        # Step 4-5: Login with invalid credentials
        login_page.login("invalid@test.com", "WrongPassword123")

        # Step 6: Verify error message
        assert login_page.is_login_error_displayed(), "Login error not displayed"
        error_message = login_page.get_login_error_message()
        assert "incorrect" in error_message.lower(), f"Unexpected error message: {error_message}"
        logger.info(f"Error message displayed: {error_message}")

    @pytest.mark.regression
    def test_logout_user(self, home_page, login_page):
        """
        Test Case TC_LG_003: Logout User
        """
        logger.info("Starting test: Logout user")

        # Create and login user
        user_data = UserData.generate_user()

        home_page.open()
        home_page.click_signup_login()

        # Register
        login_page.enter_signup_details(user_data['name'], user_data['email'])
        login_page.click_signup_button()
        login_page.complete_registration(user_data)

        if login_page.is_account_created():
            login_page.click_continue()
            assert home_page.is_logged_in(), "User not logged in after continue"

            # Verify logged in
            assert home_page.is_logged_in(), "User not logged in"
            logger.info("User logged in successfully")

            # Logout
            home_page.click_logout()
            assert login_page.is_login_form_visible(), "Not redirected to login page"

            # Verify redirected to login page
            assert login_page.is_login_form_visible(), "Not redirected to login page"
            logger.info("User logged out and redirected to login page")

            # Cleanup: Login and delete account
            login_page.login(user_data['email'], user_data['password'])

            if home_page.is_logged_in():
                home_page.click_delete_account()
                if login_page.is_account_deleted():
                    login_page.click_continue()
                    logger.info("Test completed successfully")

    @pytest.mark.sanity
    def test_login_form_validation(self, home_page, login_page):
        """
        Test Case TC_LG_004: Verify login form validations
        """
        logger.info("Starting test: Login form validation")

        home_page.open()
        home_page.click_signup_login()

        # Verify login form elements
        assert login_page.is_login_form_visible(), "Login form not visible"
        assert login_page.is_element_visible(login_page.LOGIN_EMAIL), "Email field not visible"
        assert login_page.is_element_visible(login_page.LOGIN_PASSWORD), "Password field not visible"
        assert login_page.is_element_visible(login_page.LOGIN_BUTTON), "Login button not visible"

        logger.info("All login form elements are present")

    @pytest.mark.regression
    def test_login_with_empty_credentials(self, home_page, login_page):
        """
        Test Case TC_LG_005: Login with empty email and password
        """
        logger.info("Starting test: Login with empty credentials")

        home_page.open()
        home_page.click_signup_login()

        # Try to login with empty fields
        login_page.login("", "")

        # Should remain on login page
        assert login_page.is_login_form_visible(), "Should remain on login page"
        logger.info("Login prevented with empty credentials")

    @pytest.mark.regression
    def test_login_remembers_last_session(self, home_page, login_page):
        """
        Test Case TC_LG_006: Verify login state persistence
        """
        logger.info("Starting test: Login state persistence")

        # Create user
        user_data = UserData.generate_user()

        home_page.open()
        home_page.click_signup_login()

        login_page.enter_signup_details(user_data['name'], user_data['email'])
        login_page.click_signup_button()
        login_page.complete_registration(user_data)

        if login_page.is_account_created():
            login_page.click_continue()
            assert home_page.is_logged_in(), "User not logged in after continue"

            # Verify logged in
            assert home_page.is_logged_in(), "User not logged in"

            # Navigate to different page and back
            home_page.click_products()
            assert home_page.wait_helper.wait_for_url_contains("/products"), "Products page did not load"
            home_page.click(home_page.HOME_LINK)
            assert home_page.is_home_page_loaded(), "Home page did not reload"

            # Should still be logged in
            assert home_page.is_logged_in(), "User session not maintained"
            logger.info("Login state persisted across navigation")

            # Cleanup
            home_page.click_delete_account()
            if login_page.is_account_deleted():
                login_page.click_continue()
                logger.info("Test completed successfully")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])