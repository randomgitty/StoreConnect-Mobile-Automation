import logging 
import time
from pages.top_500_items_OOS_page import Top500ItemsOOS_Page
from pages.login_page import LoginPage
from pages.product_details_page import ProductDetailsPage
logger = logging.getLogger(__name__)

def test_top_500_items_flow(driver, test_data): 
    credentials = test_data['login_credentials']
    username = credentials['username']
    password = credentials['password']
    remember_me = credentials.get('remember_me', True)

    login_page = LoginPage(driver)
    home_page = login_page.login_and_go_to_home(username=username, password=password, remember_me=remember_me)
    home_page.navigate_to_top_500_items()
    top_items_page = Top500ItemsOOS_Page(driver)
    top_items_page.complete__top_500_items_OOS_flow()
    logger.info("✅ Applied Filter in Top 500 Items – OOS successfully")

    product_name = "PURE DRINKING WATER 500ml"
    top_items_page.click_product_card(product_name)
    product_details = ProductDetailsPage(driver)
    product_details.navigate_to_stocks()
    product_details._log_stock_info()
    product_details.navigate_to_sales()
    product_details._log_sales_info()
    driver.press_keycode(4)
    time.sleep(3)
    top_items_page.OOS_items_tab() 
    product_name = "PURE DRINKING WATER 500ml"
    driver.implicitly_wait(5)
    top_items_page.click_product_card(product_name)
    product_details.navigate_to_stocks()
    product_details._log_stock_info()
    product_details.navigate_to_sales()
    product_details._log_sales_info()

    
    