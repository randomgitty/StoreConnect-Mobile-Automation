import logging 
from pages.login_page import LoginPage
from pages.service_and_repair_page import ServiceAndRepairPage
logger = logging.getLogger(__name__)

def test_service_and_repair_flow(driver, test_data): 
    credentials = test_data['login_credentials']
    username = credentials['username']
    password = credentials['password']
    remember_me = credentials.get('remember_me', True)
    phone_number = test_data['service_and_repair']['phone_number']
    login_page = LoginPage(driver)
    home_page = login_page.login_and_go_to_home(username=username, password=password, remember_me=remember_me)
    home_page.navigate_to_service_and_repair()
    service_repair_page = ServiceAndRepairPage(driver)
    service_repair_page.fetch_customer(phone_number=phone_number)
    service_repair_page.complete_service_request_flow(customer_name=test_data['service_and_repair']['customer_name'],
                                                    email=test_data['service_and_repair']['email'], 
                                                    item_name=test_data['service_and_repair']['item_name'], 
                                                    issue_description_text=test_data['service_and_repair']['issue_description_text'])
    logger.info("✅ Service Request submitted successfully")
    #service_repair_page.apply_filter_by_phone_number(phone_number=phone_number)
    #service_repair_page.verify_filtered_results_for_phone_number(phone_number=phone_number)
    #logger.info("✅ Completed Service and Repair flow successfully") 
