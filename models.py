from extensions import db
from flask_login import UserMixin, current_user
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from timezone_utils import now_ist

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.Enum('Admin', 'Team Lead', 'Team Member', 'MD', name='user_role'), nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.team_id'))
    
    # Relationships
    team = db.relationship('Team', foreign_keys=[team_id], back_populates='members')
    led_team = db.relationship('Team', back_populates='team_lead', foreign_keys='Team.lead_id')

    def get_id(self):
        return str(self.user_id)
        
    @property
    def is_team_lead(self):
        return self.role == 'Team Lead'

class Team(db.Model):
    __tablename__ = 'teams'
    
    team_id = db.Column(db.Integer, primary_key=True)
    team_name = db.Column(db.String(100), unique=True, nullable=False)
    lead_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    
    # Relationships
    team_lead = db.relationship('User', foreign_keys=[lead_id], back_populates='led_team')
    members = db.relationship('User', back_populates='team', foreign_keys='User.team_id')
    issues = db.relationship('Issue', backref=db.backref('team', uselist=False), lazy=True)
    
    # Team 1 Form Relationships
    team1_calendar = db.relationship('Team1CalendarSchedule', backref='team', lazy=True)
    team1_asa = db.relationship('Team1ASAActivities', backref='team', lazy=True)
    team1_asa_sports = db.relationship('Team1ASASports', backref='team', lazy=True)
    team1_asa_general = db.relationship('Team1ASAGeneral', backref='team', lazy=True)
    team1_student_attendance = db.relationship('Team1StudentAttendance', backref='team', lazy=True)
    team1_student_grooming = db.relationship('Team1StudentGrooming', backref='team', lazy=True)
    team1_student_late_coming = db.relationship('Team1StudentLateComing', backref='team', lazy=True)
    team1_admission_status = db.relationship('Team1AdmissionStatus', backref='team', lazy=True)
    team1_transfer_certificate = db.relationship('Team1TransferCertificate', backref='team', lazy=True)
    team1_parent_activity = db.relationship('Team1ParentActivity', backref='team', lazy=True)
    team1_parent_visit = db.relationship('Team1ParentVisit', backref='team', lazy=True)
    team1_exam_schedule = db.relationship('Team1ExamSchedule', backref='team', lazy=True)
    team1_external_info = db.relationship('Team1ExternalInfo', backref='team', lazy=True)
    team1_sick_bay = db.relationship('Team1SickBay', backref='team', lazy=True)
    team1_home_school_comm = db.relationship('Team1HomeSchoolComm', backref='team', lazy=True)
    team1_disciplinary = db.relationship('Team1Disciplinary', backref='team', lazy=True)
    team1_logistics = db.relationship('Team1Logistics', backref='team', lazy=True)
    team1_competition_cert = db.relationship('Team1CompetitionCert', backref='team', lazy=True)
    team1_staff_concern = db.relationship('Team1StaffConcern', backref='team', lazy=True)
    team1_parent_concern = db.relationship('Team1ParentConcern', backref='team', lazy=True)
    team1_aep_attendance = db.relationship('Team1AEPAttendance', backref='team', lazy=True)
    team1_extended_class_attendance = db.relationship('Team1ExtendedClassAttendance', backref='team', lazy=True)
    team1_training_session = db.relationship('Team1TrainingSession', backref='team', lazy=True)
    team1_weekly_meeting = db.relationship('Team1WeeklyMeeting', backref='team', lazy=True)
    team1_parent_concern_detail = db.relationship('Team1ParentConcernDetail', backref='team', lazy=True)
    team1_student_concern = db.relationship('Team1StudentConcern', backref='team', lazy=True)
    team1_special_education = db.relationship('Team1SpecialEducation', backref='team', lazy=True)
    team1_hostel = db.relationship('Team1Hostel', backref='team', lazy=True)
    team1_sec = db.relationship('Team1SEC', backref='team', lazy=True)
    team1_school_counsellor = db.relationship('Team1SchoolCounsellor', backref='team', lazy=True)
    team1_scholorius = db.relationship('Team1Scholorius', backref='team', lazy=True)
    
    # Team 2 Form Relationships
    team2_hr_attendance = db.relationship('Team2HRAttendance', backref='team', lazy=True)
    team2_admin_attendance = db.relationship('Team2AdminAttendance', backref='team', lazy=True)
    team2_total_hr_attendance = db.relationship('Team2TotalHRAttendance', backref='team', lazy=True)
    team2_recruitment_activity = db.relationship('Team2RecruitmentActivity', backref='team', lazy=True)
    team2_pending_recruitment = db.relationship('Team2PendingRecruitment', backref='team', lazy=True)
    team2_recruitment_pipeline = db.relationship('Team2RecruitmentPipeline', backref='team', lazy=True)
    team2_staff_status_updates = db.relationship('Team2StaffStatusUpdates', backref='team', lazy=True)
    team2_salary_pending = db.relationship('Team2SalaryPending', backref='team', lazy=True)
    team2_police_verification = db.relationship('Team2PoliceVerification', backref='team', lazy=True)
    team2_interview_schedule = db.relationship('Team2InterviewSchedule', backref='team', lazy=True)
    team2_exit_information = db.relationship('Team2ExitInformation', backref='team', lazy=True)
    team2_issues_staff_concerns = db.relationship('Team2IssuesStaffConcerns', backref='team', lazy=True)
    team2_kural_recitation = db.relationship('Team2KuralRecitation', backref='team', lazy=True)
    team2_front_office_phone_calls = db.relationship('Team2FrontOfficePhoneCalls', backref='team', lazy=True)
    team2_visitor_log = db.relationship('Team2VisitorLog', backref='team', lazy=True)
    team2_bsnl_phone_status = db.relationship('Team2BSNLPhoneStatus', backref='team', lazy=True)
    team2_materials_inward = db.relationship('Team2MaterialsInward', backref='team', lazy=True) 
    team2_materials_outward = db.relationship('Team2MaterialsOutward', backref='team', lazy=True)
    team2_materials_movement = db.relationship('Team2MaterialsMovement', backref='team', lazy=True)
    team2_returnable_material_tracking = db.relationship('Team2ReturnableMaterialTracking', backref='team', lazy=True)
    team2_returnable_goods_report = db.relationship('Team2ReturnableGoodsReport', backref='team', lazy=True)    
    team2_campus_camera_status = db.relationship('Team2CampusCameraStatus', backref='team', lazy=True)  
    team2_vehicle_camera_status = db.relationship('Team2VehicleCameraStatus', backref='team', lazy=True)
    team2_bus_ac_camera_status = db.relationship('Team2BusACCameraStatus', backref='team', lazy=True)
    team2_gps_monitoring = db.relationship('Team2GPSMonitoring', backref='team', lazy=True)
    team2_issues_identified_monitoring = db.relationship('Team2IssuesIdentifiedMonitoring', backref='team', lazy=True)
    team2_issues_identified_control_room = db.relationship('Team2IssuesIdentifiedControlRoom', backref='team', lazy=True)
    team2_camera_footage_entry = db.relationship('Team2CameraFootageEntry', backref='team', lazy=True)
    team2_biometrics_access_card_punching = db.relationship('Team2BiometricsAccessCardPunching', backref='team', lazy=True)
    team2_water_tds_deviation = db.relationship('Team2WaterTDSDeviation', backref='team', lazy=True)
    team2_testing_cleaning = db.relationship('Team2TestingCleaning', backref='team', lazy=True)
    team2_water_level = db.relationship('Team2WaterLevel', backref='team', lazy=True)
    team2_housekeeping_general = db.relationship('Team2HousekeepingGeneral', backref='team', lazy=True)
    team2_pool_testing = db.relationship('Team2PoolTesting', backref='team', lazy=True)
    team2_washroom_cleanliness = db.relationship('Team2WashroomCleanliness', backref='team', lazy=True)
    team2_transport_attendance = db.relationship('Team2TransportAttendance', backref='team', lazy=True)
    team2_ac_working_status = db.relationship('Team2ACWorkingStatus', backref='team', lazy=True)
    team2_late_reporting = db.relationship('Team2LateReporting', backref='team', lazy=True)
    team2_maintenance_service_issues = db.relationship('Team2MaintenanceServiceIssues', backref='team', lazy=True)
    team2_car_maintenance_cleaning = db.relationship('Team2CarMaintenanceCleaning', backref='team', lazy=True)
    team2_vehicle_renewals_delays = db.relationship('Team2VehicleRenewalsDelays', backref='team', lazy=True)
    team2_special_trip = db.relationship('Team2SpecialTrip', backref='team', lazy=True)
    team2_parent_concern_detail = db.relationship('Team2ParentConcernDetail', backref='team', lazy=True)
    team2_training_attendance = db.relationship('Team2TrainingAttendance', backref='team', lazy=True)
    team2_training_details = db.relationship('Team2TrainingDetails', backref='team', lazy=True)
    team2_manpower_planning = db.relationship('Team2ManpowerPlanning', backref='team', lazy=True)
    team2_overall_consolidation = db.relationship('Team2OverallConsolidation', backref='team', lazy=True)
    team2_uniform_details = db.relationship('Team2UniformDetails', backref='team', lazy=True)
    team2_department_wise_uniform_details = db.relationship('Team2DepartmentWiseUniformDetails', backref='team', lazy=True)
    team2_calendar_schedule = db.relationship('Team2CalendarSchedule', backref='team', lazy=True)
    team2_general_maintenance_it_products = db.relationship('Team2GeneralMaintenanceITProducts', backref='team', lazy=True)
    team2_net_connectivity_print_details = db.relationship('Team2NetConnectivityPrintDetails', backref='team', lazy=True)
    team2_health_check_up = db.relationship('Team2HealthCheckUp', backref='team', lazy=True)
    team2_intercom_maintenance = db.relationship('Team2IntercomMaintenance', backref='team', lazy=True)
    team2_md_social_media = db.relationship('Team2MDSocialMedia', backref='team', lazy=True)
    team2_website_updates = db.relationship('Team2WebsiteUpdates', backref='team', lazy=True)
    team2_thoorigai_team_social_media = db.relationship('Team2ThoorigaiTeamSocialMedia', backref='team', lazy=True)
    team2_govt_official_documents = db.relationship('Team2GovtOfficialDocuments', backref='team', lazy=True)
    team2_documents_movement = db.relationship('Team2DocumentsMovement', backref='team', lazy=True)
    team2_transport_verification = db.relationship('Team2TransportVerification', backref='team', lazy=True)
    team2_security_materials_outward = db.relationship('Team2SecurityMaterialsOutward', backref='team', lazy=True)
    team2_security_materials_inout = db.relationship('Team2SecurityMaterialsInout', backref='team', lazy=True)
    team2_alcohol_test = db.relationship('Team2AlcoholTest', backref='team', lazy=True)
    team2_security_govt_inout = db.relationship('Team2SecurityGovtInout', backref='team', lazy=True)
    team2_security_info_note = db.relationship('Team2SecurityInfoNote', backref='team', lazy=True)
    team2_attendance_replacement = db.relationship('Team2AttendanceReplacement', backref='team', lazy=True)
    team2_count_verification = db.relationship('Team2CountVerification', backref='team', lazy=True)
    team2_genset_details = db.relationship('Team2GensetDetails', backref='team', lazy=True)
    team2_solar_details = db.relationship('Team2SolarDetails', backref='team', lazy=True)
    team2_eb_details = db.relationship('Team2EBDetails', backref='team', lazy=True)
    team2_electricity_consumption = db.relationship('Team2ElectricityConsumption', backref='team', lazy=True)
    team2_ac_temp_deviation = db.relationship('Team2ACTempDeviation', backref='team', lazy=True)
    team2_motor = db.relationship('Team2Motor', backref='team', lazy=True)
    team2_pest_control = db.relationship('Team2PestControl', backref='team', lazy=True)
    team2_labor_eb_solar_genset = db.relationship('Team2LaborEbSolarGenset', backref='team', lazy=True)
    team2_ac_temperature_check = db.relationship('Team2ACTemperatureCheck', backref='team', lazy=True)

    # Team 3 Form Relationships
    team3_audit = db.relationship('Team3Audit', backref='team', lazy=True)
    team3_new_audit = db.relationship('Team3NewAudit', backref='team', lazy=True)

    # Critical / CAPA workflow
    capa_findings = db.relationship('CapaFinding', backref='team', lazy=True)

class Issue(db.Model):
    __tablename__ = 'issues'
    
    issue_id = db.Column(db.Integer, primary_key=True)
    issue_title = db.Column(db.String(200), nullable=False)
    issue_description = db.Column(db.Text, nullable=False)
    priority = db.Column(db.String(20), nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.team_id'), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='Pending')
    solved_by = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    solved_description = db.Column(db.Text)
    created_by_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(ZoneInfo('Asia/Kolkata')))
    updated_at = db.Column(db.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(ZoneInfo('Asia/Kolkata')), onupdate=lambda: datetime.now(ZoneInfo('Asia/Kolkata')))
    
    # Relationships
    creator = db.relationship('User', foreign_keys=[created_by_id], backref=db.backref('created_issues', lazy=True))
    resolver = db.relationship('User', foreign_keys=[solved_by], backref=db.backref('resolved_issues', lazy=True))

class Report(db.Model):
    __tablename__ = 'reports'
    
    report_id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.team_id'), nullable=False)
    total_issues = db.Column(db.Integer, nullable=False)
    resolved_issues = db.Column(db.Integer, nullable=False)
    pending_issues = db.Column(db.Integer, nullable=False)
    avg_resolution_time = db.Column(db.Float)
    report_date = db.Column(db.Date, nullable=False)

# Base form models with common fields
class BaseForm(db.Model):
    __abstract__ = True
    
    form_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.team_id'), nullable=False)
    submitted_by = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    submitted_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(ZoneInfo("Asia/Kolkata"))
    )

# Team 1 Form Model    
class Team1CalendarSchedule(BaseForm):
    __tablename__ = 'team1_calendar_schedule'

    # Jr. School
    cal_session_jr = db.Column(db.String(200))
    cal_dept_jr = db.Column(db.String(200))
    cal_plan_jr = db.Column(db.String(50))
    cal_total_jr = db.Column(db.Integer)
    cal_expected_jr = db.Column(db.Integer)
    cal_present_pct_jr = db.Column(db.Float)
    cal_absent_pct_jr = db.Column(db.Float)
    cal_issue_nature_jr = db.Column(db.String(50))
    cal_issue_desc_jr = db.Column(db.Text)
    cal_comment_jr = db.Column(db.Text)

    # Sr. School
    cal_session_sr = db.Column(db.String(200))
    cal_dept_sr = db.Column(db.String(200))
    cal_plan_sr = db.Column(db.String(50))
    cal_total_sr = db.Column(db.Integer)
    cal_expected_sr = db.Column(db.Integer)
    cal_present_pct_sr = db.Column(db.Float)
    cal_absent_pct_sr = db.Column(db.Float)
    cal_issue_nature_sr = db.Column(db.String(50))
    cal_issue_desc_sr = db.Column(db.Text)
    cal_comment_sr = db.Column(db.Text)

    
    # Relationships
    submitter = db.relationship('User', foreign_keys='Team1CalendarSchedule.submitted_by', backref=db.backref('submitted_team1_calendar', lazy=True))

class Team1ASAActivities(BaseForm):
    __tablename__ = 'team1_asa_activities'
    
    # Paid Activities
    asa_strength_paid = db.Column(db.Integer)
    asa_enrolled_paid = db.Column(db.Integer)
    asa_enrol_pct_paid = db.Column(db.Float)
    asa_activities_paid = db.Column(db.String(200))
    asa_expected_paid = db.Column(db.Integer)
    asa_attended_paid = db.Column(db.Integer)
    asa_attend_pct_paid = db.Column(db.Float)
    
    # Regular Activities
    asa_strength_reg = db.Column(db.Integer)
    asa_enrolled_reg = db.Column(db.Integer)
    asa_enrol_pct_reg = db.Column(db.Float)
    asa_activities_reg = db.Column(db.String(200))
    asa_expected_reg = db.Column(db.Integer)
    asa_attended_reg = db.Column(db.Integer)
    asa_attend_pct_reg = db.Column(db.Float)
    
    # Rifle Shooting
    asa_strength_rifle = db.Column(db.Integer)
    asa_enrolled_rifle = db.Column(db.Integer)
    asa_enrol_pct_rifle = db.Column(db.Float)
    asa_activities_rifle = db.Column(db.String(200))
    asa_expected_rifle = db.Column(db.Integer)
    asa_attended_rifle = db.Column(db.Integer)
    asa_attend_pct_rifle = db.Column(db.Float)
    
    # NCC
    asa_strength_ncc = db.Column(db.Integer)
    asa_enrolled_ncc = db.Column(db.Integer)
    asa_enrol_pct_ncc = db.Column(db.Float)
    asa_activities_ncc = db.Column(db.String(200))
    asa_expected_ncc = db.Column(db.Integer)
    asa_attended_ncc = db.Column(db.Integer)
    asa_attend_pct_ncc = db.Column(db.Float)
    
    # Relationships
    submitter = db.relationship('User', foreign_keys='Team1ASAActivities.submitted_by', backref=db.backref('submitted_team1_asa', lazy=True))

class Team1ASASports(BaseForm):
    __tablename__ = 'team1_asa_sports'
    
    # Sports ASA data stored as JSON
    # Format: {"activity_name": {"strength": 0, "enrolled": 0, "enrol_pct": 0, "activities": "", "expected": 0, "attended": 0, "attend_pct": 0}}
    asa_sports_data = db.Column(db.JSON)
    
    # Relationships
    submitter = db.relationship('User', foreign_keys='Team1ASASports.submitted_by', backref=db.backref('submitted_team1_asa_sports', lazy=True))

