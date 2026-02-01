
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from config.config import LOGIN_URL
from utilities.logger import get_logger

logger = get_logger(__name__)


class LoginPage(BasePage):
    """Login and Signup page locators and methods"""

    # Signup Section Locators
    SIGNUP_HEADING = (By.XPATH, "//h2[contains(text(), 'New User Signup!')]")
    SIGNUP_NAME = (By.CSS_SELECTOR, "input[data-qa='signup-name']")
    SIGNUP_EMAIL = (By.CSS_SELECTOR, "input[data-qa='signup-email']")
    SIGNUP_BUTTON = (By.CSS_SELECTOR, "button[data-qa='signup-button']")

    # Login Section Locators
    LOGIN_HEADING = (By.XPATH, "//h2[contains(text(), 'Login to your account')]")
    LOGIN_EMAIL = (By.CSS_SELECTOR, "input[data-qa='login-email']")
    LOGIN_PASSWORD = (By.CSS_SELECTOR, "input[data-qa='login-password']")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button[data-qa='login-button']")

    # Account Information Form
    ACCOUNT_INFO_HEADING = (By.XPATH, "//b[contains(text(), 'Enter Account Information')]")
    TITLE_MR = (By.ID, "id_gender1")
    TITLE_MRS = (By.ID, "id_gender2")
    PASSWORD = (By.ID, "password")
    DAY_DROPDOWN = (By.ID, "days")
    MONTH_DROPDOWN = (By.ID, "months")
    YEAR_DROPDOWN = (By.ID, "years")
    NEWSLETTER_CHECKBOX = (By.ID, "newsletter")
    SPECIAL_OFFERS_CHECKBOX = (By.ID, "optin")

    # Address Information
    FIRST_NAME = (By.ID, "first_name")
    LAST_NAME = (By.ID, "last_name")
    COMPANY = (By.ID, "company")
    ADDRESS1 = (By.ID, "address1")
    ADDRESS2 = (By.ID, "address2")
    COUNTRY_DROPDOWN = (By.ID, "country")
    STATE = (By.ID, "state")
    CITY = (By.ID, "city")
    ZIPCODE = (By.ID, "zipcode")
    MOBILE_NUMBER = (By.ID, "mobile_number")

    # Buttons
    CREATE_ACCOUNT_BUTTON = (By.CSS_SELECTOR, "button[data-qa='create-account']")
    CONTINUE_BUTTON = (By.CSS_SELECTOR, "a[data-qa='continue-button']")

    # Messages
    ACCOUNT_CREATED_HEADING = (By.CSS_SELECTOR, "h2[data-qa='account-created']")
    ACCOUNT_DELETED_HEADING = (By.CSS_SELECTOR, "h2[data-qa='account-deleted']")
    LOGIN_ERROR_MESSAGE = (By.CSS_SELECTOR, "p[style*='color: red']")
    EMAIL_EXIST_ERROR = (By.XPATH, "//p[contains(text(), 'Email Address already exist!')]")

    def __init__(self, driver):
        super().__init__(driver)

    def open(self):
        """Open login/signup page"""
        self.open_url(LOGIN_URL)
        logger.info("Login/Signup page opened")

    def is_signup_form_visible(self):
        """Check if signup form is visible"""
        return self.is_element_visible(self.SIGNUP_HEADING)

    def is_login_form_visible(self):
        """Check if login form is visible"""
        return self.is_element_visible(self.LOGIN_HEADING)

    def enter_signup_details(self, name, email):
        """Enter name and email in signup form"""
        self.send_keys(self.SIGNUP_NAME, name)
        self.send_keys(self.SIGNUP_EMAIL, email)
        logger.info(f"Entered signup details - Name: {name}, Email: {email}")

    def click_signup_button(self):
        """Click on signup button"""
        self.click(self.SIGNUP_BUTTON)
        logger.info("Clicked on Signup button")

    def is_account_info_page_visible(self):
        """Check if account information page is visible"""
        return self.is_element_visible(self.ACCOUNT_INFO_HEADING)

    def fill_account_information(self, title, password, day, month, year,
                                 newsletter=False, special_offers=False):
        """Fill account information form"""
        # Select title
        if title.lower() == "mr":
            self.click(self.TITLE_MR)
        else:
            self.click(self.TITLE_MRS)

        # Enter password
        self.send_keys(self.PASSWORD, password)

        # Select date of birth
        self.select_dropdown_by_value(self.DAY_DROPDOWN, str(day))
        self.select_dropdown_by_value(self.MONTH_DROPDOWN, str(month))
        self.select_dropdown_by_value(self.YEAR_DROPDOWN, str(year))

        # Checkboxes
        if newsletter:
            self.click(self.NEWSLETTER_CHECKBOX)
        if special_offers:
            self.click(self.SPECIAL_OFFERS_CHECKBOX)

        logger.info("Filled account information")

    def fill_address_information(self, first_name, last_name, company, address1,
                                 address2, country, state, city, zipcode, mobile):
        """Fill address information form"""
        self.send_keys(self.FIRST_NAME, first_name)
        self.send_keys(self.LAST_NAME, last_name)
        self.send_keys(self.COMPANY, company)
        self.send_keys(self.ADDRESS1, address1)
        self.send_keys(self.ADDRESS2, address2)
        self.select_dropdown_by_text(self.COUNTRY_DROPDOWN, country)
        self.send_keys(self.STATE, state)
        self.send_keys(self.CITY, city)
        self.send_keys(self.ZIPCODE, zipcode)
        self.send_keys(self.MOBILE_NUMBER, mobile)
        logger.info("Filled address information")

    def click_create_account(self):
        """Click on Create Account button"""
        self.scroll_to_element(self.CREATE_ACCOUNT_BUTTON)
        self.click(self.CREATE_ACCOUNT_BUTTON)
        logger.info("Clicked on Create Account button")

    def is_account_created(self):
        """Check if account created message is visible"""
        return self.is_element_visible(self.ACCOUNT_CREATED_HEADING, timeout=10)

    def get_account_created_message(self):
        """Get account created message"""
        if self.is_account_created():
            return self.get_text(self.ACCOUNT_CREATED_HEADING)
        return None

    def click_continue(self):
        """Click on Continue button"""
        self.click(self.CONTINUE_BUTTON)
        logger.info("Clicked on Continue button")

    def is_account_deleted(self):
        """Check if account deleted message is visible"""
        return self.is_element_visible(self.ACCOUNT_DELETED_HEADING, timeout=10)

    def get_account_deleted_message(self):
        """Get account deleted message"""
        if self.is_account_deleted():
            return self.get_text(self.ACCOUNT_DELETED_HEADING)
        return None

    def login(self, email, password):
        """Perform login with email and password"""
        self.send_keys(self.LOGIN_EMAIL, email)
        self.send_keys(self.LOGIN_PASSWORD, password)
        self.click(self.LOGIN_BUTTON)
        logger.info(f"Attempted login with email: {email}")

    def is_login_error_displayed(self):
        """Check if login error message is displayed"""
        return self.is_element_visible(self.LOGIN_ERROR_MESSAGE, timeout=5)

    def get_login_error_message(self):
        """Get login error message"""
        if self.is_login_error_displayed():
            return self.get_text(self.LOGIN_ERROR_MESSAGE)
        return None

    def is_email_exist_error_displayed(self):
        """Check if email already exist error is displayed"""
        return self.is_element_visible(self.EMAIL_EXIST_ERROR, timeout=5)

    def complete_registration(self, user_data):
        """
        Complete full registration process

        Args:
            user_data (dict): Dictionary containing all user information
        """
        self.fill_account_information(
            title=user_data['title'],
            password=user_data['password'],
            day=user_data['day'],
            month=user_data['month'],
            year=user_data['year'],
            newsletter=user_data.get('newsletter', False),
            special_offers=user_data.get('special_offers', False)
        )

        self.fill_address_information(
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            company=user_data.get('company', ''),
            address1=user_data['address1'],
            address2=user_data.get('address2', ''),
            country=user_data['country'],
            state=user_data['state'],
            city=user_data['city'],
            zipcode=user_data['zipcode'],
            mobile=user_data['mobile']
        )

        self.click_create_account()
        logger.info("Completed registration form")