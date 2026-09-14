import os
import platform
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

import warnings

class Config:
    """Base application configuration."""
    _secret_key = os.getenv('SECRET_KEY')
    _insecure_defaults = ('dev-secret-key', 'qmisd-sr-final-2024-secret-key-123')
    _is_debug = os.getenv('FLASK_DEBUG', 'False').lower() in ('true', '1', 't')

    if not _secret_key or _secret_key in _insecure_defaults:
        if not _is_debug and os.getenv('FLASK_ENV') == 'production':
            raise ValueError(
                "CRITICAL SECURITY CONFIGURATION ERROR: SECRET_KEY environment variable is "
                "missing or using an insecure known default. In production, SECRET_KEY must be set "
                "to a cryptographically secure random value."
            )
        else:
            warnings.warn(
                "SECRET_KEY is unset or using an insecure fallback value. "
                "Please configure a strong SECRET_KEY in your .env file."
            )
            _secret_key = _secret_key or 'dev-secret-key'

    SECRET_KEY = _secret_key
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Session and Cookie Security settings
    SESSION_PERMANENT = True
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=int(os.getenv('SESSION_LIFETIME_MINUTES', '45')))
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = os.getenv('SESSION_COOKIE_SAMESITE', 'Lax')
    SESSION_COOKIE_SECURE = os.getenv('SESSION_COOKIE_SECURE', 'False').lower() in ('true', '1', 't')

    # File upload limit (default 64MB to prevent memory exhaustion DoS)
    MAX_CONTENT_LENGTH = int(os.getenv('MAX_CONTENT_LENGTH', str(64 * 1024 * 1024)))

    # Caching configuration
    CACHE_DEFAULT_TIMEOUT = int(os.getenv('CACHE_DEFAULT_TIMEOUT', '300'))
    CACHE_KEY_PREFIX = 'qmis_'
    CACHE_THRESHOLD = 1000

    cache_type_env = (os.getenv('CACHE_TYPE') or '').strip()
    redis_url_env = os.getenv('REDIS_URL')

    if cache_type_env:
        CACHE_TYPE = cache_type_env
        if cache_type_env.lower() in ('rediscache', 'redis') and redis_url_env:
            CACHE_REDIS_URL = redis_url_env
    else:
        is_windows = platform.system().lower().startswith('win')
        if is_windows:
            CACHE_TYPE = 'SimpleCache'
        elif redis_url_env:
            CACHE_TYPE = 'RedisCache'
            CACHE_REDIS_URL = redis_url_env
        else:
            CACHE_TYPE = 'SimpleCache'

