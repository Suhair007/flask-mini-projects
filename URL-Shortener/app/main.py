from flask import Flask, jsonify, request, redirect, abort
from app.models import URLStore
from app.utils import validate_url, sanitize_url
import threading

app = Flask(__name__)

# Global URL store instance
url_store = URLStore()

@app.route('/')
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "URL Shortener API"
    })

@app.route('/api/health')
def api_health():
    return jsonify({
        "status": "ok",
        "message": "URL Shortener API is running"
    })

@app.route('/api/shorten', methods=['POST'])
def shorten_url():
    """Shorten a URL endpoint"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Request body is required'}), 400
        
        original_url = data.get('url')
        if not original_url:
            return jsonify({'error': 'URL is required'}), 400
        
        # Validate URL
        is_valid, error_message = validate_url(original_url)
        if not is_valid:
            return jsonify({'error': error_message}), 400
        
        # Sanitize URL
        clean_url = sanitize_url(original_url)
        
        # Generate short code
        short_code = url_store.add_url(clean_url)
        
        return jsonify({
            'short_code': short_code,
            'short_url': f'http://localhost:5000/{short_code}',
            'original_url': clean_url
        }), 201
        
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/<short_code>')
def redirect_to_url(short_code):
    """Redirect to original URL"""
    original_url = url_store.get_url(short_code)
    
    if not original_url:
        abort(404)
    
    return redirect(original_url, code=302)

@app.route('/api/stats/<short_code>')
def get_stats(short_code):
    """Get analytics for a short code"""
    stats = url_store.get_stats(short_code)
    
    if not stats:
        return jsonify({'error': 'Short code not found'}), 404
    
    return jsonify({
        'url': stats['url'],
        'clicks': stats['clicks'],
        'created_at': stats['created_at']
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Resource not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)