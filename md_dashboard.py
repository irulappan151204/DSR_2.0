# md_dashboard.py

from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_file, session
from flask_login import UserMixin, login_user, login_required, logout_user, current_user
from sqlalchemy import func

from datetime import datetime, timedelta, date as dt_date
import os
from dotenv import load_dotenv
from extensions import db, login_manager, bcrypt, socketio, cache
from flask_migrate import Migrate
from commands import create_admin_command
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from io import BytesIO
from fpdf import FPDF
from statistics_routes import statistics_bp
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from zoneinfo import ZoneInfo
from models import User, Team, Issue, Report, Team1CalendarSchedule, Team1StudentAttendance, Team1ParentConcernDetail, Team1ASAActivities, Team1ASASports, Team1ASAGeneral, Team1StudentGrooming, Team1StudentLateComing, Team1AdmissionStatus, Team1TransferCertificate, Team1ParentActivity, Team1ParentVisit, Team1ExamSchedule, Team1ExternalInfo, Team1SickBay, Team1HomeSchoolComm, Team1Disciplinary, Team1Logistics, Team1CompetitionCert, Team1StaffConcern, Team1StudentConcern, Team1ParentConcern, Team1AEPAttendance, Team1ExtendedClassAttendance, Team1TrainingSession, Team1WeeklyMeeting, Team1SpecialEducation, Team1Hostel, Team1SEC, Team1SchoolCounsellor, Team1Scholorius,Team2HRAttendance, Team2TotalHRAttendance, Team2AdminAttendance, Team2RecruitmentActivity, Team2PendingRecruitment, Team2RecruitmentPipeline, Team2StaffStatusUpdates, Team2SalaryPending, Team2PoliceVerification, Team2InterviewSchedule, Team2ExitInformation, Team2IssuesStaffConcerns, Team2KuralRecitation, Team2FrontOfficePhoneCalls, Team2VisitorLog, Team2BSNLPhoneStatus, Team2MaterialsInward, Team2MaterialsOutward, Team2MaterialsMovement, Team2ReturnableMaterialTracking, Team2ReturnableGoodsReport, Team2CampusCameraStatus, Team2VehicleCameraStatus, Team2BusACCameraStatus, Team2GPSMonitoring, Team2IssuesIdentifiedMonitoring, Team2IssuesIdentifiedControlRoom, Team2CameraFootageEntry,  Team2BiometricsAccessCardPunching, Team2WaterTDSDeviation, Team2TestingCleaning, Team2PoolTesting, Team2WashroomCleanliness, Team2TransportAttendance, Team2ACWorkingStatus, Team2LateReporting, Team2MaintenanceServiceIssues, Team2CarMaintenanceCleaning,  Team2VehicleRenewalsDelays, Team2SpecialTrip, Team2ParentConcernDetail, Team2ACTemperatureCheck, Team2LaborEbSolarGenset, Team2Motor, Team2PestControl, Team2ACTempDeviation, Team2ElectricityConsumption, Team2EBDetails, Team2SolarDetails, Team2GensetDetails, Team2CountVerification, Team2AttendanceReplacement, Team2SecurityInfoNote,  Team2SecurityGovtInout, Team2AlcoholTest, Team2SecurityMaterialsInout, Team2SecurityMaterialsOutward, Team2TransportVerification, Team2DocumentsMovement, Team2GovtOfficialDocuments, Team2ThoorigaiTeamSocialMedia, Team2WebsiteUpdates, Team2MDSocialMedia, Team2IntercomMaintenance, Team2HealthCheckUp, Team2NetConnectivityPrintDetails, Team2GeneralMaintenanceITProducts,  Team2CalendarSchedule, Team2TrainingAttendance, Team2TrainingDetails, Team2ManpowerPlanning, Team2OverallConsolidation, Team2WaterLevel, Team2HousekeepingGeneral, Acknowledgement, Team2UniformDetails, Team2DepartmentWiseUniformDetails, Team3Audit, Team3NewAudit,FileStorage
from collections import defaultdict
from models import Acknowledgement
from datetime import datetime, timedelta
from cache_utils import per_user_cache_key

md_dashboard_bp = Blueprint('md_dashboard', __name__)


def get_authorized_dashboard_teams(user):
    """
    Returns the list of authorized teams for dashboard viewing based on user role.

    Rules:
    - MD: All teams in database (+ All Teams view).
    - Audit Team Lead (or Admin, team_id == 3): All teams in database.
    - Other Team Leads (e.g., Academics Lead, Admin Lead):
      Only:
      1. Their own team's submissions/forms
      2. Audit team's submissions/forms
      (Other teams are excluded).
    """
    all_db_teams = Team.query.order_by(Team.team_id).all()

    display_names = {
        'Team 1': 'Academics',
        'Team 2': 'Admin',
        'Team 3': 'Audit',
    }

    def format_team(t):
        return {
            'key': f'team{t.team_id}',
            'name': display_names.get(t.team_name, t.team_name),
            'team_id': t.team_id,
            'team_name': t.team_name,
        }

    # MD has access to all teams
    if user.role == 'MD':
        return [format_team(t) for t in all_db_teams]

    # Audit team lead / admin has access to all teams
    if user.team_id == 3 or user.role == 'Admin':
        return [format_team(t) for t in all_db_teams]

    # Standard Team Lead (Academics, Admin, etc.):
    # Allowed: 1. Their own team; 2. Audit team (team_id == 3)
    allowed = []
    for t in all_db_teams:
        if t.team_id == user.team_id or t.team_id == 3:
            allowed.append(format_team(t))

    # Sort so the user's own team appears first, then Audit
    allowed.sort(key=lambda x: (x['team_id'] != user.team_id, x['team_id']))
    return allowed


