from datetime import datetime
from zoneinfo import ZoneInfo
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from extensions import db
from models import Action, User
from repositories.action_repository import get_action_or_404
from services.action_service import prepare_actions_dashboard

actions_bp = Blueprint('actions', __name__, template_folder='templates/actions')

@actions_bp.route('/actions', methods=['GET'])
@login_required
def action_home():
    filter_date = request.args.get('filter_date')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    data = prepare_actions_dashboard(current_user, filter_date, start_date, end_date)

    return render_template(
        'actions/action_form.html',
        users=data['users'],
        actions=data['actions'],
        action_counts=data['action_counts'],
        priority_counts=data['priority_counts'],
        team_action_counts=data['team_action_counts'],
        has_pending_actions=data['has_pending_actions'],
        filter_date=data['filter_date'],
        start_date=data['start_date'],
        end_date=data['end_date']
    )

@actions_bp.route('/actions/create', methods=['POST'])
@login_required
def create_action():
    title = request.form.get('title') or request.form.get('title_select')
    priority = request.form.get('priority')
    due_date = request.form.get('due_date')
    action_text = request.form.get('action')

    if current_user.role == 'MD':
        assigned_users = request.form.getlist('assigned_user')
        if 'all' in assigned_users:
            all_members = User.query.filter(~User.role.in_(['MD', 'Admin'])).all()
            assigned_user_ids = [u.user_id for u in all_members]
        else:
            assigned_user_ids = []
            for uid_str in assigned_users:
                if not uid_str:
                    continue
                for part in uid_str.split(','):
                    part = part.strip()
                    if part:
                        try:
                            assigned_user_ids.append(int(part))
                        except ValueError:
                            pass
    elif current_user.is_team_lead:
        assigned_users = request.form.getlist('assigned_user')
        if 'all' in assigned_users:
            all_members = User.query.filter(~User.role.in_(['Admin'])).all()
            assigned_user_ids = [u.user_id for u in all_members]
        else:
            assigned_user_ids = []
            for uid_str in assigned_users:
                if not uid_str:
                    continue
                for part in uid_str.split(','):
                    part = part.strip()
                    if part:
                        try:
                            assigned_user_ids.append(int(part))
                        except ValueError:
                            pass
        if not assigned_user_ids:
            flash('Please select at least one user to assign the action.', 'danger')
            redirect_to = request.form.get('redirect_to', url_for('actions.action_home'))
            return redirect(redirect_to)
    else:
        flash('You are not authorized to create actions.', 'danger')
        redirect_to = request.form.get('redirect_to', url_for('actions.action_home'))
        return redirect(redirect_to)

    try:
        assigned_user_ids = list(set(assigned_user_ids))
        if not title:
            flash('Please select or provide a Title/Description.', 'danger')
            redirect_to = request.form.get('redirect_to', url_for('actions.action_home'))
            return redirect(redirect_to)
        for uid in assigned_user_ids:
            action = Action(
                title=title,
                assigned_user_id=uid,
                priority=priority,
                due_date=datetime.strptime(due_date, '%Y-%m-%dT%H:%M').replace(tzinfo=ZoneInfo('Asia/Kolkata')),
                action_text=action_text,
                created_by=current_user.user_id
            )
            db.session.add(action)
        db.session.commit()
        flash('Action(s) created successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error creating action(s): {str(e)}', 'danger')

    redirect_to = request.form.get('redirect_to', url_for('actions.action_home'))
    return redirect(redirect_to)

@actions_bp.route('/actions/finish/<int:action_id>', methods=['POST'])
@login_required
def finish_action(action_id):
    action = get_action_or_404(action_id)
    if action.assigned_user_id != current_user.user_id:
        flash('You are not authorized to update this action.', 'danger')
        redirect_to = request.form.get('redirect_to', url_for('actions.action_home'))
        return redirect(redirect_to)

    status = request.form.get('status')
    completion_message = request.form.get('completion_message')

    action.status = status
    action.completion_message = completion_message

    if status == 'Finished':
        action.completed_at = datetime.now(ZoneInfo('Asia/Kolkata'))
        flash('Action marked as finished!', 'success')
    else:
        flash(f'Action status updated to {status}!', 'success')

    db.session.commit()
    redirect_to = request.form.get('redirect_to', url_for('actions.action_home'))
    return redirect(redirect_to)

@actions_bp.route('/actions/loop/<int:action_id>', methods=['GET', 'POST'])
@login_required
def loop_action(action_id):
    if not (current_user.role == 'MD' or current_user.is_team_lead):
        flash('You are not authorized to create follow-up actions.', 'danger')
        redirect_to = request.form.get('redirect_to', url_for('actions.action_home'))
        return redirect(redirect_to)

    target_action = get_action_or_404(action_id)
    users = User.query.filter(~User.role.in_(['Admin'])).all()

    if request.method == 'POST':
        title = request.form.get('title')
        assigned_user = request.form.get('assigned_user')
        priority = request.form.get('priority')
        due_date = request.form.get('due_date')
        action_text = request.form.get('action')
        loop_message = request.form.get('loop_message', '')

        try:
            action = Action(
                title=title,
                assigned_user_id=int(assigned_user),
                priority=priority,
                due_date=datetime.strptime(due_date, '%Y-%m-%dT%H:%M').replace(tzinfo=ZoneInfo('Asia/Kolkata')),
                action_text=action_text,
                created_by=current_user.user_id,
                parent_action_id=action_id,
                loop_message=loop_message
            )
            db.session.add(action)
            db.session.commit()
            flash('Follow-up action created successfully!', 'success')
            redirect_to = request.form.get('redirect_to', url_for('actions.action_home'))
            return redirect(redirect_to)
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating follow-up action: {str(e)}', 'danger')

    return render_template('actions/action_form.html', users=users, parent_action=target_action, loop_mode=True)
