from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
from pages.base_page import BasePage
from pages.home_page import HomePage
import os
import allure
import time 
import logging

logger = logging.getLogger(__name__)

class LoginPage(BasePage):
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.screenshot_dir = "screenshots"
        os.makedirs(self.screenshot_dir, exist_ok=True) 

    my_tawasol_button = (AppiumBy.ACCESSIBILITY_ID, 'myTawasol')
    username_field = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.EditText").instance(0)')
    password_field = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.EditText").instance(1)')
    rememberme_toggle = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.Switch")')
    sign_in_button = (AppiumBy.XPATH, '//android.view.View[@content-desc="Sign In"]') 
    dashboard_title = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Home")')
    dashboard_title_fallback = (AppiumBy.XPATH, '//android.view.View[@content-desc="Home\nBETA"]')
    

    def click_my_tawasol(self):
        time.sleep(3)
        btn = self.wait.until(EC.element_to_be_clickable(self.my_tawasol_button))
        btn.click()
        logger.info('Selected myTawasol Login Method')
        allure.attach(
            self.driver.get_screenshot_as_png(),
            name="Clicked myTawasol",
            attachment_type=allure.attachment_type.PNG
        )

    def enter_username(self, username):
        logger.info(f"Entering username: {username}")
        field = self.wait.until(EC.presence_of_element_located(self.username_field))
        field.click()
        field.send_keys(username)
        allure.attach(
            self.driver.get_screenshot_as_png(),
            name=f"Entered Username: {username}",
            attachment_type=allure.attachment_type.PNG
        )

    def enter_password(self, password):
        logger.info(f"Entering password: {'*' * len(password)}")
        field = self.wait.until(EC.presence_of_element_located(self.password_field))
        field.click()
        time.sleep(5)
        field.send_keys(password)
        logger.info("Password entered")
        allure.attach(
            self.driver.get_screenshot_as_png(),
            name=f"Entered Password: {password}",
            attachment_type=allure.attachment_type.PNG
        )

    def remember_me_toggle(self, remember_me: bool):
        if remember_me == True: 
            self.click(self.rememberme_toggle)
            logger.info("Remember Me toggled ON")
        else:
            self.click(self.rememberme_toggle)
            logger.info("Remember Me left OFF")

    def click_sign_in_button(self, retries=5, timeout=10):
        """
        Robustly clicks the 'Sign In' button with retries and explicit waits.
        """
        sign_in_locator = (AppiumBy.ACCESSIBILITY_ID, "Sign In")  
        # sign_in_locator = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Sign In")')
        # sign_in_locator = (AppiumBy.ID, "com.yourapp:id/sign_in_button") # if you know the resource-id
        for attempt in range(retries):
            try:
                logger.info(f"Attempt {attempt + 1} to click 'Sign In' button...")
                button = WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(sign_in_locator))
                # self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", button)
                button.click()
                logger.info("✅ 'Sign In' button clicked successfully!")
                return

            except (TimeoutException, ElementClickInterceptedException, NoSuchElementException) as e:
                logger.warning(f"Click failed on attempt {attempt + 1}: {e}")
                time.sleep(1)
        raise Exception("Failed to click 'Sign In' button after multiple attempts.")

    def is_logged_in(self):
        """Check if login was successful (e.g., dashboard appears)"""
        try:
            self.wait.until(
                EC.presence_of_element_located(self.dashboard_title)
            )
            return True
        except:
            try:
                self.wait.until(
                    EC.presence_of_element_located(self.dashboard_title_fallback)
                )
                logger.info("Using Self Healing Locators - Dashboard Title Fallback worked")
                return True
            except NoSuchElementException:
                raise
                

    # --- COMPOSITE METHOD ---

    @allure.step("Complete Login Flow: myTawasol → Username → Password → Remember Me → Sign In")
    def complete_login_flow(self, username, password, remember_me=True):
        """
        Automate full login flow
        :param username: str
        :param password: str
        :param remember_me: bool (True=ON, False=OFF)
        """
        self.click_my_tawasol()
        self.driver.implicitly_wait(5)
        self.enter_username(username)
        self.enter_password(password)
        self.hide_keyboard() 
        self.remember_me_toggle(remember_me)
        self.click_sign_in_button()
        time.sleep(10)
        logger.info('SUCCESS: Completed full login flow')
        assert self.is_logged_in(), "Login failed - user not redirected to dashboard"
        

    @allure.step("Login and navigate to Home")
    def login_and_go_to_home(self, username, password, remember_me=True):
        """
        Complete login flow and return HomePage object
        """
        self.complete_login_flow(username, password, remember_me)
        self.driver.implicitly_wait(30)
        logger.info("✅ Login successful — returning HomePage")
        return HomePage(self.driver)


