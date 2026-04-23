import pytest
import logging
import allure
from pages.change_branch_page import ChangeBranchPage
from pages.login_page import LoginPage

# Use logger with module name
logger = logging.getLogger(__name__)

@allure.epic("Change Branch")
@allure.feature("Change Branch")
@allure.story("User changes branch via myTawasol") 

def test_ChangeBranchFlow(driver, test_data):

    credentials = test_data['login_credentials']
    username = credentials['username']
    password = credentials['password']
    remember_me = credentials.get('remember_me', True)
    logger.info(f"Starting login test for user: {username}")
    login_page = LoginPage(driver)
    login_page.complete_login_flow(username=username, password=password, remember_me=remember_me)
    assert login_page.is_logged_in(), "Login failed: user not redirected to dashboard"
    logger.info("✅ Login successful - dashboard loaded")
    branch = ChangeBranchPage(driver)
    branch.complete_change_branch_flow(branch_name="Al Warqa")
    logger.info(f"✅ Changed branch")