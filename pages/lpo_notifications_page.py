from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from pages.base_page import BasePage
import time 
import logging

logger = logging.getLogger(__name__)

class LpoNotificationsPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
    
    def get_page_title(self):
        title_locator = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("LPO Notifications")')
        try:
            title_element = WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located(title_locator)
            )
            title_text = title_element.text
            logger.info(f"✅ LPO Notifications Page Title: {title_text}")
            return title_text
        except (TimeoutException, NoSuchElementException) as e:
            logger.error(f"❌ Failed to get LPO Notifications Page Title: {e}")
            return None


       
    def complete_lpo_notifications_flow(self):
        self.get_page_title()
        logger.info("✅ Completed LPO Notifications flow")
        