# <!-- S.No 3: Students Attendance -->
class Team1StudentAttendance(BaseForm):
    __tablename__ = 'team1_student_attendance'
    
    # Kindergarten
    att_str_kg = db.Column(db.Integer)
    att_present_kg = db.Column(db.Integer)
    att_leave_kg = db.Column(db.Integer)
    att_absent_kg = db.Column(db.Integer)
    att_present_pct_kg = db.Column(db.Float)
    att_issue_nature_kg = db.Column(db.String(50))
    att_issue_desc_kg = db.Column(db.Text)
    att_comment_kg = db.Column(db.Text)
    
    # Grades 1 to 5
    att_str_g15 = db.Column(db.Integer)
    att_present_g15 = db.Column(db.Integer)
    att_leave_g15 = db.Column(db.Integer)
    att_absent_g15 = db.Column(db.Integer)
    att_present_pct_g15 = db.Column(db.Float)
    att_issue_nature_g15 = db.Column(db.String(50))
    att_issue_desc_g15 = db.Column(db.Text)
    att_comment_g15 = db.Column(db.Text)
    
    # Grades 6 to 10
    att_str_g610 = db.Column(db.Integer)
    att_present_g610 = db.Column(db.Integer)
    att_leave_g610 = db.Column(db.Integer)
    att_absent_g610 = db.Column(db.Integer)
    att_present_pct_g610 = db.Column(db.Float)
    att_issue_nature_g610 = db.Column(db.String(50))
    att_issue_desc_g610 = db.Column(db.Text)
    att_comment_g610 = db.Column(db.Text)
    
    # Grades 11 to 12
    att_str_g1112 = db.Column(db.Integer)
    att_present_g1112 = db.Column(db.Integer)
    att_leave_g1112 = db.Column(db.Integer)
    att_absent_g1112 = db.Column(db.Integer)
    att_present_pct_g1112 = db.Column(db.Float)
    att_issue_nature_g1112 = db.Column(db.String(50))
    att_issue_desc_g1112 = db.Column(db.Text)
    att_comment_g1112 = db.Column(db.Text)
    
    # Overall
    att_str_overall = db.Column(db.Integer)
    att_present_overall = db.Column(db.Integer)
    att_leave_overall = db.Column(db.Integer)
    att_absent_overall = db.Column(db.Integer)
    att_present_pct_overall = db.Column(db.Float)
    att_issue_nature_overall = db.Column(db.String(50))
    att_issue_desc_overall = db.Column(db.Text)
    att_comment_overall = db.Column(db.Text)
    
    # Relationships
    submitter = db.relationship('User', foreign_keys='Team1StudentAttendance.submitted_by', backref=db.backref('submitted_team1_attendance', lazy=True))

#S.No 4: Students Grooming 

class Team1StudentGrooming(BaseForm):
    __tablename__ = 'team1_student_grooming'

    # Default values for S.No, Work Activity, Department/Category
    grooming_s_no = db.Column(db.Integer)  # S.No
    grooming_work_activity = db.Column(db.String(100), default='Students Grooming')  # Work Activity
    grooming_dept_category = db.Column(db.String(100), default='PE')  # Department/Category

    # Grooming Details
    grooming_total_strength = db.Column(db.Integer)
    grooming_regular_students = db.Column(db.Integer)
    grooming_defaulters_count = db.Column(db.Integer)
    grooming_defaulters_pct = db.Column(db.Float)
    grooming_issue_nature = db.Column(db.String(50))
    grooming_issue_desc = db.Column(db.Text)
    grooming_comments = db.Column(db.Text)

    # Relationships
    submitter = db.relationship('User', foreign_keys='Team1StudentGrooming.submitted_by', backref=db.backref('submitted_team1_grooming', lazy=True))

#S.No 5: Students Late Coming

class Team1StudentLateComing(BaseForm):
    __tablename__ = 'team1_student_late_coming'

    # Default values for S.No, Work Activity, Department/Category
    late_coming_s_no = db.Column(db.Integer)  # S.No
    late_coming_work_activity = db.Column(db.String(100), default='Students Late Coming')  # Work Activity
    late_coming_dept_category = db.Column(db.String(100), default='PE')  # Department/Category

    # Late Coming Details
    late_coming_total_strength = db.Column(db.Integer)
    late_coming_regular_students = db.Column(db.Integer)
    late_coming_defaulters_count = db.Column(db.Integer)
    late_coming_defaulters_pct = db.Column(db.Float)
    late_coming_issue_nature = db.Column(db.String(50))
    late_coming_issue_desc = db.Column(db.Text)
    late_coming_comments = db.Column(db.Text)

    # Relationships
    submitter = db.relationship('User', foreign_keys='Team1StudentLateComing.submitted_by', backref=db.backref('submitted_team1_late_coming', lazy=True))

# S.No 6: Admission Status
class Team1AdmissionStatus(BaseForm):
    __tablename__ = 'team1_admission_status'

    # Default values for S.No, Work Activity, Department/Category
    admission_s_no = db.Column(db.Integer)  # S.No
    admission_work_activity = db.Column(db.String(100))  # Work Activity
    admission_dept_category = db.Column(db.String(100), default='Admissions')  # Department/Category

    # Admission Details
    admission_total = db.Column(db.Integer)
    admission_walkin = db.Column(db.Integer)
    admission_appln = db.Column(db.Integer)
    admission_ela = db.Column(db.Integer)
    admission_recommended = db.Column(db.Integer)
    admission_status = db.Column(db.String(100))
    admission_issue_nature = db.Column(db.String(50))
    admission_issue_desc = db.Column(db.Text)
    admission_comments = db.Column(db.Text)

    # Relationships
    submitter = db.relationship('User', foreign_keys='Team1AdmissionStatus.submitted_by', backref=db.backref('submitted_team1_admission_status', lazy=True))

#S.No 7: Transfer Certificate
class Team1TransferCertificate(BaseForm):
    __tablename__ = 'team1_transfer_certificate'

    # Default values for S.No, Work Activity, Department/Category
    transfer_certificate_s_no = db.Column(db.Integer, default=7)  # S.No
    transfer_certificate_work_activity = db.Column(db.String(100), default='Transfer Cert')  # Work Activity
    transfer_certificate_dept_category = db.Column(db.String(100), default='MLM')  # Department/Category

    # Transfer Certificate Details
    transfer_certificate_grade = db.Column(db.String(10))
    transfer_certificate_student_name = db.Column(db.String(100))
    transfer_certificate_year_at_qmis = db.Column(db.String(10))
    transfer_certificate_reason = db.Column(db.String(255))
    transfer_certificate_staff_in_charge = db.Column(db.String(100))
    transfer_certificate_sibling = db.Column(db.String(50))
    transfer_certificate_issue_nature = db.Column(db.String(50))
    transfer_certificate_issue_desc = db.Column(db.Text)
    transfer_certificate_comments = db.Column(db.Text)

    # Relationships
    submitter = db.relationship('User', foreign_keys='Team1TransferCertificate.submitted_by', backref=db.backref('submitted_team1_transfer_certificate', lazy=True))

#S.No 8: Parent Activity
class Team1ParentActivity(BaseForm):
    __tablename__ = 'team1_parent_activity'

    # Default values for S.No, Work Activity, Department/Category
    parent_activity_s_no = db.Column(db.Integer, default=8)  # S.No
    parent_activity_work_activity = db.Column(db.String(100), default='Parent Activity')  # Work Activity
    parent_activity_dept_category = db.Column(db.String(100))  # Dept/Cat

    # Parent Activity Details
    parent_activity_session = db.Column(db.String(100))  # Session/Activity
    parent_activity_dept = db.Column(db.String(100))  # Dept
    parent_activity_expected = db.Column(db.Integer)  # Expected
    parent_activity_reported = db.Column(db.Integer)  # Reported
    parent_activity_not_reported = db.Column(db.Integer)  # Not Reported
    parent_activity_present_pct = db.Column(db.Float)  # Present %
    parent_activity_absent_pct = db.Column(db.Float)  # Absent %
    parent_activity_issue_nature = db.Column(db.String(50))  # Nature of Issue
    parent_activity_issue_desc = db.Column(db.Text)  # Issue Desc
    parent_activity_comments = db.Column(db.Text)  # Comments

    # Relationships
    submitter = db.relationship('User', foreign_keys='Team1ParentActivity.submitted_by', backref=db.backref('submitted_team1_parent_activity', lazy=True))

#S.No 9: Parent Visit
class Team1ParentVisit(BaseForm):
    __tablename__ = 'team1_parent_visit'

    # Default values for S.No, Work Activity, Department/Category
    parent_visit_s_no = db.Column(db.Integer, default=9)  # S.No
    parent_visit_work_activity = db.Column(db.String(100), default='Parent Visit')  # Work Activity
    parent_visit_dept_category = db.Column(db.String(100))  # Dept/Cat

    # Parent Visit Details
    parent_visit_grade = db.Column(db.String(10))  # Grade
    parent_visit_student_name = db.Column(db.String(100))  # Student Name
    parent_visit_year_at_qmis = db.Column(db.String(10))  # Year@QMIS
    parent_visit_parents_profession = db.Column(db.String(100))  # Parent's Profession
    parent_visit_concern_appreciation = db.Column(db.Text)  # Concern/Appreciation
    parent_visit_staff_in_charge = db.Column(db.String(100))  # Staff In-charge
    parent_visit_issue_nature = db.Column(db.String(50))  # Nature of Issue
    parent_visit_issue_desc = db.Column(db.Text)  # Issue Desc
    parent_visit_comments = db.Column(db.Text)  # Comments

    # Relationships
    submitter = db.relationship('User', foreign_keys='Team1ParentVisit.submitted_by', backref=db.backref('submitted_team1_parent_visit', lazy=True))

#S.No 10: Exam Schedule

class Team1ExamSchedule(BaseForm):
    __tablename__ = 'team1_exam_schedule'

    # Default values for S.No, Work Activity, Department/Category
    exam_schedule_s_no = db.Column(db.Integer, default=10)  # S.No
    exam_schedule_work_activity = db.Column(db.String(100), default='Exam Schedule')  # Work Activity

    # Exam Schedule Details for different grades
    exam_schedule_g15 = db.Column(db.String(100))  # Schedule for Gr 1 to 5
    exam_str_g15 = db.Column(db.Integer)  # Total Strength for Gr 1 to 5
    exam_att_g15 = db.Column(db.Integer)  # Attended for Gr 1 to 5
    exam_notatt_g15 = db.Column(db.Integer)  # Not Attended for Gr 1 to 5
    exam_issue_nature_g15 = db.Column(db.String(50))  # Nature of Issue for Gr 1 to 5
    exam_issue_desc_g15 = db.Column(db.Text)  # Issue Description for Gr 1 to 5
    exam_comment_g15 = db.Column(db.Text)  # Comments for Gr 1 to 5

    exam_schedule_g68 = db.Column(db.String(100))  # Schedule for Gr 6 to 8
    exam_str_g68 = db.Column(db.Integer)  # Total Strength for Gr 6 to 8
    exam_att_g68 = db.Column(db.Integer)  # Attended for Gr 6 to 8
    exam_notatt_g68 = db.Column(db.Integer)  # Not Attended for Gr 6 to 8
    exam_issue_nature_g68 = db.Column(db.String(50))  # Nature of Issue for Gr 6 to 8
    exam_issue_desc_g68 = db.Column(db.Text)  # Issue Description for Gr 6 to 8
    exam_comment_g68 = db.Column(db.Text)  # Comments for Gr 6 to 8

    exam_schedule_g910 = db.Column(db.String(100))  # Schedule for Gr 9 and 10
    exam_str_g910 = db.Column(db.Integer)  # Total Strength for Gr 9 and 10
    exam_att_g910 = db.Column(db.Integer)  # Attended for Gr 9 and 10
    exam_notatt_g910 = db.Column(db.Integer)  # Not Attended for Gr 9 and 10
    exam_issue_nature_g910 = db.Column(db.String(50))  # Nature of Issue for Gr 9 and 10
    exam_issue_desc_g910 = db.Column(db.Text)  # Issue Description for Gr 9 and 10
    exam_comment_g910 = db.Column(db.Text)  # Comments for Gr 9 and 10

    exam_schedule_g11 = db.Column(db.String(100))  # Schedule for Gr 11
    exam_str_g11 = db.Column(db.Integer)  # Total Strength for Gr 11
    exam_att_g11 = db.Column(db.Integer)  # Attended for Gr 11
    exam_notatt_g11 = db.Column(db.Integer)  # Not Attended for Gr 11
    exam_issue_nature_g11 = db.Column(db.String(50))  # Nature of Issue for Gr 11
    exam_issue_desc_g11 = db.Column(db.Text)  # Issue Description for Gr 11
    exam_comment_g11 = db.Column(db.Text)  # Comments for Gr 11

    exam_schedule_g12 = db.Column(db.String(100))  # Schedule for Gr 12
    exam_str_g12 = db.Column(db.Integer)  # Total Strength for Gr 12
    exam_att_g12 = db.Column(db.Integer)  # Attended for Gr 12
    exam_notatt_g12 = db.Column(db.Integer)  # Not Attended for Gr 12
    exam_issue_nature_g12 = db.Column(db.String(50))  # Nature of Issue for Gr 12
    exam_issue_desc_g12 = db.Column(db.Text)  # Issue Description for Gr 12
    exam_comment_g12 = db.Column(db.Text)  # Comments for Gr 12

    # Relationships
    submitter = db.relationship('User', foreign_keys='Team1ExamSchedule.submitted_by', backref=db.backref('submitted_team1_exam_schedule', lazy=True))

#S.No 11: External Agency Info


# S.No 11: External Agency Info
class Team1ExternalInfo(BaseForm):
    __tablename__ = 'team1_external_info'
    
    # Common fields
    external_info_work_activity = db.Column(db.String(100), default='External Info')  # Work Activity
    
    # CIS
    ext_mode_receiving_cis = db.Column(db.String(50))  # Mode Receiving for CIS
    ext_mode_sending_cis = db.Column(db.String(50))  # Mode Sending for CIS
    ext_subj_cis = db.Column(db.String(255))  # Subject for CIS
    ext_from_cis = db.Column(db.String(255))  # From for CIS
    ext_to_cis = db.Column(db.String(255))  # To for CIS
    ext_issue_nature_cis = db.Column(db.String(50))  # Nature of Issue for CIS
    ext_issue_desc_cis = db.Column(db.Text)  # Issue Description for CIS
    ext_comment_cis = db.Column(db.Text)  # Comments for CIS
    
    # CBSE
    ext_mode_receiving_cbse = db.Column(db.String(50))  # Mode Receiving for CBSE
    ext_mode_sending_cbse = db.Column(db.String(50))  # Mode Sending for CBSE
    ext_subj_cbse = db.Column(db.String(255))  # Subject for CBSE
    ext_from_cbse = db.Column(db.String(255))  # From for CBSE
    ext_to_cbse = db.Column(db.String(255))  # To for CBSE
    ext_issue_nature_cbse = db.Column(db.String(50))  # Nature of Issue for CBSE
    ext_issue_desc_cbse = db.Column(db.Text)  # Issue Description for CBSE
    ext_comment_cbse = db.Column(db.Text)  # Comments for CBSE
    
    # CEO/State Government
    ext_mode_receiving_state = db.Column(db.String(50))  # Mode Receiving for State Gov
    ext_mode_sending_state = db.Column(db.String(50))  # Mode Sending for State Gov
    ext_subj_state = db.Column(db.String(255))  # Subject for State Gov
    ext_from_state = db.Column(db.String(255))  # From for State Gov
    ext_to_state = db.Column(db.String(255))  # To for State Gov
    ext_issue_nature_state = db.Column(db.String(50))  # Nature of Issue for State Gov
    ext_issue_desc_state = db.Column(db.Text)  # Issue Description for State Gov
    ext_comment_state = db.Column(db.Text)  # Comments for State Gov
    
    # EMIS
    ext_mode_receiving_emis = db.Column(db.String(50))  # Mode Receiving for EMIS
    ext_mode_sending_emis = db.Column(db.String(50))  # Mode Sending for EMIS
    ext_subj_emis = db.Column(db.String(255))  # Subject for EMIS
    ext_from_emis = db.Column(db.String(255))  # From for EMIS
    ext_to_emis = db.Column(db.String(255))  # To for EMIS
    ext_issue_nature_emis = db.Column(db.String(50))  # Nature of Issue for EMIS
    ext_issue_desc_emis = db.Column(db.Text)  # Issue Description for EMIS
    ext_comment_emis = db.Column(db.Text)  # Comments for EMIS
    
    # Relationships
    submitter = db.relationship('User', foreign_keys='Team1ExternalInfo.submitted_by', backref=db.backref('submitted_team1_external_info', lazy=True))

# S.No 12: Sick Bay

class Team1SickBay(BaseForm):
    __tablename__ = 'team1_sick_bay'
    
    # Common fields
    sick_bay_work_activity = db.Column(db.String(100), default='Health Room')  # Work Activity
    sick_bay_dept_cat = db.Column(db.String(100), default='Students')  # Department/Category
    
    # Student information
    sick_grade = db.Column(db.String(20))  # Grade
    sick_name = db.Column(db.String(255))  # Student Name
    sick_illness = db.Column(db.String(255))  # Illness
    sick_inf_by = db.Column(db.String(255))  # Informed By
    sick_inf_to = db.Column(db.String(255))  # Informed to PRM
    sick_issue_nature = db.Column(db.String(50))  # Nature of Issue
    sick_issue_desc = db.Column(db.Text)  # Issue Description
    sick_comment = db.Column(db.Text)  # Comments
    
    # Relationships
    submitter = db.relationship('User', foreign_keys='Team1SickBay.submitted_by', backref=db.backref('submitted_team1_sick_bay', lazy=True))

#S.No 13: Home School Communications 

