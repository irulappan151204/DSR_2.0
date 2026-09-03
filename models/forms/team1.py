from extensions import db
from .base import BaseForm

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


class Team1ASAGeneral(BaseForm):
    __tablename__ = 'team1_asa_general'
    
    # General ASA data stored as JSON
    # Format: {"activity_name": {"strength": 0, "enrolled": 0, "enrol_pct": 0, "activities": "", "expected": 0, "attended": 0, "attend_pct": 0}}
    asa_general_data = db.Column(db.JSON)
    
    # Relationships
    submitter = db.relationship('User', foreign_keys='Team1ASAGeneral.submitted_by', backref=db.backref('submitted_team1_asa_general', lazy=True))

