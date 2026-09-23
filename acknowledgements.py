import logging
from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from flask_login import login_required, current_user
from datetime import datetime, timedelta, date as dt_date
from extensions import db, cache
from cache_utils import bust_user_dashboard_cache
from models import Acknowledgement, User, Team1CalendarSchedule, Team1ASAActivities, Team1ASASports, Team1ASAGeneral, Team1StudentAttendance, Team1StudentGrooming, Team1StudentLateComing, Team1AdmissionStatus, Team1TransferCertificate, Team1ParentActivity, Team1ParentVisit, Team1ExamSchedule, Team1ExternalInfo, Team1SickBay, Team1HomeSchoolComm, Team1Disciplinary, Team1Logistics, Team1CompetitionCert, Team1StaffConcern, Team1StudentConcern, Team1ParentConcern, Team1ParentConcernDetail, Team1AEPAttendance, Team1ExtendedClassAttendance, Team1TrainingSession, Team1WeeklyMeeting, Team1SpecialEducation, Team1Hostel, Team1SEC, Team1SchoolCounsellor, Team1Scholorius, Team2HRAttendance, Team2TotalHRAttendance, Team2AdminAttendance, Team2RecruitmentActivity, Team2PendingRecruitment, Team2RecruitmentPipeline, Team2StaffStatusUpdates, Team2SalaryPending, Team2PoliceVerification, Team2InterviewSchedule, Team2ExitInformation, Team2IssuesStaffConcerns, Team2KuralRecitation, Team2FrontOfficePhoneCalls, Team2VisitorLog, Team2BSNLPhoneStatus, Team2MaterialsInward, Team2MaterialsOutward, Team2MaterialsMovement, Team2ReturnableMaterialTracking, Team2ReturnableGoodsReport, Team2CampusCameraStatus, Team2VehicleCameraStatus, Team2BusACCameraStatus, Team2GPSMonitoring, Team2IssuesIdentifiedMonitoring, Team2IssuesIdentifiedControlRoom, Team2CameraFootageEntry, Team2BiometricsAccessCardPunching, Team2WaterTDSDeviation, Team2TestingCleaning, Team2PoolTesting, Team2WashroomCleanliness, Team2TransportAttendance, Team2ACWorkingStatus, Team2LateReporting, Team2MaintenanceServiceIssues, Team2CarMaintenanceCleaning, Team2VehicleRenewalsDelays, Team2SpecialTrip, Team2ParentConcernDetail, Team2ACTemperatureCheck, Team2LaborEbSolarGenset, Team2Motor, Team2PestControl, Team2ACTempDeviation, Team2ElectricityConsumption, Team2EBDetails, Team2SolarDetails, Team2GensetDetails, Team2CountVerification, Team2AttendanceReplacement, Team2SecurityInfoNote, Team2SecurityGovtInout, Team2AlcoholTest, Team2SecurityMaterialsInout, Team2SecurityMaterialsOutward, Team2TransportVerification, Team2DocumentsMovement, Team2GovtOfficialDocuments, Team2ThoorigaiTeamSocialMedia, Team2WebsiteUpdates, Team2MDSocialMedia, Team2IntercomMaintenance, Team2HealthCheckUp, Team2NetConnectivityPrintDetails, Team2GeneralMaintenanceITProducts, Team2CalendarSchedule, Team2TrainingAttendance, Team2TrainingDetails, Team2ManpowerPlanning, Team2OverallConsolidation, Team2WaterLevel, Team2HousekeepingGeneral, Team2UniformDetails, Team2DepartmentWiseUniformDetails, Team3Audit, Team3NewAudit
from sqlalchemy import func

logger = logging.getLogger(__name__)

acknowledgements_bp = Blueprint('acknowledgements', __name__)

# Helper: Only MD and Team Leads

def is_acknowledger(user):
    return user.role == 'MD' or user.is_team_lead


def get_unack_count_for_user(user):
    """Return number of reports awaiting acknowledgment for MD or Team Lead (cached)."""
    if not user or not getattr(user, 'is_authenticated', False) or not is_acknowledger(user):
        return 0
    today = dt_date.today()
    unack_cache_key = f"unack_count:{user.user_id}:{today.isoformat()}"
    try:
        cached_unack = cache.get(unack_cache_key)
        if cached_unack is not None:
            return cached_unack
    except Exception:
        pass

    start_date = today - timedelta(days=30)
    report_dates = get_report_dates_for_user(user, start_date, today)
    try:
        user_acks = {a.date: a for a in Acknowledgement.query.filter_by(user_id=user.user_id).all()}
        pending_dates = [d for d in report_dates if not (user_acks.get(d) and user_acks.get(d).acknowledged_at)]
        count = len(pending_dates)
        try:
            cache.set(unack_cache_key, count, timeout=300)
        except Exception:
            pass
        return count
    except Exception as e:
        logger.error(f"Error calculating unack count: {e}")
        return 0


