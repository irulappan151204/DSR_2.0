import re
import models as models_module
from sqlalchemy import or_

# Mapping of model class names to human-readable metadata
FORM_METADATA = {
    # ── Team 1: Academics ─────────────────────────────────────────
    'Team1CalendarSchedule': {'title': 'Academic Calendar Schedule', 'dept': 'Team 1', 'dept_name': 'Academics', 'badge': 'badge-team1'},
    'Team1ASAActivities': {'title': 'ASA Activities', 'dept': 'Team 1', 'dept_name': 'Academics', 'badge': 'badge-team1'},
    'Team1ASASports': {'title': 'ASA Sports Attendance', 'dept': 'Team 1', 'dept_name': 'Academics', 'badge': 'badge-team1'},
    'Team1ASAGeneral': {'title': 'ASA General Attendance', 'dept': 'Team 1', 'dept_name': 'Academics', 'badge': 'badge-team1'},
    'Team1StudentAttendance': {'title': 'Student Attendance', 'dept': 'Team 1', 'dept_name': 'Academics', 'badge': 'badge-team1'},
    'Team1StudentGrooming': {'title': 'Student Grooming Defaulters', 'dept': 'Team 1', 'dept_name': 'Academics', 'badge': 'badge-team1'},
    'Team1StudentLateComing': {'title': 'Student Late Coming Log', 'dept': 'Team 1', 'dept_name': 'Academics', 'badge': 'badge-team1'},
    'Team1AdmissionStatus': {'title': 'Admission Status Report', 'dept': 'Team 1', 'dept_name': 'Academics', 'badge': 'badge-team1'},
    'Team1TransferCertificate': {'title': 'Transfer Certificate (TC)', 'dept': 'Team 1', 'dept_name': 'Academics', 'badge': 'badge-team1'},
    'Team1ParentActivity': {'title': 'Parent Activity Attendance', 'dept': 'Team 1', 'dept_name': 'Academics', 'badge': 'badge-team1'},
    'Team1ParentVisit': {'title': 'Parent Visit Log', 'dept': 'Team 1', 'dept_name': 'Academics', 'badge': 'badge-team1'},
    'Team1ExamSchedule': {'title': 'Exam Schedule & Attendance', 'dept': 'Team 1', 'dept_name': 'Academics', 'badge': 'badge-team1'},
    'Team1ExternalInfo': {'title': 'External Agency Info', 'dept': 'Team 1', 'dept_name': 'Academics', 'badge': 'badge-team1'},
    'Team1SickBay': {'title': 'Sick Bay / Health Room', 'dept': 'Team 1', 'dept_name': 'Academics', 'badge': 'badge-team1'},
    'Team1HomeSchoolComm': {'title': 'Home-School Communication', 'dept': 'Team 1', 'dept_name': 'Academics', 'badge': 'badge-team1'},
    'Team1Disciplinary': {'title': 'Disciplinary Measures Log', 'dept': 'Team 1', 'dept_name': 'Academics', 'badge': 'badge-team1'},
    'Team1Logistics': {'title': 'Academic Logistics Status', 'dept': 'Team 1', 'dept_name': 'Academics', 'badge': 'badge-team1'},
    'Team1CompetitionCert': {'title': 'Competitions & Certificates', 'dept': 'Team 1', 'dept_name': 'Academics', 'badge': 'badge-team1'},
    'Team1StaffConcern': {'title': 'Staff Concerns', 'dept': 'Team 1', 'dept_name': 'Academics', 'badge': 'badge-team1'},
    'Team1ParentConcern': {'title': 'Parent Concerns Summary', 'dept': 'Team 1', 'dept_name': 'Academics', 'badge': 'badge-team1'},
    'Team1StudentConcern': {'title': 'Student Concerns', 'dept': 'Team 1', 'dept_name': 'Academics', 'badge': 'badge-team1'},
    'Team1ParentConcernDetail': {'title': 'Parent Concern Details', 'dept': 'Team 1', 'dept_name': 'Academics', 'badge': 'badge-team1'},
    'Team1AEPAttendance': {'title': 'AEP Attendance', 'dept': 'Team 1', 'dept_name': 'Academics', 'badge': 'badge-team1'},
    'Team1ExtendedClassAttendance': {'title': 'Extended Class Attendance', 'dept': 'Team 1', 'dept_name': 'Academics', 'badge': 'badge-team1'},
    'Team1TrainingSession': {'title': 'Teacher Training Sessions', 'dept': 'Team 1', 'dept_name': 'Academics', 'badge': 'badge-team1'},
    'Team1WeeklyMeeting': {'title': 'Weekly Department Meetings', 'dept': 'Team 1', 'dept_name': 'Academics', 'badge': 'badge-team1'},
    'Team1SpecialEducation': {'title': 'Special Education (SEN)', 'dept': 'Team 1', 'dept_name': 'Academics', 'badge': 'badge-team1'},
    'Team1Hostel': {'title': 'Hostel Daily Status', 'dept': 'Team 1', 'dept_name': 'Academics', 'badge': 'badge-team1'},
    'Team1SEC': {'title': 'SEC Activity Status', 'dept': 'Team 1', 'dept_name': 'Academics', 'badge': 'badge-team1'},
    'Team1SchoolCounsellor': {'title': 'School Counsellor Log', 'dept': 'Team 1', 'dept_name': 'Academics', 'badge': 'badge-team1'},
    'Team1Scholorius': {'title': 'Scholorius Portal Updates', 'dept': 'Team 1', 'dept_name': 'Academics', 'badge': 'badge-team1'},

    # ── Team 2: Operations & Administration ───────────────────────
    'Team2HRAttendance': {'title': 'HR Attendance', 'dept': 'Team 2', 'dept_name': 'Operations', 'badge': 'badge-team2'},
    'Team2AdminAttendance': {'title': 'Admin Staff Attendance', 'dept': 'Team 2', 'dept_name': 'Operations', 'badge': 'badge-team2'},
    'Team2TotalHRAttendance': {'title': 'Total HR Attendance', 'dept': 'Team 2', 'dept_name': 'Operations', 'badge': 'badge-team2'},
    'Team2RecruitmentActivity': {'title': 'Recruitment Activity', 'dept': 'Team 2', 'dept_name': 'Operations', 'badge': 'badge-team2'},
    'Team2PendingRecruitment': {'title': 'Pending Recruitment', 'dept': 'Team 2', 'dept_name': 'Operations', 'badge': 'badge-team2'},
    'Team2RecruitmentPipeline': {'title': 'Recruitment Pipeline', 'dept': 'Team 2', 'dept_name': 'Operations', 'badge': 'badge-team2'},
    'Team2StaffStatusUpdates': {'title': 'Staff Status Updates', 'dept': 'Team 2', 'dept_name': 'Operations', 'badge': 'badge-team2'},
    'Team2SalaryPending': {'title': 'Salary Pending Log', 'dept': 'Team 2', 'dept_name': 'Operations', 'badge': 'badge-team2'},
    'Team2PoliceVerification': {'title': 'Police Verification', 'dept': 'Team 2', 'dept_name': 'Operations', 'badge': 'badge-team2'},
    'Team2InterviewSchedule': {'title': 'Interview Schedule', 'dept': 'Team 2', 'dept_name': 'Operations', 'badge': 'badge-team2'},
    'Team2ExitInformation': {'title': 'Staff Exit Information', 'dept': 'Team 2', 'dept_name': 'Operations', 'badge': 'badge-team2'},
    'Team2IssuesStaffConcerns': {'title': 'Operations Staff Concerns', 'dept': 'Team 2', 'dept_name': 'Operations', 'badge': 'badge-team2'},
    'Team2KuralRecitation': {'title': 'Kural Recitation Status', 'dept': 'Team 2', 'dept_name': 'Operations', 'badge': 'badge-team2'},
    'Team2FrontOfficePhoneCalls': {'title': 'Front Office Phone Calls', 'dept': 'Team 2', 'dept_name': 'Operations', 'badge': 'badge-team2'},
    'Team2VisitorLog': {'title': 'Visitor Log Register', 'dept': 'Team 2', 'dept_name': 'Operations', 'badge': 'badge-team2'},
    'Team2BSNLPhoneStatus': {'title': 'BSNL Landline Status', 'dept': 'Team 2', 'dept_name': 'Operations', 'badge': 'badge-team2'},
    'Team2MaterialsInward': {'title': 'Materials Inward Log', 'dept': 'Team 2', 'dept_name': 'Operations', 'badge': 'badge-team2'},
    'Team2MaterialsOutward': {'title': 'Materials Outward Log', 'dept': 'Team 2', 'dept_name': 'Operations', 'badge': 'badge-team2'},
    'Team2MaterialsMovement': {'title': 'Materials Movement', 'dept': 'Team 2', 'dept_name': 'Operations', 'badge': 'badge-team2'},
    'Team2ReturnableMaterialTracking': {'title': 'Returnable Material Tracking', 'dept': 'Team 2', 'dept_name': 'Operations', 'badge': 'badge-team2'},
    'Team2ReturnableGoodsReport': {'title': 'Returnable Goods Report', 'dept': 'Team 2', 'dept_name': 'Operations', 'badge': 'badge-team2'},
    'Team2CampusCameraStatus': {'title': 'Campus CCTV Camera Status', 'dept': 'Team 2', 'dept_name': 'Operations', 'badge': 'badge-team2'},
    'Team2VehicleCameraStatus': {'title': 'Vehicle Camera Status', 'dept': 'Team 2', 'dept_name': 'Operations', 'badge': 'badge-team2'},
    'Team2BusACCameraStatus': {'title': 'Bus AC & Camera Status', 'dept': 'Team 2', 'dept_name': 'Operations', 'badge': 'badge-team2'},
    'Team2GPSMonitoring': {'title': 'Transport GPS Monitoring', 'dept': 'Team 2', 'dept_name': 'Operations', 'badge': 'badge-team2'},
    'Team2IssuesIdentifiedMonitoring': {'title': 'CCTV Monitoring Issues', 'dept': 'Team 2', 'dept_name': 'Operations', 'badge': 'badge-team2'},
    'Team2IssuesIdentifiedControlRoom': {'title': 'Control Room Identified Issues', 'dept': 'Team 2', 'dept_name': 'Operations', 'badge': 'badge-team2'},
    'Team2CameraFootageEntry': {'title': 'CCTV Footage Request/Entry', 'dept': 'Team 2', 'dept_name': 'Operations', 'badge': 'badge-team2'},
    'Team2BiometricsAccessCardPunching': {'title': 'Biometrics & Access Cards', 'dept': 'Team 2', 'dept_name': 'Operations', 'badge': 'badge-team2'},
    'Team2WaterTDSDeviation': {'title': 'Water TDS Deviation', 'dept': 'Team 2', 'dept_name': 'Operations', 'badge': 'badge-team2'},
    'Team2TestingCleaning': {'title': 'Water Testing & Cleaning', 'dept': 'Team 2', 'dept_name': 'Operations', 'badge': 'badge-team2'},
    'Team2WaterLevel': {'title': 'Water Level Monitoring', 'dept': 'Team 2', 'dept_name': 'Operations', 'badge': 'badge-team2'},
    'Team2HousekeepingGeneral': {'title': 'Housekeeping General Status', 'dept': 'Team 2', 'dept_name': 'Operations', 'badge': 'badge-team2'},
    'Team2PoolTesting': {'title': 'Swimming Pool Water Testing', 'dept': 'Team 2', 'dept_name': 'Operations', 'badge': 'badge-team2'},
    'Team2WashroomCleanliness': {'title': 'Washroom Cleanliness Check', 'dept': 'Team 2', 'dept_name': 'Operations', 'badge': 'badge-team2'},
    'Team2TransportAttendance': {'title': 'Transport Staff Attendance', 'dept': 'Team 2', 'dept_name': 'Operations', 'badge': 'badge-team2'},
    'Team2ACWorkingStatus': {'title': 'Air Conditioner Working Status', 'dept': 'Team 2', 'dept_name': 'Operations', 'badge': 'badge-team2'},
    'Team2LateReporting': {'title': 'Late Reporting Register', 'dept': 'Team 2', 'dept_name': 'Operations', 'badge': 'badge-team2'},
    'Team2MaintenanceServiceIssues': {'title': 'Maintenance & Service Issues', 'dept': 'Team 2', 'dept_name': 'Operations', 'badge': 'badge-team2'},
    'Team2CarMaintenanceCleaning': {'title': 'Car Maintenance & Cleaning', 'dept': 'Team 2', 'dept_name': 'Operations', 'badge': 'badge-team2'},
    'Team2VehicleRenewalsDelays': {'title': 'Vehicle Renewals & Delays', 'dept': 'Team 2', 'dept_name': 'Operations', 'badge': 'badge-team2'},
    'Team2SpecialTrip': {'title': 'Transport Special Trips', 'dept': 'Team 2', 'dept_name': 'Operations', 'badge': 'badge-team2'},
    'Team2ACTemperatureCheck': {'title': 'AC Temperature Check', 'dept': 'Team 2', 'dept_name': 'Operations', 'badge': 'badge-team2'},
    'Team2LaborEbSolarGenset': {'title': 'Labor / EB / Solar / Genset', 'dept': 'Team 2', 'dept_name': 'Operations', 'badge': 'badge-team2'},
    'Team2Motor': {'title': 'Water Motor Status', 'dept': 'Team 2', 'dept_name': 'Operations', 'badge': 'badge-team2'},
    'Team2PestControl': {'title': 'Pest Control Schedule', 'dept': 'Team 2', 'dept_name': 'Operations', 'badge': 'badge-team2'},
    'Team2ACTempDeviation': {'title': 'AC Temperature Deviation', 'dept': 'Team 2', 'dept_name': 'Operations', 'badge': 'badge-team2'},
    'Team2ElectricityConsumption': {'title': 'Electricity Consumption Log', 'dept': 'Team 2', 'dept_name': 'Operations', 'badge': 'badge-team2'},
    'Team2EBDetails': {'title': 'EB Meter Readings', 'dept': 'Team 2', 'dept_name': 'Operations', 'badge': 'badge-team2'},
    'Team2SolarDetails': {'title': 'Solar Power Generation', 'dept': 'Team 2', 'dept_name': 'Operations', 'badge': 'badge-team2'},
    'Team2GensetDetails': {'title': 'Genset Generator Readings', 'dept': 'Team 2', 'dept_name': 'Operations', 'badge': 'badge-team2'},
    'Team2CountVerification': {'title': 'Security Headcount Verification', 'dept': 'Team 2', 'dept_name': 'Operations', 'badge': 'badge-team2'},
    'Team2AttendanceReplacement': {'title': 'Attendance Replacement', 'dept': 'Team 2', 'dept_name': 'Operations', 'badge': 'badge-team2'},
    'Team2SecurityInfoNote': {'title': 'Security Information Note', 'dept': 'Team 2', 'dept_name': 'Operations', 'badge': 'badge-team2'},
    'Team2SecurityGovtInout': {'title': 'Govt Officials In/Out Log', 'dept': 'Team 2', 'dept_name': 'Operations', 'badge': 'badge-team2'},
    'Team2AlcoholTest': {'title': 'Security Alcohol Breath Test', 'dept': 'Team 2', 'dept_name': 'Operations', 'badge': 'badge-team2'},
    'Team2SecurityMaterialsInout': {'title': 'Security Materials In/Out', 'dept': 'Team 2', 'dept_name': 'Operations', 'badge': 'badge-team2'},
    'Team2SecurityMaterialsOutward': {'title': 'Security Materials Outward', 'dept': 'Team 2', 'dept_name': 'Operations', 'badge': 'badge-team2'},
    'Team2TransportVerification': {'title': 'Transport Verification Register', 'dept': 'Team 2', 'dept_name': 'Operations', 'badge': 'badge-team2'},
    'Team2DocumentsMovement': {'title': 'Official Documents Movement', 'dept': 'Team 2', 'dept_name': 'Operations', 'badge': 'badge-team2'},
    'Team2GovtOfficialDocuments': {'title': 'Govt Official Documents', 'dept': 'Team 2', 'dept_name': 'Operations', 'badge': 'badge-team2'},
    'Team2ThoorigaiTeamSocialMedia': {'title': 'Thoorigai Social Media', 'dept': 'Team 2', 'dept_name': 'Operations', 'badge': 'badge-team2'},
    'Team2WebsiteUpdates': {'title': 'School Website Updates', 'dept': 'Team 2', 'dept_name': 'Operations', 'badge': 'badge-team2'},
    'Team2MDSocialMedia': {'title': 'MD Social Media Updates', 'dept': 'Team 2', 'dept_name': 'Operations', 'badge': 'badge-team2'},
    'Team2IntercomMaintenance': {'title': 'Intercom Line Maintenance', 'dept': 'Team 2', 'dept_name': 'Operations', 'badge': 'badge-team2'},
    'Team2HealthCheckUp': {'title': 'Staff Health Check-Up', 'dept': 'Team 2', 'dept_name': 'Operations', 'badge': 'badge-team2'},
    'Team2NetConnectivityPrintDetails': {'title': 'Network & Printing Status', 'dept': 'Team 2', 'dept_name': 'Operations', 'badge': 'badge-team2'},
    'Team2GeneralMaintenanceITProducts': {'title': 'IT Hardware Maintenance', 'dept': 'Team 2', 'dept_name': 'Operations', 'badge': 'badge-team2'},
    'Team2CalendarSchedule': {'title': 'Operations Calendar Schedule', 'dept': 'Team 2', 'dept_name': 'Operations', 'badge': 'badge-team2'},
    'Team2TrainingAttendance': {'title': 'Operations Training Attendance', 'dept': 'Team 2', 'dept_name': 'Operations', 'badge': 'badge-team2'},
    'Team2TrainingDetails': {'title': 'Operations Training Details', 'dept': 'Team 2', 'dept_name': 'Operations', 'badge': 'badge-team2'},
    'Team2ParentConcernDetail': {'title': 'Operations Parent Concerns', 'dept': 'Team 2', 'dept_name': 'Operations', 'badge': 'badge-team2'},
    'Team2ManpowerPlanning': {'title': 'Manpower Planning', 'dept': 'Team 2', 'dept_name': 'Operations', 'badge': 'badge-team2'},
    'Team2OverallConsolidation': {'title': 'Operations Daily Consolidation', 'dept': 'Team 2', 'dept_name': 'Operations', 'badge': 'badge-team2'},
    'Team2UniformDetails': {'title': 'Student Uniform Distribution', 'dept': 'Team 2', 'dept_name': 'Operations', 'badge': 'badge-team2'},
    'Team2DepartmentWiseUniformDetails': {'title': 'Dept-Wise Uniform Details', 'dept': 'Team 2', 'dept_name': 'Operations', 'badge': 'badge-team2'},

    # ── Team 3: Audit ─────────────────────────────────────────────
    'Team3Audit': {'title': 'Audit Checklist', 'dept': 'Team 3', 'dept_name': 'Audit', 'badge': 'badge-team3'},
    'Team3NewAudit': {'title': 'Quality Audit Observation', 'dept': 'Team 3', 'dept_name': 'Audit', 'badge': 'badge-team3'},
}

