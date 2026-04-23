from appium.webdriver.common.appiumby import AppiumBy
from pages.base_page import BasePage
import allure
import logging
import time

logger = logging.getLogger(__name__)

class HomePage(BasePage):
    product_dimension_card = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Product Dimension")')
    items_with_new_price_card = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Item With New Price")')
    @allure.step("Navigate to Product Dimension module")
    def navigate_to_product_dimension(self, timeout: int = 50):
        """
        Wait up to `timeout` seconds for the Product Dimension card to be clickable,
        click it, and raise on failure so the test stops instead of proceeding.
        """
        try:
            time.sleep(30)
            element = self.wait_for_clickable(self.product_dimension_card, timeout=timeout)
            element.click()
            logger.info("✅ Navigated to Product Dimension module")
            allure.attach(
                self.driver.get_screenshot_as_png(),
                name="Navigated to Product Dimension",
                attachment_type=allure.attachment_type.PNG
            )
        except Exception as e:
            # Log full exception and re-raise so test execution stops here
            logger.exception(f"Failed to navigate to Product Dimension within {timeout}s: {e}")
            raise
    
    @allure.step("Navigate to Items with New Price module")
    def navigate_to_items_with_new_price(self):
        time.sleep(25)
        items_tab = self.wait_for_clickable(self.items_with_new_price_card, timeout=150)
        items_tab.click()
        logger.info("✅ Navigated to Items with New Price module")
        allure.attach(
            self.driver.get_screenshot_as_png(),
            name="Navigated to Items with New Price",
            attachment_type=allure.attachment_type.PNG)
        
    def navigate_to_items_with_no_sales(self):
        items_no_sales_card = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Item With No Sales")')
        time.sleep(20)
        items_no_sales_tab = self.wait_for_clickable(items_no_sales_card, timeout=150)
        items_no_sales_tab.click()
        logger.info("✅ Navigated to Items with No Sales module")
        allure.attach(
            self.driver.get_screenshot_as_png(),
            name="Navigated to Items with No Sales",
            attachment_type=allure.attachment_type.PNG)
        
    def navigate_to_items_newly_received(self):
        items_newly_received_card = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Item Newly Received")')
        time.sleep(20)
        items_newly_received_tab = self.wait_for_clickable(items_newly_received_card, timeout=150)
        items_newly_received_tab.click()
        time.sleep(15)
        logger.info("✅ Navigated to Items Newly Received module")
        allure.attach(
            self.driver.get_screenshot_as_png(),
            name="Navigated to Items Newly Received",
            attachment_type=allure.attachment_type.PNG)
    
    def navigate_to_top_500_items(self):
        top_500_items_card = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Top 500 Items – OOS")')
        time.sleep(15)
        top_500_items_tab = self.wait_for_clickable(top_500_items_card, timeout=150)
        top_500_items_tab.click()
        logger.info("✅ Navigated to Top 500 Items module")
        allure.attach(
            self.driver.get_screenshot_as_png(),
            name="Navigated to Top 500 Items",
            attachment_type=allure.attachment_type.PNG)

    def navigate_to_service_and_repair(self):
        service_and_repair_card = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Service & Repair")')
        time.sleep(20)
        service_and_repair_tab = self.wait_for_clickable(service_and_repair_card, timeout=150)
        service_and_repair_tab.click()
        logger.info("✅ Navigated to Service & Repair module")
        allure.attach(
            self.driver.get_screenshot_as_png(),
            name="Navigated to Service & Repair",
            attachment_type=allure.attachment_type.PNG)
        
    def navigate_to_authority_matrix(self):
        authority_matrix_card = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Authority Matrix")')
        time.sleep(20)
        authority_matrix_tab = self.wait_for_clickable(authority_matrix_card, timeout=150)
        authority_matrix_tab.click()
        logger.info("✅ Navigated to Authority Matrix module")
        allure.attach(
            self.driver.get_screenshot_as_png(),
            name="Navigated to Authority Matrix",
            attachment_type=allure.attachment_type.PNG)
        
    def navigate_to_homepage_from_current_module(self):
        back_icon = (AppiumBy.ACCESSIBILITY_ID, 'Back')
        back_icon_element = self.wait_for_clickable(back_icon, timeout=50)
        back_icon_element.click()
        back_icon_element.click()  # Click twice to ensure return to home
        logger.info(" Navigated back to Home Page from current module")

    def navigate_to_eros_discount_voucher(self):
        eros_discount_voucher_card = (AppiumBy.ACCESSIBILITY_ID, 'EROS Discount Voucher')
        time.sleep(10)
        eros_discount_voucher_tab = self.wait_for_clickable(eros_discount_voucher_card, timeout=150)
        eros_discount_voucher_tab.click()
        logger.info("✅ Navigated to EROS Discount Voucher module")
        allure.attach(
            self.driver.get_screenshot_as_png(),
            name="Navigated to EROS Discount Voucher",
            attachment_type=allure.attachment_type.PNG)
        
    def navigate_to_lpo_notifications(self):
        lpo_notifications_card = (AppiumBy.ACCESSIBILITY_ID, 'LPO Notifications')
        time.sleep(10)
        lpo_notifications_tab = self.wait_for_clickable(lpo_notifications_card, timeout=150)
        lpo_notifications_tab.click()
        logger.info("✅ Navigated to LPO Notifications module")
        allure.attach(
            self.driver.get_screenshot_as_png(),
            name="Navigated to LPO Notifications",
            attachment_type=allure.attachment_type.PNG)
        
    @allure.step("Navigate to Product Facing module")    
    def navigate_to_product_facing(self): 
        product_facing_card = (AppiumBy.ACCESSIBILITY_ID, 'Product Facing')
        time.sleep(10)
        product_facing_tab = self.wait_for_clickable(product_facing_card, timeout=150)
        product_facing_tab.click()
        logger.info("✅ Navigated to Product Facing module")
        allure.attach(
            self.driver.get_screenshot_as_png(),
            name="Navigated to Product Facing",
            attachment_type=allure.attachment_type.PNG)




        