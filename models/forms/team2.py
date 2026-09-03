from extensions import db
from .base import BaseForm

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

