import allure
import logging
from pages.login_page import LoginPage
from pages.home_page import HomePage
from pages.product_dimension_page import ProductDimensionPage

logger = logging.getLogger(__name__)

@allure.epic("Product Management")
@allure.feature("Product Dimension")
@allure.story("User updates product dimensions after login")
def test_update_product_dimension(driver, test_data):
    credentials = test_data['login_credentials']
    product_data = test_data['product_dimension']
    username = credentials['username']
    password = credentials['password']
    remember_me = credentials.get('remember_me', True)
    product_code = product_data.get('product_code', product_data.get('product_barcode'))
    height = product_data['height']
    width = product_data['width']
    depth = product_data['depth']
    logger.info(f"Starting product dimension test for product: {product_code}")
    login_page = LoginPage(driver)
    home_page = login_page.login_and_go_to_home(username=username, password=password, remember_me=remember_me)
    home_page.navigate_to_product_dimension()
    product_dim_page = ProductDimensionPage(driver)
    product_dim_page.complete_product_dimension_flow(product_code=product_code, height=height, width=width, depth=depth)
    logger.info("✅ Product dimension test completed successfully")