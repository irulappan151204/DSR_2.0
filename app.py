# pyrefly: ignore [missing-import]
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_file, session, send_from_directory
from werkzeug.utils import secure_filename
import io
from flask_login import UserMixin, login_user, login_required, logout_user, current_user

from datetime import datetime, timedelta, timezone
import os
from dotenv import load_dotenv
import platform
from extensions import db, login_manager, bcrypt, socketio, cache
from cache_utils import per_user_cache_key
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
from report_routes import report_bp
## Removed team-specific statistics blueprints in favor of unified statistics
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from zoneinfo import ZoneInfo
from models import User, Team, Issue, Report, Team1CalendarSchedule, Team1StudentAttendance, Team1ParentConcernDetail, Team1ASAActivities, Team1ASASports, Team1ASAGeneral, Team1StudentGrooming, Team1StudentLateComing, Team1AdmissionStatus, Team1TransferCertificate, Team1ParentActivity, Team1ParentVisit, Team1ExamSchedule, Team1ExternalInfo, Team1SickBay, Team1HomeSchoolComm, Team1Disciplinary, Team1Logistics, Team1CompetitionCert, Team1StaffConcern, Team1ParentConcern,Team1StudentConcern, Team1AEPAttendance, Team1ExtendedClassAttendance, Team1TrainingSession, Team1WeeklyMeeting, Team1SpecialEducation, Team1Hostel, Team1SEC, Team1SchoolCounsellor,Team1Scholorius, Team2HRAttendance, Team2AdminAttendance, Team2RecruitmentActivity, Team2PendingRecruitment, Team2RecruitmentPipeline, Team2StaffStatusUpdates, Team2SalaryPending, Team2PoliceVerification, Team2InterviewSchedule, Team2ExitInformation, Team2IssuesStaffConcerns, Team2KuralRecitation, Team2FrontOfficePhoneCalls, Team2VisitorLog, Team2BSNLPhoneStatus, Team2MaterialsInward, Team2MaterialsOutward, Team2MaterialsMovement, Team2ReturnableMaterialTracking, Team2ReturnableGoodsReport, Team2CampusCameraStatus, Team2VehicleCameraStatus, Team2BusACCameraStatus, Team2GPSMonitoring, Team2IssuesIdentifiedMonitoring, Team2IssuesIdentifiedControlRoom, Team2CameraFootageEntry,  Team2BiometricsAccessCardPunching, Team2WaterTDSDeviation, Team2TestingCleaning, Team2WaterLevel, Team2HousekeepingGeneral, Team2PoolTesting, Team2WashroomCleanliness, Team2TransportAttendance, Team2ACWorkingStatus, Team2LateReporting, Team2MaintenanceServiceIssues, Team2CarMaintenanceCleaning,  Team2VehicleRenewalsDelays, Team2SpecialTrip, Team2ACTemperatureCheck, Team2LaborEbSolarGenset, Team2Motor, Team2PestControl, Team2ACTempDeviation, Team2ElectricityConsumption, Team2EBDetails, Team2SolarDetails, Team2GensetDetails, Team2CountVerification, Team2AttendanceReplacement, Team2SecurityInfoNote,  Team2SecurityGovtInout, Team2AlcoholTest, Team2SecurityMaterialsInout, Team2SecurityMaterialsOutward, Team2TransportVerification, Team2DocumentsMovement, Team2GovtOfficialDocuments, Team2ThoorigaiTeamSocialMedia, Team2WebsiteUpdates, Team2MDSocialMedia, Team2IntercomMaintenance, Team2HealthCheckUp, Team2NetConnectivityPrintDetails, Team2GeneralMaintenanceITProducts,  Team2CalendarSchedule, Team2TrainingAttendance, Team2TrainingDetails, Team2ManpowerPlanning,Team2OverallConsolidation,   Team2UniformDetails,Team2DepartmentWiseUniformDetails, Team3Audit, FileStorage, Team3NewAudit
from actions import actions_bp
from acknowledgements import acknowledgements_bp
from critical import (critical_bp, can_audit,
                      pending_critical_count as critical_pending_count)
