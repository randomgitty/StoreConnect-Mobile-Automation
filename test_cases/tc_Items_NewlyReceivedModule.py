import logging 
import allure 
import pytest
from pages.items_with_new_price_page import ItemsWithNewPricePage 
from pages.items_with_no_sales_page import ItemsWithNoSalesPage 
from pages.items_newly_recieved_page import ItemsNewlyReceivedPage
from pages.login_page import LoginPage
from pages.product_details_page import ProductDetailsPage
logger = logging.getLogger(__name__)


@allure.epic("Items")
@allure.feature("Items With No Sales")
@allure.story("User views items with no sales via myTawasol")

def test_items_newly_received(driver, test_data):
    credentials = test_data['login_credentials']
    username = credentials['username']
    password = credentials['password']
    remember_me = credentials.get('remember_me', True)

    login_page = LoginPage(driver)
    home_page = login_page.login_and_go_to_home(username=username, password=password, remember_me=remember_me)
    home_page.navigate_to_items_newly_received()
    
    items_page = ItemsNewlyReceivedPage(driver)
    has_data = items_page.complete_item_with_newly_received_flow()

    if has_data:
        product_details = ProductDetailsPage(driver)
        product_details.navigate_to_stocks()
        logger.info("✅ Navigated to Stocks tab")
        product_details.navigate_to_stocks()
        product_details._log_stock_info()
        product_details.navigate_to_sales()
        product_details._log_sales_info()
    else:
        logger.info("✅ No data case handled — test passed without product interaction")