# Ordered list of all operational form models (excludes CapaFinding which has dedicated workflow handling)
ALL_FORM_MODEL_NAMES = list(FORM_METADATA.keys())


def get_model_meta(model_name):
    """Return friendly metadata dictionary for a model name, with automatic fallback."""
    if model_name in FORM_METADATA:
        return FORM_METADATA[model_name]
    
    # Automatic fallback for any unlisted model
    clean_title = re.sub(r'([A-Z])', r' \1', model_name).strip()
    clean_title = clean_title.replace('Team 1 ', '').replace('Team 2 ', '').replace('Team 3 ', '')
    dept = 'Team 1' if 'Team1' in model_name else ('Team 2' if 'Team2' in model_name else ('Team 3' if 'Team3' in model_name else 'General'))
    return {
        'title': clean_title or model_name,
        'dept': dept,
        'dept_name': 'Academics' if dept == 'Team 1' else ('Operations' if dept == 'Team 2' else ('Audit' if dept == 'Team 3' else 'General')),
        'badge': 'badge-team1' if dept == 'Team 1' else ('badge-team2' if dept == 'Team 2' else 'badge-team3')
    }


def get_form_choices():
    """Return choices formatted for an HTML <select> dropdown, grouped by department."""
    groups = {
        'Academics (Team 1)': [],
        'Operations & Administration (Team 2)': [],
        'Quality Audit (Team 3)': [],
    }
    for model_name, meta in FORM_METADATA.items():
        item = {'key': model_name, 'title': meta['title'], 'dept': meta['dept']}
        if meta['dept'] == 'Team 1':
            groups['Academics (Team 1)'].append(item)
        elif meta['dept'] == 'Team 2':
            groups['Operations & Administration (Team 2)'].append(item)
        elif meta['dept'] == 'Team 3':
            groups['Quality Audit (Team 3)'].append(item)

    # Sort each group alphabetically by title
    for grp in groups.values():
        grp.sort(key=lambda x: x['title'])
    return groups


