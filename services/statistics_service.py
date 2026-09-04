from datetime import datetime, timedelta
from repositories.statistics_repository import get_team_by_name
from services.statistics import (
    build_date_filter,
    apply_nature_filter,
    zero_out,
    calculate_kpi_totals,
    collect_available_dates,
    TEAM1_MODELS,
    populate_team1_issue_nature,
    TEAM2_MODELS,
    populate_team2_issue_nature,
    TEAM3_MODELS,
    populate_team3_issue_nature
)

def get_statistics_context(current_user, args):
    """Compile all statistics data, filters, KPI totals, and available dates

    for the statistics dashboard view.
    Returns None if user is not authorized (neither MD nor Team Lead).
    """
    is_md = (current_user.role == 'MD')
    is_team_lead = getattr(current_user, 'is_team_lead', False)
    if not (is_md or is_team_lead):
        return None

    # Get selected filters from query parameters
    has_date_param = 'date' in args
    has_start_param = 'start_date' in args
    has_end_param = 'end_date' in args

    selected_date = args.get('date', None)
    start_date_str = args.get('start_date', '')
    end_date_str = args.get('end_date', '')
    selected_nature = (args.get('nature', 'all') or 'all').strip().lower()

    selected_date_obj = None
    start_date = None
    end_date = None
    defaulted_to_yesterday = False

    # Default logic: if no query params provided at all -> default yesterday
    if not has_date_param and not has_start_param and not has_end_param:
        yesterday = (datetime.now() - timedelta(days=1)).date()
        selected_date = yesterday.strftime('%Y-%m-%d')
        defaulted_to_yesterday = True
    else:
        # Respect explicit input; if empty date and no range, treat as 'all'
        if (selected_date is None or str(selected_date).strip() == '') and not (start_date_str and end_date_str):
            selected_date = 'all'
        # If using date range, clear selected_date to avoid conflicts
        elif start_date_str and end_date_str:
            selected_date = None

    if start_date_str and end_date_str:
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        except ValueError:
            start_date = None
            end_date = None

    if selected_date and selected_date != 'all':
        try:
            selected_date_obj = datetime.strptime(selected_date, '%Y-%m-%d').date()
        except ValueError:
            selected_date = 'all'

    def date_filter_fn(model):
        return build_date_filter(
            model,
            start_date=start_date,
            end_date=end_date,
            selected_date=selected_date,
            selected_date_obj=selected_date_obj
        )

    # Fetch teams
    team1 = get_team_by_name('Team 1')
    team2 = get_team_by_name('Team 2')
    team3 = get_team_by_name('Team 3')

    # Populate statistics per team
    team1_issue_nature = populate_team1_issue_nature(team1, date_filter_fn)
    team2_issue_nature = populate_team2_issue_nature(team2, date_filter_fn)
    team3_issue_nature = populate_team3_issue_nature(team3, date_filter_fn)

    # Collect available distinct dates based on user role
    available_dates = collect_available_dates(
        is_team_lead,
        is_md,
        current_user,
        TEAM1_MODELS,
        TEAM2_MODELS,
        TEAM3_MODELS
    )

    # Build KPI totals BEFORE applying nature filter so the KPI can show all three counts
    kpi_totals = calculate_kpi_totals(team1_issue_nature, team2_issue_nature, team3_issue_nature)

    # Apply nature filter to datasets used for charts/tables
    team1_issue_nature = apply_nature_filter(team1_issue_nature, selected_nature)
    team2_issue_nature = apply_nature_filter(team2_issue_nature, selected_nature)
    team3_issue_nature = apply_nature_filter(team3_issue_nature, selected_nature)

    # If Team Lead, hide other teams by zeroing out their stats
    if is_team_lead and not is_md:
        if current_user.team_id == 1:
            team2_issue_nature = zero_out(team2_issue_nature)
            team3_issue_nature = zero_out(team3_issue_nature)
        elif current_user.team_id == 2:
            team1_issue_nature = zero_out(team1_issue_nature)
            team3_issue_nature = zero_out(team3_issue_nature)
        elif current_user.team_id == 3:
            team1_issue_nature = zero_out(team1_issue_nature)
            team2_issue_nature = zero_out(team2_issue_nature)

    return {
        'team1_issue_nature': team1_issue_nature,
        'team2_issue_nature': team2_issue_nature,
        'team3_issue_nature': team3_issue_nature,
        'selected_date': selected_date,
        'selected_nature': selected_nature,
        'start_date': start_date_str,
        'end_date': end_date_str,
        'available_dates': available_dates,
        'defaulted_to_yesterday': defaulted_to_yesterday,
        'is_md': is_md,
        'is_team_lead': is_team_lead,
        'kpi_totals': kpi_totals
    }
