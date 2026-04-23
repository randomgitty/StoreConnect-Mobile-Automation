import allure
from pages.login_page import LoginPage
from pages.product_facing_page import ProductFacingPage
from pages.change_branch_page import ChangeBranchPage
import logging
import time

logger = logging.getLogger(__name__)


@allure.epic("Product Facing")
@allure.feature("Product Facing")
@allure.story("Complete Product Facing Flow with QR Scan and Add Facing")
def test_product_facing_flow(driver, test_data):
    """
    Test Complete Product Facing Flow:
    1. Login
    2. Change Branch
    3. Navigate to Product Facing
    4. Scan Gondola QR Code
    5. Click Add Facing
    6. Enter Barcode and Search
    7. Enter Facing and Rows Count
    8. Save
    """
    # Load test data
    credentials = test_data['login_credentials']
    product_facing_data = test_data['product_facing']
    
    username = credentials['username']
    password = credentials['password']
    remember_me = credentials.get('remember_me', True)
    
    # -- Login
    login_page = LoginPage(driver)
    home_page = login_page.login_and_go_to_home(
        username=username, 
        password=password, 
        remember_me=remember_me
    )
    logger.info(f"✅ Login SUCCESS: Logged in as {username}")
    time.sleep(3)
    
    # -- Change Branch to Mirdiff
    branch = ChangeBranchPage(driver)
    branch.complete_change_branch_flow(branch_name="Mirdiff")
    logger.info("✅ Changed branch to Mirdiff")
    
    # -- Navigate to Product Facing
    home_page.navigate_to_product_facing()
    logger.info("✅ Navigated to Product Facing module")
    time.sleep(3)
    
    # -- Initialize Product Facing Page
    product_facing_page = ProductFacingPage(driver)
    
    # -- Verify QR Code Scan (as shown in screenshot)
    logger.info("📱 Verifying Gondola QR Code Scan...")
    product_facing_page.verify_qr_scan_success()
    time.sleep(3)
    
    # -- Complete Add Facing Flow
    barcode = product_facing_data['barcode']
    facing_count = product_facing_data['facing_count']
    rows_count = product_facing_data['rows_count']
    
    logger.info("Starting Add Facing Flow...")
    product_facing_page.complete_add_facing_flow(
        barcode=barcode,
        facing_count=facing_count,
        rows_count=rows_count
    )
    
    logger.info("✅✅✅ PRODUCT FACING TEST COMPLETED SUCCESSFULLY ✅✅✅")
    
    # Final screenshot
    allure.attach(
        driver.get_screenshot_as_png(),
        name="Final Product Facing Screen",
        attachment_type=allure.attachment_type.PNG
    )