def fetch_capa_history(user_id, start_dt=None, end_dt=None, limit=200):
    """Fetch CAPA findings where the user is recipient, author, or respondent."""
    try:
        from models import CapaFinding
        q = CapaFinding.query.filter(
            or_(
                CapaFinding.submitted_by == user_id,
                CapaFinding.recipient_id == user_id,
                CapaFinding.capa_1_submitted_by == user_id,
                CapaFinding.capa_2_submitted_by == user_id
            )
        )
        if start_dt:
            q = q.filter(CapaFinding.submitted_at >= start_dt)
        if end_dt:
            q = q.filter(CapaFinding.submitted_at < end_dt)

        return q.order_by(CapaFinding.submitted_at.desc()).limit(limit).all()
    except Exception:
        return []


def fetch_form_history(user_id, start_dt=None, end_dt=None, form_query=None, limit_per_model=100):
    """Query user submission records across operational form models.
    
    If form_query is provided, queries ONLY that single model for ultra-fast performance.
    """
    results = []

    # If the user filtered by a specific form, execute only 1 targeted query
    models_to_query = [form_query] if (form_query and form_query in FORM_METADATA) else ALL_FORM_MODEL_NAMES

    for model_name in models_to_query:
        try:
            model_cls = getattr(models_module, model_name, None)
            if not model_cls:
                continue

            q = model_cls.query.filter_by(submitted_by=user_id)
            if start_dt:
                q = q.filter(model_cls.submitted_at >= start_dt)
            if end_dt:
                q = q.filter(model_cls.submitted_at < end_dt)

            q = q.order_by(model_cls.submitted_at.desc())
            records = q.limit(limit_per_model).all()
            if records:
                results.append((model_name, records))
        except Exception:
            continue

    return results
