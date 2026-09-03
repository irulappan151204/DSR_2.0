# critical.py
# Backwards-compatibility wrapper re-exporting from repositories, services, and routes

from repositories.capa_repository import (
    can_audit, get_finding_by_id, get_finding_or_404, next_audit_reference,
    get_visible_findings_query, get_pending_critical_count as pending_critical_count,
    search_users_query, AUDIT_TEAM_ID, AUDIT_ROLES
)
from services.capa_service import (
    get_audit_lookups, can_view_finding, audit_required, team_display, user_label,
    log_event, transition, store_uploads, bust_user_cache, bust_team_lead_cache,
    bust_audit_caches, _clean,
    MAX_UPLOAD_BYTES, TEAM_DISPLAY_NAMES, ALLOWED_TRANSITIONS,
    AUDIT_FREQUENCIES, AUDIT_COMPONENTS, AUDIT_GRADES, AUDIT_SECTIONS,
    AUDIT_NATURE_OPTIONS, AUDIT_SPECIFICATIONS, AUDIT_STAFF_NAMES
)
from routes.capa_routes import (
    critical_bp, critical_home, new_finding, create_finding,
    edit_finding, update_finding, finding_detail, search_users,
    submit_response, submit_review
)

__all__ = [
    'critical_bp', 'can_audit', 'pending_critical_count', 'next_audit_reference',
    'get_audit_lookups', 'can_view_finding', 'audit_required', 'team_display',
    'user_label', 'log_event', 'transition', 'store_uploads', 'bust_user_cache',
    'bust_team_lead_cache', 'bust_audit_caches', 'critical_home', 'new_finding',
    'create_finding', 'edit_finding', 'update_finding', 'finding_detail',
    'search_users', 'submit_response', 'submit_review'
]