from timezone_utils import now_ist
import models as models_module


# Load environment variables
load_dotenv()

# Set Flask app environment variable
os.environ['FLASK_APP'] = 'app.py'

app = Flask(__name__)
from config import Config
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'login'
bcrypt.init_app(app)
socketio.init_app(app)
# Configure cache
cache_config = {
    'CACHE_TYPE': 'simple',  # Use simple memory cache for development
    'CACHE_DEFAULT_TIMEOUT': 300,  # 5 minutes default
    'CACHE_KEY_PREFIX': 'qmis_',
    'CACHE_THRESHOLD': 1000,  # Maximum number of items in cache
}
cache.init_app(app, config=cache_config)
migrate = Migrate(app, db)

# ✅ Register blueprint
app.register_blueprint(statistics_bp)
app.register_blueprint(md_dashboard_bp)
app.register_blueprint(report_bp)
app.register_blueprint(actions_bp)
app.register_blueprint(acknowledgements_bp)
app.register_blueprint(critical_bp)

# Register CLI commands
app.cli.add_command(create_admin_command)

# Custom Jinja2 filter for JSON escaping
from utils.filters import json_escape
app.template_filter('json_escape')(json_escape)

# Context processor to check for pending actions
@app.context_processor
def inject_pending_actions():
    """Inject pending actions status into all templates"""
    if current_user.is_authenticated:
        now = datetime.now(ZoneInfo('Asia/Kolkata'))
        start_date_obj = datetime.strptime('2025-07-01', '%Y-%m-%d').date()
        end_date_obj = now.date()
        date_filter = db.and_(
            db.func.date(Action.created_at) >= start_date_obj,
            db.func.date(Action.created_at) <= end_date_obj
        )
        
        base_q = Action.query.filter(
            Action.parent_action_id.is_(None),
            Action.status != 'Finished',
            date_filter
        )
        
        if current_user.role == 'MD':
            pending_actions = base_q.count()
        elif current_user.is_team_lead:
            team_user_ids = [r[0] for r in db.session.query(User.user_id).filter_by(team_id=current_user.team_id).all()]
            pending_actions = base_q.filter(
                (Action.assigned_user_id.in_(team_user_ids)) |
                (Action.created_by.in_(team_user_ids))
            ).count()
        else:
            pending_actions = base_q.filter(
                (Action.assigned_user_id == current_user.user_id) |
                (Action.created_by == current_user.user_id)
            ).count()
        
        return {
            'has_pending_actions': pending_actions > 0,
            'pending_actions_count': pending_actions
        }
    return {
        'has_pending_actions': False,
        'pending_actions_count': 0
    }


# Context processor for the Critical / CAPA nav badge
@app.context_processor
def inject_pending_critical():
    """Inject the Critical/CAPA pending count into all templates.

    Mirrors inject_pending_actions: a recipient sees findings awaiting their
    response, audit users additionally see everything pending review.
    """
    if not current_user.is_authenticated:
        return {
            'has_pending_critical': False,
            'pending_critical_count': 0,
            'can_view_critical': False
        }

    pending = critical_pending_count(current_user)
    return {
        'has_pending_critical': pending > 0,
        'pending_critical_count': pending,
        'can_view_critical': True
    }

# per-user cache key is provided by cache_utils.per_user_cache_key

# ---------------------------------------------------------------------------
# Jinja filter: ensure every datetime is displayed in Asia/Kolkata regardless
# of what the database stored. Handles three cases gracefully:
#   • TZ-aware value (UTC or otherwise)  → converts to IST
#   • Naive value                        → assumes it is UTC then converts
#   • Anything else / bad data          → falls back to str()
# ---------------------------------------------------------------------------

