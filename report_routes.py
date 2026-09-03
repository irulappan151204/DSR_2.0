# report_routes.py

from flask import Blueprint, redirect, url_for, flash, render_template
from flask_login import login_required, current_user
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_file, session
from flask_login import UserMixin, login_user, login_required, logout_user, current_user

from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from extensions import db, login_manager, bcrypt, socketio
from flask_migrate import Migrate
from commands import create_admin_command
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from io import BytesIO
from fpdf import FPDF
from statistics_routes import statistics_bp
from md_dashboard import md_dashboard_bp
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from zoneinfo import ZoneInfo
from timezone_utils import ist_day_bounds
from models import BaseForm, User, Team, Issue, Report, Action, Team1CalendarSchedule, Team1StudentAttendance, Team1ParentConcernDetail, Team1ASAActivities, Team1ASASports, Team1ASAGeneral, Team1StudentGrooming, Team1StudentLateComing, Team1AdmissionStatus, Team1TransferCertificate, Team1ParentActivity, Team1ParentVisit, Team1ExamSchedule, Team1ExternalInfo, Team1SickBay, Team1HomeSchoolComm, Team1Disciplinary, Team1Logistics, Team1CompetitionCert, Team1StaffConcern, Team1StudentConcern, Team1ParentConcern, Team1AEPAttendance, Team1ExtendedClassAttendance, Team1TrainingSession, Team1WeeklyMeeting, Team1SpecialEducation, Team1SchoolCounsellor, Team1Scholorius, Team2HRAttendance, Team2AdminAttendance, Team2RecruitmentActivity, Team2PendingRecruitment, Team2RecruitmentPipeline, Team2StaffStatusUpdates, Team2SalaryPending, Team2PoliceVerification, Team2InterviewSchedule, Team2ExitInformation, Team2IssuesStaffConcerns, Team2KuralRecitation, Team2FrontOfficePhoneCalls, Team2VisitorLog, Team2BSNLPhoneStatus, Team2MaterialsInward, Team2MaterialsOutward, Team2MaterialsMovement, Team2ReturnableMaterialTracking, Team2ReturnableGoodsReport, Team2CampusCameraStatus, Team2VehicleCameraStatus, Team2BusACCameraStatus, Team2GPSMonitoring, Team2IssuesIdentifiedMonitoring, Team2IssuesIdentifiedControlRoom,  Team2BiometricsAccessCardPunching, Team2WaterTDSDeviation, Team2TestingCleaning, Team2PoolTesting, Team2WashroomCleanliness, Team2TransportAttendance, Team2ACWorkingStatus, Team2LateReporting, Team2MaintenanceServiceIssues, Team2CarMaintenanceCleaning,  Team2VehicleRenewalsDelays, Team2SpecialTrip, Team2ACTemperatureCheck, Team2LaborEbSolarGenset, Team2Motor, Team2PestControl, Team2ACTempDeviation, Team2ElectricityConsumption, Team2EBDetails, Team2SolarDetails, Team2GensetDetails, Team2CountVerification, Team2AttendanceReplacement, Team2SecurityInfoNote,  Team2SecurityGovtInout, Team2AlcoholTest, Team2SecurityMaterialsInout, Team2SecurityMaterialsOutward, Team2TransportVerification, Team2DocumentsMovement, Team2GovtOfficialDocuments, Team2ThoorigaiTeamSocialMedia, Team2WebsiteUpdates, Team2MDSocialMedia, Team2IntercomMaintenance, Team2HealthCheckUp, Team2NetConnectivityPrintDetails, Team2GeneralMaintenanceITProducts,  Team2CalendarSchedule, Team2TrainingAttendance, Team2TrainingDetails, Team3Audit, Team3NewAudit
import matplotlib.pyplot as plt
import base64
from tempfile import NamedTemporaryFile
from collections import defaultdict
from extensions import db, login_manager, bcrypt, socketio, cache
from cache_utils import per_user_cache_key

report_bp = Blueprint('report', __name__)

