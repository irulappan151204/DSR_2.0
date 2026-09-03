# routes/forms/__init__.py
from .team1_forms import register_team1_forms
from .team2_forms import register_team2_forms
from .team3_forms import register_team3_forms

def register_all_form_routes(app):
    """Register all 108 form submission handlers on the Flask app."""
    register_team1_forms(app)
    register_team2_forms(app)
    register_team3_forms(app)
