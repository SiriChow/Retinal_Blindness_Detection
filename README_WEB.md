# Retinal Blindness Detection - Web Application

This is a modern web-based version of the retinal blindness detection system, replacing the original Tkinter GUI with a responsive web interface built using Flask.

## Features

### 🎯 Core Functionality
- **AI-Powered Analysis**: Uses ResNet152 deep learning model for diabetic retinopathy detection
- **5-Class Classification**: No DR, Mild, Moderate, Severe, Proliferative DR
- **Real-time Predictions**: Upload images and get instant analysis results
- **Confidence Scoring**: Detailed probability breakdown for all classes

### 🌐 Web Interface
- **Modern Responsive Design**: Works on desktop, tablet, and mobile devices
- **Drag & Drop Upload**: Easy image upload with drag-and-drop functionality
- **User Authentication**: Secure login/signup system with SQLite database
- **Prediction History**: Track all your previous analyses
- **Interactive Results**: Visual representation of prediction confidence

### 🔒 Security & Privacy
- **Secure File Handling**: Files are processed and immediately deleted
- **User Sessions**: Secure session management
- **Input Validation**: Comprehensive file type and size validation
- **Database Security**: Hashed passwords and prepared statements

## Installation & Setup

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Quick Start

1. **Clone the repository** (if not already done):
   ```bash
   git clone https://github.com/souravs17031999/Retinal_blindness_detection_Pytorch
   cd Retinal_blindness_detection_Pytorch
   ```

2. **Install web dependencies**:
   ```bash
   pip install -r requirements_web.txt
   ```

3. **Run the web application**:
   ```bash
   python app.py
   ```

4. **Access the application**:
   Open your web browser and go to: `http://localhost:5000`

### With Pre-trained Model (Recommended)

To use the actual trained model for accurate predictions:

1. **Download the pre-trained model** (classifier.pt) - follow the original repository instructions
2. **Update the model path** in `app.py`:
   ```python
   model = initialize_model('path/to/your/classifier.pt')
   ```

## Usage Guide

### Getting Started
1. **Sign Up**: Create a new account with username and password
2. **Login**: Access your dashboard with your credentials
3. **Upload Image**: Drag and drop or browse for a retinal image
4. **Analyze**: Click "Analyze Image" to get AI predictions
5. **View Results**: See detailed classification and confidence scores
6. **History**: Check your prediction history anytime

### Supported Image Formats
- JPEG/JPG
- PNG
- GIF
- BMP
- TIFF
- Maximum file size: 16MB

### Understanding Results

The system classifies retinal images into 5 categories:

| Class | Severity | Description |
|-------|----------|-------------|
| **No DR** | ✅ Normal | No diabetic retinopathy detected |
| **Mild** | ⚠️ Low Risk | Early signs, monitor regularly |
| **Moderate** | ⚠️ Medium Risk | Moderate DR, requires attention |
| **Severe** | ❌ High Risk | Severe DR, needs medical care |
| **Proliferative DR** | ❌ Critical | Advanced DR, urgent treatment |

## Technical Architecture

### Backend
- **Framework**: Flask (Python web framework)
- **Model**: PyTorch ResNet152
- **Database**: SQLite (for user management and history)
- **Image Processing**: PIL/Pillow for image handling

### Frontend
- **UI Framework**: Bootstrap 5
- **Icons**: Font Awesome
- **JavaScript**: Vanilla JS with modern ES6+ features
- **Responsive Design**: Mobile-first approach

### File Structure
```
Retinal_blindness_detection_Pytorch/
├── app.py                 # Main Flask application
├── model_web.py          # Web-compatible model wrapper
├── requirements_web.txt  # Web application dependencies
├── templates/            # HTML templates
│   ├── base.html
│   ├── login.html
│   ├── signup.html
│   ├── dashboard.html
│   └── history.html
├── static/              # Static assets
│   ├── css/style.css
│   └── js/main.js
├── uploads/             # Temporary upload directory
└── users.db            # SQLite database (created on first run)
```

## Differences from Original

### Replaced Components
| Original | Web Version |
|----------|-------------|
| Tkinter GUI | Modern Web Interface |
| MySQL Database | SQLite Database |
| Local Desktop App | Web Application |
| Manual File Selection | Drag & Drop Upload |
| Basic Results Display | Interactive Results Modal |

### Enhanced Features
- **Responsive Design**: Works on all devices
- **Better UX**: Modern, intuitive interface
- **Cloud Ready**: Can be easily deployed to cloud platforms
- **Multi-user Support**: User accounts and session management
- **History Tracking**: Persistent prediction history
- **Real-time Feedback**: Loading states and progress indicators

## Deployment Options

### Local Development
```bash
python app.py
```
Access at: `http://localhost:5000`

### Production Deployment
For production deployment, consider:
- **Heroku**: Easy cloud deployment
- **AWS/GCP/Azure**: Scalable cloud hosting
- **Docker**: Containerized deployment
- **nginx + gunicorn**: Traditional web server setup

### Environment Variables (Production)
```bash
export FLASK_ENV=production
export SECRET_KEY=your-super-secure-secret-key
export DATABASE_URL=your-database-url
```

## Important Notes

### ⚠️ Medical Disclaimer
This system is designed for **educational and screening purposes only**. The AI predictions should **never replace professional medical diagnosis**. Always consult with qualified healthcare professionals for proper medical evaluation and treatment.

### 🔒 Privacy & Security
- User passwords are hashed using SHA-256
- Uploaded images are processed and immediately deleted
- Sessions are secure and expire appropriately
- No image data is permanently stored

### 🚀 Performance
- The ResNet152 model is computationally intensive
- Consider using GPU acceleration for better performance
- File uploads are limited to 16MB for reasonable processing times

## Troubleshooting

### Common Issues

1. **Module not found errors**:
   ```bash
   pip install -r requirements_web.txt
   ```

2. **Permission errors**:
   - Ensure the uploads directory is writable
   - Check file permissions on the project directory

3. **Model loading errors**:
   - Verify the model file path is correct
   - Ensure the model file is compatible with the PyTorch version

4. **Database errors**:
   - Delete `users.db` to reset the database
   - Check write permissions in the project directory

### Debug Mode
Enable debug mode for development:
```python
app.run(debug=True)
```

## Contributing

Feel free to contribute to this web version by:
- Reporting bugs
- Suggesting enhancements
- Submitting pull requests
- Improving documentation

## License

This project maintains the same license as the original repository.

---

**Original Repository**: [souravs17031999/Retinal_blindness_detection_Pytorch](https://github.com/souravs17031999/Retinal_blindness_detection_Pytorch)

**Web Version Features**: Modern UI, Multi-user support, Cloud-ready deployment