def get_report_dates_for_user(user, start_date, end_date):
    """Get dates that have actual reports submitted for a user based on their role"""
    report_dates = set()
    
    # Helper function to get dates with reports for any model and team
    def add_report_dates_from_model(model, team_id):
        rows = db.session.query(
            func.date(model.submitted_at)
        ).filter(
            model.team_id == team_id,
            func.date(model.submitted_at) >= start_date,
            func.date(model.submitted_at) <= end_date
        ).distinct().all()
        for row in rows:
            report_dates.add(row[0])
    
    # Define all models by team
    team1_models = [
        Team1CalendarSchedule, Team1ASAActivities, Team1ASASports, Team1ASAGeneral,
        Team1StudentAttendance, Team1StudentGrooming, Team1StudentLateComing,
        Team1AdmissionStatus, Team1TransferCertificate, Team1ParentActivity,
        Team1ParentVisit, Team1ExamSchedule, Team1ExternalInfo, Team1SickBay,
        Team1HomeSchoolComm, Team1Disciplinary, Team1Logistics, Team1CompetitionCert,
        Team1StaffConcern, Team1StudentConcern, Team1ParentConcern, Team1ParentConcernDetail,
        Team1AEPAttendance, Team1ExtendedClassAttendance, Team1TrainingSession,
        Team1WeeklyMeeting, Team1SpecialEducation, Team1Hostel, Team1SEC,
        Team1SchoolCounsellor, Team1Scholorius
    ]
    
    team2_models = [
        Team2HRAttendance, Team2TotalHRAttendance, Team2AdminAttendance,
        Team2RecruitmentActivity, Team2PendingRecruitment, Team2RecruitmentPipeline,
        Team2StaffStatusUpdates, Team2SalaryPending, Team2PoliceVerification,
        Team2InterviewSchedule, Team2ExitInformation, Team2IssuesStaffConcerns,
        Team2KuralRecitation, Team2FrontOfficePhoneCalls, Team2VisitorLog,
        Team2BSNLPhoneStatus, Team2MaterialsInward, Team2MaterialsOutward,
        Team2MaterialsMovement, Team2ReturnableMaterialTracking, Team2ReturnableGoodsReport,
        Team2CampusCameraStatus, Team2VehicleCameraStatus, Team2BusACCameraStatus,
        Team2GPSMonitoring, Team2IssuesIdentifiedMonitoring, Team2IssuesIdentifiedControlRoom,
        Team2CameraFootageEntry, Team2BiometricsAccessCardPunching, Team2WaterTDSDeviation,
        Team2TestingCleaning, Team2PoolTesting, Team2WashroomCleanliness,
        Team2TransportAttendance, Team2ACWorkingStatus, Team2LateReporting,
        Team2MaintenanceServiceIssues, Team2CarMaintenanceCleaning, Team2VehicleRenewalsDelays,
        Team2SpecialTrip, Team2ParentConcernDetail, Team2ACTemperatureCheck,
        Team2LaborEbSolarGenset, Team2Motor, Team2PestControl, Team2ACTempDeviation,
        Team2ElectricityConsumption, Team2EBDetails, Team2SolarDetails, Team2GensetDetails,
        Team2CountVerification, Team2AttendanceReplacement, Team2SecurityInfoNote,
        Team2SecurityGovtInout, Team2AlcoholTest, Team2SecurityMaterialsInout,
        Team2SecurityMaterialsOutward, Team2TransportVerification, Team2DocumentsMovement,
        Team2GovtOfficialDocuments, Team2ThoorigaiTeamSocialMedia, Team2WebsiteUpdates,
        Team2MDSocialMedia, Team2IntercomMaintenance, Team2HealthCheckUp,
        Team2NetConnectivityPrintDetails, Team2GeneralMaintenanceITProducts,
        Team2CalendarSchedule, Team2TrainingAttendance, Team2TrainingDetails,
        Team2ManpowerPlanning, Team2OverallConsolidation, Team2WaterLevel,
        Team2HousekeepingGeneral, Team2UniformDetails, Team2DepartmentWiseUniformDetails
    ]
    
    team3_models = [Team3Audit, Team3NewAudit]
    
    # Add dates from models based on user role
    if user.role == 'MD':
        # MD should acknowledge reports from all teams
        for model in team1_models:
            add_report_dates_from_model(model, 1)
        for model in team2_models:
            add_report_dates_from_model(model, 2)
        for model in team3_models:
            add_report_dates_from_model(model, 3)
    elif user.is_team_lead:
        # Team leads only acknowledge their own team's reports
        if user.team_id == 1:
            for model in team1_models:
                add_report_dates_from_model(model, 1)
        elif user.team_id == 2:
            for model in team2_models:
                add_report_dates_from_model(model, 2)
        elif user.team_id == 3:
            for model in team3_models:
                add_report_dates_from_model(model, 3)
    
    return report_dates

