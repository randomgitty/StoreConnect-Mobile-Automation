import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from pages.base_page import BasePage
from selenium.webdriver.support import expected_conditions as EC
import allure
import logging

logger = logging.getLogger(__name__)


class ProductFacingPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

        # Locators
        self.location_dropdown = (AppiumBy.ACCESSIBILITY_ID, 'Location\nSelect location')
        self.barcode_field_locator = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.EditText")')
        self.search_icon_button = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.Button").instance(1)')
        self.add_facing_button = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Add Facing")')
        self.facing_field = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.EditText").instance(0)')
        self.rows_field = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.EditText").instance(1)')
        self.save_button = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Save")')
        self.scan_success_indicator = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Scan successful")')
        self.review_item_button = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Review Item")')

    @allure.step("Verify QR Code Scan Success")
    def verify_qr_scan_success(self):
        """Verify that QR code was scanned successfully"""
        try:
            scan_success = self.wait.until(
                EC.presence_of_element_located(self.scan_success_indicator)
            )
            logger.info("✅ QR Code Scan Successful")
            allure.attach(
                self.driver.get_screenshot_as_png(),
                name="QR Scan Success",
                attachment_type=allure.attachment_type.PNG
            )
            return True
        except:
            logger.warning("QR scan success indicator not found, continuing...")
            return False

    @allure.step("Click on Add Facing button")
    def click_add_facing_button(self):
        """Click the Add Facing button after QR scan"""
        add_facing = self.wait_for_clickable(self.add_facing_button)
        add_facing.click()
        logger.info("✅ Clicked on Add Facing button")
        time.sleep(2)
        allure.attach(
            self.driver.get_screenshot_as_png(),
            name="Add Facing Button Clicked",
            attachment_type=allure.attachment_type.PNG
        )

    @allure.step("Select location: {location_name}")
    def select_location(self, location_name: str):
        valid_locations = {"Regular", "Checkout", "Crossmatch"}
        if location_name not in valid_locations:
            raise ValueError(
                f"Invalid location_name '{location_name}'. "
                f"Expected one of {valid_locations}"
            )
        self.wait_for_clickable(self.location_dropdown).click()
        logger.info("Clicked on location dropdown")
        location_option = (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().description("{location_name}")')

        element = self.wait_for_clickable(location_option)
        element.click()
        logger.info(f"✅ Selected Location: {location_name}")

    @allure.step("Click on Barcode field")
    def click_barcode_field(self): 
        barcode_field = self.wait_for_clickable(self.barcode_field_locator)
        barcode_field.click()
        logger.info("Clicked on Barcode field")
        logger.info("Searching for Product ... ")

    @allure.step("Enter barcode: {barcode}")
    def enter_barcode(self, barcode: str):
        self.send_keys(self.barcode_field_locator, barcode)
        logger.info(f"Entered Barcode: {barcode}")
        allure.attach(
            self.driver.get_screenshot_as_png(),
            name="Barcode Entered",
            attachment_type=allure.attachment_type.PNG
        )
        

    @allure.step("Complete search product by barcode: {barcode}")
    def complete_search_product_by_barcode(self, barcode: str):
        self.click_barcode_field()
        self.enter_barcode(barcode)
        search_button = self.wait_for_clickable(self.search_icon_button)
        search_button.click()
        logger.info("Clicked on Search button")
        allure.attach(
            self.driver.get_screenshot_as_png(),
            name="After Search Click",
            attachment_type=allure.attachment_type.PNG
        )
        
        try: 
            okay_button_locator = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Okay")')
            okay_button = self.wait.until(EC.element_to_be_clickable(okay_button_locator))
            okay_button.click()
            logger.info("Assortment Error: Item Assortment Status - N")
        except:
            logger.info("✅ Product found successfully.")

    @allure.step("Scroll down to facing fields")
    def scroll_to_facing_fields(self):
        """Scroll down to find the facing and rows input fields"""
        self.driver.execute_script("mobile: swipe", {
            "direction": "down",
            "percent": 0.5
        })
        time.sleep(2)
        logger.info("✅ Scrolled down to facing fields")

    @allure.step("Enter Facing: {facing_count}")
    def enter_facing_count(self, facing_count: str):
        element = self.wait_for_clickable(self.facing_field)
        element.clear()
        element.click()
        element.send_keys(str(facing_count))
        logger.info(f"✅ Entered Facing Count: {facing_count}")
        allure.attach(
            self.driver.get_screenshot_as_png(),
            name="Facing Count Entered",
            attachment_type=allure.attachment_type.PNG
        )
        self.driver.hide_keyboard()
        time.sleep(2)
    
    @allure.step("Enter Rows: {rows_count}")
    def enter_rows_count(self, rows_count: str):
        element = self.wait_for_clickable(self.rows_field)
        element.clear()
        element.click()
        element.send_keys(str(rows_count))
        logger.info(f"✅ Entered Rows Count: {rows_count}")
        allure.attach(
            self.driver.get_screenshot_as_png(),
            name="Rows Count Entered",
            attachment_type=allure.attachment_type.PNG
        )
        self.driver.hide_keyboard()
        time.sleep(2)
        
    @allure.step("Click on Save button")
    def click_save_button(self):
        save_button = self.wait_for_clickable(self.save_button)
        save_button.click()
        logger.info("✅ Clicked on Save button")
        time.sleep(3)
        allure.attach(
            self.driver.get_screenshot_as_png(),
            name="After Save Click",
            attachment_type=allure.attachment_type.PNG
        )
        
    @allure.step("Complete Product Facing Entry")
    def complete_product_facing_entry(self, facing_count: str, rows_count: str):
        logger.info("Swiping down")
        self.swipe_to_down()
        self.enter_facing_count(facing_count)
        self.enter_rows_count(rows_count)
        logger.info("✅ Completed Product Facing Entry")
        allure.attach(
            self.driver.get_screenshot_as_png(),
            name="Product Facing Entry Completed",
            attachment_type=allure.attachment_type.PNG
        )
        self.click_save_button()
        logger.info("✅ Test Successfully Completed for Product Facing Entry")

    @allure.step("Complete Add Facing Flow")
    def complete_add_facing_flow(self, barcode: str, facing_count: str, rows_count: str):
        """
        Complete flow after QR scan:
        Click Add Facing -> Enter Barcode -> Search -> Enter Facing & Rows -> Save
        """
        self.click_add_facing_button()
        time.sleep(2)
        self.complete_search_product_by_barcode(barcode)
        self.complete_product_facing_entry(facing_count, rows_count)