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

def test_items_with_no_sales(driver, test_data): 
    credentials = test_data['login_credentials']
    username = credentials['username']
    password = credentials['password']
    remember_me = credentials.get('remember_me', True)

    login_page = LoginPage(driver)
    home_page = login_page.login_and_go_to_home(username=username, password=password, remember_me=remember_me)
    home_page.navigate_to_items_with_no_sales()
    items_no_sales = ItemsWithNoSalesPage(driver)
    items_no_sales.complete_item_with_no_sales_flow()
    logger.info("✅ Completed Items with No Sales flow successfully")
    product_details = ProductDetailsPage(driver)
    product_details.navigate_to_stocks()
    product_details._log_stock_info()
    product_details.navigate_to_sales()
    product_details._log_sales_info()