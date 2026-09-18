from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from extensions import db, bcrypt
from models import User

def register_auth_routes(app):
    """Register authentication and profile routes."""
    @app.route('/')
    def index():
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))
        return redirect(url_for('login'))

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            user = User.query.filter_by(username=username).first()
            if user and not user.is_active:
                flash('This account has been deactivated. Please contact an administrator.', 'error')
                return render_template('login.html')

            if user and bcrypt.check_password_hash(user.password, password):
                login_user(user)
                if user.is_team_lead:
                    if user.team_id == 1:
                        return redirect(url_for('md_dashboard.md_dashboard', team='team1'))
                    elif user.team_id == 2:
                        return redirect(url_for('md_dashboard.md_dashboard', team='team2'))
                    elif user.team_id == 3:
                        return redirect(url_for('md_dashboard.md_dashboard', team='team3'))
                return redirect(url_for('dashboard'))
            flash('Invalid username or password', 'error')
        return render_template('login.html')

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('login'))

    @app.route('/profile')
    @login_required
    def profile():
        """Render the user profile page with dynamic activity stats."""
        from sqlalchemy import text, func
        from models import Issue, Action, Acknowledgement

        user = current_user
        stats = {}

        # Forms submitted (across all form tables)
        try:
            form_count = 0
            from routes.admin import ALL_FORM_TABLES
            for tbl in ALL_FORM_TABLES:
                try:
                    row = db.session.execute(
                        text(f"SELECT COUNT(*) FROM `{tbl}` WHERE submitted_by = :uid"),
                        {"uid": user.user_id}
                    ).scalar()
                    form_count += row or 0
                except Exception:
                    continue
            stats['forms_submitted'] = form_count
        except Exception:
            stats['forms_submitted'] = 0

        # Issues created
        try:
            stats['issues_created'] = Issue.query.filter_by(created_by_id=user.user_id).count()
        except Exception:
            stats['issues_created'] = 0

        # Issues resolved
        try:
            stats['issues_resolved'] = Issue.query.filter_by(solved_by=user.user_id).count()
        except Exception:
            stats['issues_resolved'] = 0

        # Actions assigned (pending)
        try:
            stats['actions_pending'] = Action.query.filter_by(
                assigned_user_id=user.user_id, status='Pending'
            ).count()
        except Exception:
            stats['actions_pending'] = 0

        # Actions completed
        try:
            stats['actions_completed'] = Action.query.filter_by(
                assigned_user_id=user.user_id, status='Completed'
            ).count()
        except Exception:
            stats['actions_completed'] = 0

        # CAPA findings (if user is recipient or creator)
        try:
            from models import CapaFinding
            stats['capa_assigned'] = CapaFinding.query.filter_by(recipient_id=user.user_id).count()
        except Exception:
            stats['capa_assigned'] = 0

        # Acknowledgements
        try:
            stats['acknowledgements'] = Acknowledgement.query.filter_by(user_id=user.user_id).count()
        except Exception:
            stats['acknowledgements'] = 0

        return render_template('profile.html', user=user, stats=stats)