@acknowledgements_bp.route('/ack', methods=['GET'])
@login_required
def view_acknowledgements():
    today = dt_date.today()
    start_date = today - timedelta(days=30)
    
    # Get dates that have actual reports submitted
    report_dates = get_report_dates_for_user(current_user, start_date, today)

    def get_pending_for_user(user):
        user_acks = {a.date: a for a in Acknowledgement.query.filter_by(user_id=user.user_id).all()}
        pending_dates = []
        for d in report_dates:
            ack = user_acks.get(d)
            if not (ack and ack.acknowledged_at):
                pending_dates.append(d)
        return pending_dates

    if current_user.role == 'MD':
        # Show all Team Leads and MD
        users = [current_user] + list(User.query.filter_by(role='Team Lead').all())
    elif current_user.is_team_lead:
        users = [current_user]
    else:
        return redirect(url_for('dashboard'))

    ack_summary = []
    team_summary = None
    
    if current_user.role == 'MD':
        # Calculate team summary statistics for MD
        team_summary = {}
        team_display_names = {
            'Team 1': 'Academic',
            'Team 2': 'Admin', 
            'Team 3': 'Audit'
        }
        
        # Get all team leads
        team_leads = User.query.filter_by(role='Team Lead').all()
        
        for team_lead in team_leads:
            team_name = team_lead.team.team_name if team_lead.team else 'N/A'
            display_name = team_display_names.get(team_name, team_name)
            
            if display_name not in team_summary:
                team_summary[display_name] = {'acknowledged': 0, 'unacknowledged': 0}
            
            # Get all acknowledgements for this team lead
            user_acks = {a.date: a for a in Acknowledgement.query.filter_by(user_id=team_lead.user_id).all()}
            
            for date in report_dates:
                ack = user_acks.get(date)
                if ack and ack.acknowledged_at:
                    team_summary[display_name]['acknowledged'] += 1
                else:
                    team_summary[display_name]['unacknowledged'] += 1
    
    for user in users:
        pending_dates = get_pending_for_user(user)
        
        # Use display name for team if user is MD
        team_name = user.team.team_name if user.team else 'N/A'
        if current_user.role == 'MD':
            display_team_name = team_display_names.get(team_name, team_name)
        else:
            display_team_name = team_name
            
        ack_summary.append({
            'user_id': user.user_id,
            'username': user.username,
            'role': user.role,
            'team': display_team_name,
            'pending_count': len(pending_dates),
            'pending_dates': [d.strftime('%b %d, %Y') for d in pending_dates],
            'pending_date_strs': [d.strftime('%Y-%m-%d') for d in pending_dates],
            'is_self': user.user_id == current_user.user_id
        })
    return render_template('acknowledgements/ack_list.html', ack_summary=ack_summary, is_md=(current_user.role=='MD'), team_summary=team_summary)

