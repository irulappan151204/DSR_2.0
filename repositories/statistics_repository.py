from sqlalchemy import func
from extensions import db
from models import Team

def get_team_by_name(team_name):
    """Retrieve team by its name."""
    return Team.query.filter_by(team_name=team_name).first()

def get_model_records(model, team_id, date_filters=None):
    """Query all records for a model matching team_id and optional date_filters."""
    filters = [model.team_id == team_id]
    if date_filters:
        filters.extend(date_filters)
    return model.query.filter(*filters).all()

def get_distinct_dates_for_model(model, team_id):
    """Retrieve all distinct dates (YYYY-MM-DD) for a given model and team."""
    rows = db.session.query(
        func.date(model.submitted_at)
    ).filter(
        model.team_id == team_id
    ).distinct().all()
    return [row[0] for row in rows if row[0] is not None]
