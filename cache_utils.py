from flask import request
from flask_login import current_user


def per_user_cache_key():
    """Build a cache key scoped per user and request URL.

    Safe to import in blueprints without causing circular imports.
    """
    try:
        user_part = f"user:{current_user.user_id}" if current_user.is_authenticated else "anon"
    except Exception:
        user_part = "anon"
    return f"{user_part}|path:{request.path}|qs:{request.query_string.decode()}"


def bust_user_dashboard_cache(user_id):
    """Drop all cached dashboard and history views for a given user_id."""
    from extensions import cache
    try:
        backend = getattr(cache, 'cache', None)
        internal_cache = getattr(backend, '_cache', None)
        if isinstance(internal_cache, dict):
            prefix = f"user:{user_id}|"
            keys_to_del = [k for k in internal_cache.keys() if prefix in k]
            for k in keys_to_del:
                internal_cache.pop(k, None)
    except Exception:
        pass

    # Explicit deletes for any cache backend (Redis, Memcached, etc.)
    paths = ['/dashboard', '/lead/dashboard', '/md/dashboard', '/my_history']
    query_strings = ['', 'team=team1', 'team=team2', 'team=team3', 'team=all', 'team=all&date=', 'team=team1&date=', 'team=team2&date=', 'team=team3&date=']
    for p in paths:
        for qs in query_strings:
            try:
                cache.delete(f"user:{user_id}|path:{p}|qs:{qs}")
            except Exception:
                pass




