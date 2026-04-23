import json
import os

def load_test_data(env="uat"):
    """
    Load test data for given environment
    """
    file_path = os.path.join("test_data", f"test_data_{env}.json")
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Test data file not found: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)