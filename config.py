import os
import platform
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base application configuration."""
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Session settings
    SESSION_PERMANENT = True
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=45)

    # Caching configuration
    CACHE_DEFAULT_TIMEOUT = int(os.getenv('CACHE_DEFAULT_TIMEOUT', '300'))
    CACHE_KEY_PREFIX = 'qmis_'
    CACHE_THRESHOLD = 1000

    cache_type_env = (os.getenv('CACHE_TYPE') or '').strip()
    redis_url_env = os.getenv('REDIS_URL')

    if cache_type_env:
        CACHE_TYPE = cache_type_env
        if cache_type_env.lower() == 'rediscache' and redis_url_env:
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
