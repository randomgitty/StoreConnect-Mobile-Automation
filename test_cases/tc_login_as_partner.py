import pytest
import logging
import allure
from pages.home_page import HomePage
from pages.login_page import LoginPage, LoginAsPartner
from pages.base_page import BasePage 
from pages.product_details_page import ProductDetailsPage
from pages.change_branch_page import ChangeBranchPage

# Use logger with module name
logger = logging.getLogger(__name__)

@allure.epic("Authentication")
@allure.feature("Login")
@allure.story("User logs in as Partner via myTawasol with valid credentials")

def test_login_as_partner(driver, test_data):
    """
    Test login as Partner with valid credentials from test_data.json
    """
    credentials = test_data['login_as_partner']
    partner_username = credentials['partner_username']
    partner_password = credentials['partner_password']
    login_partner_page = LoginAsPartner(driver)
    logger.info(f"Starting login as Partner test ")
    home_page = login_partner_page.login_as_partner(
        partner_username=partner_username,
        partner_password=partner_password)
    assert isinstance(home_page, HomePage), "Login failed – did not reach HomePage"
    logger.info("Login as Partner test PASSED")