@app.template_filter('ist_strftime')
def ist_strftime_filter(date, format_string):
    """Format *date* in IST using *format_string* similar to strftime.

    The database stores timestamps in UTC, but the UI should always display
    Asia/Kolkata times.  This helper converts:

    • TZ-aware → directly to IST.
    • Naive    → interprets as UTC before converting.
    """
    if date is None:
        return ''

    try:
        # If the datetime is naive we assume it was stored in IST already
        # because MySQL DATETIME drops timezone information.
        if date.tzinfo is None:
            date = date.replace(tzinfo=ZoneInfo("Asia/Kolkata"))

        # Ensure we are in IST and format
        ist_date = date.astimezone(ZoneInfo("Asia/Kolkata"))
        return ist_date.strftime(format_string)
    except Exception:
        # Fallback – at least return something rather than crash the template
        return str(date)

# Import models after all extensions are initialized
from models import User, Team, Issue, Report, Action, Acknowledgement, Team1CalendarSchedule, Team1ASAActivities, Team1ASASports, Team1ASAGeneral, Team2HRAttendance, Team2AdminAttendance,Team2TotalHRAttendance, Team2RecruitmentActivity, Team2PendingRecruitment, Team2RecruitmentPipeline, Team2StaffStatusUpdates, Team2SalaryPending, Team2PoliceVerification, Team2InterviewSchedule, Team2ExitInformation, Team2IssuesStaffConcerns, Team2KuralRecitation, Team2FrontOfficePhoneCalls, Team2VisitorLog, Team2BSNLPhoneStatus, Team2MaterialsInward, Team2MaterialsOutward, Team2MaterialsMovement, Team2ReturnableMaterialTracking, Team2ReturnableGoodsReport, Team2CampusCameraStatus, Team2VehicleCameraStatus, Team2BusACCameraStatus, Team2GPSMonitoring, Team2IssuesIdentifiedMonitoring, Team2IssuesIdentifiedControlRoom, Team2CameraFootageEntry,  Team2BiometricsAccessCardPunching, Team2WaterTDSDeviation, Team2TestingCleaning, Team2WaterLevel, Team2PoolTesting, Team2WashroomCleanliness, Team2TransportAttendance, Team2ACWorkingStatus, Team2LateReporting, Team2MaintenanceServiceIssues, Team2CarMaintenanceCleaning,  Team2VehicleRenewalsDelays, Team2SpecialTrip, Team2ParentConcernDetail, Team2ACTemperatureCheck, Team2LaborEbSolarGenset, Team2Motor, Team2PestControl, Team2ACTempDeviation, Team2ElectricityConsumption, Team2EBDetails, Team2SolarDetails, Team2GensetDetails, Team2CountVerification, Team2AttendanceReplacement, Team2SecurityInfoNote,  Team2SecurityGovtInout, Team2AlcoholTest, Team2SecurityMaterialsInout, Team2SecurityMaterialsOutward, Team2TransportVerification, Team2DocumentsMovement, Team2GovtOfficialDocuments,  Team2ThoorigaiTeamSocialMedia, Team2WebsiteUpdates, Team2MDSocialMedia, Team2IntercomMaintenance, Team2HealthCheckUp, Team2NetConnectivityPrintDetails, Team2GeneralMaintenanceITProducts,  Team2CalendarSchedule, Team2TrainingAttendance, Team2TrainingDetails


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Create all database tables
with app.app_context():
    db.create_all()


