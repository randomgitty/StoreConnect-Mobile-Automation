from appium.webdriver.common.appiumby import AppiumBy
from pages.base_page import BasePage
import allure
import logging

logger = logging.getLogger(__name__)

class ProductDimensionPage(BasePage):
    # === LOCATORS ===
    product_search_field = (AppiumBy.ANDROID_UIAUTOMATOR,'new UiSelector().className("android.widget.EditText")')
    search_button = (AppiumBy.ANDROID_UIAUTOMATOR,'new UiSelector().description("Search")')
    height_field = (AppiumBy.ANDROID_UIAUTOMATOR,'new UiSelector().className("android.widget.EditText").instance(1)')
    width_field = (AppiumBy.ANDROID_UIAUTOMATOR,'new UiSelector().className("android.widget.EditText").instance(2)')
    depth_field = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.EditText").instance(3)')
    submit_button = (AppiumBy.ANDROID_UIAUTOMATOR,'new UiSelector().description("Submit")')
    success_message = (AppiumBy.ANDROID_UIAUTOMATOR,'new UiSelector().description("Product Dimension")')
    submit_button_fallback = (AppiumBy.ANDROID_UIAUTOMATOR,'new UiSelector().description("Update")')
    search_fallback_button = (AppiumBy.ANDROID_UIAUTOMATOR,'new UiSelector().className("android.widget.Button").instance(1)')
        
    def enter_product_code(self, product_code):
        self.send_keys(self.product_search_field, product_code)
        logger.info(f"Entered product code: {product_code}")
        allure.attach(
            self.driver.get_screenshot_as_png(),
            name="Product Code Entered",
            attachment_type=allure.attachment_type.PNG)

    @allure.step("Click Search button")
    def click_search(self):
        try: 
            self.click(self.search_button)
            logger.info("Clicked Search button")
        except: 
            self.click(self.search_fallback_button)
            logger.info('SUCCESS: Self Healing Locator Selected - Search Fallback button clicked')
        allure.attach(
            self.driver.get_screenshot_as_png(),
            name="After Search Click",
            attachment_type=allure.attachment_type.PNG)

    @allure.step("Enter Height: {height}")
    def enter_height(self, height: str):
        try:
            self.wait_for_clickable(self.height_field)
            self.click(self.height_field)
            self.send_keys(self.height_field, height)
            logger.info(f"Entered Height: {height}")
            self.driver.implicitly_wait(10)
            allure.attach(self.driver.get_screenshot_as_png(), name="Height Entered", attachment_type=allure.attachment_type.PNG)
        except Exception as e:
            logger.error(f" Failed to enter height: {e}")
            raise
            
    @allure.step("Enter Width: {width}")
    def enter_width(self, width: str):
        try: 
            self.wait_for_clickable(self.width_field)
            self.click(self.width_field)
            self.send_keys(self.width_field, width)
            logger.info(f"Entered Width: {width}")
            allure.attach(self.driver.get_screenshot_as_png(), name="Width Entered", attachment_type=allure.attachment_type.PNG)
        except Exception as e:
            logger.error(f" Failed to enter width: {e}")    
            try:
                element = self.wait_for_clickable(self.width_field, timeout=30)
                element.clear()
                element.send_keys(width)
                logger.info(f"Entered Width: {width}")
                allure.attach(
                    self.driver.get_screenshot_as_png(),
                    name="Width Entered",
                    attachment_type=allure.attachment_type.PNG)
            except Exception as e:
                logger.exception(f"Failed to enter width: {e}")
                raise

    @allure.step("Enter Depth: {depth}")
    def enter_depth(self, depth: str):
        self.wait_for_clickable(self.depth_field)
        self.click(self.depth_field)
        self.send_keys(self.depth_field, depth)
        self.hide_keyboard()
        
        logger.info(f"Entered Depth: {depth}")
        allure.attach(
            self.driver.get_screenshot_as_png(),
            name="Depth Entered",
            attachment_type=allure.attachment_type.PNG)
        try:
                element = self.wait_for_clickable(self.depth_field, timeout=30)
                element.clear()
                element.send_keys(depth)
                logger.info(f"Entered Depth: {depth}")
                allure.attach(
                    self.driver.get_screenshot_as_png(),
                    name="Depth Entered",
                    attachment_type=allure.attachment_type.PNG)
        except Exception as e:
                logger.exception(f"Failed to enter depth: {e}")
                raise
        
    def take_photo_using_camera(self):
        camera_icon = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.view.View").instance(10)')
        self.wait_for_clickable(camera_icon)
        self.click(camera_icon)
        logger.info("Clicked on camera icon to take photo")

        self.driver.implicitly_wait(30)
        take_photo_opt = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Take a Photo")')
        self.wait_for_clickable(take_photo_opt)    
        self.click(take_photo_opt)
        self.driver.implicitly_wait(35)
        logger.info("Selected Take a Photo option")
        shutter_button = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("com.android.camera2:id/shutter_button")')
        self.wait_for_clickable(shutter_button)
        self.click(shutter_button)
        self.driver.implicitly_wait(20)
        done_button = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("com.android.camera2:id/done_button")')
        self.wait_for_clickable(done_button)
        self.click(done_button)
        self.driver.implicitly_wait(20)
        logger.info("Photo taken and confirmed")

    @allure.step("Click Submit button")
    def click_submit(self):
        try: 
            self.click(self.submit_button)
            logger.info("Clicked Submit button")
            allure.attach(
            self.driver.get_screenshot_as_png(),
            name="After Submit Click",
            attachment_type=allure.attachment_type.PNG)
        except:
            self.click(self.submit_button_fallback)
            logger.info('SUCCESS: Self Healing Locator Selected')
           
    @allure.step("Verify success message is displayed")
    def is_success_message_displayed(self, timeout=10) -> bool:
        try:
            self.wait.until(
                lambda d: self.is_element_present(self.success_message, timeout=timeout))
            logger.info("✅ Success message displayed")
            return True
        except Exception as e:
            logger.error(f"❌ Success message not found: {e}")
            return False

    @allure.step("Complete Product Dimension Flow")
    def complete_product_dimension_flow(self, product_code: str, height: str, width: str, depth: str):
        """
        Full end-to-end flow:
        1. Enter product code
        2. Click Search
        3. Enter Height, Width, Depth
        4. Click Submit
        5. Verify success
        """
        self.click_search_bar_product()
        self.enter_product_code(product_code)
        self.click_search()
        self.enter_height(height)
        self.enter_width(width)
        self.enter_depth(depth)
        self.take_photo_using_camera()
        self.click_submit()

        assert self.is_success_message_displayed(), "Product dimension update failed"
        logger.info("✅ Product dimension flow completed successfully")