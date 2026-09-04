from timezone_utils import ist_day_bounds
from repositories.statistics_repository import get_distinct_dates_for_model

def build_date_filter(model, start_date=None, end_date=None, selected_date=None, selected_date_obj=None):
    """Return SQLAlchemy filters that respect IST calendar day(s) while
    the DB stores UTC values."""
    filters = []
    if start_date and end_date:
        s_utc, _ = ist_day_bounds(start_date)
        _, e_utc = ist_day_bounds(end_date)
        filters.append(model.submitted_at >= s_utc)
        filters.append(model.submitted_at <= e_utc)
    elif selected_date and selected_date != 'all' and selected_date_obj:
        s_utc, e_utc = ist_day_bounds(selected_date_obj)
        filters.append(model.submitted_at >= s_utc)
        filters.append(model.submitted_at <= e_utc)
    return filters

def record_nature(stats_dict, key, nature_val):
    """Increment status counts for a specific section and overall total."""
    if not nature_val:
        return
    nature = str(nature_val).lower()
    if ('all_well' in nature or 'all well' in nature):
        stats_dict[key]['all_well'] += 1
        stats_dict['overall']['all_well'] += 1
    elif ('manageable' in nature):
        stats_dict[key]['manageable'] += 1
        stats_dict['overall']['manageable'] += 1
    elif ('critical' in nature):
        stats_dict[key]['critical'] += 1
        stats_dict['overall']['critical'] += 1

def apply_nature_filter(stats_dict, selected_nature):
    """Zero-out non-selected natures if nature filter is applied."""
    if selected_nature == 'all':
        return stats_dict
    allowed = {'all_well', 'manageable', 'critical'}
    for section_key, counts in stats_dict.items():
        if isinstance(counts, dict):
            for label in list(allowed):
                if label != selected_nature and label in counts:
                    counts[label] = 0
    return stats_dict

def zero_out(stats_dict):
    """Zero-out all numeric values in a team statistics dictionary."""
    for section_key, counts in stats_dict.items():
        if isinstance(counts, dict):
            for k in counts.keys():
                if isinstance(counts[k], (int, float)):
                    counts[k] = 0
    return stats_dict

def calculate_kpi_totals(team1_issue_nature, team2_issue_nature, team3_issue_nature):
    """Build KPI totals BEFORE applying nature filter so the KPI can show all three counts."""
    kpi_totals = {
        'team1': {
            'all_well': team1_issue_nature['overall']['all_well'],
            'manageable': team1_issue_nature['overall']['manageable'],
            'critical': team1_issue_nature['overall']['critical'],
        },
        'team2': {
            'all_well': team2_issue_nature['overall']['all_well'],
            'manageable': team2_issue_nature['overall']['manageable'],
            'critical': team2_issue_nature['overall']['critical'],
        },
        'team3': {
            'all_well': team3_issue_nature['overall']['all_well'],
            'manageable': team3_issue_nature['overall']['manageable'],
            'critical': team3_issue_nature['overall']['critical'],
        }
    }
    kpi_totals['combined'] = {
        'all_well': kpi_totals['team1']['all_well'] + kpi_totals['team2']['all_well'] + kpi_totals['team3']['all_well'],
        'manageable': kpi_totals['team1']['manageable'] + kpi_totals['team2']['manageable'] + kpi_totals['team3']['manageable'],
        'critical': kpi_totals['team1']['critical'] + kpi_totals['team2']['critical'] + kpi_totals['team3']['critical'],
    }
    return kpi_totals

def collect_available_dates(is_team_lead, is_md, current_user, team1_models, team2_models, team3_models):
    """Collect and return sorted distinct available dates based on user role."""
    available_dates = set()

    def add_dates(model, team_id):
        dates = get_distinct_dates_for_model(model, team_id)
        for d in dates:
            available_dates.add(d)

    if is_team_lead and not is_md:
        if current_user.team_id == 1:
            for model in team1_models:
                add_dates(model, 1)
        elif current_user.team_id == 2:
            for model in team2_models:
                add_dates(model, 2)
        elif current_user.team_id == 3:
            for model in team3_models:
                add_dates(model, 3)
    else:
        # MD: include all teams
        for model in team1_models:
            add_dates(model, 1)
        for model in team2_models:
            add_dates(model, 2)
        for model in team3_models:
            add_dates(model, 3)

    return sorted(available_dates, reverse=True)
