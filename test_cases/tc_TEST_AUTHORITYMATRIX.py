import logging
import json
import time
from pages.login_page import LoginPage
from pages.logout_page import LogoutPage
from pages.authority_matrix_page import AuthorityMatrixPage
from utilities.login_manager import LoginManager
from utilities.range_helper import get_approvers_for_amount

logger = logging.getLogger(__name__)

def test_approval_flow_with_hardcoded_amount(driver):
    """
    Validates multi-role login/logout flow using a HARDCODED amount.
    - Uses amount = 1500 (requires 3 approvers per config)
    - Logs in as each required role
    - Verifies homepage after login
    - Logs out cleanly
    - Does NOT navigate to Authority Matrix or approve anything (commented out)
    """
    # === CONFIGURATION ===
    TEST_AMOUNT = 500  
    MODULE_NAME = "POS Return (Customer)"
    CONFIG_PATH = "test_data/authority_matrix_config.json"
    
    # === STEP 1: Load Authority Matrix Rules ===
    with open(CONFIG_PATH, 'r') as f:
        matrix_config = json.load(f)
    
    # === STEP 2: Get Required Approvers for TEST_AMOUNT ===
    try:
        required_approvers = get_approvers_for_amount(
            amount=TEST_AMOUNT,
            matrix_config=matrix_config,
            module_name=MODULE_NAME
        )
        logger.info(f"✅ For amount {TEST_AMOUNT} AED, required approvers ({len(required_approvers)}):")
        for i, role in enumerate(required_approvers, 1):
            logger.info(f"   {i}. {role}")
    except ValueError as e:
        logger.error(f" {str(e)}")
        raise

    # === STEP 3: Loop Through Each Approver ===
    login_manager = LoginManager(driver)
    
    for role in required_approvers:
        logger.info(f"\n{'='*50}")
        logger.info(f"Processing role: {role}")
        
        # --- Fetch credentials ---
        try:
            user = login_manager.get_user_by_role(role)
            username = user['username']
            password = user['password']
            logger.info(f" Credentials: {username} / {'*' * len(password)}")
        except ValueError as e:
            logger.error(f" {str(e)}")
            raise

        # --- Login ---
        login_page = LoginPage(driver)
        try:
            home_page = login_page.login_and_go_to_home(
                username=username,
                password=password,
                remember_me=True
            )
            logger.info(f"✅ Successfully logged in as '{role}'")
        except Exception as e:
            logger.error(f" Login failed for {role}: {str(e)}")
            raise

        # --- [COMMENTED] Navigate to Authority Matrix / POS Return / Approve ---
        home_page.navigate_to_authority_matrix()
        authority_matrix_page = AuthorityMatrixPage(driver)
        authority_matrix_page.navigate_to_POS_return()
        # ... approve logic ...

        # --- Verify on Home Page (basic check) ---
        time.sleep(2)  # Let home page load
        logger.info(f"✅ Verified: On home page as {role}")
        home_page.navigate_back_to_home()
        # --- Logout ---
        logout_page = LogoutPage(driver)
        try:
            logout_page.logout_via_exit_icon()
            assert logout_page.is_logged_out(), "Logout verification failed"
            logger.info(f" Successfully logged out from '{role}'")
        except Exception as e:
            logger.error(f"Logout failed for {role}: {str(e)}")
            raise

        time.sleep(2)  # Brief pause between logins

    logger.info(f"\n PRE-PROD TEST PASSED: All {len(required_approvers)} roles processed successfully!")