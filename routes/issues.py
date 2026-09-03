from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from extensions import db, socketio
from models import Issue, Team

def register_issues_routes(app):
    """Register issue tracker routes."""
    @app.route('/issues')
    @login_required
    def list_issues():
        if current_user.role == 'Admin':
            issues = Issue.query.all()
        elif current_user.role == 'Team Lead':
            issues = Issue.query.filter_by(team_id=current_user.team_id).all()
        elif current_user.role == 'Team Member':
            issues = Issue.query.filter_by(team_id=current_user.team_id).all()
        else:  # MD
            issues = Issue.query.all()
        return render_template('issues/list.html', issues=issues)

    @app.route('/issues/<int:issue_id>')
    @login_required
    def view_issue(issue_id):
        issue = Issue.query.get_or_404(issue_id)
        if current_user.role not in ['Admin', 'MD'] and issue.team_id != current_user.team_id:
            flash('Access denied.', 'error')
            return redirect(url_for('list_issues'))
        return render_template('issues/view.html', issue=issue)

    @app.route('/issues/create', methods=['GET', 'POST'])
    @login_required
    def create_issue():
        if current_user.role != 'Admin':
            flash('Access denied. Only Admin can create issues.', 'error')
            return redirect(url_for('list_issues'))

        if request.method == 'POST':
            issue_title = request.form.get('title')
            team_id = request.form.get('team_id')

            new_issue = Issue(
                issue_title=issue_title,
                issue_description="",
                priority="Medium",
                team_id=team_id,
                status='Open',
                created_by_id=current_user.user_id
            )
            db.session.add(new_issue)
            db.session.commit()
            flash('Issue created successfully.', 'success')
            return redirect(url_for('list_issues'))

        teams = Team.query.all()
        return render_template('issues/create.html', teams=teams)

    @app.route('/issues/<int:issue_id>/edit', methods=['GET', 'POST'])
    @login_required
    def edit_issue(issue_id):
        issue = Issue.query.get_or_404(issue_id)

        if current_user.role not in ['Admin', 'Team Lead'] or (current_user.role == 'Team Lead' and issue.team_id != current_user.team_id):
            flash('Access denied.', 'error')
            return redirect(url_for('list_issues'))

        if request.method == 'POST':
            issue.issue_title = request.form.get('title')
            issue.issue_description = request.form.get('description')
            issue.priority = request.form.get('priority')
            issue.status = request.form.get('status')

            if current_user.role == 'Admin':
                new_team_id = request.form.get('team_id')
                if new_team_id:
                    issue.team_id = new_team_id

            if issue.status == 'Solved':
                issue.solved_by = current_user.user_id
                issue.solved_description = request.form.get('solved_description')

            db.session.commit()
            flash('Issue updated successfully.', 'success')
            return redirect(url_for('list_issues'))

        teams = Team.query.all()
        return render_template('issues/edit.html', issue=issue, teams=teams)

    @app.route('/issues/<int:issue_id>/delete')
    @login_required
    def delete_issue(issue_id):
        issue = Issue.query.get_or_404(issue_id)
        if current_user.role != 'Admin':
            flash('Access denied. Only administrators can delete issues.', 'error')
            return redirect(url_for('list_issues'))

        db.session.delete(issue)
        db.session.commit()
        flash('Issue deleted successfully.', 'success')
        return redirect(url_for('list_issues'))

    @app.route('/issues/<int:issue_id>/resolve', methods=['POST'])
    @login_required
    def resolve_issue(issue_id):
        issue = Issue.query.get_or_404(issue_id)
        if current_user.role not in ['Admin', 'Team Lead'] or (current_user.role == 'Team Lead' and issue.team_id != current_user.team_id):
            flash('Access denied.', 'error')
            return redirect(url_for('list_issues'))

        issue.status = 'Solved'
        issue.solved_by = current_user.user_id
        issue.solved_description = request.form.get('solved_description')

        db.session.commit()
        flash('Issue resolved successfully.', 'success')
        return redirect(url_for('view_issue', issue_id=issue_id))

    @app.route('/update_issue', methods=['POST'])
    @login_required
    def update_issue():
        if current_user.role not in ['Team Lead', 'Team Member']:
            flash('Access denied. Only team members can update issues.', 'danger')
            return redirect(url_for('dashboard'))

        issue_id = request.form.get('issue_id')
        description = request.form.get('description')
        priority = request.form.get('priority')
        status = request.form.get('status')

        issue = Issue.query.get_or_404(issue_id)
        if current_user.team_id != issue.team_id:
            flash('Access denied. You can only update issues for your team.', 'danger')
            return redirect(url_for('dashboard'))

        issue.issue_description = description
        issue.priority = priority
        issue.status = status

        db.session.commit()
        socketio.emit('issue_update', {'issue_id': issue_id})

        flash('Issue updated successfully!', 'success')
        return redirect(url_for('dashboard'))
