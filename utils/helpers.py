from datetime import datetime

def safe_int(value):
    """Safely cast value to int or return None."""
    try:
        return int(value) if value and str(value).strip() else None
    except (ValueError, TypeError):
        return None

def safe_float(value):
    """Safely cast value to float or return None."""
    try:
        return float(value) if value and str(value).strip() else None
    except (ValueError, TypeError):
        return None

def safe_date(value):
    """Safely parse YYYY-MM-DD date or return None."""
    try:
        return datetime.strptime(value, '%Y-%m-%d').date() if value and str(value).strip() else None
    except (ValueError, TypeError):
        return None

def safe_time(value):
    """Safely parse HH:MM or HH:MM:SS time or return None."""
    try:
        return datetime.strptime(value, '%H:%M').time() if value and str(value).strip() else None
    except (ValueError, TypeError):
        try:
            return datetime.strptime(value, '%H:%M:%S').time() if value and str(value).strip() else None
        except (ValueError, TypeError):
            return None
