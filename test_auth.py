import requests
import time

# Base URL for the application
BASE_URL = 'http://localhost:8081'

def test_signup():
    # Test signup with a new user
    signup_data = {
        'username': f'testuser_{int(time.time())}',  # Use timestamp to ensure unique username
        'password': 'testpassword'
    }
    
    print(f"Attempting to sign up with username: {signup_data['username']}")
    
    response = requests.post(f"{BASE_URL}/signup", data=signup_data)
    
    print(f"Signup Response Status: {response.status_code}")
    print(f"Signup Response URL: {response.url}")
    print(f"Signup Response Content: {response.text[:100]}..." if len(response.text) > 100 else response.text)
    
    return signup_data

def test_login(credentials):
    # Test login with the created user
    login_data = {
        'username': credentials['username'],
        'password': credentials['password']
    }
    
    print(f"\nAttempting to log in with username: {login_data['username']}")
    
    response = requests.post(f"{BASE_URL}/login", data=login_data)
    
    print(f"Login Response Status: {response.status_code}")
    print(f"Login Response URL: {response.url}")
    print(f"Login Response Content: {response.text[:100]}..." if len(response.text) > 100 else response.text)

if __name__ == '__main__':
    # Run the tests
    user_credentials = test_signup()
    test_login(user_credentials)