class Team1HomeSchoolComm(BaseForm):
    __tablename__ = 'team1_home_school_comm'
    
    # Common fields
    hsc_work_activity = db.Column(db.String(100), default='Home School Communication')  # Work Activity
    hsc_dept_cat = db.Column(db.String(100), default='MLM')  # Department/Category
    
    # Home School Communication details
    hsc_grade = db.Column(db.String(20))  # Grade
    hsc_plan = db.Column(db.String(50))  # Planned/Unplanned
    hsc_print_date = db.Column(db.Date)  # Printed Date
    hsc_dist_date = db.Column(db.Date)  # Distributed Date
    hsc_activity = db.Column(db.String(255))  # Activity/Event
    hsc_status = db.Column(db.String(50))  # Status
    hsc_issue_nature = db.Column(db.String(50))  # Nature of Issue
    hsc_issue_desc = db.Column(db.Text)  # Issue Description
    hsc_comment = db.Column(db.Text)  # Comments
    
    # Relationships
    submitter = db.relationship('User', foreign_keys='Team1HomeSchoolComm.submitted_by', backref=db.backref('submitted_team1_home_school_comm', lazy=True))

#S.No 14: Disciplinary Measures
class Team1Disciplinary(BaseForm):
    __tablename__ = 'team1_disciplinary'
    
    # Common fields
    disc_work_activity = db.Column(db.String(100), default='Disciplinary')  # Work Activity
    disc_dept_cat = db.Column(db.String(100), default='MLM')  # Department/Category
    
    # Disciplinary details
    disc_grade = db.Column(db.String(20))  # Grade
    disc_name = db.Column(db.String(255))  # Student Name
    disc_issue = db.Column(db.Text)  # Issue
    disc_action = db.Column(db.Text)  # Action Taken
    disc_issue_nature = db.Column(db.String(50))  # Nature of Issue
    disc_issue_desc = db.Column(db.Text)  # Issue Description
    disc_comment = db.Column(db.Text)  # Comments
    
    # Relationships
    submitter = db.relationship('User', foreign_keys='Team1Disciplinary.submitted_by', backref=db.backref('submitted_team1_disciplinary', lazy=True))

# S.No 15: Logistics 

class Team1Logistics(BaseForm):
    __tablename__ = 'team1_logistics'
    
    # Common fields
    log_work_activity = db.Column(db.String(100), default='Logistics')  # Work Activity
    log_dept_cat = db.Column(db.String(100), default='Logistics Team')  # Department/Category
    
    # Logistics details
    log_in_mat = db.Column(db.String(255))  # Materials Inward - Material
    log_in_qty = db.Column(db.Integer)  # Materials Inward - Qty
    log_out_mat = db.Column(db.String(255))  # Materials Outward - Material
    log_out_qty = db.Column(db.Integer)  # Materials Outward - Qty
    log_sale_qty = db.Column(db.Integer)  # Additional Sales - Qty
    log_sale_mat = db.Column(db.String(255))  # Additional Sales - Material
    log_issue_nature = db.Column(db.String(50))  # Nature of Issue
    log_issue_desc = db.Column(db.Text)  # Issue Description
    log_comment = db.Column(db.Text)  # Comments
    
    # Relationships
    submitter = db.relationship('User', foreign_keys='Team1Logistics.submitted_by', backref=db.backref('submitted_team1_logistics', lazy=True))

#S.No 16: Intra Grade Competition Certificate

class Team1CompetitionCert(BaseForm):
    __tablename__ = 'team1_competition_cert'
    
    # Common fields
    cert_work_activity = db.Column(db.String(100), default='Competition Cert')  # Work Activity
    cert_dept_cat = db.Column(db.String(100), default='Certificates Team')  # Department/Category
    
    # Competition Certificate details
    cert_grade = db.Column(db.String(20))  # Grade
    cert_activity = db.Column(db.String(255))  # Activity
    cert_date = db.Column(db.Date)  # Activity Date
    cert_no = db.Column(db.Integer)  # No. of Certificates
    cert_status = db.Column(db.String(100))  # Distribution Status
    cert_issue_nature = db.Column(db.String(50))  # Nature of Issue
    cert_issue_desc = db.Column(db.Text)  # Issue Description
    cert_comment = db.Column(db.Text)  # Comments
    
    # Relationships
    submitter = db.relationship('User', foreign_keys='Team1CompetitionCert.submitted_by', backref=db.backref('submitted_team1_competition_cert', lazy=True))

#S.No 17: Staff Concern
class Team1StaffConcern(BaseForm):
    __tablename__ = 'team1_staff_concern'
    
    # Common fields
    sc_work_activity = db.Column(db.String(100), default='Staff Concern')  # Work Activity
    sc_cat = db.Column(db.String(100))  # Department/Category
    
    # Staff Concern details
    sc_name = db.Column(db.String(255))  # Name
    sc_dept = db.Column(db.String(100))  # Department
    sc_incharge = db.Column(db.String(255))  # Incharges Handled
    sc_issue_nature = db.Column(db.String(50))  # Nature of Issue
    sc_issue_desc = db.Column(db.Text)  # Issue Description
    sc_comment = db.Column(db.Text)  # Comments
    
    # Relationships
    submitter = db.relationship('User', foreign_keys='Team1StaffConcern.submitted_by', backref=db.backref('submitted_team1_staff_concern', lazy=True))

#S.No 17b: Student Concern
class Team1StudentConcern(BaseForm):
    __tablename__ = 'team1_student_concern'
    
    # Common fields
    st_work_activity = db.Column(db.String(100), default='Student Concern')  # Work Activity
    st_cat = db.Column(db.String(100))  # Department/Category
    
    # Student Concern details
    st_name = db.Column(db.String(255))  # Student Name
    st_class = db.Column(db.String(100))  # Class/Section
    st_incharge = db.Column(db.String(255))  # Incharges Handled
    st_issue_nature = db.Column(db.String(50))  # Nature of Issue
    st_issue_desc = db.Column(db.Text)  # Issue Description
    st_comment = db.Column(db.Text)  # Comments
    
    # Relationships
    submitter = db.relationship('User', foreign_keys='Team1StudentConcern.submitted_by', backref=db.backref('submitted_team1_student_concern', lazy=True))


#S.No 18: Parent Concern
class Team1ParentConcern(BaseForm):
    __tablename__ = 'team1_parent_concern'

    pc_work_activity = db.Column(db.String(100), default='Parent Concern')
    pc_cat = db.Column(db.String(100))
    pc_summary_no = db.Column(db.Integer)
    pc_summary_closed = db.Column(db.Integer)
    pc_summary_loop13 = db.Column(db.Integer)
    pc_summary_loop3plus = db.Column(db.Integer)
    pc_summary_issue_nature = db.Column(db.String(50))
    pc_summary_issue_desc = db.Column(db.Text)
    pc_summary_comment = db.Column(db.Text)

    submitter = db.relationship('User', foreign_keys='Team1ParentConcern.submitted_by',
                                backref=db.backref('submitted_team1_parent_concern', lazy=True))

#S.No 18b: Parent Concern Detail
class Team1ParentConcernDetail(BaseForm):
    __tablename__ = 'team1_parent_concern_detail'

    pc_work_activity = db.Column(db.String(100), default='Parent Concern Detail')
    pc_detail_name = db.Column(db.String(255))
    pc_detail_grade = db.Column(db.String(20))
    pc_detail_concern = db.Column(db.Text)
    pc_detail_incharge = db.Column(db.String(255))
    pc_detail_issue_nature = db.Column(db.String(50))
    pc_detail_comment = db.Column(db.Text)


    submitter = db.relationship('User', foreign_keys='Team1ParentConcernDetail.submitted_by',
                                backref=db.backref('submitted_team1_parent_concern_detail', lazy=True))


#S.No 19: AEP Attendance


class Team1AEPAttendance(BaseForm):
    __tablename__ = 'team1_aep_attendance'

    #work activity
    aep_work_activity = db.Column(db.String(100), default='AEP Attendance')  # Work Activity
    
    # Grade 11 AEP Attendance   
    aep_str_g11 = db.Column(db.Integer)  # Strength
    aep_enr_g11 = db.Column(db.Integer)  # Enrolled
    aep_enrpct_g11 = db.Column(db.Float)  # % Enrollment
    aep_prog_g11 = db.Column(db.String(255))  # Programmes/Subjects
    aep_exp_g11 = db.Column(db.Integer)  # Expected
    aep_att_g11 = db.Column(db.Integer)  # Attended
    aep_attpct_g11 = db.Column(db.Float)  # % Attendance
    
    # Grade 12 AEP Attendance  
    aep_str_g12 = db.Column(db.Integer)  # Strength 
    aep_enr_g12 = db.Column(db.Integer)  # Enrolled
    aep_enrpct_g12 = db.Column(db.Float)  # % Enrollment
    aep_prog_g12 = db.Column(db.String(255))  # Programmes/Subjects
    aep_exp_g12 = db.Column(db.Integer)  # Expected
    aep_att_g12 = db.Column(db.Integer)  # Attended
    aep_attpct_g12 = db.Column(db.Float)  # % Attendance
    
    # Relationships
    submitter = db.relationship('User', foreign_keys='Team1AEPAttendance.submitted_by', backref=db.backref('submitted_team1_aep_attendance', lazy=True))

# S.No 20: Extended Class Attendance

class Team1ExtendedClassAttendance(BaseForm):
    __tablename__ = 'team1_extended_class_attendance'
    
    # Work Activity
    ec_work_activity = db.Column(db.String(100), default='Extended Class Attendance')  # Work Activity
    
    # Grades 3 to 5 Extended Class Attendance
    ec_grade_35 = db.Column(db.String(20), default='3 to 5')  # Grade/Group
    ec_str_g35 = db.Column(db.Integer)  # Strength
    ec_enr_g35 = db.Column(db.Integer)  # Enrolled
    ec_enrpct_g35 = db.Column(db.Float)  # % Enrollment
    ec_subj_g35 = db.Column(db.String(255))  # Programmes/Subjects
    ec_exp_g35 = db.Column(db.Integer)  # Expected
    ec_att_g35 = db.Column(db.Integer)  # Attended
    ec_attpct_g35 = db.Column(db.Float)  # % Attendance
    
    # Grades 6 to 8 Extended Class Attendance
    ec_grade_68 = db.Column(db.String(20), default='6 to 8')  # Grade/Group
    ec_str_g68 = db.Column(db.Integer)  # Strength
    ec_enr_g68 = db.Column(db.Integer)  # Enrolled
    ec_enrpct_g68 = db.Column(db.Float)  # % Enrollment
    ec_subj_g68 = db.Column(db.String(255))  # Programmes/Subjects
    ec_exp_g68 = db.Column(db.Integer)  # Expected
    ec_att_g68 = db.Column(db.Integer)  # Attended
    ec_attpct_g68 = db.Column(db.Float)  # % Attendance
    
    # Grades 9 and 10 Extended Class Attendance
    ec_grade_910 = db.Column(db.String(20), default='9 and 10')  # Grade/Group
    ec_str_g910 = db.Column(db.Integer)  # Strength
    ec_enr_g910 = db.Column(db.Integer)  # Enrolled
    ec_enrpct_g910 = db.Column(db.Float)  # % Enrollment
    ec_subj_g910 = db.Column(db.String(255))  # Programmes/Subjects
    ec_exp_g910 = db.Column(db.Integer)  # Expected
    ec_att_g910 = db.Column(db.Integer)  # Attended
    ec_attpct_g910 = db.Column(db.Float)  # % Attendance
    
    # Grades 11 and 12 Extended Class Attendance
    ec_grade_1112 = db.Column(db.String(20), default='11 and 12')  # Grade/Group
    ec_str_g1112 = db.Column(db.Integer)  # Strength
    ec_enr_g1112 = db.Column(db.Integer)  # Enrolled
    ec_enrpct_g1112 = db.Column(db.Float)  # % Enrollment
    ec_subj_g1112 = db.Column(db.String(255))  # Programmes/Subjects
    ec_exp_g1112 = db.Column(db.Integer)  # Expected
    ec_att_g1112 = db.Column(db.Integer)  # Attended
    ec_attpct_g1112 = db.Column(db.Float)  # % Attendance
    
    # Relationships
    submitter = db.relationship('User', foreign_keys='Team1ExtendedClassAttendance.submitted_by', backref=db.backref('submitted_team1_extended_class_attendance', lazy=True))


#S.No 21: Training Session
class Team1TrainingSession(BaseForm):
    __tablename__ = 'team1_training_session'
    
    # Work Activity
    train_work_activity = db.Column(db.String(100), default='Training Session')  # Work Activity
    
    # Training Session Details
    train_teacher = db.Column(db.String(255))  # Teacher Name
    train_topic = db.Column(db.String(255))  # Topic
    train_by = db.Column(db.String(255))  # Conducted by
    train_mode = db.Column(db.String(20))  # In Person/Online
    train_duration = db.Column(db.String(50))  # Duration
    train_report = db.Column(db.String(255))  # Report Shared
    train_participants = db.Column(db.Integer)  # No. Participants
    
    # Relationships
    submitter = db.relationship('User', foreign_keys='Team1TrainingSession.submitted_by', backref=db.backref('submitted_team1_training_session', lazy=True))

#S.No 22: Team Weekly Meeting
class Team1WeeklyMeeting(BaseForm):
    __tablename__ = 'team1_weekly_meeting'
    
    # Work Activity
    meet_work_activity = db.Column(db.String(100), default='Weekly Meeting')  # Work Activity
    
    # Weekly Meeting Details for different grades
    meet_grade_kg = db.Column(db.String(20), default='KG')  # Grade/Group
    meet_head_kg = db.Column(db.String(255))  # Headed by
    meet_agenda_kg = db.Column(db.Text)  # Agenda
    meet_str_kg = db.Column(db.Integer)  # Actual Strength
    meet_att_kg = db.Column(db.Integer)  # Attended
    meet_attpct_kg = db.Column(db.Float)  # % Attendance

    meet_grade_12 = db.Column(db.String(20), default='1 and 2')  # Grade/Group
    meet_head_12 = db.Column(db.String(255))  # Headed by
    meet_agenda_12 = db.Column(db.Text)  # Agenda
    meet_str_12 = db.Column(db.Integer)  # Actual Strength
    meet_att_12 = db.Column(db.Integer)  # Attended
    meet_attpct_12 = db.Column(db.Float)  # % Attendance

    meet_grade_35 = db.Column(db.String(20), default='3 to 5')  # Grade/Group
    meet_head_35 = db.Column(db.String(255))  # Headed by
    meet_agenda_35 = db.Column(db.Text)  # Agenda
    meet_str_35 = db.Column(db.Integer)  # Actual Strength
    meet_att_35 = db.Column(db.Integer)  # Attended
    meet_attpct_35 = db.Column(db.Float)  # % Attendance

    meet_grade_68 = db.Column(db.String(20), default='6 to 8')  # Grade/Group
    meet_head_68 = db.Column(db.String(255))  # Headed by
    meet_agenda_68 = db.Column(db.Text)  # Agenda
    meet_str_68 = db.Column(db.Integer)  # Actual Strength
    meet_att_68 = db.Column(db.Integer)  # Attended
    meet_attpct_68 = db.Column(db.Float)  # % Attendance

    meet_grade_910 = db.Column(db.String(20), default='9 and 10')  # Grade/Group
    meet_head_910 = db.Column(db.String(255))  # Headed by
    meet_agenda_910 = db.Column(db.Text)  # Agenda
    meet_str_910 = db.Column(db.Integer)  # Actual Strength
    meet_att_910 = db.Column(db.Integer)  # Attended
    meet_attpct_910 = db.Column(db.Float)  # % Attendance

    meet_grade_1112 = db.Column(db.String(20), default='11 and 12')  # Grade/Group
    meet_head_1112 = db.Column(db.String(255))  # Headed by
    meet_agenda_1112 = db.Column(db.Text)  # Agenda
    meet_str_1112 = db.Column(db.Integer)  # Actual Strength
    meet_att_1112 = db.Column(db.Integer)  # Attended
    meet_attpct_1112 = db.Column(db.Float)  # % Attendance
    
    # Relationships
    submitter = db.relationship('User', foreign_keys='Team1WeeklyMeeting.submitted_by', backref=db.backref('submitted_team1_weekly_meeting', lazy=True))

#S.No 23: Special Education
class Team1SpecialEducation(BaseForm):
    __tablename__ = 'team1_special_education'

    # Fields based on your HTML form
    class_name = db.Column(db.String(255))                # e.g., Children with special needs
    total_students = db.Column(db.Integer)               # Total No. Students
    as_on_date = db.Column(db.Date)                      # Date
    attended = db.Column(db.Integer)                     # Attended count
    not_attended = db.Column(db.Integer)                 # Not attended count
    nature_of_issue = db.Column(db.String(50))           # Critical / Manageable / All Well
    observations = db.Column(db.Text)                    # New joinee / assessment / observation
    issue_description = db.Column(db.Text)               # Issue description
    comments = db.Column(db.Text)                        # Comments
    schedule = db.Column(db.String(100))                 # Pre-filled schedule

    # Relationships for submitter and team info
    submitter = db.relationship('User', foreign_keys='Team1SpecialEducation.submitted_by',
                                backref=db.backref('submitted_team1_special_education', lazy=True))
    
# S.No 24: Hostel
class Team1Hostel(BaseForm):
    __tablename__ = 'team1_hostel'

    # Fields based on your HTML form
    hostel_students = db.Column(db.String(255))         # No. of Students or Name/Count
    hostel_payment = db.Column(db.String(50))           # Payment Status (Paid/Pending/Partial)
    hostel_food_concern = db.Column(db.Text)            # Food Concern
    hostel_general_concern = db.Column(db.Text)         # General Concern

    # Relationships for submitter and team info
    submitter = db.relationship('User', foreign_keys='Team1Hostel.submitted_by',
                                 backref=db.backref('submitted_team1_hostel', lazy=True))


