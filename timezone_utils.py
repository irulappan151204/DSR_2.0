from datetime import datetime, timezone
from zoneinfo import ZoneInfo

# Re-usable timezone objects
IST_TZ = ZoneInfo("Asia/Kolkata")
UTC_TZ = timezone.utc

# ---------------------------------------------------------------------------
# Helpers for working with IST and keeping the DB in UTC
# ---------------------------------------------------------------------------

def now_ist() -> datetime:
    """Return current time in Asia/Kolkata (tz-aware)."""
    return datetime.now(IST_TZ)


def ist_day_bounds(date_obj):
    """Return naive datetime bounds (start, end) for the *IST* calendar
    day *date_obj*.

    We treat the values stored in the DB as naive **IST** datetimes because
    MySQL DATETIME drops timezone information.  The returned start/end are
    therefore naive as well so they can be compared directly to the column.
    """

    # 00:00 and 23:59:59.999999 of that date in IST (naive)
    start_naive = datetime.combine(date_obj, datetime.min.time())
    end_naive = datetime.combine(date_obj, datetime.max.time())
    return start_naive, end_naive


def build_ist_date_filter(model, column_name: str = "submitted_at", *,
                           start_date=None, end_date=None, single_date=None):
    """Return a list of SQLAlchemy filters to apply on *model.column_name* so
    that comparisons are done on IST calendar days while the actual column is
    stored as UTC values.

    • If *single_date* is given, we filter the UTC column between the UTC
      bounds of that IST date.
    • If *start_date* and *end_date* are given we build a between filter for
      the whole range inclusive.
    """
    column = getattr(model, column_name)
    filters = []
    if single_date is not None:
        s, e = ist_day_bounds(single_date)
        filters.append(column >= s)
        filters.append(column <= e)
    elif start_date is not None and end_date is not None:
        s_utc, _ = ist_day_bounds(start_date)
        _, e_utc = ist_day_bounds(end_date)
        filters.append(column >= s_utc)
        filters.append(column <= e_utc)
    return filters 