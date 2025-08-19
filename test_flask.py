#!/usr/bin/env python3
"""
Simple Flask test to verify installation and basic functionality
"""
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return '''
    <h1>✅ Flask is Working!</h1>
    <p>Your web server is running successfully.</p>
    <p><a href="/test">Test another route</a></p>
    '''

@app.route('/test')
def test():
    return '<h2>🎉 All routes working!</h2><p><a href="/">Back to home</a></p>'

if __name__ == '__main__':
    print("🚀 Starting minimal Flask test server...")
    print("📍 Access at: http://localhost:8080")
    print("🛑 Press Ctrl+C to stop")
    app.run(debug=True, host='localhost', port=8080)
