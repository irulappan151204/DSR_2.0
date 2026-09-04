from models import (
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
)

TEAM1_MODELS = [
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

def get_initial_team1_issue_nature():
    return {
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


def populate_team1_issue_nature(team1, date_filter_fn):
    team1_issue_nature = get_initial_team1_issue_nature()
    if not team1:
        return team1_issue_nature

     # Get Team 1 Calendar Schedule data
    query_filters = [Team1CalendarSchedule.team_id == team1.team_id] + date_filter_fn(Team1CalendarSchedule)
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
    query_filters = [Team1StudentAttendance.team_id == team1.team_id] + date_filter_fn(Team1StudentAttendance)
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
    query_filters = [Team1StudentGrooming.team_id == team1.team_id] + date_filter_fn(Team1StudentGrooming)
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
    query_filters = [Team1StudentLateComing.team_id == team1.team_id] + date_filter_fn(Team1StudentLateComing)
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
    query_filters = [Team1AdmissionStatus.team_id == team1.team_id] + date_filter_fn(Team1AdmissionStatus)
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
    query_filters = [Team1TransferCertificate.team_id == team1.team_id] + date_filter_fn(Team1TransferCertificate)
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
    query_filters = [Team1ParentActivity.team_id == team1.team_id] + date_filter_fn(Team1ParentActivity)
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
    query_filters = [Team1ParentVisit.team_id == team1.team_id] + date_filter_fn(Team1ParentVisit)
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
    query_filters = [Team1ExamSchedule.team_id == team1.team_id] + date_filter_fn(Team1ExamSchedule)
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
    query_filters = [Team1ExternalInfo.team_id == team1.team_id] + date_filter_fn(Team1ExternalInfo)
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
    query_filters = [Team1SickBay.team_id == team1.team_id] + date_filter_fn(Team1SickBay)
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
    query_filters = [Team1HomeSchoolComm.team_id == team1.team_id] + date_filter_fn(Team1HomeSchoolComm)
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
    query_filters = [Team1Disciplinary.team_id == team1.team_id] + date_filter_fn(Team1Disciplinary)
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
    query_filters = [Team1Logistics.team_id == team1.team_id] + date_filter_fn(Team1Logistics)
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
    query_filters = [Team1CompetitionCert.team_id == team1.team_id] + date_filter_fn(Team1CompetitionCert)
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
    query_filters = [Team1StaffConcern.team_id == team1.team_id] + date_filter_fn(Team1StaffConcern)
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
    query_filters = [Team1StudentConcern.team_id == team1.team_id] + date_filter_fn(Team1StudentConcern)
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
    query_filters = [Team1ParentConcern.team_id == team1.team_id] + date_filter_fn(Team1ParentConcern)
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
    query_filters = [Team1ParentConcernDetail.team_id == team1.team_id] + date_filter_fn(Team1ParentConcernDetail)
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
    query_filters = [Team1SpecialEducation.team_id == team1.team_id] + date_filter_fn(Team1SpecialEducation)
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
    query_filters = [Team1SchoolCounsellor.team_id == team1.team_id] + date_filter_fn(Team1SchoolCounsellor)
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


    return team1_issue_nature