@report_bp.route('/generate-report')
@cache.cached(timeout=300, key_prefix=per_user_cache_key)
@login_required
def generate_report():
    if current_user.role not in ['Admin', 'MD']:
        flash('Access denied. Only Admin and MD can generate reports.', 'danger')
        return redirect(url_for('dashboard'))
    
    # Get selected date from query parameters
    selected_date = request.args.get('date', 'all')
    start_date_str = request.args.get('start_date', '')
    end_date_str = request.args.get('end_date', '')
    selected_date_obj = None
    start_date = None
    end_date = None
    defaulted_to_yesterday = False
    if not (start_date_str and end_date_str) and (not selected_date or selected_date == 'all'):
        # If no filter, default to yesterday
        yesterday = (datetime.now() - timedelta(days=1)).date()
        selected_date = yesterday.strftime('%Y-%m-%d')
        defaulted_to_yesterday = True
    if start_date_str and end_date_str:
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        except ValueError:
            start_date = None
            end_date = None
    if selected_date != 'all':
        try:
            selected_date_obj = datetime.strptime(selected_date, '%Y-%m-%d').date()
        except ValueError:
            selected_date = 'all'

    # Helper to build date filter for database queries
    def build_date_filter(model):
        """Return SQLAlchemy filters that respect IST calendar day(s) while
        the DB stores UTC values."""
        filters = []
        if start_date and end_date:
            s_utc, _ = ist_day_bounds(start_date)
            _, e_utc = ist_day_bounds(end_date)
            filters.append(model.submitted_at >= s_utc)
            filters.append(model.submitted_at <= e_utc)
        elif selected_date != 'all' and selected_date_obj:
            s_utc, e_utc = ist_day_bounds(selected_date_obj)
            filters.append(model.submitted_at >= s_utc)
            filters.append(model.submitted_at <= e_utc)
        return filters

    # ------------------------------------------------------------------
    # Action Statistics Calculation
    # ------------------------------------------------------------------
    # Helper function to build date filter for Action model (uses created_at instead of submitted_at)
    def build_action_date_filter():
        """Return SQLAlchemy filters for Action model that respect IST calendar day(s) while
        the DB stores UTC values."""
        filters = []
        if start_date and end_date:
            s_utc, _ = ist_day_bounds(start_date)
            _, e_utc = ist_day_bounds(end_date)
            filters.append(Action.created_at >= s_utc)
            filters.append(Action.created_at <= e_utc)
        elif selected_date != 'all' and selected_date_obj:
            s_utc, e_utc = ist_day_bounds(selected_date_obj)
            filters.append(Action.created_at >= s_utc)
            filters.append(Action.created_at <= e_utc)
        return filters

    # Get all actions with date filter
    action_filters = build_action_date_filter()
    base_action_query = Action.query
    if action_filters:
        base_action_query = base_action_query.filter(*action_filters)
    all_actions = base_action_query.all()

    # Action statistics by status
    action_status_counts = {
        'total_initiated': len(all_actions),
        'solved_completed': len([a for a in all_actions if a.status == 'Finished']),
        'pending': len([a for a in all_actions if a.status == 'Pending']),
        'in_progress': len([a for a in all_actions if a.status == 'In Progress']),
        'follow_up': len([a for a in all_actions if a.parent_action_id is not None])
    }

    # Action statistics by team
    team_action_stats = {}
    team_display_names = {
        'Team 1': 'Academic',
        'Team 2': 'Admin', 
        'Team 3': 'Audit'
    }

    for team in Team.query.all():
        team_users = [u.user_id for u in User.query.filter_by(team_id=team.team_id).all()]
        display_name = team_display_names.get(team.team_name, team.team_name)
        
        # Actions assigned to team members
        team_assigned_actions = [a for a in all_actions if a.assigned_user_id in team_users]
        # Actions created by team members
        team_created_actions = [a for a in all_actions if a.created_by in team_users]
        
        team_action_stats[display_name] = {
            'assigned': len(team_assigned_actions),
            'created': len(team_created_actions),
            'total': len(set(team_assigned_actions + team_created_actions)),
            'completed': len([a for a in team_assigned_actions if a.status == 'Finished']),
            'pending': len([a for a in team_assigned_actions if a.status == 'Pending']),
            'follow_up': len([a for a in team_assigned_actions if a.parent_action_id is not None])
        }

    # Action statistics by individual members
    member_action_stats = []
    for user in User.query.all():
        user_actions = [a for a in all_actions if a.assigned_user_id == user.user_id]
        user_created_actions = [a for a in all_actions if a.created_by == user.user_id]
        
        team_name = user.team.team_name if user.team else 'No Team'
        display_team_name = team_display_names.get(team_name, team_name)
        
        member_action_stats.append({
            'user_id': user.user_id,
            'username': user.username,
            'team': display_team_name,
            'assigned': len(user_actions),
            'created': len(user_created_actions),
            'completed': len([a for a in user_actions if a.status == 'Finished']),
            'pending': len([a for a in user_actions if a.status == 'Pending']),
            'in_progress': len([a for a in user_actions if a.status == 'In Progress']),
            'follow_up': len([a for a in user_actions if a.parent_action_id is not None])
        })

    # Sort member stats by team, then by assigned actions (descending), then by username
    member_action_stats.sort(key=lambda x: (x['team'], -x['assigned'], x['username'].lower()))

    # Action statistics by priority
    priority_stats = {
        'Critical': len([a for a in all_actions if a.priority == 'Critical']),
        'High': len([a for a in all_actions if a.priority == 'High']),
        'Medium': len([a for a in all_actions if a.priority == 'Medium']),
        'Low': len([a for a in all_actions if a.priority == 'Low'])
    }

    # Get issue nature statistics by team and department
    team1_issue_nature = {
        'jr_school': {'all_well': 0, 'manageable': 0, 'critical': 0},
        'sr_school': {'all_well': 0, 'manageable': 0, 'critical': 0},
        'student_attendance_kindergarten': {'all_well': 0, 'manageable': 0, 'critical': 0},
        'student_attendance_grade_1_5': {'all_well': 0, 'manageable': 0, 'critical': 0},
        'student_attendance_grade_6_10': {'all_well': 0, 'manageable': 0, 'critical': 0},
        'student_attendance_grade_11_12': {'all_well': 0, 'manageable': 0, 'critical': 0},
        'student_attendance_overall': {'all_well': 0, 'manageable': 0, 'critical': 0},
        'groom_issue_nature': {'all_well': 0, 'manageable': 0, 'critical': 0},
        'late_coming_issue_nature': {'all_well': 0, 'manageable': 0, 'critical': 0},
        'admission_status_issue_nature': {'all_well': 0, 'manageable': 0, 'critical': 0},
        'admission_status_issue_nature_Bumble_Bee': {'all_well': 0, 'manageable': 0, 'critical': 0},
        'admission_status_issue_nature_Bumble_b_Leeds_Excel': {'all_well': 0, 'manageable': 0, 'critical': 0},
        'tc_issue_nature': {'all_well': 0, 'manageable': 0, 'critical': 0},
        'parent_activity_issue_nature': {'all_well': 0, 'manageable': 0, 'critical': 0},
        'parent_visiting_issue_nature': {'all_well': 0, 'manageable': 0, 'critical': 0},
        'exam_issue_nature_g15': {'all_well': 0, 'manageable': 0, 'critical': 0},
        'exam_issue_nature_g68': {'all_well': 0, 'manageable': 0, 'critical': 0},
        'exam_issue_nature_g910': {'all_well': 0, 'manageable': 0, 'critical': 0},
        'exam_issue_nature_g11': {'all_well': 0, 'manageable': 0, 'critical': 0},
        'exam_issue_nature_g12': {'all_well': 0, 'manageable': 0, 'critical': 0},
        'ext_issue_nature_cis': {'all_well': 0, 'manageable': 0, 'critical': 0},
        'ext_issue_nature_cbse': {'all_well': 0, 'manageable': 0, 'critical': 0},
        'ext_issue_nature_state': {'all_well': 0, 'manageable': 0, 'critical': 0},
        'ext_issue_nature_emis': {'all_well': 0, 'manageable': 0, 'critical': 0},
        'sick_issue_nature': {'all_well': 0, 'manageable': 0, 'critical': 0},
        'home_school_comm_issue_nature': {'all_well': 0, 'manageable': 0, 'critical': 0},
        'disciplinary_issue_nature': {'all_well': 0, 'manageable': 0, 'critical': 0},
        'logistics_issue_nature': {'all_well': 0, 'manageable': 0, 'critical': 0},
        'cert_issue_nature': {'all_well': 0, 'manageable': 0, 'critical': 0},
        'staff_concern_issue_nature': {'all_well': 0, 'manageable': 0, 'critical': 0},
        'student_concern_issue_nature': {'all_well': 0, 'manageable': 0, 'critical': 0},
        'pc_summary_issue_nature': {'all_well': 0, 'manageable': 0, 'critical': 0},
        'pc_detail_issue_nature': {'all_well': 0, 'manageable': 0, 'critical': 0},
        'special_education_issue_nature': {'all_well': 0, 'manageable': 0, 'critical': 0},
        'school_counsellor_issue_nature': {'all_well': 0, 'manageable': 0, 'critical': 0},
        'overall': {'all_well': 0, 'manageable': 0, 'critical': 0}
    }
    
    team2_issue_nature = {
        'jr_school': {'all_well': 0, 'manageable': 0, 'critical': 0},
        'sr_school': {'all_well': 0, 'manageable': 0, 'critical': 0},
        'eca': {'all_well': 0, 'manageable': 0, 'critical': 0}, 
        'admin_staff': {'all_well': 0, 'manageable': 0, 'critical': 0},
        'drivers': {'all_well': 0, 'manageable': 0, 'critical': 0},
        'security': {'all_well': 0, 'manageable': 0, 'critical': 0},
        'housekeeping': {'all_well': 0, 'manageable': 0, 'critical': 0},
        'conductors': {'all_well': 0, 'manageable': 0, 'critical': 0},
        'recruitment_academic': {'all_well': 0, 'manageable': 0, 'critical': 0},
        'recruitment_admin': {'all_well': 0, 'manageable': 0, 'critical': 0},
        'pending_academic': {'all_well': 0, 'manageable': 0, 'critical': 0},
        'pending_admin': {'all_well': 0, 'manageable': 0, 'critical': 0},   
        'interview_schedule': {'all_well': 0, 'manageable': 0, 'critical': 0},
        'exit_information': {'all_well': 0, 'manageable': 0, 'critical': 0},
        'issues_staff_concerns': {'all_well': 0, 'manageable': 0, 'critical': 0},
        'kural_recitation': {'all_well': 0, 'manageable': 0, 'critical': 0},
        'front_office_phone_calls_academics': {'all_well': 0, 'manageable': 0, 'critical': 0},
        'front_office_phone_calls_admin': {'all_well': 0, 'manageable': 0, 'critical': 0},
        'front_office_phone_calls_general': {'all_well': 0, 'manageable': 0, 'critical': 0},
        'visitor_log': {'all_well': 0, 'manageable': 0, 'critical': 0},
        'bsnl_phone_status': {'all_well': 0, 'manageable': 0, 'critical': 0},
        'materials_inward': {'all_well': 0, 'manageable': 0, 'critical': 0},
        'materials_outward': {'all_well': 0, 'manageable': 0, 'critical': 0},
        'materials_movement': {'all_well': 0, 'manageable': 0, 'critical': 0},
        'returnable_material_tracking': {'all_well': 0, 'manageable': 0, 'critical': 0},
        'returnable_goods_report': {'all_well': 0, 'manageable': 0, 'critical': 0},
        'campus_camera_status': {'all_well': 0, 'manageable': 0, 'critical': 0},
        'vehicle_camera_status': {'all_well': 0, 'manageable': 0, 'critical': 0},
        'bus_ac_camera_status': {'all_well': 0, 'manageable': 0, 'critical': 0},
        'gps_monitoring': {'all_well': 0, 'manageable': 0, 'critical': 0},
        'issues_identified_monitoring': {'all_well': 0, 'manageable': 0, 'critical': 0},
        'teachers_late_reporting': {'all_well': 0, 'manageable': 0, 'critical': 0},
        'biometrics_access_card_punching': {'all_well': 0, 'manageable': 0, 'critical': 0},
        'water_tds_deviation': {'all_well': 0, 'manageable': 0, 'critical': 0},
        'testing_cleaning_general': {'all_well': 0, 'manageable': 0, 'critical': 0},
        'testing_cleaning_pool': {'all_well': 0, 'manageable': 0, 'critical': 0},
        'transport_attendance': {'all_well': 0, 'manageable': 0, 'critical': 0},
        'transport_ac_status': {'all_well': 0, 'manageable': 0, 'critical': 0},
        'late_reporting': {'all_well': 0, 'manageable': 0, 'critical': 0},
        'maintenance_service_issues': {'all_well': 0, 'manageable': 0, 'critical': 0},
        'car_maintenance_cleaning': {'all_well': 0, 'manageable': 0, 'critical': 0},
        'vehicle_renewals_delays': {'all_well': 0, 'manageable': 0, 'critical': 0},
        'delayed_halt': {'all_well': 0, 'manageable': 0, 'critical': 0},
        'fc_renewal': {'all_well': 0, 'manageable': 0, 'critical': 0},
        'road_tax': {'all_well': 0, 'manageable': 0, 'critical': 0},
        'permit': {'all_well': 0, 'manageable': 0, 'critical': 0},
        'insurance': {'all_well': 0, 'manageable': 0, 'critical': 0},
        'special_trip': {'all_well': 0, 'manageable': 0, 'critical': 0},
        'ac_temp_first_floor': {'all_well': 0, 'manageable': 0, 'critical': 0},
        'ac_temp_second_floor': {'all_well': 0, 'manageable': 0, 'critical': 0},
        'ac_temp_third_floor': {'all_well': 0, 'manageable': 0, 'critical': 0},
        'ac_temp_ground_floor': {'all_well': 0, 'manageable': 0, 'critical': 0},
        'maintenance_labor': {'all_well': 0, 'manageable': 0, 'critical': 0},
        'motor': {'all_well': 0, 'manageable': 0, 'critical': 0},
        'pest_control': {'all_well': 0, 'manageable': 0, 'critical': 0},
        'ac_temp_deviation': {'all_well': 0, 'manageable': 0, 'critical': 0},
        'electricity_consumption': {'all_well': 0, 'manageable': 0, 'critical': 0},
        'eb_details': {'all_well': 0, 'manageable': 0, 'critical': 0},
        'solar_details': {'all_well': 0, 'manageable': 0, 'critical': 0},
        'genset_details': {'all_well': 0, 'manageable': 0, 'critical': 0},      
        'security_count_verification': {'all_well': 0, 'manageable': 0, 'critical': 0},
        'security_attendance_replacement': {'all_well': 0, 'manageable': 0, 'critical': 0},
        'security_info_note': {'all_well': 0, 'manageable': 0, 'critical': 0},
        'govt_officials_inout': {'all_well': 0, 'manageable': 0, 'critical': 0},
        'security_materials_inward': {'all_well': 0, 'manageable': 0, 'critical': 0},
        'security_materials_outward': {'all_well': 0, 'manageable': 0, 'critical': 0},
        'security_transport_verification': {'all_well': 0, 'manageable': 0, 'critical': 0},
        'documents_movement': {'all_well': 0, 'manageable': 0, 'critical': 0},
        'govt_official_documents': {'all_well': 0, 'manageable': 0, 'critical': 0},
        'digital_marketing_thoorigai_social_media': {'all_well': 0, 'manageable': 0, 'critical': 0},
        'digital_marketing_thoorigai_website_updates': {'all_well': 0, 'manageable': 0, 'critical': 0},
        'digital_marketing_md_social_media': {'all_well': 0, 'manageable': 0, 'critical': 0},
        'intercom_maintenance': {'all_well': 0, 'manageable': 0, 'critical': 0},
        'health_check_up': {'all_well': 0, 'manageable': 0, 'critical': 0},
        'net_connectivity_print_details': {'all_well': 0, 'manageable': 0, 'critical': 0},
        'general_maintenance_it_products': {'all_well': 0, 'manageable': 0, 'critical': 0},
        'calendar_schedule_admin': {'all_well': 0, 'manageable': 0, 'critical': 0},
        'calendar_schedule_house_keeping': {'all_well': 0, 'manageable': 0, 'critical': 0},
        'calendar_schedule_security': {'all_well': 0, 'manageable': 0, 'critical': 0},
        'calendar_schedule_transport': {'all_well': 0, 'manageable': 0, 'critical': 0},
        'training_attendance_academics_jr': {'all_well': 0, 'manageable': 0, 'critical': 0},
        'training_attendance_academics_sr': {'all_well': 0, 'manageable': 0, 'critical': 0},
        'training_attendance_admin': {'all_well': 0, 'manageable': 0, 'critical': 0},
        'training_attendance_drivers': {'all_well': 0, 'manageable': 0, 'critical': 0},
        'training_attendance_securities': {'all_well': 0, 'manageable': 0, 'critical': 0},
        'training_attendance_drivers_sub': {'all_well': 0, 'manageable': 0, 'critical': 0},
        'training_attendance_conductors': {'all_well': 0, 'manageable': 0, 'critical': 0},
        'training_details_cbse_cis_external': {'all_well': 0, 'manageable': 0, 'critical': 0},
        'overall': {'all_well': 0, 'manageable': 0, 'critical': 0}
    }

    team3_issue_nature = {
        'audit_issue_nature': {'all_well': 0, 'manageable': 0, 'critical': 0},
        'new_audit_issue_nature': {'all_well': 0, 'manageable': 0, 'critical': 0},
        'overall': {'all_well': 0, 'manageable': 0, 'critical': 0}
    }


        # Get Team 1 data
    team1 = Team.query.filter_by(team_name='Team 1').first()
    if team1:
         # Get Team 1 Calendar Schedule data
        query_filters = [Team1CalendarSchedule.team_id == team1.team_id] + build_date_filter(Team1CalendarSchedule)
        calendar_data = Team1CalendarSchedule.query.filter(*query_filters).all()

        for item in calendar_data:
            # Process Jr. School data
            if item.cal_issue_nature_jr:
                nature = item.cal_issue_nature_jr.lower()
                if ('all_well' in nature or 'all well' in nature):
                    team1_issue_nature['jr_school']['all_well'] += 1
                    team1_issue_nature['overall']['all_well'] += 1
                elif ('manageable' in nature):
                    team1_issue_nature['jr_school']['manageable'] += 1
                    team1_issue_nature['overall']['manageable'] += 1
                elif ('critical' in nature):
                    team1_issue_nature['jr_school']['critical'] += 1
                    team1_issue_nature['overall']['critical'] += 1
            
            # Process Sr. School data
            if item.cal_issue_nature_sr:
                nature = item.cal_issue_nature_sr.lower()
                if ('all_well' in nature or 'all well' in nature):
                    team1_issue_nature['sr_school']['all_well'] += 1
                    team1_issue_nature['overall']['all_well'] += 1
                elif ('manageable' in nature):
                    team1_issue_nature['sr_school']['manageable'] += 1
                    team1_issue_nature['overall']['manageable'] += 1
                elif ('critical' in nature):
                    team1_issue_nature['sr_school']['critical'] += 1
                    team1_issue_nature['overall']['critical'] += 1

            # Get Team 1 Students Attendance
        # Get Team 1 Students Attendance data
        query_filters = [Team1StudentAttendance.team_id == team1.team_id] + build_date_filter(Team1StudentAttendance)
        student_attendance_data = Team1StudentAttendance.query.filter(*query_filters).all()

        for item in student_attendance_data:
                # Process student_attendance_kindergarten
            if item.att_issue_nature_kg:
                nature = item.att_issue_nature_kg.lower()
                if ('all_well' in nature or 'all well' in nature):
                    team1_issue_nature['student_attendance_kindergarten']['all_well'] += 1
                    team1_issue_nature['overall']['all_well'] += 1
                elif ('manageable' in nature):
                    team1_issue_nature['student_attendance_kindergarten']['manageable'] += 1
                    team1_issue_nature['overall']['manageable'] += 1
                elif ('critical' in nature):
                    team1_issue_nature['student_attendance_kindergarten']['critical'] += 1
                    team1_issue_nature['overall']['critical'] += 1

                # Process student_attendance_grade_1_5
            if item.att_issue_nature_g15:
                nature = item.att_issue_nature_g15.lower()
                if ('all_well' in nature or 'all well' in nature):
                    team1_issue_nature['student_attendance_grade_1_5']['all_well'] += 1
                    team1_issue_nature['overall']['all_well'] += 1
                elif ('manageable' in nature):
                    team1_issue_nature['student_attendance_grade_1_5']['manageable'] += 1
                    team1_issue_nature['overall']['manageable'] += 1
                elif ('critical' in nature):
                    team1_issue_nature['student_attendance_grade_1_5']['critical'] += 1
                    team1_issue_nature['overall']['critical'] += 1

                # Process student_attendance_grade_6_10
            if item.att_issue_nature_g610:
                nature = item.att_issue_nature_g610.lower()
                if ('all_well' in nature or 'all well' in nature):
                    team1_issue_nature['student_attendance_grade_6_10']['all_well'] += 1
                    team1_issue_nature['overall']['all_well'] += 1
                elif ('manageable' in nature):
                    team1_issue_nature['student_attendance_grade_6_10']['manageable'] += 1
                    team1_issue_nature['overall']['manageable'] += 1
                elif ('critical' in nature):
                    team1_issue_nature['student_attendance_grade_6_10']['critical'] += 1
                    team1_issue_nature['overall']['critical'] += 1

                # Process student_attendance_grade_11_12
            if item.att_issue_nature_g1112:
                nature = item.att_issue_nature_g1112.lower()
                if ('all_well' in nature or 'all well' in nature):
                    team1_issue_nature['student_attendance_grade_11_12']['all_well'] += 1
                    team1_issue_nature['overall']['all_well'] += 1
                elif ('manageable' in nature):
                    team1_issue_nature['student_attendance_grade_11_12']['manageable'] += 1
                    team1_issue_nature['overall']['manageable'] += 1
                elif ('critical' in nature):
                    team1_issue_nature['student_attendance_grade_11_12']['critical'] += 1
                    team1_issue_nature['overall']['critical'] += 1

                # Process student_attendance_overall
            if item.att_issue_nature_overall:
                nature = item.att_issue_nature_overall.lower()
                if ('all_well' in nature or 'all well' in nature):
                    team1_issue_nature['student_attendance_overall']['all_well'] += 1
                    team1_issue_nature['overall']['all_well'] += 1
                elif ('manageable' in nature):
                    team1_issue_nature['student_attendance_overall']['manageable'] += 1
                    team1_issue_nature['overall']['manageable'] += 1
                elif ('critical' in nature):
                    team1_issue_nature['student_attendance_overall']['critical'] += 1
                    team1_issue_nature['overall']['critical'] += 1

                
            # Get Team 1 Students Grooming data
        query_filters = [Team1StudentGrooming.team_id == team1.team_id] + build_date_filter(Team1StudentGrooming)
        student_grooming_data = Team1StudentGrooming.query.filter(*query_filters).all()

        for item in student_grooming_data:
                # Process grooming_issue_nature
            if item.grooming_issue_nature:
                nature = item.grooming_issue_nature.lower()
                if ('all_well' in nature or 'all well' in nature):
                    team1_issue_nature['groom_issue_nature']['all_well'] += 1
                    team1_issue_nature['overall']['all_well'] += 1
                elif ('manageable' in nature):
                    team1_issue_nature['groom_issue_nature']['manageable'] += 1
                    team1_issue_nature['overall']['manageable'] += 1
                elif ('critical' in nature):
                    team1_issue_nature['groom_issue_nature']['critical'] += 1
                    team1_issue_nature['overall']['critical'] += 1

                        # Get Team 1 Students Late Coming data
        query_filters = [Team1StudentLateComing.team_id == team1.team_id] + build_date_filter(Team1StudentLateComing)
        student_late_coming_data = Team1StudentLateComing.query.filter(*query_filters).all()
        for item in student_late_coming_data:
                if item.late_coming_issue_nature:
                    nature = item.late_coming_issue_nature.lower()
                    if ('all_well' in nature or 'all well' in nature):
                        team1_issue_nature['late_coming_issue_nature']['all_well'] += 1
                        team1_issue_nature['overall']['all_well'] += 1
                    elif ('manageable' in nature):
                        team1_issue_nature['late_coming_issue_nature']['manageable'] += 1
                        team1_issue_nature['overall']['manageable'] += 1
                    elif ('critical' in nature):
                        team1_issue_nature['late_coming_issue_nature']['critical'] += 1
                        team1_issue_nature['overall']['critical'] += 1

            # Get Team 1 Admission Status data
        query_filters = [Team1AdmissionStatus.team_id == team1.team_id] + build_date_filter(Team1AdmissionStatus)
        admission_status_data = Team1AdmissionStatus.query.filter(*query_filters).all()
        for item in admission_status_data:
                if item.admission_dept_category == 'Adm Status - School' and item.admission_issue_nature:
                    nature = item.admission_issue_nature.lower()
                    if ('all_well' in nature or 'all well' in nature):
                        team1_issue_nature['admission_status_issue_nature']['all_well'] += 1
                        team1_issue_nature['overall']['all_well'] += 1
                    elif ('manageable' in nature):
                        team1_issue_nature['admission_status_issue_nature']['manageable'] += 1
                        team1_issue_nature['overall']['manageable'] += 1
                    elif ('critical' in nature):
                        team1_issue_nature['admission_status_issue_nature']['critical'] += 1
                        team1_issue_nature['overall']['critical'] += 1

                elif item.admission_dept_category == 'Adm. S - Bumble Bee' and item.admission_issue_nature:
                    nature = item.admission_issue_nature.lower()
                    if ('all_well' in nature or 'all well' in nature):
                        team1_issue_nature['admission_status_issue_nature_Bumble_Bee']['all_well'] += 1
                        team1_issue_nature['overall']['all_well'] += 1
                    elif ('manageable' in nature):
                        team1_issue_nature['admission_status_issue_nature_Bumble_Bee']['manageable'] += 1
                        team1_issue_nature['overall']['manageable'] += 1
                    elif ('critical' in nature):
                        team1_issue_nature['admission_status_issue_nature_Bumble_Bee']['critical'] += 1
                        team1_issue_nature['overall']['critical'] += 1

                elif item.admission_dept_category == 'Bumble B Leeds Excel' and item.admission_issue_nature:
                    nature = item.admission_issue_nature.lower()
                    if ('all_well' in nature or 'all well' in nature):
                        team1_issue_nature['admission_status_issue_nature_Bumble_b_Leeds_Excel']['all_well'] += 1
                        team1_issue_nature['overall']['all_well'] += 1
                    elif ('manageable' in nature):
                        team1_issue_nature['admission_status_issue_nature_Bumble_b_Leeds_Excel']['manageable'] += 1
                        team1_issue_nature['overall']['manageable'] += 1
                    elif ('critical' in nature):
                        team1_issue_nature['admission_status_issue_nature_Bumble_b_Leeds_Excel']['critical'] += 1
                        team1_issue_nature['overall']['critical'] += 1

        # Get Team 1 TC data
        query_filters = [Team1TransferCertificate.team_id == team1.team_id] + build_date_filter(Team1TransferCertificate)
        tc_data = Team1TransferCertificate.query.filter(*query_filters).all()

        for item in tc_data:
            if item.transfer_certificate_issue_nature:
                nature = item.transfer_certificate_issue_nature.lower()
                if ('all_well' in nature or 'all well' in nature):
                    team1_issue_nature['tc_issue_nature']['all_well'] += 1
                    team1_issue_nature['overall']['all_well'] += 1
                elif ('manageable' in nature):
                    team1_issue_nature['tc_issue_nature']['manageable'] += 1
                    team1_issue_nature['overall']['manageable'] += 1
                elif ('critical' in nature):
                    team1_issue_nature['tc_issue_nature']['critical'] += 1
                    team1_issue_nature['overall']['critical'] += 1

        # Get Team 1 Parent Activity data
        query_filters = [Team1ParentActivity.team_id == team1.team_id] + build_date_filter(Team1ParentActivity)
        pa_data = Team1ParentActivity.query.filter(*query_filters).all()

        for item in pa_data:
            if item.parent_activity_issue_nature:
                    nature = item.parent_activity_issue_nature.lower()
                    if ('all_well' in nature or 'all well' in nature):
                        team1_issue_nature['parent_activity_issue_nature']['all_well'] += 1
                        team1_issue_nature['overall']['all_well'] += 1
                    elif ('manageable' in nature):
                        team1_issue_nature['parent_activity_issue_nature']['manageable'] += 1
                        team1_issue_nature['overall']['manageable'] += 1
                    elif ('critical' in nature):
                        team1_issue_nature['parent_activity_issue_nature']['critical'] += 1
                        team1_issue_nature['overall']['critical'] += 1

        # Get Team 1 Parent Visit data
        query_filters = [Team1ParentVisit.team_id == team1.team_id] + build_date_filter(Team1ParentVisit)
        pv_data = Team1ParentVisit.query.filter(*query_filters).all()

        for item in pv_data:
            if item.parent_visit_issue_nature:
                nature = item.parent_visit_issue_nature.lower()
                if ('all_well' in nature or 'all well' in nature):
                    team1_issue_nature['parent_visiting_issue_nature']['all_well'] += 1
                    team1_issue_nature['overall']['all_well'] += 1
                elif ('manageable' in nature):
                    team1_issue_nature['parent_visiting_issue_nature']['manageable'] += 1
                    team1_issue_nature['overall']['manageable'] += 1
                elif ('critical' in nature):
                    team1_issue_nature['parent_visiting_issue_nature']['critical'] += 1
                    team1_issue_nature['overall']['critical'] += 1

        # Get Team 1 Exam Schedule data
        query_filters = [Team1ExamSchedule.team_id == team1.team_id] + build_date_filter(Team1ExamSchedule)
        exam_schedule_data = Team1ExamSchedule.query.filter(*query_filters).all()

        for item in exam_schedule_data:
            # process exam_issue_nature_g15
            if item.exam_issue_nature_g15:
                nature = item.exam_issue_nature_g15.lower()
                if ('all_well' in nature or 'all well' in nature):
                    team1_issue_nature['exam_issue_nature_g15']['all_well'] += 1
                    team1_issue_nature['overall']['all_well'] += 1
                elif ('manageable' in nature):
                    team1_issue_nature['exam_issue_nature_g15']['manageable'] += 1
                    team1_issue_nature['overall']['manageable'] += 1
                elif ('critical' in nature):
                    team1_issue_nature['exam_issue_nature_g15']['critical'] += 1
                    team1_issue_nature['overall']['critical'] += 1

            # process exam_issue_nature_g68
            if item.exam_issue_nature_g68:
                nature = item.exam_issue_nature_g68.lower()
                if ('all_well' in nature or 'all well' in nature):
                    team1_issue_nature['exam_issue_nature_g68']['all_well'] += 1
                    team1_issue_nature['overall']['all_well'] += 1
                elif ('manageable' in nature):
                    team1_issue_nature['exam_issue_nature_g68']['manageable'] += 1
                    team1_issue_nature['overall']['manageable'] += 1
                elif ('critical' in nature):
                    team1_issue_nature['exam_issue_nature_g68']['critical'] += 1
                    team1_issue_nature['overall']['critical'] += 1

            # process exam_issue_nature_g910
            if item.exam_issue_nature_g910:
                nature = item.exam_issue_nature_g910.lower()
                if ('all_well' in nature or 'all well' in nature):
                    team1_issue_nature['exam_issue_nature_g910']['all_well'] += 1
                    team1_issue_nature['overall']['all_well'] += 1
                elif ('manageable' in nature):
                    team1_issue_nature['exam_issue_nature_g910']['manageable'] += 1
                    team1_issue_nature['overall']['manageable'] += 1
                elif ('critical' in nature):
                    team1_issue_nature['exam_issue_nature_g910']['critical'] += 1
                    team1_issue_nature['overall']['critical'] += 1

            # process exam_issue_nature_g11
            if item.exam_issue_nature_g11:
                nature = item.exam_issue_nature_g11.lower()
                if ('all_well' in nature or 'all well' in nature):
                    team1_issue_nature['exam_issue_nature_g11']['all_well'] += 1
                    team1_issue_nature['overall']['all_well'] += 1
                elif ('manageable' in nature):
                    team1_issue_nature['exam_issue_nature_g11']['manageable'] += 1
                    team1_issue_nature['overall']['manageable'] += 1
                elif ('critical' in nature):
                    team1_issue_nature['exam_issue_nature_g11']['critical'] += 1
                    team1_issue_nature['overall']['critical'] += 1

            # process exam_issue_nature_g12
            if item.exam_issue_nature_g12:
                nature = item.exam_issue_nature_g12.lower()
                if ('all_well' in nature or 'all well' in nature):
                    team1_issue_nature['exam_issue_nature_g12']['all_well'] += 1
                    team1_issue_nature['overall']['all_well'] += 1
                elif ('manageable' in nature):
                    team1_issue_nature['exam_issue_nature_g12']['manageable'] += 1
                    team1_issue_nature['overall']['manageable'] += 1
                elif ('critical' in nature):
                    team1_issue_nature['exam_issue_nature_g12']['critical'] += 1
                    team1_issue_nature['overall']['critical'] += 1

        # Get Team 1 External Agency Info
        query_filters = [Team1ExternalInfo.team_id == team1.team_id] + build_date_filter(Team1ExternalInfo)
        external_info_entries = Team1ExternalInfo.query.filter(*query_filters).all()

        for item in external_info_entries:
            # process ext_issue_nature_cis
            if item.ext_issue_nature_cis:
                nature = item.ext_issue_nature_cis.lower()
                if ('all_well' in nature or 'all well' in nature):
                    team1_issue_nature['ext_issue_nature_cis']['all_well'] += 1
                    team1_issue_nature['overall']['all_well'] += 1
                elif ('manageable' in nature):
                    team1_issue_nature['ext_issue_nature_cis']['manageable'] += 1
                    team1_issue_nature['overall']['manageable'] += 1
                elif ('critical' in nature):
                    team1_issue_nature['ext_issue_nature_cis']['critical'] += 1
                    team1_issue_nature['overall']['critical'] += 1

            # process ext_issue_nature_cbse
            if item.ext_issue_nature_cbse:
                nature = item.ext_issue_nature_cbse.lower()
                if ('all_well' in nature or 'all well' in nature):
                    team1_issue_nature['ext_issue_nature_cbse']['all_well'] += 1
                    team1_issue_nature['overall']['all_well'] += 1
                elif ('manageable' in nature):
                    team1_issue_nature['ext_issue_nature_cbse']['manageable'] += 1
                    team1_issue_nature['overall']['manageable'] += 1
                elif ('critical' in nature):
                    team1_issue_nature['ext_issue_nature_cbse']['critical'] += 1
                    team1_issue_nature['overall']['critical'] += 1

            # process ext_issue_nature_state
            if item.ext_issue_nature_state:
                nature = item.ext_issue_nature_state.lower()
                if ('all_well' in nature or 'all well' in nature):
                    team1_issue_nature['ext_issue_nature_state']['all_well'] += 1
                    team1_issue_nature['overall']['all_well'] += 1
                elif ('manageable' in nature):
                    team1_issue_nature['ext_issue_nature_state']['manageable'] += 1
                    team1_issue_nature['overall']['manageable'] += 1
                elif ('critical' in nature):
                    team1_issue_nature['ext_issue_nature_state']['critical'] += 1
                    team1_issue_nature['overall']['critical'] += 1

            # process ext_issue_nature_emis
            if item.ext_issue_nature_emis:
                nature = item.ext_issue_nature_emis.lower()
                if ('all_well' in nature or 'all well' in nature):
                    team1_issue_nature['ext_issue_nature_emis']['all_well'] += 1
                    team1_issue_nature['overall']['all_well'] += 1
                elif ('manageable' in nature):
                    team1_issue_nature['ext_issue_nature_emis']['manageable'] += 1
                    team1_issue_nature['overall']['manageable'] += 1
                elif ('critical' in nature):
                    team1_issue_nature['ext_issue_nature_emis']['critical'] += 1
                    team1_issue_nature['overall']['critical'] += 1

        # Get Team 1 sick bay
        query_filters = [Team1SickBay.team_id == team1.team_id] + build_date_filter(Team1SickBay)
        sick_bay_entries = Team1SickBay.query.filter(*query_filters).all()

        for entry in sick_bay_entries:
            if entry.sick_issue_nature:
                nature = entry.sick_issue_nature.lower()
                if ('all_well' in nature or 'all well' in nature):
                    team1_issue_nature['sick_issue_nature']['all_well'] += 1
                    team1_issue_nature['overall']['all_well'] += 1
                elif ('manageable' in nature):
                    team1_issue_nature['sick_issue_nature']['manageable'] += 1
                    team1_issue_nature['overall']['manageable'] += 1
                elif ('critical' in nature):
                    team1_issue_nature['sick_issue_nature']['critical'] += 1
                    team1_issue_nature['overall']['critical'] += 1

        # Get Team 1 home school communication
        query_filters = [Team1HomeSchoolComm.team_id == team1.team_id] + build_date_filter(Team1HomeSchoolComm)
        home_school_comm_entries = Team1HomeSchoolComm.query.filter(*query_filters).all()
        for entry in home_school_comm_entries:
            if entry.hsc_issue_nature:
                nature = entry.hsc_issue_nature.lower()
                if ('all_well' in nature or 'all well' in nature):
                    team1_issue_nature['home_school_comm_issue_nature']['all_well'] += 1
                    team1_issue_nature['overall']['all_well'] += 1
                elif ('manageable' in nature):
                    team1_issue_nature['home_school_comm_issue_nature']['manageable'] += 1
                    team1_issue_nature['overall']['manageable'] += 1
                elif ('critical' in nature):
                    team1_issue_nature['home_school_comm_issue_nature']['critical'] += 1
                    team1_issue_nature['overall']['critical'] += 1

        # Get Team 1 disciplinary measures
        query_filters = [Team1Disciplinary.team_id == team1.team_id] + build_date_filter(Team1Disciplinary)
        disciplinary_entries = Team1Disciplinary.query.filter(*query_filters).all()
        for entry in disciplinary_entries:
            if entry.disc_issue_nature:
                nature = entry.disc_issue_nature.lower()
                if ('all_well' in nature or 'all well' in nature):
                    team1_issue_nature['disciplinary_issue_nature']['all_well'] += 1
                    team1_issue_nature['overall']['all_well'] += 1
                elif ('manageable' in nature):
                    team1_issue_nature['disciplinary_issue_nature']['manageable'] += 1
                    team1_issue_nature['overall']['manageable'] += 1
                elif ('critical' in nature):
                    team1_issue_nature['disciplinary_issue_nature']['critical'] += 1
                    team1_issue_nature['overall']['critical'] += 1

        # Get Team 1 logistics
        query_filters = [Team1Logistics.team_id == team1.team_id] + build_date_filter(Team1Logistics)
        logistics_entries = Team1Logistics.query.filter(*query_filters).all()
        for entry in logistics_entries:
            if entry.log_issue_nature:
                nature = entry.log_issue_nature.lower()
                if ('all_well' in nature or 'all well' in nature):
                    team1_issue_nature['logistics_issue_nature']['all_well'] += 1
                    team1_issue_nature['overall']['all_well'] += 1
                elif ('manageable' in nature):
                    team1_issue_nature['logistics_issue_nature']['manageable'] += 1
                    team1_issue_nature['overall']['manageable'] += 1
                elif ('critical' in nature):
                    team1_issue_nature['logistics_issue_nature']['critical'] += 1
                    team1_issue_nature['overall']['critical'] += 1

        # Get Team 1 Intra Grade Competition Certificate
        query_filters = [Team1CompetitionCert.team_id == team1.team_id] + build_date_filter(Team1CompetitionCert)
        competition_cert_entries = Team1CompetitionCert.query.filter(*query_filters).all()
        for entry in competition_cert_entries:
            if entry.cert_issue_nature:
                nature = entry.cert_issue_nature.lower()
                if ('all_well' in nature or 'all well' in nature):
                    team1_issue_nature['cert_issue_nature']['all_well'] += 1
                    team1_issue_nature['overall']['all_well'] += 1
                elif ('manageable' in nature):
                    team1_issue_nature['cert_issue_nature']['manageable'] += 1
                    team1_issue_nature['overall']['manageable'] += 1
                elif ('critical' in nature):
                    team1_issue_nature['cert_issue_nature']['critical'] += 1
                    team1_issue_nature['overall']['critical'] += 1

        # Get Team 1 staff_concern_issue_nature
        query_filters = [Team1StaffConcern.team_id == team1.team_id] + build_date_filter(Team1StaffConcern)
        staff_concern_entries = Team1StaffConcern.query.filter(*query_filters).all()
        for entry in staff_concern_entries:
            if entry.sc_issue_nature:
                nature = entry.sc_issue_nature.lower()
                if ('all_well' in nature or 'all well' in nature):
                    team1_issue_nature['staff_concern_issue_nature']['all_well'] += 1
                    team1_issue_nature['overall']['all_well'] += 1
                elif ('manageable' in nature):
                    team1_issue_nature['staff_concern_issue_nature']['manageable'] += 1
                    team1_issue_nature['overall']['manageable'] += 1
                elif ('critical' in nature):
                    team1_issue_nature['staff_concern_issue_nature']['critical'] += 1
                    team1_issue_nature['overall']['critical'] += 1

        # Get Team 1 student_concern_issue_nature
        query_filters = [Team1StudentConcern.team_id == team1.team_id] + build_date_filter(Team1StudentConcern)
        student_concern_entries = Team1StudentConcern.query.filter(*query_filters).all()
        for entry in student_concern_entries:
            if entry.st_issue_nature:
                nature = entry.st_issue_nature.lower()
                if ('all_well' in nature or 'all well' in nature):
                    team1_issue_nature['student_concern_issue_nature']['all_well'] += 1
                    team1_issue_nature['overall']['all_well'] += 1
                elif ('manageable' in nature):
                    team1_issue_nature['student_concern_issue_nature']['manageable'] += 1
                    team1_issue_nature['overall']['manageable'] += 1
                elif ('critical' in nature):
                    team1_issue_nature['student_concern_issue_nature']['critical'] += 1
                    team1_issue_nature['overall']['critical'] += 1

        # Get Team 1 Parent Concern Summary
        query_filters = [Team1ParentConcern.team_id == team1.team_id] + build_date_filter(Team1ParentConcern)
        parent_concern_summaries = Team1ParentConcern.query.filter(*query_filters).all()
        for entry in parent_concern_summaries:
            if entry.pc_summary_issue_nature:
                nature = entry.pc_summary_issue_nature.lower()
                if ('all_well' in nature or 'all well' in nature):
                    team1_issue_nature['pc_summary_issue_nature']['all_well'] += 1
                    team1_issue_nature['overall']['all_well'] += 1
                elif ('manageable' in nature):
                    team1_issue_nature['pc_summary_issue_nature']['manageable'] += 1
                    team1_issue_nature['overall']['manageable'] += 1
                elif ('critical' in nature):
                    team1_issue_nature['pc_summary_issue_nature']['critical'] += 1
                    team1_issue_nature['overall']['critical'] += 1

        # Get Team 1 Parent Concern Detail
        query_filters = [Team1ParentConcernDetail.team_id == team1.team_id] + build_date_filter(Team1ParentConcernDetail)
        parent_concern_details = Team1ParentConcernDetail.query.filter(*query_filters).all()
        for entry in parent_concern_details:
            if entry.pc_detail_issue_nature:
                nature = entry.pc_detail_issue_nature.lower()
                if ('all_well' in nature or 'all well' in nature):
                    team1_issue_nature['pc_detail_issue_nature']['all_well'] += 1
                    team1_issue_nature['overall']['all_well'] += 1
                elif ('manageable' in nature):
                    team1_issue_nature['pc_detail_issue_nature']['manageable'] += 1
                    team1_issue_nature['overall']['manageable'] += 1
                elif ('critical' in nature):
                    team1_issue_nature['pc_detail_issue_nature']['critical'] += 1
                    team1_issue_nature['overall']['critical'] += 1

        # Get Team 1 Special Education data
        query_filters = [Team1SpecialEducation.team_id == team1.team_id] + build_date_filter(Team1SpecialEducation)
        special_education_data = Team1SpecialEducation.query.filter(*query_filters).all()
        for item in special_education_data:
            if item.nature_of_issue:
                nature = item.nature_of_issue.lower()
                if ('all_well' in nature or 'all well' in nature):
                    team1_issue_nature['special_education_issue_nature']['all_well'] += 1
                    team1_issue_nature['overall']['all_well'] += 1
                elif ('manageable' in nature):
                    team1_issue_nature['special_education_issue_nature']['manageable'] += 1
                    team1_issue_nature['overall']['manageable'] += 1
                elif ('critical' in nature):
                    team1_issue_nature['special_education_issue_nature']['critical'] += 1
                    team1_issue_nature['overall']['critical'] += 1

        # Get Team 1 School Counsellor data
        query_filters = [Team1SchoolCounsellor.team_id == team1.team_id] + build_date_filter(Team1SchoolCounsellor)
        school_counsellor_data = Team1SchoolCounsellor.query.filter(*query_filters).all()
        for item in school_counsellor_data:
            if item.rapid_nature_of_issues:
                nature = item.rapid_nature_of_issues.lower()
                if ('all_well' in nature or 'all well' in nature):
                    team1_issue_nature['school_counsellor_issue_nature']['all_well'] += 1
                    team1_issue_nature['overall']['all_well'] += 1
                elif ('manageable' in nature):
                    team1_issue_nature['school_counsellor_issue_nature']['manageable'] += 1
                    team1_issue_nature['overall']['manageable'] += 1
                elif ('critical' in nature):
                    team1_issue_nature['school_counsellor_issue_nature']['critical'] += 1
                    team1_issue_nature['overall']['critical'] += 1
    
           
            
    # Get Team 2 data
    team2 = Team.query.filter_by(team_name='Team 2').first()
    if team2:
        # Get Team 2 HR Attendance data
        query_filters = [Team2HRAttendance.team_id == team2.team_id] + build_date_filter(Team2HRAttendance)
        hr_data = Team2HRAttendance.query.filter(*query_filters).all()
        
        for item in hr_data:
            # Process Jr. School data
            if item.hr_att_jr_school_nature:
                nature = item.hr_att_jr_school_nature.lower()
                if ('all_well' in nature or 'all well' in nature):
                    team2_issue_nature['jr_school']['all_well'] += 1
                    team2_issue_nature['overall']['all_well'] += 1
                elif ('manageable' in nature):
                    team2_issue_nature['jr_school']['manageable'] += 1
                    team2_issue_nature['overall']['manageable'] += 1
                elif ('critical' in nature):
                    team2_issue_nature['jr_school']['critical'] += 1
                    team2_issue_nature['overall']['critical'] += 1
            
            # Process Sr. School data
            if item.hr_att_sr_school_nature:
                nature = item.hr_att_sr_school_nature.lower()
                if ('all_well' in nature or 'all well' in nature):
                    team2_issue_nature['sr_school']['all_well'] += 1
                    team2_issue_nature['overall']['all_well'] += 1
                elif ('manageable' in nature):
                    team2_issue_nature['sr_school']['manageable'] += 1
                    team2_issue_nature['overall']['manageable'] += 1
                elif ('critical' in nature):
                    team2_issue_nature['sr_school']['critical'] += 1
                    team2_issue_nature['overall']['critical'] += 1
            
            # Process ECA data
            if item.hr_att_eca_nature:
                nature = item.hr_att_eca_nature.lower()
                if ('all_well' in nature or 'all well' in nature):
                    team2_issue_nature['eca']['all_well'] += 1
                    team2_issue_nature['overall']['all_well'] += 1
                elif ('manageable' in nature):
                    team2_issue_nature['eca']['manageable'] += 1
                    team2_issue_nature['overall']['manageable'] += 1
                elif ('critical' in nature):
                    team2_issue_nature['eca']['critical'] += 1
                    team2_issue_nature['overall']['critical'] += 1
        
        # Get Team 2 Admin Attendance data
        query_filters = [Team2AdminAttendance.team_id == team2.team_id] + build_date_filter(Team2AdminAttendance)
        admin_data = Team2AdminAttendance.query.filter(*query_filters).all()
        
        for item in admin_data:
            # Process Admin Staff data
            if item.hr_att_admin_nature:
                nature = item.hr_att_admin_nature.lower()
                if ('all_well' in nature or 'all well' in nature):
                    team2_issue_nature['admin_staff']['all_well'] += 1
                    team2_issue_nature['overall']['all_well'] += 1
                elif ('manageable' in nature):
                    team2_issue_nature['admin_staff']['manageable'] += 1
                    team2_issue_nature['overall']['manageable'] += 1
                elif ('critical' in nature):
                    team2_issue_nature['admin_staff']['critical'] += 1
                    team2_issue_nature['overall']['critical'] += 1
            
            # Process Drivers data
            if item.hr_att_drivers_nature:
                nature = item.hr_att_drivers_nature.lower()
                if ('all_well' in nature or 'all well' in nature):
                    team2_issue_nature['drivers']['all_well'] += 1
                    team2_issue_nature['overall']['all_well'] += 1
                elif ('manageable' in nature):
                    team2_issue_nature['drivers']['manageable'] += 1
                    team2_issue_nature['overall']['manageable'] += 1
                elif ('critical' in nature):
                    team2_issue_nature['drivers']['critical'] += 1
                    team2_issue_nature['overall']['critical'] += 1
            
            # Process Security data
            if item.hr_att_sec_nature:
                nature = item.hr_att_sec_nature.lower()
                if ('all_well' in nature or 'all well' in nature):
                    team2_issue_nature['security']['all_well'] += 1
                    team2_issue_nature['overall']['all_well'] += 1
                elif ('manageable' in nature):
                    team2_issue_nature['security']['manageable'] += 1
                    team2_issue_nature['overall']['manageable'] += 1
                elif ('critical' in nature):
                    team2_issue_nature['security']['critical'] += 1
                    team2_issue_nature['overall']['critical'] += 1
            
            # Process Housekeeping data
            if item.hr_att_hk_nature:
                nature = item.hr_att_hk_nature.lower()
                if ('all_well' in nature or 'all well' in nature):
                    team2_issue_nature['housekeeping']['all_well'] += 1
                    team2_issue_nature['overall']['all_well'] += 1
                elif ('manageable' in nature):
                    team2_issue_nature['housekeeping']['manageable'] += 1
                    team2_issue_nature['overall']['manageable'] += 1
                elif ('critical' in nature):
                    team2_issue_nature['housekeeping']['critical'] += 1
                    team2_issue_nature['overall']['critical'] += 1
            
            # Process Conductors data
            if item.hr_att_cond_nature:
                nature = item.hr_att_cond_nature.lower()
                if ('all_well' in nature or 'all well' in nature):
                    team2_issue_nature['conductors']['all_well'] += 1
                    team2_issue_nature['overall']['all_well'] += 1
                elif ('manageable' in nature):
                    team2_issue_nature['conductors']['manageable'] += 1
                    team2_issue_nature['overall']['manageable'] += 1
                elif ('critical' in nature):
                    team2_issue_nature['conductors']['critical'] += 1
                    team2_issue_nature['overall']['critical'] += 1

    # Get Team 2 Recruitment Activity data
    query_filters = [Team2RecruitmentActivity.team_id == team2.team_id] + build_date_filter(Team2RecruitmentActivity)
    rec_data = Team2RecruitmentActivity.query.filter(*query_filters).all()
    
    for item in rec_data:
        # Process Academic Recruitment data
        if item.rec_act_acad_nature:
            nature = item.rec_act_acad_nature.lower()
            if ('all_well' in nature or 'all well' in nature):
                team2_issue_nature['recruitment_academic']['all_well'] += 1
                team2_issue_nature['overall']['all_well'] += 1
            elif ('manageable' in nature):
                team2_issue_nature['recruitment_academic']['manageable'] += 1
                team2_issue_nature['overall']['manageable'] += 1
            elif ('critical' in nature):
                team2_issue_nature['recruitment_academic']['critical'] += 1
                team2_issue_nature['overall']['critical'] += 1
        
        # Process Admin Recruitment data
        if item.rec_act_admin_nature:
            nature = item.rec_act_admin_nature.lower()
            if ('all_well' in nature or 'all well' in nature):
                team2_issue_nature['recruitment_admin']['all_well'] += 1
                team2_issue_nature['overall']['all_well'] += 1
            elif ('manageable' in nature):
                team2_issue_nature['recruitment_admin']['manageable'] += 1
                team2_issue_nature['overall']['manageable'] += 1
            elif ('critical' in nature):
                team2_issue_nature['recruitment_admin']['critical'] += 1
                team2_issue_nature['overall']['critical'] += 1

    # Get Team 2 Pending Recruitment data
    query_filters = [Team2PendingRecruitment.team_id == team2.team_id] + build_date_filter(Team2PendingRecruitment)
    pending_data = Team2PendingRecruitment.query.filter(*query_filters).all()
    
    for item in pending_data:
        # Process Academic Pending data
        if item.rec_pend_acad_nature:
            nature = item.rec_pend_acad_nature.lower()
            if ('all_well' in nature or 'all well' in nature):
                team2_issue_nature['pending_academic']['all_well'] += 1
                team2_issue_nature['overall']['all_well'] += 1
            elif ('manageable' in nature):
                team2_issue_nature['pending_academic']['manageable'] += 1
                team2_issue_nature['overall']['manageable'] += 1
            elif ('critical' in nature):
                team2_issue_nature['pending_academic']['critical'] += 1
                team2_issue_nature['overall']['critical'] += 1
        
        # Process Admin Pending data
        if item.rec_pend_admin_nature:
            nature = item.rec_pend_admin_nature.lower()
            if ('all_well' in nature or 'all well' in nature):
                team2_issue_nature['pending_admin']['all_well'] += 1
                team2_issue_nature['overall']['all_well'] += 1
            elif ('manageable' in nature):
                team2_issue_nature['pending_admin']['manageable'] += 1
                team2_issue_nature['overall']['manageable'] += 1
            elif ('critical' in nature):
                team2_issue_nature['pending_admin']['critical'] += 1
                team2_issue_nature['overall']['critical'] += 1

    # Get Team 2 Interview Schedule data
    query_filters = [Team2InterviewSchedule.team_id == team2.team_id] + build_date_filter(Team2InterviewSchedule)
    interview_data = Team2InterviewSchedule.query.filter(*query_filters).all()
    
    for item in interview_data:
        # Process Interview Schedule data - using the correct field name
        if item.nature_of_issue:
            nature = item.nature_of_issue.lower()
            if ('all_well' in nature or 'all well' in nature):
                team2_issue_nature['interview_schedule']['all_well'] += 1
                team2_issue_nature['overall']['all_well'] += 1
            elif ('manageable' in nature):
                team2_issue_nature['interview_schedule']['manageable'] += 1
                team2_issue_nature['overall']['manageable'] += 1
            elif ('critical' in nature):
                team2_issue_nature['interview_schedule']['critical'] += 1
                team2_issue_nature['overall']['critical'] += 1  

     # Get Team 2  Exit Information data
    query_filters = [Team2ExitInformation.team_id == team2.team_id] + build_date_filter(Team2ExitInformation)
    exit_information_data = Team2ExitInformation.query.filter(*query_filters).all()
    
    for item in exit_information_data:
        # Process Exit Information data - using the correct field name
        if item.exit_nature:
            nature = item.exit_nature.lower()
            if ('all_well' in nature or 'all well' in nature):
                team2_issue_nature['exit_information']['all_well'] += 1
                team2_issue_nature['overall']['all_well'] += 1
            elif ('manageable' in nature):
                team2_issue_nature['exit_information']['manageable'] += 1
                team2_issue_nature['overall']['manageable'] += 1
            elif ('critical' in nature):
                team2_issue_nature['exit_information']['critical'] += 1
                team2_issue_nature['overall']['critical'] += 1

    # Get Team 2  5a Issues / Staff Concerns
    query_filters = [Team2IssuesStaffConcerns.team_id == team2.team_id] + build_date_filter(Team2IssuesStaffConcerns)
    issues_staff_concerns_data = Team2IssuesStaffConcerns.query.filter(*query_filters).all()

    for item in issues_staff_concerns_data:
        # Single concern nature field in current schema
        if item.concern_nature:
            nature = item.concern_nature.lower()
            if ('all_well' in nature or 'all well' in nature):
                team2_issue_nature['issues_staff_concerns']['all_well'] += 1
                team2_issue_nature['overall']['all_well'] += 1
            elif ('manageable' in nature):
                team2_issue_nature['issues_staff_concerns']['manageable'] += 1
                team2_issue_nature['overall']['manageable'] += 1
            elif ('critical' in nature):
                team2_issue_nature['issues_staff_concerns']['critical'] += 1
                team2_issue_nature['overall']['critical'] += 1

    # Process Kural Recitation data
    query_filters = [Team2KuralRecitation.team_id == team2.team_id] + build_date_filter(Team2KuralRecitation)
    kural_recitation_data = Team2KuralRecitation.query.filter(*query_filters).all()

    for item in kural_recitation_data:
        if item.kural_nature:
            nature = item.kural_nature.lower()
            if ('all_well' in nature or 'all well' in nature):
                team2_issue_nature['kural_recitation']['all_well'] += 1
                team2_issue_nature['overall']['all_well'] += 1
            elif ('manageable' in nature):
                team2_issue_nature['kural_recitation']['manageable'] += 1
                team2_issue_nature['overall']['manageable'] += 1
            elif ('critical' in nature):
                team2_issue_nature['kural_recitation']['critical'] += 1
                team2_issue_nature['overall']['critical'] += 1

    # Get Team 2- 6 


    # Process Front Office Phone Calls data
    query_filters = [Team2FrontOfficePhoneCalls.team_id == team2.team_id] + build_date_filter(Team2FrontOfficePhoneCalls)
    front_office_phone_calls_data = Team2FrontOfficePhoneCalls.query.filter(*query_filters).all()

    for item in front_office_phone_calls_data:
        if item.nature:
            nature = item.nature.lower()
            category = item.category.lower()
            if ('all_well' in nature or 'all well' in nature):
                team2_issue_nature[f'front_office_phone_calls_{category}']['all_well'] += 1
                team2_issue_nature['overall']['all_well'] += 1
            elif ('manageable' in nature):
                team2_issue_nature[f'front_office_phone_calls_{category}']['manageable'] += 1
                team2_issue_nature['overall']['manageable'] += 1
            elif ('critical' in nature):
                team2_issue_nature[f'front_office_phone_calls_{category}']['critical'] += 1
                team2_issue_nature['overall']['critical'] += 1

    # Process Visitor Log data
    query_filters = [Team2VisitorLog.team_id == team2.team_id] + build_date_filter(Team2VisitorLog)
    visitor_log_data = Team2VisitorLog.query.filter(*query_filters).all()

    for item in visitor_log_data:
        if item.nature:
            nature = item.nature.lower()
            if ('all_well' in nature or 'all well' in nature):
                team2_issue_nature['visitor_log']['all_well'] += 1
                team2_issue_nature['overall']['all_well'] += 1
            elif ('manageable' in nature):
                team2_issue_nature['visitor_log']['manageable'] += 1
                team2_issue_nature['overall']['manageable'] += 1
            elif ('critical' in nature):
                team2_issue_nature['visitor_log']['critical'] += 1
                team2_issue_nature['overall']['critical'] += 1

    # Process BSNL Phone Status data
    query_filters = [Team2BSNLPhoneStatus.team_id == team2.team_id] + build_date_filter(Team2BSNLPhoneStatus)
    bsnl_phone_status_data = Team2BSNLPhoneStatus.query.filter(*query_filters).all()

    for item in bsnl_phone_status_data:
        if item.nature:
            nature = item.nature.lower()
            if ('all_well' in nature or 'all well' in nature):
                team2_issue_nature['bsnl_phone_status']['all_well'] += 1
                team2_issue_nature['overall']['all_well'] += 1
            elif ('manageable' in nature):
                team2_issue_nature['bsnl_phone_status']['manageable'] += 1
                team2_issue_nature['overall']['manageable'] += 1
            elif ('critical' in nature):
                team2_issue_nature['bsnl_phone_status']['critical'] += 1
                team2_issue_nature['overall']['critical'] += 1


        # team 2 7
    # Process Materials Inward data
    query_filters = [Team2MaterialsInward.team_id == team2.team_id] + build_date_filter(Team2MaterialsInward)
    materials_inward_data = Team2MaterialsInward.query.filter(*query_filters).all()

    for item in materials_inward_data:
        if item.nature:
            nature = item.nature.lower()
            if ('all_well' in nature or 'all well' in nature):
                team2_issue_nature['materials_inward']['all_well'] += 1
                team2_issue_nature['overall']['all_well'] += 1
            elif ('manageable' in nature):
                team2_issue_nature['materials_inward']['manageable'] += 1
                team2_issue_nature['overall']['manageable'] += 1
            elif ('critical' in nature):
                team2_issue_nature['materials_inward']['critical'] += 1
                team2_issue_nature['overall']['critical'] += 1

    # Process Materials Outward data
    query_filters = [Team2MaterialsOutward.team_id == team2.team_id] + build_date_filter(Team2MaterialsOutward)
    materials_outward_data = Team2MaterialsOutward.query.filter(*query_filters).all()

    for item in materials_outward_data:
        if item.nature:
            nature = item.nature.lower()
            if ('all_well' in nature or 'all well' in nature):
                team2_issue_nature['materials_outward']['all_well'] += 1
                team2_issue_nature['overall']['all_well'] += 1
            elif ('manageable' in nature):
                team2_issue_nature['materials_outward']['manageable'] += 1
                team2_issue_nature['overall']['manageable'] += 1
            elif ('critical' in nature):
                team2_issue_nature['materials_outward']['critical'] += 1
                team2_issue_nature['overall']['critical'] += 1

    # Process Materials Movement data
    query_filters = [Team2MaterialsMovement.team_id == team2.team_id] + build_date_filter(Team2MaterialsMovement)
    materials_movement_data = Team2MaterialsMovement.query.filter(*query_filters).all()

    for item in materials_movement_data:
        if item.nature:
            nature = item.nature.lower()
            if ('all_well' in nature or 'all well' in nature):
                team2_issue_nature['materials_movement']['all_well'] += 1
                team2_issue_nature['overall']['all_well'] += 1
            elif ('manageable' in nature):
                team2_issue_nature['materials_movement']['manageable'] += 1
                team2_issue_nature['overall']['manageable'] += 1
            elif ('critical' in nature):
                team2_issue_nature['materials_movement']['critical'] += 1
                team2_issue_nature['overall']['critical'] += 1

    # Process Returnable Material Tracking data
    query_filters = [Team2ReturnableMaterialTracking.team_id == team2.team_id] + build_date_filter(Team2ReturnableMaterialTracking)
    returnable_material_tracking_data = Team2ReturnableMaterialTracking.query.filter(*query_filters).all()

    for item in returnable_material_tracking_data:
        if item.nature:
            nature = item.nature.lower()
            if ('all_well' in nature or 'all well' in nature):
                team2_issue_nature['returnable_material_tracking']['all_well'] += 1
                team2_issue_nature['overall']['all_well'] += 1
            elif ('manageable' in nature):
                team2_issue_nature['returnable_material_tracking']['manageable'] += 1
                team2_issue_nature['overall']['manageable'] += 1
            elif ('critical' in nature):
                team2_issue_nature['returnable_material_tracking']['critical'] += 1
                team2_issue_nature['overall']['critical'] += 1

    # Process Returnable Goods Report data
    query_filters = [Team2ReturnableGoodsReport.team_id == team2.team_id] + build_date_filter(Team2ReturnableGoodsReport)
    returnable_goods_report_data = Team2ReturnableGoodsReport.query.filter(*query_filters).all()

    for item in returnable_goods_report_data:
        if item.nature:
            nature = item.nature.lower()
            if ('all_well' in nature or 'all well' in nature):
                team2_issue_nature['returnable_goods_report']['all_well'] += 1
                team2_issue_nature['overall']['all_well'] += 1
            elif ('manageable' in nature):
                team2_issue_nature['returnable_goods_report']['manageable'] += 1
                team2_issue_nature['overall']['manageable'] += 1
            elif ('critical' in nature):
                team2_issue_nature['returnable_goods_report']['critical'] += 1
                team2_issue_nature['overall']['critical'] += 1

                # team 2 8
    # Process Campus Camera Status data
    query_filters = [Team2CampusCameraStatus.team_id == team2.team_id] + build_date_filter(Team2CampusCameraStatus)
    campus_camera_status_data = Team2CampusCameraStatus.query.filter(*query_filters).all()

    for item in campus_camera_status_data:
        if item.nature_of_issue:
            nature = item.nature_of_issue.lower()
            if ('all_well' in nature or 'all well' in nature):
                team2_issue_nature['campus_camera_status']['all_well'] += 1
                team2_issue_nature['overall']['all_well'] += 1
            elif ('manageable' in nature):
                team2_issue_nature['campus_camera_status']['manageable'] += 1
                team2_issue_nature['overall']['manageable'] += 1
            elif ('critical' in nature):
                team2_issue_nature['campus_camera_status']['critical'] += 1
                team2_issue_nature['overall']['critical'] += 1

    # Process Vehicle Camera Status data
    query_filters = [Team2VehicleCameraStatus.team_id == team2.team_id] + build_date_filter(Team2VehicleCameraStatus)
    vehicle_camera_status_data = Team2VehicleCameraStatus.query.filter(*query_filters).all()

    for item in vehicle_camera_status_data:
        if item.nature_of_issue:
            nature = item.nature_of_issue.lower()
            if ('all_well' in nature or 'all well' in nature):
                team2_issue_nature['vehicle_camera_status']['all_well'] += 1
                team2_issue_nature['overall']['all_well'] += 1
            elif ('manageable' in nature):
                team2_issue_nature['vehicle_camera_status']['manageable'] += 1
                team2_issue_nature['overall']['manageable'] += 1
            elif ('critical' in nature):
                team2_issue_nature['vehicle_camera_status']['critical'] += 1
                team2_issue_nature['overall']['critical'] += 1

    # Process Bus AC Camera Status data
    query_filters = [Team2BusACCameraStatus.team_id == team2.team_id] + build_date_filter(Team2BusACCameraStatus)
    bus_ac_camera_status_data = Team2BusACCameraStatus.query.filter(*query_filters).all()

    for item in bus_ac_camera_status_data:
        if item.nature_of_issue:
            nature = item.nature_of_issue.lower()
            if ('all_well' in nature or 'all well' in nature):
                team2_issue_nature['bus_ac_camera_status']['all_well'] += 1
                team2_issue_nature['overall']['all_well'] += 1
            elif ('manageable' in nature):
                team2_issue_nature['bus_ac_camera_status']['manageable'] += 1
                team2_issue_nature['overall']['manageable'] += 1
            elif ('critical' in nature):
                team2_issue_nature['bus_ac_camera_status']['critical'] += 1
                team2_issue_nature['overall']['critical'] += 1

    # Process GPS Monitoring data
    query_filters = [Team2GPSMonitoring.team_id == team2.team_id] + build_date_filter(Team2GPSMonitoring)
    gps_monitoring_data = Team2GPSMonitoring.query.filter(*query_filters).all()

    for item in gps_monitoring_data:
        if item.nature_of_issue:
            nature = item.nature_of_issue.lower()
            if ('all_well' in nature or 'all well' in nature):
                team2_issue_nature['gps_monitoring']['all_well'] += 1
                team2_issue_nature['overall']['all_well'] += 1
            elif ('manageable' in nature):
                team2_issue_nature['gps_monitoring']['manageable'] += 1
                team2_issue_nature['overall']['manageable'] += 1
            elif ('critical' in nature):
                team2_issue_nature['gps_monitoring']['critical'] += 1
                team2_issue_nature['overall']['critical'] += 1

    # Process Issues Identified Monitoring data
    query_filters = [Team2IssuesIdentifiedMonitoring.team_id == team2.team_id] + build_date_filter(Team2IssuesIdentifiedMonitoring)
    issues_identified_monitoring_data = Team2IssuesIdentifiedMonitoring.query.filter(*query_filters).all()

    for item in issues_identified_monitoring_data:
        if item.nature_of_issue:
            nature = item.nature_of_issue.lower()
            if ('all_well' in nature or 'all well' in nature):
                team2_issue_nature['issues_identified_monitoring']['all_well'] += 1
                team2_issue_nature['overall']['all_well'] += 1
            elif ('manageable' in nature):
                team2_issue_nature['issues_identified_monitoring']['manageable'] += 1
                team2_issue_nature['overall']['manageable'] += 1
            elif ('critical' in nature):
                team2_issue_nature['issues_identified_monitoring']['critical'] += 1
                team2_issue_nature['overall']['critical'] += 1

    # Process Teachers Late Reporting data
    query_filters = [Team2IssuesIdentifiedControlRoom.team_id == team2.team_id] + build_date_filter(Team2IssuesIdentifiedControlRoom)
    teachers_late_reporting_data = Team2IssuesIdentifiedControlRoom.query.filter(*query_filters).all()

    for item in teachers_late_reporting_data:
        if item.nature_of_issue:
            nature = item.nature_of_issue.lower()
            if ('all_well' in nature or 'all well' in nature):
                team2_issue_nature['teachers_late_reporting']['all_well'] += 1
                team2_issue_nature['overall']['all_well'] += 1
            elif ('manageable' in nature):
                team2_issue_nature['teachers_late_reporting']['manageable'] += 1
                team2_issue_nature['overall']['manageable'] += 1
            elif ('critical' in nature):
                team2_issue_nature['teachers_late_reporting']['critical'] += 1
                team2_issue_nature['overall']['critical'] += 1

    # Process Biometrics Access Card Punching data
    query_filters = [Team2BiometricsAccessCardPunching.team_id == team2.team_id] + build_date_filter(Team2BiometricsAccessCardPunching)
    biometrics_data = Team2BiometricsAccessCardPunching.query.filter(*query_filters).all()

    for item in biometrics_data:
        if item.nature_of_issue:
            nature = item.nature_of_issue.lower()
            if ('all_well' in nature or 'all well' in nature):
                team2_issue_nature['biometrics_access_card_punching']['all_well'] += 1
                team2_issue_nature['overall']['all_well'] += 1
            elif ('manageable' in nature):
                team2_issue_nature['biometrics_access_card_punching']['manageable'] += 1
                team2_issue_nature['overall']['manageable'] += 1
            elif ('critical' in nature):
                team2_issue_nature['biometrics_access_card_punching']['critical'] += 1
                team2_issue_nature['overall']['critical'] += 1

    # Process Water TDS Deviation data
    query_filters = [Team2WaterTDSDeviation.team_id == team2.team_id] + build_date_filter(Team2WaterTDSDeviation)
    water_tds_data = Team2WaterTDSDeviation.query.filter(*query_filters).all()

    for item in water_tds_data:
        if item.nature_of_issue:
            nature = item.nature_of_issue.lower()
            if ('all_well' in nature or 'all well' in nature):
                team2_issue_nature['water_tds_deviation']['all_well'] += 1
                team2_issue_nature['overall']['all_well'] += 1
            elif ('manageable' in nature):
                team2_issue_nature['water_tds_deviation']['manageable'] += 1
                team2_issue_nature['overall']['manageable'] += 1
            elif ('critical' in nature):
                team2_issue_nature['water_tds_deviation']['critical'] += 1
                team2_issue_nature['overall']['critical'] += 1

    # Process Testing & Cleaning data
    query_filters = [Team2TestingCleaning.team_id == team2.team_id] + build_date_filter(Team2TestingCleaning)
    testing_cleaning_data = Team2TestingCleaning.query.filter(*query_filters).all()

    for item in testing_cleaning_data:
        if item.nature_of_issue:
            nature = item.nature_of_issue.lower()
            if ('all_well' in nature or 'all well' in nature):
                team2_issue_nature['testing_cleaning_general']['all_well'] += 1
                team2_issue_nature['overall']['all_well'] += 1
            elif ('manageable' in nature):
                team2_issue_nature['testing_cleaning_general']['manageable'] += 1
                team2_issue_nature['overall']['manageable'] += 1
            elif ('critical' in nature):
                team2_issue_nature['testing_cleaning_general']['critical'] += 1
                team2_issue_nature['overall']['critical'] += 1

    # Process Pool Testing data
    query_filters = [Team2PoolTesting.team_id == team2.team_id] + build_date_filter(Team2PoolTesting)
    pool_testing_data = Team2PoolTesting.query.filter(*query_filters).all()

    for item in pool_testing_data:
        if item.nature_of_issue:
            nature = item.nature_of_issue.lower()
            if ('all_well' in nature or 'all well' in nature):
                team2_issue_nature['testing_cleaning_pool']['all_well'] += 1
                team2_issue_nature['overall']['all_well'] += 1
            elif ('manageable' in nature):
                team2_issue_nature['testing_cleaning_pool']['manageable'] += 1
                team2_issue_nature['overall']['manageable'] += 1
            elif ('critical' in nature):
                team2_issue_nature['testing_cleaning_pool']['critical'] += 1
                team2_issue_nature['overall']['critical'] += 1

    # Team 2 - Section 13: Transport (12 sub-sections)
    # 1. Transport Attendance
    query_filters = [Team2TransportAttendance.team_id == team2.team_id] + build_date_filter(Team2TransportAttendance)
    attendance_data = Team2TransportAttendance.query.filter(*query_filters).all()
    for item in attendance_data:
        if item.nature_of_issue:
            nature = item.nature_of_issue.lower()
            if ('all_well' in nature or 'all well' in nature):
                team2_issue_nature['transport_attendance']['all_well'] += 1
                team2_issue_nature['overall']['all_well'] += 1
            elif ('manageable' in nature):
                team2_issue_nature['transport_attendance']['manageable'] += 1
                team2_issue_nature['overall']['manageable'] += 1
            elif ('critical' in nature):
                team2_issue_nature['transport_attendance']['critical'] += 1
                team2_issue_nature['overall']['critical'] += 1

    # 2. Transport AC Status
    query_filters = [Team2ACWorkingStatus.team_id == team2.team_id] + build_date_filter(Team2ACWorkingStatus)
    ac_status_data = Team2ACWorkingStatus.query.filter(*query_filters).all()
    for item in ac_status_data:
        if item.nature_of_issue:
            nature = item.nature_of_issue.lower()
            if ('all_well' in nature or 'all well' in nature):
                team2_issue_nature['transport_ac_status']['all_well'] += 1
                team2_issue_nature['overall']['all_well'] += 1
            elif ('manageable' in nature):
                team2_issue_nature['transport_ac_status']['manageable'] += 1
                team2_issue_nature['overall']['manageable'] += 1
            elif ('critical' in nature):
                team2_issue_nature['transport_ac_status']['critical'] += 1
                team2_issue_nature['overall']['critical'] += 1

    # 3. Late Reporting
    query_filters = [Team2LateReporting.team_id == team2.team_id] + build_date_filter(Team2LateReporting)
    late_reporting_data = Team2LateReporting.query.filter(*query_filters).all()
    for item in late_reporting_data:
        if item.nature_of_issue:
            nature = item.nature_of_issue.lower()
            if ('all_well' in nature or 'all well' in nature):
                team2_issue_nature['late_reporting']['all_well'] += 1
                team2_issue_nature['overall']['all_well'] += 1
            elif ('manageable' in nature):
                team2_issue_nature['late_reporting']['manageable'] += 1
                team2_issue_nature['overall']['manageable'] += 1
            elif ('critical' in nature):
                team2_issue_nature['late_reporting']['critical'] += 1
                team2_issue_nature['overall']['critical'] += 1

    # 4. Maintenance / Service / Issues
    query_filters = [Team2MaintenanceServiceIssues.team_id == team2.team_id] + build_date_filter(Team2MaintenanceServiceIssues)
    maintenance_service_data = Team2MaintenanceServiceIssues.query.filter(*query_filters).all()
    for item in maintenance_service_data:
        if item.nature_of_issue:
            nature = item.nature_of_issue.lower()
            if ('all_well' in nature or 'all well' in nature):
                team2_issue_nature['maintenance_service_issues']['all_well'] += 1
                team2_issue_nature['overall']['all_well'] += 1
            elif ('manageable' in nature):
                team2_issue_nature['maintenance_service_issues']['manageable'] += 1
                team2_issue_nature['overall']['manageable'] += 1
            elif ('critical' in nature):
                team2_issue_nature['maintenance_service_issues']['critical'] += 1
                team2_issue_nature['overall']['critical'] += 1

    # 5. Car Maintenance/Cleaning
    query_filters = [Team2CarMaintenanceCleaning.team_id == team2.team_id] + build_date_filter(Team2CarMaintenanceCleaning)
    car_maintenance_data = Team2CarMaintenanceCleaning.query.filter(*query_filters).all()
    for item in car_maintenance_data:
        if item.nature_of_issue:
            nature = item.nature_of_issue.lower()
            if ('all_well' in nature or 'all well' in nature):
                team2_issue_nature['car_maintenance_cleaning']['all_well'] += 1
                team2_issue_nature['overall']['all_well'] += 1
            elif ('manageable' in nature):
                team2_issue_nature['car_maintenance_cleaning']['manageable'] += 1
                team2_issue_nature['overall']['manageable'] += 1
            elif ('critical' in nature):
                team2_issue_nature['car_maintenance_cleaning']['critical'] += 1
                team2_issue_nature['overall']['critical'] += 1

    # 6. Vehicle Renewals / Delays (with 5 subtypes)
    query_filters = [Team2VehicleRenewalsDelays.team_id == team2.team_id] + build_date_filter(Team2VehicleRenewalsDelays)
    vehicle_renewals_data = Team2VehicleRenewalsDelays.query.filter(*query_filters).all()
    for item in vehicle_renewals_data:
        if item.particulars:
            key = None
            particulars = item.particulars.lower()
            if 'delayed halt' in particulars:
                key = 'delayed_halt'
            elif 'fc renewal' in particulars:
                key = 'fc_renewal'
            elif 'road tax' in particulars:
                key = 'road_tax'
            elif 'permit' in particulars:
                key = 'permit'
            elif 'insurance' in particulars:
                key = 'insurance'
            else:
                key = 'vehicle_renewals_delays'
            if item.nature_of_issue:
                nature = item.nature_of_issue.lower()
                if ('all_well' in nature or 'all well' in nature):
                    team2_issue_nature[key]['all_well'] += 1
                    team2_issue_nature['overall']['all_well'] += 1
                elif ('manageable' in nature):
                    team2_issue_nature[key]['manageable'] += 1
                    team2_issue_nature['overall']['manageable'] += 1
                elif ('critical' in nature):
                    team2_issue_nature[key]['critical'] += 1
                    team2_issue_nature['overall']['critical'] += 1

    # 7. Special Trip
    query_filters = [Team2SpecialTrip.team_id == team2.team_id] + build_date_filter(Team2SpecialTrip)
    special_trip_data = Team2SpecialTrip.query.filter(*query_filters).all()
    for item in special_trip_data:
        if item.nature_of_issue:
            nature = item.nature_of_issue.lower()
            if ('all_well' in nature or 'all well' in nature):
                team2_issue_nature['special_trip']['all_well'] += 1
                team2_issue_nature['overall']['all_well'] += 1
            elif ('manageable' in nature):
                team2_issue_nature['special_trip']['manageable'] += 1
                team2_issue_nature['overall']['manageable'] += 1
            elif ('critical' in nature):
                team2_issue_nature['special_trip']['critical'] += 1
                team2_issue_nature['overall']['critical'] += 1

            
    # Team 2 Section 14: AC Temperature Check (by floor)
    query_filters = [Team2ACTemperatureCheck.team_id == team2.team_id] + build_date_filter(Team2ACTemperatureCheck)
    ac_temp_data = Team2ACTemperatureCheck.query.filter(*query_filters).all()
    for item in ac_temp_data:
        # Floor mapping: 1=First, 2=Second, 3=Third, 4=Ground
        floor_map = {
            '1': 'ac_temp_first_floor',
            '2': 'ac_temp_second_floor',
            '3': 'ac_temp_third_floor',
            '4': 'ac_temp_ground_floor',
            'First Floor': 'ac_temp_first_floor',
            'Second Floor': 'ac_temp_second_floor',
            'Third Floor': 'ac_temp_third_floor',
            'Ground Floor': 'ac_temp_ground_floor',
        }
        floor_key = floor_map.get(str(item.floor).strip(), None)
        if floor_key and item.nature_of_issue:
            nature = item.nature_of_issue.lower()
            if ('all_well' in nature or 'all well' in nature):
                team2_issue_nature[floor_key]['all_well'] += 1
                team2_issue_nature['overall']['all_well'] += 1
            elif ('manageable' in nature):
                team2_issue_nature[floor_key]['manageable'] += 1
                team2_issue_nature['overall']['manageable'] += 1
            elif ('critical' in nature):
                team2_issue_nature[floor_key]['critical'] += 1
                team2_issue_nature['overall']['critical'] += 1

    # Team 2 Section 15: Labor, EB, Solar, Genset, Motor/Pest, AC Temp Deviation, Electricity Consumption
    # 15.1 Maintenance Labor
    query_filters = [Team2LaborEbSolarGenset.team_id == team2.team_id] + build_date_filter(Team2LaborEbSolarGenset)
    labor_data = Team2LaborEbSolarGenset.query.filter(*query_filters).all()
    for item in labor_data:
        if item.nature_of_issue:
            nature = item.nature_of_issue.lower()
            if ('all_well' in nature or 'all well' in nature):
                team2_issue_nature['maintenance_labor']['all_well'] += 1
                team2_issue_nature['overall']['all_well'] += 1
            elif ('manageable' in nature):
                team2_issue_nature['maintenance_labor']['manageable'] += 1
                team2_issue_nature['overall']['manageable'] += 1
            elif ('critical' in nature):
                team2_issue_nature['maintenance_labor']['critical'] += 1
                team2_issue_nature['overall']['critical'] += 1

    # 15.2a Motor Control
    query_filters = [Team2Motor.team_id == team2.team_id] + build_date_filter(Team2Motor)
    motor_data = Team2Motor.query.filter(*query_filters).all()
    for item in motor_data:
        if item.nature_of_issue:
            nature = item.nature_of_issue.lower()
            if ('all_well' in nature or 'all well' in nature):
                team2_issue_nature['motor']['all_well'] += 1
                team2_issue_nature['overall']['all_well'] += 1
            elif ('manageable' in nature):
                team2_issue_nature['motor']['manageable'] += 1
                team2_issue_nature['overall']['manageable'] += 1
            elif ('critical' in nature):
                team2_issue_nature['motor']['critical'] += 1
                team2_issue_nature['overall']['critical'] += 1

    # 15.2b Pest Control
    query_filters = [Team2PestControl.team_id == team2.team_id] + build_date_filter(Team2PestControl)
    pest_control_data = Team2PestControl.query.filter(*query_filters).all()
    for item in pest_control_data:
        if item.nature_of_issue:
            nature = item.nature_of_issue.lower()
            if ('all_well' in nature or 'all well' in nature):
                team2_issue_nature['pest_control']['all_well'] += 1
                team2_issue_nature['overall']['all_well'] += 1
            elif ('manageable' in nature):
                team2_issue_nature['pest_control']['manageable'] += 1
                team2_issue_nature['overall']['manageable'] += 1
            elif ('critical' in nature):
                team2_issue_nature['pest_control']['critical'] += 1
                team2_issue_nature['overall']['critical'] += 1

    # 15.3 AC Temp Deviation
    query_filters = [Team2ACTempDeviation.team_id == team2.team_id] + build_date_filter(Team2ACTempDeviation)
    ac_temp_dev_data = Team2ACTempDeviation.query.filter(*query_filters).all()
    for item in ac_temp_dev_data:
        if item.nature_of_issue:
            nature = item.nature_of_issue.lower()
            if ('all_well' in nature or 'all well' in nature):
                team2_issue_nature['ac_temp_deviation']['all_well'] += 1
                team2_issue_nature['overall']['all_well'] += 1
            elif ('manageable' in nature):
                team2_issue_nature['ac_temp_deviation']['manageable'] += 1
                team2_issue_nature['overall']['manageable'] += 1
            elif ('critical' in nature):
                team2_issue_nature['ac_temp_deviation']['critical'] += 1
                team2_issue_nature['overall']['critical'] += 1

    # 15.4 Electricity Consumption
    query_filters = [Team2ElectricityConsumption.team_id == team2.team_id] + build_date_filter(Team2ElectricityConsumption)
    elec_data = Team2ElectricityConsumption.query.filter(*query_filters).all()
    for item in elec_data:
        # No nature_of_issue field, but overall_issue_desc may contain nature
        if hasattr(item, 'overall_issue_desc') and item.overall_issue_desc:
            nature = item.overall_issue_desc.lower()
            if ('all_well' in nature or 'all well' in nature):
                team2_issue_nature['electricity_consumption']['all_well'] += 1
                team2_issue_nature['overall']['all_well'] += 1
            elif ('manageable' in nature):
                team2_issue_nature['electricity_consumption']['manageable'] += 1
                team2_issue_nature['overall']['manageable'] += 1
            elif ('critical' in nature):
                team2_issue_nature['electricity_consumption']['critical'] += 1
                team2_issue_nature['overall']['critical'] += 1

    # 15.5 EB Details
    query_filters = [Team2EBDetails.team_id == team2.team_id] + build_date_filter(Team2EBDetails)
    eb_details_data = Team2EBDetails.query.filter(*query_filters).all()
    for item in eb_details_data:
        if item.nature_of_issue:
            nature = item.nature_of_issue.lower()
            if ('all_well' in nature or 'all well' in nature):
                team2_issue_nature['eb_details']['all_well'] += 1
                team2_issue_nature['overall']['all_well'] += 1
            elif ('manageable' in nature):
                team2_issue_nature['eb_details']['manageable'] += 1
                team2_issue_nature['overall']['manageable'] += 1
            elif ('critical' in nature):
                team2_issue_nature['eb_details']['critical'] += 1
                team2_issue_nature['overall']['critical'] += 1

    # 15.6 Solar Details
    query_filters = [Team2SolarDetails.team_id == team2.team_id] + build_date_filter(Team2SolarDetails)
    solar_details_data = Team2SolarDetails.query.filter(*query_filters).all()
    for item in solar_details_data:
        if item.nature_of_issue:
            nature = item.nature_of_issue.lower()
            if ('all_well' in nature or 'all well' in nature):
                team2_issue_nature['solar_details']['all_well'] += 1
                team2_issue_nature['overall']['all_well'] += 1
            elif ('manageable' in nature):
                team2_issue_nature['solar_details']['manageable'] += 1
                team2_issue_nature['overall']['manageable'] += 1
            elif ('critical' in nature):
                team2_issue_nature['solar_details']['critical'] += 1
                team2_issue_nature['overall']['critical'] += 1

    # 15.7 Genset Details
    query_filters = [Team2GensetDetails.team_id == team2.team_id] + build_date_filter(Team2GensetDetails)
    genset_details_data = Team2GensetDetails.query.filter(*query_filters).all()
    for item in genset_details_data:
        if item.nature_of_issue:
            nature = item.nature_of_issue.lower()
            if ('all_well' in nature or 'all well' in nature):
                team2_issue_nature['genset_details']['all_well'] += 1
                team2_issue_nature['overall']['all_well'] += 1
            elif ('manageable' in nature):
                team2_issue_nature['genset_details']['manageable'] += 1
                team2_issue_nature['overall']['manageable'] += 1
            elif ('critical' in nature):
                team2_issue_nature['genset_details']['critical'] += 1
                team2_issue_nature['overall']['critical'] += 1


    # Team 2 Section 16: Security Issue Nature Aggregation

    # 16.a Count Verification (Security)
    query_filters = [Team2CountVerification.team_id == team2.team_id] + build_date_filter(Team2CountVerification)
    count_verification_data = Team2CountVerification.query.filter(*query_filters).all()
    for item in count_verification_data:
        if item.nature_of_issue:
            nature = item.nature_of_issue.lower()
            if ('all_well' in nature or 'all well' in nature):
                team2_issue_nature['security_count_verification']['all_well'] += 1
                team2_issue_nature['overall']['all_well'] += 1
            elif ('manageable' in nature):
                team2_issue_nature['security_count_verification']['manageable'] += 1
                team2_issue_nature['overall']['manageable'] += 1
            elif ('critical' in nature):
                team2_issue_nature['security_count_verification']['critical'] += 1
                team2_issue_nature['overall']['critical'] += 1

    # 16.b Attendance Replacement (Security)
    query_filters = [Team2AttendanceReplacement.team_id == team2.team_id] + build_date_filter(Team2AttendanceReplacement)
    attendance_replacement_data = Team2AttendanceReplacement.query.filter(*query_filters).all()
    for item in attendance_replacement_data:
        if item.nature_of_issue:
            nature = item.nature_of_issue.lower()
            if ('all_well' in nature or 'all well' in nature):
                team2_issue_nature['security_attendance_replacement']['all_well'] += 1
                team2_issue_nature['overall']['all_well'] += 1
            elif ('manageable' in nature):
                team2_issue_nature['security_attendance_replacement']['manageable'] += 1
                team2_issue_nature['overall']['manageable'] += 1
            elif ('critical' in nature):
                team2_issue_nature['security_attendance_replacement']['critical'] += 1
                team2_issue_nature['overall']['critical'] += 1

    # 16.c Security Info Note
    query_filters = [Team2SecurityInfoNote.team_id == team2.team_id] + build_date_filter(Team2SecurityInfoNote)
    security_info_note_data = Team2SecurityInfoNote.query.filter(*query_filters).all()
    for item in security_info_note_data:
        if item.nature_of_issue:
            nature = item.nature_of_issue.lower()
            if ('all_well' in nature or 'all well' in nature):
                team2_issue_nature['security_info_note']['all_well'] += 1
                team2_issue_nature['overall']['all_well'] += 1
            elif ('manageable' in nature):
                team2_issue_nature['security_info_note']['manageable'] += 1
                team2_issue_nature['overall']['manageable'] += 1
            elif ('critical' in nature):
                team2_issue_nature['security_info_note']['critical'] += 1
                team2_issue_nature['overall']['critical'] += 1

    # 16.d Govt Officials In/Out
    query_filters = [Team2SecurityGovtInout.team_id == team2.team_id] + build_date_filter(Team2SecurityGovtInout)
    govt_inout_data = Team2SecurityGovtInout.query.filter(*query_filters).all()
    for item in govt_inout_data:
        if item.nature_of_issue:
            nature = item.nature_of_issue.lower()
            if ('all_well' in nature or 'all well' in nature):
                team2_issue_nature['govt_officials_inout']['all_well'] += 1
                team2_issue_nature['overall']['all_well'] += 1
            elif ('manageable' in nature):
                team2_issue_nature['govt_officials_inout']['manageable'] += 1
                team2_issue_nature['overall']['manageable'] += 1
            elif ('critical' in nature):
                team2_issue_nature['govt_officials_inout']['critical'] += 1
                team2_issue_nature['overall']['critical'] += 1

    # 16.f Materials Inward (Security)
    query_filters = [Team2SecurityMaterialsInout.team_id == team2.team_id] + build_date_filter(Team2SecurityMaterialsInout)
    materials_inward_data = Team2SecurityMaterialsInout.query.filter(*query_filters).all()
    for item in materials_inward_data:
        if item.nature_of_issue:
            nature = item.nature_of_issue.lower()
            if ('all_well' in nature or 'all well' in nature):
                team2_issue_nature['security_materials_inward']['all_well'] += 1
                team2_issue_nature['overall']['all_well'] += 1
            elif ('manageable' in nature):
                team2_issue_nature['security_materials_inward']['manageable'] += 1
                team2_issue_nature['overall']['manageable'] += 1
            elif ('critical' in nature):
                team2_issue_nature['security_materials_inward']['critical'] += 1
                team2_issue_nature['overall']['critical'] += 1

    # 16.g Materials Outward (Security)
    query_filters = [Team2SecurityMaterialsOutward.team_id == team2.team_id] + build_date_filter(Team2SecurityMaterialsOutward)
    materials_outward_data = Team2SecurityMaterialsOutward.query.filter(*query_filters).all()
    for item in materials_outward_data:
        if item.nature_of_issue:
            nature = item.nature_of_issue.lower()
            if ('all_well' in nature or 'all well' in nature):
                team2_issue_nature['security_materials_outward']['all_well'] += 1
                team2_issue_nature['overall']['all_well'] += 1
            elif ('manageable' in nature):
                team2_issue_nature['security_materials_outward']['manageable'] += 1
                team2_issue_nature['overall']['manageable'] += 1
            elif ('critical' in nature):
                team2_issue_nature['security_materials_outward']['critical'] += 1
                team2_issue_nature['overall']['critical'] += 1

    # 16.h Transport Verification (Security)
    query_filters = [Team2TransportVerification.team_id == team2.team_id] + build_date_filter(Team2TransportVerification)
    transport_verification_data = Team2TransportVerification.query.filter(*query_filters).all()
    for item in transport_verification_data:
        if item.nature_of_issue:
            nature = item.nature_of_issue.lower()
            if ('all_well' in nature or 'all well' in nature):
                team2_issue_nature['security_transport_verification']['all_well'] += 1
                team2_issue_nature['overall']['all_well'] += 1
            elif ('manageable' in nature):
                team2_issue_nature['security_transport_verification']['manageable'] += 1
                team2_issue_nature['overall']['manageable'] += 1
            elif ('critical' in nature):
                team2_issue_nature['security_transport_verification']['critical'] += 1
                team2_issue_nature['overall']['critical'] += 1

    # 17. Documents Movement (Team 2)
    query_filters = [Team2DocumentsMovement.team_id == team2.team_id] + build_date_filter(Team2DocumentsMovement)
    documents_movement_data = Team2DocumentsMovement.query.filter(*query_filters).all()
    for item in documents_movement_data:
        # Row 1: New File / Document Entry
        if item.doc_new_nature:
            nature = item.doc_new_nature.lower()
            if ('all_well' in nature or 'all well' in nature):
                team2_issue_nature['documents_movement']['all_well'] += 1
                team2_issue_nature['overall']['all_well'] += 1
            elif ('manageable' in nature):
                team2_issue_nature['documents_movement']['manageable'] += 1
                team2_issue_nature['overall']['manageable'] += 1
            elif ('critical' in nature):
                team2_issue_nature['documents_movement']['critical'] += 1
                team2_issue_nature['overall']['critical'] += 1
        # Row 2: Non-Returnable File / Document
        if item.doc_nonret_nature:
            nature = item.doc_nonret_nature.lower()
            if ('all_well' in nature or 'all well' in nature):
                team2_issue_nature['documents_movement']['all_well'] += 1
                team2_issue_nature['overall']['all_well'] += 1
            elif ('manageable' in nature):
                team2_issue_nature['documents_movement']['manageable'] += 1
                team2_issue_nature['overall']['manageable'] += 1
            elif ('critical' in nature):
                team2_issue_nature['documents_movement']['critical'] += 1
                team2_issue_nature['overall']['critical'] += 1
        # Row 3: Original File / Doc Movement
        if item.doc_orig_nature:
            nature = item.doc_orig_nature.lower()
            if ('all_well' in nature or 'all well' in nature):
                team2_issue_nature['documents_movement']['all_well'] += 1
                team2_issue_nature['overall']['all_well'] += 1
            elif ('manageable' in nature):
                team2_issue_nature['documents_movement']['manageable'] += 1
                team2_issue_nature['overall']['manageable'] += 1
            elif ('critical' in nature):
                team2_issue_nature['documents_movement']['critical'] += 1
                team2_issue_nature['overall']['critical'] += 1

    # 18. Govt Official Documents (Team 2)
    query_filters = [Team2GovtOfficialDocuments.team_id == team2.team_id] + build_date_filter(Team2GovtOfficialDocuments)
    govt_official_documents_data = Team2GovtOfficialDocuments.query.filter(*query_filters).all()
    for item in govt_official_documents_data:
        if item.nature_of_issue:
            nature = item.nature_of_issue.lower()
            if ('all_well' in nature or 'all well' in nature):
                team2_issue_nature['govt_official_documents']['all_well'] += 1
                team2_issue_nature['overall']['all_well'] += 1
            elif ('manageable' in nature):
                team2_issue_nature['govt_official_documents']['manageable'] += 1
                team2_issue_nature['overall']['manageable'] += 1
            elif ('critical' in nature):
                team2_issue_nature['govt_official_documents']['critical'] += 1
                team2_issue_nature['overall']['critical'] += 1

    # 19.a Thoorigai Team Social Media (Team 2)
    query_filters = [Team2ThoorigaiTeamSocialMedia.team_id == team2.team_id] + build_date_filter(Team2ThoorigaiTeamSocialMedia)
    thoorigai_social_media_data = Team2ThoorigaiTeamSocialMedia.query.filter(*query_filters).all()
    for item in thoorigai_social_media_data:
        if item.nature_of_issue:
            nature = item.nature_of_issue.lower()
            if ('all_well' in nature or 'all well' in nature):
                team2_issue_nature['digital_marketing_thoorigai_social_media']['all_well'] += 1
                team2_issue_nature['overall']['all_well'] += 1
            elif ('manageable' in nature):
                team2_issue_nature['digital_marketing_thoorigai_social_media']['manageable'] += 1
                team2_issue_nature['overall']['manageable'] += 1
            elif ('critical' in nature):
                team2_issue_nature['digital_marketing_thoorigai_social_media']['critical'] += 1
                team2_issue_nature['overall']['critical'] += 1

    # 19.b Thoorigai Website Updates (Team 2)
    query_filters = [Team2WebsiteUpdates.team_id == team2.team_id] + build_date_filter(Team2WebsiteUpdates)
    thoorigai_website_updates_data = Team2WebsiteUpdates.query.filter(*query_filters).all()
    for item in thoorigai_website_updates_data:
        if item.nature_of_issue:
            nature = item.nature_of_issue.lower()
            if ('all_well' in nature or 'all well' in nature):
                team2_issue_nature['digital_marketing_thoorigai_website_updates']['all_well'] += 1
                team2_issue_nature['overall']['all_well'] += 1
            elif ('manageable' in nature):
                team2_issue_nature['digital_marketing_thoorigai_website_updates']['manageable'] += 1
                team2_issue_nature['overall']['manageable'] += 1
            elif ('critical' in nature):
                team2_issue_nature['digital_marketing_thoorigai_website_updates']['critical'] += 1
                team2_issue_nature['overall']['critical'] += 1

    # 19.c MD Social Media (Team 2)
    query_filters = [Team2MDSocialMedia.team_id == team2.team_id] + build_date_filter(Team2MDSocialMedia)
    md_social_media_data = Team2MDSocialMedia.query.filter(*query_filters).all()
    for item in md_social_media_data:
        if item.nature_of_issue:
            nature = item.nature_of_issue.lower()
            if ('all_well' in nature or 'all well' in nature):
                team2_issue_nature['digital_marketing_md_social_media']['all_well'] += 1
                team2_issue_nature['overall']['all_well'] += 1
            elif ('manageable' in nature):
                team2_issue_nature['digital_marketing_md_social_media']['manageable'] += 1
                team2_issue_nature['overall']['manageable'] += 1
            elif ('critical' in nature):
                team2_issue_nature['digital_marketing_md_social_media']['critical'] += 1
                team2_issue_nature['overall']['critical'] += 1

    
    # 20. Intercom Maintenance (Team 2)
    query_filters = [Team2IntercomMaintenance.team_id == team2.team_id] + build_date_filter(Team2IntercomMaintenance)
    intercom_maintenance_data = Team2IntercomMaintenance.query.filter(*query_filters).all()
    for item in intercom_maintenance_data:
        if item.nature_of_issue:
            nature = item.nature_of_issue.lower()
            if ('all_well' in nature or 'all well' in nature):
                team2_issue_nature['intercom_maintenance']['all_well'] += 1
                team2_issue_nature['overall']['all_well'] += 1
            elif ('manageable' in nature):
                team2_issue_nature['intercom_maintenance']['manageable'] += 1
                team2_issue_nature['overall']['manageable'] += 1
            elif ('critical' in nature):
                team2_issue_nature['intercom_maintenance']['critical'] += 1
                team2_issue_nature['overall']['critical'] += 1

    # 21. Health Check Up (Team 2)
    query_filters = [Team2HealthCheckUp.team_id == team2.team_id] + build_date_filter(Team2HealthCheckUp)
    health_check_up_data = Team2HealthCheckUp.query.filter(*query_filters).all()
    for item in health_check_up_data:
        if item.nature_of_issue:
            nature = item.nature_of_issue.lower()
            if ('all_well' in nature or 'all well' in nature):
                team2_issue_nature['health_check_up']['all_well'] += 1
                team2_issue_nature['overall']['all_well'] += 1
            elif ('manageable' in nature):
                team2_issue_nature['health_check_up']['manageable'] += 1
                team2_issue_nature['overall']['manageable'] += 1
            elif ('critical' in nature):
                team2_issue_nature['health_check_up']['critical'] += 1
                team2_issue_nature['overall']['critical'] += 1

    # 22. Net Connectivity & Print Details (Team 2)
    query_filters = [Team2NetConnectivityPrintDetails.team_id == team2.team_id] + build_date_filter(Team2NetConnectivityPrintDetails)
    net_connectivity_data = Team2NetConnectivityPrintDetails.query.filter(*query_filters).all()
    for item in net_connectivity_data:
        if item.nature_of_issue:
            nature = item.nature_of_issue.lower()
            if ('all_well' in nature or 'all well' in nature):
                team2_issue_nature['net_connectivity_print_details']['all_well'] += 1
                team2_issue_nature['overall']['all_well'] += 1
            elif ('manageable' in nature):
                team2_issue_nature['net_connectivity_print_details']['manageable'] += 1
                team2_issue_nature['overall']['manageable'] += 1
            elif ('critical' in nature):
                team2_issue_nature['net_connectivity_print_details']['critical'] += 1
                team2_issue_nature['overall']['critical'] += 1

    # 23. General Maintenance - IT Products (Team 2)
    query_filters = [Team2GeneralMaintenanceITProducts.team_id == team2.team_id] + build_date_filter(Team2GeneralMaintenanceITProducts)
    general_maintenance_it_data = Team2GeneralMaintenanceITProducts.query.filter(*query_filters).all()
    for item in general_maintenance_it_data:
        if item.nature_of_issue:
            nature = item.nature_of_issue.lower()
            if ('all_well' in nature or 'all well' in nature):
                team2_issue_nature['general_maintenance_it_products']['all_well'] += 1
                team2_issue_nature['overall']['all_well'] += 1
            elif ('manageable' in nature):
                team2_issue_nature['general_maintenance_it_products']['manageable'] += 1
                team2_issue_nature['overall']['manageable'] += 1
            elif ('critical' in nature):
                team2_issue_nature['general_maintenance_it_products']['critical'] += 1
                team2_issue_nature['overall']['critical'] += 1

    # 24. Calendar Schedule (Team 2)
    query_filters = [Team2CalendarSchedule.team_id == team2.team_id] + build_date_filter(Team2CalendarSchedule)
    calendar_schedule_data = Team2CalendarSchedule.query.filter(*query_filters).all()
    for item in calendar_schedule_data:
        if item.nature_of_issue:
            nature = item.nature_of_issue.lower()
            # Map department to the correct key in team2_issue_nature
            dept_map = {
                'admin': 'calendar_schedule_admin',
                'house keeping': 'calendar_schedule_house_keeping',
                'security': 'calendar_schedule_security',
                'transport': 'calendar_schedule_transport'
            }
            dept_key = dept_map.get((item.department or '').strip().lower())
            if dept_key:
                if ('all_well' in nature or 'all well' in nature):
                    team2_issue_nature[dept_key]['all_well'] += 1
                    team2_issue_nature['overall']['all_well'] += 1
                elif ('manageable' in nature):
                    team2_issue_nature[dept_key]['manageable'] += 1
                    team2_issue_nature['overall']['manageable'] += 1
                elif ('critical' in nature):
                    team2_issue_nature[dept_key]['critical'] += 1
                    team2_issue_nature['overall']['critical'] += 1

    # 25. Training Attendance (Team 2)
    query_filters = [Team2TrainingAttendance.team_id == team2.team_id] + build_date_filter(Team2TrainingAttendance)
    training_attendance_data = Team2TrainingAttendance.query.filter(*query_filters).all()
    for item in training_attendance_data:
        if item.nature_of_issue:
            nature = item.nature_of_issue.lower()
            # Map department_group and dept to the correct key in team2_issue_nature
            dept_map = {
                ('academics', 'academics - jr.school'): 'training_attendance_academics_jr',
                ('academics', 'academics - sr.school'): 'training_attendance_academics_sr',
                ('admin', 'admin - admin'): 'training_attendance_admin',
                ('admin', 'admin - drivers'): 'training_attendance_drivers',
                ('admin', 'admin - securities'): 'training_attendance_securities',
                ('admin', 'admin - drivers (sub)'): 'training_attendance_drivers_sub',
                ('admin', 'admin - conductors'): 'training_attendance_conductors',
            }
            dept_group = (item.department_group or '').strip().lower()
            dept = (item.dept or '').strip().lower()
            dept_key = dept_map.get((dept_group, dept))
            if dept_key:
                if ('all_well' in nature or 'all well' in nature):
                    team2_issue_nature[dept_key]['all_well'] += 1
                    team2_issue_nature['overall']['all_well'] += 1
                elif ('manageable' in nature):
                    team2_issue_nature[dept_key]['manageable'] += 1
                    team2_issue_nature['overall']['manageable'] += 1
                elif ('critical' in nature):
                    team2_issue_nature[dept_key]['critical'] += 1
                    team2_issue_nature['overall']['critical'] += 1

    # 26. Training Details (CBSE/CIS/External) (Team 2)
    query_filters = [Team2TrainingDetails.team_id == team2.team_id] + build_date_filter(Team2TrainingDetails)
    training_details_data = Team2TrainingDetails.query.filter(*query_filters).all()
    for item in training_details_data:
        if item.nature_of_issue:
            nature = item.nature_of_issue.lower()
            key = 'training_details_cbse_cis_external'
            if ('all_well' in nature or 'all well' in nature):
                team2_issue_nature[key]['all_well'] += 1
                team2_issue_nature['overall']['all_well'] += 1
            elif ('manageable' in nature):
                team2_issue_nature[key]['manageable'] += 1
                team2_issue_nature['overall']['manageable'] += 1
            elif ('critical' in nature):
                team2_issue_nature[key]['critical'] += 1
                team2_issue_nature['overall']['critical'] += 1

    # Get Team 3 data
    team3 = Team.query.filter_by(team_name='Team 3').first()
    if team3:
        # Get Team 3 Audit data
        query_filters = [Team3Audit.team_id == team3.team_id] + build_date_filter(Team3Audit)
        audit_data = Team3Audit.query.filter(*query_filters).all()
        
        for item in audit_data:
            # Process Audit data
            if item.issue_nature:  # Changed from nature_of_issue to issue_nature
                nature = item.issue_nature.lower()
                if ('all_well' in nature or 'all well' in nature):
                    team3_issue_nature['audit_issue_nature']['all_well'] += 1
                    team3_issue_nature['overall']['all_well'] += 1
                elif ('manageable' in nature):
                    team3_issue_nature['audit_issue_nature']['manageable'] += 1
                    team3_issue_nature['overall']['manageable'] += 1
                elif ('critical' in nature):
                    team3_issue_nature['audit_issue_nature']['critical'] += 1
                    team3_issue_nature['overall']['critical'] += 1

        # Get Team 3 New Audit data
        query_filters_new = [Team3NewAudit.team_id == team3.team_id] + build_date_filter(Team3NewAudit)
        new_audit_data = Team3NewAudit.query.filter(*query_filters_new).all()
        
        for item in new_audit_data:
            # Process New Audit data
            if item.issue_nature:
                nature = item.issue_nature.lower()
                if ('all_well' in nature or 'all well' in nature):
                    team3_issue_nature['new_audit_issue_nature']['all_well'] += 1
                    team3_issue_nature['overall']['all_well'] += 1
                elif ('manageable' in nature):
                    team3_issue_nature['new_audit_issue_nature']['manageable'] += 1
                    team3_issue_nature['overall']['manageable'] += 1
                elif ('critical' in nature):
                    team3_issue_nature['new_audit_issue_nature']['critical'] += 1
                    team3_issue_nature['overall']['critical'] += 1


    # Generate Premium Matplotlib charts with enhanced styling
    import matplotlib
    matplotlib.use('Agg')  # Use Agg backend to avoid GUI issues
    import matplotlib.pyplot as plt
    import numpy as np
    import io
    import base64
    from matplotlib.patches import Rectangle
    from matplotlib.patches import FancyBboxPatch
    import matplotlib.patches as mpatches
    
    # Set global style for premium look
    plt.style.use('default')
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans', 'Liberation Sans']
    plt.rcParams['axes.facecolor'] = '#ffffff'
    plt.rcParams['figure.facecolor'] = '#ffffff'
    plt.rcParams['savefig.facecolor'] = '#ffffff'
    plt.rcParams['axes.edgecolor'] = '#e2e8f0'
    plt.rcParams['axes.linewidth'] = 1.5
    plt.rcParams['grid.color'] = '#f1f5f9'
    plt.rcParams['grid.linestyle'] = '--'
    plt.rcParams['grid.linewidth'] = 0.8
    plt.rcParams['grid.alpha'] = 0.7
    
    # Premium color palette with gradients
    colors = {
        'all_well': {
            'primary': '#10b981',
            'light': '#34d399',
            'dark': '#059669',
            'gradient': ['#10b981', '#34d399', '#6ee7b7']
        },
        'manageable': {
            'primary': '#f59e0b',
            'light': '#fbbf24',
            'dark': '#d97706',
            'gradient': ['#f59e0b', '#fbbf24', '#fcd34d']
        },
        'critical': {
            'primary': '#ef4444',
            'light': '#f87171',
            'dark': '#dc2626',
            'gradient': ['#ef4444', '#f87171', '#fca5a5']
        },
        'background': '#ffffff',
        'text': '#1e293b',
        'text_secondary': '#64748b',
        'border': '#e2e8f0',
        'grid': '#f1f5f9'
    }
    
    # Team 1 Chart
    plt.figure(figsize=(20, 15))
    team1_departments = ['Jr. School', 'Sr. School', 'Student Attendance Kindergarten', 'Student Attendance Grade 1 to 5', 'Student Attendance Grade 6 to 10', 'Student Attendance Grade 11 to 12',  'Student Attendance Overall',  'Grooming', 'Late Coming',  'Admission Status',  'Admission Status Bumble Bee',  'Admission Status Bumble B Leeds Excel', 'Transfer Certificate ', 'Parent Activity ', 'Parent Visiting ', 'Exam Grade 1 to 5', 'Exam Grade 6 to 8', 'Exam Grade 9 to 10', 'Exam Grade 11', 'Exam Grade 12', 'Information from External Agencies CIS', ' Information from External Agencies CBSE', ' Information from External Agencies CEO/STATE GOV', ' Information from External Agencies EMIS', 'Sick Bay', 'Home School Communications ', 'Disciplinary Measures',   'Logistics ', 'Intra Grade Competition Certificate ', 'Staff Concern', 'Parent Concern', 'Parent Concern Detail']
    team1_all_well = [team1_issue_nature['jr_school']['all_well'], 
                      team1_issue_nature['sr_school']['all_well'],
                      team1_issue_nature['student_attendance_kindergarten']['all_well'],
                      team1_issue_nature['student_attendance_grade_1_5']['all_well'],
                      team1_issue_nature['student_attendance_grade_6_10']['all_well'],
                      team1_issue_nature['student_attendance_grade_11_12']['all_well'],
                      team1_issue_nature['student_attendance_overall']['all_well'],
                      team1_issue_nature['groom_issue_nature']['all_well'],
                      team1_issue_nature['late_coming_issue_nature']['all_well'],
                      team1_issue_nature['admission_status_issue_nature']['all_well'],
                      team1_issue_nature['admission_status_issue_nature_Bumble_Bee']['all_well'],
                      team1_issue_nature['admission_status_issue_nature_Bumble_b_Leeds_Excel']['all_well'],
                      team1_issue_nature['tc_issue_nature']['all_well'],
                      team1_issue_nature['parent_activity_issue_nature']['all_well'],
                      team1_issue_nature['parent_visiting_issue_nature']['all_well'],
                      team1_issue_nature['exam_issue_nature_g15']['all_well'],
                      team1_issue_nature['exam_issue_nature_g68']['all_well'],
                      team1_issue_nature['exam_issue_nature_g910']['all_well'],
                      team1_issue_nature['exam_issue_nature_g11']['all_well'],
                      team1_issue_nature['exam_issue_nature_g12']['all_well'],
                      team1_issue_nature['ext_issue_nature_cis']['all_well'],
                      team1_issue_nature['ext_issue_nature_cbse']['all_well'],
                      team1_issue_nature['ext_issue_nature_state']['all_well'],
                      team1_issue_nature['ext_issue_nature_emis']['all_well'],
                      team1_issue_nature['sick_issue_nature']['all_well'],
                      team1_issue_nature['home_school_comm_issue_nature']['all_well'],
                      team1_issue_nature['disciplinary_issue_nature']['all_well'],
                      team1_issue_nature['logistics_issue_nature']['all_well'],
                      team1_issue_nature['cert_issue_nature']['all_well'],
                      team1_issue_nature['staff_concern_issue_nature']['all_well'],
                      team1_issue_nature['pc_summary_issue_nature']['all_well'],
                      team1_issue_nature['pc_detail_issue_nature']['all_well']]
    team1_manageable = [team1_issue_nature['jr_school']['manageable'], 
                        team1_issue_nature['sr_school']['manageable'],
                        team1_issue_nature['student_attendance_kindergarten']['manageable'],
                        team1_issue_nature['student_attendance_grade_1_5']['manageable'],
                        team1_issue_nature['student_attendance_grade_6_10']['manageable'],
                        team1_issue_nature['student_attendance_grade_11_12']['manageable'],
                        team1_issue_nature['student_attendance_overall']['manageable'],
                        team1_issue_nature['groom_issue_nature']['manageable'],
                        team1_issue_nature['late_coming_issue_nature']['manageable'],
                        team1_issue_nature['admission_status_issue_nature']['manageable'],
                        team1_issue_nature['admission_status_issue_nature_Bumble_Bee']['manageable'],
                        team1_issue_nature['admission_status_issue_nature_Bumble_b_Leeds_Excel']['manageable'],
                        team1_issue_nature['tc_issue_nature']['manageable'],
                        team1_issue_nature['parent_activity_issue_nature']['manageable'],
                        team1_issue_nature['parent_visiting_issue_nature']['manageable'],
                        team1_issue_nature['exam_issue_nature_g15']['manageable'],
                        team1_issue_nature['exam_issue_nature_g68']['manageable'],
                        team1_issue_nature['exam_issue_nature_g910']['manageable'],
                        team1_issue_nature['exam_issue_nature_g11']['manageable'],
                        team1_issue_nature['exam_issue_nature_g12']['manageable'],
                        team1_issue_nature['ext_issue_nature_cis']['manageable'],
                        team1_issue_nature['ext_issue_nature_cbse']['manageable'],
                        team1_issue_nature['ext_issue_nature_state']['manageable'],
                        team1_issue_nature['ext_issue_nature_emis']['manageable'],
                        team1_issue_nature['sick_issue_nature']['manageable'],
                        team1_issue_nature['home_school_comm_issue_nature']['manageable'],
                        team1_issue_nature['disciplinary_issue_nature']['manageable'],
                        team1_issue_nature['logistics_issue_nature']['manageable'],
                        team1_issue_nature['cert_issue_nature']['manageable'],
                        team1_issue_nature['staff_concern_issue_nature']['manageable'],
                        team1_issue_nature['pc_summary_issue_nature']['manageable'],
                        team1_issue_nature['pc_detail_issue_nature']['manageable']]
    team1_critical = [team1_issue_nature['jr_school']['critical'], 
                      team1_issue_nature['sr_school']['critical'],
                      team1_issue_nature['student_attendance_kindergarten']['critical'],
                      team1_issue_nature['student_attendance_grade_1_5']['critical'],
                      team1_issue_nature['student_attendance_grade_6_10']['critical'],
                      team1_issue_nature['student_attendance_grade_11_12']['critical'],
                      team1_issue_nature['student_attendance_overall']['critical'],
                      team1_issue_nature['groom_issue_nature']['critical'],
                      team1_issue_nature['late_coming_issue_nature']['critical'],
                      team1_issue_nature['admission_status_issue_nature']['critical'],
                      team1_issue_nature['admission_status_issue_nature_Bumble_Bee']['critical'],
                      team1_issue_nature['admission_status_issue_nature_Bumble_b_Leeds_Excel']['critical'],
                      team1_issue_nature['tc_issue_nature']['critical'],
                      team1_issue_nature['parent_activity_issue_nature']['critical'],
                      team1_issue_nature['parent_visiting_issue_nature']['critical'],
                      team1_issue_nature['exam_issue_nature_g15']['critical'],
                      team1_issue_nature['exam_issue_nature_g68']['critical'],
                      team1_issue_nature['exam_issue_nature_g910']['critical'],
                      team1_issue_nature['exam_issue_nature_g11']['critical'],
                      team1_issue_nature['exam_issue_nature_g12']['critical'],
                      team1_issue_nature['ext_issue_nature_cis']['critical'],
                      team1_issue_nature['ext_issue_nature_cbse']['critical'],
                      team1_issue_nature['ext_issue_nature_state']['critical'],
                      team1_issue_nature['ext_issue_nature_emis']['critical'],
                      team1_issue_nature['sick_issue_nature']['critical'],
                      team1_issue_nature['home_school_comm_issue_nature']['critical'],
                      team1_issue_nature['disciplinary_issue_nature']['critical'],
                      team1_issue_nature['logistics_issue_nature']['critical'],
                      team1_issue_nature['cert_issue_nature']['critical'],
                      team1_issue_nature['staff_concern_issue_nature']['critical'],
                      team1_issue_nature['pc_summary_issue_nature']['critical'],
                      team1_issue_nature['pc_detail_issue_nature']['critical']]
    
    x = np.arange(len(team1_departments))
    width = 0.25
    
    # Create premium figure with enhanced styling
    fig, ax = plt.subplots(figsize=(20, 12), facecolor=colors['background'])
    fig.patch.set_facecolor(colors['background'])
    
    # Add subtle background gradient effect
    ax.set_facecolor(colors['background'])
    
    # Create premium bars with gradients and shadows
    bars1 = ax.bar(x - width, team1_all_well, width, 
                  label=f'All Well ({sum(team1_all_well)})', 
                  color=colors['all_well']['primary'], 
                  alpha=0.95, 
                  edgecolor=colors['all_well']['dark'], 
                  linewidth=1.2,
                  zorder=3)
    
    bars2 = ax.bar(x, team1_manageable, width, 
                  label=f'Manageable ({sum(team1_manageable)})', 
                  color=colors['manageable']['primary'], 
                  alpha=0.95, 
                  edgecolor=colors['manageable']['dark'], 
                  linewidth=1.2,
                  zorder=3)
    
    bars3 = ax.bar(x + width, team1_critical, width, 
                  label=f'Critical ({sum(team1_critical)})', 
                  color=colors['critical']['primary'], 
                  alpha=0.95, 
                  edgecolor=colors['critical']['dark'], 
                  linewidth=1.2,
                  zorder=3)
    
    # Enhanced styling
    ax.set_xlabel('Department', fontsize=16, fontweight='bold', color=colors['text'], labelpad=20)
    ax.set_ylabel('Issue Count', fontsize=16, fontweight='bold', color=colors['text'], labelpad=20)
    ax.set_title('Team 1 - Department-wise Issue Analysis', fontsize=22, fontweight='bold', 
                pad=30, color=colors['text'])
    
    # Premium axis styling
    ax.set_xticks(x)
    ax.set_xticklabels(team1_departments, rotation=45, fontsize=11, ha='right', color=colors['text_secondary'])
    ax.tick_params(axis='both', colors=colors['text_secondary'], labelsize=12)
    
    # Enhanced grid with premium styling
    ax.grid(axis='y', linestyle='--', alpha=0.4, color=colors['grid'], linewidth=0.8, zorder=1)
    ax.set_axisbelow(True)
    
    # Premium legend with enhanced styling
    legend = ax.legend(fontsize=13, frameon=True, 
                      facecolor=colors['background'], 
                      edgecolor=colors['border'],
                      borderpad=1.2,
                      shadow=True,
                      fancybox=True,
                      loc='upper right')
    
    for text in legend.get_texts():
        text.set_color(colors['text'])
        text.set_fontweight('bold')
    
    # Enhanced value labels with premium styling
    for bars in [bars1, bars2, bars3]:
        for bar in bars:
            height = bar.get_height()
            if height > 0:
                ax.text(bar.get_x() + bar.get_width()/2, height + 0.1, 
                       f'{int(height)}', 
                       ha='center', va='bottom', 
                       fontsize=11, fontweight='bold', 
                       color=colors['text'],
                       bbox=dict(boxstyle="round,pad=0.3", 
                                facecolor=colors['background'], 
                                edgecolor=colors['border'],
                                alpha=0.8))
    
    # Add subtle border around the plot
    for spine in ax.spines.values():
        spine.set_color(colors['border'])
        spine.set_linewidth(1.5)
    
    plt.tight_layout(pad=3.0)
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=300, facecolor=colors['background'], 
                bbox_inches='tight', edgecolor='none')
    buf.seek(0)
    team1_chart_image = base64.b64encode(buf.read()).decode('utf-8')
    plt.close()
    
    # Team 2 Chart - with updated styling
    plt.style.use('seaborn-v0_8-whitegrid')
    team2_departments = ['Jr. School', 'Sr. School', 'ECA', 'Admin Staff', 'Drivers', 'Security', 'Housekeeping', 'Conductors', 'Recruitment Academic', 'Recruitment Admin', 'Recruitment Pending Academic', 'Recruitment Pending Admin', 'Interview Schedule', 'Exit',  'Issues Staff Concerns', 'Kural Recitation', 'Front Office Phone Calls Academics', 'Front Office Phone Calls Admin', 'Front Office Phone Calls General', 'Visitor Log', 'BSNL Phone Status', 'Materials Inward', 'Materials Outward', 'Materials Movement', 'Returnable Material Tracking', 'Returnable Goods Report', 'Campus Camera Status', 'Vehicle Camera Status', 'Bus AC Camera Status', 'GPS Monitoring', 'Issues Identified Monitoring', 'Teachers Late Reporting', 'Biometrics Access Card Punching', 'Water TDS Deviation', 'Testing Cleaning General', 'Testing Cleaning Pool', 'Transport Attendance', 'Transport Ac Status', 'Late Reporting', 'Maintenance Service Issues', 'Car Maintenance Cleaning', 'Vehicle Renewals Delays', 'Delayed Halt', 'FC Renewal', 'Road Tax', 'Permit', 'Insurance', 'Special Trip', 'AC Temp First Floor', 'AC Temp Second Floor', 'AC Temp Third Floor', 'AC Temp Ground Floor', 'Maintenance Labor', 'Motor Pest Control', 'AC Temp Deviation', 'Electricity Consumption', 'EB Details', 'Solar Details', 'Genset Details', 'Security Count Verification', 'Security Attendance Replacement', 'Security Info Note', 'Govt Officials IN/OUT', 'Security Materials Inward', 'Security Materials Outward', 'Security Transport Verification', 'Documents Movement', 'Government Official Documents', 'Digital Marketing Thoorigai Social Media', 'Digital Marketing Thoorigai Website Updates', 'Digital Marketing Md Social Media', 'Intercom Maintenance', 'Health Check Up', 'Net Connectivity / Print Details', 'General Maintenance IT Products', 'Calendar Schedule Admin', 'Calendar Schedule House Keeping', 'Calendar Schedule Security', 'Calendar Schedule Transport', 'Training Attendance Academics Jr', 'Training Attendance Academics Sr', 'Training Attendance Admin', 'Training Attendance Drivers', 'Training Attendance Securities', 'Training Attendance Drivers Sub', 'Training Attendance Conductors', 'Training Details CBSE/ CIS/ EXTERNAL']
    team2_all_well = [
        team2_issue_nature['jr_school']['all_well'],
        team2_issue_nature['sr_school']['all_well'],
        team2_issue_nature['eca']['all_well'],
        team2_issue_nature['admin_staff']['all_well'],
        team2_issue_nature['drivers']['all_well'],
        team2_issue_nature['security']['all_well'],
        team2_issue_nature['housekeeping']['all_well'],
        team2_issue_nature['conductors']['all_well'],
        team2_issue_nature['recruitment_academic']['all_well'],
        team2_issue_nature['recruitment_admin']['all_well'],
        team2_issue_nature['pending_academic']['all_well'],
        team2_issue_nature['pending_admin']['all_well'],
        team2_issue_nature['interview_schedule']['all_well'],
        team2_issue_nature['exit_information']['all_well'],
        team2_issue_nature['issues_staff_concerns']['all_well'],
        team2_issue_nature['kural_recitation']['all_well'],
        team2_issue_nature['front_office_phone_calls_academics']['all_well'],
        team2_issue_nature['front_office_phone_calls_admin']['all_well'],
        team2_issue_nature['front_office_phone_calls_general']['all_well'],
        team2_issue_nature['visitor_log']['all_well'],
        team2_issue_nature['bsnl_phone_status']['all_well'],
        team2_issue_nature['materials_inward']['all_well'],
        team2_issue_nature['materials_outward']['all_well'],
        team2_issue_nature['materials_movement']['all_well'],
        team2_issue_nature['returnable_material_tracking']['all_well'],
        team2_issue_nature['returnable_goods_report']['all_well'],
        team2_issue_nature['campus_camera_status']['all_well'],
        team2_issue_nature['vehicle_camera_status']['all_well'],
        team2_issue_nature['bus_ac_camera_status']['all_well'],
        team2_issue_nature['gps_monitoring']['all_well'],
        team2_issue_nature['issues_identified_monitoring']['all_well'],
        team2_issue_nature['teachers_late_reporting']['all_well'],
        team2_issue_nature['biometrics_access_card_punching']['all_well'],
        team2_issue_nature['water_tds_deviation']['all_well'],
        team2_issue_nature['testing_cleaning_general']['all_well'],
        team2_issue_nature['testing_cleaning_pool']['all_well'],
        team2_issue_nature['transport_attendance']['all_well'],
        team2_issue_nature['transport_ac_status']['all_well'],
        team2_issue_nature['late_reporting']['all_well'],
        team2_issue_nature['maintenance_service_issues']['all_well'],
        team2_issue_nature['car_maintenance_cleaning']['all_well'],
        team2_issue_nature['vehicle_renewals_delays']['all_well'],
        team2_issue_nature['delayed_halt']['all_well'],
        team2_issue_nature['fc_renewal']['all_well'],
        team2_issue_nature['road_tax']['all_well'],
        team2_issue_nature['permit']['all_well'],
        team2_issue_nature['insurance']['all_well'],
        team2_issue_nature['special_trip']['all_well'],
        team2_issue_nature['ac_temp_first_floor']['all_well'],
        team2_issue_nature['ac_temp_second_floor']['all_well'],
        team2_issue_nature['ac_temp_third_floor']['all_well'],
        team2_issue_nature['ac_temp_ground_floor']['all_well'],
        team2_issue_nature['maintenance_labor']['all_well'],
        team2_issue_nature['motor']['all_well'],
        team2_issue_nature['pest_control']['all_well'],
        team2_issue_nature['ac_temp_deviation']['all_well'],
        team2_issue_nature['electricity_consumption']['all_well'],
        team2_issue_nature['eb_details']['all_well'],
        team2_issue_nature['solar_details']['all_well'],
        team2_issue_nature['genset_details']['all_well'],
        team2_issue_nature['security_count_verification']['all_well'],
        team2_issue_nature['security_attendance_replacement']['all_well'],
        team2_issue_nature['security_info_note']['all_well'],
        team2_issue_nature['govt_officials_inout']['all_well'],
        team2_issue_nature['security_materials_inward']['all_well'],
        team2_issue_nature['security_materials_outward']['all_well'],
        team2_issue_nature['security_transport_verification']['all_well'],
        team2_issue_nature['documents_movement']['all_well'],
        team2_issue_nature['govt_official_documents']['all_well'],
        team2_issue_nature['digital_marketing_thoorigai_social_media']['all_well'],
        team2_issue_nature['digital_marketing_thoorigai_website_updates']['all_well'],
        team2_issue_nature['digital_marketing_md_social_media']['all_well'],
        team2_issue_nature['intercom_maintenance']['all_well'],
        team2_issue_nature['health_check_up']['all_well'],
        team2_issue_nature['net_connectivity_print_details']['all_well'],
        team2_issue_nature['general_maintenance_it_products']['all_well'],
        team2_issue_nature['calendar_schedule_admin']['all_well'],
        team2_issue_nature['calendar_schedule_house_keeping']['all_well'],
        team2_issue_nature['calendar_schedule_security']['all_well'],
        team2_issue_nature['calendar_schedule_transport']['all_well'],
        team2_issue_nature['training_attendance_academics_jr']['all_well'],
        team2_issue_nature['training_attendance_academics_sr']['all_well'],
        team2_issue_nature['training_attendance_admin']['all_well'],
        team2_issue_nature['training_attendance_drivers']['all_well'],
        team2_issue_nature['training_attendance_securities']['all_well'],
        team2_issue_nature['training_attendance_drivers_sub']['all_well'],
        team2_issue_nature['training_attendance_conductors']['all_well'],
        team2_issue_nature['training_details_cbse_cis_external']['all_well']
    ]
    team2_manageable = [
        team2_issue_nature['jr_school']['manageable'],
        team2_issue_nature['sr_school']['manageable'],
        team2_issue_nature['eca']['manageable'],
        team2_issue_nature['admin_staff']['manageable'],
        team2_issue_nature['drivers']['manageable'],
        team2_issue_nature['security']['manageable'],
        team2_issue_nature['housekeeping']['manageable'],
        team2_issue_nature['conductors']['manageable'],
        team2_issue_nature['recruitment_academic']['manageable'],
        team2_issue_nature['recruitment_admin']['manageable'],
        team2_issue_nature['pending_academic']['manageable'],
        team2_issue_nature['pending_admin']['manageable'],
        team2_issue_nature['interview_schedule']['manageable'],
        team2_issue_nature['exit_information']['manageable'],
        team2_issue_nature['issues_staff_concerns']['manageable'],
        team2_issue_nature['kural_recitation']['manageable'],
        team2_issue_nature['front_office_phone_calls_academics']['manageable'],
        team2_issue_nature['front_office_phone_calls_admin']['manageable'],
        team2_issue_nature['front_office_phone_calls_general']['manageable'],
        team2_issue_nature['visitor_log']['manageable'],
        team2_issue_nature['bsnl_phone_status']['manageable'],
        team2_issue_nature['materials_inward']['manageable'],
        team2_issue_nature['materials_outward']['manageable'],
        team2_issue_nature['materials_movement']['manageable'],
        team2_issue_nature['returnable_material_tracking']['manageable'],
        team2_issue_nature['returnable_goods_report']['manageable'],
        team2_issue_nature['campus_camera_status']['manageable'],
        team2_issue_nature['vehicle_camera_status']['manageable'],
        team2_issue_nature['bus_ac_camera_status']['manageable'],
        team2_issue_nature['gps_monitoring']['manageable'],
        team2_issue_nature['issues_identified_monitoring']['manageable'],
        team2_issue_nature['teachers_late_reporting']['manageable'],
        team2_issue_nature['biometrics_access_card_punching']['manageable'],
        team2_issue_nature['water_tds_deviation']['manageable'],
        team2_issue_nature['testing_cleaning_general']['manageable'],
        team2_issue_nature['testing_cleaning_pool']['manageable'],
        team2_issue_nature['transport_attendance']['manageable'],
        team2_issue_nature['transport_ac_status']['manageable'],
        team2_issue_nature['late_reporting']['manageable'],
        team2_issue_nature['maintenance_service_issues']['manageable'],
        team2_issue_nature['car_maintenance_cleaning']['manageable'],
        team2_issue_nature['vehicle_renewals_delays']['manageable'],
        team2_issue_nature['delayed_halt']['manageable'],
        team2_issue_nature['fc_renewal']['manageable'],
        team2_issue_nature['road_tax']['manageable'],
        team2_issue_nature['permit']['manageable'],
        team2_issue_nature['insurance']['manageable'],
        team2_issue_nature['special_trip']['manageable'],
        team2_issue_nature['ac_temp_first_floor']['manageable'],
        team2_issue_nature['ac_temp_second_floor']['manageable'],
        team2_issue_nature['ac_temp_third_floor']['manageable'],
        team2_issue_nature['ac_temp_ground_floor']['manageable'],
        team2_issue_nature['maintenance_labor']['manageable'],
        team2_issue_nature['motor']['manageable'],
        team2_issue_nature['pest_control']['manageable'],
        team2_issue_nature['ac_temp_deviation']['manageable'],
        team2_issue_nature['electricity_consumption']['manageable'],
        team2_issue_nature['eb_details']['manageable'],
        team2_issue_nature['solar_details']['manageable'],
        team2_issue_nature['genset_details']['manageable'],
        team2_issue_nature['security_count_verification']['manageable'],
        team2_issue_nature['security_attendance_replacement']['manageable'],
        team2_issue_nature['security_info_note']['manageable'],
        team2_issue_nature['govt_officials_inout']['manageable'],
        team2_issue_nature['security_materials_inward']['manageable'],
        team2_issue_nature['security_materials_outward']['manageable'],
        team2_issue_nature['security_transport_verification']['manageable'],
        team2_issue_nature['documents_movement']['manageable'],
        team2_issue_nature['govt_official_documents']['manageable'],
        team2_issue_nature['digital_marketing_thoorigai_social_media']['manageable'],
        team2_issue_nature['digital_marketing_thoorigai_website_updates']['manageable'],
        team2_issue_nature['digital_marketing_md_social_media']['manageable'],
        team2_issue_nature['intercom_maintenance']['manageable'],
        team2_issue_nature['health_check_up']['manageable'],
        team2_issue_nature['net_connectivity_print_details']['manageable'],
        team2_issue_nature['general_maintenance_it_products']['manageable'],
        team2_issue_nature['calendar_schedule_admin']['manageable'],
        team2_issue_nature['calendar_schedule_house_keeping']['manageable'],
        team2_issue_nature['calendar_schedule_security']['manageable'],
        team2_issue_nature['calendar_schedule_transport']['manageable'],
        team2_issue_nature['training_attendance_academics_jr']['manageable'],
        team2_issue_nature['training_attendance_academics_sr']['manageable'],
        team2_issue_nature['training_attendance_admin']['manageable'],
        team2_issue_nature['training_attendance_drivers']['manageable'],
        team2_issue_nature['training_attendance_securities']['manageable'],
        team2_issue_nature['training_attendance_drivers_sub']['manageable'],
        team2_issue_nature['training_attendance_conductors']['manageable'],
        team2_issue_nature['training_details_cbse_cis_external']['manageable']
    ]
    team2_critical = [
        team2_issue_nature['jr_school']['critical'],
        team2_issue_nature['sr_school']['critical'],
        team2_issue_nature['eca']['critical'],
        team2_issue_nature['admin_staff']['critical'],
        team2_issue_nature['drivers']['critical'],
        team2_issue_nature['security']['critical'],
        team2_issue_nature['housekeeping']['critical'],
        team2_issue_nature['conductors']['critical'],
        team2_issue_nature['recruitment_academic']['critical'],
        team2_issue_nature['recruitment_admin']['critical'],
        team2_issue_nature['pending_academic']['critical'],
        team2_issue_nature['pending_admin']['critical'],
        team2_issue_nature['interview_schedule']['critical'],
        team2_issue_nature['exit_information']['critical'],
        team2_issue_nature['issues_staff_concerns']['critical'],
        team2_issue_nature['kural_recitation']['critical'],
        team2_issue_nature['front_office_phone_calls_academics']['critical'],
        team2_issue_nature['front_office_phone_calls_admin']['critical'],
        team2_issue_nature['front_office_phone_calls_general']['critical'],
        team2_issue_nature['visitor_log']['critical'],
        team2_issue_nature['bsnl_phone_status']['critical'],
        team2_issue_nature['materials_inward']['critical'],
        team2_issue_nature['materials_outward']['critical'],
        team2_issue_nature['materials_movement']['critical'],
        team2_issue_nature['returnable_material_tracking']['critical'],
        team2_issue_nature['returnable_goods_report']['critical'],
        team2_issue_nature['campus_camera_status']['critical'],
        team2_issue_nature['vehicle_camera_status']['critical'],
        team2_issue_nature['bus_ac_camera_status']['critical'],
        team2_issue_nature['gps_monitoring']['critical'],
        team2_issue_nature['issues_identified_monitoring']['critical'],
        team2_issue_nature['teachers_late_reporting']['critical'],
        team2_issue_nature['biometrics_access_card_punching']['critical'],
        team2_issue_nature['water_tds_deviation']['critical'],
        team2_issue_nature['testing_cleaning_general']['critical'],
        team2_issue_nature['testing_cleaning_pool']['critical'],
        team2_issue_nature['transport_attendance']['critical'],
        team2_issue_nature['transport_ac_status']['critical'],
        team2_issue_nature['late_reporting']['critical'],
        team2_issue_nature['maintenance_service_issues']['critical'],
        team2_issue_nature['car_maintenance_cleaning']['critical'],
        team2_issue_nature['vehicle_renewals_delays']['critical'],
        team2_issue_nature['delayed_halt']['critical'],
        team2_issue_nature['fc_renewal']['critical'],
        team2_issue_nature['road_tax']['critical'],
        team2_issue_nature['permit']['critical'],
        team2_issue_nature['insurance']['critical'],
        team2_issue_nature['special_trip']['critical'],
        team2_issue_nature['ac_temp_first_floor']['critical'],
        team2_issue_nature['ac_temp_second_floor']['critical'],
        team2_issue_nature['ac_temp_third_floor']['critical'],
        team2_issue_nature['ac_temp_ground_floor']['critical'],
        team2_issue_nature['maintenance_labor']['critical'],
        team2_issue_nature['motor']['critical'],
        team2_issue_nature['pest_control']['critical'],
        team2_issue_nature['ac_temp_deviation']['critical'],
        team2_issue_nature['electricity_consumption']['critical'],
        team2_issue_nature['eb_details']['critical'],
        team2_issue_nature['solar_details']['critical'],
        team2_issue_nature['genset_details']['critical'],
        team2_issue_nature['security_count_verification']['critical'],
        team2_issue_nature['security_attendance_replacement']['critical'],
        team2_issue_nature['security_info_note']['critical'],
        team2_issue_nature['govt_officials_inout']['critical'],
        team2_issue_nature['security_materials_inward']['critical'],
        team2_issue_nature['security_materials_outward']['critical'],
        team2_issue_nature['security_transport_verification']['critical'],
        team2_issue_nature['documents_movement']['critical'],
        team2_issue_nature['govt_official_documents']['critical'],
        team2_issue_nature['digital_marketing_thoorigai_social_media']['critical'],
        team2_issue_nature['digital_marketing_thoorigai_website_updates']['critical'],
        team2_issue_nature['digital_marketing_md_social_media']['critical'],
        team2_issue_nature['intercom_maintenance']['critical'],
        team2_issue_nature['health_check_up']['critical'],
        team2_issue_nature['net_connectivity_print_details']['critical'],
        team2_issue_nature['general_maintenance_it_products']['critical'],
        team2_issue_nature['calendar_schedule_admin']['critical'],
        team2_issue_nature['calendar_schedule_house_keeping']['critical'],
        team2_issue_nature['calendar_schedule_security']['critical'],
        team2_issue_nature['calendar_schedule_transport']['critical'],
        team2_issue_nature['training_attendance_academics_jr']['critical'],
        team2_issue_nature['training_attendance_academics_sr']['critical'],
        team2_issue_nature['training_attendance_admin']['critical'],
        team2_issue_nature['training_attendance_drivers']['critical'],
        team2_issue_nature['training_attendance_securities']['critical'],
        team2_issue_nature['training_attendance_drivers_sub']['critical'],
        team2_issue_nature['training_attendance_conductors']['critical'],
        team2_issue_nature['training_details_cbse_cis_external']['critical']
    ]
    

    
    # Team 2 Chart - Premium styling with enhanced design
    num_departments = len(team2_departments)
    n_splits = 3
    split_size = (num_departments + n_splits - 1) // n_splits  # ceil division
    team2_chart_images = []
    
    for i in range(n_splits):
        start = i * split_size
        end = min((i + 1) * split_size, num_departments)
        sub_departments = team2_departments[start:end]
        sub_all_well = team2_all_well[start:end]
        sub_manageable = team2_manageable[start:end]
        sub_critical = team2_critical[start:end]
        
        x = np.arange(len(sub_departments))
        width = 0.25
        
        # Create premium figure with enhanced styling
        fig, ax = plt.subplots(figsize=(18, 10), facecolor=colors['background'])
        fig.patch.set_facecolor(colors['background'])
        
        # Add subtle background gradient effect
        ax.set_facecolor(colors['background'])
        
        # Create premium bars with enhanced styling
        bars1 = ax.bar(x - width, sub_all_well, width, 
                      label=f'All Well ({sum(sub_all_well)})', 
                      color=colors['all_well']['primary'], 
                      alpha=0.95, 
                      edgecolor=colors['all_well']['dark'], 
                      linewidth=1.2,
                      zorder=3)
        
        bars2 = ax.bar(x, sub_manageable, width, 
                      label=f'Manageable ({sum(sub_manageable)})', 
                      color=colors['manageable']['primary'], 
                      alpha=0.95, 
                      edgecolor=colors['manageable']['dark'], 
                      linewidth=1.2,
                      zorder=3)
        
        bars3 = ax.bar(x + width, sub_critical, width, 
                      label=f'Critical ({sum(sub_critical)})', 
                      color=colors['critical']['primary'], 
                      alpha=0.95, 
                      edgecolor=colors['critical']['dark'], 
                      linewidth=1.2,
                      zorder=3)
        
        # Enhanced styling
        ax.set_xlabel('Department', fontsize=16, fontweight='bold', color=colors['text'], labelpad=20)
        ax.set_ylabel('Issue Count', fontsize=16, fontweight='bold', color=colors['text'], labelpad=20)
        ax.set_title(f'Team 2 - Departments {start+1}-{end}', fontsize=22, fontweight='bold', 
                    pad=30, color=colors['text'])
        
        # Premium axis styling
        ax.set_xticks(x)
        ax.set_xticklabels(sub_departments, rotation=45, fontsize=10, ha='right', color=colors['text_secondary'])
        ax.tick_params(axis='both', colors=colors['text_secondary'], labelsize=11)
        
        # Enhanced grid with premium styling
        ax.grid(axis='y', linestyle='--', alpha=0.4, color=colors['grid'], linewidth=0.8, zorder=1)
        ax.set_axisbelow(True)
        
        # Premium legend with enhanced styling
        legend = ax.legend(fontsize=13, frameon=True, 
                          facecolor=colors['background'], 
                          edgecolor=colors['border'],
                          borderpad=1.2,
                          shadow=True,
                          fancybox=True,
                          loc='upper right')
        
        for text in legend.get_texts():
            text.set_color(colors['text'])
            text.set_fontweight('bold')
            
        # Enhanced value labels with premium styling
        for bars in [bars1, bars2, bars3]:
            for bar in bars:
                height = bar.get_height()
                if height > 0:
                    ax.text(bar.get_x() + bar.get_width()/2, height + 0.1, 
                           f'{int(height)}', 
                           ha='center', va='bottom', 
                           fontsize=10, fontweight='bold', 
                           color=colors['text'],
                           bbox=dict(boxstyle="round,pad=0.3", 
                                    facecolor=colors['background'], 
                                    edgecolor=colors['border'],
                                    alpha=0.8))
        
        # Add subtle border around the plot
        for spine in ax.spines.values():
            spine.set_color(colors['border'])
            spine.set_linewidth(1.5)
        
        plt.tight_layout(pad=3.0)
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=300, facecolor=colors['background'], 
                    bbox_inches='tight', edgecolor='none')
        buf.seek(0)
        team2_chart_images.append(base64.b64encode(buf.read()).decode('utf-8'))
        plt.close(fig)
    
    team2_chart_image1, team2_chart_image2, team2_chart_image3 = team2_chart_images

