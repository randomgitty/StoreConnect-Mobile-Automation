import json
from pages.login_page import LoginPage

class LoginManager:
    def __init__(self, driver):
        self.driver = driver
        self.users = self._load_credentials()

    def _load_credentials(self):
        with open('config/credentials.json', 'r') as f:
            return json.load(f)['users']

    def login_as_role(self, target_role):
        """Login with the first user having the specified role using the existing LoginPage."""
        for user in self.users:
            if user['role'] == target_role:
                login_page = LoginPage(self.driver)
                home_page = login_page.login_and_go_to_home(
                    username=user['username'],
                    password=user['password'],
                    remember_me=True  
                )
                print(f"✅ Logged in as: {target_role} ({user['username']})")
                return home_page  
        raise ValueError(f"No user found for role: {target_role}")
    
    def get_user_by_role(self, target_role):
        """
        Returns user credentials (dict) for a given role.
        Raises ValueError if not found.
        """
        for user in self.users:
            if user['role'] == target_role:
                return user
        raise ValueError(f"No user found for role: '{target_role}'")   

    def logout(self):
        pass