# S.No 25: SEC
class Team1SEC(BaseForm):
    __tablename__ = 'team1_sec'

    sec_committee = db.Column(db.String(255))        # Committee Name
    sec_schedule = db.Column(db.Date)                # Schedule Date
    sec_meeting_status = db.Column(db.String(50))    # Meeting Status (Conducted / Not Conducted / Postponed)
    sec_md_mom_review = db.Column(db.Text)           # MD MOM Review
    sec_next_meeting = db.Column(db.Date)            # Next Meeting Date
    sec_atr_completion_status = db.Column(db.String(50))  # ATR Completion Status (Completed / Pending / In Progress)

    # Relationships for submitter and team info
    submitter = db.relationship(
        'User',
        foreign_keys='Team1SEC.submitted_by',
        backref=db.backref('submitted_team1_sec', lazy=True)
    )


# S.No 26: School Counsellor Tracking
class Team1SchoolCounsellor(BaseForm):
    __tablename__ = 'team1_school_counsellor'

    # Fields from the HTML form
    rapid_category = db.Column(db.String(50))          # KK or Others
    rapid_subtopic = db.Column(db.String(100))         # Subtopic like Gadgets, Family, etc.
    rapid_total_issues = db.Column(db.String(50))      # Total number of issues (Text or Number)
    rapid_met_so_far = db.Column(db.String(50))        # Meetings done so far
    rapid_pending = db.Column(db.String(50))           # Pending count/text
    rapid_follow_up = db.Column(db.String(50))         # Follow up details
    rapid_issue_closed = db.Column(db.Date)            # Issue Closed Date
    rapid_critical = db.Column(db.String(50))          # Critical count
    rapid_manageable = db.Column(db.String(50))        # Manageable count
    rapid_issue_categories = db.Column(db.String(255)) # Issue categories text
    rapid_nature_of_issues = db.Column(db.String(50))  # All Well / Manageable / Critical
    rapid_count = db.Column(db.String(50))             # Count
    rapid_duration = db.Column(db.String(50))          # Duration (text)
    rapid_comments = db.Column(db.Text)                # Comments / Name / Grade / Issues

    # Relationships for submitter and team info
    submitter = db.relationship('User', foreign_keys='Team1SchoolCounsellor.submitted_by',
                                 backref=db.backref('submitted_school_counsellor', lazy=True))
    
    # S.No 26: Scholorius / Smart Tail
class Team1Scholorius(BaseForm):
    __tablename__ = 'team1_scholorius'

    scholorius_program = db.Column(db.String(255))      # Program Name
    scholorius_date = db.Column(db.Date)                # Program Date
    scholorius_status = db.Column(db.String(50))        # Status (Completed / Pending / Rescheduled)
    scholorius_remark = db.Column(db.Text)              # Remarks

    # Relationships for submitter and team info
    submitter = db.relationship('User', foreign_keys='Team1Scholorius.submitted_by',
                                backref=db.backref('submitted_team1_scholorius', lazy=True))



# Team 2 Form Models

# team 2: 1 a HR Attendance
class Team2HRAttendance(BaseForm):
    __tablename__ = 'team2_hr_attendance'
    
    # Jr. School
    hr_att_jr_school_total = db.Column(db.Integer)
    hr_att_jr_school_present = db.Column(db.Integer)
    hr_att_jr_school_leave = db.Column(db.Integer)
    hr_att_jr_school_leave_perc = db.Column(db.Float)
    hr_att_jr_school_nature = db.Column(db.String(50))
    hr_att_jr_school_issue_desc = db.Column(db.Text)
    hr_att_jr_school_comments = db.Column(db.Text)

    # Sr. School
    hr_att_sr_school_total = db.Column(db.Integer)
    hr_att_sr_school_present = db.Column(db.Integer)
    hr_att_sr_school_leave = db.Column(db.Integer)
    hr_att_sr_school_leave_perc = db.Column(db.Float)
    hr_att_sr_school_nature = db.Column(db.String(50))
    hr_att_sr_school_issue_desc = db.Column(db.Text)
    hr_att_sr_school_comments = db.Column(db.Text)

    # ECA
    hr_att_eca_total = db.Column(db.Integer)
    hr_att_eca_present = db.Column(db.Integer)
    hr_att_eca_leave = db.Column(db.Integer)
    hr_att_eca_leave_perc = db.Column(db.Float)
    hr_att_eca_nature = db.Column(db.String(50))
    hr_att_eca_issue_desc = db.Column(db.Text)
    hr_att_eca_comments = db.Column(db.Text)

    # Academics Overall
    hr_att_acad_overall_total = db.Column(db.Integer)
    hr_att_acad_overall_present = db.Column(db.Integer)
    hr_att_acad_overall_leave = db.Column(db.Integer)
    hr_att_acad_overall_leave_perc = db.Column(db.Float)
    
    # Relationships
    submitter = db.relationship('User', foreign_keys='Team2HRAttendance.submitted_by', backref=db.backref('submitted_team2_hr_attendance', lazy=True))

# team 2: 1 b Admin Attendance
class Team2AdminAttendance(BaseForm):
    __tablename__ = 'team2_admin_attendance'
    
    # Admin Staff
    hr_att_admin_total = db.Column(db.Integer)
    hr_att_admin_present = db.Column(db.Integer)
    hr_att_admin_leave = db.Column(db.Integer)
    hr_att_admin_leave_perc = db.Column(db.Float)
    hr_att_admin_nature = db.Column(db.String(50))
    hr_att_admin_issue_desc = db.Column(db.Text)
    hr_att_admin_comments = db.Column(db.Text)

    # Drivers
    hr_att_drivers_total = db.Column(db.Integer)
    hr_att_drivers_present = db.Column(db.Integer)
    hr_att_drivers_leave = db.Column(db.Integer)
    hr_att_drivers_leave_perc = db.Column(db.Float)
    hr_att_drivers_nature = db.Column(db.String(50))
    hr_att_drivers_issue_desc = db.Column(db.Text)
    hr_att_drivers_comments = db.Column(db.Text)

    # Securities
    hr_att_sec_total = db.Column(db.Integer)
    hr_att_sec_present = db.Column(db.Integer)
    hr_att_sec_leave = db.Column(db.Integer)
    hr_att_sec_leave_perc = db.Column(db.Float)
    hr_att_sec_nature = db.Column(db.String(50))
    hr_att_sec_issue_desc = db.Column(db.Text)
    hr_att_sec_comments = db.Column(db.Text)

    # Housekeeping
    hr_att_hk_total = db.Column(db.Integer)
    hr_att_hk_present = db.Column(db.Integer)
    hr_att_hk_leave = db.Column(db.Integer)
    hr_att_hk_leave_perc = db.Column(db.Float)
    hr_att_hk_nature = db.Column(db.String(50))
    hr_att_hk_issue_desc = db.Column(db.Text)
    hr_att_hk_comments = db.Column(db.Text)

    # Conductors
    hr_att_cond_total = db.Column(db.Integer)
    hr_att_cond_present = db.Column(db.Integer)
    hr_att_cond_leave = db.Column(db.Integer)
    hr_att_cond_leave_perc = db.Column(db.Float)
    hr_att_cond_nature = db.Column(db.String(50))
    hr_att_cond_issue_desc = db.Column(db.Text)
    hr_att_cond_comments = db.Column(db.Text)

    # Admin Overall
    hr_att_admin_overall_total = db.Column(db.Integer)
    hr_att_admin_overall_present = db.Column(db.Integer)
    hr_att_admin_overall_leave = db.Column(db.Integer)
    hr_att_admin_overall_leave_perc = db.Column(db.Float)
    
    # Relationships
    submitter = db.relationship('User', foreign_keys='Team2AdminAttendance.submitted_by', backref=db.backref('submitted_team2_admin_attendance', lazy=True))

# team 2: 1 d Total HR Attendance
class Team2TotalHRAttendance(BaseForm):
    __tablename__ = 'team2_total_hr_attendance'

    # Fields
    category = db.Column(db.String(100), default="HR Overall Attendance")  # Static category name
    total = db.Column(db.Integer, nullable=False, default=0)
    present = db.Column(db.Integer, nullable=False, default=0)
    leave = db.Column(db.Integer, nullable=False, default=0)
    leave_perc = db.Column(db.Float, nullable=True)  # Auto-calculated
    nature_of_issue = db.Column(db.String(50), nullable=True)  # All Well / Manageable / Critical
    issue_description = db.Column(db.Text, nullable=True)
    comments = db.Column(db.Text, nullable=True)

    # Relationships
    submitter = db.relationship('User', foreign_keys='Team2TotalHRAttendance.submitted_by',
                                 backref=db.backref('submitted_team2_total_hr_attendance', lazy=True))

# team 2: 2a Recruitment Activity
class Team2RecruitmentActivity(BaseForm):
    __tablename__ = 'team2_recruitment_activity'
    
    # Academics
    rec_act_acad_vac_nos = db.Column(db.Integer)
    rec_act_acad_pos = db.Column(db.Text)
    rec_act_acad_update = db.Column(db.Text)
    rec_act_acad_nature = db.Column(db.String(50))
    rec_act_acad_issue_desc = db.Column(db.Text)
    rec_act_acad_comments = db.Column(db.Text)

    # Admin
    rec_act_admin_vac_nos = db.Column(db.Integer)
    rec_act_admin_pos = db.Column(db.Text)
    rec_act_admin_update = db.Column(db.Text)
    rec_act_admin_nature = db.Column(db.String(50))
    rec_act_admin_issue_desc = db.Column(db.Text)
    rec_act_admin_comments = db.Column(db.Text)
    
    # Relationships
    submitter = db.relationship('User', foreign_keys='Team2RecruitmentActivity.submitted_by', backref=db.backref('submitted_team2_recruitment_activity', lazy=True))

# team 2: 2b Pending Recruitment
class Team2PendingRecruitment(BaseForm):
    __tablename__ = 'team2_pending_recruitment'
    
    # Academics
    rec_pend_acad_count = db.Column(db.Integer)
    rec_pend_acad_pos = db.Column(db.Text)
    rec_pend_acad_closure = db.Column(db.Date)
    rec_pend_acad_nature = db.Column(db.String(50))
    rec_pend_acad_issue_desc = db.Column(db.Text)
    rec_pend_acad_comments = db.Column(db.Text)

    # Admin
    rec_pend_admin_count = db.Column(db.Integer)
    rec_pend_admin_pos = db.Column(db.Text)
    rec_pend_admin_closure = db.Column(db.Date)
    rec_pend_admin_nature = db.Column(db.String(50))
    rec_pend_admin_issue_desc = db.Column(db.Text)
    rec_pend_admin_comments = db.Column(db.Text)
    
    # Relationships
    submitter = db.relationship('User', foreign_keys='Team2PendingRecruitment.submitted_by', backref=db.backref('submitted_team2_pending_recruitment', lazy=True))
# team 2: Recruitment Pipeline
class Team2RecruitmentPipeline(BaseForm):
    __tablename__ = 'team2_recruitment_pipeline'


    category = db.Column(db.String(50), nullable=False)  # 'Academic' or 'Non-Academic'
    position = db.Column(db.String(200))
    hired = db.Column(db.String(200))
    shortlisted = db.Column(db.String(200))

    # Relationships
    submitter = db.relationship(
        'User',
        foreign_keys='Team2RecruitmentPipeline.submitted_by',
        backref=db.backref('submitted_team2_recruitment_pipeline', lazy=True)
    )

# team 2: 2d Staff Status Updates
class Team2StaffStatusUpdates(BaseForm):
    __tablename__ = 'team2_staff_status_updates'

    # Members under Observation
    obs_name = db.Column(db.String(100), nullable=False)  # Name of the Member under Observation
    obs_dept = db.Column(db.String(100), nullable=True)   # Department
    obs_desig = db.Column(db.String(100), nullable=True)  # Designation
    obs_doj = db.Column(db.Date, nullable=True)           # Date of Joining
    obs_shadow = db.Column(db.String(100), nullable=True) # Shadow Staff
    obs_completed = db.Column(db.Date, nullable=True)     # Observation Completed Date
    obs_comments = db.Column(db.Text, nullable=True)      # Comments
    
    # Relationships
    submitter = db.relationship('User', foreign_keys='Team2StaffStatusUpdates.submitted_by', backref=db.backref('submitted_team2_staff_status_updates', lazy=True))

# team 2: 2e Salary Pending
class Team2SalaryPending(BaseForm):
    __tablename__ = 'team2_salary_pending'

    sal_pend_name = db.Column(db.String(100), nullable=True)      # Name of Member
    sal_pend_dept = db.Column(db.String(100), nullable=True)      # Department
    sal_pend_desig = db.Column(db.String(100), nullable=True)     # Designation
    sal_pend_comments = db.Column(db.Text, nullable=True)         # Reason/Comments

    # Relationships
    submitter = db.relationship(
        'User',
        foreign_keys='Team2SalaryPending.submitted_by',
        backref=db.backref('submitted_team2_salary_pending', lazy=True)
    )

# team 2: 2f Police Verification
class Team2PoliceVerification(BaseForm):
    __tablename__ = 'team2_police_verification'

    department = db.Column(db.String(100), nullable=True)       # Department
    strength = db.Column(db.Integer, nullable=True)             # Strength
    completed = db.Column(db.Text, nullable=True)               # Completed names & count
    pending = db.Column(db.Text, nullable=True)                 # Pending names & count
    remarks = db.Column(db.Text, nullable=True)                  # Remarks

    # Relationships
    submitter = db.relationship('User', foreign_keys='Team2PoliceVerification.submitted_by',
                                 backref=db.backref('submitted_police_verifications', lazy=True))

# team 2: 3 Interview Schedule
class Team2InterviewSchedule(BaseForm):
    __tablename__ = 'team2_interview_schedule'

    department_category = db.Column(db.String(100), nullable=False)  # Dropdown value
    candidate_count = db.Column(db.Integer, nullable=True)  # No. of Candidates
    interview_completion = db.Column(db.String(100), nullable=True)  # First Phase Completion
    interview_status = db.Column(db.String(100), nullable=True)  # Shortlisted / Waiting / Rejected
    nature_of_issue = db.Column(db.String(100), nullable=True)  # Nature of Issue
    issue_description = db.Column(db.Text, nullable=True)  # Issue Description
    comments = db.Column(db.Text, nullable=True)  # Comments

    # BaseForm will already have team_id, submitted_by, and created_at/updated_at
    submitter = db.relationship(
        'User',
        foreign_keys='Team2InterviewSchedule.submitted_by',
        backref=db.backref('submitted_team2_interview_schedule', lazy=True)
    )

# team 2: 4 Exit 
class Team2ExitInformation(BaseForm):
    __tablename__ = 'team2_exit_information'

    exit_activity = db.Column(db.String(255), nullable=True)  # Work Activity (e.g., "Exit")
    exit_department = db.Column(db.String(100), nullable=True)  # Department / Category
    exit_notice = db.Column(db.String(100), nullable=True)  # Relieving Notice Period
    exit_name = db.Column(db.String(100), nullable=True)  # Staff Name
    exit_dept = db.Column(db.String(100), nullable=True)  # Department
    exit_reason = db.Column(db.Text, nullable=True)  # Reason
    exit_nature = db.Column(db.String(50), nullable=True)  # Nature of Issue
    exit_issue_desc = db.Column(db.Text, nullable=True)  # Issue Description
    exit_comments = db.Column(db.Text, nullable=True)  # Comments

    # Relationships
    submitter = db.relationship(
        'User',
        foreign_keys='Team2ExitInformation.submitted_by',
        backref=db.backref('submitted_team2_exit_information', lazy=True)
    )

# team 2: Issues / Staff Concerns
class Team2IssuesStaffConcerns(BaseForm):
    __tablename__ = 'team2_issues_staff_concerns'

    concern_sno = db.Column(db.String(20), nullable=True)  # S.No (e.g., 5.a)
    concern_activity = db.Column(db.String(255), nullable=True)  # Work Activity
    concern_dept = db.Column(db.String(100), nullable=True)  # Department
    concern_person = db.Column(db.String(100), nullable=True)  # Name of Person
    concern_incharge = db.Column(db.String(255), nullable=True)  # Incharges Handled
    concern_nature = db.Column(db.String(50), nullable=True)  # Nature of Issue
    concern_issue_desc = db.Column(db.Text, nullable=True)  # Issue Description
    concern_comments = db.Column(db.Text, nullable=True)  # Comments

    # Relationships
    submitter = db.relationship('User', foreign_keys='Team2IssuesStaffConcerns.submitted_by', backref=db.backref('submitted_team2_staff_concerns', lazy=True))

# team 2: 5b Kural Recitation
class Team2KuralRecitation(BaseForm):
    __tablename__ = 'team2_kural_recitation'

    # Kural Recitation
    kural_team = db.Column(db.String(100), nullable=True)  # Support Team   
    kural_name = db.Column(db.String(100), nullable=True)  # Name
    kural_happened = db.Column(db.String(10), nullable=True)  # Happened (Yes/No)
    kural_not_happened_reason = db.Column(db.Text, nullable=True)  # Not Happened - Reason
    kural_nature = db.Column(db.String(50), nullable=True)  # Nature of Issue
    kural_issue_desc = db.Column(db.Text, nullable=True)  # Issue Description
    kural_comments = db.Column(db.Text, nullable=True)  # Comments
    
    # Relationships
    submitter = db.relationship('User', foreign_keys='Team2KuralRecitation.submitted_by', backref=db.backref('submitted_team2_kural_recitation', lazy=True))

# -------------------------------
# Front Office Phone Calls Model
# -------------------------------
# team 2: 6a Front Office Phone Calls
class Team2FrontOfficePhoneCalls(BaseForm):
    __tablename__ = 'team2_front_office_phone_calls'

    category = db.Column(db.String(100), nullable=True)  # Academics/Admin/General
    incoming = db.Column(db.Text, nullable=True)
    outgoing = db.Column(db.Text, nullable=True)
    nature = db.Column(db.String(50), nullable=True)  # Critical/Manageable/All Well
    issue_description = db.Column(db.Text, nullable=True)
    comments = db.Column(db.Text, nullable=True)

    submitter = db.relationship('User', foreign_keys='Team2FrontOfficePhoneCalls.submitted_by',
                                backref=db.backref('submitted_team2_front_office_phone_calls', lazy=True))


