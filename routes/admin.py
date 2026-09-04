from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from sqlalchemy import text
from extensions import db, bcrypt
from models import User, Team, Action, Issue, Acknowledgement, FileStorage
from cache_utils import bust_user_dashboard_cache
from services.capa_service import bust_team_lead_cache
from utils.admin_audit import log_admin_action

ALL_FORM_TABLES = [
    'team1_calendar_schedule', 'team1_asa_activities', 'team1_asa_sports', 'team1_student_attendance',
    'team1_student_grooming', 'team1_student_late_coming', 'team1_admission_status',
    'team1_transfer_certificate', 'team1_parent_activity', 'team1_parent_visit',
    'team1_exam_schedule', 'team1_external_info', 'team1_sick_bay',
    'team1_home_school_comm', 'team1_disciplinary', 'team1_logistics',
    'team1_competition_cert', 'team1_staff_concern', 'team1_student_concern', 'team1_parent_concern',
    'team1_parent_concern_detail', 'team1_aep_attendance', 'team1_extended_class_attendance',
    'team1_training_session', 'team1_weekly_meeting', 'team1_special_education',
    'team1_hostel', 'team1_sec', 'team1_school_counsellor', 'team1_scholorius',
    'team2_hr_attendance', 'team2_admin_attendance', 'team2_total_hr_attendance',
    'team2_recruitment_activity', 'team2_pending_recruitment', 'team2_recruitment_pipeline',
    'team2_staff_status_updates', 'team2_salary_pending', 'team2_police_verification',
    'team2_interview_schedule', 'team2_exit_information', 'team2_issues_staff_concerns',
    'team2_kural_recitation', 'team2_front_office_phone_calls', 'team2_visitor_log',
    'team2_bsnl_phone_status', 'team2_materials_inward', 'team2_materials_outward',
    'team2_materials_movement', 'team2_returnable_material_tracking',
    'team2_returnable_goods_report', 'team2_campus_camera_status', 'team2_vehicle_camera_status',
    'team2_bus_ac_camera_status', 'team2_gps_monitoring', 'team2_issues_identified_monitoring',
    'team2_issues_identified_control_room', 'team2_camera_footage_entry',
    'team2_biometrics_access_card_punching', 'team2_water_tds_deviation', 'team2_testing_cleaning',
    'team2_water_level', 'team2_housekeeping_general', 'team2_pool_testing',
    'team2_washroom_cleanliness', 'team2_transport_attendance', 'team2_ac_working_status',
    'team2_late_reporting', 'team2_maintenance_service_issues', 'team2_car_maintenance_cleaning',
    'team2_vehicle_renewals_delays', 'team2_special_trip', 'team2_parent_concern_detail',
    'team2_ac_temperature_check', 'team2_labor_eb_solar_genset', 'team2_motor',
    'team2_pest_control', 'team2_ac_temp_deviation', 'team2_electricity_consumption',
    'team2_eb_details', 'team2_solar_details', 'team2_genset_details',
    'team2_count_verification', 'team2_attendance_replacement', 'team2_security_info_note',
    'team2_security_govt_inout', 'team2_alcohol_test', 'team2_security_materials_inout',
    'team2_security_materials_outward', 'team2_transport_verification', 'team2_documents_movement',
    'team2_govt_official_documents', 'team2_thoorigai_team_social_media', 'team2_website_updates',
    'team2_md_social_media', 'team2_intercom_maintenance', 'team2_health_check_up',
    'team2_net_connectivity_print_details', 'team2_general_maintenance_it_products',
    'team2_calendar_schedule', 'team2_training_attendance', 'team2_training_details',
    'team2_manpower_planning', 'team2_overall_consolidation', 'uniform_details',
    'department_wise_uniform_details', 'team3_audit', 'team3_new_audit', 'team1_asa_general'
]

