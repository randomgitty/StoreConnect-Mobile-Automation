from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from pages.base_page import BasePage
from pages.change_branch_page import ChangeBranchPage
from pages.home_page import HomePage

import os
import allure
import time 
import logging
import json

logger = logging.getLogger(__name__)


class EROS_DiscountVoucherPage(BasePage):
    def __init__(self, driver): 
        super().__init__(driver)
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
    tamayaz_tab = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Tamayaz Card")')
    phone_tab = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Phone Number")')
    tamayaz_input_field = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.EditText")')
    phone_input_field = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.EditText")')
    fetch_customer = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.Button").instance(1)')
    barcode_field = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.EditText").instance(1)') 
    fetch_product = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.Button").instance(2)')
    retry_button = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Retry")')
    amount_radio_button = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Amount")')
    percentage_radio_button = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Percentage")')
    discount_amount_field = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.EditText").instance(1)')
    discount_percentage_field = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.EditText").instance(3)')
    quantity_field = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("1")')
    submit_request_button = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Submit Request")')
    approve_button = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Approve")')
    reject_button = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Reject")')
    remarks_field = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.EditText").instance(1)')
    ok_button = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Okay")')

    def get_page_title(self):
        try:
            title = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("EROS Discount Vocher")')
            title_element = self.wait_for_visible(title, timeout=20)
            title_text = title_element.text.strip()
            if not title_text:
                title_text = title_element.get_attribute("contentDescription").strip()
            logger.info(f"✅ Page title retrieved: '{title_text}'")
            return title_text
        except: 
            title_locator = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("EROS Discount Voucher")')
            title_element = self.wait_for_visible(title_locator, timeout=20)
            title_text = title_element.text.strip()
            if not title_text:
                title_text = title_element.get_attribute("contentDescription").strip()
            logger.info(f"✅ Page title retrieved: '{title_text}'")
            return title_text
    
    def click_add_request_button(self):
        add_request_button = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.Button").instance(2)')
        time.sleep(5)
        button_element = self.wait_for_clickable(add_request_button, timeout=10)
        button_element.click()
        logger.info("✅ Clicked 'Add Request' button on EROS Discount Voucher page")

    def initiate_request(self, customer_identification_by: str, tamayaz_id, phone_number):
        if customer_identification_by == 'Tamayaz Card': 
            self.click(self.tamayaz_tab)
            logger.info("Selected 'Tamayaz Card' tab for customer identification")
            time.sleep(1)
            self.wait_for_clickable(self.tamayaz_input_field) 
            self.click(self.tamayaz_input_field)
            self.send_keys(self.tamayaz_input_field, tamayaz_id)
            logger.info(f"Entered Tamayaz ID: {tamayaz_id}")
            self.click(self.fetch_customer)
            logger.info("SUCCESS: Fetched customer details using Tamayaz ID")
        else: 
            self.click(self.phone_tab)
            logger.info("Selected 'Phone Number' tab for customer identification")
            time.sleep(1)
            self.wait_for_clickable(self.phone_input_field) 
            self.click(self.phone_input_field)
            self.send_keys(self.phone_input_field, phone_number)
            logger.info(f"Entered Phone Number")
            self.click(self.fetch_customer)
            logger.info("SUCCESS: Fetched customer details using Phone Number")

    

    def enter_product_barcode(self, barcode): 
            self.wait_for_clickable(self.barcode_field, timeout=10)
            self.click(self.barcode_field)
            logger.info("Entering product barcode...")
            self.send_keys(self.barcode_field, barcode)
            logger.info(f"Entered product barcode: {barcode}")
            self.click(self.fetch_product)
            logger.info("SUCCESS: Product Details Fetched")
            if self.is_element_visible(self.retry_button):
                self.click(self.retry_button)
                logger.info("Clicked 'Retry' button to re-fetch product details")
            else: 
                pass 
                time.sleep(5)

    def discount_type(self, discount_type: bool, amount, percentage):
        if discount_type == True: 
            self.click(self.amount_radio_button)
            logger.info("Selected 'Amount' discount type")
            self.wait_for_clickable(self.discount_amount_field, timeout=10)
            self.click(self.discount_amount_field)
            self.send_keys(self.discount_amount_field, amount)
            logger.info(f"Entered discount amount: {amount}")
            self.hide_keyboard()
            self.swipe_to_down()
            logger.info("Successfully Swiped down to Submit Request button")
            self.click(self.submit_request_button)
            logger.info("Clicked on Submit Request button")
        else: 
            self.click(self.percentage_radio_button)
            logger.info("Selected 'Percentage' discount type")
            self.wait_for_clickable(self.discount_percentage_field, timeout=10)
            self.click(self.discount_percentage_field)
            self.send_keys(self.discount_percentage_field, percentage)
            logger.info(f"Entered discount percentage: {percentage}")
            self.hide_keyboard()
            self.swipe_to_bottom()
            logger.info("Successfully Swiped down to Submit Request button")
            self.click(self.submit_request_button)
            logger.info("Clicked on Submit Request button")

    def validate_request_submitted(self): 
        time.sleep(8)
        cards = self.driver.find_elements(AppiumBy.XPATH, "//*[contains(@content-desc, 'Al Warqa Branch')]")
        assert len(cards) > 0, "No request found for 'Al Warqa Branch'!"
        logger.info("✅ Request for 'Al Warqa Branch' found (Pending status assumed)")

    def click_ok_button(self): 
        time.sleep(2)
        ok_button = (AppiumBy.ACCESSIBILITY_ID, "Okay") 
        try:
            logger.info("Looking for 'Okay' confirmation dialog...")
            ok_element = self.wait_for_clickable(ok_button, timeout=10)
            ok_element.click()
            logger.info("Clicked 'Okay' on confirmation dialog.")
        except TimeoutException:
            logger.info("No 'Okay' dialog found — proceeding without it.")
            #self.take_screenshot("no_okay_dialog")

    def complete_eros_discount_voucher_flow(self, customer_identification_by: str, tamayaz_id, phone_number, barcode, discount_type: bool, amount, percentage):
        self.get_page_title()
        self.click_add_request_button()
        logger.info("Navigating to Initiate Request Page...")
        self.initiate_request(customer_identification_by, tamayaz_id, phone_number)
        self.enter_product_barcode(barcode)
        self.swipe_to_down()
        logger.info("Successfully Swiped down to Discount Type section")
        self.discount_type(discount_type, amount, percentage)
        logger.info("✅ EROS Discount Voucher request submitted successfully")
        self.click_ok_button()
        self.validate_request_submitted()
        self.driver.press_keycode(4) 
        logger.info("Navigated back to Home Page after initiating EROS Discount Voucher request")
        time.sleep(5)

    def open_request(self):
        product_card_locator = (
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().descriptionContains("Al Warqa").descriptionContains("Pending")'
        )

        # 3. Click the first request card
        pos_cards = self.driver.find_elements(*product_card_locator)
        if not pos_cards:
            raise AssertionError("No POS Return card found with 'Al Warqa' and 'Pending' status.")
        pos_cards[0].click()
 
    def open_request_by_barcode(self, barcode):
        """PARTNER: Find and open the request with exact barcode"""
        time.sleep(5)
        cards = self.driver.find_elements(
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().descriptionContains("Barcode:").clickable(true)'
        )
        for card in cards:
            desc = card.get_attribute("content-desc") or ""
            if barcode in desc and "Pending" in desc:
                card.click()
                logger.info(f"Opened request card with barcode {barcode}")
                time.sleep(3)
                return True
        raise AssertionError(f"Request with barcode {barcode} not found for Partner")



    def approve_or_reject_request(self, approve=True, remarks=None):
        """PARTNER: Approve or Reject with optional remarks"""
        if approve:
            self.click(self.approve_button)
            logger.info("PARTNER APPROVED THE REQUEST")
        else:
            self.click(self.reject_button)
            time.sleep(1)
            self.send_keys(self.remarks_field, remarks or "Test automation script rejected")
            self.click(self.reject_button)
            logger.info("PARTNER REJECTED THE REQUEST WITH REMARKS")

        time.sleep(5)
        allure.attach(self.driver.get_screenshot_as_png(),
                      name="Final_Status_After_Partner_Action",
                      attachment_type=allure.attachment_type.PNG)
    
        
    def approve_request(self):
        self.swipe_to_down()
        self.click(self.approve_button)
        logger.info("PARTNER APPROVED THE REQUEST")
        time.sleep(1)
        
        #self.click(self.ok_button) #locator needs to be updated 
   
        

        

    


        