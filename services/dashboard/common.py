# services/dashboard/common.py
from models import Team

def get_authorized_dashboard_teams(user):
    """
    Returns the list of authorized teams for dashboard viewing based on user role.

    Rules:
    - MD: All teams in database (+ All Teams view).
    - Audit Team Lead (or Admin, team_id == 3): All teams in database.
    - Other Team Leads (e.g., Academics Lead, Admin Lead):
      Only:
      1. Their own team's submissions/forms
      2. Audit team's submissions/forms
      (Other teams are excluded).
    """
    all_db_teams = Team.query.order_by(Team.team_id).all()

    display_names = {
        'Team 1': 'Academics',
        'Team 2': 'Admin',
        'Team 3': 'Audit',
    }

    def format_team(t):
        return {
            'key': f'team{t.team_id}',
            'name': display_names.get(t.team_name, t.team_name),
            'team_id': t.team_id,
            'team_name': t.team_name,
        }

    # MD has access to all teams
    if user.role == 'MD':
        return [format_team(t) for t in all_db_teams]

    # Audit team lead / admin has access to all teams
    if user.team_id == 3 or user.role == 'Admin':
        return [format_team(t) for t in all_db_teams]

    # Standard Team Lead (Academics, Admin, etc.):
    # Allowed: 1. Their own team; 2. Audit team (team_id == 3)
    allowed = []
    for t in all_db_teams:
        if t.team_id == user.team_id or t.team_id == 3:
            allowed.append(format_team(t))

    # Sort so the user's own team appears first, then Audit
    allowed.sort(key=lambda x: (x['team_id'] != user.team_id, x['team_id']))
    return allowed
