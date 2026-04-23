import allure
from pages.login_page import LoginPage
from pages.authority_matrix_page import AuthorityMatrixPage
from pages.logout_page import LogoutPage
from utilities.login_manager import LoginManager
from utilities.range_helper import get_approvers_for_amount
import logging
import time 
import json 
logger = logging.getLogger(__name__)

@allure.epic("Authority Matrix")
@allure.feature("Authority Matrix")
@allure.story("User views Authority Matrix via myTawasol")

def test_authority_matrix(driver, test_data): 
    credentials = test_data['login_credentials']
    username = credentials['username']
    password = credentials['password']
    remember_me = credentials.get('remember_me', True)
    # -- Login
    login_page = LoginPage(driver)
    home_page = login_page.login_and_go_to_home(username=username, password=password, remember_me=remember_me)
    logger.info(f"✅ Login SUCCESS: Logged in as {username}")
    time.sleep(4)
    # -- Navigate to Authority Matrix
  
    home_page.navigate_to_authority_matrix()
    authority_matrix_page = AuthorityMatrixPage(driver)
    authority_matrix_page.get_page_title()
    available_modules = authority_matrix_page.get_available_modules()
    logger.info(f"Total Modules : {len(available_modules)}")

    # -- Navigation 
    authority_matrix_page.complete_POS_return_customer_flow()
    logger.info("Logout SUCCESS") 
    
    # -- Logout Flow 
    logout_page = LogoutPage(driver)
    logout_page.logout_via_exit_icon()
    assert logout_page.is_logged_out(), "Logout failed - login page not displayed" 
    
