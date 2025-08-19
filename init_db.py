import os
import psycopg2
from urllib.parse import urlparse

# Get database URL from environment
database_url = os.environ.get('DATABASE_URL')

# Fix for Heroku's postgres:// vs postgresql:// issue
if database_url and database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql://', 1)

if not database_url:
    print("No DATABASE_URL found. Using SQLite instead.")
    from app import init_db
    init_db()
    exit(0)

# Parse the URL
result = urlparse(database_url)
username = result.username
password = result.password
database = result.path[1:]
host = result.hostname
port = result.port

# Connect to the database
conn = psycopg2.connect(
    database=database,
    user=username,
    password=password,
    host=host,
    port=port
)

# Create tables
with conn.cursor() as cur:
    # Create users table
    cur.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Create predictions table
    cur.execute('''
    CREATE TABLE IF NOT EXISTS predictions (
        id SERIAL PRIMARY KEY,
        user_id INTEGER,
        filename TEXT,
        predicted_class TEXT,
        confidence REAL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    ''')
    
    conn.commit()
    print("Database tables created successfully.")

conn.close()