from appium.webdriver.common.appiumby import AppiumBy
from pages.base_page import BasePage
from selenium.common.exceptions import TimeoutException
import allure
import logging
import time

logger = logging.getLogger(__name__)

class ChangeBranchPage(BasePage):
    change_branch_button = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Change")')
    
    @allure.step("Click Change Branch button")
    def click_change_button(self):
        time.sleep(15)
        change_branch_btn = self.wait_for_clickable(self.change_branch_button, timeout=30)
        change_branch_btn.click()
        logger.info("✅ Clicked Change Branch button")
        allure.attach(
            self.driver.get_screenshot_as_png(),
            name="Clicked Change Branch",
            attachment_type=allure.attachment_type.PNG
        )
    @allure.step("Search and select branch: {branch_name}")
    def search_branch(self, branch_name: str): 
        click_search_field = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.EditText")')
        search_field = self.wait_for_clickable(click_search_field, timeout=30)
        search_field.click()
        logger.info("Clicked branch search field")

        search_field.send_keys(branch_name)
        logger.info(f"✅ Entered branch name to search: '{branch_name}'")
        allure.attach(
            self.driver.get_screenshot_as_png(),
            name=f"Searched for branch: {branch_name}",
            attachment_type=allure.attachment_type.PNG
        )

        result_locator = (AppiumBy.ACCESSIBILITY_ID, branch_name)

        try:
            # Wait for the result to be clickable
            branch_result = self.wait_for_clickable(result_locator, timeout=20)
            branch_result.click()
            logger.info(f"SUCCESS: Branch '{branch_name}' searched and selected")
            allure.attach(
                self.driver.get_screenshot_as_png(),
                name=f"Selected branch: {branch_name}",
                attachment_type=allure.attachment_type.PNG
            )
        except TimeoutException:
            error_msg = f"Branch '{branch_name}' not found in search results"
            logger.error(error_msg)
            allure.attach(
                self.driver.get_screenshot_as_png(),
                name=f"Branch not found: {branch_name}",
                attachment_type=allure.attachment_type.PNG
            )
            raise AssertionError(error_msg)   
        
    @allure.step("Complete change branch flow")
    def complete_change_branch_flow(self, branch_name: str):
        self.click_change_button()
        self.search_branch(branch_name=branch_name)      
