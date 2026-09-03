from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import User, Action, Team  # and Action (to be created)
from datetime import datetime, timedelta
from extensions import db
from sqlalchemy import or_
from sqlalchemy.orm import joinedload
from sqlalchemy.orm.attributes import set_committed_value
from collections import defaultdict
from zoneinfo import ZoneInfo

actions_bp = Blueprint('actions', __name__, template_folder='templates/actions')

@actions_bp.route('/actions', methods=['GET'])
@login_required
def action_home():
    now = datetime.now(ZoneInfo('Asia/Kolkata'))
    
    # Get date filter parameters
    filter_date = request.args.get('filter_date')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    # If no date filter is provided by the user, default **range** from 2025-07-01 up to today.
    # This shows cumulative counts since the beginning of the academic year by default, while
    # still allowing users to override the filter via the UI.
    if not filter_date and not start_date and not end_date:
        start_date = '2025-07-01'
        end_date = now.date().strftime('%Y-%m-%d')
    
    # Build date filter query
    date_filter = None
    if filter_date:
        try:
            filter_date_obj = datetime.strptime(filter_date, '%Y-%m-%d').date()
            date_filter = db.func.date(Action.created_at) == filter_date_obj
        except ValueError:
            filter_date = None
    elif start_date and end_date:
        try:
            start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()
            date_filter = db.and_(
                db.func.date(Action.created_at) >= start_date_obj,
                db.func.date(Action.created_at) <= end_date_obj
            )
        except ValueError:
            start_date = None
            end_date = None
    
    action_counts = {}
    priority_counts = {}
    team_action_counts = None
    has_pending_actions = False
    
    if current_user.role == 'MD':
        users = User.query.all()
        base_query = Action.query.options(joinedload(Action.assigned_user))
        if date_filter is not None:
            base_query = base_query.filter(date_filter)
        actions = base_query.all()
        has_pending_actions = any(a.status != 'Finished' for a in actions)
    elif current_user.is_team_lead:
        # Team Leads: keep full user list for assignment UI,
        # but restrict visibility/counts to actions created by or assigned to their team
        users = User.query.all()
        team_user_ids = [u.user_id for u in User.query.filter_by(team_id=current_user.team_id).all()]
        
        # Get all actions (parent and child) that are:
        # 1. Assigned to team members OR created by team members OR assigned to the team lead
        # 2. OR are follow-up actions assigned to team members or team lead
        # 3. OR are follow-up actions created by team members or team lead
        base_query = Action.query.options(joinedload(Action.assigned_user)).filter(
            (Action.assigned_user_id.in_(team_user_ids)) |
            (Action.created_by.in_(team_user_ids)) |
            (Action.assigned_user_id == current_user.user_id) |
            (Action.created_by == current_user.user_id)
        )
        if date_filter is not None:
            base_query = base_query.filter(date_filter)
        actions = base_query.all()
        
        # Also include parent actions of child actions that are assigned to team members or team lead
        # This ensures we see the full context when team members are assigned follow-up actions
        child_actions = Action.query.options(joinedload(Action.assigned_user)).filter(
            ((Action.assigned_user_id.in_(team_user_ids)) | (Action.assigned_user_id == current_user.user_id)) & 
            (Action.parent_action_id != None)
        )
        if date_filter is not None:
            child_actions = child_actions.filter(date_filter)
        child_actions = child_actions.all()
        
        # Get parent actions of these child actions
        parent_ids = set(ca.parent_action_id for ca in child_actions if ca.parent_action_id)
        if parent_ids:
            parent_actions = Action.query.options(joinedload(Action.assigned_user)).filter(Action.id.in_(parent_ids))
            if date_filter is not None:
                parent_actions = parent_actions.filter(date_filter)
            parent_actions = parent_actions.all()
            
            # Merge all actions, avoiding duplicates
            action_ids = set(a.id for a in actions)
            for pa in parent_actions:
                if pa.id not in action_ids:
                    actions.append(pa)
                    action_ids.add(pa.id)
        
        has_pending_actions = any(a.status != 'Finished' for a in actions)
    else:
        # Team Members: restrict to only their own assigned actions
        users = User.query.filter_by(team_id=current_user.team_id).all()
        base_query = Action.query.options(joinedload(Action.assigned_user)).filter(
            (Action.assigned_user_id == current_user.user_id) |
            (Action.created_by == current_user.user_id)
        )
        if date_filter is not None:
            base_query = base_query.filter(date_filter)
        actions = base_query.all()
        
        # Also include parent actions of child actions assigned to the current user
        # This ensures we see the full context when assigned follow-up actions
        child_actions = Action.query.options(joinedload(Action.assigned_user)).filter(
            (Action.assigned_user_id == current_user.user_id) & (Action.parent_action_id != None)
        )
        if date_filter is not None:
            child_actions = child_actions.filter(date_filter)
        child_actions = child_actions.all()
        
        # Get parent actions of these child actions
        parent_ids = set(ca.parent_action_id for ca in child_actions if ca.parent_action_id)
        if parent_ids:
            parent_actions = Action.query.options(joinedload(Action.assigned_user)).filter(Action.id.in_(parent_ids))
            if date_filter is not None:
                parent_actions = parent_actions.filter(date_filter)
            parent_actions = parent_actions.all()
            
            # Merge all actions, avoiding duplicates
            action_ids = set(a.id for a in actions)
            for pa in parent_actions:
                if pa.id not in action_ids:
                    actions.append(pa)
                    action_ids.add(pa.id)
        
        has_pending_actions = any(a.status != 'Finished' for a in actions)
    
    # Add overdue and finished status for template
    for action in actions:
        due_date = action.due_date
        if due_date is not None and due_date.tzinfo is None:
            due_date = due_date.replace(tzinfo=ZoneInfo('Asia/Kolkata'))
        action.is_overdue = (action.status != 'Finished' and due_date < now)
        action.is_finished = (action.status == 'Finished')

    # For MD: compute team action counts in memory
    if current_user.role == 'MD':
        teams = Team.query.all()
        team_action_counts = {}
        team_display_names = {
            'Team 1': 'Academic',
            'Team 2': 'Admin', 
            'Team 3': 'Audit'
        }
        for team in teams:
            team_user_set = set(u.user_id for u in users if u.team_id == team.team_id)
            display_name = team_display_names.get(team.team_name, team.team_name)
            
            t_parents = [a for a in actions if a.parent_action_id is None and (a.assigned_user_id in team_user_set or a.created_by in team_user_set)]
            t_children = [a for a in actions if a.parent_action_id is not None and (a.assigned_user_id in team_user_set or a.created_by in team_user_set)]
            
            team_action_counts[display_name] = {
                'total': len(t_parents),
                'completed': sum(1 for a in t_parents if a.status == 'Finished'),
                'pending': sum(1 for a in t_parents if a.status != 'Finished'),
                'overdue': sum(1 for a in t_parents if a.is_overdue),
                'followup': len(t_children),
                'priority': {p: sum(1 for a in t_parents if a.priority == p) for p in ['Critical', 'High', 'Medium', 'Low']}
            }

    # --- Enhanced sorting/grouping logic for multiple levels of nesting ---
    def sort_actions_group(action_list):
        """Sort actions: unfinished first (by created_at desc), then finished (by completed_at desc, then created_at desc)"""
        unfinished = [a for a in action_list if a.status != 'Finished']
        finished = [a for a in action_list if a.status == 'Finished']
        unfinished_sorted = sorted(unfinished, key=lambda a: a.created_at, reverse=True)
        finished_sorted = sorted(finished, key=lambda a: (a.completed_at or datetime.min, a.created_at), reverse=True)
        return unfinished_sorted + finished_sorted

    def build_action_tree(actions_list):
        """Build a hierarchical tree structure for actions with multiple levels of nesting without N+1 queries"""
        # Separate parent and child actions
        parent_actions = [a for a in actions_list if a.parent_action_id is None]
        child_actions = [a for a in actions_list if a.parent_action_id is not None]
        
        # Build a mapping from parent_id to its children
        children_by_parent = defaultdict(list)
        for child in child_actions:
            children_by_parent[child.parent_action_id].append(child)
        
        # Sort parent actions
        parent_actions_sorted = sort_actions_group(parent_actions)
        
        # Recursively build child_actions for each parent
        def build_children_for_parent(parent):
            if parent.id in children_by_parent:
                children = sort_actions_group(children_by_parent[parent.id])
                # Recursively build children for each child (for nested follow-ups)
                for child in children:
                    child_nested = build_children_for_parent(child)
                    set_committed_value(child, 'child_actions', child_nested)
                return children
            else:
                return []
        
        # Build the complete tree using set_committed_value to prevent lazy load queries
        for parent in parent_actions_sorted:
            children = build_children_for_parent(parent)
            set_committed_value(parent, 'child_actions', children)
        
        # Ensure all actions have child_actions loaded so template never triggers lazy load
        for a in actions_list:
            if 'child_actions' not in a.__dict__:
                set_committed_value(a, 'child_actions', [])
        
        return parent_actions_sorted

    # Build the action tree
    parent_actions = build_action_tree(actions)
    
    # Flatten the tree for the final ordered list (for backward compatibility)
    def flatten_action_tree(parent_list):
        """Flatten the tree structure into a list while maintaining hierarchy"""
        result = []
        for parent in parent_list:
            result.append(parent)
            if hasattr(parent, 'child_actions') and parent.child_actions:
                result.extend(flatten_action_tree(parent.child_actions))
        return result
    
    # Create the final ordered list
    ordered_actions = flatten_action_tree(parent_actions)
    
    # Also include orphaned children (whose parent is not in the list)
    all_parent_ids = set()
    def collect_parent_ids(parent_list):
        for parent in parent_list:
            all_parent_ids.add(parent.id)
            if hasattr(parent, 'child_actions') and parent.child_actions:
                collect_parent_ids(parent.child_actions)
    
    collect_parent_ids(parent_actions)
    orphan_children = [a for a in actions if a.parent_action_id is not None and a.parent_action_id not in all_parent_ids]
    if orphan_children:
        ordered_actions.extend(sort_actions_group(orphan_children))
    
    actions = ordered_actions
    # --- End enhanced logic ---

    # Calculate counts in memory directly from actions list to eliminate 16+ redundant SQL queries
    if current_user.role == 'MD':
        parent_actions_list = [a for a in actions if a.parent_action_id is None]
        child_actions_list = [a for a in actions if a.parent_action_id is not None]
        action_counts = {
            'parent': {
                'total': len(parent_actions_list),
                'completed': sum(1 for a in parent_actions_list if a.status == 'Finished'),
                'pending': sum(1 for a in parent_actions_list if a.status != 'Finished'),
                'overdue': sum(1 for a in parent_actions_list if a.is_overdue)
            },
            'child': {
                'total': len(child_actions_list),
                'completed': sum(1 for a in child_actions_list if a.status == 'Finished'),
                'pending': sum(1 for a in child_actions_list if a.status != 'Finished'),
                'overdue': sum(1 for a in child_actions_list if a.is_overdue)
            }
        }
        priority_counts = {
            'parent': {p: sum(1 for a in parent_actions_list if a.priority == p) for p in ['Critical', 'High', 'Medium', 'Low']},
            'child': {p: sum(1 for a in child_actions_list if a.priority == p) for p in ['Critical', 'High', 'Medium', 'Low']}
        }
    elif current_user.role == 'Admin':
        parent_actions_list = [a for a in actions if a.parent_action_id is None]
        action_counts = {
            'total': len(parent_actions_list),
            'completed': sum(1 for a in parent_actions_list if a.status == 'Finished'),
            'pending': sum(1 for a in parent_actions_list if a.status != 'Finished'),
            'overdue': sum(1 for a in parent_actions_list if a.is_overdue)
        }
        priority_counts = {p: sum(1 for a in parent_actions_list if a.priority == p) for p in ['Critical', 'High', 'Medium', 'Low']}
    elif current_user.is_team_lead:
        parent_actions_list = [a for a in actions if a.parent_action_id is None]
        child_actions_list = [a for a in actions if a.parent_action_id is not None]
        action_counts = {
            'parent': {
                'total': len(parent_actions_list),
                'completed': sum(1 for a in parent_actions_list if a.status == 'Finished'),
                'pending': sum(1 for a in parent_actions_list if a.status != 'Finished'),
                'overdue': sum(1 for a in parent_actions_list if a.is_overdue)
            },
            'child': {
                'total': len(child_actions_list),
                'completed': sum(1 for a in child_actions_list if a.status == 'Finished'),
                'pending': sum(1 for a in child_actions_list if a.status != 'Finished'),
                'overdue': sum(1 for a in child_actions_list if a.is_overdue)
            }
        }
        priority_counts = {
            'parent': {p: sum(1 for a in parent_actions_list if a.priority == p) for p in ['Critical', 'High', 'Medium', 'Low']},
            'child': {p: sum(1 for a in child_actions_list if a.priority == p) for p in ['Critical', 'High', 'Medium', 'Low']}
        }
    else:
        parent_actions_list = [a for a in actions if a.parent_action_id is None]
        action_counts = {
            'total': len(parent_actions_list),
            'completed': sum(1 for a in parent_actions_list if a.status == 'Finished'),
            'pending': sum(1 for a in parent_actions_list if a.status != 'Finished'),
            'overdue': sum(1 for a in parent_actions_list if a.is_overdue)
        }
        priority_counts = {p: sum(1 for a in parent_actions_list if a.priority == p) for p in ['Critical', 'High', 'Medium', 'Low']}
    
    return render_template('actions/action_form.html', 
                         users=users, 
                         actions=actions, 
                         action_counts=action_counts, 
                         priority_counts=priority_counts, 
                         team_action_counts=team_action_counts, 
                         has_pending_actions=has_pending_actions,
                         filter_date=filter_date,
                         start_date=start_date,
                         end_date=end_date)