# -------------------------------
# Visitor Log Model
# -------------------------------
# team 2: 6b Visitor Log
class Team2VisitorLog(BaseForm):
    __tablename__ = 'team2_visitor_log'

    visitor_type = db.Column(db.String(100), nullable=True)  # Parent / Office / Company
    purpose = db.Column(db.Text, nullable=True)
    person_met = db.Column(db.String(100), nullable=True)
    nature = db.Column(db.String(50), nullable=True)  # Critical/Manageable/All Well
    issue_description = db.Column(db.Text, nullable=True)
    comments = db.Column(db.Text, nullable=True)

    submitter = db.relationship('User', foreign_keys='Team2VisitorLog.submitted_by',
                                backref=db.backref('submitted_team2_visitor_logs', lazy=True))


# -------------------------------
# BSNL Phone Status Model
# -------------------------------
# team 2: 6c BSNL Phone Status
class Team2BSNLPhoneStatus(BaseForm):
    __tablename__ = 'team2_bsnl_phone_status'

    department = db.Column(db.String(100), nullable=True, default="Front Office")
    working = db.Column(db.String(20), nullable=True)  # Yes/No/Details
    not_working = db.Column(db.String(20), nullable=True)  # Yes/No/Details
    rectified = db.Column(db.String(20), nullable=True)  # Yes/No/Date
    nature = db.Column(db.String(50), nullable=True)  # Critical/Manageable/All Well
    issue_description = db.Column(db.Text, nullable=True)
    comments = db.Column(db.Text, nullable=True)

    submitter = db.relationship('User', foreign_keys='Team2BSNLPhoneStatus.submitted_by',
                                backref=db.backref('submitted_team2_bsnl_phone_status', lazy=True))
    

# -------------------------------
# Materials Inward Model
# -------------------------------
# team 2: 7a Materials Inward
class Team2MaterialsInward(BaseForm):
    __tablename__ = 'team2_materials_inward'

    sno = db.Column(db.Integer, autoincrement=True)  # Remove primary_key=True
    work_activity = db.Column(db.String(100), nullable=True)
    department_category = db.Column(db.String(100), nullable=True)
    product_material = db.Column(db.String(100), nullable=True)
    in_time = db.Column(db.Time, nullable=True)
    vendor = db.Column(db.String(100), nullable=True)
    description = db.Column(db.Text, nullable=True)
    quantity = db.Column(db.Integer, nullable=True)
    nature = db.Column(db.String(50), nullable=True)  # Critical/Manageable/All Well
    issue_description = db.Column(db.Text, nullable=True)
    comments = db.Column(db.Text, nullable=True)

    submitter = db.relationship('User', foreign_keys='Team2MaterialsInward.submitted_by',
                                backref=db.backref('submitted_team2_materials_inward', lazy=True))

# -------------------------------
# Materials Outward Model
# -------------------------------
# team 2: 7b Materials Outward
class Team2MaterialsOutward(BaseForm):
    __tablename__ = 'team2_materials_outward'

    work_activity = db.Column(db.String(100), nullable=True, default='Materials Outward')
    department = db.Column(db.String(100), nullable=True, default='Materials')
    product_material = db.Column(db.String(100), nullable=True)
    out_time = db.Column(db.Time, nullable=True)
    vendor = db.Column(db.String(100), nullable=True)
    description = db.Column(db.Text, nullable=True)
    quantity = db.Column(db.Integer, nullable=True)
    nature = db.Column(db.String(50), nullable=True)  # Critical/Manageable/All Well
    issue_description = db.Column(db.Text, nullable=True)
    comments = db.Column(db.Text, nullable=True)

    submitter = db.relationship('User', foreign_keys='Team2MaterialsOutward.submitted_by',
                                backref=db.backref('submitted_team2_materials_outward', lazy=True))

# -------------------------------
# Materials Movement Model
# -------------------------------
# team 2: 7c Materials Movement
class Team2MaterialsMovement(BaseForm):
    __tablename__ = 'team2_materials_movement'

    returnable = db.Column(db.Text, nullable=True)
    non_returnable = db.Column(db.Text, nullable=True)
    nature = db.Column(db.String(50), nullable=True)  # Critical/Manageable/All Well
    issue_description = db.Column(db.Text, nullable=True)
    comments = db.Column(db.Text, nullable=True)

    submitter = db.relationship('User', foreign_keys='Team2MaterialsMovement.submitted_by',
                                backref=db.backref('submitted_team2_materials_movement', lazy=True))

# -------------------------------
# Returnable Material Tracking Model
# -------------------------------
# team 2: 7, 2 b Returnable Material Tracking
class Team2ReturnableMaterialTracking(BaseForm):
    __tablename__ = 'team2_returnable_material_tracking'

    description = db.Column(db.Text, nullable=True)
    quantity = db.Column(db.Integer, nullable=True)
    issue_date = db.Column(db.Date, nullable=True)
    return_date = db.Column(db.Date, nullable=True)
    nature = db.Column(db.String(50), nullable=True)  # Critical/Manageable/All Well
    issue_description = db.Column(db.Text, nullable=True)
    comments = db.Column(db.Text, nullable=True)

    submitter = db.relationship('User', foreign_keys='Team2ReturnableMaterialTracking.submitted_by',
                                backref=db.backref('submitted_team2_returnable_material_tracking', lazy=True))

# team 2: 7, 2 c Returnable Goods Report
class Team2ReturnableGoodsReport(BaseForm):
    __tablename__ = 'team2_returnable_goods_report'

    description = db.Column(db.Text, nullable=True)
    quantity = db.Column(db.Integer, nullable=True)
    issue_date = db.Column(db.Date, nullable=True)
    return_date = db.Column(db.Date, nullable=True) 
    nature = db.Column(db.String(50), nullable=True)  # Critical/Manageable/All Well
    issue_description = db.Column(db.Text, nullable=True)
    comments = db.Column(db.Text, nullable=True)

    submitter = db.relationship('User', foreign_keys='Team2ReturnableGoodsReport.submitted_by',
                                backref=db.backref('submitted_team2_returnable_goods_report', lazy=True))
    
# team 2: 8 a Campus Camera Status
class Team2CampusCameraStatus(BaseForm):
    __tablename__ = 'team2_campus_camera_status'

    work_activity = db.Column(db.String(100), nullable=True, default='Camera & Monitoring')
    department = db.Column(db.String(100), nullable=True, default='Control Room')
    particulars = db.Column(db.String(100), nullable=True)
    total_cameras = db.Column(db.Integer, nullable=True)
    working_cameras = db.Column(db.Integer, nullable=True)
    not_working_details = db.Column(db.Text, nullable=True)
    nature_of_issue = db.Column(db.String(50), nullable=True)  # Critical/Manageable/All Well
    issue_description = db.Column(db.Text, nullable=True)
    comments = db.Column(db.Text, nullable=True)
      # Footage [If any]

    submitter = db.relationship('User', foreign_keys='Team2CampusCameraStatus.submitted_by',
                                backref=db.backref('submitted_team2_campus_camera_status', lazy=True))
    
#<!-- 8b. Vehicle Camera Status -->
class Team2VehicleCameraStatus(BaseForm):
    __tablename__ = 'team2_vehicle_camera_status'

    work_activity = db.Column(db.String(100), nullable=True, default='Camera & Monitoring')
    department = db.Column(db.String(100), nullable=True, default='Control Room')
    particulars = db.Column(db.String(100), nullable=True, default='Vehicles')
    route_numbers = db.Column(db.String(100), nullable=True)  # List of Route Nos.
    camera_id = db.Column(db.String(100), nullable=True)  # Camera ID/No.
    working_status = db.Column(db.String(10), nullable=True)  # Yes/No
    not_working_details = db.Column(db.Text, nullable=True)  # List/IDs
    nature_of_issue = db.Column(db.String(50), nullable=True)  # Critical/Manageable/All Well
    issue_description = db.Column(db.Text, nullable=True)
    comments = db.Column(db.Text, nullable=True)

    submitter = db.relationship('User', foreign_keys='Team2VehicleCameraStatus.submitted_by',
                                backref=db.backref('submitted_team2_vehicle_camera_status', lazy=True))
    
#<!-- 8c. Bus AC Camera Status -->
class Team2BusACCameraStatus(BaseForm):
    __tablename__ = 'team2_bus_ac_camera_status'

    work_activity = db.Column(db.String(100), nullable=True, default='Camera & Monitoring')
    department = db.Column(db.String(100), nullable=True, default='Control Room')
    particulars = db.Column(db.String(100), nullable=True, default='Bus AC')
    route = db.Column(db.String(100), nullable=True)  # Route details
    camera_id = db.Column(db.String(100), nullable=True)  # Camera ID/No.
    working_status = db.Column(db.String(10), nullable=True)  # Yes/No
    not_working_details = db.Column(db.Text, nullable=True)  # Details if not working
    nature_of_issue = db.Column(db.String(50), nullable=True)  # Critical/Manageable/All Well
    issue_description = db.Column(db.Text, nullable=True)
    comments = db.Column(db.Text, nullable=True)

    submitter = db.relationship('User', foreign_keys='Team2BusACCameraStatus.submitted_by',
                                backref=db.backref('submitted_team2_bus_ac_camera_status', lazy=True))
    
#8d. GPS Monitoring
class Team2GPSMonitoring(BaseForm):
    __tablename__ = 'team2_gps_monitoring'

    work_activity = db.Column(db.String(100), nullable=True, default='Camera & Monitoring')
    department = db.Column(db.String(100), nullable=True, default='Control Room')
    particulars = db.Column(db.String(100), nullable=True, default='GPS')
    vehicles = db.Column(db.String(100), nullable=True)  # Vehicles details
    halt_2_mins = db.Column(db.String(100), nullable=True)  # 2 min halt details
    over_speed = db.Column(db.String(100), nullable=True)  # Over speed details 
    footage_file_id = db.Column(db.Integer, db.ForeignKey('file_storage.file_id'), nullable=True)  # File reference
    nature_of_issue = db.Column(db.String(50), nullable=True)  # Critical/Manageable/All Well
    issue_description = db.Column(db.Text, nullable=True)
    comments = db.Column(db.Text, nullable=True)

    submitter = db.relationship('User', foreign_keys='Team2GPSMonitoring.submitted_by',
                                backref=db.backref('submitted_team2_gps_monitoring', lazy=True))
    footage_file = db.relationship('FileStorage', foreign_keys=[footage_file_id], backref='gps_monitoring_entries')
    
#8e. Issues Identified (Monitoring)
class Team2IssuesIdentifiedMonitoring(BaseForm):
    __tablename__ = 'team2_issues_identified_monitoring'

    work_activity = db.Column(db.String(100), nullable=True, default='Camera & Monitoring')
    department = db.Column(db.String(100), nullable=True, default='Control Room')
    particulars = db.Column(db.String(100), nullable=True)
    venue = db.Column(db.String(100), nullable=True)
    time = db.Column(db.Time, nullable=True)
    nature_of_issue = db.Column(db.String(50), nullable=True)  # Critical/Manageable/All Well
    escalated_to = db.Column(db.String(100), nullable=True)
    action_taken = db.Column(db.Text, nullable=True)
    any_issues_on_observation = db.Column(db.Text, nullable=True)

    submitter = db.relationship('User', foreign_keys='Team2IssuesIdentifiedMonitoring.submitted_by',
                                backref=db.backref('submitted_team2_issues_identified_monitoring', lazy=True))
    
#8f. Issues Identified (Control Room)   
class Team2IssuesIdentifiedControlRoom(BaseForm):
    __tablename__ = 'team2_issues_identified_control_room'

    work_activity = db.Column(db.String(100), nullable=True, default='Camera & Monitoring')
    department = db.Column(db.String(100), nullable=True, default='Control Room')
    particulars = db.Column(db.String(100), nullable=True)
    no_of_late_reports = db.Column(db.Integer, nullable=True)
    no_of_members_entered_reason = db.Column(db.Integer, nullable=True)
    on_time_acknowledgement = db.Column(db.String(10), nullable=True)  # Yes/No
    nature_of_issue = db.Column(db.String(50), nullable=True)  # Critical/Manageable/All Well
    escalated_to = db.Column(db.String(100), nullable=True)
    action_taken = db.Column(db.Text, nullable=True)

    submitter = db.relationship('User', foreign_keys='Team2IssuesIdentifiedControlRoom.submitted_by',
                                backref=db.backref('submitted_team2_issues_identified_control_room', lazy=True))    
    
    # team2_issues_camera_footage
class Team2CameraFootageEntry(BaseForm):
    __tablename__ = 'team2_camera_footage_entry'

    work_activity = db.Column(db.String(100), nullable=True, default='Camera & Monitoring')
    department = db.Column(db.String(100), nullable=True, default='Control Room')
    particulars = db.Column(db.String(100), nullable=True)  # e.g., Out of Class, Clustered
    name = db.Column(db.String(100), nullable=True)
    comments = db.Column(db.Text, nullable=True)

    submitter = db.relationship('User', foreign_keys='Team2CameraFootageEntry.submitted_by',
                                backref=db.backref('submitted_team2_camera_footage_entry', lazy=True))

    
#9. Biometrics Access Card Punching 
class Team2BiometricsAccessCardPunching(BaseForm):
    __tablename__ = 'team2_biometrics_access_card_punching'

    work_activity = db.Column(db.String(100), nullable=True, default='Biometrics Access Card Punching')
    department = db.Column(db.String(100), nullable=True, default='Control Room')
    particulars = db.Column(db.String(100), nullable=True)
    total_punching = db.Column(db.Integer, nullable=True)   
    absent_punching = db.Column(db.Integer, nullable=True)
    punched_punching = db.Column(db.Integer, nullable=True)
    not_punching = db.Column(db.Integer, nullable=True)
    nature_of_issue = db.Column(db.String(50), nullable=True)  # Critical/Manageable/All Well
    issue_description = db.Column(db.Text, nullable=True)
    comments = db.Column(db.Text, nullable=True)    

    submitter = db.relationship('User', foreign_keys='Team2BiometricsAccessCardPunching.submitted_by',
                                backref=db.backref('submitted_team2_biometrics_access_card_punching', lazy=True))   
    
#10. Water TDS Deviation
class Team2WaterTDSDeviation(BaseForm):
    __tablename__ = 'team2_water_tds_deviation'

    work_activity = db.Column(db.String(100), nullable=True, default='Water TDS Deviation')
    department = db.Column(db.String(100), nullable=True, default='House Keeping')
    particulars = db.Column(db.String(100), nullable=True)
    ro_details = db.Column(db.String(100), nullable=True)
    tds = db.Column(db.Float, nullable=True)
    ph = db.Column(db.Float, nullable=True)
    nature_of_issue = db.Column(db.String(50), nullable=True)
    issue_description = db.Column(db.Text, nullable=True)
    comments = db.Column(db.Text, nullable=True)

    submitter = db.relationship('User', foreign_keys='Team2WaterTDSDeviation.submitted_by',
                                backref=db.backref('submitted_team2_water_tds_deviation', lazy=True))
  
    
#11. Testing & Cleaning
class Team2TestingCleaning(BaseForm):
    __tablename__ = 'team2_testing_cleaning'

    work_activity = db.Column(db.String(100), nullable=True, default='Testing & Cleaning')      
    department = db.Column(db.String(100), nullable=True, default='Testing & Cleaning')
    particulars = db.Column(db.String(100), nullable=True)
    regular_process = db.Column(db.String(100), nullable=True)
    deep_cleaning = db.Column(db.String(100), nullable=True)
    event_arrangement = db.Column(db.String(100), nullable=True)
    nature_of_issue = db.Column(db.String(50), nullable=True)  # Critical/Manageable/All Well
    issue_description = db.Column(db.Text, nullable=True)
    comments = db.Column(db.Text, nullable=True)

    submitter = db.relationship('User', foreign_keys='Team2TestingCleaning.submitted_by',
                                backref=db.backref('submitted_team2_testing_cleaning', lazy=True))
    
    # Water Level Checking
class Team2WaterLevel(BaseForm):
    __tablename__ = 'team2_water_level'

    work_activity = db.Column(db.String(100), nullable=True)       # Work / Activity
    department = db.Column(db.String(100), nullable=True)          # Department / Category
    particulars = db.Column(db.String(100), nullable=True)         # Particulars
    floor = db.Column(db.String(50), nullable=True)                # Floor
    venue = db.Column(db.String(100), nullable=True)               # Venue
    nature_of_issue = db.Column(db.String(50), nullable=True)      # Nature of Issue (Critical / Manageable / All Well)
    issue_description = db.Column(db.Text, nullable=True)          # Issue Description
    comments = db.Column(db.Text, nullable=True)                   # Comments

    submitter = db.relationship('User', foreign_keys='Team2WaterLevel.submitted_by',
                                backref=db.backref('submitted_team2_water_level', lazy=True))

# Housekeeping General
class Team2HousekeepingGeneral(BaseForm):
    __tablename__ = 'team2_housekeeping_general'

    work_activity = db.Column(db.String(100), nullable=True)   # Work / Activity
    department = db.Column(db.String(100), nullable=True)      # Department / Category
    particulars = db.Column(db.String(100), nullable=True)     # Particulars
    name = db.Column(db.String(100), nullable=True)            # Name
    observation = db.Column(db.Text, nullable=True)            # Observation of HK Team
    remark = db.Column(db.Text, nullable=True)                 # Remark

    submitter = db.relationship(
        'User',
        foreign_keys='Team2HousekeepingGeneral.submitted_by',
        backref=db.backref('submitted_team2_housekeeping_general', lazy=True)
    )