@acknowledgements_bp.route('/ack/team-leads', methods=['GET'])
@login_required
def view_team_leads_acknowledgements():
    # RBAC: Only MD and Team Leads are allowed
    if current_user.role != 'MD' and not current_user.is_team_lead:
        return redirect(url_for('profile'))
    
    # Get data for the last 30 days
    today = dt_date.today()
    start_date = today - timedelta(days=30)
    
    # MD sees all team leads; Team Lead sees strictly only themselves
    if current_user.role == 'MD':
        team_leads = User.query.filter_by(role='Team Lead').all()
    else:
        team_leads = [current_user]
    
    # Get all dates that have actual reports submitted
    all_report_dates = set()
    
    # Helper function to get dates with reports for any model and team
    def add_report_dates_from_model(model, team_id):
        rows = db.session.query(
            func.date(model.submitted_at)
        ).filter(
            model.team_id == team_id,
            func.date(model.submitted_at) >= start_date,
            func.date(model.submitted_at) <= today
        ).distinct().all()
        for row in rows:
            all_report_dates.add(row[0])
    
    # Define all models by team
    team1_models = [
        Team1CalendarSchedule, Team1ASAActivities, Team1ASASports, Team1ASAGeneral,
        Team1StudentAttendance, Team1StudentGrooming, Team1StudentLateComing,
        Team1AdmissionStatus, Team1TransferCertificate, Team1ParentActivity,
        Team1ParentVisit, Team1ExamSchedule, Team1ExternalInfo, Team1SickBay,
        Team1HomeSchoolComm, Team1Disciplinary, Team1Logistics, Team1CompetitionCert,
        Team1StaffConcern, Team1StudentConcern, Team1ParentConcern, Team1ParentConcernDetail,
        Team1AEPAttendance, Team1ExtendedClassAttendance, Team1TrainingSession,
        Team1WeeklyMeeting, Team1SpecialEducation, Team1Hostel, Team1SEC,
        Team1SchoolCounsellor, Team1Scholorius
    ]
    
    team2_models = [
        Team2HRAttendance, Team2TotalHRAttendance, Team2AdminAttendance,
        Team2RecruitmentActivity, Team2PendingRecruitment, Team2RecruitmentPipeline,
        Team2StaffStatusUpdates, Team2SalaryPending, Team2PoliceVerification,
        Team2InterviewSchedule, Team2ExitInformation, Team2IssuesStaffConcerns,
        Team2KuralRecitation, Team2FrontOfficePhoneCalls, Team2VisitorLog,
        Team2BSNLPhoneStatus, Team2MaterialsInward, Team2MaterialsOutward,
        Team2MaterialsMovement, Team2ReturnableMaterialTracking, Team2ReturnableGoodsReport,
        Team2CampusCameraStatus, Team2VehicleCameraStatus, Team2BusACCameraStatus,
        Team2GPSMonitoring, Team2IssuesIdentifiedMonitoring, Team2IssuesIdentifiedControlRoom,
        Team2CameraFootageEntry, Team2BiometricsAccessCardPunching, Team2WaterTDSDeviation,
        Team2TestingCleaning, Team2PoolTesting, Team2WashroomCleanliness,
        Team2TransportAttendance, Team2ACWorkingStatus, Team2LateReporting,
        Team2MaintenanceServiceIssues, Team2CarMaintenanceCleaning, Team2VehicleRenewalsDelays,
        Team2SpecialTrip, Team2ParentConcernDetail, Team2ACTemperatureCheck,
        Team2LaborEbSolarGenset, Team2Motor, Team2PestControl, Team2ACTempDeviation,
        Team2ElectricityConsumption, Team2EBDetails, Team2SolarDetails, Team2GensetDetails,
        Team2CountVerification, Team2AttendanceReplacement, Team2SecurityInfoNote,
        Team2SecurityGovtInout, Team2AlcoholTest, Team2SecurityMaterialsInout,
        Team2SecurityMaterialsOutward, Team2TransportVerification, Team2DocumentsMovement,
        Team2GovtOfficialDocuments, Team2ThoorigaiTeamSocialMedia, Team2WebsiteUpdates,
        Team2MDSocialMedia, Team2IntercomMaintenance, Team2HealthCheckUp,
        Team2NetConnectivityPrintDetails, Team2GeneralMaintenanceITProducts,
        Team2CalendarSchedule, Team2TrainingAttendance, Team2TrainingDetails,
        Team2ManpowerPlanning, Team2OverallConsolidation, Team2WaterLevel,
        Team2HousekeepingGeneral, Team2UniformDetails, Team2DepartmentWiseUniformDetails
    ]
    
    team3_models = [Team3Audit, Team3NewAudit]
    
    # Add dates from models based on user role (MD = all teams, Team Lead = their team only)
    if current_user.role == 'MD':
        for model in team1_models:
            add_report_dates_from_model(model, 1)
        for model in team2_models:
            add_report_dates_from_model(model, 2)
        for model in team3_models:
            add_report_dates_from_model(model, 3)
    else:
        lead_team_id = current_user.team_id
        if lead_team_id == 1:
            for model in team1_models:
                add_report_dates_from_model(model, 1)
        elif lead_team_id == 2:
            for model in team2_models:
                add_report_dates_from_model(model, 2)
        elif lead_team_id == 3:
            for model in team3_models:
                add_report_dates_from_model(model, 3)
    
    # Calculate team summary statistics
    team_summary = {}
    team_display_names = {
        'Team 1': 'Academic',
        'Team 2': 'Admin', 
        'Team 3': 'Audit'
    }
    
    for team_lead in team_leads:
        team_name = team_lead.team.team_name if team_lead.team else 'N/A'
        display_name = team_display_names.get(team_name, team_name)
        
        if display_name not in team_summary:
            team_summary[display_name] = {'acknowledged': 0, 'unacknowledged': 0}
        
        # Get all acknowledgements for this team lead
        user_acks = {a.date: a for a in Acknowledgement.query.filter_by(user_id=team_lead.user_id).all()}
        
        for date in all_report_dates:
            ack = user_acks.get(date)
            if ack and ack.acknowledged_at:
                team_summary[display_name]['acknowledged'] += 1
            else:
                team_summary[display_name]['unacknowledged'] += 1
    
    rows = []
    for user in team_leads:
        # Get all acknowledgements for this user
        user_acks = {a.date: a for a in Acknowledgement.query.filter_by(user_id=user.user_id).all()}
        
        for date in all_report_dates:
            ack = user_acks.get(date)
            status = "Acknowledged" if ack and ack.acknowledged_at else "Pending"
            ack_time = ack.acknowledged_at if ack and ack.acknowledged_at else None
            
            # Use display name for team
            team_name = user.team.team_name if user.team else 'N/A'
            display_team_name = team_display_names.get(team_name, team_name)
            
            rows.append({
                'username': user.username,
                'team': display_team_name,
                'date': date,
                'date_str': date.strftime('%Y-%m-%d'),
                'display_date': date.strftime('%b %d, %Y'),
                'status': status,
                'ack_time': ack_time,
                'ack_time_str': ack_time.strftime('%b %d, %Y %I:%M %p') if ack_time else '-'
            })
    
    # Sort by team (using original team names for sorting), then by date (newest first), then by username
    def get_sort_key(row):
        # Get original team name for sorting
        team_name = row['team']
        # Reverse map display name to original name for sorting
        original_team_name = None
        for orig, display in team_display_names.items():
            if display == team_name:
                original_team_name = orig
                break
        return (original_team_name or team_name, -int(row['date'].strftime('%Y%m%d')), row['username'])
    
    rows.sort(key=get_sort_key)
    
    return render_template('acknowledgements/team_leads_ack_list.html', rows=rows, team_summary=team_summary, is_md=(current_user.role == 'MD'))

