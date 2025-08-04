import pytest
import json
from app.main import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_check(client):
    """Test health check endpoint"""
    response = client.get('/')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'
    assert data['service'] == 'URL Shortener API'

def test_shorten_url_success(client):
    """Test successful URL shortening"""
    response = client.post('/api/shorten', 
                          json={'url': 'https://www.google.com'})
    assert response.status_code == 201
    data = response.get_json()
    assert 'short_code' in data
    assert 'short_url' in data
    assert 'original_url' in data
    assert len(data['short_code']) == 6
    assert data['original_url'] == 'https://www.google.com'

def test_shorten_url_missing_url(client):
    """Test shortening with missing URL"""
    response = client.post('/api/shorten', json={})
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data

def test_shorten_url_invalid_url(client):
    """Test shortening with invalid URL"""
    response = client.post('/api/shorten', 
                          json={'url': 'not-a-url'})
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data

def test_redirect_success(client):
    """Test successful redirect"""
    # First create a short URL
    shorten_response = client.post('/api/shorten', 
                                  json={'url': 'https://www.example.com'})
    short_code = shorten_response.get_json()['short_code']
    
    # Then test redirect
    response = client.get(f'/{short_code}')
    assert response.status_code == 302
    assert response.location == 'https://www.example.com'

def test_redirect_not_found(client):
    """Test redirect with non-existent short code"""
    response = client.get('/nonexistent')
    assert response.status_code == 404

def test_stats_success(client):
    """Test getting stats for a short code"""
    # First create a short URL
    shorten_response = client.post('/api/shorten', 
                                  json={'url': 'https://www.test.com'})
    short_code = shorten_response.get_json()['short_code']
    
    # Access the URL to increment clicks
    client.get(f'/{short_code}')
    client.get(f'/{short_code}')
    
    # Get stats
    response = client.get(f'/api/stats/{short_code}')
    assert response.status_code == 200
    data = response.get_json()
    assert data['url'] == 'https://www.test.com'
    assert data['clicks'] == 2
    assert 'created_at' in data

def test_stats_not_found(client):
    """Test getting stats for non-existent short code"""
    response = client.get('/api/stats/nonexistent')
    assert response.status_code == 404