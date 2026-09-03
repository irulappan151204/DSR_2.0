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
