"""
Utility functions for input validation and sanitization.
"""

import re
from urllib.parse import urlparse


def validate_email(email):
    """
    Validate email format.
    
    Args:
        email: Email string to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not email or not isinstance(email, str):
        return False
    
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_username(username):
    """
    Validate username format.
    
    Args:
        username: Username string to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not username or not isinstance(username, str):
        return False
    
    # Username should be 3-50 characters, alphanumeric and underscores only
    if len(username) < 3 or len(username) > 50:
        return False
    
    pattern = r'^[a-zA-Z0-9_]+$'
    return re.match(pattern, username) is not None


def validate_password(password):
    """
    Validate password strength.
    
    Args:
        password: Password string to validate
        
    Returns:
        tuple: (bool, str) - (is_valid, error_message)
    """
    if not password or not isinstance(password, str):
        return False, "Password is required"
    
    if len(password) < 6:
        return False, "Password must be at least 6 characters"
    
    if len(password) > 128:
        return False, "Password is too long"
    
    return True, ""


def validate_url(url):
    """
    Validate URL format.
    
    Args:
        url: URL string to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not url or not isinstance(url, str):
        return False
    
    try:
        result = urlparse(url)
        return all([result.scheme in ['http', 'https'], result.netloc])
    except (ValueError, TypeError):
        return False


def sanitize_string(text, max_length=1000):
    """
    Sanitize string input by removing potentially harmful characters.
    
    Args:
        text: Text to sanitize
        max_length: Maximum allowed length
        
    Returns:
        str: Sanitized text
    """
    if not text:
        return ""
    
    if not isinstance(text, str):
        text = str(text)
    
    # Truncate to max length
    text = text[:max_length]
    
    # Remove null bytes
    text = text.replace('\x00', '')
    
    # Strip leading/trailing whitespace
    text = text.strip()
    
    return text


def validate_pagination_params(page, per_page, max_per_page=100):
    """
    Validate and sanitize pagination parameters.
    
    Args:
        page: Page number
        per_page: Items per page
        max_per_page: Maximum items per page allowed
        
    Returns:
        tuple: (page, per_page) - validated values
    """
    try:
        page = int(page) if page else 1
        per_page = int(per_page) if per_page else 20
    except (ValueError, TypeError):
        page = 1
        per_page = 20
    
    # Ensure positive values
    page = max(1, page)
    per_page = max(1, min(per_page, max_per_page))
    
    return page, per_page
