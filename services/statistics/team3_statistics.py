from models import Team3Audit, Team3NewAudit

TEAM3_MODELS = [
    Team3Audit,
    Team3NewAudit
]

def get_initial_team3_issue_nature():
    return {
        'audit_issue_nature': {'all_well': 0, 'manageable': 0, 'critical': 0},
        'new_audit_issue_nature': {'all_well': 0, 'manageable': 0, 'critical': 0},
        'overall': {'all_well': 0, 'manageable': 0, 'critical': 0}
    }

def populate_team3_issue_nature(team3, date_filter_fn):
    team3_issue_nature = get_initial_team3_issue_nature()
    if not team3:
        return team3_issue_nature

    # Team 3 legacy Audit data
    query_filters = [Team3Audit.team_id == team3.team_id] + date_filter_fn(Team3Audit)
    for item in Team3Audit.query.filter(*query_filters).all():
        if item.issue_nature:
            nature = item.issue_nature.lower()
            if ('all_well' in nature or 'all well' in nature):
                team3_issue_nature['audit_issue_nature']['all_well'] += 1
                team3_issue_nature['overall']['all_well'] += 1
            elif ('manageable' in nature):
                team3_issue_nature['audit_issue_nature']['manageable'] += 1
                team3_issue_nature['overall']['manageable'] += 1
            elif ('critical' in nature):
                team3_issue_nature['audit_issue_nature']['critical'] += 1
                team3_issue_nature['overall']['critical'] += 1

    # Team 3 new audit form data
    query_filters_new = [Team3NewAudit.team_id == team3.team_id] + date_filter_fn(Team3NewAudit)
    for item in Team3NewAudit.query.filter(*query_filters_new).all():
        if item.issue_nature:
            nature = item.issue_nature.lower()
            if ('all_well' in nature or 'all well' in nature):
                team3_issue_nature['new_audit_issue_nature']['all_well'] += 1
                team3_issue_nature['overall']['all_well'] += 1
            elif ('manageable' in nature):
                team3_issue_nature['new_audit_issue_nature']['manageable'] += 1
                team3_issue_nature['overall']['manageable'] += 1
            elif ('critical' in nature):
                team3_issue_nature['new_audit_issue_nature']['critical'] += 1
                team3_issue_nature['overall']['critical'] += 1

    return team3_issue_nature
