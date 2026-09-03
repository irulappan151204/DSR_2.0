# statistics_routes.py
from flask import Blueprint, render_template
from flask_login import login_required
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_file, session
from flask_login import UserMixin, login_user, login_required, logout_user, current_user

from datetime import datetime, timedelta
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
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from zoneinfo import ZoneInfo
from models import User, Team, Issue, Report, Team1CalendarSchedule, Team1StudentAttendance, Team1ParentConcernDetail, Team1ASAActivities, Team1ASASports, Team1ASAGeneral, Team1StudentGrooming, Team1StudentLateComing, Team1AdmissionStatus, Team1TransferCertificate, Team1ParentActivity, Team1ParentVisit, Team1ExamSchedule, Team1ExternalInfo, Team1SickBay, Team1HomeSchoolComm, Team1Disciplinary, Team1Logistics, Team1CompetitionCert, Team1StaffConcern, Team1StudentConcern, Team1ParentConcern, Team1AEPAttendance, Team1ExtendedClassAttendance, Team1TrainingSession, Team1WeeklyMeeting, Team1SpecialEducation, Team1SchoolCounsellor, Team1Scholorius, Team2HRAttendance, Team2AdminAttendance, Team2RecruitmentActivity, Team2PendingRecruitment, Team2RecruitmentPipeline, Team2StaffStatusUpdates, Team2SalaryPending, Team2PoliceVerification, Team2InterviewSchedule, Team2ExitInformation, Team2IssuesStaffConcerns, Team2KuralRecitation, Team2FrontOfficePhoneCalls, Team2VisitorLog, Team2BSNLPhoneStatus, Team2MaterialsInward, Team2MaterialsOutward, Team2MaterialsMovement, Team2ReturnableMaterialTracking, Team2ReturnableGoodsReport, Team2CampusCameraStatus, Team2VehicleCameraStatus, Team2BusACCameraStatus, Team2GPSMonitoring, Team2IssuesIdentifiedMonitoring, Team2IssuesIdentifiedControlRoom,  Team2BiometricsAccessCardPunching, Team2WaterTDSDeviation, Team2TestingCleaning, Team2PoolTesting, Team2WaterLevel, Team2WashroomCleanliness, Team2TransportAttendance, Team2ACWorkingStatus, Team2LateReporting, Team2MaintenanceServiceIssues, Team2CarMaintenanceCleaning,  Team2VehicleRenewalsDelays, Team2SpecialTrip, Team2ACTemperatureCheck, Team2LaborEbSolarGenset, Team2Motor, Team2PestControl, Team2ACTempDeviation, Team2ElectricityConsumption, Team2EBDetails, Team2SolarDetails, Team2GensetDetails, Team2CountVerification, Team2AttendanceReplacement, Team2SecurityInfoNote,  Team2SecurityGovtInout, Team2AlcoholTest, Team2SecurityMaterialsInout, Team2SecurityMaterialsOutward, Team2TransportVerification, Team2DocumentsMovement, Team2GovtOfficialDocuments, Team2ThoorigaiTeamSocialMedia, Team2WebsiteUpdates, Team2MDSocialMedia, Team2IntercomMaintenance, Team2HealthCheckUp, Team2NetConnectivityPrintDetails, Team2GeneralMaintenanceITProducts,  Team2CalendarSchedule, Team2TrainingAttendance, Team2TrainingDetails, Team3Audit, Team3NewAudit

from timezone_utils import ist_day_bounds
from cache_utils import per_user_cache_key
statistics_bp = Blueprint('statistics', __name__)

