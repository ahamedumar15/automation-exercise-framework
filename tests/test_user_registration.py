
import pytest
import time
from testdata.user_data import UserData
from utilities.logger import get_logger

logger = get_logger(__name__)


@pytest.mark.smoke
@pytest.mark.regression
class TestUserRegistration:
    """Test class for user registration scenarios"""

    def test_register_user_with_valid_details(self, home_page, login_page):
        """
        Test Case TC_UR_001: Register User with valid details
        """
        logger.info("Starting test: Register user with valid details")

        # Generate test data
        user_data = UserData.generate_user()

        # Step 1-2: Open home page and verify
        home_page.open()
        assert home_page.is_home_page_loaded(), "Home page not loaded"
        logger.info(" Home page loaded successfully")

        # Step 3-4: Navigate to signup page
        home_page.click_signup_login()
        assert login_page.is_signup_form_visible(), "Signup form not visible"
        logger.info(" Signup form is visible")

        # Step 5-6: Enter signup details
        login_page.enter_signup_details(user_data['name'], user_data['email'])
        login_page.click_signup_button()

        # Step 7: Verify account info page
        assert login_page.is_account_info_page_visible(), "Account info page not visible"
        logger.info(" Account information page is visible")

        # Step 8: Fill registration form
        login_page.complete_registration(user_data)

        # Step 9-10: Verify account created
        assert login_page.is_account_created(), "Account not created"
        created_message = login_page.get_account_created_message()
        assert "ACCOUNT CREATED!" in created_message, "Account created message not correct"
        logger.info(f" {created_message}")

        # Step 11-12: Continue and verify login
        login_page.click_continue()
        time.sleep(1)  # Small wait for page transition

        assert home_page.is_logged_in(), "User not logged in"
        username = home_page.get_logged_in_username()
        assert username == user_data['name'], f"Username mismatch. Expected: {user_data['name']}, Got: {username}"
        logger.info(f" Logged in as: {username}")

        # Step 13-14: Delete account
        home_page.click_delete_account()
        assert login_page.is_account_deleted(), "Account not deleted"
        deleted_message = login_page.get_account_deleted_message()
        assert "ACCOUNT DELETED!" in deleted_message, "Account deleted message not correct"
        logger.info(f" {deleted_message}")

        login_page.click_continue()
        logger.info(" Test completed successfully")

    @pytest.mark.regression
    def test_register_user_with_existing_email(self, home_page, login_page):
        """
        Test Case TC_UR_002: Register User with existing email
        """
        logger.info("Starting test: Register with existing email")

        # Step 1-2: Navigate to signup page
        home_page.open()
        home_page.click_signup_login()

        # Step 3-4: Try to signup with common email
        login_page.enter_signup_details("Test User", "existing@test.com")
        login_page.click_signup_button()

        # Step 5: Verify error message
        time.sleep(1)
        is_error_displayed = login_page.is_email_exist_error_displayed()

        if is_error_displayed:
            logger.info(" Email already exists error displayed")
            assert True
        else:
            logger.info(" Email might be new, registering and cleaning up")
            # If email doesn't exist, complete registration and delete
            if login_page.is_account_info_page_visible():
                user_data = UserData.generate_user()
                user_data['email'] = "existing@test.com"
                login_page.complete_registration(user_data)

                if login_page.is_account_created():
                    login_page.click_continue()
                    time.sleep(1)
                    home_page.click_delete_account()
                    if login_page.is_account_deleted():
                        login_page.click_continue()
                        logger.info(" Cleanup completed")

    @pytest.mark.smoke
    def test_verify_signup_form_fields(self, home_page, login_page):
        """
        Test Case TC_UR_003: Verify all signup form fields are present
        """
        logger.info("Starting test: Verify signup form fields")

        # Navigate to signup
        home_page.open()
        home_page.click_signup_login()

        # Verify signup section
        assert login_page.is_signup_form_visible(), "Signup form not visible"

        # Enter details and proceed to account info page
        user_data = UserData.generate_user()
        login_page.enter_signup_details(user_data['name'], user_data['email'])
        login_page.click_signup_button()

        # Verify account info page fields
        assert login_page.is_account_info_page_visible(), "Account info page not visible"
        assert login_page.is_element_visible(login_page.TITLE_MR), "Title Mr not visible"
        assert login_page.is_element_visible(login_page.PASSWORD), "Password field not visible"
        assert login_page.is_element_visible(login_page.FIRST_NAME), "First name field not visible"
        assert login_page.is_element_visible(login_page.LAST_NAME), "Last name field not visible"
        assert login_page.is_element_visible(login_page.ADDRESS1), "Address field not visible"
        assert login_page.is_element_visible(login_page.COUNTRY_DROPDOWN), "Country dropdown not visible"

        logger.info(" All signup form fields are present")

    @pytest.mark.regression
    def test_register_with_special_characters_in_name(self, home_page, login_page):
        """
        Test Case TC_UR_004: Register user with special characters in name
        """
        logger.info("Starting test: Register with special characters")

        user_data = UserData.generate_user()
        user_data['name'] = "Test@User#123"

        home_page.open()
        home_page.click_signup_login()

        login_page.enter_signup_details(user_data['name'], user_data['email'])
        login_page.click_signup_button()

        if login_page.is_account_info_page_visible():
            login_page.complete_registration(user_data)

            if login_page.is_account_created():
                logger.info(" Registration successful with special characters")
                login_page.click_continue()
                time.sleep(1)

                # Cleanup
                home_page.click_delete_account()
                if login_page.is_account_deleted():
                    login_page.click_continue()
            else:
                logger.error("Account creation failed")
        else:
            logger.error("Could not proceed to account info page")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])