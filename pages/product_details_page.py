import allure
import logging
from appium.webdriver.common.appiumby import AppiumBy
from pages.base_page import BasePage
from pages.product_dimension_page import ProductDimensionPage

logger = logging.getLogger(__name__)


class ProductDetailsPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.product_dimension_page = ProductDimensionPage(self.driver)
        self.product_search_field = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.EditText")')
        self.search_button = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Search")')
        self.product_title = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Product Details")')
        self.stocks_tab = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("STOCK")')
        self.sales_tab = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("SALES")')
        self.stock_info_container = (AppiumBy.XPATH, '//android.view.View[contains(@content-desc, "Current Stock in Branch")]')
        self.sales_info_container = (AppiumBy.XPATH, '//android.view.View[contains(@content-desc, "Yesterday")]')

    def navigate_to_stocks(self):
        """Navigate to Stocks section from Product Details"""
        try:
            self.wait_for_clickable(self.stocks_tab)
            self.click(self.stocks_tab)
            logger.info("✅ Navigated to STOCKS tab")
            allure.attach(
                self.driver.get_screenshot_as_png(),
                name="Stocks Tab View",
                attachment_type=allure.attachment_type.PNG
            )
        except Exception as e:
            logger.error(f"❌ Failed to navigate to Stocks section: {e}")
            raise

    def navigate_to_sales(self):
        """Navigate to Sales section from Product Details"""
        try:
            self.wait_for_clickable(self.sales_tab)
            self.click(self.sales_tab)
            logger.info("✅ Navigated to SALES tab")
            allure.attach(
                self.driver.get_screenshot_as_png(),
                name="Sales Tab View",
                attachment_type=allure.attachment_type.PNG
            )
        except Exception as e:
            logger.error(f" Failed to navigate to Sales section: {e}")
            raise

    def _parse_dynamic_content(self, locator, known_keys):
        """Safely parse key-value pairs from content-desc"""
        try:
            element = self.wait_for_clickable(locator, timeout=10)
            full_text = element.get_attribute("contentDescription").strip()

            if not full_text:
                logger.warning("⚠️ Empty contentDescription")
                return {}

            lines = [line.strip() for line in full_text.split('\n') if line.strip()]
            data = {}
            for i in range(0, len(lines), 2):
                if i + 1 < len(lines):
                    data[lines[i]] = lines[i + 1]
            result = {}
            for expected_key in known_keys:
                for actual_key in data:
                    if expected_key.lower() in actual_key.lower():
                        result[expected_key] = data[actual_key]
                        break
                else:
                    result[expected_key] = "N/A"
            return result

        except Exception as e:
            logger.warning(f"⚠️ Failed to parse content: {e}")
            return {k: "N/A" for k in known_keys}

    def _log_stock_info(self):
        known_keys = [
            "Current Stock in Branch",
            "Quantity Ordered",
            "Last Delivery Date",
            "Reserved / Safety Stock"
        ]
        data = self._parse_dynamic_content(self.stock_info_container, known_keys)
        for key, value in data.items():
            logger.info(f"Stock Tab: {key} = {value}")

    def _log_sales_info(self):
        known_keys = [
            "Yesterday",
            "Last 7 Days Average"
        ]
        data = self._parse_dynamic_content(self.sales_info_container, known_keys)
        for key, value in data.items():
            logger.info(f"Sales Tab: {key} = {value}")

    def complete_product_details_flow(self, product_code: str):
        """
        Complete the product details flow by searching for a product using its code.
        """
        self.click_search_bar_product()
        self.product_dimension_page.enter_product_code(product_code)
        self.product_dimension_page.click_search()
        logger.info(f"✅ Completed product search for: {product_code}")

        self.navigate_to_stocks()
        self._log_stock_info()

        self.navigate_to_sales()
        self._log_sales_info()

        logger.info("✅ Completed full Product Details flow")