import pytest
import logging
import allure
from pages.login_page import LoginPage
from pages.base_page import BasePage 
from pages.product_details_page import ProductDetailsPage
from pages.change_branch_page import ChangeBranchPage
from test_cases.tc_complete_flow import test_valid_login

logger = logging.getLogger(__name__)
@allure.epic("Details")
@allure.feature("Product Details")
@allure.story("User views product details")
def test_product_details_flow(driver, test_data):
    test_valid_login(driver, test_data)
    product_data = test_data['product_dimension']
    product_code = product_data.get('product_code', product_data.get('product_barcode'))
    logger.info(f"Starting product details test for product: {product_code}")
    product_details_page = ProductDetailsPage(driver)
    product_details_page.complete_product_details_flow(product_code=product_code)
    logger.info("✅ Product details flow completed successfully")