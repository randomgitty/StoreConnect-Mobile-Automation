import json
import os
from appium import webdriver
from appium.options.android import UiAutomator2Options 

class DriverFactory:
    @staticmethod
    
    def get_driver(env="beta"):
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        config_path = os.path.join(project_root, "config", f"{env}.json")

        with open(config_path, "r") as f:
            config = json.load(f)

        app_path = config["app_path"]

        # Convert relative app path to absolute path from project root
        if not os.path.isabs(app_path):
            app_path = os.path.join(project_root, app_path)

        app_path = os.path.abspath(app_path)

        if not os.path.exists(app_path):
            raise FileNotFoundError(f"APK not found at: {app_path}")
            

        desired_caps = {
            'platformName': config['platform_name'],
            'appium:deviceName': config['device_name'],
            'appium:app': config['app_path'],
            'appium:automationName': config['automation_name'],
            'appium:noReset': False,
            'appium:fullReset': False, 
            'appium:newCommandTimeout': 600,
            'appium:autoGrantPermissions': True, 
            "skipDeviceInitialization": True,
            "disableAndroidWatchers": True,                      # removes uiautomator lag
            "ignoreUnimportantViews": True,                      # huge speed boost
            "enableMultiWindows": True,
            "uiautomator2ServerLaunchTimeout": 60000,
            "adbExecTimeout": 60000,
            # Critical for Android 11+
            "settings[waitForIdleTimeout]": 0,                   # disables idle wait
            "settings[waitForSelectorTimeout]": 30000,
            "settings[actionAcknowledgmentTimeout]": 500,       # was 3000 ms → too long
            "settings[keyInjectionDelay]": 0,
            "appium:enforceXPath1": True, 
        }
        # Start Appium session
        options = UiAutomator2Options().load_capabilities(desired_caps)
        driver = webdriver.Remote('http://127.0.0.1:4723', options=options)
        return driver