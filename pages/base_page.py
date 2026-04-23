from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
import allure 
import logging 
import time
import re
from appium.webdriver.common.appiumby import AppiumBy

logger = logging.getLogger(__name__)
class BasePage:
    product_search_field = (AppiumBy.ANDROID_UIAUTOMATOR,'new UiSelector().className("android.widget.EditText")')
    search_button = (AppiumBy.ANDROID_UIAUTOMATOR,'new UiSelector().description("Search")')
    back_arrow_locator = (AppiumBy.ID, 'Back')
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)
        # store default timeout for use in methods that accept a timeout arg
        self.default_timeout = timeout

    def get_text_or_default(self, locator, default="N/A"):
        """Helper to safely get text of an element, return default if not found"""
        try:
            element = self.wait_for_visible(locator)
            return element.text.strip()
        except:
            return default
    
    def is_element_visible(self, locator, timeout=10):
        """Check if an element is visible within the given timeout."""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False

    def swipe_to_bottom(self):
        size = self.driver.get_window_size()
        start_x = size['width'] // 2
        start_y = int(size['height'] * 0.8)
        end_y = int(size['height'] * 0.2)
        for _ in range(1):  # Swipe multiple times to ensure reaching bottom
            self.driver.swipe(start_x, start_y, start_x, end_y, 800)
    def wait_for_visible(self, locator, timeout=10):
        """Wait for element to be visible"""
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
        except TimeoutException:
            raise TimeoutException(f"Element {locator} not visible after {timeout} seconds")
        
    def swipe_to_down(self):
        size = self.driver.get_window_size()
        start_x = size['width'] // 2
        start_y = int(size['height'] * 0.8)
        end_y = int(size['height'] * 0.2)
        for _ in range(3):  # Swipe multiple times to ensure reaching bottom
            self.driver.swipe(start_x, start_y, start_x, end_y, 800)

    def wait_for_clickable(self, locator, timeout=10):
        """Wait until element is clickable (both present & enabled)."""
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(locator)
            )
        except TimeoutException:
            raise TimeoutException(f"Element {locator} not clickable after {timeout} seconds")
        
    def click(self, locator):
        """Wait for element to be clickable and click it"""
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()
    
    def wait_for_element(self, locator, timeout=10):
        """
        Waits until the element is present in the DOM.
        """
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.presence_of_element_located(locator)) 
         

    def presence_of_element(self, locator):
        """Wait for element to be present"""
        element = self.wait.until(EC.presence_of_element_located(locator))
        return element
    

    def hide_keyboard(self):
        """Hide the on-screen keyboard"""
        try:
            self.driver.hide_keyboard()
        except:
           self.driver.execute_script('mobile: hideKeyboard')
           logger.info("Keyboard hidden using fallback method")

    # (Removed duplicate wait_for_clickable definition; unified above.)
    
    @allure.step("Click product search field")
    def click_search_bar_product(self):
        self.wait_for_clickable(self.product_search_field)
        self.click(self.product_search_field)
        logger.info("Clicked on product search field")
        allure.attach(
            self.driver.get_screenshot_as_png(),
            name="Clicked Product Search Field",
            attachment_type=allure.attachment_type.PNG)
        
    def send_keys(self, locator, text, timeout: int | None = None):
        """Wait for element presence (or until `timeout`) and send keys.

        Args:
            locator: locator tuple
            text: text to type
            timeout: optional timeout in seconds. If None, uses page default.
        """
        t = timeout if timeout is not None else self.default_timeout
        element = WebDriverWait(self.driver, t).until(
            EC.presence_of_element_located(locator)
        )
        element.clear()
        element.send_keys(text)

    def is_element_present(self, locator, timeout=5):
        """Check if element is present"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return True
        except:
            return False
        
    def navigate_back_twice(self):
        """Navigate back twice."""
        for i in range(2):
            self.click(self.back_arrow_locator)
            logger.info(f"✅ Navigated back ({i+1}/2)")
            time.sleep(1)
    def navigate_back_once(self):
        """Navigate back twice."""
        for i in range(1):
            self.click(self.back_arrow_locator)
            logger.info(f"✅ Navigated back ({i+1}/2)")
            time.sleep(1)
        

    def click_first_product_card(self):
        """
        Clicks the first visible 'product card' on the screen without scrolling.
        - min_card_height: filter small elements (buttons/labels) by height in pixels
        - wait_seconds: how long to wait for product elements to appear
        """
        try:
            element = self.wait_for_clickable(AppiumBy.CLASS_NAME, "android.view.View")
            element.click()
            logger.info("✅ Clicked on the first product card")
        except:
            self.driver.tap([(540, 1616)])
            logger.warning("Fallback: Clicked first product card using bounds")
            logger.info("✅ Clicked on the first product card using tap")



    def click_and_verify_page_title(self, card_locator, expected_title, timeout=20):
        """
        Clicks a card using given locator, then verifies the page title matches expected title.
        Logs all steps and raises assertion error if title doesn't match.

        :param card_locator: tuple (AppiumBy, locator_string) for the card to click
        :param expected_title: string — expected page title to verify after click
        :param timeout: int — wait timeout for element visibility
        :return: str — actual page title found
        """
        logger.info(f"Clicking card with locator: {card_locator}")

        try:
            card_element = self.wait_for_clickable(card_locator, timeout=timeout)
            card_element.click()
            title_locator = (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().description("{expected_title}")')
            title_element = self.wait_for_visible(title_locator, timeout=timeout)
            actual_title = title_element.text.strip()
            if not actual_title:
                actual_title = title_element.get_attribute("contentDescription").strip()

            #logger.info(f"Page title retrieved: '{actual_title}'")

            assert actual_title == expected_title, (
                f"❌ Page title mismatch! Expected: '{expected_title}', Found: '{actual_title}'"
            )

            logger.info(f"✅ Page title verified: '{actual_title}'")
            return actual_title

        except Exception as e:
            logger.error(f"Failed to click or verify page title: {str(e)}")
            raise AssertionError(f"Failed to navigate to '{expected_title}': {str(e)}")
        