from datetime import datetime, timedelta
from repositories.history_repository import fetch_history_records

def get_user_history_rows(user_id, start=None, end=None, form_query=None):
    """Parse filters, fetch historical records, and construct template rows."""
    start_dt = None
    end_dt = None
    try:
        if start:
            start_dt = datetime.strptime(start, '%Y-%m-%d')
        if end:
            # inclusive end of day
            end_dt = datetime.strptime(end, '%Y-%m-%d') + timedelta(days=1)
    except Exception:
        start_dt = None
        end_dt = None

    history_rows = []
    results_by_model = fetch_history_records(user_id, start_dt, end_dt, form_query)

    for model_name, records in results_by_model:
        for r in records:
            form_data = {}
            for field_name in dir(r):
                if not field_name.startswith('_') and field_name not in [
                    'form_id', 'team_id', 'submitted_by', 'submitted_at',
                    'metadata', 'query', 'query_class'
                ]:
                    try:
                        value = getattr(r, field_name)
                        if value is not None and value != '':
                            form_data[field_name] = str(value)
                    except Exception:
                        pass

            history_rows.append({
                'form_name': model_name,
                'submitted_at': r.submitted_at,
                'team_id': r.team_id,
                'form_id': r.form_id,
                'form_data': form_data
            })

    # Sort overall by submitted_at desc
    history_rows.sort(key=lambda x: x['submitted_at'], reverse=True)
    return history_rows