# -----------------------------
# Submission History (My History)
# -----------------------------
@app.route('/my_history')
@cache.cached(timeout=300, key_prefix=per_user_cache_key)
@login_required
def my_history():
    # Optional filters
    start = request.args.get('start')  # YYYY-MM-DD
    end = request.args.get('end')      # YYYY-MM-DD
    form_query = request.args.get('form')  # optional: model class name filter

    start_dt = None
    end_dt = None
    try:
        if start:
            start_dt = datetime.strptime(start, '%Y-%m-%d')
        if end:
            # inclusive end of day
            end_dt = datetime.strptime(end, '%Y-%m-%d') + timedelta(days=1)
    except Exception:
        start_dt = None
        end_dt = None

    # Collect all concrete BaseForm subclasses
    # We imported models as models_module so we can introspect
    history_rows = []
    
    # Define the BaseForm models manually since introspection is complex
    base_form_models = [
        'Team1CalendarSchedule', 'Team1ASAActivities', 'Team1ASASports', 'Team1ASAGeneral',
        'Team1StudentAttendance', 'Team1StudentGrooming', 'Team1StudentLateComing',
        'Team1AdmissionStatus', 'Team1TransferCertificate', 'Team1ParentActivity',
        'Team1ParentVisit', 'Team1ExamSchedule', 'Team1ExternalInfo', 'Team1SickBay',
        'Team1HomeSchoolComm', 'Team1Disciplinary', 'Team1Logistics', 'Team1CompetitionCert',
        'Team1StaffConcern', 'Team1ParentConcern', 'Team1StudentConcern', 'Team1AEPAttendance',
        'Team1ExtendedClassAttendance', 'Team1TrainingSession', 'Team1WeeklyMeeting',
        'Team1SpecialEducation', 'Team1Hostel', 'Team1SEC', 'Team1SchoolCounsellor',
        'Team1Scholorius', 'Team1ParentConcernDetail',
        'Team2HRAttendance', 'Team2AdminAttendance', 'Team2TotalHRAttendance',
        'Team2RecruitmentActivity', 'Team2PendingRecruitment', 'Team2RecruitmentPipeline',
        'Team2StaffStatusUpdates', 'Team2SalaryPending', 'Team2PoliceVerification',
        'Team2InterviewSchedule', 'Team2ExitInformation', 'Team2IssuesStaffConcerns',
        'Team2KuralRecitation', 'Team2FrontOfficePhoneCalls', 'Team2VisitorLog',
        'Team2BSNLPhoneStatus', 'Team2MaterialsInward', 'Team2MaterialsOutward',
        'Team2MaterialsMovement', 'Team2ReturnableMaterialTracking', 'Team2ReturnableGoodsReport',
        'Team2CampusCameraStatus', 'Team2VehicleCameraStatus', 'Team2BusACCameraStatus',
        'Team2GPSMonitoring', 'Team2IssuesIdentifiedMonitoring', 'Team2IssuesIdentifiedControlRoom',
        'Team2CameraFootageEntry', 'Team2BiometricsAccessCardPunching', 'Team2WaterTDSDeviation',
        'Team2TestingCleaning', 'Team2WaterLevel', 'Team2HousekeepingGeneral', 'Team2PoolTesting', 'Team2WashroomCleanliness',
        'Team2TransportAttendance', 'Team2ACWorkingStatus', 'Team2LateReporting',
        'Team2MaintenanceServiceIssues', 'Team2CarMaintenanceCleaning', 'Team2VehicleRenewalsDelays',
        'Team2SpecialTrip', 'Team2ACTemperatureCheck', 'Team2LaborEbSolarGenset',
        'Team2Motor', 'Team2PestControl', 'Team2ACTempDeviation', 'Team2ElectricityConsumption',
        'Team2EBDetails', 'Team2SolarDetails', 'Team2GensetDetails', 'Team2CountVerification',
        'Team2AttendanceReplacement', 'Team2SecurityInfoNote', 'Team2SecurityGovtInout',
        'Team2AlcoholTest', 'Team2SecurityMaterialsInout', 'Team2SecurityMaterialsOutward',
        'Team2TransportVerification', 'Team2DocumentsMovement', 'Team2GovtOfficialDocuments',
        'Team2ThoorigaiTeamSocialMedia', 'Team2WebsiteUpdates', 'Team2MDSocialMedia',
        'Team2IntercomMaintenance', 'Team2HealthCheckUp', 'Team2NetConnectivityPrintDetails',
        'Team2GeneralMaintenanceITProducts', 'Team2CalendarSchedule', 'Team2TrainingAttendance',
        'Team2TrainingDetails', 'Team2ParentConcernDetail', 'Team2ManpowerPlanning', 'Team2OverallConsolidation', 
        'Team2UniformDetails', 'Team2DepartmentWiseUniformDetails', 'Team3Audit', 'Team3NewAudit',
        'CapaFinding'
    ]
    
    for model_name in base_form_models:
        # Optional filter for a single form/model
        if form_query and model_name != form_query:
            continue
            
        try:
            model_cls = getattr(models_module, model_name)
            if model_name == 'CapaFinding':
                q = model_cls.query.filter(
                    or_(
                        model_cls.submitted_by == current_user.user_id,
                        model_cls.capa_1_submitted_by == current_user.user_id,
                        model_cls.recipient_id == current_user.user_id
                    )
                )
            else:
                q = model_cls.query.filter_by(submitted_by=current_user.user_id)
            if start_dt:
                q = q.filter(model_cls.submitted_at >= start_dt)
            if end_dt:
                q = q.filter(model_cls.submitted_at < end_dt)
            q = q.order_by(model_cls.submitted_at.desc())
            results = q.limit(500).all()

            for r in results:
                # Collect all non-None fields from the record
                form_data = {}
                for field_name in dir(r):
                    if not field_name.startswith('_') and field_name not in ['form_id', 'team_id', 'submitted_by', 'submitted_at', 'metadata', 'query', 'query_class']:
                        try:
                            value = getattr(r, field_name)
                            if value is not None and value != '':
                                form_data[field_name] = str(value)
                        except:
                            pass

                history_rows.append({
                    'form_name': model_name,
                    'submitted_at': r.submitted_at,
                    'team_id': r.team_id,
                    'form_id': r.form_id,
                    'form_data': form_data
                })
        except Exception as e:
            # Ignore models without these fields or other errors
            continue

    # Sort overall by submitted_at desc
    history_rows.sort(key=lambda x: x['submitted_at'], reverse=True)

    return render_template('my_history.html', rows=history_rows, start=start or '', end=end or '', form_query=form_query or '')


