from flask import Flask, jsonify
from datetime import datetime
import os

app = Flask(__name__)

@app.route('/')
def home():
    """Welcome endpoint"""
    return jsonify({
        'message': 'Welcome to the ColorStack Teaching Demo!',
        'endpoints': {
            '/': 'This welcome message',
            '/api/health': 'Health check endpoint',
            '/api/time': 'Get current server time'
        }
    })

@app.route('/api/health')
def health():
    """Health check endpoint for container orchestration"""
    return jsonify({
        'status': 'healthy',
        'service': 'web-service',
        'version': '1.0.0'
    })

@app.route('/api/time')
def get_time():
    """Returns current server time"""
    return jsonify({
        'server_time': datetime.now().isoformat(),
        'timezone': 'UTC',
        'timestamp': datetime.now().timestamp()
    })

if __name__ == '__main__':
    # Get port from environment variable or default to 5000
    port = int(os.getenv('PORT', 5000))
    # Run the app
    app.run(host='0.0.0.0', port=port, debug=True)
