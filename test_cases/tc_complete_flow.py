import pytest
import logging
import allure
from pages.login_page import LoginPage
from pages.base_page import BasePage 
from pages.product_details_page import ProductDetailsPage
from pages.change_branch_page import ChangeBranchPage

# Use logger with module name
logger = logging.getLogger(__name__)

@allure.epic("Authentication")
@allure.feature("Login")
@allure.story("User logs in via myTawasol with valid credentials")

def test_valid_login(driver, test_data):
    """
    Test login with valid credentials from test_data.json
    """
    credentials = test_data['login_credentials']
    username = credentials['username']
    password = credentials['password']
    remember_me = credentials.get('remember_me', True)
    logger.info(f"Starting login test for user: {username}")
    login_page = LoginPage(driver)
    login_page.complete_login_flow(username=username, password=password, remember_me=remember_me)
    assert login_page.is_logged_in(), "Login failed: user not redirected to dashboard"
    logger.info("✅ Login successful - dashboard loaded")

def test_product_details_flow(driver, test_data):
    test_valid_login(driver, test_data)
    product_data = test_data['product_dimension']
    product_code = product_data.get('product_code', product_data.get('product_barcode'))
    logger.info(f"Starting product details test for product: {product_code}")
    product_details_page = ProductDetailsPage(driver)
    product_details_page.complete_product_details_flow(product_code=product_code)
    logger.info("✅ Product details flow completed successfully")

def test_change_branch_flow(driver, test_data):
    test_valid_login(driver, test_data)
    branch = ChangeBranchPage(driver)
    branch.complete_change_branch_flow(branch_name="Al Warqa")
    logger.info(f"✅ Changed branch")