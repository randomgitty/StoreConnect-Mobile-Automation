from pages.eros_discount_voucher_page import EROS_DiscountVoucherPage
from pages.login_page import LoginPage
from pages.authority_matrix_page import AuthorityMatrixPage
from pages.logout_page import LogoutPage
from pages.change_branch_page import ChangeBranchPage
from pages.login_page import LoginAsPartner
from utilities.login_manager import LoginManager
from utilities.range_helper import get_approvers_for_amount
import logging
import time 
import json 
import allure 
logger = logging.getLogger(__name__)

@allure.epic("EROS Discount Voucher")
@allure.feature("EROS Discount Voucher")
@allure.story("User views EROS Discount Voucher via myTawasol")

def test_EROS_DiscountVoucher(driver, test_data):
    partner = test_data["login_as_partner"]
    eros_test_data = test_data['eros_discount_voucher']
    credentials = test_data['login_credentials']
    username = credentials['username']
    password = credentials['password']
    remember_me = credentials.get('remember_me', True)
    
    # -- Login
    login_page = LoginPage(driver)
    home_page = login_page.login_and_go_to_home(username=username, password=password, remember_me=remember_me)
    logger.info(f"✅ Login SUCCESS: Logged in as {username}")
    time.sleep(3)

    # -- Navigate to EROS Discount Voucher
    change_branch_page = ChangeBranchPage(driver)
    change_branch_page.complete_change_branch_flow("Al Warqa")  
    home_page.navigate_to_eros_discount_voucher()  
    eros_discount_voucher_page = EROS_DiscountVoucherPage(driver)
    eros_discount_voucher_page.complete_eros_discount_voucher_flow(customer_identification_by="Tamayaz Card", tamayaz_id=eros_test_data['tamayaz_id'], phone_number=eros_test_data['phone_number'], barcode=eros_test_data['barcode'], discount_type=True, amount=eros_test_data['discount_amount'], percentage=eros_test_data['discount_percentage']) 
    
    LogoutPage(driver).logout()

    # =================================================================
    # 3. PARTNER LOGIN & APPROVE
    # =================================================================

    LoginAsPartner(driver).login_as_partner(partner["partner_username"], partner["partner_password"]) 
    change_branch_page = ChangeBranchPage(driver)
    change_branch_page.complete_change_branch_flow("Al Warqa")   
    home_page.navigate_to_eros_discount_voucher()
    #eros_discount_voucher_page.open_request_by_barcode(eros_test_data['barcode'])
    eros_discount_voucher_page.open_request()
    eros_discount_voucher_page.approve_request()



