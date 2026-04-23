import os 
import pytest
from utilities.driver_factory import DriverFactory
from utilities.json_reader import load_test_data
import logging
import os

def pytest_addoption(parser):
    parser.addoption("--env", default="uat", help="Environment: uat, stage, beta")

@pytest.fixture(scope="session")
def test_data(request):
    env = request.config.getoption("--env")
    return load_test_data(env)

@pytest.fixture(scope="function")
def driver(request):
    env = request.config.getoption("--env")
    driver = DriverFactory.get_driver(env=env)
    print(f"\n ▶️  Running tests on environment: {env}")
    yield driver
    driver.quit()