@statistics_bp.route('/statistics')
@cache.cached(timeout=300, key_prefix=per_user_cache_key)
@login_required
def view_statistics():
    # Role-based access: MD sees all teams; Team Leads see only their own team
    is_md = (current_user.role == 'MD')
    is_team_lead = getattr(current_user, 'is_team_lead', False)
    if not (is_md or is_team_lead):
        flash('Access denied. Only MD and Team Leads can view statistics.', 'danger')
        return redirect(url_for('dashboard'))
    
    # Get selected filters from query parameters
    has_date_param = 'date' in request.args
    has_start_param = 'start_date' in request.args
    has_end_param = 'end_date' in request.args

    selected_date = request.args.get('date', None)
    start_date_str = request.args.get('start_date', '')
    end_date_str = request.args.get('end_date', '')
    selected_nature = (request.args.get('nature', 'all') or 'all').strip().lower()
    selected_date_obj = None
    start_date = None
    end_date = None
    defaulted_to_yesterday = False
    # Default logic: if no query params provided at all → default yesterday
    if not has_date_param and not has_start_param and not has_end_param:
        yesterday = (datetime.now() - timedelta(days=1)).date()
        selected_date = yesterday.strftime('%Y-%m-%d')
        defaulted_to_yesterday = True
    else:
        # Respect explicit input; if empty date and no range, treat as 'all'
        if (selected_date is None or str(selected_date).strip() == '') and not (start_date_str and end_date_str):
            selected_date = 'all'
        # If using date range, clear selected_date to avoid conflicts
        elif start_date_str and end_date_str:
            selected_date = None
    if start_date_str and end_date_str:
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        except ValueError:
            start_date = None
            end_date = None
    if selected_date and selected_date != 'all':
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
        elif selected_date and selected_date != 'all' and selected_date_obj:
            s_utc, e_utc = ist_day_bounds(selected_date_obj)
            filters.append(model.submitted_at >= s_utc)
            filters.append(model.submitted_at <= e_utc)
        return filters

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
        'hr_overall': {'all_well': 0, 'manageable': 0, 'critical': 0},
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
        'water_level_checking': {'all_well': 0, 'manageable': 0, 'critical': 0},
        'washroom_cleanliness': {'all_well': 0, 'manageable': 0, 'critical': 0},
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

        # Compute HR Overall after HR/Admin attendance sections
        team2_issue_nature['hr_overall']['all_well'] = (
            team2_issue_nature['jr_school']['all_well'] + team2_issue_nature['sr_school']['all_well'] +
            team2_issue_nature['eca']['all_well'] + team2_issue_nature['admin_staff']['all_well'] +
            team2_issue_nature['drivers']['all_well'] + team2_issue_nature['security']['all_well'] +
            team2_issue_nature['housekeeping']['all_well'] + team2_issue_nature['conductors']['all_well']
        )
        team2_issue_nature['hr_overall']['manageable'] = (
            team2_issue_nature['jr_school']['manageable'] + team2_issue_nature['sr_school']['manageable'] +
            team2_issue_nature['eca']['manageable'] + team2_issue_nature['admin_staff']['manageable'] +
            team2_issue_nature['drivers']['manageable'] + team2_issue_nature['security']['manageable'] +
            team2_issue_nature['housekeeping']['manageable'] + team2_issue_nature['conductors']['manageable']
        )
        team2_issue_nature['hr_overall']['critical'] = (
            team2_issue_nature['jr_school']['critical'] + team2_issue_nature['sr_school']['critical'] +
            team2_issue_nature['eca']['critical'] + team2_issue_nature['admin_staff']['critical'] +
            team2_issue_nature['drivers']['critical'] + team2_issue_nature['security']['critical'] +
            team2_issue_nature['housekeeping']['critical'] + team2_issue_nature['conductors']['critical']
        )

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
    # Process Water Level Checking
    query_filters = [Team2WaterLevel.team_id == team2.team_id] + build_date_filter(Team2WaterLevel)
    water_level_data = Team2WaterLevel.query.filter(*query_filters).all()

    for item in water_level_data:
        if item.nature_of_issue:
            nature = item.nature_of_issue.lower()
            if ('all_well' in nature or 'all well' in nature):
                team2_issue_nature['water_level_checking']['all_well'] += 1
                team2_issue_nature['overall']['all_well'] += 1
            elif ('manageable' in nature):
                team2_issue_nature['water_level_checking']['manageable'] += 1
                team2_issue_nature['overall']['manageable'] += 1
            elif ('critical' in nature):
                team2_issue_nature['water_level_checking']['critical'] += 1
                team2_issue_nature['overall']['critical'] += 1

    # Process Washroom Cleanliness (derive from cleanliness field)
    query_filters = [Team2WashroomCleanliness.team_id == team2.team_id] + build_date_filter(Team2WashroomCleanliness)
    washroom_data = Team2WashroomCleanliness.query.filter(*query_filters).all()

    for item in washroom_data:
        value = (getattr(item, 'cleanliness', None) or '').lower()
        if value:
            if ('all_well' in value or 'all well' in value):
                team2_issue_nature['washroom_cleanliness']['all_well'] += 1
                team2_issue_nature['overall']['all_well'] += 1
            elif 'manageable' in value:
                team2_issue_nature['washroom_cleanliness']['manageable'] += 1
                team2_issue_nature['overall']['manageable'] += 1
            elif 'critical' in value:
                team2_issue_nature['washroom_cleanliness']['critical'] += 1
                team2_issue_nature['overall']['critical'] += 1

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
        # Team 3 legacy Audit data
        query_filters = [Team3Audit.team_id == team3.team_id] + build_date_filter(Team3Audit)
        for item in Team3Audit.query.filter(*query_filters).all():
            if item.issue_nature:
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

        # Team 3 new audit form data
        query_filters_new = [Team3NewAudit.team_id == team3.team_id] + build_date_filter(Team3NewAudit)
        for item in Team3NewAudit.query.filter(*query_filters_new).all():
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

    from sqlalchemy import func

    available_dates = set()

    # Helper function for any model and team
    def add_dates_from_model(model, team_id):
        rows = db.session.query(
            func.date(model.submitted_at)
        ).filter(
            model.team_id == team_id
        ).distinct().all()
        for row in rows:
            available_dates.add(row[0])

    # TEAM 1 MODELS
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
        Team1SchoolCounsellor
    ]

    # TEAM 2 MODELS
    team2_models = [
        Team2HRAttendance,
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
        Team2WaterLevel,
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
        Team2BiometricsAccessCardPunching,
        Team2CampusCameraStatus,
        Team2VehicleCameraStatus,
        Team2BusACCameraStatus,
        Team2GPSMonitoring,
        Team2IssuesIdentifiedMonitoring,
        Team2IssuesIdentifiedControlRoom
    ]

    # TEAM 3 MODELS
    team3_models = [
        Team3Audit,
        Team3NewAudit
    ]

    # Add available dates based on role
    if is_team_lead and not is_md:
        if current_user.team_id == 1:
            for model in team1_models:
                add_dates_from_model(model, 1)
        elif current_user.team_id == 2:
            for model in team2_models:
                add_dates_from_model(model, 2)
        elif current_user.team_id == 3:
            for model in team3_models:
                add_dates_from_model(model, 3)
    else:
        # MD: include all teams
        for model in team1_models:
            add_dates_from_model(model, 1)
        for model in team2_models:
            add_dates_from_model(model, 2)
        for model in team3_models:
            add_dates_from_model(model, 3)

    # Sort final result
    available_dates = sorted(available_dates, reverse=True)

    # Apply nature filter post-processing to zero-out non-selected natures
    def apply_nature_filter(stats_dict):
        if selected_nature == 'all':
            return stats_dict
        allowed = {'all_well', 'manageable', 'critical'}
        for section_key, counts in stats_dict.items():
            if isinstance(counts, dict):
                for label in list(allowed):
                    if label != selected_nature and label in counts:
                        counts[label] = 0
        return stats_dict

    # Build KPI totals BEFORE applying nature filter so the KPI can show all three counts
    kpi_totals = {
        'team1': {
            'all_well': team1_issue_nature['overall']['all_well'],
            'manageable': team1_issue_nature['overall']['manageable'],
            'critical': team1_issue_nature['overall']['critical'],
        },
        'team2': {
            'all_well': team2_issue_nature['overall']['all_well'],
            'manageable': team2_issue_nature['overall']['manageable'],
            'critical': team2_issue_nature['overall']['critical'],
        },
        'team3': {
            'all_well': team3_issue_nature['overall']['all_well'],
            'manageable': team3_issue_nature['overall']['manageable'],
            'critical': team3_issue_nature['overall']['critical'],
        }
    }
    kpi_totals['combined'] = {
        'all_well': kpi_totals['team1']['all_well'] + kpi_totals['team2']['all_well'] + kpi_totals['team3']['all_well'],
        'manageable': kpi_totals['team1']['manageable'] + kpi_totals['team2']['manageable'] + kpi_totals['team3']['manageable'],
        'critical': kpi_totals['team1']['critical'] + kpi_totals['team2']['critical'] + kpi_totals['team3']['critical'],
    }

    # Apply nature filter to datasets used for charts/tables
    team1_issue_nature = apply_nature_filter(team1_issue_nature)
    team2_issue_nature = apply_nature_filter(team2_issue_nature)
    team3_issue_nature = apply_nature_filter(team3_issue_nature)

    # If Team Lead, hide other teams by zeroing out their stats
    def zero_out(stats_dict):
        for section_key, counts in stats_dict.items():
            if isinstance(counts, dict):
                for k in counts.keys():
                    if isinstance(counts[k], (int, float)):
                        counts[k] = 0
        return stats_dict

    if is_team_lead and not is_md:
        if current_user.team_id == 1:
            team2_issue_nature = zero_out(team2_issue_nature)
            team3_issue_nature = zero_out(team3_issue_nature)
        elif current_user.team_id == 2:
            team1_issue_nature = zero_out(team1_issue_nature)
            team3_issue_nature = zero_out(team3_issue_nature)
        elif current_user.team_id == 3:
            team1_issue_nature = zero_out(team1_issue_nature)
            team2_issue_nature = zero_out(team2_issue_nature)

    return render_template(
    'statistics.html',
    team1_issue_nature=team1_issue_nature,
    team2_issue_nature=team2_issue_nature,
    team3_issue_nature=team3_issue_nature,
    selected_date=selected_date,
    selected_nature=selected_nature,
    start_date=start_date_str,
    end_date=end_date_str,
    available_dates=available_dates,
    defaulted_to_yesterday=defaulted_to_yesterday,
    is_md=is_md,
    is_team_lead=is_team_lead,
    kpi_totals=kpi_totals
)


# view statistics complete data