#11. Pool Testing
class Team2PoolTesting(BaseForm):
    __tablename__ = 'team2_pool_testing'

    work_activity = db.Column(db.String(100), nullable=True, default='Pool Testing')
    department = db.Column(db.String(100), nullable=True, default='Testing & Cleaning') 
    particulars = db.Column(db.String(100), nullable=True)
    chlorine_level = db.Column(db.Float, nullable=True)
    ph_level = db.Column(db.Float, nullable=True)
    water_cleanliness = db.Column(db.String(100), nullable=True)
    nature_of_issue = db.Column(db.String(50), nullable=True)  # Critical/Manageable/All Well
    issue_description = db.Column(db.Text, nullable=True)
    comments = db.Column(db.Text, nullable=True)

    submitter = db.relationship('User', foreign_keys='Team2PoolTesting.submitted_by',
                                backref=db.backref('submitted_team2_pool_testing', lazy=True))
    
#12. Washroom Cleanliness (Updated)
class Team2WashroomCleanliness(BaseForm):
    __tablename__ = 'team2_washroom_cleanliness'

    work_activity = db.Column(db.String(100), nullable=True, default='Washroom Cleanliness')
    department = db.Column(db.String(100), nullable=True, default='Housekeeping')  
    floor = db.Column(db.String(50), nullable=True)  # Ground / First / Second 
    particulars = db.Column(db.String(100), nullable=True)
    boys_washroom = db.Column(db.String(100), nullable=True)
    girls_washroom = db.Column(db.String(100), nullable=True)
    cleanliness = db.Column(db.String(100), nullable=True)
    smell = db.Column(db.String(100), nullable=True)
    restroom_equipment = db.Column(db.String(100), nullable=True)   
    
    submitter = db.relationship('User', foreign_keys='Team2WashroomCleanliness.submitted_by',
                                backref=db.backref('submitted_team2_washroom_cleanliness', lazy=True))
 
#13. Transport Attendance
class Team2TransportAttendance(BaseForm):
    __tablename__ = 'team2_transport_attendance'

    work_activity = db.Column(db.String(100), nullable=True, default='Transport Attendance')
    department = db.Column(db.String(100), nullable=True, default='Transport')
    particulars = db.Column(db.String(100), nullable=True)
    students_morning = db.Column(db.String(100), nullable=True)
    students_evening = db.Column(db.String(100), nullable=True)
    staff_morning = db.Column(db.String(100), nullable=True)
    staff_evening = db.Column(db.String(100), nullable=True)
    nature_of_issue = db.Column(db.String(50), nullable=True)  # Critical/Manageable/All Well
    issue_description = db.Column(db.Text, nullable=True)
    comments = db.Column(db.Text, nullable=True)    
    
    submitter = db.relationship('User', foreign_keys='Team2TransportAttendance.submitted_by',
                                backref=db.backref('submitted_team2_transport_attendance', lazy=True))

# AC Working Status
class Team2ACWorkingStatus(BaseForm):
    __tablename__ = 'team2_ac_working_status'

    work_activity = db.Column(db.String(100), nullable=True, default='AC Working Status')
    department = db.Column(db.String(100), nullable=True, default='Transport')
    particulars = db.Column(db.String(100), nullable=True)
    route_numbers = db.Column(db.String(100), nullable=True)
    nature_of_issue = db.Column(db.String(50), nullable=True)  # Critical/Manageable/All Well
    issue_description = db.Column(db.Text, nullable=True)
    comments = db.Column(db.Text, nullable=True)
    
    submitter = db.relationship('User', foreign_keys='Team2ACWorkingStatus.submitted_by',
                                backref=db.backref('submitted_team2_ac_working_status', lazy=True))
    
#team 2 Late Reporting  
class Team2LateReporting(BaseForm):
    __tablename__ = 'team2_late_reporting'

    work_activity = db.Column(db.String(100), nullable=True, default='Late Reporting')
    department = db.Column(db.String(100), nullable=True, default='Transport')
    particulars = db.Column(db.String(100), nullable=True)
    route_numbers = db.Column(db.String(100), nullable=True)
    nature_of_issue = db.Column(db.String(50), nullable=True)  # Critical/Manageable/All Well
    issue_description = db.Column(db.Text, nullable=True)
    comments = db.Column(db.Text, nullable=True)
    
    submitter = db.relationship('User', foreign_keys='Team2LateReporting.submitted_by',
                                backref=db.backref('submitted_team2_late_reporting', lazy=True))
#team 2 Maintenance / Service / Issues
class Team2MaintenanceServiceIssues(BaseForm):
    __tablename__ = 'team2_maintenance_service_issues'

    work_activity = db.Column(db.String(100), nullable=True, default='Maintenance / Service / Issues')
    department = db.Column(db.String(100), nullable=True, default='Transport')
    particulars = db.Column(db.String(100), nullable=True)
    route_numbers = db.Column(db.String(100), nullable=True)
    work_nature = db.Column(db.String(100), nullable=True)
    venue = db.Column(db.String(100), nullable=True)
    work_status = db.Column(db.String(100), nullable=True)
    nature_of_issue = db.Column(db.String(50), nullable=True)  # Critical/Manageable/All Well
    issue_description = db.Column(db.Text, nullable=True)
    comments = db.Column(db.Text, nullable=True)    
    
    submitter = db.relationship('User', foreign_keys='Team2MaintenanceServiceIssues.submitted_by',
                                backref=db.backref('submitted_team2_maintenance_service_issues', lazy=True))
    
# Car Maintenance/Cleaning
class Team2CarMaintenanceCleaning(BaseForm):
    __tablename__ = 'team2_car_maintenance_cleaning'

    work_activity = db.Column(db.String(100), nullable=True, default='Car Maintenance/Cleaning')
    department = db.Column(db.String(100), nullable=True, default='Transport')  
    particulars = db.Column(db.String(100), nullable=True)
    car_number = db.Column(db.String(100), nullable=True)
    cleaned_by = db.Column(db.String(100), nullable=True)
    maintenance_service_issues = db.Column(db.String(100), nullable=True)
    nature_of_issue = db.Column(db.String(50), nullable=True)  # Critical/Manageable/All Well
    issue_description = db.Column(db.Text, nullable=True)
    comments = db.Column(db.Text, nullable=True)    
    
    submitter = db.relationship('User', foreign_keys='Team2CarMaintenanceCleaning.submitted_by',
                                backref=db.backref('submitted_team2_car_maintenance_cleaning', lazy=True))
# Vehicle Renewals / Delays
class Team2VehicleRenewalsDelays(BaseForm):
    __tablename__ = 'team2_vehicle_renewals_delays'

    work_activity = db.Column(db.String(100), nullable=True, default='Vehicle Renewals / Delays')
    department = db.Column(db.String(100), nullable=True, default='Transport')  
    particulars = db.Column(db.String(100), nullable=True)
    vehicle_numbers = db.Column(db.String(100), nullable=True)
    route_numbers = db.Column(db.String(100), nullable=True)
    nature_of_issue = db.Column(db.String(50), nullable=True)  # Critical/Manageable/All Well
    issue_description = db.Column(db.Text, nullable=True)
    comments = db.Column(db.Text, nullable=True)
    
    submitter = db.relationship('User', foreign_keys='Team2VehicleRenewalsDelays.submitted_by',
                                backref=db.backref('submitted_team2_vehicle_renewals_delays', lazy=True))
# Special Trip
class Team2SpecialTrip(BaseForm):
    __tablename__ = 'team2_special_trip'

    work_activity = db.Column(db.String(100), nullable=True, default='Special Trip')
    department = db.Column(db.String(100), nullable=True, default='Transport')  
    particulars = db.Column(db.String(100), nullable=True)
    route_numbers = db.Column(db.String(100), nullable=True)
    actual_out_time = db.Column(db.String(100), nullable=True)
    nature_of_issue = db.Column(db.String(50), nullable=True)  # Critical/Manageable/All Well
    issue_description = db.Column(db.Text, nullable=True)
    comments = db.Column(db.Text, nullable=True)    
    
    submitter = db.relationship('User', foreign_keys='Team2SpecialTrip.submitted_by',
                                backref=db.backref('submitted_team2_special_trip', lazy=True))
    
    #S.No 18b: Parent Concern Detail
class Team2ParentConcernDetail(BaseForm):
    __tablename__ = 'team2_parent_concern_detail'

    pc_work_activity = db.Column(db.String(100), default='Parent Concern Detail')
    pc_detail_name = db.Column(db.String(255))
    pc_detail_grade = db.Column(db.String(20))
    pc_detail_concern = db.Column(db.Text)
    pc_detail_incharge = db.Column(db.String(255))
    pc_detail_issue_nature = db.Column(db.String(50))
    pc_detail_comment = db.Column(db.Text)


    submitter = db.relationship('User', foreign_keys='Team2ParentConcernDetail.submitted_by',
                                backref=db.backref('submitted_team2_parent_concern_detail', lazy=True))

        
# 14 AC Temperature Check
class Team2ACTemperatureCheck(BaseForm):
    __tablename__ = 'team2_ac_temperature_check'

    work_activity = db.Column(db.String(100), nullable=True, default='AC Temperature Check')
    department = db.Column(db.String(100), nullable=True, default='AC Temp')
    floor = db.Column(db.String(100), nullable=True)
    particulars = db.Column(db.String(100), nullable=True)
    classroom = db.Column(db.String(100), nullable=True)
    temperature = db.Column(db.String(100), nullable=True)
    hot_cold_normal = db.Column(db.String(100), nullable=True)
    working_condition = db.Column(db.String(100), nullable=True)
    nature_of_issue = db.Column(db.String(50), nullable=True)  # Critical/Manageable/All Well
    issue_description = db.Column(db.Text, nullable=True)
    comments = db.Column(db.Text, nullable=True)    
    
    submitter = db.relationship('User', foreign_keys='Team2ACTemperatureCheck.submitted_by',
                                backref=db.backref('submitted_team2_ac_temperature_check', lazy=True))
    
# 15 Labor, EB, Solar, Genset
class Team2LaborEbSolarGenset(BaseForm):
    __tablename__ = 'team2_labor_eb_solar_genset'

    work_activity = db.Column(db.String(100), nullable=True, default='Labor, EB, Solar, Genset')
    department = db.Column(db.String(100), nullable=True, default='Labor, EB, Solar, Genset')   
    nature_of_work = db.Column(db.String(100), nullable=True)
    no_of_labours = db.Column(db.String(100), nullable=True)    
    venue = db.Column(db.String(100), nullable=True)
    nature_of_issue = db.Column(db.String(50), nullable=True)  # Critical/Manageable/All Well
    issue_description = db.Column(db.Text, nullable=True)
    comments = db.Column(db.Text, nullable=True)
    
    submitter = db.relationship('User', foreign_keys='Team2LaborEbSolarGenset.submitted_by',
                                backref=db.backref('submitted_team2_labor_eb_solar_genset', lazy=True))
    
# Motor Control
class Team2Motor(BaseForm):
    __tablename__ = 'team2_motor'

    work_activity = db.Column(db.String(100), nullable=True, default='Motor Control')
    department = db.Column(db.String(100), nullable=True, default='Motor')
    on_time = db.Column(db.String(100), nullable=True)
    off_time = db.Column(db.String(100), nullable=True)
    nature_of_issue = db.Column(db.String(50), nullable=True)  # Critical/Manageable/All Well
    issue_description = db.Column(db.Text, nullable=True)
    comments = db.Column(db.Text, nullable=True)
    
    submitter = db.relationship('User', foreign_keys='Team2Motor.submitted_by',
                                backref=db.backref('submitted_team2_motor', lazy=True))

# Pest Control
class Team2PestControl(BaseForm):
    __tablename__ = 'team2_pest_control'

    work_activity = db.Column(db.String(100), nullable=True, default='Pest Control')
    department = db.Column(db.String(100), nullable=True, default='Pest Control')
    in_time = db.Column(db.String(100), nullable=True)
    out_time = db.Column(db.String(100), nullable=True)
    area_covered = db.Column(db.String(100), nullable=True)
    nature_of_issue = db.Column(db.String(50), nullable=True)  # Critical/Manageable/All Well
    issue_description = db.Column(db.Text, nullable=True)
    comments = db.Column(db.Text, nullable=True)
    
    submitter = db.relationship('User', foreign_keys='Team2PestControl.submitted_by',
                                backref=db.backref('submitted_team2_pest_control', lazy=True))
    
#AC Temp Deviation (>27°C)
class Team2ACTempDeviation(BaseForm):
    __tablename__ = 'team2_ac_temp_deviation'

    work_activity = db.Column(db.String(100), nullable=True, default='AC Temp Deviation (>27°C)')
    department = db.Column(db.String(100), nullable=True, default='AC Temp')    
    particulars = db.Column(db.String(100), nullable=True)
    venue = db.Column(db.String(100), nullable=True)
    nature_of_issue = db.Column(db.String(50), nullable=True)  # Critical/Manageable/All Well
    issue_description = db.Column(db.Text, nullable=True)
    comments = db.Column(db.Text, nullable=True)
    
    submitter = db.relationship('User', foreign_keys='Team2ACTempDeviation.submitted_by',
                                backref=db.backref('submitted_team2_ac_temp_deviation', lazy=True)) 

#Electricity Consumption
class Team2ElectricityConsumption(BaseForm):
    __tablename__ = 'team2_electricity_consumption'

    work_activity = db.Column(db.String(100), nullable=True, default='Electricity Consumption')
    department = db.Column(db.String(100), nullable=True, default='Electricity')
    category = db.Column(db.String(100), nullable=True)

    # Store unit fields as string to gracefully handle empty or non-numeric entries coming from form inputs.
    # Numeric calculations are not performed on these fields inside the application – they are displayed only,
    # so keeping them as string avoids ValueError exceptions when the database stores '' or other text values.
    total_units = db.Column(db.String(100), nullable=True)
    eb = db.Column(db.String(100), nullable=True)
    solar = db.Column(db.String(100), nullable=True)
    genset = db.Column(db.String(100), nullable=True)

    solar_issue = db.Column(db.String(100), nullable=True)
    genset_issue = db.Column(db.String(100), nullable=True)
    eb_issue = db.Column(db.String(100), nullable=True)
    overall_issue_desc = db.Column(db.Text, nullable=True)
    overall_comments = db.Column(db.Text, nullable=True)

    submitter = db.relationship(
        'User',
        foreign_keys='Team2ElectricityConsumption.submitted_by',
        backref=db.backref('submitted_team2_electricity_consumption', lazy=True)
    )

#EB Details
class Team2EBDetails(BaseForm):
    __tablename__ = 'team2_eb_details'

    work_activity = db.Column(db.String(100), nullable=True, default='EB Details')
    department = db.Column(db.String(100), nullable=True, default='Electricity')
    category = db.Column(db.String(100), nullable=True)
    rw_230_240 = db.Column(db.String(100), nullable=True)
    yw_230_240 = db.Column(db.String(100), nullable=True)
    bw_230_240 = db.Column(db.String(100), nullable=True)
    max_demand_104 = db.Column(db.String(100), nullable=True)
    units_per_day = db.Column(db.String(100), nullable=True)    
    nature_of_issue = db.Column(db.String(50), nullable=True)  # Critical/Manageable/All Well

    
    submitter = db.relationship('User', foreign_keys='Team2EBDetails.submitted_by',
                                backref=db.backref('submitted_team2_eb_details', lazy=True))
    
#Solar Details
class Team2SolarDetails(BaseForm):
    __tablename__ = 'team2_solar_details'

    work_activity = db.Column(db.String(100), nullable=True, default='Solar Details')
    department = db.Column(db.String(100), nullable=True, default='Solar')  
    category = db.Column(db.String(100), nullable=True)
    capacity = db.Column(db.String(100), nullable=True)
    units_per_day = db.Column(db.String(100), nullable=True)
    remarks = db.Column(db.String(100), nullable=True)
    time = db.Column(db.String(100), nullable=True)
    max_production = db.Column(db.String(100), nullable=True)
    nature_of_issue = db.Column(db.String(50), nullable=True)  # Critical/Manageable/All Well
    issue_description = db.Column(db.Text, nullable=True)
    comments = db.Column(db.Text, nullable=True)    
    
    submitter = db.relationship('User', foreign_keys='Team2SolarDetails.submitted_by',
                                backref=db.backref('submitted_team2_solar_details', lazy=True))

#Genset Details
class Team2GensetDetails(BaseForm):
    __tablename__ = 'team2_genset_details'

    work_activity = db.Column(db.String(100), nullable=True, default='Genset Details')
    department = db.Column(db.String(100), nullable=True, default='Genset')
    category = db.Column(db.String(100), nullable=True)
    on_time = db.Column(db.String(100), nullable=True)
    off_time = db.Column(db.String(100), nullable=True)
    battery_voltage = db.Column(db.String(100), nullable=True)
    coolant_temp = db.Column(db.String(100), nullable=True)
    nature_of_issue = db.Column(db.String(50), nullable=True)  # Critical/Manageable/All Well
    issue_description = db.Column(db.Text, nullable=True)
    comments = db.Column(db.Text, nullable=True)
    
    submitter = db.relationship('User', foreign_keys='Team2GensetDetails.submitted_by',
                                backref=db.backref('submitted_team2_genset_details', lazy=True))

#16 a Count Verification
class Team2CountVerification(BaseForm):
    __tablename__ = 'team2_count_verification'

    work_activity = db.Column(db.String(100), nullable=True, default='Count Verification')
    department = db.Column(db.String(100), nullable=True, default='Security')
    category = db.Column(db.String(100), nullable=True)
    particulars = db.Column(db.String(100), nullable=True)
    total = db.Column(db.String(100), nullable=True)
    received = db.Column(db.String(100), nullable=True)
    submitted = db.Column(db.String(100), nullable=True)
    nature_of_issue = db.Column(db.String(50), nullable=True)  # Critical/Manageable/All Well
    issue_description = db.Column(db.Text, nullable=True)
    comments = db.Column(db.Text, nullable=True)

    submitter = db.relationship('User', foreign_keys='Team2CountVerification.submitted_by',
                                backref=db.backref('submitted_team2_count_verification', lazy=True))
    