@acknowledgements_bp.route('/ack', methods=['POST'])
@login_required
def acknowledge_report():
    if not is_acknowledger(current_user):
        return jsonify({'error': 'Unauthorized'}), 403
    
    try:
        data = request.get_json()
        if not data:
            # Try to get form data if JSON fails
            date_str = request.form.get('date')
            if not date_str:
                return jsonify({'error': 'No date provided'}), 400
        else:
            date_str = data.get('date')
            
        try:
            ack_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except Exception:
            return jsonify({'error': 'Invalid date format'}), 400
            
        ack = Acknowledgement.query.filter_by(user_id=current_user.user_id, date=ack_date).first()
        if not ack:
            ack = Acknowledgement(user_id=current_user.user_id, date=ack_date)
            db.session.add(ack)
        ack.acknowledged_at = datetime.now()
        db.session.commit()
        
        # Invalidate unacknowledged count cache and dashboard view caches
        try:
            today = dt_date.today()
            cache.delete(f"unack_count:{current_user.user_id}:{today.isoformat()}")
            bust_user_dashboard_cache(current_user.user_id)
        except Exception:
            pass

    except Exception:
        logger.exception("Failed to acknowledge date")
        return jsonify({'error': 'Failed to acknowledge date'}), 500

@acknowledgements_bp.route('/ack/md', methods=['GET'])
@login_required
def view_md_acknowledgements():
    if current_user.role != 'MD':
        return redirect(url_for('dashboard'))
    today = dt_date.today()
    start_date = today - timedelta(days=30)
    
    # Get dates that have actual reports submitted for MD
    report_dates = get_report_dates_for_user(current_user, start_date, today)
    
    user_acks = {a.date: a for a in Acknowledgement.query.filter_by(user_id=current_user.user_id).all()}
    rows = []
    for d in sorted(report_dates):  # Sort dates in ascending order
        ack = user_acks.get(d)
        status = 'Acknowledged' if ack and ack.acknowledged_at else 'Pending'
        ack_time = ack.acknowledged_at if ack and ack.acknowledged_at else None
        rows.append({
            'date': d,
            'date_str': d.strftime('%Y-%m-%d'),
            'display_date': d.strftime('%b %d, %Y'),
            'status': status,
            'ack_time': ack_time,
            'ack_time_str': ack_time.strftime('%b %d, %Y %I:%M %p') if ack_time else '-',
        })
    return render_template('acknowledgements/md_ack_list.html', rows=rows) 