@md_dashboard_bp.route('/md/dashboard')
@md_dashboard_bp.route('/lead/dashboard')
@cache.cached(timeout=300, key_prefix=per_user_cache_key)
@login_required
def md_dashboard():
    # Allow MDs and Team Leads
    if not (current_user.role == 'MD' or getattr(current_user, 'is_team_lead', False)):
        flash('Access denied. MD or Team Lead privileges required.', 'error')
        return redirect(url_for('dashboard'))
    
    # Determine authorized teams based on user permissions
    authorized_teams = get_authorized_dashboard_teams(current_user)
    authorized_keys = {t['key'] for t in authorized_teams}
    if current_user.role == 'MD':
        authorized_keys.add('all')

    # Safe default team based on role
    if current_user.role == 'MD':
        default_team = 'all'
    elif current_user.team_id:
        default_team = f'team{current_user.team_id}'
    else:
        default_team = authorized_teams[0]['key'] if authorized_teams else 'team1'

    # Get selected team from query parameters and enforce strict authorization
    selected_team = request.args.get('team')
    if not selected_team or selected_team not in authorized_keys:
        selected_team = default_team

    # Get today's date for the date filter
    today_date = datetime.now().strftime('%Y-%m-%d')

    # Get selected date from query parameters, default to today
    selected_date = request.args.get('date', today_date)
    
    # Check if "all dates" is selected
    show_all_dates = (selected_date == 'all')
    
    # Validate date format (only if not showing all dates)
    if not show_all_dates:
        try:
            selected_date_obj = datetime.strptime(selected_date, '%Y-%m-%d').date()
        except ValueError:
            selected_date = today_date
            selected_date_obj = datetime.strptime(today_date, '%Y-%m-%d').date()
        
        start_of_day = datetime.combine(selected_date_obj, datetime.min.time())
        end_of_day = datetime.combine(selected_date_obj, datetime.max.time())
    else:
        # For "all dates", we'll skip date filtering in queries
        selected_date_obj = None
        start_of_day = None
        end_of_day = None
    
    # Get teams/users/issues scoped by role
    if current_user.role == 'MD':
        teams = Team.query.all()
        users = User.query.all()
        issue_query = Issue.query
    else:
        teams = [Team.query.get(current_user.team_id)]
        users = User.query.filter_by(team_id=current_user.team_id).all()
        issue_query = Issue.query.filter_by(team_id=current_user.team_id)
    
    all_issues = issue_query.all()
    total_issues = len(all_issues)
    resolved_issues = len([i for i in all_issues if i.status == 'Solved'])
    pending_issues = len([i for i in all_issues if i.status == 'Pending'])
    open_issues = len([i for i in all_issues if i.status == 'Open'])
    
    # Get recent issues
    recent_issues = issue_query.order_by(Issue.created_at.desc()).limit(10).all()
    
    # Initialize data variables
    team1_calendar_data = []
    team1_asa_data = []
    team1_asa_sports_data = []
    team1_asa_general_data = []
    team1_student_attendance_data = []
    team1_student_grooming_data = []    
    team1_student_late_coming_data = []
    team1_admission_status_data = []
    team1_transfer_certificate_data = []
    team1_parent_activity_data = []
    team1_parent_visit_data = []
    team1_exam_schedule_data = []
    team1_external_info_data = []
    team1_sick_bay_data = []
    team1_home_school_communication_data = []
    team1_disciplinary_measures_data = []
    team1_logistics_data = []
    team1_competition_certificate_data = []
    team1_staff_concern_data = []
    team1_student_concern_data = []
    team1_parent_concern_data = []
    team1_parent_concern_detail_data = []
    team1_aep_attendance_data = []
    team1_extended_class_data = []
    team1_training_session_data = []
    team1_weekly_meeting_data = []
    team1_special_education_data = []
    team1_hostel_data = []
    team1_sec_data = []
    team1_school_counsellor_data = []
    team1_scholorius_data = []

    team2_hr_attendance_data = []
    team2_total_hr_attendance_data = []
    team2_admin_attendance_data = []
    team2_recruitment_activity_data = []
    team2_pending_recruitment_data = []
    team2_recruitment_pipeline_data = []
    team2_staff_status_updates_data = []
    team2_salary_pending_data = []
    team2_police_verification_data = []
    team2_interview_schedule_data = []
    team2_exit_information_data = []
    team2_issues_staff_concerns_data = []
    team2_kural_recitation_data = []
    team2_front_office_phone_calls_data = []
    team2_visitor_log_data = []
    team2_bsnl_phone_status_data = []
    team2_materials_inward_data = []
    team2_materials_outward_data = []
    team2_materials_movement_data = []
    team2_returnable_material_tracking_data = []
    team2_returnable_goods_report_data = []
    team2_campus_camera_status_data = []
    team2_vehicle_camera_status_data = []
    team2_bus_ac_camera_status_data = []
    team2_gps_monitoring_data = []
    team2_issues_identified_monitoring_data = []
    team2_teachers_late_reporting_data = []
    team2_water_tds_deviation_data = []
    team2_testing_cleaning_data = []
    team2_water_level_data = []
    team2_housekeeping_general_data = []
    team2_pool_testing_data = []
    team2_washroom_cleanliness_data = []
    team2_transport_attendance_data = []
    team2_ac_working_status_data=[]
    team2_late_reporting_data=[]
    team2_maintenance_service_issues_data=[]
    team2_car_maintenance_cleaning_data=[]
    team2_vehicle_renewals_delays_data=[]
    team2_special_trip_data=[]
    team2_parent_concern_detail_data=[]
    team2_ac_temperature_data=[]
    team2_maintenance_labor_data=[]
    team2_motor_data=[]
    team2_pest_control_data=[]
    team2_ac_temp_deviation_data=[]
    team2_electricity_consumption_data=[]
    team2_eb_details_data=[]
    team2_solar_details_data=[]
    team2_genset_details_data=[]
    team2_count_verification_data=[]
    team2_attendance_replacement_data=[]
    team2_security_info_note_data=[]
    team2_security_govt_inout_data=[]
    team2_alcohol_test_data=[]
    team2_security_materials_inward_data=[]
    team2_security_materials_outward_data=[]
    team2_transport_verification_data=[]
    team2_documents_movement_data=[]
    team2_govt_official_documents_data=[]
    team2_thoorigai_social_media_data=[]
    team2_website_updates_data=[]
    team2_md_social_media_data=[]
    team2_intercom_maintenance_data=[]
    team2_health_check_up_data=[]
    team2_net_connectivity_print_details_data=[]
    team2_general_maintenance_it_data=[]
    team2_calendar_schedule_data=[]
    team2_training_attendance_data=[]
    team2_training_details_data=[]
    team2_camera_footage_data = []
    team2_manpower_planning_data = []
    team2_overall_consolidation_data = []
    team2_uniform_details_data = []
    team2_dept_wise_uniform_details_data = []
    team2_biometrics_access_card_punching_data = []
    team2_campus_camera_status_data = []
    team2_vehicle_camera_status_data = []
    team2_bus_ac_camera_status_data = []
    team2_gps_monitoring_data = []
    team2_issues_identified_monitoring_data = []
    team2_teachers_late_reporting_data = [] 

    team3_audit_data = []
    team3_new_audit_data = []



    
  # Get Team 1 data if selected team is 'all' or 'team1'
    if selected_team in ['all', 'team1']:
        team1 = Team.query.filter_by(team_name='Team 1').first()
        if team1:
            # Get Team 1 Calendar Schedule data with proper date filtering
            query = Team1CalendarSchedule.query.filter(Team1CalendarSchedule.team_id == team1.team_id)
            if not show_all_dates:
                query = query.filter(
                    Team1CalendarSchedule.submitted_at >= start_of_day,
                    Team1CalendarSchedule.submitted_at <= end_of_day
                )
            calendar_data = query.order_by(Team1CalendarSchedule.submitted_at.desc()).all()
            team1_calendar_data = [{
                'date': item.submitted_at,
                'jr_school': {
                    'session': item.cal_session_jr,
                    'department': item.cal_dept_jr,
                    'plan': item.cal_plan_jr,
                    'total': item.cal_total_jr,
                    'expected': item.cal_expected_jr,
                    'present_pct': item.cal_present_pct_jr,
                    'absent_pct': item.cal_absent_pct_jr,
                    'issue_nature': item.cal_issue_nature_jr,
                    'issue_desc': item.cal_issue_desc_jr,
                    'comment': item.cal_comment_jr
                },
                'sr_school': {
                    'session': item.cal_session_sr,
                    'department': item.cal_dept_sr,
                    'plan': item.cal_plan_sr,
                    'total': item.cal_total_sr,
                    'expected': item.cal_expected_sr,
                    'present_pct': item.cal_present_pct_sr,
                    'absent_pct': item.cal_absent_pct_sr,
                    'issue_nature': item.cal_issue_nature_sr,
                    'issue_desc': item.cal_issue_desc_sr,
                    'comment': item.cal_comment_sr
                },
            } for item in calendar_data]
            
            # Get Team 1 ASA Activities data with proper date filtering
            query = Team1ASAActivities.query.filter(Team1ASAActivities.team_id == team1.team_id)
            if not show_all_dates:
                query = query.filter(
                    Team1ASAActivities.submitted_at >= start_of_day,
                    Team1ASAActivities.submitted_at <= end_of_day
                )
            asa_data = query.order_by(Team1ASAActivities.submitted_at.desc()).all()
            team1_asa_data = []
            for item in asa_data:
                asa_item = {
                    'date': item.submitted_at,
                    'rifle': {
                        'strength': item.asa_strength_rifle,
                        'enrolled': item.asa_enrolled_rifle,
                        'enrol_pct': item.asa_enrol_pct_rifle,
                        'activities': item.asa_activities_rifle,
                        'expected': item.asa_expected_rifle,
                        'attended': item.asa_attended_rifle,
                        'attend_pct': item.asa_attend_pct_rifle
                    },
                    'ncc': {
                        'strength': item.asa_strength_ncc,
                        'enrolled': item.asa_enrolled_ncc,
                        'enrol_pct': item.asa_enrol_pct_ncc,
                        'activities': item.asa_activities_ncc,
                        'expected': item.asa_expected_ncc,
                        'attended': item.asa_attended_ncc,
                        'attend_pct': item.asa_attend_pct_ncc
                    }
                }
                # Only add if there's actual data for rifle or ncc
                if (item.asa_strength_rifle or item.asa_enrolled_rifle or item.asa_expected_rifle or item.asa_attended_rifle or
                    item.asa_strength_ncc or item.asa_enrolled_ncc or item.asa_expected_ncc or item.asa_attended_ncc):
                    team1_asa_data.append(asa_item)

            # Get Team 1 ASA Sports data with proper date filtering
            query = Team1ASASports.query.filter(Team1ASASports.team_id == team1.team_id)
            if not show_all_dates:
                query = query.filter(
                    Team1ASASports.submitted_at >= start_of_day,
                    Team1ASASports.submitted_at <= end_of_day
                )
            asa_sports_data = query.order_by(Team1ASASports.submitted_at.desc()).all()
            team1_asa_sports_data = []
            for item in asa_sports_data:
                sports_data = item.asa_sports_data or {}
                formatted_item = {
                    'date': item.submitted_at,
                }
                # Convert JSON data to expected format
                for activity in ['athletics', 'basketball', 'football', 'throwball', 'total']:
                    activity_data = sports_data.get(activity, {})
                    formatted_item[activity] = {
                        'strength': activity_data.get('strength'),
                        'enrolled': activity_data.get('enrolled'),
                        'enrol_pct': activity_data.get('enrol_pct'),
                        'activities': activity_data.get('activities', ''),
                        'expected': activity_data.get('expected'),
                        'attended': activity_data.get('attended'),
                        'attend_pct': activity_data.get('attend_pct')
                    }
                team1_asa_sports_data.append(formatted_item)

            # Get Team 1 ASA General data with proper date filtering
            query = Team1ASAGeneral.query.filter(Team1ASAGeneral.team_id == team1.team_id)
            if not show_all_dates:
                query = query.filter(
                    Team1ASAGeneral.submitted_at >= start_of_day,
                    Team1ASAGeneral.submitted_at <= end_of_day
                )
            asa_general_data = query.order_by(Team1ASAGeneral.submitted_at.desc()).all()
            team1_asa_general_data = []
            for item in asa_general_data:
                general_data = item.asa_general_data or {}
                formatted_item = {
                    'date': item.submitted_at,
                }
                # Convert JSON data to expected format
                activities = ['taekwondo', 'silambam', 'kungfu', 'yoga', 'tabletennis', 'skating',
                             'classicaldance', 'westerndance', 'keyboard', 'guitar', 'drums', 'total']
                for activity in activities:
                    activity_data = general_data.get(activity, {})
                    formatted_item[activity] = {
                        'strength': activity_data.get('strength'),
                        'enrolled': activity_data.get('enrolled'),
                        'enrol_pct': activity_data.get('enrol_pct'),
                        'activities': activity_data.get('activities', ''),
                        'expected': activity_data.get('expected'),
                        'attended': activity_data.get('attended'),
                        'attend_pct': activity_data.get('attend_pct')
                    }
                team1_asa_general_data.append(formatted_item)

            # Get Team 1 Student Attendance data with proper date filtering
            query = Team1StudentAttendance.query.filter(Team1StudentAttendance.team_id == team1.team_id)
            if not show_all_dates:
                query = query.filter(
                    Team1StudentAttendance.submitted_at >= start_of_day,
                    Team1StudentAttendance.submitted_at <= end_of_day
                )
            student_attendance_data = query.order_by(Team1StudentAttendance.submitted_at.desc()).all()
            team1_student_attendance_data = [{
                'date': item.submitted_at,
                'kindergarten': {
                    'total_strength': item.att_str_kg,
                    'present': item.att_present_kg,
                    'leave': item.att_leave_kg,
                    'absent': item.att_absent_kg,
                    'present_pct': item.att_present_pct_kg,
                    'issue_nature': item.att_issue_nature_kg,
                    'issue_desc': item.att_issue_desc_kg,
                    'comment': item.att_comment_kg
                },
                'grades_1_to_5': {
                    'total_strength': item.att_str_g15,
                    'present': item.att_present_g15,
                    'leave': item.att_leave_g15,
                    'absent': item.att_absent_g15,
                    'present_pct': item.att_present_pct_g15,
                    'issue_nature': item.att_issue_nature_g15,
                    'issue_desc': item.att_issue_desc_g15,
                    'comment': item.att_comment_g15
                },
                'grades_6_to_10': {
                    'total_strength': item.att_str_g610,
                    'present': item.att_present_g610,
                    'leave': item.att_leave_g610,
                    'absent': item.att_absent_g610,
                    'present_pct': item.att_present_pct_g610,
                    'issue_nature': item.att_issue_nature_g610,
                    'issue_desc': item.att_issue_desc_g610,
                    'comment': item.att_comment_g610
                },
                'grades_11_to_12': {
                    'total_strength': item.att_str_g1112,
                    'present': item.att_present_g1112,
                    'leave': item.att_leave_g1112,
                    'absent': item.att_absent_g1112,
                    'present_pct': item.att_present_pct_g1112,
                    'issue_nature': item.att_issue_nature_g1112,
                    'issue_desc': item.att_issue_desc_g1112,
                    'comment': item.att_comment_g1112
                },
                'overall': {
                    'total_strength': item.att_str_overall,
                    'present': item.att_present_overall,
                    'leave': item.att_leave_overall,
                    'absent': item.att_absent_overall,
                    'present_pct': item.att_present_pct_overall,
                    'issue_nature': item.att_issue_nature_overall,
                    'issue_desc': item.att_issue_desc_overall,
                    'comment': item.att_comment_overall
                }
            } for item in student_attendance_data]

            # Get Team 1 Student Grooming data with proper date filtering
            query = Team1StudentGrooming.query.filter(Team1StudentGrooming.team_id == team1.team_id)
            if not show_all_dates:
                query = query.filter(
                    Team1StudentGrooming.submitted_at >= start_of_day,
                    Team1StudentGrooming.submitted_at <= end_of_day
                )
            grooming_data = query.order_by(Team1StudentGrooming.submitted_at.desc()).all()
            team1_student_grooming_data = [{
                'date': item.submitted_at,
                'total_strength': item.grooming_total_strength,
                'regular_students': item.grooming_regular_students,
                'defaulters_count': item.grooming_defaulters_count,
                'defaulters_percentage': item.grooming_defaulters_pct,
                'issue_nature': item.grooming_issue_nature,
                'issue_description': item.grooming_issue_desc,
                'comments': item.grooming_comments
            } for item in grooming_data]

            # Get Team 1 Student Late Coming data with proper date filtering
            query = Team1StudentLateComing.query.filter(Team1StudentLateComing.team_id == team1.team_id)

            if not show_all_dates:

                query = query.filter(

                    Team1StudentLateComing.submitted_at >= start_of_day,

                    Team1StudentLateComing.submitted_at <= end_of_day

                )

            late_coming_data = query.order_by(Team1StudentLateComing.submitted_at.desc()).all()
            team1_student_late_coming_data = [{
                'date': item.submitted_at,
                'total_strength': item.late_coming_total_strength,
                'regular_students': item.late_coming_regular_students,
                'defaulters_count': item.late_coming_defaulters_count,
                'defaulters_percentage': item.late_coming_defaulters_pct,
                'issue_nature': item.late_coming_issue_nature,
                'issue_description': item.late_coming_issue_desc,
                'comments': item.late_coming_comments
            } for item in late_coming_data]

            # Get Team 1 Admission Status data with proper date filtering
            query = Team1AdmissionStatus.query.filter(Team1AdmissionStatus.team_id == team1.team_id)

            if not show_all_dates:

                query = query.filter(

                    Team1AdmissionStatus.submitted_at >= start_of_day,

                    Team1AdmissionStatus.submitted_at <= end_of_day

                )

            admission_status_data = query.order_by(Team1AdmissionStatus.submitted_at.desc()).all()
    
            # Group admission status entries by submission timestamp
            grouped_admission_data = {}
            for item in admission_status_data:
                timestamp = item.submitted_at
                if timestamp not in grouped_admission_data:
                    grouped_admission_data[timestamp] = {
                        'date': timestamp,
                        'school': {},
                        'bumble_bee': {},
                        'leeds_excel': {}
                    }
                
                if 'School' in item.admission_dept_category:
                    grouped_admission_data[timestamp]['school'] = {
                        'total': item.admission_total,
                        'walkin': item.admission_walkin,
                        'appln': item.admission_appln,
                        'ela': item.admission_ela,
                        'recommended': item.admission_recommended,
                        'status': item.admission_status,
                        'issue_nature': item.admission_issue_nature,
                        'issue_desc': item.admission_issue_desc,
                        'comments': item.admission_comments
                    }
                elif 'Bumble Bee' in item.admission_dept_category:
                    grouped_admission_data[timestamp]['bumble_bee'] = {
                        'total': item.admission_total,
                        'walkin': item.admission_walkin,
                        'appln': item.admission_appln,
                        'ela': item.admission_ela,
                        'recommended': item.admission_recommended,
                        'status': item.admission_status,
                        'issue_nature': item.admission_issue_nature,
                        'issue_desc': item.admission_issue_desc,
                        'comments': item.admission_comments
                    }
                elif 'Leeds Excel' in item.admission_dept_category or 'Leeds' in item.admission_dept_category:
                    grouped_admission_data[timestamp]['leeds_excel'] = {
                        'total': item.admission_total,
                        'walkin': item.admission_walkin,
                        'appln': item.admission_appln,
                        'ela': item.admission_ela,
                        'recommended': item.admission_recommended,
                        'status': item.admission_status,
                        'issue_nature': item.admission_issue_nature,
                        'issue_desc': item.admission_issue_desc,
                        'comments': item.admission_comments
                    }
            
            # Convert the grouped data to a list
            team1_admission_status_data = list(grouped_admission_data.values())

            # Get Team 1 Transfer Certificate data with proper date filtering
            query = Team1TransferCertificate.query.filter(Team1TransferCertificate.team_id == team1.team_id)

            if not show_all_dates:

                query = query.filter(

                    Team1TransferCertificate.submitted_at >= start_of_day,

                    Team1TransferCertificate.submitted_at <= end_of_day

                )

            transfer_certificate_data = query.order_by(Team1TransferCertificate.submitted_at.desc()).all()
            team1_transfer_certificate_data = [{
                    'date': item.submitted_at,
                    'work_activity': item.transfer_certificate_work_activity,
                    'dept_cat': item.transfer_certificate_dept_category,
                    'grade': item.transfer_certificate_grade,
                    'student_name': item.transfer_certificate_student_name,
                    'year_at_qmis': item.transfer_certificate_year_at_qmis,
                    'reason': item.transfer_certificate_reason,
                    'staff_in_charge': item.transfer_certificate_staff_in_charge,
                    'sibling': item.transfer_certificate_sibling,
                    'nature_of_issue': item.transfer_certificate_issue_nature,
                    'issue_description': item.transfer_certificate_issue_desc,
                    'comments': item.transfer_certificate_comments
                } for item in transfer_certificate_data]
            
            # Get Team 1 Parent Activity data with proper date filtering
            query = Team1ParentActivity.query.filter(Team1ParentActivity.team_id == team1.team_id)

            if not show_all_dates:

                query = query.filter(

                    Team1ParentActivity.submitted_at >= start_of_day,

                    Team1ParentActivity.submitted_at <= end_of_day

                )

            parent_activity_data = query.order_by(Team1ParentActivity.submitted_at.desc()).all()
            team1_parent_activity_data = [{
                'date': item.submitted_at,
                'work_activity': item.parent_activity_work_activity,
                'dept_cat': item.parent_activity_dept_category,
                'session_activity': item.parent_activity_session,
                'dept': item.parent_activity_dept,
                'expected': item.parent_activity_expected,
                'reported': item.parent_activity_reported,
                'not_reported': item.parent_activity_not_reported,
                'present_pct': item.parent_activity_present_pct,
                'absent_pct': item.parent_activity_absent_pct,
                'nature_of_issue': item.parent_activity_issue_nature,
                'issue_description': item.parent_activity_issue_desc,
                'comments': item.parent_activity_comments
            } for item in parent_activity_data]

            # Get Team 1 Parent Visit data with proper date filtering
            query = Team1ParentVisit.query.filter(Team1ParentVisit.team_id == team1.team_id)

            if not show_all_dates:

                query = query.filter(

                    Team1ParentVisit.submitted_at >= start_of_day,

                    Team1ParentVisit.submitted_at <= end_of_day

                )

            parent_visit_data = query.order_by(Team1ParentVisit.submitted_at.desc()).all()
            team1_parent_visit_data = [{    
                'date': item.submitted_at,
                'work_activity': item.parent_visit_work_activity,
                'dept_cat': item.parent_visit_dept_category,
                'grade': item.parent_visit_grade,
                'student_name': item.parent_visit_student_name,
                'year_at_qmis': item.parent_visit_year_at_qmis,
                'parents_profession': item.parent_visit_parents_profession,
                'concern_appreciation': item.parent_visit_concern_appreciation,
                'staff_in_charge': item.parent_visit_staff_in_charge,
                'nature_of_issue': item.parent_visit_issue_nature,
                'issue_description': item.parent_visit_issue_desc,
                'comments': item.parent_visit_comments
            } for item in parent_visit_data]

            # Get Team 1 Exam Schedule data with proper date filtering
            query = Team1ExamSchedule.query.filter(Team1ExamSchedule.team_id == team1.team_id)

            if not show_all_dates:

                query = query.filter(

                    Team1ExamSchedule.submitted_at >= start_of_day,

                    Team1ExamSchedule.submitted_at <= end_of_day

                )

            exam_schedule_data = query.order_by(Team1ExamSchedule.submitted_at.desc()).all()
            team1_exam_schedule_data = [{
                'date': item.submitted_at,
                'g15': {
                    'schedule': item.exam_schedule_g15,
                    'total_strength': item.exam_str_g15,
                    'attended': item.exam_att_g15,
                    'not_attended': item.exam_notatt_g15,
                    'nature_of_issue': item.exam_issue_nature_g15,
                    'issue_description': item.exam_issue_desc_g15,
                    'comments': item.exam_comment_g15
                },
                'g68': {
                    'schedule': item.exam_schedule_g68,
                    'total_strength': item.exam_str_g68,
                    'attended': item.exam_att_g68,
                    'not_attended': item.exam_notatt_g68,
                    'nature_of_issue': item.exam_issue_nature_g68,
                    'issue_description': item.exam_issue_desc_g68,
                    'comments': item.exam_comment_g68
                },
                'g910': {
                    'schedule': item.exam_schedule_g910,
                    'total_strength': item.exam_str_g910,
                    'attended': item.exam_att_g910,
                    'not_attended': item.exam_notatt_g910,
                    'nature_of_issue': item.exam_issue_nature_g910,
                    'issue_description': item.exam_issue_desc_g910,
                    'comments': item.exam_comment_g910
                },
                'g11': {
                    'schedule': item.exam_schedule_g11,
                    'total_strength': item.exam_str_g11,
                    'attended': item.exam_att_g11,
                    'not_attended': item.exam_notatt_g11,
                    'nature_of_issue': item.exam_issue_nature_g11,
                    'issue_description': item.exam_issue_desc_g11,
                    'comments': item.exam_comment_g11
                },
                'g12': {
                    'schedule': item.exam_schedule_g12,
                    'total_strength': item.exam_str_g12,
                    'attended': item.exam_att_g12,
                    'not_attended': item.exam_notatt_g12,
                    'nature_of_issue': item.exam_issue_nature_g12,
                    'issue_description': item.exam_issue_desc_g12,
                    'comments': item.exam_comment_g12
                }
            } for item in exam_schedule_data]   
    
            # Get Team 1 External Info data with proper date filtering
            query = Team1ExternalInfo.query.filter(Team1ExternalInfo.team_id == team1.team_id)

            if not show_all_dates:

                query = query.filter(

                    Team1ExternalInfo.submitted_at >= start_of_day,

                    Team1ExternalInfo.submitted_at <= end_of_day

                )

            external_info_data = query.order_by(Team1ExternalInfo.submitted_at.desc()).all()
            team1_external_info_data = [{
                'date': item.submitted_at,
                'cis': {
                    'mode_receiving': item.ext_mode_receiving_cis,
                    'mode_sending': item.ext_mode_sending_cis,
                    'subject': item.ext_subj_cis,
                    'from': item.ext_from_cis,
                    'to': item.ext_to_cis,
                    'nature_of_issue': item.ext_issue_nature_cis,
                    'issue_description': item.ext_issue_desc_cis,
                    'comments': item.ext_comment_cis
                },
                'cbse': {
                    'mode_receiving': item.ext_mode_receiving_cbse,
                    'mode_sending': item.ext_mode_sending_cbse,
                    'subject': item.ext_subj_cbse,
                    'from': item.ext_from_cbse,
                    'to': item.ext_to_cbse,
                    'nature_of_issue': item.ext_issue_nature_cbse,
                    'issue_description': item.ext_issue_desc_cbse,
                    'comments': item.ext_comment_cbse
                },
                'state': {
                    'mode_receiving': item.ext_mode_receiving_state,
                    'mode_sending': item.ext_mode_sending_state,
                    'subject': item.ext_subj_state,
                    'from': item.ext_from_state,
                    'to': item.ext_to_state,
                    'nature_of_issue': item.ext_issue_nature_state,
                    'issue_description': item.ext_issue_desc_state,
                    'comments': item.ext_comment_state
                },
                'emis': {
                    'mode_receiving': item.ext_mode_receiving_emis,
                    'mode_sending': item.ext_mode_sending_emis,
                    'subject': item.ext_subj_emis,
                    'from': item.ext_from_emis,
                    'to': item.ext_to_emis,
                    'nature_of_issue': item.ext_issue_nature_emis,
                    'issue_description': item.ext_issue_desc_emis,
                    'comments': item.ext_comment_emis
                }
            } for item in external_info_data]

            #  get 12: Sick Bay data
            # Get Team 1 Sick Bay data with proper date filtering
            query = Team1SickBay.query.filter(Team1SickBay.team_id == team1.team_id)

            if not show_all_dates:

                query = query.filter(

                    Team1SickBay.submitted_at >= start_of_day,

                    Team1SickBay.submitted_at <= end_of_day

                )

            sick_bay_data = query.order_by(Team1SickBay.submitted_at.desc()).all()
            team1_sick_bay_data = [{
                'date': item.submitted_at,
                'grade': item.sick_grade,
                'student_name': item.sick_name,
                'illness': item.sick_illness,
                'informed_by': item.sick_inf_by,
                'informed_to_prm': item.sick_inf_to,
                'nature_of_issue': item.sick_issue_nature,
                'issue_description': item.sick_issue_desc,
                'comments': item.sick_comment
            } for item in sick_bay_data]

            # Get Team 1 Home School Communications data with proper date filtering
            query = Team1HomeSchoolComm.query.filter(Team1HomeSchoolComm.team_id == team1.team_id)

            if not show_all_dates:

                query = query.filter(

                    Team1HomeSchoolComm.submitted_at >= start_of_day,

                    Team1HomeSchoolComm.submitted_at <= end_of_day

                )

            home_school_comm_data = query.order_by(Team1HomeSchoolComm.submitted_at.desc()).all()
            team1_home_school_communication_data = [{
                'date': item.submitted_at,
                'grade': item.hsc_grade,
                'planned_unplanned': item.hsc_plan,
                'printed_date': item.hsc_print_date,
                'distributed_date': item.hsc_dist_date,
                'activity_event': item.hsc_activity,
                'status': item.hsc_status,
                'nature_of_issue': item.hsc_issue_nature,
                'issue_description': item.hsc_issue_desc,
                'comments': item.hsc_comment
            } for item in home_school_comm_data]


            # Get Team 1 Disciplinary measures data with proper date filtering
            query = Team1Disciplinary.query.filter(Team1Disciplinary.team_id == team1.team_id)

            if not show_all_dates:

                query = query.filter(

                    Team1Disciplinary.submitted_at >= start_of_day,

                    Team1Disciplinary.submitted_at <= end_of_day

                )

            disciplinary_data = query.order_by(Team1Disciplinary.submitted_at.desc()).all()
            team1_disciplinary_measures_data = [{
                
                'date': item.submitted_at,
                'grade': item.disc_grade,
                'student_name': item.disc_name,
                'issue': item.disc_issue,
                'action_taken': item.disc_action,
                'nature_of_issue': item.disc_issue_nature,
                'issue_description': item.disc_issue_desc,
                'comments': item.disc_comment
            } for item in disciplinary_data]

            # Get Team 1 Logistics data with proper date filtering
            query = Team1Logistics.query.filter(Team1Logistics.team_id == team1.team_id)

            if not show_all_dates:

                query = query.filter(

                    Team1Logistics.submitted_at >= start_of_day,

                    Team1Logistics.submitted_at <= end_of_day

                )

            logistics_data = query.order_by(Team1Logistics.submitted_at.desc()).all()
            team1_logistics_data = [{
                
                'date': item.submitted_at,
                'inward_material': item.log_in_mat,
                'inward_quantity': item.log_in_qty,
                'outward_material': item.log_out_mat,
                'outward_quantity': item.log_out_qty,
                'additional_sales_quantity': item.log_sale_qty,
                'additional_sales_material': item.log_sale_mat,
                'nature_of_issue': item.log_issue_nature,
                'issue_description': item.log_issue_desc,
                'comments': item.log_comment
            } for item in logistics_data]


            # Get Team 1 Competition Certificate data with proper date filtering
            query = Team1CompetitionCert.query.filter(Team1CompetitionCert.team_id == team1.team_id)

            if not show_all_dates:

                query = query.filter(

                    Team1CompetitionCert.submitted_at >= start_of_day,

                    Team1CompetitionCert.submitted_at <= end_of_day

                )

            competition_cert_data = query.order_by(Team1CompetitionCert.submitted_at.desc()).all()
            team1_competition_certificate_data = [{
                
                'date': item.submitted_at,
                'work_activity': item.cert_work_activity,
                'dept_cat': item.cert_dept_cat,
                'grade': item.cert_grade,
                'activity': item.cert_activity,
                'activity_date': item.cert_date,
                'no_of_certs': item.cert_no,
                'dist_status': item.cert_status,
                'nature_of_issue': item.cert_issue_nature,
                'issue_description': item.cert_issue_desc,
                'comments': item.cert_comment
            } for item in competition_cert_data]

            # Get Team 1 Staff Concern data with proper date filtering
            query = Team1StaffConcern.query.filter(Team1StaffConcern.team_id == team1.team_id)

            if not show_all_dates:

                query = query.filter(

                    Team1StaffConcern.submitted_at >= start_of_day,

                    Team1StaffConcern.submitted_at <= end_of_day

                )

            staff_concern_data = query.order_by(Team1StaffConcern.submitted_at.desc()).all()
            team1_staff_concern_data = [{
                
                'date': item.submitted_at,
                'work_activity': item.sc_work_activity,
                'dept_cat': item.sc_cat,
                'name': item.sc_name,
                'dept': item.sc_dept,
                'incharges_handled': item.sc_incharge,
                'nature_of_issue': item.sc_issue_nature,
                'issue_description': item.sc_issue_desc,
                'comments': item.sc_comment
            } for item in staff_concern_data]

            # Get Team 1 Student Concern data with proper date filtering
            query = Team1StudentConcern.query.filter(Team1StudentConcern.team_id == team1.team_id)

            if not show_all_dates:

                query = query.filter(

                    Team1StudentConcern.submitted_at >= start_of_day,

                    Team1StudentConcern.submitted_at <= end_of_day

                )

            student_concern_data = query.order_by(Team1StudentConcern.submitted_at.desc()).all()
            team1_student_concern_data = [{
                
                'date': item.submitted_at,
                'work_activity': item.st_work_activity,
                'dept_cat': item.st_cat,
                'student_name': item.st_name,
                'class_section': item.st_class,
                'incharges_handled': item.st_incharge,
                'nature_of_issue': item.st_issue_nature,
                'issue_description': item.st_issue_desc,
                'comments': item.st_comment
            } for item in student_concern_data]

            # Get Team 1 Parent Concern Summary data with proper date filtering
            query = Team1ParentConcern.query.filter(Team1ParentConcern.team_id == team1.team_id)

            if not show_all_dates:

                query = query.filter(

                    Team1ParentConcern.submitted_at >= start_of_day,

                    Team1ParentConcern.submitted_at <= end_of_day

                )

            parent_concern_data = query.order_by(Team1ParentConcern.submitted_at.desc()).all()
            team1_parent_concern_data = [{
                
                'date': item.submitted_at,
                'work_activity': item.pc_work_activity,
                'dept_cat': item.pc_cat,
                'no_of_concerns': item.pc_summary_no,
                'closed': item.pc_summary_closed,
                'loop_1_3_days': item.pc_summary_loop13,
                'loop_3plus_days': item.pc_summary_loop3plus,
                'nature_of_issue': item.pc_summary_issue_nature,
                'issue_description': item.pc_summary_issue_desc,
                'comments': item.pc_summary_comment
            } for item in parent_concern_data]

            # Get Team 1 Parent Concern Details data with proper date filtering
            query = Team1ParentConcernDetail.query.filter(Team1ParentConcernDetail.team_id == team1.team_id)

            if not show_all_dates:

                query = query.filter(

                    Team1ParentConcernDetail.submitted_at >= start_of_day,

                    Team1ParentConcernDetail.submitted_at <= end_of_day

                )

            parent_concern_detail_data = query.order_by(Team1ParentConcernDetail.submitted_at.desc()).all()
            team1_parent_concern_detail_data = [{
                
                'date': item.submitted_at,
                'work_activity': item.pc_work_activity,
                'student_name': item.pc_detail_name,
                'grade': item.pc_detail_grade,
                'concern_expressed': item.pc_detail_concern,
                'incharges_handled': item.pc_detail_incharge,
                'nature_of_issue': item.pc_detail_issue_nature,
                'comments': item.pc_detail_comment
            } for item in parent_concern_detail_data]

            # Get Team 1 AEP Attendance data with proper date filtering
            query = Team1AEPAttendance.query.filter(Team1AEPAttendance.team_id == team1.team_id)

            if not show_all_dates:

                query = query.filter(

                    Team1AEPAttendance.submitted_at >= start_of_day,

                    Team1AEPAttendance.submitted_at <= end_of_day

                )

            aep_attendance_data = query.order_by(Team1AEPAttendance.submitted_at.desc()).all()
            team1_aep_attendance_data = [{
        
            'date': item.submitted_at,
            'grade_11': {
                'strength': item.aep_str_g11,
                'enrolled': item.aep_enr_g11,
                'enrolled_percentage': item.aep_enrpct_g11,
                'programs': item.aep_prog_g11,
                'expected': item.aep_exp_g11,
                'attended': item.aep_att_g11,
                'attendance_percentage': item.aep_attpct_g11
            },
            'grade_12': {
                'strength': item.aep_str_g12,
                'enrolled': item.aep_enr_g12,
                'enrolled_percentage': item.aep_enrpct_g12,
                'programs': item.aep_prog_g12,
                'expected': item.aep_exp_g12,
                'attended': item.aep_att_g12,
                'attendance_percentage': item.aep_attpct_g12
                }
            } for item in aep_attendance_data]

            # Get Team 1 Extended Class Attendance data with proper date filtering
            query = Team1ExtendedClassAttendance.query.filter(Team1ExtendedClassAttendance.team_id == team1.team_id)

            if not show_all_dates:

                query = query.filter(

                    Team1ExtendedClassAttendance.submitted_at >= start_of_day,

                    Team1ExtendedClassAttendance.submitted_at <= end_of_day

                )

            extended_class_data = query.order_by(Team1ExtendedClassAttendance.submitted_at.desc()).all()
            team1_extended_class_data = [{
              
                'date': item.submitted_at,
                'grade_3_5': {
                    'strength': item.ec_str_g35,
                    'enrolled': item.ec_enr_g35,
                    'enrolled_percentage': item.ec_enrpct_g35,
                    'subjects': item.ec_subj_g35,
                    'expected': item.ec_exp_g35,
                    'attended': item.ec_att_g35,
                    'attendance_percentage': item.ec_attpct_g35
                },
                'grade_6_8': {
                    'strength': item.ec_str_g68,
                    'enrolled': item.ec_enr_g68,
                    'enrolled_percentage': item.ec_enrpct_g68,
                    'subjects': item.ec_subj_g68,
                    'expected': item.ec_exp_g68,
                    'attended': item.ec_att_g68,
                    'attendance_percentage': item.ec_attpct_g68
                },
                'grade_9_10': {
                    'strength': item.ec_str_g910,
                    'enrolled': item.ec_enr_g910,
                    'enrolled_percentage': item.ec_enrpct_g910,
                    'subjects': item.ec_subj_g910,
                    'expected': item.ec_exp_g910,
                    'attended': item.ec_att_g910,
                    'attendance_percentage': item.ec_attpct_g910
                },
                'grade_11_12': {
                    'strength': item.ec_str_g1112,
                    'enrolled': item.ec_enr_g1112,
                    'enrolled_percentage': item.ec_enrpct_g1112,
                    'subjects': item.ec_subj_g1112,
                    'expected': item.ec_exp_g1112,
                    'attended': item.ec_att_g1112,
                    'attendance_percentage': item.ec_attpct_g1112
                }
            } for item in extended_class_data]

            # Get Team 1 Training Session data with proper date filtering
            query = Team1TrainingSession.query.filter(Team1TrainingSession.team_id == team1.team_id)

            if not show_all_dates:

                query = query.filter(

                    Team1TrainingSession.submitted_at >= start_of_day,

                    Team1TrainingSession.submitted_at <= end_of_day

                )

            training_session_data = query.order_by(Team1TrainingSession.submitted_at.desc()).all()
            team1_training_session_data = [{
              
                'date': item.submitted_at,
                'teacher_name': item.train_teacher,
                'topic': item.train_topic,
                'conducted_by': item.train_by,
                'mode': item.train_mode,
                'duration': item.train_duration,
                'report_shared': item.train_report,
                'participants': item.train_participants,
            } for item in training_session_data]

            # Get Team 1 Weekly Meeting data with proper date filtering
            query = Team1WeeklyMeeting.query.filter(Team1WeeklyMeeting.team_id == team1.team_id)

            if not show_all_dates:

                query = query.filter(

                    Team1WeeklyMeeting.submitted_at >= start_of_day,

                    Team1WeeklyMeeting.submitted_at <= end_of_day

                )

            weekly_meeting_data = query.order_by(Team1WeeklyMeeting.submitted_at.desc()).all()
            team1_weekly_meeting_data = [{
                
                'date': item.submitted_at,
                'kg': {
                    'headed_by': item.meet_head_kg,
                    'agenda': item.meet_agenda_kg,
                    'strength': item.meet_str_kg,
                    'attended': item.meet_att_kg,
                    'attendance_percentage': item.meet_attpct_kg
                },
                'grade_1_2': {
                    'headed_by': item.meet_head_12,
                    'agenda': item.meet_agenda_12,
                    'strength': item.meet_str_12,
                    'attended': item.meet_att_12,
                    'attendance_percentage': item.meet_attpct_12
                },
                'grade_3_5': {
                    'headed_by': item.meet_head_35,
                    'agenda': item.meet_agenda_35,
                    'strength': item.meet_str_35,
                    'attended': item.meet_att_35,
                    'attendance_percentage': item.meet_attpct_35
                },
                'grade_6_8': {
                    'headed_by': item.meet_head_68,
                    'agenda': item.meet_agenda_68,
                    'strength': item.meet_str_68,
                    'attended': item.meet_att_68,
                    'attendance_percentage': item.meet_attpct_68
                },
                'grade_9_10': {
                    'headed_by': item.meet_head_910,
                    'agenda': item.meet_agenda_910,
                    'strength': item.meet_str_910,
                    'attended': item.meet_att_910,
                    'attendance_percentage': item.meet_attpct_910
                },
                'grade_11_12': {
                    'headed_by': item.meet_head_1112,
                    'agenda': item.meet_agenda_1112,
                    'strength': item.meet_str_1112,
                    'attended': item.meet_att_1112,
                    'attendance_percentage': item.meet_attpct_1112
                }
            } for item in weekly_meeting_data]

                # Get Team 1 Special Education data with proper date filtering
            query = Team1SpecialEducation.query.filter(Team1SpecialEducation.team_id == team1.team_id)

            if not show_all_dates:

                query = query.filter(

                    Team1SpecialEducation.submitted_at >= start_of_day,

                    Team1SpecialEducation.submitted_at <= end_of_day

                )

            special_education_data = query.order_by(Team1SpecialEducation.submitted_at.desc()).all()
            team1_special_education_data = []
            for item in special_education_data:
                team1_special_education_data.append({
                    'date': item.submitted_at,
                    'class_name': item.class_name,
                    'total_students': item.total_students,
                    'as_on_date': item.as_on_date,
                    'attended': item.attended,
                    'not_attended': item.not_attended,
                    'nature_of_issue': item.nature_of_issue,
                    'observations': item.observations,
                    'issue_description': item.issue_description,
                    'comments': item.comments,
                    'schedule': item.schedule
                })

                # Get Team 1 Hostel data with proper date filtering
            query = Team1Hostel.query.filter(Team1Hostel.team_id == team1.team_id)

            if not show_all_dates:

                query = query.filter(

                    Team1Hostel.submitted_at >= start_of_day,

                    Team1Hostel.submitted_at <= end_of_day

                )

            hostel_data = query.order_by(Team1Hostel.submitted_at.desc()).all()
            team1_hostel_data = []
            for item in hostel_data:
                team1_hostel_data.append({
                    'date': item.submitted_at,
                    'hostel_students': item.hostel_students,
                    'hostel_payment': item.hostel_payment,
                    'hostel_food_concern': item.hostel_food_concern,
                    'hostel_general_concern': item.hostel_general_concern
                })

                # Get Team 1 SEC data with proper date filtering
            # Get Team 1 SEC data with proper date filtering
            query = Team1SEC.query.filter(Team1SEC.team_id == team1.team_id)

            if not show_all_dates:

                query = query.filter(

                    Team1SEC.submitted_at >= start_of_day,

                    Team1SEC.submitted_at <= end_of_day

                )

            sec_data = query.order_by(Team1SEC.submitted_at.desc()).all()
            team1_sec_data = []
            for item in sec_data:
                team1_sec_data.append({
                    'date': item.submitted_at,
                    'sec_committee': item.sec_committee,
                    'sec_schedule': item.sec_schedule,
                    'sec_meeting_status': item.sec_meeting_status,
                    'sec_md_mom_review': item.sec_md_mom_review,
                    'sec_next_meeting': item.sec_next_meeting,
                    'sec_atr_completion_status': item.sec_atr_completion_status
                })

                # Get Team 1 School Counsellor data with proper date filtering
            query = Team1SchoolCounsellor.query.filter(Team1SchoolCounsellor.team_id == team1.team_id)

            if not show_all_dates:

                query = query.filter(

                    Team1SchoolCounsellor.submitted_at >= start_of_day,

                    Team1SchoolCounsellor.submitted_at <= end_of_day

                )

            school_counsellor_data = query.order_by(Team1SchoolCounsellor.submitted_at.desc()).all()
            team1_school_counsellor_data = []
            for item in school_counsellor_data:
                team1_school_counsellor_data.append({
                    'date': item.submitted_at,
                    'rapid_category': item.rapid_category,
                    'rapid_subtopic': item.rapid_subtopic,
                    'rapid_total_issues': item.rapid_total_issues,
                    'rapid_met_so_far': item.rapid_met_so_far,
                    'rapid_pending': item.rapid_pending,
                    'rapid_follow_up': item.rapid_follow_up,
                    'rapid_issue_closed': item.rapid_issue_closed,
                    'rapid_critical': item.rapid_critical,
                    'rapid_manageable': item.rapid_manageable,
                    'rapid_issue_categories': item.rapid_issue_categories,
                    'rapid_nature_of_issues': item.rapid_nature_of_issues,
                    'rapid_count': item.rapid_count,
                    'rapid_duration': item.rapid_duration,
                    'rapid_comments': item.rapid_comments
                })

                # Get Team 1 Scholorius data with proper date filtering
            query = Team1Scholorius.query.filter(Team1Scholorius.team_id == team1.team_id)

            if not show_all_dates:

                query = query.filter(

                    Team1Scholorius.submitted_at >= start_of_day,

                    Team1Scholorius.submitted_at <= end_of_day

                )

            scholorius_data = query.order_by(Team1Scholorius.submitted_at.desc()).all()
            team1_scholorius_data = []
            for item in scholorius_data:
                team1_scholorius_data.append({
                    'date': item.submitted_at,
                    'scholorius_program': item.scholorius_program,
                    'scholorius_date': item.scholorius_date,
                    'scholorius_status': item.scholorius_status,
                    'scholorius_remark': item.scholorius_remark
                })


        # team 1 completed


 # Get Team 2 data if selected team is 'all' or 'team2'
    if selected_team in ['all', 'team2']:
        team2 = Team.query.filter_by(team_name='Team 2').first()
        if team2:
            # Get Team 2 HR Attendance data with proper date filtering
            query = Team2HRAttendance.query.filter(Team2HRAttendance.team_id == team2.team_id)

            if not show_all_dates:

                query = query.filter(

                    Team2HRAttendance.submitted_at >= start_of_day,

                    Team2HRAttendance.submitted_at <= end_of_day

                )

            hr_data = query.order_by(Team2HRAttendance.submitted_at.desc()).all()
            team2_hr_attendance_data = [{
                'date': item.submitted_at,
                'jr_school': {
                    'total': item.hr_att_jr_school_total,
                    'present': item.hr_att_jr_school_present,
                    'leave': item.hr_att_jr_school_leave,
                    'leave_perc': item.hr_att_jr_school_leave_perc,
                    'nature': item.hr_att_jr_school_nature,
                    'issue_desc': item.hr_att_jr_school_issue_desc,
                    'comments': item.hr_att_jr_school_comments
                },
                'sr_school': {
                    'total': item.hr_att_sr_school_total,
                    'present': item.hr_att_sr_school_present,
                    'leave': item.hr_att_sr_school_leave,
                    'leave_perc': item.hr_att_sr_school_leave_perc,
                    'nature': item.hr_att_sr_school_nature,
                    'issue_desc': item.hr_att_sr_school_issue_desc,
                    'comments': item.hr_att_sr_school_comments
                },
                'eca': {
                    'total': item.hr_att_eca_total,
                    'present': item.hr_att_eca_present,
                    'leave': item.hr_att_eca_leave,
                    'leave_perc': item.hr_att_eca_leave_perc,
                    'nature': item.hr_att_eca_nature,
                    'issue_desc': item.hr_att_eca_issue_desc,
                    'comments': item.hr_att_eca_comments
                },
                'overall': {
                    'total': item.hr_att_acad_overall_total,
                    'present': item.hr_att_acad_overall_present,
                    'leave': item.hr_att_acad_overall_leave,
                    'leave_perc': item.hr_att_acad_overall_leave_perc
                }
            } for item in hr_data]

            # Get Team 2 Total HR Attendance data
            query = Team2TotalHRAttendance.query.filter(Team2TotalHRAttendance.team_id == team2.team_id)

            if not show_all_dates:

                query = query.filter(

                    Team2TotalHRAttendance.submitted_at >= start_of_day,

                    Team2TotalHRAttendance.submitted_at <= end_of_day

                )

            total_hr_data = query.order_by(Team2TotalHRAttendance.submitted_at.desc()).all()
            team2_total_hr_attendance_data = [{
                'date': item.submitted_at,
                'category': item.category,
                'total': item.total,
                'present': item.present,
                'leave': item.leave,
                'leave_perc': item.leave_perc,
                'nature': item.nature_of_issue,
                'issue_desc': item.issue_description,
                'comments': item.comments
            } for item in total_hr_data]
            
            # Query filtered by team ID and exact date (with datetime range for index use)
            query = Team2AdminAttendance.query.filter(Team2AdminAttendance.team_id == team2.team_id)

            if not show_all_dates:

                query = query.filter(

                    Team2AdminAttendance.submitted_at >= start_of_day,

                    Team2AdminAttendance.submitted_at <= end_of_day

                )

            admin_data = query.order_by(Team2AdminAttendance.submitted_at.desc()).all()

            # Build structured data (without submitter)
            team2_admin_attendance_data = [{
                'date': item.submitted_at,
                'admin_staff': {
                    'total': item.hr_att_admin_total,
                    'present': item.hr_att_admin_present,
                    'leave': item.hr_att_admin_leave,
                    'leave_perc': item.hr_att_admin_leave_perc,
                    'nature': item.hr_att_admin_nature,
                    'issue_desc': item.hr_att_admin_issue_desc,
                    'comments': item.hr_att_admin_comments
                },
                'drivers': {
                    'total': item.hr_att_drivers_total,
                    'present': item.hr_att_drivers_present,
                    'leave': item.hr_att_drivers_leave,
                    'leave_perc': item.hr_att_drivers_leave_perc,
                    'nature': item.hr_att_drivers_nature,
                    'issue_desc': item.hr_att_drivers_issue_desc,
                    'comments': item.hr_att_drivers_comments
                },
                'security': {
                    'total': item.hr_att_sec_total,
                    'present': item.hr_att_sec_present,
                    'leave': item.hr_att_sec_leave,
                    'leave_perc': item.hr_att_sec_leave_perc,
                    'nature': item.hr_att_sec_nature,
                    'issue_desc': item.hr_att_sec_issue_desc,
                    'comments': item.hr_att_sec_comments
                },
                'housekeeping': {
                    'total': item.hr_att_hk_total,
                    'present': item.hr_att_hk_present,
                    'leave': item.hr_att_hk_leave,
                    'leave_perc': item.hr_att_hk_leave_perc,
                    'nature': item.hr_att_hk_nature,
                    'issue_desc': item.hr_att_hk_issue_desc,
                    'comments': item.hr_att_hk_comments
                },
                'conductors': {
                    'total': item.hr_att_cond_total,
                    'present': item.hr_att_cond_present,
                    'leave': item.hr_att_cond_leave,
                    'leave_perc': item.hr_att_cond_leave_perc,
                    'nature': item.hr_att_cond_nature,
                    'issue_desc': item.hr_att_cond_issue_desc,
                    'comments': item.hr_att_cond_comments
                },
                'overall': {
                    'total': item.hr_att_admin_overall_total,
                    'present': item.hr_att_admin_overall_present,
                    'leave': item.hr_att_admin_overall_leave,
                    'leave_perc': item.hr_att_admin_overall_leave_perc
                }
            } for item in admin_data]
            
            # Get Team 2 Recruitment Activity data with proper date filtering
            query = Team2RecruitmentActivity.query.filter(Team2RecruitmentActivity.team_id == team2.team_id)

            if not show_all_dates:

                query = query.filter(

                    Team2RecruitmentActivity.submitted_at >= start_of_day,

                    Team2RecruitmentActivity.submitted_at <= end_of_day

                )

            recruitment_data = query.order_by(Team2RecruitmentActivity.submitted_at.desc()).all()

            team2_recruitment_activity_data = [{
                'date': item.submitted_at,
                'academic': {
                    'vacancies': item.rec_act_acad_vac_nos,
                    'positions': item.rec_act_acad_pos,
                    'update_text': item.rec_act_acad_update,
                    'nature': item.rec_act_acad_nature,
                    'issue_desc': item.rec_act_acad_issue_desc,
                    'comments': item.rec_act_acad_comments
                },
                'admin': {
                    'vacancies': item.rec_act_admin_vac_nos,
                    'positions': item.rec_act_admin_pos,
                    'update_text': item.rec_act_admin_update,
                    'nature': item.rec_act_admin_nature,
                    'issue_desc': item.rec_act_admin_issue_desc,
                    'comments': item.rec_act_admin_comments
                }
            } for item in recruitment_data]
            
            # Get Team 2 Pending Recruitment data with proper date filtering
            query = Team2PendingRecruitment.query.filter(Team2PendingRecruitment.team_id == team2.team_id)

            if not show_all_dates:

                query = query.filter(

                    Team2PendingRecruitment.submitted_at >= start_of_day,

                    Team2PendingRecruitment.submitted_at <= end_of_day

                )

            pending_data = query.order_by(Team2PendingRecruitment.submitted_at.desc()).all()

            team2_pending_recruitment_data = [{
                'date': item.submitted_at,
                'academic': {
                    'count': item.rec_pend_acad_count,
                    'positions': item.rec_pend_acad_pos,
                    'closure_date': item.rec_pend_acad_closure,
                    'nature': item.rec_pend_acad_nature,
                    'issue_desc': item.rec_pend_acad_issue_desc,
                    'comments': item.rec_pend_acad_comments
                },
                'admin': {
                    'count': item.rec_pend_admin_count,
                    'positions': item.rec_pend_admin_pos,
                    'closure_date': item.rec_pend_admin_closure,
                    'nature': item.rec_pend_admin_nature,
                    'issue_desc': item.rec_pend_admin_issue_desc,
                    'comments': item.rec_pend_admin_comments
                }
            } for item in pending_data]
            
            # Get Team 2 Recruitment Pipeline data (new schema: one row per position)
            query = Team2RecruitmentPipeline.query.filter(Team2RecruitmentPipeline.team_id == team2.team_id)
            if not show_all_dates:
                query = query.filter(
                    Team2RecruitmentPipeline.submitted_at >= start_of_day,
                    Team2RecruitmentPipeline.submitted_at <= end_of_day
                )
            pipeline_rows = query.order_by(Team2RecruitmentPipeline.submitted_at.desc()).all()

            # Group rows by submitted date (day) into academic/non-academic buckets
            grouped_pipeline = {}
            for row in pipeline_rows:
                date_key = row.submitted_at.date() if hasattr(row.submitted_at, 'date') else row.submitted_at
                if date_key not in grouped_pipeline:
                    grouped_pipeline[date_key] = {
                        'date': date_key,
                        'academic': [],
                        'non_academic': []
                    }

                entry = {
                    'position': row.position,
                    'hired': row.hired,
                    'shortlisted': row.shortlisted
                }

                category_value = (row.category or '').lower()
                if category_value.startswith('non'):
                    grouped_pipeline[date_key]['non_academic'].append(entry)
                else:
                    grouped_pipeline[date_key]['academic'].append(entry)

            # Sort by date descending
            team2_recruitment_pipeline_data = sorted(grouped_pipeline.values(), key=lambda x: x['date'], reverse=True)

            # Get Team 2 Staff Status Updates data
            query = Team2StaffStatusUpdates.query.filter(Team2StaffStatusUpdates.team_id == team2.team_id)

            if not show_all_dates:

                query = query.filter(

                    Team2StaffStatusUpdates.submitted_at >= start_of_day,

                    Team2StaffStatusUpdates.submitted_at <= end_of_day

                )

            staff_status_updates_data = query.order_by(Team2StaffStatusUpdates.submitted_at.desc()).all()

            team2_staff_status_updates_data = [{
                'date': item.submitted_at,
                'obs_name': item.obs_name,
                'obs_dept': item.obs_dept,  
                'obs_desig': item.obs_desig,
                'obs_doj': item.obs_doj,
                'obs_shadow': item.obs_shadow,
                'obs_completed': item.obs_completed,
                'obs_comments': item.obs_comments,
            } for item in staff_status_updates_data] 
            
            # Get Team 2 Salary Pending data
            query = Team2SalaryPending.query.filter(Team2SalaryPending.team_id == team2.team_id)

            if not show_all_dates:

                query = query.filter(

                    Team2SalaryPending.submitted_at >= start_of_day,

                    Team2SalaryPending.submitted_at <= end_of_day

                )

            salary_pending_data = query.order_by(Team2SalaryPending.submitted_at.desc()).all()

            team2_salary_pending_data = [{
                'date': item.submitted_at,
                'sal_pend_name': item.sal_pend_name,
                'sal_pend_dept': item.sal_pend_dept,
                'sal_pend_desig': item.sal_pend_desig,
                'sal_pend_comments': item.sal_pend_comments
            } for item in salary_pending_data]  

            
            # Get Team 2 Police Verification data
            query = Team2PoliceVerification.query.filter(Team2PoliceVerification.team_id == team2.team_id)

            if not show_all_dates:

                query = query.filter(

                    Team2PoliceVerification.submitted_at >= start_of_day,

                    Team2PoliceVerification.submitted_at <= end_of_day

                )

            police_verification_data = query.order_by(Team2PoliceVerification.submitted_at.desc()).all()
            team2_police_verification_data = [{
                'date': item.submitted_at,
                'department': item.department,
                'strength': item.strength,
                'completed': item.completed,
                'pending': item.pending,
                'remarks': item.remarks,
            } for item in police_verification_data] 
            
            # Get Team 2 Interview Schedule data
            query = Team2InterviewSchedule.query.filter(Team2InterviewSchedule.team_id == team2.team_id)

            if not show_all_dates:

                query = query.filter(

                    Team2InterviewSchedule.submitted_at >= start_of_day,

                    Team2InterviewSchedule.submitted_at <= end_of_day

                )

            interview_schedule_data = query.order_by(Team2InterviewSchedule.submitted_at.desc()).all()
            team2_interview_schedule_data = [{
                'date': item.submitted_at,
                'department_category': item.department_category,
                'candidate_count': item.candidate_count,
                'interview_completion': item.interview_completion,
                'interview_status': item.interview_status,
                'nature_of_issue': item.nature_of_issue,
                'issue_description': item.issue_description,
                'comments': item.comments,
            } for item in interview_schedule_data]
            
            # Get Team 2 Exit Information data
            query = Team2ExitInformation.query.filter(Team2ExitInformation.team_id == team2.team_id)

            if not show_all_dates:

                query = query.filter(

                    Team2ExitInformation.submitted_at >= start_of_day,

                    Team2ExitInformation.submitted_at <= end_of_day

                )

            exit_information_data = query.order_by(Team2ExitInformation.submitted_at.desc()).all()
            team2_exit_information_data = [{
                'date': item.submitted_at,
                'exit_activity': item.exit_activity,
                'exit_department': item.exit_department,
                'exit_notice': item.exit_notice,
                'exit_name': item.exit_name,
                'exit_dept': item.exit_dept,
                'exit_reason': item.exit_reason,
                'exit_nature': item.exit_nature,
                'exit_issue_desc': item.exit_issue_desc,
                'exit_comments': item.exit_comments,
            } for item in exit_information_data]
            
          # Get Team 2 Issues / Staff Concerns data
            query = Team2IssuesStaffConcerns.query.filter(
                Team2IssuesStaffConcerns.team_id == team2.team_id,
                Team2IssuesStaffConcerns.submitted_at.isnot(None)
            )
            if not show_all_dates:
                query = query.filter(
                    Team2IssuesStaffConcerns.submitted_at >= start_of_day,
                    Team2IssuesStaffConcerns.submitted_at <= end_of_day
                )
            issues_staff_concerns_data = query.order_by(Team2IssuesStaffConcerns.submitted_at.desc()).all()
            team2_issues_staff_concerns_data = [{
                'date': item.submitted_at,
                'sno': item.concern_sno,
                'activity': item.concern_activity,
                'dept': item.concern_dept,
                'person': item.concern_person,
                'incharge': item.concern_incharge,
                'nature': item.concern_nature,
                'issue_desc': item.concern_issue_desc,
                'comments': item.concern_comments
            } for item in issues_staff_concerns_data]


            # Get Team 2 Kural Recitation data
            query = Team2KuralRecitation.query.filter(Team2KuralRecitation.team_id == team2.team_id)

            if not show_all_dates:

                query = query.filter(

                    Team2KuralRecitation.submitted_at >= start_of_day,

                    Team2KuralRecitation.submitted_at <= end_of_day

                )

            kural_recitation_data = query.order_by(Team2KuralRecitation.submitted_at.desc()).all()
            team2_kural_recitation_data = [{
                'date': item.submitted_at,
                'team': item.kural_team,
                'name': item.kural_name,
                'happened': item.kural_happened,
                'not_happened_reason': item.kural_not_happened_reason,
                'nature': item.kural_nature,
                'issue_desc': item.kural_issue_desc,
                'comments': item.kural_comments
            } for item in kural_recitation_data]
            
            # Get Team 2 Front Office Phone Calls data
            query = Team2FrontOfficePhoneCalls.query.filter(Team2FrontOfficePhoneCalls.team_id == team2.team_id)

            if not show_all_dates:

                query = query.filter(

                    Team2FrontOfficePhoneCalls.submitted_at >= start_of_day,

                    Team2FrontOfficePhoneCalls.submitted_at <= end_of_day

                )

            front_office_phone_calls_data = query.order_by(Team2FrontOfficePhoneCalls.submitted_at.desc()).all()
            team2_front_office_phone_calls_data = [{
                'date': item.submitted_at,
                'category': item.category,
                'incoming': item.incoming,
                'outgoing': item.outgoing,
                'nature': item.nature,
                'issue_description': item.issue_description,
                'comments': item.comments
            } for item in front_office_phone_calls_data]
            
            # Get Team 2 Visitor Log data
            query = Team2VisitorLog.query.filter(Team2VisitorLog.team_id == team2.team_id)

            if not show_all_dates:

                query = query.filter(

                    Team2VisitorLog.submitted_at >= start_of_day,

                    Team2VisitorLog.submitted_at <= end_of_day

                )

            visitor_log_data = query.order_by(Team2VisitorLog.submitted_at.desc()).all()
            team2_visitor_log_data = [{
                'date': item.submitted_at,
                'visitor_type': item.visitor_type,
                'purpose': item.purpose,
                'person_met': item.person_met,
                'nature': item.nature,
                'issue_description': item.issue_description,
                'comments': item.comments
            } for item in visitor_log_data]
            
            # Get Team 2 BSNL Phone Status data
            query = Team2BSNLPhoneStatus.query.filter(Team2BSNLPhoneStatus.team_id == team2.team_id)

            if not show_all_dates:

                query = query.filter(

                    Team2BSNLPhoneStatus.submitted_at >= start_of_day,

                    Team2BSNLPhoneStatus.submitted_at <= end_of_day

                )

            bsnl_phone_status_data = query.order_by(Team2BSNLPhoneStatus.submitted_at.desc()).all()
            team2_bsnl_phone_status_data = [{
                'date': item.submitted_at,
                'department': item.department,
                'working': item.working,
                'not_working': item.not_working,
                'rectified': item.rectified,
                'nature': item.nature,
                'issue_description': item.issue_description,
                'comments': item.comments
            } for item in bsnl_phone_status_data]
            
            # Get Team 2 Materials Inward data
            query = Team2MaterialsInward.query.filter(Team2MaterialsInward.team_id == team2.team_id)

            if not show_all_dates:

                query = query.filter(

                    Team2MaterialsInward.submitted_at >= start_of_day,

                    Team2MaterialsInward.submitted_at <= end_of_day

                )

            materials_inward_data = query.order_by(Team2MaterialsInward.submitted_at.desc()).all()
            team2_materials_inward_data = [{
                'date': item.submitted_at,
                'work_activity': item.work_activity,
                'department_category': item.department_category,
                'product_material': item.product_material,
                'in_time': item.in_time.strftime('%H:%M:%S') if item.in_time else None,
                'vendor': item.vendor,
                'description': item.description,
                'quantity': item.quantity,
                'nature': item.nature,
                'issue_description': item.issue_description,
                'comments': item.comments
            } for item in materials_inward_data]
            
            # Get Team 2 Materials Outward data
            query = Team2MaterialsOutward.query.filter(Team2MaterialsOutward.team_id == team2.team_id)

            if not show_all_dates:

                query = query.filter(

                    Team2MaterialsOutward.submitted_at >= start_of_day,

                    Team2MaterialsOutward.submitted_at <= end_of_day

                )

            materials_outward_data = query.order_by(Team2MaterialsOutward.submitted_at.desc()).all()
            team2_materials_outward_data = [{
                'date': item.submitted_at,
                'product_material': item.product_material,
                'out_time': item.out_time.strftime('%H:%M:%S') if item.out_time else None,
                'vendor': item.vendor,
                'description': item.description,
                'quantity': item.quantity,
                'nature': item.nature,
                'issue_description': item.issue_description,
                'comments': item.comments
            } for item in materials_outward_data]
            
            # Get Team 2 Materials Movement data
            query = Team2MaterialsMovement.query.filter(Team2MaterialsMovement.team_id == team2.team_id)

            if not show_all_dates:

                query = query.filter(

                    Team2MaterialsMovement.submitted_at >= start_of_day,

                    Team2MaterialsMovement.submitted_at <= end_of_day

                )

            materials_movement_data = query.order_by(Team2MaterialsMovement.submitted_at.desc()).all()
            team2_materials_movement_data = [{
                'date': item.submitted_at,
                'returnable': item.returnable,
                'non_returnable': item.non_returnable,
                'nature': item.nature,
                'issue_description': item.issue_description,
                'comments': item.comments
            } for item in materials_movement_data]
            
            # Get Team 2 Returnable Material Tracking data
            query = Team2ReturnableMaterialTracking.query.filter(Team2ReturnableMaterialTracking.team_id == team2.team_id)

            if not show_all_dates:

                query = query.filter(

                    Team2ReturnableMaterialTracking.submitted_at >= start_of_day,

                    Team2ReturnableMaterialTracking.submitted_at <= end_of_day

                )

            returnable_material_tracking_data = query.order_by(Team2ReturnableMaterialTracking.submitted_at.desc()).all()
            team2_returnable_material_tracking_data = [{
                'date': item.submitted_at,
                'description': item.description,
                'quantity': item.quantity,
                'issue_date': item.issue_date.strftime('%Y-%m-%d') if item.issue_date else None,
                'return_date': item.return_date.strftime('%Y-%m-%d') if item.return_date else None,
                'nature': item.nature,
                'issue_description': item.issue_description,
                'comments': item.comments
            } for item in returnable_material_tracking_data]
            
            # Get Team 2 Returnable Goods Report data
            query = Team2ReturnableGoodsReport.query.filter(Team2ReturnableGoodsReport.team_id == team2.team_id)

            if not show_all_dates:

                query = query.filter(

                    Team2ReturnableGoodsReport.submitted_at >= start_of_day,

                    Team2ReturnableGoodsReport.submitted_at <= end_of_day

                )

            returnable_goods_report_data = query.order_by(Team2ReturnableGoodsReport.submitted_at.desc()).all()
            team2_returnable_goods_report_data = [{
                'date': item.submitted_at,
                'description': item.description,
                'quantity': item.quantity,
                'issue_date': item.issue_date.strftime('%Y-%m-%d') if item.issue_date else None,
                'return_date': item.return_date.strftime('%Y-%m-%d') if item.return_date else None,
                'nature': item.nature,
                'issue_description': item.issue_description,
                'comments': item.comments
            } for item in returnable_goods_report_data]

            # Get Team 2 Campus Camera Status data
            query = Team2CampusCameraStatus.query.filter(Team2CampusCameraStatus.team_id == team2.team_id)

            if not show_all_dates:

                query = query.filter(

                    Team2CampusCameraStatus.submitted_at >= start_of_day,

                    Team2CampusCameraStatus.submitted_at <= end_of_day

                )

            campus_camera_status_data = query.order_by(Team2CampusCameraStatus.submitted_at.desc()).all()
            team2_campus_camera_status_data = [{
                'date': item.submitted_at,
                'particulars': item.particulars,
                'total_cameras': item.total_cameras,
                'working_cameras': item.working_cameras,
                'not_working_details': item.not_working_details,
                'nature_of_issue': item.nature_of_issue,
                'issue_description': item.issue_description,
                'comments': item.comments
            } for item in campus_camera_status_data]
            
            # Get Team 2 Vehicle Camera Status data
            query = Team2VehicleCameraStatus.query.filter(Team2VehicleCameraStatus.team_id == team2.team_id)

            if not show_all_dates:

                query = query.filter(

                    Team2VehicleCameraStatus.submitted_at >= start_of_day,

                    Team2VehicleCameraStatus.submitted_at <= end_of_day

                )

            vehicle_camera_status_data = query.order_by(Team2VehicleCameraStatus.submitted_at.desc()).all()
            team2_vehicle_camera_status_data = [{
                'date': item.submitted_at,
                'particulars': item.particulars,
                'route_numbers': item.route_numbers,
                'camera_id': item.camera_id,
                'working_status': item.working_status,
                'not_working_details': item.not_working_details,
                'nature_of_issue': item.nature_of_issue,
                'issue_description': item.issue_description,
                'comments': item.comments
            } for item in vehicle_camera_status_data]

            # Get Team 2 Bus AC Camera Status data
            query = Team2BusACCameraStatus.query.filter(Team2BusACCameraStatus.team_id == team2.team_id)

            if not show_all_dates:

                query = query.filter(

                    Team2BusACCameraStatus.submitted_at >= start_of_day,

                    Team2BusACCameraStatus.submitted_at <= end_of_day

                )

            bus_ac_camera_status_data = query.order_by(Team2BusACCameraStatus.submitted_at.desc()).all()
            team2_bus_ac_camera_status_data = [{
                'date': item.submitted_at,
                'particulars': item.particulars,
                'route': item.route,
                'camera_id': item.camera_id,
                'working_status': item.working_status,
                'not_working_details': item.not_working_details,
                'nature_of_issue': item.nature_of_issue,
                'issue_description': item.issue_description,
                'comments': item.comments
            } for item in bus_ac_camera_status_data]