# Basic routes
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

# Helper functions
from utils.helpers import safe_int, safe_float, safe_date, safe_time

def ensure_default_teams():
    # Create Team 1 if it doesn't exist
    team1 = Team.query.filter_by(team_name='Team 1').first()
    if not team1:
        team1 = Team(team_name='Team 1')
        db.session.add(team1)
    
    # Create Team 2 if it doesn't exist
    team2 = Team.query.filter_by(team_name='Team 2').first()
    if not team2:
        team2 = Team(team_name='Team 2')
        db.session.add(team2)

    # Create Team 3 if it doesn't exist
    team3 = Team.query.filter_by(team_name='Team 3').first()
    if not team3:
        team3 = Team(team_name='Team 3')
        db.session.add(team3)
    
    db.session.commit()

@app.route('/dashboard')
@login_required
@cache.cached(timeout=300, key_prefix=per_user_cache_key)
def dashboard():
    if current_user.role == 'Admin':
        # Ensure default teams exist
        ensure_default_teams()
        
        users = User.query.all()
        teams = Team.query.all()
        total_issues = Issue.query.count()
        open_issues = Issue.query.filter_by(status='Open').count()
        recent_issues = Issue.query.order_by(Issue.created_at.desc()).limit(5).all()
        return render_template('admin_dashboard.html',
                             users=users,
                             teams=teams,
                             total_issues=total_issues,
                             open_issues=open_issues,
                             recent_issues=recent_issues)
    elif current_user.role == 'Team Lead':
        # Redirect all team leads to unified dashboard scoped to their team
        team_param = 'team1' if current_user.team_id == 1 else 'team2' if current_user.team_id == 2 else 'team3'
        return redirect(url_for('md_dashboard.md_dashboard', team=team_param))
    elif current_user.role == 'Team Member':
        team_issues = Issue.query.filter_by(team_id=current_user.team_id).all()
        total_issues = len(team_issues)
        pending_issues = len([i for i in team_issues if i.status == 'Open'])
        in_progress_issues = len([i for i in team_issues if i.status == 'In Progress'])
        solved_issues = len([i for i in team_issues if i.status == 'Solved'])
        recent_issues = Issue.query.filter_by(team_id=current_user.team_id).order_by(Issue.created_at.desc()).limit(5).all()
        
        # Get the user's team information
        team = Team.query.get(current_user.team_id)
        
        return render_template('team_member_dashboard.html',
                             team_issues=team_issues,
                             total_issues=total_issues,
                             pending_issues=pending_issues,
                             in_progress_issues=in_progress_issues,
                             solved_issues=solved_issues,
                             recent_issues=recent_issues,
                             team=team)
    elif current_user.role == 'MD':
        users = User.query.all()
        teams = Team.query.all()
        total_issues = Issue.query.count()
        open_issues = Issue.query.filter_by(status='Open').count()
        recent_issues = Issue.query.order_by(Issue.created_at.desc()).limit(5).all()
        
        return render_template('md_dashboard.html',
                             users=users,
                             teams=teams,
                             total_issues=total_issues,
                             open_issues=open_issues,
                             recent_issues=recent_issues)
    return redirect(url_for('login'))