class AuthorityMatrixLoginManager(BasePage):
    """
    Manages login for different user roles based on authority matrix
    """
    def __init__(self, driver):
        super().__init__(driver)
        self.login_page = LoginPage(driver)
        self.driver = driver
        self.username_field = (AppiumBy.ID, "com.storeconnect:id/username")
        self.password_field = (AppiumBy.ID, "com.storeconnect:id/password")
        self.login_button = (AppiumBy.ID, "com.storeconnect:id/login_btn")

    def login_as_role(self, username, password):
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.presence_of_element_located(self.username_field)).send_keys(username)
        self.driver.find_element(*self.password_field).send_keys(password)
        self.driver.find_element(*self.login_button).click()
        wait.until(EC.presence_of_element_located((AppiumBy.ID, "com.storeconnect:id/dashboard_title")))
    
class LoginAsPartner(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.login_page = LoginPage(driver)
        self.driver = driver
    login_as_partner_button = (AppiumBy.ACCESSIBILITY_ID, 'Login as Partner')
    username_field = (AppiumBy.XPATH, '//android.widget.EditText[@text="1274231"]')
    partner_username_field = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.EditText").instance(0)')
    password_field = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.EditText").instance(1)')
    dashboard_title_fallback = (AppiumBy.XPATH, '//android.view.View[@content-desc="Home\nBETA"]')
    sign_in_button = (AppiumBy.ACCESSIBILITY_ID, 'Sign In')

    def is_logged_in(self):
        """Check if login was successful (e.g., dashboard appears)"""
        try:
            self.wait.until(
                EC.presence_of_element_located(self.dashboard_title)
            )
            return True
        except:
            try:
                self.wait.until(
                    EC.presence_of_element_located(self.dashboard_title_fallback)
                )
                logger.info("Using Self Healing Locators - Dashboard Title Fallback worked")
                return True
            except NoSuchElementException:
                raise

    def login_as_partner(self, partner_username, partner_password):
        self.driver.implicitly_wait(5)
        time.sleep(3)
        self.click(self.login_as_partner_button)
        logger.info("")
        try: 
            field = self.wait_for_clickable(self.username_field)
            field.click()
            field.clear()
            field.send_keys(partner_username)
            logger.info("Entered Partner Username")
        except: 
            fallback = self.wait_for_clickable(self.partner_username_field)
            fallback.click()
            fallback.clear()
            fallback.send_keys(partner_username)
            logger.info("Fallback: Entered Partner Username using alternative locator")
        time.sleep(2)
        self.click(self.password_field)
        self.send_keys(self.password_field, partner_password)
        logger.info("Entered Partner Password")
        self.hide_keyboard()
        self.click(self.sign_in_button)
        logger.info("✅ Logged in as Partner User")
        assert self.is_logged_in(), "Login failed - user not redirected to dashboard"
        return HomePage(self.driver)

    def approve_and_reject_request_flow(self, approve: bool):
        """Approve or Reject EROS Discount Voucher request"""
        self.navigate_to_authority_matrix()
        self.open_request_by_barcode(barcode="")
        time.sleep(5)
        if approve:
            approve_button = (AppiumBy.ACCESSIBILITY_ID, 'Approve')
            self.click(approve_button)
            logger.info("✅ Approved EROS Discount Voucher request")
        else:
            reject_button = (AppiumBy.ACCESSIBILITY_ID, 'Reject')
            self.click(reject_button)
            logger.info("✅ Rejected EROS Discount Voucher request")
        time.sleep(3)
        self.driver.press_keycode(4)  
        logger.info("Navigated back to Home Page after approving/rejecting EROS Discount Voucher request")
        time.sleep(5)
    