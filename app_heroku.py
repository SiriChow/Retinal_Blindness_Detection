from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os
import uuid
from model_web import initialize_model, get_prediction
import hashlib
from datetime import datetime
import psycopg2
from urllib.parse import urlparse

# Import Heroku configuration
from heroku_config import (
    DATABASE_URL, SECRET_KEY, PORT, DEBUG, UPLOAD_FOLDER
)

app = Flask(__name__)
app.secret_key = SECRET_KEY

# Configuration
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

# Database connection helper
def get_db_connection():
    if DATABASE_URL.startswith('sqlite'):
        import sqlite3
        conn = sqlite3.connect('users.db')
        conn.row_factory = sqlite3.Row
        return conn
    else:
        # Parse the URL for PostgreSQL
        result = urlparse(DATABASE_URL)
        username = result.username
        password = result.password
        database = result.path[1:]
        host = result.hostname
        port = result.port
        
        # Connect to PostgreSQL
        conn = psycopg2.connect(
            database=database,
            user=username,
            password=password,
            host=host,
            port=port
        )
        return conn

# Initialize database
def init_db(db_url=None):
    if not db_url or db_url.startswith('sqlite'):
        # SQLite initialization
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS users
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
        
        c.execute('''CREATE TABLE IF NOT EXISTS predictions
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    filename TEXT,
                    predicted_class TEXT,
                    confidence REAL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id))''')
        conn.commit()
        conn.close()
    else:
        # PostgreSQL initialization is handled by init_db.py
        pass

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Initialize the database
init_db(DATABASE_URL)

# Initialize the model
initialize_model()

@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if using SQLite or PostgreSQL
        if DATABASE_URL.startswith('sqlite'):
            cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
            user = cursor.fetchone()
        else:
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            user = cursor.fetchone()
        
        conn.close()
        
        if user and user[2] == hash_password(password):  # Check password hash
            session['user_id'] = user[0]
            session['username'] = user[1]
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Hash the password
        password_hash = hash_password(password)
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            # Check if using SQLite or PostgreSQL
            if DATABASE_URL.startswith('sqlite'):
                cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", 
                            (username, password_hash))
            else:
                cursor.execute("INSERT INTO users (username, password_hash) VALUES (%s, %s)", 
                            (username, password_hash))
            
            conn.commit()
            flash('Account created successfully! Please log in.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            conn.rollback()
            flash(f'Error creating account: {str(e)}', 'error')
        finally:
            conn.close()
    
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/predict', methods=['POST'])
def predict():
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        # Secure the filename and generate a unique name
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4()}_{filename}"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        
        # Save the file
        file.save(file_path)
        
        try:
            # Get prediction
            result = get_prediction(file_path)
            
            # Save prediction to database
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Check if using SQLite or PostgreSQL
            if DATABASE_URL.startswith('sqlite'):
                cursor.execute(
                    "INSERT INTO predictions (user_id, filename, predicted_class, confidence) VALUES (?, ?, ?, ?)",
                    (session['user_id'], unique_filename, result['class'], result['confidence'])
                )
            else:
                cursor.execute(
                    "INSERT INTO predictions (user_id, filename, predicted_class, confidence) VALUES (%s, %s, %s, %s)",
                    (session['user_id'], unique_filename, result['class'], result['confidence'])
                )
            
            conn.commit()
            conn.close()
            
            return jsonify(result), 200
            
        except Exception as e:
            # Clean up the file in case of error
            if os.path.exists(file_path):
                os.remove(file_path)
            return jsonify({'error': str(e)}), 500
    
    return jsonify({'error': 'File type not allowed'}), 400

@app.route('/history')
def history():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if using SQLite or PostgreSQL
    if DATABASE_URL.startswith('sqlite'):
        cursor.execute(
            "SELECT * FROM predictions WHERE user_id = ? ORDER BY created_at DESC",
            (session['user_id'],)
        )
    else:
        cursor.execute(
            "SELECT * FROM predictions WHERE user_id = %s ORDER BY created_at DESC",
            (session['user_id'],)
        )
    
    predictions = cursor.fetchall()
    conn.close()
    
    return render_template('history.html', predictions=predictions)

if __name__ == '__main__':
    app.run(debug=DEBUG, host='0.0.0.0', port=PORT)