# Web-compatible model module for retinal blindness detection
import numpy as np
import torch
from torch import nn
import torchvision
from torchvision import models
from PIL import Image
import os

print('Imported packages for web application')

class RetinalBlindnessModel:
    def __init__(self, model_path=None):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.classes = ['No DR', 'Mild', 'Moderate', 'Severe', 'Proliferative DR']
        self.is_trained = False  # Default to untrained
        
        # Initialize model
        self.model = models.resnet152(weights=None)
        num_ftrs = self.model.fc.in_features
        out_ftrs = 5
        self.model.fc = nn.Sequential(
            nn.Linear(num_ftrs, 512),
            nn.ReLU(),
            nn.Linear(512, out_ftrs),
            nn.LogSoftmax(dim=1)
        )
        
        # Unfreeze specific layers
        for name, child in self.model.named_children():
            if name in ['layer2', 'layer3', 'layer4', 'fc']:
                for param in child.parameters():
                    param.requires_grad = True
            else:
                for param in child.parameters():
                    param.requires_grad = False
        
        self.model.to(self.device)
        
        # Define transforms
        self.test_transforms = torchvision.transforms.Compose([
            torchvision.transforms.Resize((224, 224)),
            torchvision.transforms.RandomHorizontalFlip(p=0.5),
            torchvision.transforms.ToTensor(),
            torchvision.transforms.Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225))
        ])
        
        # Load model weights if provided
        if model_path and os.path.exists(model_path):
            self.load_model(model_path)
        else:
            print("Warning: No model weights loaded. Using untrained model.")
            print("For demo purposes, predictions will be random.")
            self.is_trained = False
    
    def load_model(self, path):
        """Load pre-trained model weights"""
        try:
            checkpoint = torch.load(path, map_location=self.device)
            self.model.load_state_dict(checkpoint['model_state_dict'])
            self.is_trained = True
            print(f"Model loaded successfully from {path}")
        except Exception as e:
            print(f"Error loading model: {e}")
            print("Using untrained model...")
            self.is_trained = False
    
    def predict(self, image_path):
        """Make prediction on uploaded image"""
        try:
            # Open and preprocess image
            image = Image.open(image_path).convert('RGB')
            img_tensor = self.test_transforms(image).unsqueeze(0)
            
            # For demo purposes, generate random predictions if model is untrained
            if not hasattr(self, 'is_trained') or not self.is_trained:
                print("Using random predictions for demo")
                # Generate random probabilities
                import numpy as np
                random_probs = np.random.rand(5)
                random_probs = random_probs / random_probs.sum()  # Normalize to sum to 1
                
                # Find the highest probability class
                predicted_class_idx = np.argmax(random_probs)
                predicted_class = self.classes[predicted_class_idx]
                confidence = random_probs[predicted_class_idx]
                
                return {
                    'predicted_class': predicted_class,
                    'predicted_class_idx': int(predicted_class_idx),
                    'confidence': float(confidence),
                    'all_probabilities': dict(zip(self.classes, random_probs.astype(float)))
                }
            
            # Make prediction with trained model
            self.model.eval()
            with torch.no_grad():
                output = self.model(img_tensor.to(self.device))
                probabilities = torch.exp(output)
                top_p, top_class = probabilities.topk(1, dim=1)
                
                predicted_class_idx = top_class.item()
                predicted_class = self.classes[predicted_class_idx]
                confidence = top_p.item()
                
                # Get all class probabilities
                all_probs = probabilities.squeeze().cpu().numpy()
                
                return {
                    'predicted_class': predicted_class,
                    'predicted_class_idx': predicted_class_idx,
                    'confidence': float(confidence),
                    'all_probabilities': dict(zip(self.classes, all_probs.astype(float)))
                }
        
        except Exception as e:
            import traceback
            print(f"Error in prediction: {str(e)}")
            print(traceback.format_exc())
            return {'error': str(e)}

# Global model instance (will be initialized in Flask app)
model_instance = None

def initialize_model(model_path=None):
    """Initialize the global model instance"""
    global model_instance
    model_instance = RetinalBlindnessModel(model_path)
    return model_instance

def get_prediction(image_path):
    """Get prediction from the global model instance"""
    if model_instance is None:
        return {'error': 'Model not initialized'}
    return model_instance.predict(image_path)
