from extensions import db
from models import Team

def ensure_default_teams():
    """Ensure that default teams (Team 1, Team 2, Team 3) exist in the database."""
    team1 = Team.query.filter_by(team_name='Team 1').first()
    if not team1:
        team1 = Team(team_name='Team 1')
        db.session.add(team1)

    team2 = Team.query.filter_by(team_name='Team 2').first()
    if not team2:
        team2 = Team(team_name='Team 2')
        db.session.add(team2)

    team3 = Team.query.filter_by(team_name='Team 3').first()
    if not team3:
        team3 = Team(team_name='Team 3')
        db.session.add(team3)

    db.session.commit()

def get_all_teams():
    """Retrieve all teams."""
    return Team.query.all()

def get_team_by_id(team_id):
    """Retrieve a team by its ID."""
    return Team.query.get(team_id)

def get_team_by_name(team_name):
    """Retrieve a team by its name."""
    return Team.query.filter_by(team_name=team_name).first()
