#!/usr/bin/env python3
"""
Startup script for the Retinal Blindness Detection Web Application
"""
import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from app import app
    
    print("=" * 60)
    print("🚀 RETINAL BLINDNESS DETECTION WEB APPLICATION")
    print("=" * 60)
    print("✅ Flask application loaded successfully")
    print("✅ Model initialized (using untrained weights for demo)")
    print("✅ Database will be created on first run")
    print()
    print("📋 FEATURES:")
    print("   • User authentication (signup/login)")
    print("   • Image upload with drag & drop")
    print("   • AI-powered diabetic retinopathy detection")
    print("   • Prediction history tracking")
    print("   • Responsive web interface")
    print()
    print("🌐 ACCESS:")
    print("   Local:   http://localhost:8081")
    print("   Network: http://0.0.0.0:8081")
    print()
    print("⚠️  NOTE: This demo uses an untrained model.")
    print("   For real predictions, place 'classifier.pt' in the project directory")
    print("   and update the model path in app.py")
    print()
    print("🛑 To stop the server: Press Ctrl+C")
    print("=" * 60)
    print()
    
    # Start the Flask development server
    app.run(debug=True, host='0.0.0.0', port=8081)

except ImportError as e:
    print(f"❌ Error importing required modules: {e}")
    print("\n📦 Please install required dependencies:")
    print("   pip install Flask Pillow torch torchvision")
    sys.exit(1)
    
except Exception as e:
    print(f"❌ Error starting application: {e}")
    sys.exit(1)
