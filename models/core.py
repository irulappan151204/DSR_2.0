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

    @property
    def is_active(self):
        """Flask-Login contract: Returns False if the account has been deactivated."""
        return not (self.password and self.password.startswith('!DISABLED$'))

    def deactivate(self):
        """Mark account inactive via the shadow flag."""
        if self.password and not self.password.startswith('!DISABLED$'):
            self.password = f"!DISABLED${self.password}"

    def reactivate(self):
        """Restore account to active state."""
        if self.password and self.password.startswith('!DISABLED$'):
            self.password = self.password.replace('!DISABLED$', '', 1)

class Team(db.Model):
    __tablename__ = 'teams'
    
    team_id = db.Column(db.Integer, primary_key=True)
    team_name = db.Column(db.String(100), unique=True, nullable=False)
    lead_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    
    # Relationships
    team_lead = db.relationship('User', foreign_keys=[lead_id], back_populates='led_team')
    members = db.relationship('User', back_populates='team', foreign_keys='User.team_id')
    issues = db.relationship('Issue', backref=db.backref('team', uselist=False), lazy=True)
    
    @property
    def designated_lead(self):
        """Returns the assigned team lead, falling back to an active member with role 'Team Lead' if lead_id is unset."""
        if self.lead_id and self.team_lead:
            return self.team_lead
        for member in self.members:
            if member.role == 'Team Lead' and member.is_active:
                return member
        for member in self.members:
            if member.role == 'Team Lead':
                return member
        return None
    
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
