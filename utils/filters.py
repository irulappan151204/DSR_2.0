def json_escape(value):
    """Escape a value for safe inclusion in JSON strings inside templates."""
    if value is None:
        return ''
    value_str = str(value)
    escaped = value_str.replace('\\', '\\\\')  # Must be first
    escaped = escaped.replace('"', '\\"')
    escaped = escaped.replace('\n', '\\n')
    escaped = escaped.replace('\r', '\\r')
    escaped = escaped.replace('\t', '\\t')
    return escaped

def ist_strftime(date, format_string):
    """Format date in IST using format_string similar to strftime."""
    if date is None:
        return ''
    try:
        from zoneinfo import ZoneInfo
        if date.tzinfo is None:
            date = date.replace(tzinfo=ZoneInfo("Asia/Kolkata"))
        ist_date = date.astimezone(ZoneInfo("Asia/Kolkata"))
        return ist_date.strftime(format_string)
    except Exception:
        return str(date)