# Prepare data
    teams = ['Team 1', 'Team 2', 'Team 3']
    all_well = [team1_issue_nature['overall']['all_well'], team2_issue_nature['overall']['all_well'], team3_issue_nature['overall']['all_well']]
    manageable = [team1_issue_nature['overall']['manageable'], team2_issue_nature['overall']['manageable'], team3_issue_nature['overall']['manageable']]
    critical = [team1_issue_nature['overall']['critical'], team2_issue_nature['overall']['critical'], team3_issue_nature['overall']['critical']]

    overall_all_well = sum(all_well)
    overall_manageable = sum(manageable)
    overall_critical = sum(critical)
    total = overall_all_well + overall_manageable + overall_critical

# Setup premium side-by-side subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10), facecolor=colors['background'])
    fig.patch.set_facecolor(colors['background'])

## --- Premium Bar Chart: Combined Teams ---
    x = np.arange(len(teams))
    width = 0.25
    
    # Create premium bars with enhanced styling
    bars1 = ax1.bar(x - width, all_well, width, 
                   label=f'All Well ({overall_all_well})', 
                   color=colors['all_well']['primary'], 
                   alpha=0.95, 
                   edgecolor=colors['all_well']['dark'], 
                   linewidth=1.2,
                   zorder=3)
    
    bars2 = ax1.bar(x, manageable, width, 
                   label=f'Manageable ({overall_manageable})', 
                   color=colors['manageable']['primary'], 
                   alpha=0.95, 
                   edgecolor=colors['manageable']['dark'], 
                   linewidth=1.2,
                   zorder=3)
    
    bars3 = ax1.bar(x + width, critical, width, 
                   label=f'Critical ({overall_critical})', 
                   color=colors['critical']['primary'], 
                   alpha=0.95, 
                   edgecolor=colors['critical']['dark'], 
                   linewidth=1.2,
                   zorder=3)

    # Enhanced styling for bar chart
    ax1.set_title('Team Performance Overview', fontsize=20, fontweight='bold', pad=25, color=colors['text'])
    ax1.set_xlabel('Teams', fontsize=16, fontweight='bold', color=colors['text'], labelpad=20)
    ax1.set_ylabel('Issue Count', fontsize=16, fontweight='bold', color=colors['text'], labelpad=20)
    ax1.set_xticks(x)
    ax1.set_xticklabels(teams, fontsize=14, fontweight='bold', color=colors['text'])
    ax1.tick_params(axis='both', colors=colors['text_secondary'], labelsize=12)
    
    # Enhanced grid with premium styling
    ax1.grid(axis='y', linestyle='--', alpha=0.4, color=colors['grid'], linewidth=0.8, zorder=1)
    ax1.set_axisbelow(True)
    
    # Premium legend with enhanced styling
    legend1 = ax1.legend(fontsize=13, frameon=True, 
                         facecolor=colors['background'], 
                         edgecolor=colors['border'],
                         borderpad=1.2,
                         shadow=True,
                         fancybox=True,
                         loc='upper right')
    
    for text in legend1.get_texts():
        text.set_color(colors['text'])
        text.set_fontweight('bold')

    # Enhanced data labels with premium styling
    for bars in [bars1, bars2, bars3]:
        for bar in bars:
            height = bar.get_height()
            if height > 0:
                ax1.text(bar.get_x() + bar.get_width()/2, height + 0.5, 
                        str(int(height)), 
                        ha='center', fontsize=12, fontweight='bold', 
                        color=colors['text'],
                        bbox=dict(boxstyle="round,pad=0.3", 
                                 facecolor=colors['background'], 
                                 edgecolor=colors['border'],
                                 alpha=0.8))

