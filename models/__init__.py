# models/__init__.py
# 100% Backwards-compatible re-export of all 120 SQLAlchemy models
import inspect

from .core import User, Team, Issue, Report
from .actions import Action
from .critical import (
    CapaFinding, CapaEvent, CapaAttachment,
    CAPA_STATUS_OPEN, CAPA_STATUS_PENDING_RECIPIENT, CAPA_STATUS_PENDING_AUDIT,
    CAPA_STATUS_REVISION_REQUIRED, CAPA_STATUS_CLOSED,
    CAPA_STATUSES, CAPA_STATUS_LABELS, CAPA_STATUS_CSS, CAPA_PRIORITIES,
    CAPA_DECISION_ACCEPTED, CAPA_DECISION_NOT_ACCEPTED,
    CAPA_STAGE_FINDING, CAPA_STAGE_RESPONSE, CAPA_STAGE_REVIEW
)
from .storage import FileStorage
from .acknowledgements import Acknowledgement
from .forms.base import BaseForm
from .forms import team1, team2, team3

# Dynamically re-export all team form classes to guarantee 100% attribute parity
for _mod in (team1, team2, team3):
    for _name, _cls in inspect.getmembers(_mod, inspect.isclass):
        if _cls.__module__ == _mod.__name__:
            globals()[_name] = _cls

# Core export list
__all__ = [
    'User', 'Team', 'Issue', 'Report',
    'Action', 'CapaFinding', 'CapaEvent', 'CapaAttachment',
    'FileStorage', 'Acknowledgement', 'BaseForm'
] + [
    _name for _mod in (team1, team2, team3)
    for _name, _cls in inspect.getmembers(_mod, inspect.isclass)
    if _cls.__module__ == _mod.__name__
]