#Attendance Replacement
class Team2AttendanceReplacement(BaseForm):
    __tablename__ = 'team2_attendance_replacement'

    work_activity = db.Column(db.String(100), nullable=True, default='Attendance Replacement')
    department = db.Column(db.String(100), nullable=True, default='Security')
    particulars = db.Column(db.String(100), nullable=True)
    allotted = db.Column(db.String(100), nullable=True)
    replaced = db.Column(db.String(100), nullable=True)
    nature_of_issue = db.Column(db.String(50), nullable=True)  # Critical/Manageable/All Well
    issue_description = db.Column(db.Text, nullable=True)
    comments = db.Column(db.Text, nullable=True)    
    
    submitter = db.relationship('User', foreign_keys='Team2AttendanceReplacement.submitted_by',
                                backref=db.backref('submitted_team2_attendance_replacement', lazy=True))

#Security Info Note 
class Team2SecurityInfoNote(BaseForm):
    __tablename__ = 'team2_security_info_note'

    work_activity = db.Column(db.String(100), nullable=True, default='Security Info Note')
    department = db.Column(db.String(100), nullable=True, default='Security')
    particulars = db.Column(db.String(100), nullable=True)  
    info_by = db.Column(db.String(100), nullable=True)
    information = db.Column(db.Text, nullable=True)
    nature_of_issue = db.Column(db.String(50), nullable=True)  # Critical/Manageable/All Well
    issue_description = db.Column(db.Text, nullable=True)
    comments = db.Column(db.Text, nullable=True)    
    
    submitter = db.relationship('User', foreign_keys='Team2SecurityInfoNote.submitted_by',
                                backref=db.backref('submitted_team2_security_info_note', lazy=True))
    
#<!-- security Inward/Outward Govt Officials -->
class Team2SecurityGovtInout(BaseForm):
    __tablename__ = 'team2_security_govt_inout'

    work_activity = db.Column(db.String(100), nullable=True, default='Inward/Outward Govt Officials')
    department = db.Column(db.String(100), nullable=True, default='Security')
    particulars = db.Column(db.String(100), nullable=True)
    in_time = db.Column(db.String(100), nullable=True)
    out_time = db.Column(db.String(100), nullable=True)
    purpose = db.Column(db.String(100), nullable=True)
    nature_of_issue = db.Column(db.String(50), nullable=True)  # Critical/Manageable/All Well
    issue_description = db.Column(db.Text, nullable=True)
    comments = db.Column(db.Text, nullable=True)
    
    submitter = db.relationship('User', foreign_keys='Team2SecurityGovtInout.submitted_by',
                                backref=db.backref('submitted_team2_security_govt_inout', lazy=True))

#security Alcohol Test
class Team2AlcoholTest(BaseForm):
    __tablename__ = 'team2_alcohol_test'

    work_activity = db.Column(db.String(100), nullable=True, default='Alcohol Test')
    department = db.Column(db.String(100), nullable=True, default='Security')
    name = db.Column(db.String(100), nullable=True)
    time = db.Column(db.String(100), nullable=True)
    reading = db.Column(db.String(100), nullable=True)
    comments = db.Column(db.Text, nullable=True)
    
    submitter = db.relationship('User', foreign_keys='Team2AlcoholTest.submitted_by',
                                backref=db.backref('submitted_team2_alcohol_test', lazy=True))
    
#<!-- security Materials Inward/Outward (Security) -->   
class Team2SecurityMaterialsInout(BaseForm):
    __tablename__ = 'team2_security_materials_inout'

    work_activity = db.Column(db.String(100), nullable=True, default='Materials Inward/Outward (Security)')
    department = db.Column(db.String(100), nullable=True, default='Security')
    product = db.Column(db.String(100), nullable=True)
    in_time = db.Column(db.String(100), nullable=True)
    vendor = db.Column(db.String(100), nullable=True)
    description = db.Column(db.Text, nullable=True)
    quantity = db.Column(db.String(100), nullable=True)
    nature_of_issue = db.Column(db.String(50), nullable=True)  # Critical/Manageable/All Well
    issue_description = db.Column(db.Text, nullable=True)   
    comments = db.Column(db.Text, nullable=True)
    
    submitter = db.relationship('User', foreign_keys='Team2SecurityMaterialsInout.submitted_by',
                                backref=db.backref('submitted_team2_security_materials_inout', lazy=True))
    
#<!-- security Materials Outward -->
class Team2SecurityMaterialsOutward(BaseForm):
    __tablename__ = 'team2_security_materials_outward'

    work_activity = db.Column(db.String(100), nullable=True, default='Materials Outward')
    department = db.Column(db.String(100), nullable=True, default='Security')
    product = db.Column(db.String(100), nullable=True)
    out_time = db.Column(db.String(100), nullable=True)
    vendor = db.Column(db.String(100), nullable=True)
    description = db.Column(db.Text, nullable=True)
    quantity = db.Column(db.String(100), nullable=True)
    nature_of_issue = db.Column(db.String(50), nullable=True)  # Critical/Manageable/All Well
    issue_description = db.Column(db.Text, nullable=True)
    comments = db.Column(db.Text, nullable=True)
    
    submitter = db.relationship('User', foreign_keys='Team2SecurityMaterialsOutward.submitted_by',
                                backref=db.backref('submitted_team2_security_materials_outward', lazy=True))
    
#<!-- securityTransport Verification -->
class Team2TransportVerification(BaseForm):
    __tablename__ = 'team2_transport_verification'

    work_activity = db.Column(db.String(100), nullable=True, default='Transport Verification')
    department = db.Column(db.String(100), nullable=True, default='Security')

    vehicle_number = db.Column(db.String(100), nullable=True)
    damage_location = db.Column(db.Text, nullable=True)
    escalated_to = db.Column(db.String(100), nullable=True)
    nature_of_issue = db.Column(db.String(50), nullable=True)  # Critical/Manageable/All Well
    issue_description = db.Column(db.Text, nullable=True)
    comments = db.Column(db.Text, nullable=True)

    submitter = db.relationship('User', foreign_keys='Team2TransportVerification.submitted_by',
                                backref=db.backref('submitted_team2_transport_verifications', lazy=True))
    
#<!-- 17 securityDocuments Movement -->
class Team2DocumentsMovement(BaseForm):
    __tablename__ = 'team2_documents_movement'

    work_activity = db.Column(db.String(100), nullable=True, default='Documents Movement')
    department = db.Column(db.String(100), nullable=True, default='File Room')

    # Row 1: New File / Document Entry
    doc_new_particulars = db.Column(db.String(100), nullable=True)  # Particulars for Row 1
    doc_new_dept = db.Column(db.String(100), nullable=True)  # Source Department
    doc_new_name = db.Column(db.String(200), nullable=True)  # Document Name
    doc_new_submitby = db.Column(db.String(200), nullable=True)  # Submitted By
    doc_new_nature = db.Column(db.String(50), nullable=True)  # Nature of Issue
    doc_new_issue = db.Column(db.Text, nullable=True)
    doc_new_comments = db.Column(db.Text, nullable=True)

    # Row 2: Non-Returnable File / Document
    doc_nonret_particulars = db.Column(db.String(100), nullable=True)  # Particulars for Row 2
    doc_nonret_dept = db.Column(db.String(100), nullable=True)  # Destination Department
    doc_nonret_name = db.Column(db.String(200), nullable=True)
    doc_nonret_issuedto = db.Column(db.String(200), nullable=True)
    doc_nonret_nature = db.Column(db.String(50), nullable=True)
    doc_nonret_issue = db.Column(db.Text, nullable=True)
    doc_nonret_comments = db.Column(db.Text, nullable=True)

    # Row 3: Original File / Doc Movement
    doc_orig_particulars = db.Column(db.String(100), nullable=True)  # Particulars for Row 3
    doc_orig_naturedoc = db.Column(db.String(200), nullable=True)  # Nature of Document
    doc_orig_issuedto = db.Column(db.String(200), nullable=True)
    doc_orig_purpose = db.Column(db.String(200), nullable=True)
    doc_orig_nature = db.Column(db.String(50), nullable=True)
    doc_orig_issue = db.Column(db.Text, nullable=True)
    doc_orig_comments = db.Column(db.Text, nullable=True)

    submitter = db.relationship('User', foreign_keys='Team2DocumentsMovement.submitted_by', backref=db.backref('submitted_team2_documents_movement', lazy=True))

#18 Govt Official Documents
class Team2GovtOfficialDocuments(BaseForm):
    __tablename__ = 'team2_govt_official_documents'

    work_activity = db.Column(db.String(100), nullable=True, default='Govt Official Documents')
    department = db.Column(db.String(100), nullable=True, default='PRO')
    
    document_name = db.Column(db.String(200), nullable=True)
    expiry_date = db.Column(db.Date, nullable=True)
    expected_renewal_date = db.Column(db.Date, nullable=True)
    
    nature_of_issue = db.Column(db.String(50), nullable=True)  # Critical / Manageable / All Well
    issue_description = db.Column(db.Text, nullable=True)
    comments = db.Column(db.Text, nullable=True)

    submitter = db.relationship(
        'User',
        foreign_keys='Team2GovtOfficialDocuments.submitted_by',
        backref=db.backref('submitted_team2_govt_official_documents', lazy=True)
    )

#<!-- 19 a Thoorigai Team Social Media -->
class Team2ThoorigaiTeamSocialMedia(BaseForm):
    __tablename__ = 'team2_thoorigai_team_social_media'

    work_activity = db.Column(db.String(100), nullable=True, default='Digital / Marketing')
    department = db.Column(db.String(100), nullable=True, default='Thoorigai Team')
    platform = db.Column(db.String(100), nullable=False)  # e.g., Facebook, Instagram, YouTube, Whatsapp
    video_status = db.Column(db.String(100), nullable=True)  # Video status
    post_status = db.Column(db.String(100), nullable=True)  # Post status
    update_status = db.Column(db.Text, nullable=True)  # Update status or description
    nature_of_issue = db.Column(db.String(50), nullable=True)  # Critical/Manageable/All Well
    issue_description = db.Column(db.Text, nullable=True)
    comments = db.Column(db.Text, nullable=True)

    submitter = db.relationship('User', foreign_keys='Team2ThoorigaiTeamSocialMedia.submitted_by', backref=db.backref('submitted_team2_thoorigai_team_social_media', lazy=True))

#<!-- 19 b Website Updates (Thoorigai) -->
class Team2WebsiteUpdates(BaseForm):
    __tablename__ = 'team2_website_updates'

    work_activity = db.Column(db.String(100), nullable=True, default='Website Updates')
    department = db.Column(db.String(100), nullable=True, default='Thoorigai Team')
    particulars = db.Column(db.String(100), nullable=False, default='Website')
    inclusion = db.Column(db.Text, nullable=True)
    deletion = db.Column(db.Text, nullable=True)
    others = db.Column(db.Text, nullable=True)
    nature_of_issue = db.Column(db.String(50), nullable=True)  # All Well/Manageable/Critical
    issue_description = db.Column(db.Text, nullable=True)
    comments = db.Column(db.Text, nullable=True)
    
    submitter = db.relationship('User', foreign_keys='Team2WebsiteUpdates.submitted_by', 
                                backref=db.backref('submitted_team2_website_updates', lazy=True))

#<!-- 19 c MD Social Media -->
class Team2MDSocialMedia(BaseForm):
    __tablename__ = 'team2_md_social_media'

    work_activity = db.Column(db.String(100), nullable=True, default='MD Social Media')
    department = db.Column(db.String(100), nullable=True, default='MD')
    platform = db.Column(db.String(100), nullable=False)  # Facebook, Instagram, etc.
    video = db.Column(db.String(255), nullable=True)
    post = db.Column(db.String(255), nullable=True)
    update = db.Column(db.Text, nullable=True)
    nature_of_issue = db.Column(db.String(50), nullable=True)  # All Well/Manageable/Critical
    issue_description = db.Column(db.Text, nullable=True)
    comments = db.Column(db.Text, nullable=True)
    
    submitter = db.relationship('User', foreign_keys='Team2MDSocialMedia.submitted_by', 
                                backref=db.backref('submitted_team2_md_social_media', lazy=True))

#<!-- 20 Intercom Maintenance -->
class Team2IntercomMaintenance(BaseForm):
    __tablename__ = 'team2_intercom_maintenance'

    work_activity = db.Column(db.String(100), nullable=True, default='Intercom Maintenance')
    department = db.Column(db.String(100), nullable=True, default='Maintenance')
    working = db.Column(db.String(255), nullable=True)
    not_working = db.Column(db.String(255), nullable=True)
    rectified = db.Column(db.String(255), nullable=True)
    nature_of_issue = db.Column(db.String(50), nullable=True)  # Critical/Manageable/All Well
    issue_description = db.Column(db.Text, nullable=True)
    comments = db.Column(db.Text, nullable=True)

    submitter = db.relationship('User', foreign_keys='Team2IntercomMaintenance.submitted_by',
                                backref=db.backref('submitted_team2_intercom_maintenance', lazy=True))
    
#<!-- 21 Health Check Up -->
class Team2HealthCheckUp(BaseForm):
    __tablename__ = 'team2_health_check_up'

    work_activity = db.Column(db.String(100), nullable=True, default='Health Check Up')
    department = db.Column(db.String(100), nullable=True, default='Health')
    department_staff = db.Column(db.String(255), nullable=True)
    staff_name = db.Column(db.String(255), nullable=True)
    illness = db.Column(db.String(255), nullable=True)
    informed_by = db.Column(db.String(255), nullable=True)
    action_taken = db.Column(db.String(255), nullable=True)
    nature_of_issue = db.Column(db.String(50), nullable=True)  # Critical/Manageable/All Well
    issue_description = db.Column(db.Text, nullable=True)
    comments = db.Column(db.Text, nullable=True)

    submitter = db.relationship('User', foreign_keys='Team2HealthCheckUp.submitted_by',
                                backref=db.backref('submitted_team2_health_check_up', lazy=True))

#<!-- 22Net Connectivity & Print Details -->
class Team2NetConnectivityPrintDetails(BaseForm):
    __tablename__ = 'team2_net_connectivity_print_details'

    work_activity = db.Column(db.String(100), nullable=True, default='Net Connectivity & Print Details')
    department = db.Column(db.String(100), nullable=True, default='IT')
    particulars = db.Column(db.String(100), nullable=False, default='Net Connectivity & Print Details')
    net_speed = db.Column(db.String(255), nullable=True)
    no_of_prints = db.Column(db.Integer, nullable=True)
    complaints = db.Column(db.Text, nullable=True)
    nature_of_issue = db.Column(db.String(50), nullable=True)  # Critical/Manageable/All Well
    issue_description = db.Column(db.Text, nullable=True)
    comments = db.Column(db.Text, nullable=True)    

    submitter = db.relationship('User', foreign_keys='Team2NetConnectivityPrintDetails.submitted_by',
                                backref=db.backref('submitted_team2_net_connectivity_print_details', lazy=True))

# 23 General Maintenance - IT Products
class Team2GeneralMaintenanceITProducts(BaseForm):
    __tablename__ = 'team2_general_maintenance_it_products'

    work_activity = db.Column(db.String(100), nullable=True, default='General Maintenance - IT Products')
    department = db.Column(db.String(100), nullable=True, default='IT') 
    particulars = db.Column(db.String(100), nullable=False, default='General Maintenance - IT Products')
    issues = db.Column(db.Text, nullable=True)
    complaintdate = db.Column(db.Date, nullable=True)
    solveddate = db.Column(db.Date, nullable=True)
    nature_of_issue = db.Column(db.String(50), nullable=True)  # Critical/Manageable/All Well
    issue_description = db.Column(db.Text, nullable=True)
    comments = db.Column(db.Text, nullable=True)    

    submitter = db.relationship('User', foreign_keys='Team2GeneralMaintenanceITProducts.submitted_by',
                                backref=db.backref('submitted_team2_general_maintenance_it_products', lazy=True))

#Section 24: Calendar Schedule
class Team2CalendarSchedule(BaseForm):
    __tablename__ = 'team2_calendar_schedule'

    work_activity = db.Column(db.String(100), nullable=True, default='Calendar Schedule')
    department = db.Column(db.String(100), nullable=True)   
    session = db.Column(db.String(100), nullable=True)
    category = db.Column(db.String(100), nullable=True)
    in_charge = db.Column(db.String(100), nullable=True)
    planned = db.Column(db.String(100), nullable=True)
    unplanned = db.Column(db.String(100), nullable=True)
    nature_of_issue = db.Column(db.String(50), nullable=True)  # Critical/Manageable/All Well
    issue_description = db.Column(db.Text, nullable=True)
    comments = db.Column(db.Text, nullable=True)

    submitter = db.relationship('User', foreign_keys='Team2CalendarSchedule.submitted_by',
                                backref=db.backref('submitted_team2_calendar_schedule', lazy=True))

#   Section 25: Training Attendance
class Team2TrainingAttendance(BaseForm):
    __tablename__ = 'team2_training_attendance'
    
    work_activity = db.Column(db.String(100), nullable=True, default='Training Attendance')
    department_group = db.Column(db.String(100), nullable=True)  # e.g., 'Academics', 'Admin'
    dept = db.Column(db.String(100), nullable=True)              # e.g., 'Academics - Jr.School'
    topic = db.Column(db.String(255), nullable=True)
    total = db.Column(db.Integer, nullable=True)
    present = db.Column(db.Integer, nullable=True)
    leave = db.Column(db.Integer, nullable=True)
    leave_percentage = db.Column(db.String(10), nullable=True)   # stored as a string (e.g., "23%")
    nature_of_issue = db.Column(db.String(50), nullable=True)    # e.g., All Well, Manageable, Critical
    issue_description = db.Column(db.Text, nullable=True)
    comments = db.Column(db.Text, nullable=True)

    submitter = db.relationship(
        'User',
        foreign_keys='Team2TrainingAttendance.submitted_by',
        backref=db.backref('submitted_team2_training_attendance', lazy=True)
    )