# Get GPS Monitoring data
            query = Team2GPSMonitoring.query.filter(Team2GPSMonitoring.team_id == team2.team_id)

            if not show_all_dates:

                query = query.filter(

                    Team2GPSMonitoring.submitted_at >= start_of_day,

                    Team2GPSMonitoring.submitted_at <= end_of_day

                )

            gps_monitoring_data = query.order_by(Team2GPSMonitoring.submitted_at.desc()).all()
            team2_gps_monitoring_data = []
            for item in gps_monitoring_data:
                team2_gps_monitoring_data.append({
                    'date': item.submitted_at,
                    'particulars': item.particulars,
                    'vehicles': item.vehicles,
                    'halt_2_mins': item.halt_2_mins,
                    'over_speed': item.over_speed,
                    'footage': f'/file/{item.footage_file_id}' if item.footage_file_id else None,
                    'nature_of_issue': item.nature_of_issue,
                    'issue_description': item.issue_description,    
                    'comments': item.comments
                })

            # Get Issues Identified (Monitoring) data
            query = Team2IssuesIdentifiedMonitoring.query.filter(Team2IssuesIdentifiedMonitoring.team_id == team2.team_id)

            if not show_all_dates:

                query = query.filter(

                    Team2IssuesIdentifiedMonitoring.submitted_at >= start_of_day,

                    Team2IssuesIdentifiedMonitoring.submitted_at <= end_of_day

                )

            issues_identified_monitoring_data = query.order_by(Team2IssuesIdentifiedMonitoring.submitted_at.desc()).all()
            team2_issues_identified_monitoring_data = []
            for item in issues_identified_monitoring_data:
                team2_issues_identified_monitoring_data.append({
                    'date': item.submitted_at,
                    'particulars': item.particulars,
                    'venue': item.venue,
                    'time': item.time,
                    'nature_of_issue': item.nature_of_issue,
                    'escalated_to': item.escalated_to,
                    'action_taken': item.action_taken,
                    'any_issues_on_observation': item.any_issues_on_observation
                })

            # Get Teachers Late Reporting data
            query = Team2IssuesIdentifiedControlRoom.query.filter(Team2IssuesIdentifiedControlRoom.team_id == team2.team_id)

            if not show_all_dates:

                query = query.filter(

                    Team2IssuesIdentifiedControlRoom.submitted_at >= start_of_day,

                    Team2IssuesIdentifiedControlRoom.submitted_at <= end_of_day

                )

            teachers_late_reporting_data = query.order_by(Team2IssuesIdentifiedControlRoom.submitted_at.desc()).all()
            team2_teachers_late_reporting_data = [{
                 'date': item.submitted_at,
                 'particulars': item.particulars,
                 'no_of_late_reports': item.no_of_late_reports,
                 'no_of_members_entered_reason': item.no_of_members_entered_reason,
                 'on_time_acknowledgement': item.on_time_acknowledgement,
                 'nature_of_issue': item.nature_of_issue,
                 'escalated_to': item.escalated_to,
                 'action_taken': item.action_taken
            } for item in teachers_late_reporting_data]

             # team2_issues_camera_footage
            query = Team2CameraFootageEntry.query.filter(Team2CameraFootageEntry.team_id == team2.team_id)

            if not show_all_dates:

                query = query.filter(

                    Team2CameraFootageEntry.submitted_at >= start_of_day,

                    Team2CameraFootageEntry.submitted_at <= end_of_day

                )

            camera_footage_data = query.order_by(Team2CameraFootageEntry.submitted_at.desc()).all()
            team2_camera_footage_data = [{
                'date': item.submitted_at,
                'particulars': item.particulars,
                'name': item.name,
                'comments': item.comments
            } for item in camera_footage_data]

            # Get Team 2 Biometrics Access Card Punching data
            query = Team2BiometricsAccessCardPunching.query.filter(Team2BiometricsAccessCardPunching.team_id == team2.team_id)

            if not show_all_dates:

                query = query.filter(

                    Team2BiometricsAccessCardPunching.submitted_at >= start_of_day,

                    Team2BiometricsAccessCardPunching.submitted_at <= end_of_day

                )

            biometrics_data = query.order_by(Team2BiometricsAccessCardPunching.submitted_at.desc()).all()
            team2_biometrics_access_card_punching_data = [
                {
                    'date': item.submitted_at,
                    'particulars': item.particulars,  # Use particulars instead of category
                    'total': item.total_punching,
                    'absent': item.absent_punching,
                    'punched': item.punched_punching,
                    'not_punched': item.not_punching,
                    'nature_of_issue': item.nature_of_issue,
                    'issue_description': item.issue_description,
                    'comments': item.comments
                }
                for item in biometrics_data
            ]



     # Get Water TDS Deviation data

            query = Team2WaterTDSDeviation.query.filter(Team2WaterTDSDeviation.team_id == team2.team_id)


            if not show_all_dates:


                query = query.filter(


                    Team2WaterTDSDeviation.submitted_at >= start_of_day,


                    Team2WaterTDSDeviation.submitted_at <= end_of_day


                )


            water_tds_deviation_data = query.order_by(Team2WaterTDSDeviation.submitted_at.desc()).all()
            team2_water_tds_deviation_data = [{
                'date': item.submitted_at,
                'particulars': item.particulars,
                'ro_details': item.ro_details,
                'tds': item.tds,
                'ph': item.ph,
                'nature_of_issue': item.nature_of_issue,
                'issue_description': item.issue_description,
                'comments': item.comments
            } for item in water_tds_deviation_data]

    # Get Testing & Cleaning data
            query = Team2TestingCleaning.query.filter(Team2TestingCleaning.team_id == team2.team_id)

            if not show_all_dates:

                query = query.filter(

                    Team2TestingCleaning.submitted_at >= start_of_day,

                    Team2TestingCleaning.submitted_at <= end_of_day

                )

            testing_cleaning_data = query.order_by(Team2TestingCleaning.submitted_at.desc()).all()
            team2_testing_cleaning_data = [{
                'date': item.submitted_at,
                'particulars': item.particulars,
                'regular_process': item.regular_process,
                'deep_cleaning': item.deep_cleaning,
                'event_arrangement': item.event_arrangement,
                'nature_of_issue': item.nature_of_issue,
                'issue_description': item.issue_description,
                'comments': item.comments
            } for item in testing_cleaning_data]

            # Get Water Level Checking data
                # Query water level data for the team and date range
            query = Team2WaterLevel.query.filter(Team2WaterLevel.team_id == team2.team_id)

            if not show_all_dates:

                query = query.filter(

                    Team2WaterLevel.submitted_at >= start_of_day,

                    Team2WaterLevel.submitted_at <= end_of_day

                )

            water_level_data = query.order_by(Team2WaterLevel.submitted_at.desc()).all()

            # Convert to a structured list of dicts for JSON or template rendering
            team2_water_level_data = [{
                'date': item.submitted_at,
                'work_activity': item.work_activity,
                'department': item.department,
                'particulars': item.particulars,
                'floor': item.floor,
                'venue': item.venue,
                'nature_of_issue': item.nature_of_issue,
                'issue_description': item.issue_description,
                'comments': item.comments
            } for item in water_level_data]

            # Get Housekeeping General data
            # Query housekeeping general data for the team and date range
            query = Team2HousekeepingGeneral.query.filter(Team2HousekeepingGeneral.team_id == team2.team_id)

            if not show_all_dates:

                query = query.filter(

                    Team2HousekeepingGeneral.submitted_at >= start_of_day,

                    Team2HousekeepingGeneral.submitted_at <= end_of_day

                )

            housekeeping_general_data = query.order_by(Team2HousekeepingGeneral.submitted_at.desc()).all()

            # Convert to a structured list of dicts for JSON or template rendering
            team2_housekeeping_general_data = [{
                'date': item.submitted_at,
                'work_activity': item.work_activity,
                'department': item.department,
                'particulars': item.particulars,
                'name': item.name,
                'observation': item.observation,
                'remark': item.remark
            } for item in housekeeping_general_data]


    # Get Pool Testing data
            query = Team2PoolTesting.query.filter(Team2PoolTesting.team_id == team2.team_id)

            if not show_all_dates:

                query = query.filter(

                    Team2PoolTesting.submitted_at >= start_of_day,

                    Team2PoolTesting.submitted_at <= end_of_day

                )

            pool_testing_data = query.order_by(Team2PoolTesting.submitted_at.desc()).all()
            team2_pool_testing_data = [{
                'date': item.submitted_at,
                'particulars': item.particulars,
                'chlorine_level': item.chlorine_level,
                'ph_level': item.ph_level,
                'water_cleanliness': item.water_cleanliness,
                'nature_of_issue': item.nature_of_issue,
                'issue_description': item.issue_description,
                'comments': item.comments
            } for item in pool_testing_data]

     # Get Washroom Cleanliness data
            query = Team2WashroomCleanliness.query.filter(Team2WashroomCleanliness.team_id == team2.team_id)

            if not show_all_dates:

                query = query.filter(

                    Team2WashroomCleanliness.submitted_at >= start_of_day,

                    Team2WashroomCleanliness.submitted_at <= end_of_day

                )

            washroom_cleanliness_data = query.order_by(Team2WashroomCleanliness.submitted_at.desc()).all()
            team2_washroom_cleanliness_data = [{
                'date': item.submitted_at,
                'floor': item.floor,
                'particulars': item.particulars,
                'boys_washroom': item.boys_washroom,
                'girls_washroom': item.girls_washroom,
                'cleanliness': item.cleanliness,
                'smell': item.smell,
                'restroom_equipment': item.restroom_equipment
            } for item in washroom_cleanliness_data]

    # get Transport Attendance  for team lead 2
            query = Team2TransportAttendance.query.filter(Team2TransportAttendance.team_id == team2.team_id)

            if not show_all_dates:

                query = query.filter(

                    Team2TransportAttendance.submitted_at >= start_of_day,

                    Team2TransportAttendance.submitted_at <= end_of_day

                )

            transport_attendance_data = query.order_by(Team2TransportAttendance.submitted_at.desc()).all()
            team2_transport_attendance_data = [{
                'date': item.submitted_at,
                'work_activity': item.work_activity,
                'department': item.department,
                'particulars': item.particulars,
                'students_morning': item.students_morning,
                'students_evening': item.students_evening,
                'staff_morning': item.staff_morning,
                'staff_evening': item.staff_evening,
                'nature_of_issue': item.nature_of_issue,
                'issue_description': item.issue_description,
                'comments': item.comments
            } for item in transport_attendance_data]

     #get AC Working Status  for team lead 2
            query = Team2ACWorkingStatus.query.filter(Team2ACWorkingStatus.team_id == team2.team_id)

            if not show_all_dates:

                query = query.filter(

                    Team2ACWorkingStatus.submitted_at >= start_of_day,

                    Team2ACWorkingStatus.submitted_at <= end_of_day

                )

            ac_working_status_data = query.order_by(Team2ACWorkingStatus.submitted_at.desc()).all()
            team2_ac_working_status_data = [{
                'date': item.submitted_at,
                'work_activity': item.work_activity,
                'department': item.department,
                'particulars': item.particulars,
                'route_numbers': item.route_numbers,
                'nature_of_issue': item.nature_of_issue,
                'issue_description': item.issue_description,
                'comments': item.comments
            } for item in ac_working_status_data]

    # Late Reporting  for team lead 2
            query = Team2LateReporting.query.filter(Team2LateReporting.team_id == team2.team_id)

            if not show_all_dates:

                query = query.filter(

                    Team2LateReporting.submitted_at >= start_of_day,

                    Team2LateReporting.submitted_at <= end_of_day

                )

            late_reporting_data = query.order_by(Team2LateReporting.submitted_at.desc()).all()
            team2_late_reporting_data = [{
                'date': item.submitted_at,
                'work_activity': item.work_activity,
                'department': item.department,
                'particulars': item.particulars,
                'route_numbers': item.route_numbers,
                'nature_of_issue': item.nature_of_issue,
                'issue_description': item.issue_description,
                'comments': item.comments
            } for item in late_reporting_data]

    # Maintenance / Service / Issues  for team lead 2
            query = Team2MaintenanceServiceIssues.query.filter(Team2MaintenanceServiceIssues.team_id == team2.team_id)

            if not show_all_dates:

                query = query.filter(

                    Team2MaintenanceServiceIssues.submitted_at >= start_of_day,

                    Team2MaintenanceServiceIssues.submitted_at <= end_of_day

                )

            maintenance_service_issues_data = query.order_by(Team2MaintenanceServiceIssues.submitted_at.desc()).all()
            team2_maintenance_service_issues_data = [{
                'date': item.submitted_at,
                'work_activity': item.work_activity,
                'department': item.department,
                'particulars': item.particulars,
                'route_numbers': item.route_numbers,
                'work_nature': item.work_nature,
                'venue': item.venue,
                'work_status': item.work_status,
                'nature_of_issue': item.nature_of_issue,
                'issue_description': item.issue_description,
                'comments': item.comments
            } for item in maintenance_service_issues_data]

    # Car Maintenance/Cleaning  for team lead 2
            query = Team2CarMaintenanceCleaning.query.filter(Team2CarMaintenanceCleaning.team_id == team2.team_id)

            if not show_all_dates:

                query = query.filter(

                    Team2CarMaintenanceCleaning.submitted_at >= start_of_day,

                    Team2CarMaintenanceCleaning.submitted_at <= end_of_day

                )

            car_maintenance_cleaning_data = query.order_by(Team2CarMaintenanceCleaning.submitted_at.desc()).all()
            team2_car_maintenance_cleaning_data = [{
                'date': item.submitted_at,
                'work_activity': item.work_activity,
                'department': item.department,
                'particulars': item.particulars,
                'car_number': item.car_number,
                'cleaned_by': item.cleaned_by,
                'maintenance_service_issues': item.maintenance_service_issues,
                'nature_of_issue': item.nature_of_issue,
                'issue_description': item.issue_description,
                'comments': item.comments
            } for item in car_maintenance_cleaning_data]

     # Vehicle Renewals / Delays  for team lead 2
            query = Team2VehicleRenewalsDelays.query.filter(Team2VehicleRenewalsDelays.team_id == team2.team_id)

            if not show_all_dates:

                query = query.filter(

                    Team2VehicleRenewalsDelays.submitted_at >= start_of_day,

                    Team2VehicleRenewalsDelays.submitted_at <= end_of_day

                )

            vehicle_renewals_delays_data = query.order_by(Team2VehicleRenewalsDelays.submitted_at.desc()).all()
            team2_vehicle_renewals_delays_data = [{
                'date': item.submitted_at,
                'work_activity': item.work_activity,
                'department': item.department,
                'particulars': item.particulars,
                'vehicle_numbers': item.vehicle_numbers,
                'route_numbers': item.route_numbers,
                'nature_of_issue': item.nature_of_issue,
                'issue_description': item.issue_description,
                'comments': item.comments
            } for item in vehicle_renewals_delays_data]

     # Special Trip  for team lead 2

            query = Team2SpecialTrip.query.filter(Team2SpecialTrip.team_id == team2.team_id)


            if not show_all_dates:


                query = query.filter(


                    Team2SpecialTrip.submitted_at >= start_of_day,


                    Team2SpecialTrip.submitted_at <= end_of_day


                )


            special_trip_data = query.order_by(Team2SpecialTrip.submitted_at.desc()).all()
            team2_special_trip_data = [{
                'date': item.submitted_at,
                'work_activity': item.work_activity,
                'department': item.department,
                'particulars': item.particulars,
                'route_numbers': item.route_numbers,
                'actual_out_time': item.actual_out_time,
                'nature_of_issue': item.nature_of_issue,
                'issue_description': item.issue_description,
                'comments': item.comments
            } for item in special_trip_data]

            # Parent Concern Details  for team lead 2 # Get Team 1 Parent Concern Details data with proper date filtering
            query = Team2ParentConcernDetail.query.filter(Team2ParentConcernDetail.team_id == team2.team_id)

            if not show_all_dates:

                query = query.filter(

                    Team2ParentConcernDetail.submitted_at >= start_of_day,

                    Team2ParentConcernDetail.submitted_at <= end_of_day

                )

            parent_concern_detail_data = query.order_by(Team2ParentConcernDetail.submitted_at.desc()).all()
            team2_parent_concern_detail_data = [{
                
                'date': item.submitted_at,
                'work_activity': item.pc_work_activity,
                'student_name': item.pc_detail_name,
                'grade': item.pc_detail_grade,
                'concern_expressed': item.pc_detail_concern,
                'incharges_handled': item.pc_detail_incharge,
                'nature_of_issue': item.pc_detail_issue_nature,
                'comments': item.pc_detail_comment
            } for item in parent_concern_detail_data]

    #get AC Temperature  for team lead 2
            query = Team2ACTemperatureCheck.query.filter(Team2ACTemperatureCheck.team_id == team2.team_id)

            if not show_all_dates:

                query = query.filter(

                    Team2ACTemperatureCheck.submitted_at >= start_of_day,

                    Team2ACTemperatureCheck.submitted_at <= end_of_day

                )

            ac_temperature_data = query.order_by(Team2ACTemperatureCheck.submitted_at.desc()).all()
            team2_ac_temperature_data = [{
                'date': item.submitted_at,
                'work_activity': item.work_activity,
                'department': item.department,
                'floor': item.floor,
                'particulars': item.particulars,
                'classroom': item.classroom,
                'temperature': item.temperature,
                'hot_cold_normal': item.hot_cold_normal,
                'working_condition': item.working_condition,
                'nature_of_issue': item.nature_of_issue,
                'issue_description': item.issue_description,
                'comments': item.comments
            } for item in ac_temperature_data]

    # get Section 15: Labor, EB, Solar, Genset

    # Labor, EB, Solar, Genset - Maintenance Labor

            query = Team2LaborEbSolarGenset.query.filter(Team2LaborEbSolarGenset.team_id == team2.team_id)


            if not show_all_dates:


                query = query.filter(


                    Team2LaborEbSolarGenset.submitted_at >= start_of_day,


                    Team2LaborEbSolarGenset.submitted_at <= end_of_day


                )


            labor_eb_solar_genset_data = query.order_by(Team2LaborEbSolarGenset.submitted_at.desc()).all()
            team2_maintenance_labor_data = [{
                'date': item.submitted_at,
                'work_activity': item.work_activity,
                'department': item.department,
                'nature_of_work': item.nature_of_work,
                'no_of_labours': item.no_of_labours,
                'venue': item.venue,
                'nature_of_issue': item.nature_of_issue,
                'issue_description': item.issue_description,
                'comments': item.comments
            } for item in labor_eb_solar_genset_data]

    # Motor Control for team lead 2
            query = Team2Motor.query.filter(Team2Motor.team_id == team2.team_id)

            if not show_all_dates:

                query = query.filter(

                    Team2Motor.submitted_at >= start_of_day,

                    Team2Motor.submitted_at <= end_of_day

                )

            motor_data = query.order_by(Team2Motor.submitted_at.desc()).all()
            team2_motor_data = [{
                'date': item.submitted_at,
                'work_activity': item.work_activity,
                'department': item.department,
                'on_time': item.on_time,
                'off_time': item.off_time,
                'nature_of_issue': item.nature_of_issue,
                'issue_description': item.issue_description,
                'comments': item.comments
            } for item in motor_data]

    # Pest Control for team lead 2
            query = Team2PestControl.query.filter(Team2PestControl.team_id == team2.team_id)

            if not show_all_dates:

                query = query.filter(

                    Team2PestControl.submitted_at >= start_of_day,

                    Team2PestControl.submitted_at <= end_of_day

                )

            pest_control_data = query.order_by(Team2PestControl.submitted_at.desc()).all()
            team2_pest_control_data = [{
                'date': item.submitted_at,
                'work_activity': item.work_activity,
                'department': item.department,
                'in_time': item.in_time,
                'out_time': item.out_time,
                'area_covered': item.area_covered,
                'nature_of_issue': item.nature_of_issue,
                'issue_description': item.issue_description,
                'comments': item.comments
            } for item in pest_control_data]

    # AC Temp Deviation (>27°C)  for team lead 2
            query = Team2ACTempDeviation.query.filter(Team2ACTempDeviation.team_id == team2.team_id)

            if not show_all_dates:

                query = query.filter(

                    Team2ACTempDeviation.submitted_at >= start_of_day,

                    Team2ACTempDeviation.submitted_at <= end_of_day

                )

            ac_temp_deviation_data = query.order_by(Team2ACTempDeviation.submitted_at.desc()).all()
            team2_ac_temp_deviation_data = [{
                'date': item.submitted_at,
                'work_activity': item.work_activity,
                'department': item.department,
                'venue': item.venue,
                'nature_of_issue': item.nature_of_issue,
                'issue_description': item.issue_description,
                'comments': item.comments
            } for item in ac_temp_deviation_data]

     # Electricity Consumption  for team lead 2
            query = Team2ElectricityConsumption.query.filter(Team2ElectricityConsumption.team_id == team2.team_id)

            if not show_all_dates:

                query = query.filter(

                    Team2ElectricityConsumption.submitted_at >= start_of_day,

                    Team2ElectricityConsumption.submitted_at <= end_of_day

                )

            electricity_consumption_data = query.order_by(Team2ElectricityConsumption.submitted_at.desc()).all()
            team2_electricity_consumption_data = [{
                'date': item.submitted_at,
                'work_activity': item.work_activity,
                'department': item.department,
                'category': item.category,
                'total_units': item.total_units,
                'eb': item.eb,
                'solar': item.solar,
                'genset': item.genset,
                'eb_issue': item.eb_issue,
                'solar_issue': item.solar_issue,
                'genset_issue': item.genset_issue,
                'overall_issue_desc': item.overall_issue_desc,
                'overall_comments': item.overall_comments
            } for item in electricity_consumption_data]

     # EB Details  for team lead 2
            query = Team2EBDetails.query.filter(Team2EBDetails.team_id == team2.team_id)

            if not show_all_dates:

                query = query.filter(

                    Team2EBDetails.submitted_at >= start_of_day,

                    Team2EBDetails.submitted_at <= end_of_day

                )

            eb_details_data = query.order_by(Team2EBDetails.submitted_at.desc()).all()
            team2_eb_details_data = [{
                'date': item.submitted_at,
                'work_activity': item.work_activity,
                'department': item.department,
                'category': item.category,
                'rw_230_240': item.rw_230_240,
                'yw_230_240': item.yw_230_240,
                'bw_230_240': item.bw_230_240,
                'max_demand_104': item.max_demand_104,
                'units_per_day': item.units_per_day,
                'nature_of_issue': item.nature_of_issue
            } for item in eb_details_data]

    # Solar Details  for team lead 2
            query = Team2SolarDetails.query.filter(Team2SolarDetails.team_id == team2.team_id)

            if not show_all_dates:

                query = query.filter(

                    Team2SolarDetails.submitted_at >= start_of_day,

                    Team2SolarDetails.submitted_at <= end_of_day

                )

            solar_details_data = query.order_by(Team2SolarDetails.submitted_at.desc()).all()
            team2_solar_details_data = [{
                'date': item.submitted_at,
                'work_activity': item.work_activity,
                'department': item.department,
                'category': item.category,
                'capacity': item.capacity,
                'units_per_day': item.units_per_day,
                'remarks': item.remarks,
                'time': item.time,
                'max_production': item.max_production,
                'nature_of_issue': item.nature_of_issue,
                'issue_description': item.issue_description,
                'comments': item.comments
            } for item in solar_details_data]

    # Genset Details  for team lead 2
            query = Team2GensetDetails.query.filter(Team2GensetDetails.team_id == team2.team_id)

            if not show_all_dates:

                query = query.filter(

                    Team2GensetDetails.submitted_at >= start_of_day,

                    Team2GensetDetails.submitted_at <= end_of_day

                )

            genset_details_data = query.order_by(Team2GensetDetails.submitted_at.desc()).all()
            team2_genset_details_data = [{
                'date': item.submitted_at,
                'work_activity': item.work_activity,
                'department': item.department,
                'category': item.category,
                'on_time': item.on_time,
                'off_time': item.off_time,
                'battery_voltage': item.battery_voltage,
                'coolant_temp': item.coolant_temp,
                'nature_of_issue': item.nature_of_issue,
                'issue_description': item.issue_description,
                'comments': item.comments
            } for item in genset_details_data]

    # Count Verification  for team lead 2

            query = Team2CountVerification.query.filter(Team2CountVerification.team_id == team2.team_id)


            if not show_all_dates:


                query = query.filter(


                    Team2CountVerification.submitted_at >= start_of_day,


                    Team2CountVerification.submitted_at <= end_of_day


                )


            count_verification_data = query.order_by(Team2CountVerification.submitted_at.desc()).all()
            team2_count_verification_data = [{
                'date': item.submitted_at,
                'work_activity': item.work_activity,
                'department': item.department,
                'category': item.category,
                'particulars': item.particulars,
                'total': item.total,
                'received': item.received,
                'submitted': item.submitted,
                'nature_of_issue': item.nature_of_issue,
                'issue_description': item.issue_description,
                'comments': item.comments
            } for item in count_verification_data]

    #Attendance Replacement  for team lead 2
            query = Team2AttendanceReplacement.query.filter(Team2AttendanceReplacement.team_id == team2.team_id)

            if not show_all_dates:

                query = query.filter(

                    Team2AttendanceReplacement.submitted_at >= start_of_day,

                    Team2AttendanceReplacement.submitted_at <= end_of_day

                )

            attendance_replacement_data = query.order_by(Team2AttendanceReplacement.submitted_at.desc()).all()
            team2_attendance_replacement_data = [{
                'date': item.submitted_at,
                'work_activity': item.work_activity,
                'department': item.department,
                'particulars': item.particulars,
                'allotted': item.allotted,
                'replaced': item.replaced,
                'nature_of_issue': item.nature_of_issue,
                'issue_description': item.issue_description,
                'comments': item.comments
            } for item in attendance_replacement_data]

    #Security Info Note  for team lead 2
            query = Team2SecurityInfoNote.query.filter(Team2SecurityInfoNote.team_id == team2.team_id)

            if not show_all_dates:

                query = query.filter(

                    Team2SecurityInfoNote.submitted_at >= start_of_day,

                    Team2SecurityInfoNote.submitted_at <= end_of_day

                )

            security_info_note_data = query.order_by(Team2SecurityInfoNote.submitted_at.desc()).all()
            team2_security_info_note_data = [{
                'date': item.submitted_at,
                'work_activity': item.work_activity,
                'department': item.department,
                'particulars': item.particulars,
                'info_by': item.info_by,
                'information': item.information,
                'nature_of_issue': item.nature_of_issue,
                'issue_description': item.issue_description,
                'comments': item.comments
            } for item in security_info_note_data]

    # Security Govt Officials In/Out  for team lead 2
            query = Team2SecurityGovtInout.query.filter(Team2SecurityGovtInout.team_id == team2.team_id)

            if not show_all_dates:

                query = query.filter(

                    Team2SecurityGovtInout.submitted_at >= start_of_day,

                    Team2SecurityGovtInout.submitted_at <= end_of_day

                )

            security_govt_inout_data = query.order_by(Team2SecurityGovtInout.submitted_at.desc()).all()
            team2_security_govt_inout_data = [{
                'date': item.submitted_at,
                'work_activity': item.work_activity,
                'department': item.department,
                'particulars': item.particulars,
                'in_time': item.in_time,
                'out_time': item.out_time,
                'purpose': item.purpose,
                'nature_of_issue': item.nature_of_issue,
                'issue_description': item.issue_description,
                'comments': item.comments
            } for item in security_govt_inout_data]

    # Security Alcohol Test  for team lead 2
            query = Team2AlcoholTest.query.filter(Team2AlcoholTest.team_id == team2.team_id)

            if not show_all_dates:

                query = query.filter(

                    Team2AlcoholTest.submitted_at >= start_of_day,

                    Team2AlcoholTest.submitted_at <= end_of_day

                )

            alcohol_test_data = query.order_by(Team2AlcoholTest.submitted_at.desc()).all()
            team2_alcohol_test_data = [{
                'date': item.submitted_at,
                'work_activity': item.work_activity,
                'department': item.department,
                'name': item.name,
                'time': item.time,
                'reading': item.reading,
                'comments': item.comments
            } for item in alcohol_test_data]

    # Security Materials Inward  for team lead 2
            query = Team2SecurityMaterialsInout.query.filter(Team2SecurityMaterialsInout.team_id == team2.team_id)

            if not show_all_dates:

                query = query.filter(

                    Team2SecurityMaterialsInout.submitted_at >= start_of_day,

                    Team2SecurityMaterialsInout.submitted_at <= end_of_day

                )

            materials_inward_data = query.order_by(Team2SecurityMaterialsInout.submitted_at.desc()).all()
            team2_security_materials_inward_data = [{
                'date': item.submitted_at,
                'work_activity': item.work_activity,
                'department': item.department,
                'product': item.product,
                'in_time': item.in_time,
                'vendor': item.vendor,
                'description': item.description,
                'quantity': item.quantity,
                'nature_of_issue': item.nature_of_issue,
                'issue_description': item.issue_description,
                'comments': item.comments
            } for item in materials_inward_data]

    # Security Materials Outward  for team lead 2

            query = Team2SecurityMaterialsOutward.query.filter(Team2SecurityMaterialsOutward.team_id == team2.team_id)


            if not show_all_dates:


                query = query.filter(


                    Team2SecurityMaterialsOutward.submitted_at >= start_of_day,


                    Team2SecurityMaterialsOutward.submitted_at <= end_of_day


                )


            materials_outward_data = query.order_by(Team2SecurityMaterialsOutward.submitted_at.desc()).all()
            team2_security_materials_outward_data = [{
                'date': item.submitted_at,
                'work_activity': item.work_activity,
                'department': item.department,
                'product': item.product,
                'out_time': item.out_time,
                'vendor': item.vendor,
                'description': item.description,
                'quantity': item.quantity,
                'nature_of_issue': item.nature_of_issue,
                'issue_description': item.issue_description,
                'comments': item.comments
            } for item in materials_outward_data]

    # Security Transport Verification  for team lead 2

            query = Team2TransportVerification.query.filter(Team2TransportVerification.team_id == team2.team_id)


            if not show_all_dates:


                query = query.filter(


                    Team2TransportVerification.submitted_at >= start_of_day,


                    Team2TransportVerification.submitted_at <= end_of_day


                )


            transport_verification_data = query.order_by(Team2TransportVerification.submitted_at.desc()).all()
            team2_transport_verification_data = [{
                'date': item.submitted_at,
                'work_activity': item.work_activity,
                'department': item.department,
                'vehicle_number': item.vehicle_number,
                'damage_location': item.damage_location,
                'escalated_to': item.escalated_to,
                'nature_of_issue': item.nature_of_issue,
                'issue_description': item.issue_description,
                'comments': item.comments
            } for item in transport_verification_data]

    # Documents Movement  for team lead 2

            query = Team2DocumentsMovement.query.filter(Team2DocumentsMovement.team_id == team2.team_id)


            if not show_all_dates:


                query = query.filter(


                    Team2DocumentsMovement.submitted_at >= start_of_day,


                    Team2DocumentsMovement.submitted_at <= end_of_day


                )


            documents_movement_data = query.order_by(Team2DocumentsMovement.submitted_at.desc()).all()
            team2_documents_movement_data = [{
                'date': item.submitted_at,
                'work_activity': item.work_activity,
                'department': item.department,
                
        # Row 1: New File / Document Entry
                'doc_new_dept': item.doc_new_dept,
                'doc_new_name': item.doc_new_name,
                'doc_new_submitby': item.doc_new_submitby,
                'doc_new_nature': item.doc_new_nature,
                'doc_new_issue': item.doc_new_issue,
                'doc_new_comments': item.doc_new_comments,
        
        # Row 2: Non-Returnable File / Document
                'doc_nonret_dept': item.doc_nonret_dept,
                'doc_nonret_name': item.doc_nonret_name,
                'doc_nonret_issuedto': item.doc_nonret_issuedto,
                'doc_nonret_nature': item.doc_nonret_nature,
                'doc_nonret_issue': item.doc_nonret_issue,
                'doc_nonret_comments': item.doc_nonret_comments,
        
        # Row 3: Original File / Doc Movement
                'doc_orig_naturedoc': item.doc_orig_naturedoc,
                'doc_orig_issuedto': item.doc_orig_issuedto,
                'doc_orig_purpose': item.doc_orig_purpose,
                'doc_orig_nature': item.doc_orig_nature,
                'doc_orig_issue': item.doc_orig_issue,
                'doc_orig_comments': item.doc_orig_comments
            } for item in documents_movement_data]

    # Govt Official Documents  for team lead 2
            query = Team2GovtOfficialDocuments.query.filter(Team2GovtOfficialDocuments.team_id == team2.team_id)

            if not show_all_dates:

                query = query.filter(

                    Team2GovtOfficialDocuments.submitted_at >= start_of_day,

                    Team2GovtOfficialDocuments.submitted_at <= end_of_day

                )

            govt_official_documents_data = query.order_by(Team2GovtOfficialDocuments.submitted_at.desc()).all()
            team2_govt_official_documents_data = [{
                'date': item.submitted_at,
                'work_activity': item.work_activity,
                'department': item.department,
        'document_name': item.document_name,
                'expiry_date': item.expiry_date,
                'expected_renewal_date': item.expected_renewal_date,
                'nature_of_issue': item.nature_of_issue,
                'issue_description': item.issue_description,
                'comments': item.comments
            } for item in govt_official_documents_data]

     # Thoorigai Team Social Media

            query = Team2ThoorigaiTeamSocialMedia.query.filter(Team2ThoorigaiTeamSocialMedia.team_id == team2.team_id)


            if not show_all_dates:


                query = query.filter(


                    Team2ThoorigaiTeamSocialMedia.submitted_at >= start_of_day,


                    Team2ThoorigaiTeamSocialMedia.submitted_at <= end_of_day


                )


            thoorigai_social_media_data = query.order_by(Team2ThoorigaiTeamSocialMedia.submitted_at.desc()).all()
            team2_thoorigai_social_media_data = [{
                'date': item.submitted_at,
                'work_activity': item.work_activity,
                'department': item.department,
                'platform': item.platform,
                'video_status': item.video_status,
                'post_status': item.post_status,
                'update_status': item.update_status,
                'nature_of_issue': item.nature_of_issue,
                'issue_description': item.issue_description,
                'comments': item.comments
            } for item in thoorigai_social_media_data]

    # Thoorigai Website Updates  for team lead 2

            query = Team2WebsiteUpdates.query.filter(Team2WebsiteUpdates.team_id == team2.team_id)


            if not show_all_dates:


                query = query.filter(


                    Team2WebsiteUpdates.submitted_at >= start_of_day,


                    Team2WebsiteUpdates.submitted_at <= end_of_day


                )


            website_updates_data = query.order_by(Team2WebsiteUpdates.submitted_at.desc()).all()
            team2_website_updates_data = [{
                'date': item.submitted_at,
                'work_activity': item.work_activity,
                'department': item.department,
                'particulars': item.particulars,
                'inclusion': item.inclusion,
                'deletion': item.deletion,
                'others': item.others,
                'nature_of_issue': item.nature_of_issue,
                'issue_description': item.issue_description,
                'comments': item.comments
            } for item in website_updates_data]

    # MD Social Media  for team lead 2

            query = Team2MDSocialMedia.query.filter(Team2MDSocialMedia.team_id == team2.team_id)


            if not show_all_dates:


                query = query.filter(


                    Team2MDSocialMedia.submitted_at >= start_of_day,


                    Team2MDSocialMedia.submitted_at <= end_of_day


                )


            md_social_media_data = query.order_by(Team2MDSocialMedia.submitted_at.desc()).all()
            team2_md_social_media_data = [{
                'date': item.submitted_at,
                'work_activity': item.work_activity,
                'department': item.department,
                'platform': item.platform,
                'video': item.video,
                'post': item.post,
                'update': item.update,
                'nature_of_issue': item.nature_of_issue,
                'issue_description': item.issue_description,
                'comments': item.comments
            } for item in md_social_media_data]

    # 20: Intercom Maintenance  for team lead 2

            query = Team2IntercomMaintenance.query.filter(Team2IntercomMaintenance.team_id == team2.team_id)


            if not show_all_dates:


                query = query.filter(


                    Team2IntercomMaintenance.submitted_at >= start_of_day,


                    Team2IntercomMaintenance.submitted_at <= end_of_day


                )


            intercom_maintenance_data = query.order_by(Team2IntercomMaintenance.submitted_at.desc()).all()
            team2_intercom_maintenance_data = [{
                'date': item.submitted_at,
                'work_activity': item.work_activity,
                'department': item.department,
                'working': item.working,
                'not_working': item.not_working,
                'rectified': item.rectified,
                'nature_of_issue': item.nature_of_issue,
                'issue_description': item.issue_description,
                'comments': item.comments
            } for item in intercom_maintenance_data]

    # 21: Health Check Up  for team lead 2
            query = Team2HealthCheckUp.query.filter(Team2HealthCheckUp.team_id == team2.team_id)

            if not show_all_dates:

                query = query.filter(

                    Team2HealthCheckUp.submitted_at >= start_of_day,

                    Team2HealthCheckUp.submitted_at <= end_of_day

                )

            health_check_up_data = query.order_by(Team2HealthCheckUp.submitted_at.desc()).all()
            team2_health_check_up_data = [{
                'date': item.submitted_at,
                'work_activity': item.work_activity,
                'department': item.department,
                'department_staff': item.department_staff,
                'staff_name': item.staff_name,
                'illness': item.illness,
                'informed_by': item.informed_by,
                'action_taken': item.action_taken,
                'nature_of_issue': item.nature_of_issue,
                'issue_description': item.issue_description,
                'comments': item.comments
            } for item in health_check_up_data]

    # 22: Net Connectivity & Print Details  for team lead 2
            query = Team2NetConnectivityPrintDetails.query.filter(Team2NetConnectivityPrintDetails.team_id == team2.team_id)

            if not show_all_dates:

                query = query.filter(

                    Team2NetConnectivityPrintDetails.submitted_at >= start_of_day,

                    Team2NetConnectivityPrintDetails.submitted_at <= end_of_day

                )

            net_connectivity_print_details_data = query.order_by(Team2NetConnectivityPrintDetails.submitted_at.desc()).all()
            team2_net_connectivity_print_details_data = [{
                'date': item.submitted_at,
                'work_activity': item.work_activity,
                'department': item.department,
                'particulars': item.particulars,
                'net_speed': item.net_speed,
                'no_of_prints': item.no_of_prints,
                'complaints': item.complaints,
                'nature_of_issue': item.nature_of_issue,
                'issue_description': item.issue_description,
                'comments': item.comments
            } for item in net_connectivity_print_details_data]

    # 23: General Maintenance - IT Products  for team lead 2
            query = Team2GeneralMaintenanceITProducts.query.filter(Team2GeneralMaintenanceITProducts.team_id == team2.team_id)

            if not show_all_dates:

                query = query.filter(

                    Team2GeneralMaintenanceITProducts.submitted_at >= start_of_day,

                    Team2GeneralMaintenanceITProducts.submitted_at <= end_of_day

                )

            general_maintenance_it_data = query.order_by(Team2GeneralMaintenanceITProducts.submitted_at.desc()).all()
            team2_general_maintenance_it_data = [{
                'date': item.submitted_at,
                'work_activity': item.work_activity,
                'department': item.department,
                'particulars': item.particulars,
                'issues': item.issues,
                'complaintdate': item.complaintdate,
                'solveddate': item.solveddate,
                'nature_of_issue': item.nature_of_issue,
                'issue_description': item.issue_description,
                'comments': item.comments
            } for item in general_maintenance_it_data]

    # 24: Calendar Schedule  for team lead 2
            query = Team2CalendarSchedule.query.filter(Team2CalendarSchedule.team_id == team2.team_id)

            if not show_all_dates:

                query = query.filter(

                    Team2CalendarSchedule.submitted_at >= start_of_day,

                    Team2CalendarSchedule.submitted_at <= end_of_day

                )

            calendar_schedule_data = query.order_by(Team2CalendarSchedule.submitted_at.desc()).all()
            team2_calendar_schedule_data = [{
                'date': item.submitted_at,
                'work_activity': item.work_activity,
                'department': item.department,
                'session': item.session,
                'category': item.category,
                'in_charge': item.in_charge,
                'planned': item.planned,
                'unplanned': item.unplanned,
                'nature_of_issue': item.nature_of_issue,
                'issue_description': item.issue_description,
                'comments': item.comments
            } for item in calendar_schedule_data]

    # 25: Training Attendance  for team lead 2
            query = Team2TrainingAttendance.query.filter(Team2TrainingAttendance.team_id == team2.team_id)

            if not show_all_dates:

                query = query.filter(

                    Team2TrainingAttendance.submitted_at >= start_of_day,

                    Team2TrainingAttendance.submitted_at <= end_of_day

                )

            training_attendance_data = query.order_by(Team2TrainingAttendance.submitted_at.desc()).all()
            grouped_training = defaultdict(lambda: {
                'date': None,
                'academics_jr': None,
                'academics_sr': None,
                'admin_staff': None,
                'drivers': None,
                'security': None,
                'drivers_sub': None,
                'conductors': None,
            })
            for item in training_attendance_data:
                date_key = item.submitted_at.date()
                entry = grouped_training[date_key]
                entry['date'] = item.submitted_at
                dept_group = (item.department_group or '').strip().lower()
                dept = (item.dept or '').strip().lower()
                data = {
                    'topic': item.topic,
                    'total': item.total,
                    'present': item.present,
                    'leave': item.leave,
                    'leave_percentage': item.leave_percentage,
                    'nature': item.nature_of_issue,
                    'issue_desc': item.issue_description,
                    'comments': item.comments,
                }
                if dept_group == 'academics' and dept == 'academics - jr.school':
                    entry['academics_jr'] = data
                elif dept_group == 'academics' and dept == 'academics - sr.school':
                    entry['academics_sr'] = data
                elif dept_group == 'admin' and dept == 'admin - admin':
                    entry['admin_staff'] = data
                elif dept_group == 'admin' and dept == 'admin - drivers':
                    entry['drivers'] = data
                elif dept_group == 'admin' and dept == 'admin - securities':
                    entry['security'] = data
                elif dept_group == 'admin' and dept == 'admin - drivers (sub)':
                    entry['drivers_sub'] = data
                elif dept_group == 'admin' and dept == 'admin - conductors':
                    entry['conductors'] = data
            team2_training_attendance_data = list(grouped_training.values())


    # 26: Training Details  for team lead 2
            query = Team2TrainingDetails.query.filter(Team2TrainingDetails.team_id == team2.team_id)

            if not show_all_dates:

                query = query.filter(

                    Team2TrainingDetails.submitted_at >= start_of_day,

                    Team2TrainingDetails.submitted_at <= end_of_day

                )

            training_details_data = query.order_by(Team2TrainingDetails.submitted_at.desc()).all()
            team2_training_details_data = [{
                'date': item.submitted_at,
                'work_activity': item.work_activity,
                'department': item.department,
                'name': item.name,
                'dept': item.dept,
                'topic': item.topic,
                'no_of_days_hrs': item.no_of_days_hrs,
                'nature_of_issue': item.nature_of_issue,
                'issue_description': item.issue_description,
                'comments': item.comments
            } for item in training_details_data]

    # 27: Manpower Planning  for team lead 2
            query = Team2ManpowerPlanning.query.filter(Team2ManpowerPlanning.team_id == team2.team_id)

            if not show_all_dates:

                query = query.filter(

                    Team2ManpowerPlanning.submitted_at >= start_of_day,

                    Team2ManpowerPlanning.submitted_at <= end_of_day

                )

            manpower_planning_data = query.order_by(Team2ManpowerPlanning.submitted_at.desc()).all()
            team2_manpower_planning_data = [{   
                'date': item.submitted_at,
                'mp_department': item.mp_department,
                'mp_staff_name': item.mp_staff_name,
                'mp_designation': item.mp_designation,
                'mp_grades': item.mp_grades,
                'mp_relieve_date': item.mp_relieve_date,    
                'mp_budget': item.mp_budget,
                'mp_new_find': item.mp_new_find
            } for item in manpower_planning_data]

    # 28: Overall Consolidation  for team lead 2    
            query = Team2OverallConsolidation.query.filter(Team2OverallConsolidation.team_id == team2.team_id)
    
            if not show_all_dates:
    
                query = query.filter(
    
                    Team2OverallConsolidation.submitted_at >= start_of_day,
    
                    Team2OverallConsolidation.submitted_at <= end_of_day
    
                )
    
            overall_consolidation_data = query.order_by(Team2OverallConsolidation.submitted_at.desc()).all()
            team2_overall_consolidation_data = [{     
                'date': item.submitted_at,
                'oc_department': item.oc_department,
                'oc_total': item.oc_total,
                'oc_required': item.oc_required,
                'oc_shortlisted': item.oc_shortlisted,
                'oc_waiting_list': item.oc_waiting_list,    
                'oc_yet_to_find': item.oc_yet_to_find
            } for item in overall_consolidation_data]
            
    # 29: Uniform Details  for team lead 2
            query = Team2UniformDetails.query.filter(Team2UniformDetails.team_id == team2.team_id)

            if not show_all_dates:

                query = query.filter(

                    Team2UniformDetails.submitted_at >= start_of_day,

                    Team2UniformDetails.submitted_at <= end_of_day

                )

            uniform_details_data = query.order_by(Team2UniformDetails.submitted_at.desc()).all()
            team2_uniform_details_data = [{
                'date': item.submitted_at,
                'uniform': item.ud_uniform,
                'designation': item.ud_designation,
                'details': item.ud_details,
                'remarks': item.ud_remarks,
                'closure_date': item.ud_closure_date
            } for item in uniform_details_data]

    # 30: Department Wise Uniform Details  for team lead 2

            query = Team2DepartmentWiseUniformDetails.query.filter(Team2DepartmentWiseUniformDetails.team_id == team2.team_id)


            if not show_all_dates:


                query = query.filter(


                    Team2DepartmentWiseUniformDetails.submitted_at >= start_of_day,


                    Team2DepartmentWiseUniformDetails.submitted_at <= end_of_day


                )


            dept_wise_uniform_details_data = query.order_by(Team2DepartmentWiseUniformDetails.submitted_at.desc()).all()
            team2_dept_wise_uniform_details_data = [{
                'date': item.submitted_at,
                'department': item.dwud_department,
                'total': item.dwud_total,
                'completed': item.dwud_completed,
                'pending': item.dwud_pending,
                'names': item.dwud_names,
                'dress_code': item.dwud_dress_code,
                'status': item.dwud_status
            } for item in dept_wise_uniform_details_data]


    # Get Team 3 audit data if selected team is 'all' or 'team3'
    if selected_team in ['all', 'team3']:
        team3 = Team.query.filter_by(team_name='Team 3').first()
        if team3:
            query = Team3Audit.query.filter(Team3Audit.team_id == team3.team_id)

            if not show_all_dates:

                query = query.filter(

                    Team3Audit.submitted_at >= start_of_day,

                    Team3Audit.submitted_at <= end_of_day

                )

            audit_data = query.order_by(Team3Audit.submitted_at.desc()).all()
            team3_audit_data = [{
                'date': item.submitted_at,
                'frequency': item.frequency,
                'audit_components': item.audit_components,
                'audit_by': item.audit_by,
                'audit_time': item.audit_time,
                'issue_nature': item.issue_nature,
                'audit_remarks': item.audit_remarks,
            } for item in audit_data]

            query = Team3NewAudit.query.filter(Team3NewAudit.team_id == team3.team_id)
            if not show_all_dates:
                query = query.filter(
                    Team3NewAudit.submitted_at >= start_of_day,
                    Team3NewAudit.submitted_at <= end_of_day
                )
            new_audit_rows = query.order_by(Team3NewAudit.submitted_at.desc()).all()
            for row in new_audit_rows:
                team3_new_audit_data.append({
                    'date': row.submitted_at,
                    'frequency': row.frequency,
                    'component': row.component,
                    'audited_by': row.audited_by,
                    'staff_name': row.staff_name,
                    'grade': row.grade,
                    'section': row.section,
                    'specification': row.specification,
                    'issue_nature': row.issue_nature,
                    'remark': row.remark,
                    'media_url': (url_for('serve_file', file_id=row.media_file_id) if row.media_file_id else None),
                    'media_name': (row.media if hasattr(row, 'media') else None)
                })




    available_dates = []

    # List of all Team 1 models
    team1_models = [
        Team1CalendarSchedule,
        Team1ASAActivities,
        Team1ASASports,
        Team1ASAGeneral,
        Team1StudentAttendance,
        Team1StudentGrooming,
        Team1StudentLateComing,
        Team1AdmissionStatus,
        Team1TransferCertificate,
        Team1ParentActivity,
        Team1ParentVisit,
        Team1ExamSchedule,
        Team1ExternalInfo,
        Team1SickBay,
        Team1HomeSchoolComm,
        Team1Disciplinary,
        Team1Logistics,
        Team1CompetitionCert,
        Team1StaffConcern,
        Team1StudentConcern,
        Team1ParentConcern,
        Team1ParentConcernDetail,
        Team1AEPAttendance,
        Team1ExtendedClassAttendance,
        Team1TrainingSession,
        Team1WeeklyMeeting,
        Team1SpecialEducation,
        Team1Hostel,
        Team1SEC,
        Team1SchoolCounsellor,
        Team1Scholorius
    ]

    
    team2_models = [
        Team2HRAttendance,
        Team2TotalHRAttendance,
        Team2AdminAttendance,
        Team2RecruitmentActivity,
        Team2PendingRecruitment,
        Team2RecruitmentPipeline,
        Team2StaffStatusUpdates,
        Team2SalaryPending,
        Team2PoliceVerification,
        Team2InterviewSchedule,
        Team2ExitInformation,
        Team2IssuesStaffConcerns,
        Team2KuralRecitation,
        Team2FrontOfficePhoneCalls,
        Team2VisitorLog,
        Team2BSNLPhoneStatus,
        Team2MaterialsInward,
        Team2MaterialsOutward,
        Team2MaterialsMovement,
        Team2ReturnableMaterialTracking,
        Team2ReturnableGoodsReport,
        Team2WaterTDSDeviation,
        Team2TestingCleaning,
        Team2PoolTesting,
        Team2WashroomCleanliness,
        Team2TransportAttendance,
        Team2ACWorkingStatus,
        Team2LateReporting,
        Team2MaintenanceServiceIssues,
        Team2CarMaintenanceCleaning,
        Team2VehicleRenewalsDelays,
        Team2SpecialTrip,
        Team2ACTemperatureCheck,
        Team2LaborEbSolarGenset,
        Team2Motor,
        Team2PestControl,
        Team2ACTempDeviation,
        Team2ElectricityConsumption,
        Team2EBDetails,
        Team2SolarDetails,
        Team2GensetDetails,
        Team2CountVerification,
        Team2AttendanceReplacement,
        Team2SecurityInfoNote,
        Team2SecurityGovtInout,
        Team2AlcoholTest,
        Team2SecurityMaterialsInout,
        Team2SecurityMaterialsOutward,
        Team2TransportVerification,
        Team2DocumentsMovement,
        Team2GovtOfficialDocuments,
        Team2ThoorigaiTeamSocialMedia,
        Team2WebsiteUpdates,
        Team2MDSocialMedia,
        Team2IntercomMaintenance,
        Team2HealthCheckUp,
        Team2NetConnectivityPrintDetails,
        Team2GeneralMaintenanceITProducts,
        Team2CalendarSchedule,
        Team2TrainingAttendance,
        Team2TrainingDetails,
        Team2ManpowerPlanning,
        Team2OverallConsolidation,
        Team2BiometricsAccessCardPunching,
        Team2CampusCameraStatus,
        Team2VehicleCameraStatus,
        Team2BusACCameraStatus,
        Team2GPSMonitoring,
        Team2IssuesIdentifiedMonitoring,
        Team2IssuesIdentifiedControlRoom,
        Team2ParentConcernDetail,
        Team2WaterLevel,
        Team2HousekeepingGeneral,
        Team2UniformDetails,
        Team2DepartmentWiseUniformDetails
    ]


    # TEAM 3 MODELS
    team3_models = [
        Team3Audit,
        Team3NewAudit
    ]

    # Add unacknowledged count for banner - cached to eliminate 72 queries per request
    today = dt_date.today()
    unack_cache_key = f"unack_count:{current_user.user_id}:{today.isoformat()}"
    cached_unack = None
    try:
        cached_unack = cache.get(unack_cache_key)
    except Exception:
        pass

    if cached_unack is not None:
        unack_count = cached_unack
    else:
        start_date = today - timedelta(days=30)
        report_dates = set()
        
        def add_report_dates_from_model(model, team_id):
            try:
                rows = db.session.query(
                    func.date(model.submitted_at)
                ).filter(
                    model.team_id == team_id,
                    func.date(model.submitted_at) >= start_date,
                    func.date(model.submitted_at) <= today
                ).distinct().all()
                for row in rows:
                    report_dates.add(row[0])
            except Exception as e:
                print(f"Error processing model {model.__name__}: {e}")
        
        if current_user.role == 'MD':
            for model in team1_models:
                add_report_dates_from_model(model, 1)
            for model in team2_models:
                add_report_dates_from_model(model, 2)
            for model in team3_models:
                add_report_dates_from_model(model, 3)
        elif current_user.is_team_lead:
            if current_user.team_id == 1:
                for model in team1_models:
                    add_report_dates_from_model(model, 1)
            elif current_user.team_id == 2:
                for model in team2_models:
                    add_report_dates_from_model(model, 2)
            elif current_user.team_id == 3:
                for model in team3_models:
                    add_report_dates_from_model(model, 3)
        
        try:
            user_acks = {a.date: a for a in Acknowledgement.query.filter_by(user_id=current_user.user_id).all()}
            pending_dates = [d for d in sorted(report_dates) if not (user_acks.get(d) and user_acks.get(d).acknowledged_at)]
            unack_count = len(pending_dates)
            try:
                cache.set(unack_cache_key, unack_count, timeout=300)
            except Exception:
                pass
        except Exception as e:
            print(f"Error calculating unacknowledged count: {e}")
            unack_count = 0
    
    return render_template('md_dashboard.html',
                         teams=teams,
                         authorized_teams=authorized_teams,
                         users=users,
                         selected_team=selected_team,
                         selected_date=selected_date,
                         total_issues=total_issues,
                         resolved_issues=resolved_issues,
                         pending_issues=pending_issues,
                         open_issues=open_issues,
                         recent_issues=recent_issues,
                          team1_calendar_data=team1_calendar_data,
                         team1_asa_data=team1_asa_data,
                         team1_asa_sports_data=team1_asa_sports_data,
                         team1_asa_general_data=team1_asa_general_data,
                         team1_student_attendance_data=team1_student_attendance_data,
                         team1_student_grooming_data=team1_student_grooming_data,
                         team1_student_late_coming_data=team1_student_late_coming_data,
                         team1_admission_status_data=team1_admission_status_data,
                         team1_transfer_certificate_data = team1_transfer_certificate_data,
                         team1_parent_activity_data = team1_parent_activity_data,
                         team1_parent_visit_data = team1_parent_visit_data,
                         team1_exam_schedule_data = team1_exam_schedule_data,
                         team1_external_info_data = team1_external_info_data,
                         team1_sick_bay_data = team1_sick_bay_data,
                         team1_home_school_communication_data = team1_home_school_communication_data,
                         team1_disciplinary_measures_data = team1_disciplinary_measures_data,
                         team1_logistics_data = team1_logistics_data,
                         team1_competition_certificate_data = team1_competition_certificate_data,
                         team1_staff_concern_data = team1_staff_concern_data,
                         team1_student_concern_data = team1_student_concern_data,
                         team1_parent_concern_data = team1_parent_concern_data,
                         team1_parent_concern_detail_data = team1_parent_concern_detail_data,
                         team1_aep_attendance_data = team1_aep_attendance_data,
                         team1_extended_class_data = team1_extended_class_data,
                         team1_training_session_data = team1_training_session_data,
                         team1_weekly_meeting_data = team1_weekly_meeting_data,
                         team1_special_education_data = team1_special_education_data,
                         team1_hostel_data = team1_hostel_data,
                         team1_sec_data = team1_sec_data,
                         team1_scholorius_data = team1_scholorius_data,
                         team1_school_counsellor_data = team1_school_counsellor_data,
                         team2_hr_attendance_data=team2_hr_attendance_data,
                         team2_total_hr_attendance_data=team2_total_hr_attendance_data,
                         team2_admin_attendance_data=team2_admin_attendance_data,
                         team2_recruitment_activity_data=team2_recruitment_activity_data,
                         team2_pending_recruitment_data=team2_pending_recruitment_data,
                         team2_recruitment_pipeline_data=team2_recruitment_pipeline_data,
                         team2_staff_status_updates_data=team2_staff_status_updates_data,
                         team2_salary_pending_data=team2_salary_pending_data,
                         team2_police_verification_data=team2_police_verification_data,
                         team2_interview_schedule_data=team2_interview_schedule_data,
                         team2_exit_information_data=team2_exit_information_data,
                         team2_issues_staff_concerns_data=team2_issues_staff_concerns_data,
                         team2_kural_recitation_data=team2_kural_recitation_data,
                         team2_front_office_phone_calls_data=team2_front_office_phone_calls_data,
                         team2_visitor_log_data=team2_visitor_log_data,
                         team2_bsnl_phone_status_data=team2_bsnl_phone_status_data,
                         team2_materials_inward_data=team2_materials_inward_data,
                         team2_materials_outward_data=team2_materials_outward_data,
                         team2_materials_movement_data=team2_materials_movement_data,
                         team2_returnable_material_tracking_data=team2_returnable_material_tracking_data,
                         team2_returnable_goods_report_data=team2_returnable_goods_report_data,
                         team2_water_tds_deviation_data=team2_water_tds_deviation_data,
                         team2_testing_cleaning_data=team2_testing_cleaning_data,
                         team2_water_level_data=team2_water_level_data,
                         team2_housekeeping_general_data=team2_housekeeping_general_data,
                         team2_pool_testing_data=team2_pool_testing_data,
                         team2_washroom_cleanliness_data=team2_washroom_cleanliness_data,
                         team2_transport_attendance_data=team2_transport_attendance_data,
                         team2_ac_working_status_data=team2_ac_working_status_data,
                         team2_late_reporting_data=team2_late_reporting_data,
                         team2_maintenance_service_issues_data=team2_maintenance_service_issues_data,
                         team2_car_maintenance_cleaning_data=team2_car_maintenance_cleaning_data,
                         team2_vehicle_renewals_delays_data=team2_vehicle_renewals_delays_data,
                         team2_special_trip_data=team2_special_trip_data,
                         team2_parent_concern_detail_data=team2_parent_concern_detail_data,
                         team2_ac_temperature_data=team2_ac_temperature_data,
                         team2_maintenance_labor_data=team2_maintenance_labor_data,
                         team2_motor_data=team2_motor_data,
                         team2_pest_control_data=team2_pest_control_data,
                         team2_ac_temp_deviation_data=team2_ac_temp_deviation_data,
                         team2_electricity_consumption_data=team2_electricity_consumption_data,
                         team2_eb_details_data=team2_eb_details_data,
                         team2_solar_details_data=team2_solar_details_data,
                         team2_genset_details_data=team2_genset_details_data,
                         team2_count_verification_data=team2_count_verification_data,
                         team2_attendance_replacement_data=team2_attendance_replacement_data,
                         team2_security_info_note_data=team2_security_info_note_data,
                         team2_security_govt_inout_data=team2_security_govt_inout_data,
                         team2_alcohol_test_data=team2_alcohol_test_data,
                         team2_security_materials_inward_data=team2_security_materials_inward_data,
                         team2_security_materials_outward_data=team2_security_materials_outward_data,
                         team2_transport_verification_data=team2_transport_verification_data,
                         team2_documents_movement_data=team2_documents_movement_data,
                         team2_govt_official_documents_data=team2_govt_official_documents_data,
                         team2_thoorigai_social_media_data=team2_thoorigai_social_media_data,
                         team2_website_updates_data=team2_website_updates_data,
                         team2_md_social_media_data=team2_md_social_media_data,
                         team2_intercom_maintenance_data=team2_intercom_maintenance_data,
                         team2_health_check_up_data=team2_health_check_up_data,
                         team2_net_connectivity_print_details_data=team2_net_connectivity_print_details_data,
                         team2_general_maintenance_it_data=team2_general_maintenance_it_data,
                         team2_calendar_schedule_data=team2_calendar_schedule_data,
                         team2_training_attendance_data=team2_training_attendance_data,
                         team2_training_details_data=team2_training_details_data,
                         team2_manpower_planning_data=team2_manpower_planning_data,
                         team2_overall_consolidation_data=team2_overall_consolidation_data,
                         team2_uniform_details_data=team2_uniform_details_data,
                         team2_dept_wise_uniform_details_data=team2_dept_wise_uniform_details_data,
                         team2_biometrics_access_card_punching_data=team2_biometrics_access_card_punching_data,
                         team2_campus_camera_status_data=team2_campus_camera_status_data,
                         team2_vehicle_camera_status_data=team2_vehicle_camera_status_data,
                         team2_bus_ac_camera_status_data=team2_bus_ac_camera_status_data,
                         team2_gps_monitoring_data=team2_gps_monitoring_data,
                         team2_issues_identified_monitoring_data=team2_issues_identified_monitoring_data,
                         team2_teachers_late_reporting_data=team2_teachers_late_reporting_data,
                         team2_camera_footage_data=team2_camera_footage_data,
                         team3_new_audit_data=team3_new_audit_data,
                         unack_count=unack_count,
                         available_dates=available_dates)