## --- Premium Pie Chart: Overall Distribution ---
    if total > 0:
        sizes = [overall_all_well, overall_manageable, overall_critical]
        labels = [f'All Well\n({overall_all_well})', f'Manageable\n({overall_manageable})', f'Critical\n({overall_critical})']
        pie_colors = [colors['all_well']['primary'], colors['manageable']['primary'], colors['critical']['primary']]
        
        # Create premium pie chart with enhanced styling
        wedges, texts, autotexts = ax2.pie(
            sizes, labels=labels, colors=pie_colors,
            autopct=lambda pct: f'{pct:.1f}%\n({int(pct*total/100)})',
            startangle=140, 
            textprops={'fontsize': 13, 'color': colors['text'], 'fontweight': 'bold'}, 
            wedgeprops=dict(width=0.6, edgecolor=colors['background'], linewidth=2))

        # Enhanced percentage text styling
        for autotext in autotexts:
            autotext.set_fontweight('bold')
            autotext.set_color(colors['text'])
            autotext.set_fontsize(12)
        
        ax2.set_title('Overall Issue Distribution', fontsize=20, fontweight='bold', pad=25, color=colors['text'])
    else:
        ax2.text(0.5, 0.5, 'No data available', ha='center', va='center', 
                fontsize=16, color=colors['text_secondary'], fontweight='bold')
        ax2.set_title('Overall Issue Distribution (No Data)', fontsize=20, fontweight='bold', 
                     pad=25, color=colors['text'])
        ax2.axis('off')

    # Add subtle borders around both plots
    for ax in [ax1, ax2]:
        for spine in ax.spines.values():
            spine.set_color(colors['border'])
            spine.set_linewidth(1.5)

    plt.tight_layout(pad=3.0)
    plt.subplots_adjust(wspace=0.2)

