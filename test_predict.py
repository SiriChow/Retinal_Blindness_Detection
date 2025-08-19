import requests
import os

# Base URL for the application
BASE_URL = 'http://localhost:8081'

def test_login_and_predict():
    # First login to get a session
    login_data = {
        'username': 'testuser',
        'password': 'testpassword'
    }
    
    # Create a session to maintain cookies
    session = requests.Session()
    
    # Login
    print("Logging in...")
    login_response = session.post(f"{BASE_URL}/login", data=login_data)
    print(f"Login Status: {login_response.status_code}")
    
    if login_response.status_code != 200:
        print("Login failed. Cannot proceed with prediction test.")
        return
    
    # Find a sample image to upload
    sample_dir = 'sampleimages'
    sample_images = [f for f in os.listdir(sample_dir) if os.path.isfile(os.path.join(sample_dir, f))]
    
    if not sample_images:
        print("No sample images found in the sampleimages directory.")
        return
    
    # Use the first sample image
    sample_image_path = os.path.join(sample_dir, sample_images[0])
    print(f"Using sample image: {sample_image_path}")
    
    # Prepare the file for upload
    with open(sample_image_path, 'rb') as img_file:
        files = {'file': (os.path.basename(sample_image_path), img_file, 'image/jpeg')}
        
        # Make the prediction request
        print("\nSending prediction request...")
        predict_response = session.post(f"{BASE_URL}/predict", files=files)
        
        print(f"Prediction Response Status: {predict_response.status_code}")
        
        # Check if the response is JSON
        try:
            result = predict_response.json()
            print("\nPrediction Result:")
            print(f"Predicted Class: {result.get('predicted_class', 'N/A')}")
            print(f"Confidence: {result.get('confidence', 'N/A')}")
            print("\nAll Probabilities:")
            for class_name, prob in result.get('all_probabilities', {}).items():
                print(f"  {class_name}: {prob:.4f}")
        except ValueError:
            print("Response is not JSON. First 500 characters:")
            print(predict_response.text[:500])

if __name__ == '__main__':
    test_login_and_predict()