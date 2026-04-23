from appium.webdriver.common.appiumby import AppiumBy
from pages.base_page import BasePage
import allure
import logging
import time 

logger = logging.getLogger(__name__)

class ServiceAndRepairPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
    _base_view = '//android.view.View[@content-desc="Customer not found. Please enter the following details to create a new return request.\nRequest Entry\nCustomer Name *\nMobile Number *\nEmail *\nItem Name *\nTransaction Date *\nIssue for description *\nUnder Warranty:\nYes"]'
    customer_name_field = f"{_base_view}/android.widget.EditText[1]"
    email_field = f"{_base_view}/android.widget.EditText[2]"
    item_name_field = f"{_base_view}/android.widget.EditText[3]"
    issue_of_description_field = f"{_base_view}/android.widget.EditText[4]"

    def get_page_title(self):
        title_locator = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Service & Repair")')
        title_element = self.wait_for_visible(title_locator, timeout=20)
        title_text = title_element.text.strip()
        if not title_text:
            title_text = title_element.get_attribute("contentDescription").strip()
        logger.info(f"✅ Page title retrieved: '{title_text}'")
        return title_text
    
    def create_new_request(self):
        new_request_button = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.Button").instance(2)')
        time.sleep(5)
        new_request_btn = self.wait_for_clickable(new_request_button, timeout=50)
        new_request_btn.click()
        logger.info("✅ Clicked on New Request button")
        allure.attach(
            self.driver.get_screenshot_as_png(),
            name="New Request Clicked",
            attachment_type=allure.attachment_type.PNG)
        
    def navigate_to_phone_num_tab(self):
        phone_num_tab_locator = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Phone Number")')
        phone_num_tab = self.wait_for_clickable(phone_num_tab_locator, timeout=50)
        phone_num_tab.click()
        logger.info("✅ Navigated to Phone Number tab")
        allure.attach(
            self.driver.get_screenshot_as_png(),
            name="Phone Number Tab Clicked",
            attachment_type=allure.attachment_type.PNG)
    def fetch_customer_by_phone_number(self, phone_number: str):
        phone_input_locator = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.EditText")')
        phone_input = self.wait_for_visible(phone_input_locator, timeout=50)
        time.sleep(3)
        phone_input.click()
        phone_input.send_keys(phone_number)
        logger.info(f"✅ Entered phone number: {phone_number}")
        time.sleep(3)
        try:
            fetch_button_locator = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Fetch Customer")') #STAG Locator
            fetch_button = self.wait_for_clickable(fetch_button_locator, timeout=10)
            fetch_button.click()
            logger.info("✅ SUCCESS: Customer Fetched by Phone Number")
        except:
            fallback_button_search = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.Button").instance(1)') #UAT
            fetch_button = self.wait_for_clickable(fallback_button_search, timeout=10)
            fetch_button.click()
            logger.info("✅ SUCCESS: Customer Fetched by Phone Number using fallback locator")
        allure.attach(
            self.driver.get_screenshot_as_png(),
            name="Fetch Customer Clicked",
            attachment_type=allure.attachment_type.PNG)
    ## -- Request Entry Flow -- ##
    def enter_customer_name(self, customer_name: str):
        customer_name_locator = (AppiumBy.XPATH, self.customer_name_field)
        customer_name_input = self.wait_for_visible(customer_name_locator, timeout=50)
        customer_name_input.click()
        logger.info(f"✅ Clicked on Customer Name input field")
        customer_name_input.send_keys(customer_name)
        logger.info(f"✅ Entered customer name: {customer_name}")
        allure.attach(
            self.driver.get_screenshot_as_png(),
            name="Customer Name Entered",
            attachment_type=allure.attachment_type.PNG)
     
    def enter_email(self, email: str):
        email_locator = (AppiumBy.XPATH, self.email_field)
        email_input = self.wait_for_visible(email_locator, timeout=50)
        email_input.click()
        email_input.send_keys(email)
        logger.info(f"✅ Entered email: {email}")
        allure.attach(
            self.driver.get_screenshot_as_png(),
            name="Email Entered",
            attachment_type=allure.attachment_type.PNG)
    def item_name_manully(self, item_name: str):
        item_name_locator = (AppiumBy.XPATH, self.item_name_field)
        item_name_input = self.wait_for_visible(item_name_locator, timeout=50)
        item_name_input.click()
        item_name_input.send_keys(item_name)
        logger.info(f"✅ Entered item name: {item_name}")
        allure.attach(
            self.driver.get_screenshot_as_png(),
            name="Item Name Entered",
            attachment_type=allure.attachment_type.PNG)
    def transaction_date(self): 
        transaction_date_locator = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Select Transaction Date")')
        transaction_date_input = self.wait_for_clickable(transaction_date_locator, timeout=50)
        transaction_date_input.click()
        logger.info("✅ Clicked on Transaction Date")
        allure.attach(
            self.driver.get_screenshot_as_png(),
            name="Transaction Date Clicked",
            attachment_type=allure.attachment_type.PNG)
        date_select_icon = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().descriptionMatches("^1,.*$")')
        date_select_button = self.wait_for_clickable(date_select_icon, timeout=50)  
        date_select_button.click()
        ok_button_locator = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("OK")')
        ok_button = self.wait_for_clickable(ok_button_locator, timeout=50)  
        ok_button.click()
        logger.info("✅ Transaction Date selected")
    

    def fetch_customer(self, phone_number: str):
        title = self.get_page_title()
        assert title == "Service & Repair", f"❌ Expected 'Service & Repair', got '{title}'"
        logger.info("✅ Page title validated")
        time.sleep(5)
        self.create_new_request()
        self.navigate_to_phone_num_tab()
        self.fetch_customer_by_phone_number(phone_number)

    def issue_of_description(self, issue_description_text: str):
        issue_description_locator = (AppiumBy.XPATH, self.issue_of_description_field)
        issue_description_input = self.wait_for_visible(issue_description_locator, timeout=50)
        issue_description_input.click()
        issue_description_input.send_keys(issue_description_text)
        logger.info(f"✅ Entered issue description: {issue_description_text}")
        allure.attach(
            self.driver.get_screenshot_as_png(),
            name="Issue Description Entered",
            attachment_type=allure.attachment_type.PNG)
    def add_image(self):
        image_locator = f"{self._base_view}/android.view.View[3]/android.view.View/android.view.View"
        add_image_locator = (AppiumBy.XPATH, image_locator)
        add_image_button = self.wait_for_clickable(add_image_locator, timeout=50)
        add_image_button.click()
        logger.info("✅ Clicked on Add Image button")
        allure.attach(
            self.driver.get_screenshot_as_png(),
            name="Add Image Clicked",
            attachment_type=allure.attachment_type.PNG)
        
        shutter_button = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("com.android.camera2:id/shutter_button")')
        self.wait_for_clickable(shutter_button)
        self.click(shutter_button)
        self.driver.implicitly_wait(20)
        done_button = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("com.android.camera2:id/done_button")')
        self.wait_for_clickable(done_button)
        self.click(done_button)
        self.driver.implicitly_wait(20)
        
    def submit_req(self):
        try:
            submit_button_locator = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Submit Request")') # STAG 
            submit_button = self.wait_for_clickable(submit_button_locator, timeout=50)
            submit_button.click()
            logger.info("✅ Clicked on Submit button")
            allure.attach(
                self.driver.get_screenshot_as_png(),
                name="Submit Button Clicked",
                attachment_type=allure.attachment_type.PNG)
        except: 
            fallback_button = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Okay")') # UAT
            submit_button = self.wait_for_clickable(fallback_button, timeout=50)    
            submit_button.click()
            logger.info("✅ Clicked on Submit button using fallback locator")
        

    def complete_service_request_flow(self,  customer_name: str, email: str, item_name: str, issue_description_text: str):
        self.enter_customer_name(customer_name=customer_name)
        self.hide_keyboard()
        self.enter_email(email=email)   
        self.hide_keyboard()
        self.item_name_manully(item_name=item_name)
        self.hide_keyboard()
        time.sleep(2)
        self.swipe_to_bottom()
        self.transaction_date()
        self.issue_of_description(issue_description_text=issue_description_text)    
        self.hide_keyboard()
        self.add_image()
        self.submit_req()

        
    def click_filter_icon(self):
        time.sleep(5)
        filter_icon_locator = (AppiumBy.XPATH, '//android.widget.FrameLayout[@resource-id="android:id/content"]/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View[1]/android.widget.Button[2]')
        filter_icon_element = self.wait_for_clickable(filter_icon_locator, timeout=20)
        filter_icon_element.click()
        logger.info("✅ Clicked on Filter icon")
        allure.attach(
            self.driver.get_screenshot_as_png(),
            name="Filter Icon Clicked",
            attachment_type=allure.attachment_type.PNG)
    def filter_by_phone_number(self, phone_number: str):
        phone_filter_locator = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.EditText").instance(1)')
        phone_filter_input = self.wait_for_visible(phone_filter_locator, timeout=50)
        phone_filter_input.click()
        phone_filter_input.send_keys(phone_number)
        logger.info(f"✅ Entered phone number in filter: {phone_number}")
        allure.attach(
            self.driver.get_screenshot_as_png(),
            name="Phone Number Filter Entered",
            attachment_type=allure.attachment_type.PNG)
    def apply_filter(self):
        apply_filter_button = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Apply")')
        apply_filter = self.wait_for_clickable(apply_filter_button, timeout=50)
        apply_filter.click()
        logger.info("✅ Clicked on Apply Filter button")
        allure.attach(
            self.driver.get_screenshot_as_png(),
            name="Apply Filter Clicked",
            attachment_type=allure.attachment_type.PNG)
    def apply_filter_by_phone_number(self, phone_number: str):
        self.click_filter_icon()
        self.filter_by_phone_number(phone_number=phone_number)
        self.driver.press_keycode(66)
        logger.info("✅ Keyboard hidden after entering phone number in filter")
        time.sleep(3)
        self.apply_filter()
    def verify_filtered_results_for_phone_number(self, phone_number: str):
        result_locator = (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().descriptionContains("{phone_number}")')
        result_element = self.wait_for_visible(result_locator, timeout=50)
        assert result_element is not None, f"❌ No results found for phone number: {phone_number}"
        logger.info(f"✅ Filtered results verified for phone number: {phone_number}")

    