# Issue management routes
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
    
    # Check access permissions
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
            issue_description="",  # Empty description as per requirement
            priority="Medium",     # Default priority as per requirement
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
    
    # Allow admin to edit any issue, team lead to edit their team's issues
    if current_user.role not in ['Admin', 'Team Lead'] or (current_user.role == 'Team Lead' and issue.team_id != current_user.team_id):
        flash('Access denied.', 'error')
        return redirect(url_for('list_issues'))
    
    if request.method == 'POST':
        issue.issue_title = request.form.get('title')
        issue.issue_description = request.form.get('description')
        issue.priority = request.form.get('priority')
        issue.status = request.form.get('status')
        
        # Only admin can change team assignment
        if current_user.role == 'Admin':
            new_team_id = request.form.get('team_id')
            if new_team_id:
                issue.team_id = new_team_id
        
        # Handle issue resolution
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
    
    # Only admin can delete any issue
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
    
    # Allow admin to resolve any issue, team lead to resolve their team's issues
    if current_user.role not in ['Admin', 'Team Lead'] or (current_user.role == 'Team Lead' and issue.team_id != current_user.team_id):
        flash('Access denied.', 'error')
        return redirect(url_for('list_issues'))
    
    issue.status = 'Solved'
    issue.solved_by = current_user.user_id
    issue.solved_description = request.form.get('solved_description')
    
    db.session.commit()
    flash('Issue resolved successfully.', 'success')
    return redirect(url_for('view_issue', issue_id=issue_id))

