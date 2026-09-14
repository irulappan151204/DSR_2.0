from flask import request, has_request_context
from flask_login import current_user


def _get_user_cache_part():
    """Extract a safe identifier string for current_user."""
    if not has_request_context():
        return "system"
    try:
        if current_user and current_user.is_authenticated:
            return f"user:{current_user.user_id}"
        return "anon"
    except Exception:
        return "anon"


def _normalize_query_string():
    """Normalize query parameters sorted alphabetically for deterministic cache keys."""
    if not has_request_context() or not request.args:
        return ''
    # Sort parameters so ?a=1&b=2 and ?b=2&a=1 yield identical keys
    sorted_items = sorted(request.args.items(multi=True))
    return '&'.join(f"{k}={v}" for k, v in sorted_items)


def per_user_cache_key():
    """Build a deterministic cache key scoped per user, role, and normalized request URL.

    Safe to import in blueprints without causing circular imports.
    """
    if not has_request_context():
        return "system:default"
    user_part = _get_user_cache_part()
    normalized_qs = _normalize_query_string()
    return f"{user_part}|path:{request.path}|qs:{normalized_qs}"


def _build_section_key(section_key=None):
    """Internal helper to construct a section cache key string from request context."""
    if not has_request_context():
        return f"section:{section_key or 'unknown'}"

    user_part = _get_user_cache_part()

    sec = section_key
    if not sec and request.view_args:
        sec = request.view_args.get('section_key') or request.view_args.get('section')
    if not sec:
        sec = request.args.get('section') or request.args.get('section_key') or 'general'

    team = ''
    if request.view_args:
        team = request.view_args.get('team_key') or request.view_args.get('team') or ''
    if not team:
        team = request.args.get('team', '')

    date_val = request.args.get('date', '')
    normalized_qs = _normalize_query_string()

    return f"section:{sec}|team:{team}|date:{date_val}|{user_part}|path:{request.path}|qs:{normalized_qs}"


def per_section_cache_key(section_key=None):
    """Build a cache key for section-level API requests.

    Can be used:
    1. Directly as a key_prefix callable: @cache.cached(key_prefix=per_section_cache_key)
    2. As a factory with explicit section name: @cache.cached(key_prefix=per_section_cache_key('calendar'))
    3. Directly to generate a key string within an active request context.
    """
    if callable(section_key):
        return _build_section_key(None)
    if isinstance(section_key, str) and not has_request_context():
        def _generator():
            return _build_section_key(section_key)
        return _generator
    return _build_section_key(section_key)


def bust_user_dashboard_cache(user_id=None):
    """Drop all cached dashboard, history, and section views for a given user_id (or all users if user_id is None)."""
    from extensions import cache
    try:
        backend = getattr(cache, 'cache', None)
        internal_cache = getattr(backend, '_cache', None)
        if isinstance(internal_cache, dict):
            if user_id is not None:
                user_marker = f"user:{user_id}"
                keys_to_del = [k for k in list(internal_cache.keys()) if user_marker in k]
            else:
                dashboard_markers = ('/dashboard', '/lead/dashboard', '/md/dashboard', '/my_history', 'section:')
                keys_to_del = [k for k in list(internal_cache.keys()) if any(m in k for m in dashboard_markers)]
            for k in keys_to_del:
                internal_cache.pop(k, None)
    except Exception:
        pass

    # Redis scan and delete if Redis client is available
    try:
        backend = getattr(cache, 'cache', None)
        client = getattr(backend, '_client', None) or getattr(backend, '_write_client', None)
        if client and hasattr(client, 'scan_iter') and hasattr(client, 'delete'):
            pattern = f"*user:{user_id}*" if user_id is not None else "*path:*dashboard*"
            keys = [k for k in client.scan_iter(match=pattern, count=100)]
            if keys:
                client.delete(*keys)
    except Exception:
        pass

    # Explicit deletes for any cache backend (fallback)
    if user_id is not None:
        paths = ['/dashboard', '/lead/dashboard', '/md/dashboard', '/my_history']
        query_strings = [
            '',
            'team=team1', 'team=team2', 'team=team3', 'team=all',
            'team=all&date=', 'team=team1&date=', 'team=team2&date=', 'team=team3&date='
        ]
        for p in paths:
            for qs in query_strings:
                try:
                    cache.delete(f"user:{user_id}|path:{p}|qs:{qs}")
                except Exception:
                    pass


def bust_section_cache(section_key=None, team=None, date_str=None, user_id=None):
    """Bust cached entries for a specific dashboard section or group of sections."""
    from extensions import cache
    try:
        backend = getattr(cache, 'cache', None)
        internal_cache = getattr(backend, '_cache', None)
        if isinstance(internal_cache, dict):
            keys_to_del = []
            for k in list(internal_cache.keys()):
                if 'section:' not in k:
                    continue
                if section_key and f"section:{section_key}" not in k:
                    continue
                if team and f"team:{team}" not in k:
                    continue
                if date_str and f"date:{date_str}" not in k:
                    continue
                if user_id and f"user:{user_id}" not in k:
                    continue
                keys_to_del.append(k)
            for k in keys_to_del:
                internal_cache.pop(k, None)
    except Exception:
        pass

    # Redis scan and delete if Redis client is available
    try:
        backend = getattr(cache, 'cache', None)
        client = getattr(backend, '_client', None) or getattr(backend, '_write_client', None)
        if client and hasattr(client, 'scan_iter') and hasattr(client, 'delete'):
            pat_parts = ["*section:"]
            pat_parts.append(f"*{section_key}*" if section_key else "*")
            if team:
                pat_parts.append(f"*team:{team}*")
            if user_id:
                pat_parts.append(f"*user:{user_id}*")
            pattern = ''.join(pat_parts)
            keys = [k for k in client.scan_iter(match=pattern, count=100)]
            if keys:
                client.delete(*keys)
    except Exception:
        pass


def bust_all_dashboard_caches():
    """Drop all dashboard and section cache keys across all users."""
    bust_user_dashboard_cache(user_id=None)
    bust_section_cache()
