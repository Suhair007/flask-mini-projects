# TODO: Implement utility functions here
# Consider functions for:
# - Generating short codes
# - Validating URLs
# - Any other helper functions you need

import re
import random
import string
from urllib.parse import urlparse
from typing import Tuple

def generate_short_code() -> str:
    """Generate a random 6-character alphanumeric code"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

def validate_url(url: str) -> Tuple[bool, str]:
    """Validate if a URL is properly formatted"""
    if not url:
        return False, "URL cannot be empty"
    
    if not isinstance(url, str):
        return False, "URL must be a string"
    
    # Basic URL validation
    try:
        result = urlparse(url)
        if not all([result.scheme, result.netloc]):
            return False, "URL must have a valid scheme and domain"
        
        # Check for common schemes
        if result.scheme not in ['http', 'https']:
            return False, "URL must use http or https scheme"
        
        # Check for valid domain
        if len(result.netloc) < 3:
            return False, "URL must have a valid domain"
        
        return True, "URL is valid"
        
    except Exception:
        return False, "Invalid URL format"

def sanitize_url(url: str) -> str:
    """Clean and normalize URL"""
    url = url.strip()
    
    # Add scheme if missing
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    return url