#Section 26: Training Details (CBSE/CIS/External)
class Team2TrainingDetails(BaseForm):
    __tablename__ = 'team2_training_details'    

    work_activity = db.Column(db.String(100), nullable=True, default='Training Details (CBSE/CIS/External)')
    department = db.Column(db.String(100), nullable=True, default='Training')   
    name = db.Column(db.String(100), nullable=True)
    dept = db.Column(db.String(100), nullable=True)
    topic = db.Column(db.String(100), nullable=True)
    no_of_days_hrs = db.Column(db.Integer, nullable=True)
    nature_of_issue = db.Column(db.String(50), nullable=True)  # Critical/Manageable/All Well
    issue_description = db.Column(db.Text, nullable=True)
    comments = db.Column(db.Text, nullable=True)

    submitter = db.relationship('User', foreign_keys='Team2TrainingDetails.submitted_by',
                                backref=db.backref('submitted_team2_training_details', lazy=True))
    
#Section 27: Manpower Planning
class Team2ManpowerPlanning(BaseForm):
    __tablename__ = 'team2_manpower_planning'

    mp_department = db.Column(db.String(100), nullable=True)  # Department
    mp_staff_name = db.Column(db.String(255), nullable=True)  # Name of Staff Planned to Relieve / Dept Change
    mp_designation = db.Column(db.String(100), nullable=True)  # Designation
    mp_grades = db.Column(db.String(100), nullable=True)  # Grades Handling
    mp_relieve_date = db.Column(db.Date, nullable=True)  # Expected Date of Relieving
    mp_budget = db.Column(db.Float, nullable=True)  # Budget
    mp_new_find = db.Column(db.String(255), nullable=True)  # New Find

    # Relationships
    submitter = db.relationship(
        'User',
        foreign_keys='Team2ManpowerPlanning.submitted_by',
        backref=db.backref('submitted_team2_manpower_planning', lazy=True)
    )

# Section 28: Overall Consolidation
class Team2OverallConsolidation(BaseForm):
    __tablename__ = 'team2_overall_consolidation'

    oc_department = db.Column(db.String(100), nullable=True)   # Department
    oc_total = db.Column(db.Integer, nullable=True)            # Total
    oc_required = db.Column(db.Integer, nullable=True)         # Required
    oc_shortlisted = db.Column(db.Integer, nullable=True)      # Shortlisted
    oc_waiting_list = db.Column(db.Integer, nullable=True)     # Waiting List
    oc_yet_to_find = db.Column(db.Integer, nullable=True)      # Yet to Find

    # Relationships
    submitter = db.relationship(
        'User',
        foreign_keys='Team2OverallConsolidation.submitted_by',
        backref=db.backref('submitted_team2_overall_consolidation', lazy=True)
    )

# =========================
# Section XX: Uniform Details
# =========================
class Team2UniformDetails(BaseForm):
    __tablename__ = 'uniform_details'

    ud_uniform = db.Column(db.String(200), nullable=True)           # Uniform
    ud_designation = db.Column(db.String(200), nullable=True)       # Designation
    ud_details = db.Column(db.Text, nullable=True)                  # Details of the Uniform
    ud_remarks = db.Column(db.Text, nullable=True)                  # Remarks
    ud_closure_date = db.Column(db.Date, nullable=True)             # Closure Date

    # Relationship to User who submitted
    submitter = db.relationship(
        'User',
        foreign_keys='Team2UniformDetails.submitted_by',
        backref=db.backref('submitted_team2_uniform_details', lazy=True)
    )


# =========================
# Section XX: Department Wise Uniform Details
# =========================
class Team2DepartmentWiseUniformDetails(BaseForm):
    __tablename__ = 'department_wise_uniform_details'

    dwud_department = db.Column(db.String(200), nullable=True)      # Department
    dwud_total = db.Column(db.Integer, nullable=True)               # Total
    dwud_completed = db.Column(db.Integer, nullable=True)           # Completed
    dwud_pending = db.Column(db.Integer, nullable=True)             # Pending
    dwud_names = db.Column(db.Text, nullable=True)                  # Names
    dwud_dress_code = db.Column(db.String(200), nullable=True)      # Dress Code
    dwud_status = db.Column(db.String(50), nullable=True)           # Status (completed / in_progress / pending)

    # Relationship to User who submitted
    submitter = db.relationship(
        'User',
        foreign_keys='Team2DepartmentWiseUniformDetails.submitted_by',
        backref=db.backref('submitted_team2_department_wise_uniform_details', lazy=True)
    )


# Team 3 Form Models

class Team3Audit(BaseForm):
    __tablename__ = 'team3_audit'

    frequency = db.Column(db.String(50), nullable=False)
    audit_components = db.Column(db.Text, nullable=False)
    audit_by = db.Column(db.String(100), nullable=False)
    audit_time = db.Column(db.Time, nullable=False)
    issue_nature = db.Column(db.String(20), nullable=False)  # critical/manageable/all_well
    audit_remarks = db.Column(db.Text, nullable=True)
    # Relationships
    submitter = db.relationship('User', foreign_keys='Team3Audit.submitted_by', backref=db.backref('submitted_team3_audit', lazy=True)) 


class Team3NewAudit(BaseForm):
    __tablename__ = 'team3_new_audit'

    frequency = db.Column(db.String(50), nullable=False)
    component = db.Column(db.Text, nullable=False)
    audited_by = db.Column(db.String(100), nullable=False)
    staff_name = db.Column(db.String(100), nullable=False)
    grade = db.Column(db.String(50), nullable=False)
    section = db.Column(db.String(50), nullable=False)
    specification = db.Column(db.Text, nullable=True)
    issue_nature = db.Column(db.String(20), nullable=False)  # critical/manageable/all_well
    remark = db.Column(db.Text, nullable=True)

    # Optional: store uploaded media file in DB BLOB store
    media_file_id = db.Column(db.Integer, db.ForeignKey('file_storage.file_id'), nullable=True)

    # Relationships
    submitter = db.relationship(
        'User',
        foreign_keys='Team3NewAudit.submitted_by',
        backref=db.backref('submitted_team3_new_audit', lazy=True)
    )
    media_file = db.relationship('FileStorage', foreign_keys=[media_file_id], backref='team3_new_audits')


class Action(db.Model):
    __tablename__ = 'actions'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    assigned_user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    priority = db.Column(db.String(20), nullable=False)
    due_date = db.Column(db.DateTime, nullable=False)
    action_text = db.Column(db.Text, nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(ZoneInfo('Asia/Kolkata')))
    status = db.Column(db.String(20), nullable=False, default='Pending')
    completed_at = db.Column(db.DateTime(timezone=True), nullable=True, default=lambda: datetime.now(ZoneInfo('Asia/Kolkata')))
    completion_message = db.Column(db.Text, nullable=True)
    loop_message = db.Column(db.Text, nullable=True)
    parent_action_id = db.Column(db.Integer, db.ForeignKey('actions.id'), nullable=True)

    # Relationships
    assigned_user = db.relationship('User', foreign_keys=[assigned_user_id], backref='assigned_actions')
    creator = db.relationship('User', foreign_keys=[created_by], backref='created_actions')
    parent_action = db.relationship('Action', remote_side=[id], backref='child_actions')

    @property
    def time_taken(self):
        if self.completed_at:
            return self.completed_at - self.created_at
        return None

class Acknowledgement(db.Model):
    __tablename__ = 'acknowledgements'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    acknowledged_at = db.Column(db.DateTime(timezone=True), nullable=True, default=lambda: datetime.now(ZoneInfo('Asia/Kolkata')))

    user = db.relationship('User', backref='acknowledgements')

    def __repr__(self):
        return f'<Acknowledgement {self.user_id} {self.date} {self.acknowledged_at}>'

class Team1ASAGeneral(BaseForm):
    __tablename__ = 'team1_asa_general'
    
    # General ASA data stored as JSON
    # Format: {"activity_name": {"strength": 0, "enrolled": 0, "enrol_pct": 0, "activities": "", "expected": 0, "attended": 0, "attend_pct": 0}}
    asa_general_data = db.Column(db.JSON)
    
    # Relationships
    submitter = db.relationship('User', foreign_keys='Team1ASAGeneral.submitted_by', backref=db.backref('submitted_team1_asa_general', lazy=True))

class FileStorage(db.Model):
    __tablename__ = 'file_storage'
    
    file_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    filename = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    file_data = db.Column(db.LargeBinary(length=4294967295), nullable=False)  # LONGBLOB storage (up to 4GB)
    file_size = db.Column(db.Integer, nullable=False)
    mime_type = db.Column(db.String(100), nullable=False)
    uploaded_by = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    uploaded_at = db.Column(db.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(ZoneInfo('Asia/Kolkata')))
    
    # Relationships
    user = db.relationship('User', backref='uploaded_files')
    
    def __repr__(self):
        return f'<FileStorage {self.original_filename}>'


# =====================================================
#  CAPA / Critical audit workflow
#  Audit -> Recipient -> Audit Review -> Closure
# =====================================================

# Workflow statuses. The backend is the only writer of CapaFinding.status --
# these values are never rendered as a user-editable form field.
CAPA_STATUS_OPEN = 'OPEN'
CAPA_STATUS_PENDING_RECIPIENT = 'PENDING_RECIPIENT_RESPONSE'
CAPA_STATUS_PENDING_AUDIT = 'PENDING_AUDIT_REVIEW'
CAPA_STATUS_REVISION_REQUIRED = 'CAPA_REVISION_REQUIRED'
CAPA_STATUS_CLOSED = 'CLOSED'

CAPA_STATUSES = (
    CAPA_STATUS_OPEN,
    CAPA_STATUS_PENDING_RECIPIENT,
    CAPA_STATUS_PENDING_AUDIT,
    CAPA_STATUS_REVISION_REQUIRED,
    CAPA_STATUS_CLOSED,
)

CAPA_STATUS_LABELS = {
    CAPA_STATUS_OPEN: 'Open',
    CAPA_STATUS_PENDING_RECIPIENT: 'Pending Recipient Response',
    CAPA_STATUS_PENDING_AUDIT: 'Pending Audit Review',
    CAPA_STATUS_REVISION_REQUIRED: 'CAPA Revision Required',
    CAPA_STATUS_CLOSED: 'Closed',
}

# CSS suffix for the existing .status-badge convention used across the app.
CAPA_STATUS_CSS = {
    CAPA_STATUS_OPEN: 'capa-open',
    CAPA_STATUS_PENDING_RECIPIENT: 'capa-pending-recipient',
    CAPA_STATUS_PENDING_AUDIT: 'capa-pending-audit',
    CAPA_STATUS_REVISION_REQUIRED: 'capa-revision',
    CAPA_STATUS_CLOSED: 'capa-closed',
}

CAPA_PRIORITIES = ('Low', 'Medium', 'High', 'Critical')

CAPA_DECISION_ACCEPTED = 'ACCEPTED'
CAPA_DECISION_NOT_ACCEPTED = 'NOT_ACCEPTED'

# Attachment stages -- which step of the workflow uploaded the evidence.
CAPA_STAGE_FINDING = 'FINDING'
CAPA_STAGE_RESPONSE = 'RESPONSE'
CAPA_STAGE_REVIEW = 'REVIEW'

class CapaFinding(BaseForm):
    """One audit finding carried through the full CAPA workflow.

    Inherits form_id / team_id / submitted_by / submitted_at from BaseForm, so
    the creator and creation time live in submitted_by / submitted_at (exposed
    below as created_by / created_at for readability).
    """
    __tablename__ = 'capa_findings'

    # --- Audit finding (created by Team 3 / Audit, immutable afterwards) ---
    audit_reference = db.Column(db.String(20), unique=True, nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    frequency = db.Column(db.String(50), nullable=True)
    component = db.Column(db.String(255), nullable=True)
    audited_by = db.Column(db.String(100), nullable=True)
    staff_name = db.Column(db.String(100), nullable=True)
    grade = db.Column(db.String(50), nullable=True)
    section = db.Column(db.String(50), nullable=True)
    specification = db.Column(db.Text, nullable=True)
    nature_of_issue = db.Column(db.String(100), nullable=False)
    remark = db.Column(db.Text, nullable=True)
    priority = db.Column(db.String(20), nullable=False, default='Medium')
    audit_date = db.Column(db.Date, nullable=False)

    # Recipient is stored as a reference to the real users table, never as text.
    recipient_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)

    # --- Workflow state (backend-controlled only) ---
    status = db.Column(db.String(32), nullable=False, default=CAPA_STATUS_PENDING_RECIPIENT)
    revision_count = db.Column(db.Integer, nullable=False, default=0)

    # --- Recipient response (CAPA 1) ---
    action_taken_report = db.Column(db.Text, nullable=True)
    root_cause_analysis = db.Column(db.Text, nullable=True)
    capa_1 = db.Column(db.Text, nullable=True)
    capa_1_submitted_at = db.Column(db.DateTime(timezone=True), nullable=True)
    capa_1_submitted_by = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=True)

    # --- Audit response (CAPA 2) ---
    capa_2 = db.Column(db.Text, nullable=True)
    capa_2_submitted_at = db.Column(db.DateTime(timezone=True), nullable=True)
    capa_2_submitted_by = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=True)

    # --- Audit decision / closure ---
    audit_decision = db.Column(db.String(16), nullable=True)  # ACCEPTED | NOT_ACCEPTED
    audit_justification = db.Column(db.Text, nullable=True)   # mandatory when NOT_ACCEPTED
    audit_reviewed_by = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=True)
    audit_reviewed_at = db.Column(db.DateTime(timezone=True), nullable=True)
    closed_at = db.Column(db.DateTime(timezone=True), nullable=True)

    updated_at = db.Column(db.DateTime(timezone=True), nullable=False,
                           default=lambda: datetime.now(ZoneInfo('Asia/Kolkata')),
                           onupdate=lambda: datetime.now(ZoneInfo('Asia/Kolkata')))

    # --- Relationships (explicit foreign_keys: several columns point at users) ---
    creator = db.relationship('User', foreign_keys='CapaFinding.submitted_by',
                              backref=db.backref('created_capa_findings', lazy='dynamic'))
    recipient = db.relationship('User', foreign_keys='CapaFinding.recipient_id',
                                backref=db.backref('assigned_capa_findings', lazy='dynamic'))
    capa_1_author = db.relationship('User', foreign_keys='CapaFinding.capa_1_submitted_by')
    capa_2_author = db.relationship('User', foreign_keys='CapaFinding.capa_2_submitted_by')
    reviewer = db.relationship('User', foreign_keys='CapaFinding.audit_reviewed_by')

    # id is the tie-breaker: MySQL DATETIME has no sub-second precision, so
    # several events written in the same request share one created_at.
    events = db.relationship('CapaEvent', back_populates='finding',
                             order_by='CapaEvent.created_at, CapaEvent.id',
                             cascade='all, delete-orphan', lazy='select')
    attachments = db.relationship('CapaAttachment', back_populates='finding',
                                  order_by='CapaAttachment.uploaded_at, CapaAttachment.id',
                                  cascade='all, delete-orphan', lazy='select')

    # created_by / created_at are the spec's names for BaseForm's columns.
    @property
    def created_by(self):
        return self.submitted_by

    @property
    def created_at(self):
        return self.submitted_at

    @property
    def status_label(self):
        return CAPA_STATUS_LABELS.get(self.status, self.status)

    @property
    def status_css(self):
        return CAPA_STATUS_CSS.get(self.status, 'capa-open')

    @property
    def is_closed(self):
        return self.status == CAPA_STATUS_CLOSED

    @property
    def awaiting_recipient(self):
        return self.status in (CAPA_STATUS_PENDING_RECIPIENT, CAPA_STATUS_REVISION_REQUIRED)

    @property
    def awaiting_audit_review(self):
        return self.status == CAPA_STATUS_PENDING_AUDIT

    def files_for_stage(self, stage):
        return [a for a in self.attachments if a.stage == stage]

    def __repr__(self):
        return f'<CapaFinding {self.audit_reference} {self.status}>'

class CapaEvent(db.Model):
    """Append-only audit trail for a CAPA finding.

    Rows are never updated or deleted -- every workflow action adds one row so
    the full history (who, what, when, old status -> new status) is preserved.
    """
    __tablename__ = 'capa_events'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    finding_id = db.Column(db.Integer, db.ForeignKey('capa_findings.form_id'), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    action = db.Column(db.String(64), nullable=False)
    old_status = db.Column(db.String(32), nullable=True)
    new_status = db.Column(db.String(32), nullable=True)
    comment = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False,
                           default=lambda: datetime.now(ZoneInfo('Asia/Kolkata')))

    finding = db.relationship('CapaFinding', back_populates='events')
    user = db.relationship('User', foreign_keys=[user_id])

    def __repr__(self):
        return f'<CapaEvent {self.finding_id} {self.action}>'


class CapaAttachment(db.Model):
    """Links a CAPA finding to files in the existing FileStorage table.

    A join table rather than FK columns on capa_findings, so each workflow stage
    can carry any number of files without duplicating the file-storage system.
    """
    __tablename__ = 'capa_attachments'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    finding_id = db.Column(db.Integer, db.ForeignKey('capa_findings.form_id'), nullable=False, index=True)
    file_id = db.Column(db.Integer, db.ForeignKey('file_storage.file_id'), nullable=False)
    stage = db.Column(db.String(16), nullable=False, default=CAPA_STAGE_FINDING)
    uploaded_by = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    uploaded_at = db.Column(db.DateTime(timezone=True), nullable=False,
                            default=lambda: datetime.now(ZoneInfo('Asia/Kolkata')))

    finding = db.relationship('CapaFinding', back_populates='attachments')
    file = db.relationship('FileStorage', foreign_keys=[file_id])
    uploader = db.relationship('User', foreign_keys=[uploaded_by])

    def __repr__(self):
        return f'<CapaAttachment {self.finding_id} {self.stage} {self.file_id}>'