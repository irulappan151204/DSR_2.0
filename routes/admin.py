from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from sqlalchemy import text
from extensions import db, bcrypt
from models import User, Team, Action, Issue, Acknowledgement, FileStorage

def register_admin_routes(app):
    """Register user and team admin management routes."""
    @app.route('/admin/users')
    @login_required
    def manage_users():
        if current_user.role != 'Admin':
            flash('Access denied. Admin privileges required.', 'error')
            return redirect(url_for('dashboard'))
        users = User.query.all()
        return render_template('admin/manage_users.html', users=users)

    @app.route('/admin/users/add', methods=['GET', 'POST'])
    @login_required
    def add_user():
        if current_user.role != 'Admin':
            flash('Access denied. Admin privileges required.', 'error')
            return redirect(url_for('dashboard'))

        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            role = request.form.get('role')
            team_id = request.form.get('team_id')

            if User.query.filter_by(username=username).first():
                flash('Username already exists.', 'error')
                return redirect(url_for('add_user'))

            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            new_user = User(
                username=username,
                password=hashed_password,
                role=role,
                team_id=team_id if team_id else None
            )
            db.session.add(new_user)
            db.session.commit()
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
            user.username = request.form.get('username')
            user.role = request.form.get('role')
            team_id = request.form.get('team_id')

            if team_id:
                user.team_id = team_id
            else:
                user.team_id = None

            if 'password' in request.form and request.form['password']:
                user.password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')

            db.session.commit()
            flash('User updated successfully.', 'success')
            return redirect(url_for('manage_users'))

        teams = Team.query.all()
        return render_template('admin/edit_user.html', user=user, teams=teams)

    @app.route('/admin/users/delete/<int:user_id>')
    @login_required
    def delete_user(user_id):
        if current_user.role != 'Admin':
            flash('Access denied. Admin privileges required.', 'error')
            return redirect(url_for('dashboard'))

        user = User.query.get_or_404(user_id)
        if user == current_user:
            flash('Cannot delete your own account.', 'error')
            return redirect(url_for('manage_users'))

        try:
            # 1. Delete all actions assigned to this user
            actions_assigned = Action.query.filter_by(assigned_user_id=user_id).all()
            for action in actions_assigned:
                db.session.delete(action)

            # 2. Delete all actions created by this user
            actions_created = Action.query.filter_by(created_by=user_id).all()
            for action in actions_created:
                db.session.delete(action)

            # 3. Handle issues - set solved_by to None if user resolved any issues
            issues_solved = Issue.query.filter_by(solved_by=user_id).all()
            for issue in issues_solved:
                issue.solved_by = None

            # 4. Delete all issues created by this user
            issues_created = Issue.query.filter_by(created_by_id=user_id).all()
            for issue in issues_created:
                db.session.delete(issue)

            # 5. Handle team lead assignment
            teams_led = Team.query.filter_by(lead_id=user_id).all()
            for team in teams_led:
                team.lead_id = None

            # 6. Delete acknowledgements for this user
            acknowledgements = Acknowledgement.query.filter_by(user_id=user_id).all()
            for ack in acknowledgements:
                db.session.delete(ack)

            # 7. Delete all files uploaded by this user
            uploaded_files = FileStorage.query.filter_by(uploaded_by=user_id).all()
            for file_record in uploaded_files:
                db.session.delete(file_record)

            # 8. Delete dashboard view logs for this user
            try:
                delete_view_logs = text("DELETE FROM dashboard_view_log WHERE user_id = :user_id")
                db.session.execute(delete_view_logs, {'user_id': user_id})
            except Exception as view_log_error:
                print(f"Could not delete dashboard view logs: {str(view_log_error)}")

            # 9. Delete form submissions across all form tables
            form_tables = [
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

            for table_name in form_tables:
                try:
                    delete_query = text(f"DELETE FROM {table_name} WHERE submitted_by = :user_id")
                    db.session.execute(delete_query, {'user_id': user_id})
                except Exception:
                    continue

            db.session.delete(user)
            db.session.commit()
            flash('User deleted successfully.', 'success')
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
            lead_id = request.form.get('lead_id')
            if not lead_id:
                flash('Please select a team lead.', 'error')
                return redirect(url_for('edit_team', team_id=team_id))

            old_lead_id = team.lead_id
            if lead_id != old_lead_id:
                if old_lead_id:
                    old_lead = User.query.get(old_lead_id)
                    if old_lead:
                        old_lead.team_id = None

                team.lead_id = lead_id
                new_lead = User.query.get(lead_id)
                if new_lead:
                    new_lead.team_id = team_id

            db.session.commit()
            flash('Team lead updated successfully.', 'success')
            return redirect(url_for('manage_teams'))

        return render_template('admin/edit_team.html', team=team, team_leads=team_leads)

    @app.route('/create-admin')
    def create_admin():
        admin = User.query.filter_by(username='admin').first()
        if admin:
            return 'Admin already exists'

        admin = User(
            username='admin',
            password=generate_password_hash('admin123'),
            role='Admin'
        )
        try:
            db.session.add(admin)
            db.session.commit()
            return 'Admin user created successfully'
        except Exception as e:
            db.session.rollback()
            return f'Error creating admin: {str(e)}'
