import allure
import time
import logging
from appium.webdriver.common.appiumby import AppiumBy
from pages.base_page import BasePage

logger = logging.getLogger(__name__)

class ItemsNewlyReceivedPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver) 
    def get_page_title(self):
        title_locator = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Item Newly Received")')
        title_element = self.wait_for_visible(title_locator, timeout=20)
        title_text = title_element.text.strip()
        if not title_text:
            title_text = title_element.get_attribute("contentDescription").strip()
        logger.info(f"✅ Page title retrieved: '{title_text}'")
        return title_text
    def click_filter(self):
        filter_button = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Filter")')
        filter_click = self.wait_for_clickable(filter_button, timeout=20)
        filter_click.click()
        logger.info("✅ Clicked on Filter button")
        allure.attach(
            self.driver.get_screenshot_as_png(),
            name="Filter Button Clicked",
            attachment_type=allure.attachment_type.PNG)

    def apply_date_filter(self):
        date_filter_opt = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("3 days")')
        element = self.wait_for_clickable(date_filter_opt, timeout=15)  
        element.click()
        logger.info("✅ Applied date filter")

    def submit_filter(self):
        submit_filter_button = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Submit")')
        submit_button = self.wait_for_clickable(submit_filter_button, timeout=15)
        submit_button.click()
        logger.info("✅ Submitted filter")

    def apply_and_submit_filter(self):
        self.click_filter()
        self.apply_date_filter()
        self.submit_filter()
        time.sleep(6)

    def get_product_card_locator(self, product_name: str):
        escaped_name = product_name.replace('"', '\\"') 
        return (AppiumBy.ANDROID_UIAUTOMATOR,f'new UiSelector().descriptionContains("{escaped_name}").instance(0)')
    

    
    def click_product_card(self):
        """Click the top product card containing 'Current Stock'."""
        product_card_locator = self.get_product_card_locator("Current Stock")   

        try:
            card_element = self.wait_for_clickable(product_card_locator, timeout=15)
            card_text = card_element.get_attribute("contentDescription")
            logger.info(f"Clicking card: '{card_text}'") 
            card_element.click()
            logger.info("✅ Clicked on the top product card containing 'Current Stock'")
            time.sleep(5)  
        except Exception as e:
            raise AssertionError(f"Failed to click product card with 'Current Stock': {str(e)}")

    def handle_no_data(self):
        no_data_locator = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("No data found")')
        try:
            no_data_element = self.wait_for_visible(no_data_locator, timeout=10)
            if no_data_element:
                logger.warning("No data available for the applied filter.")
                return True
        except:
            logger.info("✅ Data is available after applying filter. Proceeding...")
            pass
            return False


    def complete_item_with_newly_received_flow(self):
        title = self.get_page_title()
        assert title == "Item Newly Received", f"❌ Expected 'Item Newly Received', got '{title}'"
        logger.info("✅ Page title validated")
        time.sleep(15)
        self.apply_and_submit_filter()
        logger.info("✅ Applied and submitted filter")
        time.sleep(7)
        if self.handle_no_data():
            logger.info("ℹ No Data Found — skipping product interaction...")
            return False  
        self.click_product_card()
        logger.info("✅ Completed Items Newly Received flow")
        return True 