@actions_bp.route('/actions/create', methods=['POST'])
@login_required
def create_action():
    # Obtain title either from hidden/custom input (name="title") or directly from dropdown (name="title_select")
    title = request.form.get('title') or request.form.get('title_select')
    priority = request.form.get('priority')
    due_date = request.form.get('due_date')
    action_text = request.form.get('action')

    # For MD: allow multi-user assignment or 'all'
    if current_user.role == 'MD':
        assigned_users = request.form.getlist('assigned_user')
        if 'all' in assigned_users:
            # Assign to all members (excluding MD and Admin)
            all_members = User.query.filter(~User.role.in_(['MD', 'Admin'])).all()
            assigned_user_ids = [u.user_id for u in all_members]
        else:
            assigned_user_ids = []
            for uid_str in assigned_users:
                if not uid_str:
                    continue
                # Handle potential comma separated list from hidden input
                for part in uid_str.split(','):
                    part = part.strip()
                    if part:
                        try:
                            assigned_user_ids.append(int(part))
                        except ValueError:
                            pass
    elif current_user.is_team_lead:
        # Team Leads can now assign to multiple users or 'all', including MD users
        assigned_users = request.form.getlist('assigned_user')
        if 'all' in assigned_users:
            all_members = User.query.filter(~User.role.in_(['Admin'])).all()
            assigned_user_ids = [u.user_id for u in all_members]
        else:
            assigned_user_ids = []
            for uid_str in assigned_users:
                if not uid_str:
                    continue
                # Handle potential comma separated list from hidden input
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
    action = Action.query.get_or_404(action_id)
    if action.assigned_user_id != current_user.user_id:
        flash('You are not authorized to update this action.', 'danger')
        redirect_to = request.form.get('redirect_to', url_for('actions.action_home'))
        return redirect(redirect_to)
    
    status = request.form.get('status')
    completion_message = request.form.get('completion_message')
    
    action.status = status
    action.completion_message = completion_message
    
    # If status is Finished, set completed_at
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
    # Check if user is authorized to loop actions (only MD and Team Lead)
    if not (current_user.role == 'MD' or current_user.is_team_lead):
        flash('You are not authorized to create follow-up actions.', 'danger')
        redirect_to = request.form.get('redirect_to', url_for('actions.action_home'))
        return redirect(redirect_to)
    
    # Get the action to create follow-up for (can be parent or child action)
    target_action = Action.query.get_or_404(action_id)
    
    # For team leads, allow assigning to all users except Admin
    if current_user.is_team_lead:
        users = User.query.filter(~User.role.in_(['Admin'])).all()
    elif current_user.role == 'MD':
        # MD can assign to anyone except Admin
        users = User.query.filter(~User.role.in_(['Admin'])).all()
    else:
        # This shouldn't happen due to the authorization check above, but just in case
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
                parent_action_id=action_id,  # This can now be any action (parent or child)
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