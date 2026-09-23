from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from extensions import db, bcrypt, limiter
from models import User

def register_auth_routes(app):
    """Register authentication and profile routes."""
    @app.route('/')
    def index():
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))
        return redirect(url_for('login'))

    @app.route('/login', methods=['GET', 'POST'])
    @limiter.limit("5 per minute;20 per hour")
    def login():
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            user = User.query.filter_by(username=username).first()
            if user and not user.is_active:
                app.logger.warning(f"Login attempt on deactivated account: '{username}' from {request.remote_addr}")
                flash('This account has been deactivated. Please contact an administrator.', 'error')
                return render_template('login.html')

            if user and bcrypt.check_password_hash(user.password, password):
                login_user(user)
                app.logger.info(f"Successful login: '{user.username}' (ID: {user.user_id}) from {request.remote_addr}")
                if user.is_team_lead:
                    if user.team_id == 1:
                        return redirect(url_for('md_dashboard.md_dashboard', team='team1'))
                    elif user.team_id == 2:
                        return redirect(url_for('md_dashboard.md_dashboard', team='team2'))
                    elif user.team_id == 3:
                        return redirect(url_for('md_dashboard.md_dashboard', team='team3'))
                return redirect(url_for('dashboard'))
            app.logger.warning(f"Failed login attempt for username: '{username}' from {request.remote_addr}")
            flash('Invalid username or password', 'error')
        return render_template('login.html')

    @app.route('/logout')
    @login_required
    def logout():
        username = current_user.username if current_user.is_authenticated else 'unknown'
        app.logger.info(f"User logout: '{username}' from {request.remote_addr}")
        logout_user()
        return redirect(url_for('login'))

    @app.route('/profile')
    @login_required
    def profile():
        """Render the user profile page"""
        from acknowledgements import get_unack_count_for_user
        unack_count = get_unack_count_for_user(current_user)
        return render_template('profile.html', user=current_user, unack_count=unack_count)