def get_users_with_history():
    """Return a set of user IDs that have submitted forms, created/resolved issues,
    actions, files, or CAPA records to safeguard historical integrity in the UI.
    """
    uids = set()
    queries = [
        "SELECT DISTINCT created_by_id FROM issues WHERE created_by_id IS NOT NULL",
        "SELECT DISTINCT solved_by FROM issues WHERE solved_by IS NOT NULL",
        "SELECT DISTINCT assigned_user_id FROM actions WHERE assigned_user_id IS NOT NULL",
        "SELECT DISTINCT created_by FROM actions WHERE created_by IS NOT NULL",
        "SELECT DISTINCT user_id FROM acknowledgements WHERE user_id IS NOT NULL",
        "SELECT DISTINCT uploaded_by FROM file_storage WHERE uploaded_by IS NOT NULL",
        "SELECT DISTINCT recipient_id FROM capa_findings WHERE recipient_id IS NOT NULL",
        "SELECT DISTINCT capa_1_submitted_by FROM capa_findings WHERE capa_1_submitted_by IS NOT NULL",
        "SELECT DISTINCT capa_2_submitted_by FROM capa_findings WHERE capa_2_submitted_by IS NOT NULL",
        "SELECT DISTINCT audit_reviewed_by FROM capa_findings WHERE audit_reviewed_by IS NOT NULL",
        "SELECT DISTINCT user_id FROM capa_events WHERE user_id IS NOT NULL",
        "SELECT DISTINCT uploaded_by FROM capa_attachments WHERE uploaded_by IS NOT NULL",
    ]
    for tbl in ['team1_student_attendance', 'team2_hr_attendance', 'team3_audit',
                'team1_calendar_schedule', 'team2_visitor_log', 'team2_materials_inward',
                'team2_admin_attendance', 'team1_admission_status', 'team3_new_audit']:
        queries.append(f"SELECT DISTINCT submitted_by FROM {tbl} WHERE submitted_by IS NOT NULL")

    for q in queries:
        try:
            for row in db.session.execute(text(q)).fetchall():
                if row[0]:
                    uids.add(row[0])
        except Exception:
            continue
    return uids

def user_has_historical_records(user_id):
    """Deep check verifying if a specific user has ANY historical activity before deletion."""
    if Issue.query.filter((Issue.created_by_id == user_id) | (Issue.solved_by == user_id)).first():
        return True
    if Action.query.filter((Action.created_by == user_id) | (Action.assigned_user_id == user_id)).first():
        return True
    if Acknowledgement.query.filter_by(user_id=user_id).first():
        return True
    if FileStorage.query.filter_by(uploaded_by=user_id).first():
        return True

    try:
        from models import CapaFinding, CapaWorkflowHistory, CapaAttachment
        if CapaFinding.query.filter(
            (CapaFinding.recipient_id == user_id) |
            (CapaFinding.capa_1_submitted_by == user_id) |
            (CapaFinding.capa_2_submitted_by == user_id) |
            (CapaFinding.audit_reviewed_by == user_id)
        ).first():
            return True
        if CapaWorkflowHistory.query.filter_by(user_id=user_id).first():
            return True
        if CapaAttachment.query.filter_by(uploaded_by=user_id).first():
            return True
    except Exception:
        pass

    for tbl in ALL_FORM_TABLES:
        try:
            res = db.session.execute(
                text(f"SELECT 1 FROM {tbl} WHERE submitted_by = :uid LIMIT 1"),
                {'uid': user_id}
            ).fetchone()
            if res:
                return True
        except Exception:
            continue
    return False

