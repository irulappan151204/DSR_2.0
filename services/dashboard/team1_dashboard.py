# services/dashboard/team1_dashboard.py
from datetime import datetime, timedelta
from extensions import db
from models import (
    Team, Team1CalendarSchedule, Team1StudentAttendance, Team1ParentConcernDetail,
    Team1ASAActivities, Team1ASASports, Team1ASAGeneral, Team1StudentGrooming,
    Team1StudentLateComing, Team1AdmissionStatus, Team1TransferCertificate,
    Team1ParentActivity, Team1ParentVisit, Team1ExamSchedule, Team1ExternalInfo,
    Team1SickBay, Team1HomeSchoolComm, Team1Disciplinary, Team1Logistics,
    Team1CompetitionCert, Team1StaffConcern, Team1StudentConcern, Team1ParentConcern,
    Team1AEPAttendance, Team1ExtendedClassAttendance, Team1TrainingSession,
    Team1WeeklyMeeting, Team1SpecialEducation, Team1Hostel, Team1SEC,
    Team1SchoolCounsellor, Team1Scholorius
)

def get_team1_data(selected_date_obj, start_of_day, end_of_day, show_all_dates):
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

    return {
        'team1_calendar_data': team1_calendar_data,
        'team1_asa_data': team1_asa_data,
        'team1_asa_sports_data': team1_asa_sports_data,
        'team1_asa_general_data': team1_asa_general_data,
        'team1_student_attendance_data': team1_student_attendance_data,
        'team1_student_grooming_data': team1_student_grooming_data,
        'team1_student_late_coming_data': team1_student_late_coming_data,
        'team1_admission_status_data': team1_admission_status_data,
        'team1_transfer_certificate_data': team1_transfer_certificate_data,
        'team1_parent_activity_data': team1_parent_activity_data,
        'team1_parent_visit_data': team1_parent_visit_data,
        'team1_exam_schedule_data': team1_exam_schedule_data,
        'team1_external_info_data': team1_external_info_data,
        'team1_sick_bay_data': team1_sick_bay_data,
        'team1_home_school_communication_data': team1_home_school_communication_data,
        'team1_disciplinary_measures_data': team1_disciplinary_measures_data,
        'team1_logistics_data': team1_logistics_data,
        'team1_competition_certificate_data': team1_competition_certificate_data,
        'team1_staff_concern_data': team1_staff_concern_data,
        'team1_student_concern_data': team1_student_concern_data,
        'team1_parent_concern_data': team1_parent_concern_data,
        'team1_parent_concern_detail_data': team1_parent_concern_detail_data,
        'team1_aep_attendance_data': team1_aep_attendance_data,
        'team1_extended_class_data': team1_extended_class_data,
        'team1_training_session_data': team1_training_session_data,
        'team1_weekly_meeting_data': team1_weekly_meeting_data,
        'team1_special_education_data': team1_special_education_data,
        'team1_hostel_data': team1_hostel_data,
        'team1_sec_data': team1_sec_data,
        'team1_school_counsellor_data': team1_school_counsellor_data,
        'team1_scholorius_data': team1_scholorius_data,
    }

def get_empty_team1_data():
    return {
        'team1_calendar_data': [],
        'team1_asa_data': [],
        'team1_asa_sports_data': [],
        'team1_asa_general_data': [],
        'team1_student_attendance_data': [],
        'team1_student_grooming_data': [],
        'team1_student_late_coming_data': [],
        'team1_admission_status_data': [],
        'team1_transfer_certificate_data': [],
        'team1_parent_activity_data': [],
        'team1_parent_visit_data': [],
        'team1_exam_schedule_data': [],
        'team1_external_info_data': [],
        'team1_sick_bay_data': [],
        'team1_home_school_communication_data': [],
        'team1_disciplinary_measures_data': [],
        'team1_logistics_data': [],
        'team1_competition_certificate_data': [],
        'team1_staff_concern_data': [],
        'team1_student_concern_data': [],
        'team1_parent_concern_data': [],
        'team1_parent_concern_detail_data': [],
        'team1_aep_attendance_data': [],
        'team1_extended_class_data': [],
        'team1_training_session_data': [],
        'team1_weekly_meeting_data': [],
        'team1_special_education_data': [],
        'team1_hostel_data': [],
        'team1_sec_data': [],
        'team1_school_counsellor_data': [],
        'team1_scholorius_data': [],
    }