# Admin routes
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
        
        # Handle team assignment
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
        # Handle foreign key constraints before deleting the user
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
        
        # 5. Handle team lead assignment - remove from team if user is a team lead
        teams_led = Team.query.filter_by(lead_id=user_id).all()
        for team in teams_led:
            team.lead_id = None
        
        # 6. Delete acknowledgements for this user
        acknowledgements = Acknowledgement.query.filter_by(user_id=user_id).all()
        for ack in acknowledgements:
            db.session.delete(ack)
        
        # 7. Delete all files uploaded by this user
        from models import FileStorage
        uploaded_files = FileStorage.query.filter_by(uploaded_by=user_id).all()
        for file_record in uploaded_files:
            db.session.delete(file_record)
        
        # 8. Delete dashboard view logs for this user
        try:
            from sqlalchemy import text
            delete_view_logs = text("DELETE FROM dashboard_view_log WHERE user_id = :user_id")
            db.session.execute(delete_view_logs, {'user_id': user_id})
        except Exception as view_log_error:
            # Continue if table doesn't exist
            print(f"Could not delete dashboard view logs: {str(view_log_error)}")
        
        # 9. Delete all form submissions by this user
        # Using direct SQL to handle all BaseForm inherited tables at once
        from sqlalchemy import text
        
        # Get all table names that have submitted_by column (form tables)
        form_tables = [
            # Team 1 Tables
            'team1_calendar_schedule', 'team1_asa_activities', 'team1_asa_sports', 'team1_student_attendance',
            'team1_student_grooming', 'team1_student_late_coming', 'team1_admission_status',
            'team1_transfer_certificate', 'team1_parent_activity', 'team1_parent_visit',
            'team1_exam_schedule', 'team1_external_info', 'team1_sick_bay',
            'team1_home_school_comm', 'team1_disciplinary', 'team1_logistics',
            'team1_competition_cert', 'team1_staff_concern', 'team1_student_concern', 'team1_parent_concern',
            'team1_parent_concern_detail', 'team1_aep_attendance', 'team1_extended_class_attendance',
            'team1_training_session', 'team1_weekly_meeting', 'team1_special_education',
            'team1_hostel', 'team1_sec', 'team1_school_counsellor', 'team1_scholorius',
            
            # Team 2 Tables
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
            'department_wise_uniform_details',
            
            # Team 3 Tables
            'team3_audit', 'team3_new_audit',
            
            # Team 1 ASA General
            'team1_asa_general'
        ]
        
        # Delete all form submissions by this user
        for table_name in form_tables:
            try:
                delete_query = text(f"DELETE FROM {table_name} WHERE submitted_by = :user_id")
                db.session.execute(delete_query, {'user_id': user_id})
            except Exception as table_error:
                # Continue if table doesn't exist or has no submitted_by column
                print(f"Could not delete from {table_name}: {str(table_error)}")
                continue
        
        # Now delete the user
        db.session.delete(user)
        db.session.commit()
        flash('User deleted successfully.', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting user: {str(e)}', 'error')
        
    return redirect(url_for('manage_users'))

# Team management routes
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
    
    # Only allow editing Team 1 and Team 2
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
            # Remove team_id from old team lead
            if old_lead_id:
                old_lead = User.query.get(old_lead_id)
                if old_lead:
                    old_lead.team_id = None
            
            # Update team with new lead
            team.lead_id = lead_id
            new_lead = User.query.get(lead_id)
            if new_lead:
                new_lead.team_id = team_id
        
        db.session.commit()
        flash('Team lead updated successfully.', 'success')
        return redirect(url_for('manage_teams'))
    
    return render_template('admin/edit_team.html', team=team, team_leads=team_leads)

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
    
    # Check if the user is part of the team that owns this issue
    if current_user.team_id != issue.team_id:
        flash('Access denied. You can only update issues for your team.', 'danger')
        return redirect(url_for('dashboard'))
    
    issue.issue_description = description
    issue.priority = priority
    issue.status = status
    
    db.session.commit()
    
    # Emit socket event for real-time updates
    socketio.emit('issue_update', {'issue_id': issue_id})
    
    flash('Issue updated successfully!', 'success')
    return redirect(url_for('dashboard'))

@app.route('/create-admin')
def create_admin():
    # Check if admin already exists
    admin = User.query.filter_by(username='admin').first()
    if admin:
        return 'Admin already exists'
    
    # Create admin user
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

from datetime import datetime, timezone


# ==========================================================================
# Form submission routes (108 handlers: Team 1 Academics, Team 2 Admin, Team 3 Audit)
# ==========================================================================
from routes.forms import register_all_form_routes
register_all_form_routes(app)

#completed for route

@app.route('/profile')
@login_required
def profile():
    """Render the user profile page"""
    return render_template('profile.html', user=current_user)

# Route to serve uploaded files from database
@app.route('/file/<int:file_id>')
@login_required
def serve_file(file_id):
    """Serve uploaded files from database BLOB storage"""
    try:
        file_record = FileStorage.query.get_or_404(file_id)
        
        # Create response with file data
        response = send_file(
            BytesIO(file_record.file_data),
            mimetype=file_record.mime_type,
            as_attachment=False,
            download_name=file_record.original_filename
        )
        
        # Add cache headers
        response.headers['Cache-Control'] = 'public, max-age=31536000'
        return response
        
    except Exception as e:
        return jsonify({'error': 'File not found'}), 404

# Route to serve uploaded files (legacy - for backward compatibility)
@app.route('/uploads/<path:filename>')
@login_required
def serve_legacy_file(filename):
    """Serve uploaded files securely from filesystem (legacy)"""
    try:
        return send_from_directory(os.path.join(app.root_path, 'static', 'uploads'), filename)
    except Exception as e:
        return jsonify({'error': 'File not found'}), 404

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    socketio.run(app, debug=True)

