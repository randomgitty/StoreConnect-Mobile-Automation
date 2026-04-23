from appium.webdriver.common.appiumby import AppiumBy
from pages.base_page import BasePage
import allure
import logging

logger = logging.getLogger(__name__)

class Top500ItemsOOS_Page(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
    
    def get_page_title(self):
        title_locator = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Top 500 Items – OOS")')
        title_element = self.wait_for_visible(title_locator, timeout=20)
        title_text = title_element.text.strip()
        if not title_text:
            title_text = title_element.get_attribute("contentDescription").strip()
        logger.info(f"✅ Page title retrieved: '{title_text}'")
        return title_text

    def all_items_tab(self): 
        all_items_tab_locator = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("All Items")')
        all_items_tab_element = self.wait_for_clickable(all_items_tab_locator, timeout=20)
        all_items_tab_element.click()
        logger.info("✅ Clicked on All Items tab")

    def OOS_items_tab(self): 
        oos_items_tab_locator = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("OOS Only")')
        oos_items_tab_element = self.wait_for_clickable(oos_items_tab_locator, timeout=20)
        oos_items_tab_element.click()
        logger.info("✅ Clicked on OOS Items tab")

    def sort_filter(self):
        sort_filter_locator = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Sort")')
        sort_filter_element = self.wait_for_clickable(sort_filter_locator, timeout=20)
        sort_filter_element.click()
        logger.info("✅ Clicked on Sort & Filter button")
        allure.attach(
            self.driver.get_screenshot_as_png(),
            name="Sort & Filter Clicked",
            attachment_type=allure.attachment_type.PNG)
        
    def filter_icon(self):
        filter_icon_locator = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Filter")')
        filter_icon_element = self.wait_for_clickable(filter_icon_locator, timeout=20)
        filter_icon_element.click()
        logger.info("✅ Clicked on Filter icon")
        allure.attach(
            self.driver.get_screenshot_as_png(),
            name="Filter Icon Clicked",
            attachment_type=allure.attachment_type.PNG)
        
    def get_product_card_locator(self, product_name: str):
        escaped_name = product_name.replace('"', '\\"') 
        return (AppiumBy.ANDROID_UIAUTOMATOR,f'new UiSelector().descriptionContains("{escaped_name}").instance(0)')
    
    def click_product_card(self, product_name: str):
        """Click on a product card by name and wait for product details to load"""
        try:
            locator = self.get_product_card_locator(product_name)
            card = self.wait_for_clickable(locator, timeout=15)
            card.click()
            logger.info(f"✅ Clicked on product card: {product_name}")
        except Exception as e:
            logger.error(f"❌ Failed to click product card '{product_name}': {e}")
            raise

    def apply_submit_filter(self):
        category_filter_locator = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.CheckBox").instance(1)')
        category_filter_element = self.wait_for_clickable(category_filter_locator, timeout=20)
        category_filter_element.click()
        logger.info("✅ Selected FMCG category filter")
        apply_filter_locator = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Submit")')
        apply_filter_element = self.wait_for_clickable(apply_filter_locator, timeout=20)
        apply_filter_element.click()
        logger.info("✅ Successfully Applied Filter")
        allure.attach(
            self.driver.get_screenshot_as_png(),
            name="Apply Filter Clicked",
            attachment_type=allure.attachment_type.PNG)
        
    def complete__top_500_items_OOS_flow(self):
        title = self.get_page_title()
        assert title == "Top 500 Items – OOS", f"❌ Expected 'Top 500 Items – OOS', got '{title}'"
        logger.info("✅ Page title validated")
        self.filter_icon()
        self.apply_submit_filter()
        

    
    