def register_admin_routes(app):
    """Register user and team admin management routes."""

    @app.route('/admin/users')
    @login_required
    def manage_users():
        if current_user.role != 'Admin':
            flash('Access denied. Admin privileges required.', 'error')
            return redirect(url_for('dashboard'))
        users = User.query.all()
        users_with_history = get_users_with_history()
        teams = Team.query.all()
        return render_template('admin/manage_users.html', users=users, users_with_history=users_with_history, teams=teams)

    @app.route('/admin/users/add', methods=['GET', 'POST'])
    @login_required
    def add_user():
        if current_user.role != 'Admin':
            flash('Access denied. Admin privileges required.', 'error')
            return redirect(url_for('dashboard'))

        if request.method == 'POST':
            username = request.form.get('username', '').strip()
            password = request.form.get('password', '')
            role = request.form.get('role')
            team_id = request.form.get('team_id')

            if not username or not password or not role:
                flash('Username, password, and role are required.', 'error')
                return redirect(url_for('add_user'))

            if User.query.filter_by(username=username).first():
                flash('Username already exists.', 'error')
                return redirect(url_for('add_user'))

            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            new_user = User(
                username=username,
                password=hashed_password,
                role=role,
                team_id=int(team_id) if team_id else None
            )
            db.session.add(new_user)
            db.session.commit()

            if role == 'Team Lead' and new_user.team_id:
                team = Team.query.get(new_user.team_id)
                if team and not team.lead_id:
                    team.lead_id = new_user.user_id
                    db.session.commit()

            log_admin_action(
                current_user,
                'CREATE_USER',
                new_user.user_id,
                new_user.username,
                reason=f"Role: {role}, Team: {team_id}",
                ip_address=request.remote_addr
            )

            flash('User created successfully.', 'success')
            return redirect(url_for('manage_users'))

        teams = Team.query.all()
        return render_template('admin/add_user.html', teams=teams)

    @app.route('/admin/users/edit/<int:user_id>', methods=['GET', 'POST'])
    @login_required
    def edit_user(user_id):
        if current_user.role != 'Admin':
            flash('Access denied. Admin privileges required.', 'error')
            return redirect(url_for('dashboard'))

        user = User.query.get_or_404(user_id)

        if request.method == 'POST':
            new_username = request.form.get('username', '').strip()
            new_role = request.form.get('role')
            team_id = request.form.get('team_id')
            password = request.form.get('password')

            if not new_username:
                flash('Username cannot be empty.', 'error')
                return redirect(url_for('edit_user', user_id=user_id))

            # Check username uniqueness against other users
            existing = User.query.filter(User.username == new_username, User.user_id != user.user_id).first()
            if existing:
                flash('Username already exists. Please choose a different username.', 'error')
                return redirect(url_for('edit_user', user_id=user_id))

            # Prevent Admin self-demotion
            if user.user_id == current_user.user_id and new_role != 'Admin':
                flash('You cannot demote your own admin account. Admin privileges must be retained.', 'error')
                return redirect(url_for('edit_user', user_id=user_id))

            old_role = user.role
            user.username = new_username
            user.role = new_role
            user.team_id = int(team_id) if team_id else None

            # If user was demoted from Team Lead, sync Team.lead_id
            if old_role == 'Team Lead' and new_role != 'Team Lead':
                teams_led = Team.query.filter_by(lead_id=user.user_id).all()
                for t in teams_led:
                    t.lead_id = None

            # If user is a Team Lead and team changed, sync any previous teams led
            if new_role == 'Team Lead' and user.team_id:
                teams_led = Team.query.filter_by(lead_id=user.user_id).all()
                for t in teams_led:
                    if t.team_id != user.team_id:
                        t.lead_id = None
                target_team = Team.query.get(user.team_id)
                if target_team and not target_team.lead_id:
                    target_team.lead_id = user.user_id

            if password:
                user.password = bcrypt.generate_password_hash(password).decode('utf-8')

            try:
                db.session.commit()
                bust_user_dashboard_cache(user.user_id)
                log_admin_action(
                    current_user,
                    'EDIT_USER',
                    user.user_id,
                    user.username,
                    reason=f"Role: {new_role}, Team: {team_id}, PasswordChanged: {bool(password)}",
                    ip_address=request.remote_addr
                )
                flash('User updated successfully.', 'success')
                return redirect(url_for('manage_users'))
            except Exception as e:
                db.session.rollback()
                flash(f'Error updating user: {str(e)}', 'error')
                return redirect(url_for('edit_user', user_id=user_id))

        teams = Team.query.all()
        return render_template('admin/edit_user.html', user=user, teams=teams)

    @app.route('/admin/users/deactivate/<int:user_id>', methods=['POST'])
    @login_required
    def deactivate_user(user_id):
        if current_user.role != 'Admin':
            flash('Access denied. Admin privileges required.', 'error')
            return redirect(url_for('dashboard'))

        user = User.query.get_or_404(user_id)

        # Self-deactivation protection
        if user.user_id == current_user.user_id:
            flash('You cannot deactivate your own admin account.', 'error')
            return redirect(url_for('manage_users'))

        reason = request.form.get('reason', 'Employee left organization').strip()

        # If user was leading any team, vacate the lead position safely
        teams_led = Team.query.filter_by(lead_id=user.user_id).all()
        for t in teams_led:
            t.lead_id = None

        user.deactivate()
        try:
            db.session.commit()
            bust_user_dashboard_cache(user.user_id)
            log_admin_action(
                current_user,
                'DEACTIVATE_USER',
                user.user_id,
                user.username,
                reason=reason,
                ip_address=request.remote_addr
            )
            flash(f"User '{user.username}' has been deactivated. Login is now blocked while all historical records and audit logs are preserved.", 'success')
        except Exception as e:
            db.session.rollback()
            flash(f"Error deactivating user: {str(e)}", 'error')

        return redirect(url_for('manage_users'))

    @app.route('/admin/users/reactivate/<int:user_id>', methods=['POST'])
    @login_required
    def reactivate_user(user_id):
        if current_user.role != 'Admin':
            flash('Access denied. Admin privileges required.', 'error')
            return redirect(url_for('dashboard'))

        user = User.query.get_or_404(user_id)

        user.reactivate()
        try:
            db.session.commit()
            bust_user_dashboard_cache(user.user_id)
            log_admin_action(
                current_user,
                'REACTIVATE_USER',
                user.user_id,
                user.username,
                reason="Admin reactivation",
                ip_address=request.remote_addr
            )
            flash(f"User '{user.username}' has been reactivated successfully. They may now log in with their existing credentials.", 'success')
        except Exception as e:
            db.session.rollback()
            flash(f"Error reactivating user: {str(e)}", 'error')

        return redirect(url_for('manage_users'))

    @app.route('/admin/users/delete/<int:user_id>', methods=['GET', 'POST'])
    @login_required
    def delete_user(user_id):
        if current_user.role != 'Admin':
            flash('Access denied. Admin privileges required.', 'error')
            return redirect(url_for('dashboard'))

        user = User.query.get_or_404(user_id)
        if user.user_id == current_user.user_id:
            flash('Cannot delete your own account.', 'error')
            return redirect(url_for('manage_users'))

        # Enforce POST for destructive deletion
        if request.method != 'POST':
            flash('Deletions must be confirmed through the admin interface.', 'error')
            return redirect(url_for('manage_users'))

        # Safeguard: Verify if user has ANY historical data across forms, issues, actions, CAPA
        if user_has_historical_records(user_id):
            flash(
                f"Cannot delete user '{user.username}': This user has historical submissions and audit records. "
                "Deactivate the user instead to preserve audit compliance and prevent data loss.",
                'error'
            )
            return redirect(url_for('manage_users'))

        # User is confirmed to have zero historical records (e.g. test or mistake account)
        try:
            # Vacate any team lead pointers if set
            teams_led = Team.query.filter_by(lead_id=user_id).all()
            for t in teams_led:
                t.lead_id = None

            username = user.username
            db.session.delete(user)
            db.session.commit()

            log_admin_action(
                current_user,
                'DELETE_USER',
                user_id,
                username,
                reason="Fresh user with zero historical records deleted",
                ip_address=request.remote_addr
            )
            flash(f"User '{username}' was deleted successfully (0 historical records existed).", 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error deleting user: {str(e)}', 'error')

        return redirect(url_for('manage_users'))

    @app.route('/admin/teams')
    @login_required
    def manage_teams():
        if current_user.role != 'Admin':
            flash('Access denied. Admin privileges required.', 'error')
            return redirect(url_for('dashboard'))
        teams = Team.query.all()
        return render_template('admin/manage_teams.html', teams=teams)

    @app.route('/admin/teams/edit/<int:team_id>', methods=['GET', 'POST'])
    @login_required
    def edit_team(team_id):
        if current_user.role != 'Admin':
            flash('Access denied. Admin privileges required.', 'error')
            return redirect(url_for('dashboard'))

        team = Team.query.get_or_404(team_id)
        if team.team_name not in ['Team 1', 'Team 2', 'Team 3']:
            flash('Only default teams can be edited.', 'error')
            return redirect(url_for('manage_teams'))

        team_leads = User.query.filter_by(role='Team Lead').all()

        if request.method == 'POST':
            lead_id_str = request.form.get('lead_id', '').strip()
            old_lead_id = team.lead_id

            if not lead_id_str:
                # Admin selected "No Team Lead Assigned" / Vacant
                if old_lead_id:
                    old_lead = User.query.get(old_lead_id)
                    if old_lead:
                        old_lead.role = 'Team Member'
                        old_lead.team_id = team_id  # Retain in team!

                team.lead_id = None
                db.session.commit()
                bust_team_lead_cache(team_id)
                if old_lead_id:
                    bust_user_dashboard_cache(old_lead_id)

                log_admin_action(
                    current_user,
                    'VACATE_TEAM_LEAD',
                    team_id,
                    team.team_name,
                    reason="Set to vacant (No lead)",
                    ip_address=request.remote_addr
                )
                flash(f"Team lead unassigned for {team.team_name}.", 'success')
                return redirect(url_for('manage_teams'))

            new_lead_id = int(lead_id_str)
            if new_lead_id != old_lead_id:
                # 1. Preserve former lead as Team Member in the same team
                if old_lead_id:
                    old_lead = User.query.get(old_lead_id)
                    if old_lead:
                        old_lead.role = 'Team Member'
                        old_lead.team_id = team_id  # Retain in team!

                # 2. Clear previous lead pointer if new lead was leading another team
                other_teams = Team.query.filter(Team.lead_id == new_lead_id, Team.team_id != team_id).all()
                for ot in other_teams:
                    ot.lead_id = None

                # 3. Assign new lead to this team
                team.lead_id = new_lead_id
                new_lead = User.query.get(new_lead_id)
                if new_lead:
                    new_lead.role = 'Team Lead'
                    new_lead.team_id = team_id

                db.session.commit()
                bust_team_lead_cache(team_id)
                if old_lead_id:
                    bust_user_dashboard_cache(old_lead_id)
                bust_user_dashboard_cache(new_lead_id)

                log_admin_action(
                    current_user,
                    'ASSIGN_TEAM_LEAD',
                    team_id,
                    team.team_name,
                    reason=f"New Lead: {new_lead.username if new_lead else new_lead_id}",
                    ip_address=request.remote_addr
                )

                flash(f"Team lead updated successfully for {team.team_name}.", 'success')
                return redirect(url_for('manage_teams'))
            else:
                flash("No changes made to team lead.", 'info')
                return redirect(url_for('manage_teams'))

        return render_template('admin/edit_team.html', team=team, team_leads=team_leads)
