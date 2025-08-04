# TODO: Implement your data models here
# Consider what data structures you'll need for:
# - Storing URL mappings
# - Tracking click counts
# - Managing URL metadata

# app/models.py
import threading
from datetime import datetime
from typing import Dict, Optional, Tuple

class URLStore:
    """In-memory storage for URL mappings with thread safety"""
    
    def __init__(self):
        self._urls: Dict[str, Dict] = {}
        self._lock = threading.Lock()
        self._counter = 0
    
    def add_url(self, original_url: str) -> str:
        """Add a new URL and return its short code"""
        from app.utils import generate_short_code
        
        with self._lock:
            # Generate a unique short code
            while True:
                short_code = generate_short_code()
                if short_code not in self._urls:
                    break
            
            # Store the URL mapping
            self._urls[short_code] = {
                'url': original_url,
                'clicks': 0,
                'created_at': datetime.utcnow().isoformat()
            }
            
            return short_code
    
    def get_url(self, short_code: str) -> Optional[str]:
        """Get original URL and increment click count"""
        with self._lock:
            if short_code in self._urls:
                self._urls[short_code]['clicks'] += 1
                return self._urls[short_code]['url']
            return None
    
    def get_stats(self, short_code: str) -> Optional[Dict]:
        """Get analytics for a short code"""
        with self._lock:
            if short_code in self._urls:
                return self._urls[short_code].copy()
            return None
    
    def url_exists(self, short_code: str) -> bool:
        """Check if a short code exists"""
        with self._lock:
            return short_code in self._urls