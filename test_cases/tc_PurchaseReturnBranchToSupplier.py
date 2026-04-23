import allure
from pages.login_page import LoginPage
from pages.authority_matrix_page import AuthorityMatrixPage
import logging
import time 
logger = logging.getLogger(__name__)

@allure.epic("Authority Matrix")
@allure.feature("Purchase Return Branch to Supplier")
@allure.story("User views Authority Matrix via myTawasol")

def test_PurchaseReturnBranchToSupplier(driver, test_data): 
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
    # -- Navigation 
    authority_matrix_page.navigate_to_purchase_return_branch_to_supplier()
    logger.info("No Data Available")



