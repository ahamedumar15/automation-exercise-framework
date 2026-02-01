"""
Pytest configuration and fixtures
"""
import pytest
from selenium import webdriver
from utilities.driver_factory import DriverFactory
from utilities.logger import get_logger
from utilities.screenshot import ScreenshotHelper
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from pages.cart_page import CartPage
from config.config import BROWSER, SCREENSHOT_ON_FAILURE

logger = get_logger(__name__)


@pytest.fixture(scope="function")
def driver(request):
    """
    WebDriver fixture for each test
    Setup and teardown browser for each test
    """
    logger.info("=" * 80)
    logger.info(f"Starting test: {request.node.name}")
    logger.info("=" * 80)

    # Initialize driver
    driver = DriverFactory.get_driver(BROWSER)

    yield driver

    # Teardown
    if request.node.rep_call.failed and SCREENSHOT_ON_FAILURE:
        ScreenshotHelper.take_screenshot(driver, request.node.name)

    logger.info(f"Test completed: {request.node.name}")
    DriverFactory.quit_driver(driver)


@pytest.fixture(scope="function")
def home_page(driver):
    """HomePage fixture"""
    return HomePage(driver)


@pytest.fixture(scope="function")
def login_page(driver):
    """LoginPage fixture"""
    return LoginPage(driver)


@pytest.fixture(scope="function")
def products_page(driver):
    """ProductsPage fixture"""
    return ProductsPage(driver)


@pytest.fixture(scope="function")
def cart_page(driver):
    """CartPage fixture"""
    return CartPage(driver)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook to capture test result for screenshot on failure
    """
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


def pytest_configure(config):
    """Configure pytest with custom markers"""
    config.addinivalue_line("markers", "smoke: Mark test as smoke test")
    config.addinivalue_line("markers", "regression: Mark test as regression test")
    config.addinivalue_line("markers", "sanity: Mark test as sanity test")
    config.addinivalue_line("markers", "e2e: Mark test as end-to-end test")


def pytest_html_report_title(report):
    """Customize HTML report title"""
    report.title = "Automation Exercise Test Report"


@pytest.fixture(scope="session", autouse=True)
def test_suite_setup():
    """Setup before all tests"""
    logger.info("=" * 80)
    logger.info("TEST SUITE EXECUTION STARTED")
    logger.info("=" * 80)
    yield
    logger.info("=" * 80)
    logger.info("TEST SUITE EXECUTION COMPLETED")
    logger.info("=" * 80)