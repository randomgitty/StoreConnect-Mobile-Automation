from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from pages.base_page import BasePage
import time 
import logging

logger = logging.getLogger(__name__)

class LogoutPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.wait = WebDriverWait(driver, 30)

    exit_icon = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.Button").instance(0)')
    logout_button = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Log Out")')

    def logout_via_exit_icon(self):
        """Click Exit icon to logout."""
        try:
            self.driver.press_keycode(4)
            time.sleep(1)
            self.click(self.exit_icon)
            logger.info("Clicked Exit icon to logout")
            time.sleep(2)
            self.click(self.logout_button)
            logger.info("Clicked Logout button")
            time.sleep(1)
        except Exception as e:
            logger.warning(f"Logout Failed: {str(e)}.") 
            raise 
    def logout(self): 
        """Perform logout action."""
        time.sleep(2)
        self.click(self.logout_button)
        logger.info("Clicked Logout button")
        time.sleep(1)

    def is_logged_out(self, timeout=10):
        """Check if logout was successful by verifying presence of login page elements."""
        try:
            self.wait.until(EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, 'myTawasol')))
            logger.info("✅ Logout successful, login page is displayed.")
            return True
        except TimeoutException:
            logger.error("❌ Logout failed, login page not displayed within timeout.")
            return False
        