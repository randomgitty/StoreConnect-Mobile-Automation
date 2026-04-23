from pages.eros_discount_voucher_page import EROS_DiscountVoucherPage
from pages.login_page import LoginPage
from pages.authority_matrix_page import AuthorityMatrixPage
from pages.logout_page import LogoutPage
from pages.change_branch_page import ChangeBranchPage
from pages.login_page import LoginAsPartner
from pages.lpo_notifications_page import LpoNotificationsPage
from utilities.login_manager import LoginManager
from utilities.range_helper import get_approvers_for_amount
import logging
import time 
import json 
logger = logging.getLogger(__name__)

def test_LPO_Notification_flow(driver, test_data):
    credentials = test_data['login_credentials']
    username = credentials['username']
    password = credentials['password']
    remember_me = credentials.get('remember_me', True)
    # -- Login
    login_page = LoginPage(driver)
    home_page = login_page.login_and_go_to_home(username=username, password=password, remember_me=remember_me)
    logger.info(f"✅ Login SUCCESS: Logged in as {username}")
    time.sleep(3)
    home_page.navigate_to_lpo_notifications()  
    lpo_notifications_page = LpoNotificationsPage(driver)
    lpo_notifications_page.complete_lpo_notifications_flow()
