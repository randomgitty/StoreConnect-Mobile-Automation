import re
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from conftest import driver
from pages.base_page import BasePage
from pages.logout_page import LogoutPage 
import json
from utilities.login_manager import LoginManager
from pages.home_page import HomePage
from utilities.range_helper import get_approvers_for_amount
import allure
import logging
import time 

logger = logging.getLogger(__name__)

class AuthorityMatrixPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.logout_page = LogoutPage(driver)
        self.home_page = HomePage(driver)

    purchase_return = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().descriptionContains("Purchase Return").descriptionContains("Branch to Supplier")')
    dc_to_supplier = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().descriptionContains("Purchase Return").descriptionContains("DC to Supplier")')
    spoilage = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().descriptionContains("Spoilage").descriptionContains("Branch")')
    spoilage_dc = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().descriptionContains("Spoilage").descriptionContains("DC")')
    purchase_order_locator = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().descriptionContains("Purchase Order").descriptionContains("Branch to Supplier")')
    purchase_order_dc_locator = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().descriptionContains("Purchase Order").descriptionContains("DC to Supplier")')
    POS_return_locator = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().descriptionContains("POS Return").descriptionContains("Customer")')
    first_pos_card_locator = (AppiumBy.CLASS_NAME, 'android.view.View')
    remarks_field_locator = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.EditText")')
    reject_button_locator = (AppiumBy.ACCESSIBILITY_ID, 'Reject')
    approve_button_locator = (AppiumBy.ACCESSIBILITY_ID, 'Approve')




    def get_page_title(self):
        title_locator = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Authority Matrix")')
        title_element = self.wait_for_visible(title_locator, timeout=20)
        title_text = title_element.text.strip()
        if not title_text:
            title_text = title_element.get_attribute("contentDescription").strip()
        logger.info(f"✅ Page title retrieved: '{title_text}'")
        return title_text

    def get_available_modules(self):
        """
        Fetches available modules using exact contentDescription values (as observed in UI).
        This avoids reliance on empty or generic locators.
        """
        known_descriptions = [
            "POS Return\nCustomer\n14",
            "Purchase Return\nBranch to Supplier",
            "Purchase Return\nDC to Supplier",
            "Spoilage\nBranch",
            "Purchase Order\nBranch to Supplier",
            "Purchase Order\nDC to Supplier"
        ]

        modules = []
        logger.debug("Attempting to locate modules using known contentDescription values...")

        for desc in known_descriptions:
            try:
                ui_selector = f'new UiSelector().description("{desc}")'
                locator = (AppiumBy.ANDROID_UIAUTOMATOR, ui_selector)
                el = self.driver.find_element(*locator)
                parts = desc.strip().split("\n")
                if len(parts) >= 2:
                    module_name = f"{parts[0]} - {parts[1]}"
                else:
                    module_name = parts[0]

                if "Authority Matrix" not in module_name:
                    modules.append(module_name)
                    logger.debug(f"✅ Found module: '{module_name}'")
                else:
                    logger.debug(f"Skipped (Authority Matrix): '{module_name}'")

            except Exception as e:
                logger.debug(f"Module not found: {repr(desc[:30])}... | Error: {str(e)}")
                continue

        # Preserve order and remove duplicates
        modules = list(dict.fromkeys(modules))
        logger.info(f"Modules Found...")
        for mod in modules:
            logger.info(f"   • {mod}")

        return modules
    
    def navigate_to_purchase_return_branch_to_supplier(self): 
        self.click(self.purchase_return)
        logger.info("✅ Clicked and Verified Page:  Purchase Return Branch to Supplier")

    def navigate_to_purchase_return_dc_to_supplier(self): 
        self.click(self.dc_to_supplier)
        logger.info("✅ Clicked and Verified Page: Purchse Return - DC to Supplier")
    
    def navigate_to_Spoilage(self): 
        self.click(self.spoilage)
        logger.info("✅ Clicked and Verified Page: Spoiler Branch")
    
    def navigate_to_spoilage_dc(self): 
        self.click(self.spoilage_dc)
        logger.info("✅ Clicked and Verified Page: Spoilage DC")

    def navigate_to_purchase_order_branch_to_supplier(self):
        self.click(self.purchase_order_locator)
        logger.info("✅ Clicked and Verified Page: Branch to Supplier")

    def navigate_to_purchase_order_dc_to_supplier(self): 
        self.click(self.purchase_order_dc_locator)
        logger.info('✅ Clicked and Verified Page: Purchase Order DC to Supplier')

    def navigate_to_POS_return(self): 
        self.click_and_verify_page_title(
            card_locator=self.POS_return_locator, 
            expected_title="POS Return"
        )
        logger.info('SUCCESS: Navigates to POS Return Page')

    def select_process_module(self, module_name):
        """
        Select the Process Module from dropdown.
        :param module_name: str ("POS Return (Customer)", etc.)
        """
        logger.info(f"Selecting Process Module: {module_name}")
        self.click(self.process_module_dropdown)
        time.sleep(2)
        module_options = {
            "POS Return (Customer)": self.pos_return_option,
            "Purchase Return (Branch to Supplier)": self.branch_supplier_option,
            "Purchase Return (DC to Supplier)": self.dc_supplier_option
        }

        if module_name not in module_options:
            raise ValueError(f"Unknown module: {module_name}")

        option_locator = module_options[module_name]
        try:
            self.click(option_locator)
            logger.info(f"✅ Selected Module: {module_name}")
        except Exception as e:
            logger.error(f"Failed to select module {module_name}: {str(e)}")
            raise

    def get_pos_request_details(self):
        """
        Extracts ID and Amount from the first POS Return card.
        Returns: (id_num, amount)
        """
        logger.info("Extracting ID and Amount from POS Return card...")
        try:
            id_element = self.wait_for_visible(self.id_locator)
            amount_element = self.wait_for_visible(self.amount_locator)
            id_num = id_element.text.strip()
            amount = float(amount_element.text.replace('AED', '').replace(',', '').strip())
            logger.info(f"✅ Extracted: ID={id_num}, Amount={amount} AED")
            return id_num, amount
        except Exception as e:
            logger.error(f"Failed to extract ID/Amount: {str(e)}")
            raise

    def get_approval_status(self):
        """
        Gets the current approval status for each level.
        Returns a list of tuples: [(role, status), ...]
        e.g., [("Customer Sales Team Leader", "Pending"), ...]
        """
        logger.info("Getting Approval Status...")
        approval_rows = self.driver.find_elements(*self.approval_row_locator)
        statuses = []
        for row in approval_rows:
            try:
                role_element = row.find_element(AppiumBy.ID, "com.storeconnect:id/approver_role")  # Adjust
                status_element = row.find_element(AppiumBy.ID, "com.storeconnect:id/approval_status")  # Adjust
                role = role_element.text.strip()
                status = status_element.text.strip()
                statuses.append((role, status))
                logger.debug(f"   • {role}: {status}")
            except Exception as e:
                logger.warning(f"Could not read row: {str(e)}")
                continue
        return statuses
    

    def approve_reject(self, approval: bool, remarks=""):
        """
        Approves or rejects the current request.
        :param approval: True = Approve, False = Reject
        :param remarks: str (optional)
        """
        logger.info(f"{'Approving' if approval else 'Rejecting'} request with remarks: '{remarks}'")

        # Enter remarks if provided
        if remarks:
            remarks_field = self.wait_for_visible(self.remarks_field_locator)
            remarks_field.clear()
            remarks_field.send_keys(remarks)
            logger.info(f"✅ Entered remarks: {remarks}")

        # Click Approve or Reject
        button_locator = self.approve_button_locator if approval else self.reject_button_locator
        button = self.wait_for_clickable(button_locator)
        button.click()
        logger.info(f"✅ Clicked {'Approve' if approval else 'Reject'} button")

        # Wait for success toast or navigation
        time.sleep(3)
    



    def verify_range_and_approvers(self, expected_range, expected_approvers):
        """
        Verify that the current screen shows the correct approvers for the given range.
        This assumes the matrix is displayed as a list of rows, each with a range and approvers.
        """
        logger.info(f"Verifying Range: {expected_range} with Approvers: {expected_approvers}")

        range_found = False
        max_scroll_attempts = 5
        for attempt in range(max_scroll_attempts):
            try:
               
                range_elements = self.driver.find_elements(*self.range_cell_locator)
                for elem in range_elements:
                    if elem.text.strip() == expected_range:
                        range_found = True
                        row = elem 
                        approver_elements = row.find_elements(*self.approver_cell_locator)
                        approver_texts = [el.text.strip() for el in approver_elements]

                        if set(approver_texts) == set(expected_approvers):
                            logger.info(f"✅ Verified: Range '{expected_range}' has correct approvers.")
                            return
                        else:
                            raise AssertionError(
                                f"Expected approvers: {expected_approvers}, Found: {approver_texts}"
                            )

                if not range_found:
                    # Scroll down
                    self.scroll_down()
                    time.sleep(1)
            except Exception as e:
                logger.warning(f"Attempt {attempt + 1} failed: {str(e)}")

        raise AssertionError(f"Range '{expected_range}' not found after {max_scroll_attempts} attempts.")

    def select_pos_card_by_order_id(self, order_id):
        """
        Selects a specific POS Return card by order ID.
        :param order_id: str (e.g., "19005844")
        """
        logger.info(f"Searching for POS card with Order ID: {order_id}")

        order_card_locator = (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().descriptionContains("{order_id}")')
        try:
            card = self.wait_for_visible(order_card_locator, timeout=15)
            card.click()
            logger.info(f"✅ Clicked on POS card with Order ID: {order_id}")
            time.sleep(2)
        except Exception as e:
            logger.error(f"❌ Failed to find/click card with Order ID {order_id}: {str(e)}")
            raise

    def extract_sr_and_amount(self):
        desc = self.driver.find_element(
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().descriptionContains("Al Warqa").descriptionContains("Pending")'
        ).get_attribute("content-desc")

        #logger.info(f"Content-desc: {desc}")
        sr_match = re.search(r'SR\s*(\d+)', desc)
        amount_match = re.search(r'\nD\s*\n([\d,.]+)', desc)
        
        if not sr_match or not amount_match:
            # Fallback: try simpler patterns
            sr_match = re.search(r'(\d{18,})', desc)  
            amount_match = re.search(r'(\d+\.\d{2})\s*\n', desc)  
        
        if not sr_match or not amount_match:
            raise ValueError(f"Could not extract SR and amount from: {desc}")
        
        sr = sr_match.group(1)
        amount = amount_match.group(1).replace(',', '')
        logger.info(f"✅ Extracted SR: {sr} | Amount: {amount}")
        return sr, amount
    
    def get_approval_status(self):
        """
        Gets the current approval status for each level dynamically.
        Returns a list of tuples: [(role, status), ...]
        """
        
        logger.info("Getting Approval Status dynamically...")

        role_keywords = [
            "Team Leader", "Supervisor", "Manager", "Director", "COO", "CEO",
            "Receiving Area", "Customer Sales", "Branch", "DC", "Operation"
        ]
        try:
            base_selector = 'new UiSelector().className("android.view.View")'
            status_selector = '.descriptionContains("Pending").descriptionContains("Approved")'
            pending_locator = (
                AppiumBy.ANDROID_UIAUTOMATOR,
                f'{base_selector}.descriptionContains("Pending")'
            )
            approved_locator = (
                AppiumBy.ANDROID_UIAUTOMATOR,
                f'{base_selector}.descriptionContains("Approved")'
            )
            pending_elements = self.driver.find_elements(*pending_locator)
            approved_elements = self.driver.find_elements(*approved_locator)
            candidate_elements = pending_elements + approved_elements
            logger.debug(f"Found {len(candidate_elements)} candidate elements with 'Pending' or 'Approved' in content-desc.")

        except Exception as e:
            logger.error(f" Failed to find candidate elements: {str(e)}")
            return []  

        statuses = []
        for i, element in enumerate(candidate_elements):
            try:
                desc = element.get_attribute("contentDescription")
                if not desc:
                    continue 
                desc = desc.strip()
                if "Pending" in desc or "Approved" in desc:
                    parts = desc.split("\n", 1)  
                    if len(parts) == 2:
                        role = parts[0].strip()
                        status = parts[1].strip()
                        if status in ["Pending", "Approved"]:
                            role_matches_keyword = any(keyword in role for keyword in role_keywords)
                            if not role_matches_keyword:
                                logger.debug(f"   Skipped role '{role}' - doesn't match known keywords.")
                                continue

                            statuses.append((role, status))
                            logger.debug(f"   Row {i+1}: {role} -> {status}")
                        else:
                            logger.debug(f"   Skipped invalid status '{status}' for role '{role}'")
                    else:
                        logger.debug(f"   Skipped malformed row: '{desc}'")
                else:
                    logger.debug(f"   Skipped non-approval element: '{desc}'")

            except Exception as e:
                logger.warning(f"Could not process candidate element {i+1}: {str(e)}")
                continue

        if not statuses:
            logger.warning("No valid approval status rows found. Check UI structure or role keywords.")
        else:
            logger.info(f" Found {len(statuses)} approval statuses.")

        return statuses
    
    def give_remarks_and_decide(self, remarks: str): 
        """
        Enters remarks and decides to approve or reject based on remarks content.
        :param remarks: str
        """
        logger.info(f"Entering remarks: '{remarks}'")

        # Enter remarks
        remarks_field = self.wait_for_visible(self.remarks_field_locator)
        remarks_field.click() 
        remarks_field.send_keys(remarks)
        logger.info(f"✅ Entered remarks: {remarks}")
        self.hide_keyboard()

       
        approval = True if remarks.lower() == "approve" else False
        button_locator = self.approve_button_locator if approval else self.reject_button_locator
        button = self.wait_for_clickable(button_locator)
        button.click()
        logger.info(f"✅ Clicked {'Approve' if approval else 'Reject'} button")
        time.sleep(3)
        logger.info("SUCESS: Remarks Added with Decision for current user")

    def handle_no_data(self):
        no_data_locator = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("No Data Found")')
        try:
            self.wait_for_visible(no_data_locator, timeout=10)
            logger.warning("⚠️ No data available in POS Return module.")
            return True
        except Exception:
            logger.info("✅ Data is available. Proceeding with flow.")
            return False

    def complete_POS_return_customer_flow(self):
        """
        Executes the complete POS Return (Customer) flow:
        - Clicks the POS Return card
        - Extracts ID and AED amount from the first item
        - Verifies page title is 'POS Return (Customer)'
        - Asserts extracted ID & amount are consistent
        - Enters remarks from test_data.json
        - Clicks 'Approve' or 'Reject' based on remarks value
        - Logs out and logs in as the next required approver if pending
        """
        
        logger.info('Starting POS Return (Customer) flow... ')

        # 1. Navigate to POS Return Page
        self.navigate_to_POS_return()

           
        if self.handle_no_data():
            logger.warning("ℹ No data Available.")
            return None  # Indicates no data

        # 2. DYNAMIC LOCATOR FOR FIRST CARD (Al Warqa, Pending)
        product_card_locator = (
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().descriptionContains("Al Warqa").descriptionContains("Pending")'
        )

        # 3. Click the first request card
        pos_cards = self.driver.find_elements(*product_card_locator)
        if not pos_cards:
            raise AssertionError("No POS Return card found with 'Al Warqa' and 'Pending' status.")
        pos_cards[0].click()
        logger.info("✅ Clicked on the first POS Return request card")
        time.sleep(5)

        # 4. Extract SR and Amount
        sr, amount = self.extract_sr_and_amount()

        # 5. Get Approval Status List
        statuses = self.get_approval_status()
        logger.info(f"Approval Status Summary for SR {sr}:")
        total_pending = 0
        total_approved = 0
        pending_roles = []

        for role, status in statuses:
            logger.info(f"   • {role}: {status}")
            if status == "Pending":
                total_pending += 1
                pending_roles.append(role)
            elif status == "Approved":
                total_approved += 1

        logger.info(f"✅ Total Approved: {total_approved} | Total Pending: {total_pending}")

        # 6. If no pending approvals, we're done!
        if total_pending == 0:
            logger.info("All approvals completed for this request!")
            return sr, amount, []
        # 7. Get the first pending role (the one who needs to act next)
        next_role = pending_roles[0]
        logger.info(f"Required Approver: {next_role}")

        # 8. Fetch Credentials for the Next Role
        login_manager = LoginManager(self.driver)
        try:
            user_info = login_manager.get_user_by_role(next_role)
            username = user_info['username']
            password = user_info['password']
            logger.info(f"Credentials for Role: '{next_role}' | Username = {username} | Password = **********")
        except ValueError as e:
            logger.error(f" Could not find user for role '{next_role}': {str(e)}")
            raise
    
        # Give remarks and approve/reject for current user
        self.give_remarks_and_decide(remarks="Approve")
        
        # 9. Log Out Current User
        logger.info("Logging out current user...")
        self.home_page.navigate_to_homepage_from_current_module() 
        
        self.logout_page.logout_via_exit_icon()  
        time.sleep(3)
        assert self.logout_page.is_logged_out(), "Logout failed."
        logger.info("Logout SUCCESS")

        # 10. Log In as Next Approver
        logger.info(f"Logging in as next approver: {next_role}...")