# Save and encode the premium combined image
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=300, facecolor=colors['background'], 
                bbox_inches='tight', edgecolor='none')
    buf.seek(0)
    combined_image = base64.b64encode(buf.read()).decode('utf-8')
    plt.close('all')

    # Team 3 Chart - Premium styling with slim bars
    team3_departments = ['Legacy Audit', 'New Audit']
    team3_all_well = [team3_issue_nature['audit_issue_nature']['all_well'], team3_issue_nature['new_audit_issue_nature']['all_well']]
    team3_manageable = [team3_issue_nature['audit_issue_nature']['manageable'], team3_issue_nature['new_audit_issue_nature']['manageable']]
    team3_critical = [team3_issue_nature['audit_issue_nature']['critical'], team3_issue_nature['new_audit_issue_nature']['critical']]
    x = np.arange(len(team3_departments))
    width = 0.15  # Reduced width for slimmer bars
    
    # Create premium figure with enhanced styling
    fig, ax = plt.subplots(figsize=(12, 8), facecolor=colors['background'])  # Reduced figure size
    fig.patch.set_facecolor(colors['background'])
    
    # Add subtle background gradient effect
    ax.set_facecolor(colors['background'])
    
    # Create slim premium bars with enhanced styling
    bars1 = ax.bar(x - width, team3_all_well, width, 
                  label=f'All Well ({sum(team3_all_well)})', 
                  color=colors['all_well']['primary'], 
                  alpha=0.95, 
                  edgecolor=colors['all_well']['dark'], 
                  linewidth=1.0,  # Slightly thinner border
                  zorder=3)
    
    bars2 = ax.bar(x, team3_manageable, width, 
                  label=f'Manageable ({sum(team3_manageable)})', 
                  color=colors['manageable']['primary'], 
                  alpha=0.95, 
                  edgecolor=colors['manageable']['dark'], 
                  linewidth=1.0,  # Slightly thinner border
                  zorder=3)
    
    bars3 = ax.bar(x + width, team3_critical, width, 
                  label=f'Critical ({sum(team3_critical)})', 
                  color=colors['critical']['primary'], 
                  alpha=0.95, 
                  edgecolor=colors['critical']['dark'], 
                  linewidth=1.0,  # Slightly thinner border
                  zorder=3)
    
    # Enhanced styling
    ax.set_xlabel('Department', fontsize=16, fontweight='bold', color=colors['text'], labelpad=20)
    ax.set_ylabel('Issue Count', fontsize=16, fontweight='bold', color=colors['text'], labelpad=20)
    ax.set_title('Team 3 - Audit Issue Analysis (Legacy & New)', fontsize=22, fontweight='bold', 
                pad=30, color=colors['text'])
    
    # Premium axis styling with better spacing for slim bars
    ax.set_xticks(x)
    ax.set_xticklabels(team3_departments, fontsize=14, fontweight='bold', color=colors['text'])
    ax.tick_params(axis='both', colors=colors['text_secondary'], labelsize=12)
    
    # Set better x-axis limits for slim bars
    ax.set_xlim(x[0] - width*2, x[-1] + width*2)
    
    # Enhanced grid with premium styling
    ax.grid(axis='y', linestyle='--', alpha=0.4, color=colors['grid'], linewidth=0.8, zorder=1)
    ax.set_axisbelow(True)
    
    # Premium legend with enhanced styling
    legend = ax.legend(fontsize=13, frameon=True, 
                      facecolor=colors['background'], 
                      edgecolor=colors['border'],
                      borderpad=1.2,
                      shadow=True,
                      fancybox=True,
                      loc='upper right')
    
    for text in legend.get_texts():
        text.set_color(colors['text'])
        text.set_fontweight('bold')
    
    # Enhanced value labels with premium styling
    for bars in [bars1, bars2, bars3]:
        for bar in bars:
            height = bar.get_height()
            if height > 0:
                ax.text(bar.get_x() + bar.get_width()/2, height + 0.1, 
                       f'{int(height)}', 
                       ha='center', va='bottom', 
                       fontsize=12, fontweight='bold', 
                       color=colors['text'],
                       bbox=dict(boxstyle="round,pad=0.3", 
                                facecolor=colors['background'], 
                                edgecolor=colors['border'],
                                alpha=0.8))
    
    # Add subtle border around the plot
    for spine in ax.spines.values():
        spine.set_color(colors['border'])
        spine.set_linewidth(1.5)
    
    plt.tight_layout(pad=3.0)
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=300, facecolor=colors['background'], 
                bbox_inches='tight', edgecolor='none')
    buf.seek(0)
    team3_chart_image = base64.b64encode(buf.read()).decode('utf-8')
    plt.close()

    # --- PDF Generation Section ---
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, PageBreak
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_CENTER
    from reportlab.lib.units import inch
    from reportlab.lib.pagesizes import letter
    from reportlab.lib import colors
    import tempfile
    import base64
    import io

    def get_dept_col_width(departments, min_width=120, max_width=220):
        max_len = max([len(str(d)) for d in departments] + [len('Department')])
        # Estimate width: 7px per char, clamp between min and max
        return min(max(min_width, max_len * 7), max_width)
    
    def calculate_table_widths(total_width=500, num_cols=5, dept_col_width=None):
        """Calculate consistent table widths for all tables"""
        if dept_col_width:
            remaining_width = total_width - dept_col_width
            other_col_width = remaining_width // (num_cols - 1)
            return [dept_col_width] + [other_col_width] * (num_cols - 1)
        else:
            return [total_width // num_cols] * num_cols

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=30, leftMargin=30, topMargin=40, bottomMargin=40)
    elements = []
    styles = getSampleStyleSheet()
    
    # Modern Typography Styles
    title_style = ParagraphStyle('title', parent=styles['Title'], fontSize=24, alignment=TA_CENTER, 
                                textColor=colors.HexColor('#1e293b'), spaceAfter=20)
    subtitle_style = ParagraphStyle('subtitle', parent=styles['Normal'], fontSize=14, alignment=TA_CENTER, 
                                   textColor=colors.HexColor('#64748b'), spaceAfter=30)
    section_header_style = ParagraphStyle('section_header', parent=styles['Heading2'], fontSize=18, 
                                         textColor=colors.HexColor('#0f172a'), spaceAfter=15, spaceBefore=25)
    subsection_header_style = ParagraphStyle('subsection_header', parent=styles['Heading3'], fontSize=14, 
                                            textColor=colors.HexColor('#334155'), spaceAfter=10, spaceBefore=20)
    normal_style = ParagraphStyle('normal', parent=styles['Normal'], fontSize=11, textColor=colors.HexColor('#475569'))
    
    # Header Section with Clean Design
    elements.append(Paragraph('QMIS DSR', title_style))
    elements.append(Paragraph('Daily Status Report', subtitle_style))
    
    # Date Information with Better Formatting
    def format_date_range():
        if start_date and end_date:
            if start_date == end_date:
                return f"Report Date: {start_date.strftime('%B %d, %Y')}"
            else:
                return f"Report Period: {start_date.strftime('%B %d, %Y')} - {end_date.strftime('%B %d, %Y')}"
        elif selected_date != 'all' and selected_date_obj:
            return f"Report Date: {selected_date_obj.strftime('%B %d, %Y')}"
        elif defaulted_to_yesterday:
            yesterday = (datetime.now() - timedelta(days=1)).date()
            return f"Report Date: {yesterday.strftime('%B %d, %Y')} (Default)"
        else:
            return "Report Period: All Time"

    date_style = ParagraphStyle('date', parent=styles['Normal'], fontSize=12, alignment=TA_CENTER, 
                               textColor=colors.HexColor('#64748b'), spaceAfter=40)
    elements.append(Paragraph(format_date_range(), date_style))
    
    # Executive Summary with Modern Card Design
    elements.append(Paragraph('Executive Summary', section_header_style))
    elements.append(Spacer(1, 0.2*inch))
    
    # Create summary cards with better visual hierarchy
    summary_cards = []
    total_issues = overall_all_well + overall_manageable + overall_critical
    
    summary_cards.append(['Total Issues', str(total_issues), '#3b82f6'])
    summary_cards.append(['All Well', str(overall_all_well), '#10b981'])
    summary_cards.append(['Manageable', str(overall_manageable), '#f59e0b'])
    summary_cards.append(['Critical', str(overall_critical), '#ef4444'])
    
    # Add action summary cards if actions exist
    if all_actions:
        summary_cards.append(['Total Actions', str(action_status_counts['total_initiated']), '#8b5cf6'])
        summary_cards.append(['Actions Completed', str(action_status_counts['solved_completed']), '#06b6d4'])
        summary_cards.append(['Actions Pending', str(action_status_counts['pending']), '#f97316'])
        summary_cards.append(['Follow-up Actions', str(action_status_counts['follow_up']), '#ec4899'])
    
    # Create a 2x2 grid for summary cards
    summary_table_data = []
    for i in range(0, len(summary_cards), 2):
        row = []
        for j in range(2):
            if i + j < len(summary_cards):
                card = summary_cards[i + j]
                row.append([card[0], card[1], card[2]])
            else:
                row.append(['', '', ''])
        summary_table_data.append(row)
    
    # Create individual cards for better visual appeal
    for card in summary_cards:
        card_data = [[card[0], card[1]]]
        card_table = Table(card_data, colWidths=[120, 80])
        card_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, 0), colors.HexColor(card[2])),
            ('BACKGROUND', (1, 0), (1, 0), colors.HexColor('#f8fafc')),
            ('TEXTCOLOR', (0, 0), (0, 0), colors.white),
            ('TEXTCOLOR', (1, 0), (1, 0), colors.HexColor('#1e293b')),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
            ('ROUNDEDCORNERS', [8]),
            ('LEFTPADDING', (0, 0), (-1, -1), 15),
            ('RIGHTPADDING', (0, 0), (-1, -1), 15),
            ('TOPPADDING', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ]))
        elements.append(card_table)
        elements.append(Spacer(1, 0.15*inch))
    
    elements.append(Spacer(1, 0.3*inch))
    
    # Team Analysis with Clean Table Design
    elements.append(Paragraph('Team Performance Overview', section_header_style))
    elements.append(Spacer(1, 0.2*inch))
    
    team_data = [['Team', 'All Well', 'Manageable', 'Critical', 'Total']]
    for idx, team in enumerate(teams):
        team_data.append([
            team,
            str(all_well[idx]),
            str(manageable[idx]),
            str(critical[idx]),
            str(all_well[idx] + manageable[idx] + critical[idx])
        ])
    
    # Calculate consistent table widths
    team_table_widths = calculate_table_widths(total_width=500, num_cols=5)
    team_table = Table(team_data, colWidths=team_table_widths)
    team_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e293b')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#ffffff')),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor('#334155')),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 11),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
        ('ROUNDEDCORNERS', [6]),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 10),
    ]))
    elements.append(team_table)
    elements.append(Spacer(1, 0.4*inch))

    # ------------------------------------------------------------------
    # Forms Usage Calculation (per user)
    # ------------------------------------------------------------------
    user_form_ids = defaultdict(set)  # user_id → set(form_id)
    user_filled_counts = defaultdict(int)
    user_team_info = {}  # user_id → team_name

    # Get all users and their team info
    all_users = User.query.all()
    for user in all_users:
        team_name = user.team.team_name if user.team else 'No Team'
        user_team_info[user.user_id] = team_name
        user_filled_counts[user.user_id] = 0  # Initialize to 0

    # Iterate through every model that inherits from BaseForm
    for form_model in BaseForm.__subclasses__():
        # Query just the required fields to minimise memory usage
        rows = db.session.query(form_model.form_id, form_model.submitted_by).all()
        for fid, uid in rows:
            if fid is None or uid is None:
                continue
            user_form_ids[uid].add(fid)
            user_filled_counts[uid] += 1

    forms_usage_summary = []  # list of [user_id, username, team, filled]
    for uid, filled in user_filled_counts.items():
        ids = user_form_ids[uid]
        user_obj = User.query.get(uid)
        username = user_obj.username if user_obj else f'User {uid}'
        team_name = user_team_info.get(uid, 'No Team')
        forms_usage_summary.append([str(uid), username, team_name, str(filled)])

    # Sort by team first, then by forms filled count (ascending), then by username
    forms_usage_summary.sort(key=lambda x: (x[2], int(x[3]), x[1].lower()))

    total_unique_users = len(user_filled_counts)
    total_submissions = sum(user_filled_counts.values())

    # ------------------------------------------------------------------
    # Forms Usage Section in PDF
    # ------------------------------------------------------------------
    if forms_usage_summary:
        elements.append(PageBreak())
        elements.append(Paragraph('User Activity & Forms Usage', section_header_style))
        elements.append(Spacer(1, 0.2*inch))
        
        # Summary statistics with modern design
        summary_stats = [
            ['Total Users', str(total_unique_users), '#3b82f6'],
            ['Total Submissions', str(total_submissions), '#10b981']
        ]
        
        for stat in summary_stats:
            stat_data = [[stat[0], stat[1]]]
            stat_table = Table(stat_data, colWidths=[100, 80])
            stat_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, 0), colors.HexColor(stat[2])),
                ('BACKGROUND', (1, 0), (1, 0), colors.HexColor('#f8fafc')),
                ('TEXTCOLOR', (0, 0), (0, 0), colors.white),
                ('TEXTCOLOR', (1, 0), (1, 0), colors.HexColor('#1e293b')),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 11),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
                ('ROUNDEDCORNERS', [6]),
                ('LEFTPADDING', (0, 0), (-1, -1), 12),
                ('RIGHTPADDING', (0, 0), (-1, -1), 12),
                ('TOPPADDING', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ]))
            elements.append(stat_table)
            elements.append(Spacer(1, 0.1*inch))
        
        elements.append(Spacer(1, 0.2*inch))

        usage_table_data = [['User ID', 'Username', 'Team', 'Forms Filled']] + forms_usage_summary
        usage_table_widths = calculate_table_widths(total_width=500, num_cols=4)
        usage_table = Table(usage_table_data, colWidths=usage_table_widths)
        usage_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#059669')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#ffffff')),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor('#334155')),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
            ('ROUNDEDCORNERS', [6]),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
        ]))
        elements.append(usage_table)
        elements.append(Spacer(1, 0.4*inch))

    # ------------------------------------------------------------------
    # Action Statistics Section in PDF
    # ------------------------------------------------------------------
    if all_actions:
        elements.append(PageBreak())
        elements.append(Paragraph('Action Management Statistics', section_header_style))
        elements.append(Spacer(1, 0.2*inch))
        
        # Overall Action Summary
        elements.append(Paragraph('Overall Action Summary', subsection_header_style))
        elements.append(Spacer(1, 0.15*inch))
        
        action_summary_stats = [
            ['Total Actions Initiated', str(action_status_counts['total_initiated']), '#3b82f6'],
            ['Actions Completed/Solved', str(action_status_counts['solved_completed']), '#10b981'],
            ['Actions Pending', str(action_status_counts['pending']), '#f59e0b'],
            ['Actions In Progress', str(action_status_counts['in_progress']), '#8b5cf6'],
            ['Follow-up Actions', str(action_status_counts['follow_up']), '#ef4444']
        ]
        
        for stat in action_summary_stats:
            stat_data = [[stat[0], stat[1]]]
            stat_table = Table(stat_data, colWidths=[150, 80])
            stat_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, 0), colors.HexColor(stat[2])),
                ('BACKGROUND', (1, 0), (1, 0), colors.HexColor('#f8fafc')),
                ('TEXTCOLOR', (0, 0), (0, 0), colors.white),
                ('TEXTCOLOR', (1, 0), (1, 0), colors.HexColor('#1e293b')),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 11),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
                ('ROUNDEDCORNERS', [6]),
                ('LEFTPADDING', (0, 0), (-1, -1), 12),
                ('RIGHTPADDING', (0, 0), (-1, -1), 12),
                ('TOPPADDING', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ]))
            elements.append(stat_table)
            elements.append(Spacer(1, 0.1*inch))
        
        elements.append(Spacer(1, 0.2*inch))

        # Action Priority Distribution
        elements.append(Paragraph('Action Priority Distribution', subsection_header_style))
        elements.append(Spacer(1, 0.15*inch))
        
        priority_data = [['Priority', 'Count', 'Percentage']]
        total_actions = action_status_counts['total_initiated']
        for priority, count in priority_stats.items():
            percentage = (count / total_actions * 100) if total_actions > 0 else 0
            priority_data.append([priority, str(count), f'{percentage:.1f}%'])
        
        priority_table = Table(priority_data, colWidths=[120, 80, 100])
        priority_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#7c3aed')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#ffffff')),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor('#334155')),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
            ('ROUNDEDCORNERS', [6]),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
        ]))
        elements.append(priority_table)
        elements.append(Spacer(1, 0.3*inch))

        # Team Action Statistics
        elements.append(Paragraph('Team Action Statistics', subsection_header_style))
        elements.append(Spacer(1, 0.15*inch))
        
        team_action_data = [['Team', 'Assigned', 'Created', 'Completed', 'Pending', 'Follow-up', 'Total']]
        for team_name, stats in team_action_stats.items():
            team_action_data.append([
                team_name,
                str(stats['assigned']),
                str(stats['created']),
                str(stats['completed']),
                str(stats['pending']),
                str(stats['follow_up']),
                str(stats['total'])
            ])
        
        team_action_table = Table(team_action_data, colWidths=[80, 70, 70, 70, 70, 70, 70])
        team_action_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#dc2626')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#ffffff')),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor('#334155')),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
            ('ROUNDEDCORNERS', [6]),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
        ]))
        elements.append(team_action_table)
        elements.append(Spacer(1, 0.3*inch))

        # Individual Member Action Statistics
        elements.append(Paragraph('Individual Member Action Statistics', subsection_header_style))
        elements.append(Spacer(1, 0.15*inch))
        
        member_action_data = [['User ID', 'Username', 'Team', 'Assigned', 'Created', 'Completed', 'Pending', 'In Progress', 'Follow-up']]
        for member in member_action_stats:
            member_action_data.append([
                str(member['user_id']),
                member['username'],
                member['team'],
                str(member['assigned']),
                str(member['created']),
                str(member['completed']),
                str(member['pending']),
                str(member['in_progress']),
                str(member['follow_up'])
            ])
        
        member_action_table = Table(member_action_data, colWidths=[50, 80, 60, 60, 60, 60, 60, 60, 60])
        member_action_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#059669')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#ffffff')),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor('#334155')),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
            ('ROUNDEDCORNERS', [6]),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 5),
        ]))
        elements.append(member_action_table)
        elements.append(Spacer(1, 0.4*inch))

    # Charts Section with Better Organization
    elements.append(PageBreak())
    elements.append(Paragraph('Data Visualizations', section_header_style))
    elements.append(Spacer(1, 0.2*inch))
    
    def add_chart_image(base64_img, caption):
        img_data = base64.b64decode(base64_img)
        with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp_img:
            tmp_img.write(img_data)
            tmp_img.flush()
            img = Image(tmp_img.name, width=6*inch, height=3*inch)
            elements.append(img)
            elements.append(Paragraph(caption, subsection_header_style))
            elements.append(Spacer(1, 0.3*inch))

    add_chart_image(combined_image, 'Overall Issue Distribution & Team Comparison')
    add_chart_image(team1_chart_image, 'Team 1 Department-wise Issue Nature')
    add_chart_image(team2_chart_image1, 'Team 2 Departments 1-27')
    add_chart_image(team2_chart_image2, 'Team 2 Departments 28-54')
    add_chart_image(team2_chart_image3, 'Team 2 Departments 55-81')
    add_chart_image(team3_chart_image, 'Team 3 Audit Issue Analysis (Legacy & New)')

    elements.append(PageBreak())

    # Detailed Department Analysis with Clean Design
    elements.append(Paragraph('Detailed Department Analysis', section_header_style))
    elements.append(Spacer(1, 0.2*inch))
    
    # Team 1 Departments
    elements.append(Paragraph('Team 1 Departments', subsection_header_style))
    elements.append(Spacer(1, 0.15*inch))
    dept_col_width = get_dept_col_width(team1_departments)
    dept_data = [['Department', 'All Well', 'Manageable', 'Critical', 'Total']]
    for idx, dept in enumerate(team1_departments):
        dept_data.append([
            Paragraph(str(dept), normal_style),  # Use Paragraph for text wrapping
            str(team1_all_well[idx]),
            str(team1_manageable[idx]),
            str(team1_critical[idx]),
            str(team1_all_well[idx] + team1_manageable[idx] + team1_critical[idx])
        ])
    dept_table_widths = calculate_table_widths(total_width=500, num_cols=5, dept_col_width=dept_col_width)
    dept_table = Table(dept_data, colWidths=dept_table_widths, repeatRows=1)
    dept_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e293b')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#ffffff')),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor('#334155')),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('ROWHEIGHT', (0, 0), (-1, -1), 20),
        ('ROUNDEDCORNERS', [6]),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
    ]))
    elements.append(dept_table)
    elements.append(Spacer(1, 0.3*inch))

    # Team 2 Departments
    elements.append(PageBreak())
    elements.append(Paragraph('Team 2 Departments', subsection_header_style))
    elements.append(Spacer(1, 0.15*inch))
    dept2_col_width = get_dept_col_width(team2_departments)
    dept2_data = [['Department', 'All Well', 'Manageable', 'Critical', 'Total']]
    for idx, dept in enumerate(team2_departments):
        dept2_data.append([
            Paragraph(str(dept), normal_style),  # Use Paragraph for text wrapping
            str(team2_all_well[idx]),
            str(team2_manageable[idx]),
            str(team2_critical[idx]),
            str(team2_all_well[idx] + team2_manageable[idx] + team2_critical[idx])
        ])
    dept2_table_widths = calculate_table_widths(total_width=500, num_cols=5, dept_col_width=dept2_col_width)
    dept2_table = Table(dept2_data, colWidths=dept2_table_widths, repeatRows=1)
    dept2_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e293b')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#ffffff')),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor('#334155')),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('ROWHEIGHT', (0, 0), (-1, -1), 20),
        ('ROUNDEDCORNERS', [6]),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
    ]))
    elements.append(dept2_table)
    elements.append(Spacer(1, 0.3*inch))

    # Team 3 Departments
    elements.append(PageBreak())
    elements.append(Paragraph('Team 3 Departments', subsection_header_style))
    elements.append(Spacer(1, 0.15*inch))
    dept3_col_width = get_dept_col_width(team3_departments)
    dept3_data = [['Department', 'All Well', 'Manageable', 'Critical', 'Total']]
    for idx, dept in enumerate(team3_departments):
        dept3_data.append([
            Paragraph(str(dept), normal_style),  # Use Paragraph for text wrapping
            str(team3_all_well[idx]),
            str(team3_manageable[idx]),
            str(team3_critical[idx]),
            str(team3_all_well[idx] + team3_manageable[idx] + team3_critical[idx])
        ])
    dept3_table_widths = calculate_table_widths(total_width=500, num_cols=5, dept_col_width=dept3_col_width)
    dept3_table = Table(dept3_data, colWidths=dept3_table_widths, repeatRows=1)
    dept3_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e293b')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#ffffff')),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor('#334155')),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('ROWHEIGHT', (0, 0), (-1, -1), 20),
        ('ROUNDEDCORNERS', [6]),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
    ]))
    elements.append(dept3_table)
    elements.append(Spacer(1, 0.3*inch))

    # Additional Report Details
    elements.append(PageBreak())
    elements.append(Paragraph('Report Details & Analysis', section_header_style))
    elements.append(Spacer(1, 0.2*inch))
    
    # Report Generation Information
    elements.append(Paragraph('Report Information', subsection_header_style))
    elements.append(Spacer(1, 0.15*inch))
    report_info_data = [
        ['Generated By', current_user.username],
        ['User Role', current_user.role],
        ['Generation Date', datetime.now().strftime('%B %d, %Y at %I:%M %p')],
        ['Report Type', 'Daily Status Report'],
        ['Data Source', 'QMIS Database']
    ]
    
    report_info_table = Table(report_info_data, colWidths=[150, 300])
    report_info_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f1f5f9')),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#475569')),
        ('TEXTCOLOR', (1, 0), (1, -1), colors.HexColor('#1e293b')),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    elements.append(report_info_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Data Analysis Summary
    elements.append(Paragraph('Data Analysis Summary', subsection_header_style))
    elements.append(Spacer(1, 0.15*inch))
    
    # Calculate additional statistics
    total_teams = len(teams)
    avg_issues_per_team = total_issues / total_teams if total_teams > 0 else 0
    critical_percentage = (overall_critical / total_issues * 100) if total_issues > 0 else 0
    manageable_percentage = (overall_manageable / total_issues * 100) if total_issues > 0 else 0
    all_well_percentage = (overall_all_well / total_issues * 100) if total_issues > 0 else 0
    
    analysis_data = [
        ['Metric', 'Value', 'Percentage'],
        ['Total Teams', str(total_teams), '100%'],
        ['Average Issues per Team', f'{avg_issues_per_team:.1f}', f'{(avg_issues_per_team/total_issues*100):.1f}%' if total_issues > 0 else '0%'],
        ['Critical Issues', str(overall_critical), f'{critical_percentage:.1f}%'],
        ['Manageable Issues', str(overall_manageable), f'{manageable_percentage:.1f}%'],
        ['All Well Issues', str(overall_all_well), f'{all_well_percentage:.1f}%']
    ]
    
    # Add action analysis if actions exist
    if all_actions:
        action_completion_rate = (action_status_counts['solved_completed'] / action_status_counts['total_initiated'] * 100) if action_status_counts['total_initiated'] > 0 else 0
        action_pending_rate = (action_status_counts['pending'] / action_status_counts['total_initiated'] * 100) if action_status_counts['total_initiated'] > 0 else 0
        action_followup_rate = (action_status_counts['follow_up'] / action_status_counts['total_initiated'] * 100) if action_status_counts['total_initiated'] > 0 else 0
        
        analysis_data.extend([
            ['Total Actions', str(action_status_counts['total_initiated']), '100%'],
            ['Actions Completed', str(action_status_counts['solved_completed']), f'{action_completion_rate:.1f}%'],
            ['Actions Pending', str(action_status_counts['pending']), f'{action_pending_rate:.1f}%'],
            ['Follow-up Actions', str(action_status_counts['follow_up']), f'{action_followup_rate:.1f}%']
        ])
    
    analysis_table = Table(analysis_data, colWidths=[200, 100, 100])
    analysis_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e293b')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#ffffff')),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor('#334155')),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
    ]))
    elements.append(analysis_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Key Insights
    elements.append(Paragraph('Key Insights', subsection_header_style))
    elements.append(Spacer(1, 0.15*inch))
    
    insights_text = f"""
    • Total of {total_issues} issues were reported across {total_teams} teams
    • {critical_percentage:.1f}% of issues are critical and require immediate attention
    • {manageable_percentage:.1f}% of issues are manageable and can be addressed systematically
    • {all_well_percentage:.1f}% of departments are operating well
    • Average of {avg_issues_per_team:.1f} issues per team
    """
    
    # Add action insights if actions exist
    if all_actions:
        action_completion_rate = (action_status_counts['solved_completed'] / action_status_counts['total_initiated'] * 100) if action_status_counts['total_initiated'] > 0 else 0
        action_pending_rate = (action_status_counts['pending'] / action_status_counts['total_initiated'] * 100) if action_status_counts['total_initiated'] > 0 else 0
        
        insights_text += f"""
    • {action_status_counts['total_initiated']} actions were initiated during the reporting period
    • {action_status_counts['solved_completed']} actions ({action_completion_rate:.1f}%) have been completed/solved
    • {action_status_counts['pending']} actions ({action_pending_rate:.1f}%) are currently pending
    • {action_status_counts['follow_up']} follow-up actions were created to address ongoing issues
    """
    
    insights_text += f"""
    • Report generated on {datetime.now().strftime('%B %d, %Y')} at {datetime.now().strftime('%I:%M %p')}
    """
    
    insights_style = ParagraphStyle('insights', parent=normal_style, fontSize=11, 
                                   textColor=colors.HexColor('#475569'), spaceAfter=12)
    elements.append(Paragraph(insights_text, insights_style))
    elements.append(Spacer(1, 0.2*inch))
    
    # Footer
    footer_style = ParagraphStyle('footer', parent=styles['Normal'], fontSize=10, 
                                 textColor=colors.HexColor('#64748b'), alignment=TA_CENTER)
    footer_text = f"QMIS DSR Report | Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')} | Page "
    elements.append(Paragraph(footer_text, footer_style))

    # Build PDF
    doc.build(elements)
    buffer.seek(0)
    return send_file(
        buffer,
        mimetype='application/pdf',
        as_attachment=True,
        download_name='detailed_issue_report.pdf'
    )