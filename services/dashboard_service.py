from datetime import datetime
from extensions import db
from models import Team, User, Issue, Acknowledgement
from .dashboard.common import get_authorized_dashboard_teams
from .dashboard.team1_dashboard import get_team1_data, get_empty_team1_data
from .dashboard.team2_dashboard import get_team2_data, get_empty_team2_data
from .dashboard.team3_dashboard import get_team3_data

def build_dashboard_context(current_user, selected_team_arg, selected_date_arg):
    """Orchestrates all dashboard calculations based on authorized team and date."""
    authorized_teams = get_authorized_dashboard_teams(current_user)
    authorized_keys = {t['key'] for t in authorized_teams}
    if current_user.role == 'MD':
        authorized_keys.add('all')

    if current_user.role == 'MD':
        default_team = 'all'
    elif current_user.team_id:
        default_team = f'team{current_user.team_id}'
    else:
        default_team = authorized_teams[0]['key'] if authorized_teams else 'team1'

    selected_team = selected_team_arg
    if not selected_team or selected_team not in authorized_keys:
        selected_team = default_team

    today_date = datetime.now().strftime('%Y-%m-%d')
    selected_date = selected_date_arg or today_date
    show_all_dates = (selected_date == 'all')

    if not show_all_dates:
        try:
            selected_date_obj = datetime.strptime(selected_date, '%Y-%m-%d').date()
        except ValueError:
            selected_date = today_date
            selected_date_obj = datetime.strptime(today_date, '%Y-%m-%d').date()

        start_of_day = datetime.combine(selected_date_obj, datetime.min.time())
        end_of_day = datetime.combine(selected_date_obj, datetime.max.time())
    else:
        selected_date_obj = None
        start_of_day = None
        end_of_day = None

    if current_user.role == 'MD':
        teams = Team.query.all()
        users = User.query.all()
        issue_query = Issue.query
    else:
        teams = [Team.query.get(current_user.team_id)]
        users = User.query.filter_by(team_id=current_user.team_id).all()
        issue_query = Issue.query.filter_by(team_id=current_user.team_id)

    all_issues = issue_query.all()
    total_issues = len(all_issues)
    resolved_issues = len([i for i in all_issues if i.status == 'Solved'])
    pending_issues = len([i for i in all_issues if i.status == 'Pending'])
    open_issues = len([i for i in all_issues if i.status == 'Open'])
    recent_issues = issue_query.order_by(Issue.created_at.desc()).limit(10).all()

    # Base context
    context = {
        'users': users,
        'teams': teams,
        'selected_team': selected_team,
        'authorized_teams': authorized_teams,
        'selected_date': selected_date,
        'today_date': today_date,
        'show_all_dates': show_all_dates,
        'total_issues': total_issues,
        'resolved_issues': resolved_issues,
        'pending_issues': pending_issues,
        'open_issues': open_issues,
        'recent_issues': recent_issues,
        'unack_count': 0,
        'available_dates': []
    }

    # Populate Team 1 data
    if selected_team in ['all', 'team1']:
        context.update(get_team1_data(selected_date_obj, start_of_day, end_of_day, show_all_dates))
    else:
        context.update(get_empty_team1_data())

    # Populate Team 2 data
    if selected_team in ['all', 'team2']:
        context.update(get_team2_data(selected_date_obj, start_of_day, end_of_day, show_all_dates))
    else:
        context.update(get_empty_team2_data())

    # Populate Team 3 data
    if selected_team in ['all', 'team3']:
        t3_data = get_team3_data(selected_date_obj, start_of_day, end_of_day, show_all_dates, current_user)
        context.update(t3_data)
    else:
        context['team3_audit_data'] = []
        context['team3_new_audit_data'] = []

    return context
