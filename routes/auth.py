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
        """Render the user profile page"""
        return render_template('profile.html', user=current_user)
