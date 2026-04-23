import allure
import time
import logging
from appium.webdriver.common.appiumby import AppiumBy
from pages.base_page import BasePage

logger = logging.getLogger(__name__)

class ItemsWithNewPricePage(BasePage):
    def __init__(self, driver):
        super().__init__(driver) 
    def get_page_title(self):
        title_locator = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Item With New Price")')
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
    

    def handle_no_data(self):
        no_data_locator = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("No data found")')
        try:
            no_data_element = self.wait_for_visible(no_data_locator, timeout=10)
            if no_data_element:
                logger.warning("No data available for the applied filter.")
                return True
        except Exception:
            logger.info("✅ Data is available after applying filter. Proceeding...")
            return False

    def apply_and_submit_filter(self):
        self.click_filter()
        self.apply_date_filter()
        self.submit_filter()

    def get_product_card_locator(self, product_name: str):
        escaped_name = product_name.replace('"', '\\"')  # Escape quotes if any
        return (AppiumBy.ANDROID_UIAUTOMATOR,f'new UiSelector().descriptionContains("{escaped_name}").instance(0)')
    
    def click_product_card(self):
        product_card_locator = self.get_product_card_locator("Current Stock")

        try:
            card_element = self.wait_for_clickable(product_card_locator, timeout=15)
            card_element.click()
            logger.info("✅ Clicked on the top product card containing 'Stock'")
            time.sleep(5)  # Wait for navigation/animation
        except Exception as e:
            raise AssertionError(f"❌ Failed to click product card with 'Current Stock': {str(e)}")
        
        card_text = card_element.get_attribute("contentDescription")
        logger.info(f"Card Description: '{card_text}'")

    def complete_item_with_new_price_flow(self):
        title = self.get_page_title()
        assert title == "Item With New Price", f"❌ Expected 'Item With New Price', got '{title}'"
        logger.info("✅ Page title validated")
        time.sleep(5)
        self.apply_and_submit_filter()
        logger.info("✅ Applied and submitted filter")
        if self.handle_no_data():
            logger.info("ℹ Skipping product interaction — no data available. Test considered successful.")
            return # Exit early if no data
        time.sleep(5)
        self.click_product_card()
        logger.info("✅ Completed Items with New Price flow")