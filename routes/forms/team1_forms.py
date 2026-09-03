# routes/forms/team1_forms.py
from flask import request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from datetime import datetime
from zoneinfo import ZoneInfo
from werkzeug.utils import secure_filename
from extensions import db
from utils.helpers import safe_int, safe_float, safe_date, safe_time
from models import (
    Team1CalendarSchedule, Team1StudentAttendance, Team1ParentConcernDetail,
    Team1ASAActivities, Team1ASASports, Team1ASAGeneral, Team1StudentGrooming,
    Team1StudentLateComing, Team1AdmissionStatus, Team1TransferCertificate,
    Team1ParentActivity, Team1ParentVisit, Team1ExamSchedule, Team1ExternalInfo,
    Team1SickBay, Team1HomeSchoolComm, Team1Disciplinary, Team1Logistics,
    Team1CompetitionCert, Team1StaffConcern, Team1ParentConcern, Team1StudentConcern,
    Team1AEPAttendance, Team1ExtendedClassAttendance, Team1TrainingSession,
    Team1WeeklyMeeting, Team1SpecialEducation, Team1Hostel, Team1SEC,
    Team1SchoolCounsellor, Team1Scholorius, FileStorage
)

def register_team1_forms(app):
    """Register all 31 Team 1 (Academics) form submission routes."""
    # Team 1 Calendar
    @app.route('/submit_team1_calendar', methods=['POST'])
    @login_required
    def submit_team1_calendar():
        try:
            form_entry = Team1CalendarSchedule(
                team_id=current_user.team_id,
                submitted_by=current_user.user_id,
                submitted_at=now_ist(),

                # Jr. School
                cal_session_jr=request.form.get('cal_session_jr'),
                cal_dept_jr=request.form.get('cal_dept_jr'),
                cal_plan_jr=request.form.get('cal_plan_jr'),
                cal_total_jr=request.form.get('cal_total_jr'),
                cal_expected_jr=request.form.get('cal_expected_jr'),
                cal_present_pct_jr=request.form.get('cal_present_pct_jr'),
                cal_absent_pct_jr=request.form.get('cal_absent_pct_jr'),
                cal_issue_nature_jr=request.form.get('cal_issue_nature_jr'),
                cal_issue_desc_jr=request.form.get('cal_issue_desc_jr'),
                cal_comment_jr=request.form.get('cal_comment_jr'),

                # Sr. School
                cal_session_sr=request.form.get('cal_session_sr'),
                cal_dept_sr=request.form.get('cal_dept_sr'),
                cal_plan_sr=request.form.get('cal_plan_sr'),
                cal_total_sr=request.form.get('cal_total_sr'),
                cal_expected_sr=request.form.get('cal_expected_sr'),
                cal_present_pct_sr=request.form.get('cal_present_pct_sr'),
                cal_absent_pct_sr=request.form.get('cal_absent_pct_sr'),
                cal_issue_nature_sr=request.form.get('cal_issue_nature_sr'),
                cal_issue_desc_sr=request.form.get('cal_issue_desc_sr'),
                cal_comment_sr=request.form.get('cal_comment_sr')
            )

            db.session.add(form_entry)
            db.session.commit()

            return jsonify({'message': 'Calendar schedule submitted successfully!'})

        except Exception as e:
            db.session.rollback()
            print("Error submitting calendar schedule:", str(e))
            return jsonify({'error': 'Failed to submit calendar schedule. Please try again.'}), 500


    # Team 1 ASA 2 Activities
    @app.route('/submit_team1_asa', methods=['POST'])
    @login_required
    def submit_team1_asa():
        try:
            form_entry = Team1ASAActivities(
                team_id=current_user.team_id,
                submitted_by=current_user.user_id,
                # Paid Activities
                asa_strength_paid=safe_int(request.form.get('asa_strength_paid')),
                asa_enrolled_paid=safe_int(request.form.get('asa_enrolled_paid')),
                asa_enrol_pct_paid=safe_float(request.form.get('asa_enrol_pct_paid')),
                asa_activities_paid=request.form.get('asa_activities_paid'),
                asa_expected_paid=safe_int(request.form.get('asa_expected_paid')),
                asa_attended_paid=safe_int(request.form.get('asa_attended_paid')),
                asa_attend_pct_paid=safe_float(request.form.get('asa_attend_pct_paid')),
                # Regular Activities
                asa_strength_reg=safe_int(request.form.get('asa_strength_reg')),
                asa_enrolled_reg=safe_int(request.form.get('asa_enrolled_reg')),
                asa_enrol_pct_reg=safe_float(request.form.get('asa_enrol_pct_reg')),
                asa_activities_reg=request.form.get('asa_activities_reg'),
                asa_expected_reg=safe_int(request.form.get('asa_expected_reg')),
                asa_attended_reg=safe_int(request.form.get('asa_attended_reg')),
                asa_attend_pct_reg=safe_float(request.form.get('asa_attend_pct_reg')),
                # Rifle Shooting
                asa_strength_rifle=safe_int(request.form.get('asa_strength_rifle')),
                asa_enrolled_rifle=safe_int(request.form.get('asa_enrolled_rifle')),
                asa_enrol_pct_rifle=safe_float(request.form.get('asa_enrol_pct_rifle')),
                asa_activities_rifle=request.form.get('asa_activities_rifle'),
                asa_expected_rifle=safe_int(request.form.get('asa_expected_rifle')),
                asa_attended_rifle=safe_int(request.form.get('asa_attended_rifle')),
                asa_attend_pct_rifle=safe_float(request.form.get('asa_attend_pct_rifle')),
                # NCC
                asa_strength_ncc=safe_int(request.form.get('asa_strength_ncc')),
                asa_enrolled_ncc=safe_int(request.form.get('asa_enrolled_ncc')),
                asa_enrol_pct_ncc=safe_float(request.form.get('asa_enrol_pct_ncc')),
                asa_activities_ncc=request.form.get('asa_activities_ncc'),
                asa_expected_ncc=safe_int(request.form.get('asa_expected_ncc')),
                asa_attended_ncc=safe_int(request.form.get('asa_attended_ncc')),
                asa_attend_pct_ncc=safe_float(request.form.get('asa_attend_pct_ncc'))
            )

            db.session.add(form_entry)
            db.session.commit()

            return jsonify({'message': 'ASA activities submitted successfully!'})
        except Exception as e:
            db.session.rollback()
            print("Error submitting ASA activities:", str(e))
            return jsonify({'error': 'Failed to submit ASA activities. Please try again.'}), 500

    # Team 1 ASA Sports
    @app.route('/submit_team1_asa_sports', methods=['POST'])
    @login_required
    def submit_team1_asa_sports():
        try:
            # Get form data
            form_data = request.form.to_dict()

            # Activities to check
            activities = ['athletics', 'basketball', 'football', 'throwball','total']

            # Build JSON data structure
            sports_data = {}
            has_data = False

            for activity in activities:
                # Check if any field has data for this activity
                if any([
                    form_data.get(f'asa_strength_{activity}'),
                    form_data.get(f'asa_enrolled_{activity}'),
                    form_data.get(f'asa_expected_{activity}'),
                    form_data.get(f'asa_attended_{activity}')
                ]):
                    has_data = True
                    activity_data = {
                        'strength': int(form_data.get(f'asa_strength_{activity}', 0)) if form_data.get(f'asa_strength_{activity}') else None,
                        'enrolled': int(form_data.get(f'asa_enrolled_{activity}', 0)) if form_data.get(f'asa_enrolled_{activity}') else None,
                        'enrol_pct': float(form_data.get(f'asa_enrol_pct_{activity}', 0)) if form_data.get(f'asa_enrol_pct_{activity}') else None,
                        'expected': int(form_data.get(f'asa_expected_{activity}', 0)) if form_data.get(f'asa_expected_{activity}') else None,
                        'attended': int(form_data.get(f'asa_attended_{activity}', 0)) if form_data.get(f'asa_attended_{activity}') else None,
                        'attend_pct': float(form_data.get(f'asa_attend_pct_{activity}', 0)) if form_data.get(f'asa_attend_pct_{activity}') else None,
                    }
                    sports_data[activity] = activity_data

            if not has_data:
                return jsonify({'message': 'No data provided for ASA sports submission.'})

            # Create new ASA Sports record
            form_entry = Team1ASASports(
                team_id=current_user.team_id,
                submitted_by=current_user.user_id,
                asa_sports_data=sports_data
            )

            db.session.add(form_entry)
            db.session.commit()

            return jsonify({'message': 'ASA sports submitted successfully!'})

        except Exception as e:
            db.session.rollback()
            print("Error submitting ASA sports:", str(e))
            return jsonify({'error': 'Failed to submit ASA sports. Please try again.'}), 500

    # Team 1 ASA General
    @app.route('/submit_team1_asa_general', methods=['POST'])
    @login_required
    def submit_team1_asa_general():
        try:
            # Get form data
            form_data = request.form.to_dict()

            # Activities to check
            activities = ['taekwondo', 'silambam', 'kungfu', 'yoga', 'tabletennis', 'skating', 
                         'classicaldance', 'westerndance', 'keyboard', 'guitar', 'drums', 'total']

            # Build JSON data structure
            general_data = {}
            has_data = False

            for activity in activities:
                # Check if any field has data for this activity
                if any([
                    form_data.get(f'asa_strength_{activity}'),
                    form_data.get(f'asa_enrolled_{activity}'),
                    form_data.get(f'asa_expected_{activity}'),
                    form_data.get(f'asa_attended_{activity}')
                ]):
                    has_data = True
                    activity_data = {
                        'strength': int(form_data.get(f'asa_strength_{activity}', 0)) if form_data.get(f'asa_strength_{activity}') else None,
                        'enrolled': int(form_data.get(f'asa_enrolled_{activity}', 0)) if form_data.get(f'asa_enrolled_{activity}') else None,
                        'enrol_pct': float(form_data.get(f'asa_enrol_pct_{activity}', 0)) if form_data.get(f'asa_enrol_pct_{activity}') else None,
                        'expected': int(form_data.get(f'asa_expected_{activity}', 0)) if form_data.get(f'asa_expected_{activity}') else None,
                        'attended': int(form_data.get(f'asa_attended_{activity}', 0)) if form_data.get(f'asa_attended_{activity}') else None,
                        'attend_pct': float(form_data.get(f'asa_attend_pct_{activity}', 0)) if form_data.get(f'asa_attend_pct_{activity}') else None,
                    }
                    general_data[activity] = activity_data

            if not has_data:
                return jsonify({'message': 'No data provided for ASA General submission.'})

            # Create new ASA General record
            asa_general = Team1ASAGeneral(
                team_id=current_user.team_id,
                submitted_by=current_user.user_id,
                asa_general_data=general_data
            )

            db.session.add(asa_general)
            db.session.commit()

            return jsonify({'message': 'ASA General submitted successfully!'})

        except Exception as e:
            db.session.rollback()
            print("Error submitting ASA General:", str(e))
            return jsonify({'error': 'Failed to submit ASA General. Please try again.'}), 500

    #<!-- S.No 3: Students Attendance -->

    @app.route('/submit_student_attendance', methods=['POST'])
    @login_required
    def submit_student_attendance():
        try:
            # Create student attendance entry
            attendance_entry = Team1StudentAttendance(
                team_id=current_user.team_id,
                submitted_by=current_user.user_id,
                # Kindergarten
                att_str_kg=safe_int(request.form.get('att_str_kg')),
                att_present_kg=safe_int(request.form.get('att_present_kg')),
                att_leave_kg=safe_int(request.form.get('att_leave_kg')),
                att_absent_kg=safe_int(request.form.get('att_absent_kg')),
                att_present_pct_kg=safe_float(request.form.get('att_present_pct_kg')),
                att_issue_nature_kg=request.form.get('att_issue_nature_kg'),
                att_issue_desc_kg=request.form.get('att_issue_desc_kg'),
                att_comment_kg=request.form.get('att_comment_kg'),

                # Grades 1 to 5
                att_str_g15=safe_int(request.form.get('att_str_g15')),
                att_present_g15=safe_int(request.form.get('att_present_g15')),
                att_leave_g15=safe_int(request.form.get('att_leave_g15')),
                att_absent_g15=safe_int(request.form.get('att_absent_g15')),
                att_present_pct_g15=safe_float(request.form.get('att_present_pct_g15')),
                att_issue_nature_g15=request.form.get('att_issue_nature_g15'),
                att_issue_desc_g15=request.form.get('att_issue_desc_g15'),
                att_comment_g15=request.form.get('att_comment_g15'),

                # Grades 6 to 10
                att_str_g610=safe_int(request.form.get('att_str_g610')),
                att_present_g610=safe_int(request.form.get('att_present_g610')),
                att_leave_g610=safe_int(request.form.get('att_leave_g610')),
                att_absent_g610=safe_int(request.form.get('att_absent_g610')),
                att_present_pct_g610=safe_float(request.form.get('att_present_pct_g610')),
                att_issue_nature_g610=request.form.get('att_issue_nature_g610'),
                att_issue_desc_g610=request.form.get('att_issue_desc_g610'),
                att_comment_g610=request.form.get('att_comment_g610'),

                # Grades 11 to 12
                att_str_g1112=safe_int(request.form.get('att_str_g1112')),
                att_present_g1112=safe_int(request.form.get('att_present_g1112')),
                att_leave_g1112=safe_int(request.form.get('att_leave_g1112')),
                att_absent_g1112=safe_int(request.form.get('att_absent_g1112')),
                att_present_pct_g1112=safe_float(request.form.get('att_present_pct_g1112')),
                att_issue_nature_g1112=request.form.get('att_issue_nature_g1112'),
                att_issue_desc_g1112=request.form.get('att_issue_desc_g1112'),
                att_comment_g1112=request.form.get('att_comment_g1112'),

                # Overall
                att_str_overall=safe_int(request.form.get('att_str_overall')),
                att_present_overall=safe_int(request.form.get('att_present_overall')),
                att_leave_overall=safe_int(request.form.get('att_leave_overall')),
                att_absent_overall=safe_int(request.form.get('att_absent_overall')),
                att_present_pct_overall=safe_float(request.form.get('att_present_pct_overall')),
                att_issue_nature_overall=request.form.get('att_issue_nature_overall'),
                att_issue_desc_overall=request.form.get('att_issue_desc_overall'),
                att_comment_overall=request.form.get('att_comment_overall')
            )

            db.session.add(attendance_entry)
            db.session.commit()


            return jsonify({'message': 'Student attendance submitted successfully!'})
        except Exception as e:
            db.session.rollback()
            print("Error submitting student attendance:", str(e))
            return jsonify({'error': 'Failed to submit student attendance. Please try again.'}), 500


        #<!-- S.No 4: Students Grooming -->

    @app.route('/submit_grooming', methods=['POST'])
    @login_required
    def submit_grooming():
        try:
            # Get arrays of form data
            groom_strs = request.form.getlist('groom_str[]')
            groom_regs = request.form.getlist('groom_reg[]')
            groom_def_counts = request.form.getlist('groom_def_count[]')
            groom_def_pcts = request.form.getlist('groom_def_pct[]')
            groom_issue_natures = request.form.getlist('groom_issue_nature[]')
            groom_issue_descs = request.form.getlist('groom_issue_desc[]')
            groom_comments = request.form.getlist('groom_comment[]')

            # Create entries for each row
            for i in range(len(groom_strs)):
                grooming_entry = Team1StudentGrooming(
                    team_id=current_user.team_id,
                    submitted_by=current_user.user_id,
                    grooming_s_no=4,
                    grooming_work_activity='Students Grooming',
                    grooming_dept_category='PE',
                    grooming_total_strength=safe_int(groom_strs[i]),
                    grooming_regular_students=safe_int(groom_regs[i]),
                    grooming_defaulters_count=safe_int(groom_def_counts[i]),
                    grooming_defaulters_pct=safe_float(groom_def_pcts[i]),
                    grooming_issue_nature=groom_issue_natures[i],
                    grooming_issue_desc=groom_issue_descs[i],
                    grooming_comments=groom_comments[i]
                )

                db.session.add(grooming_entry)

            db.session.commit()

            return jsonify({'message': 'Student grooming submitted successfully!'})
        except Exception as e:
            db.session.rollback()
            print("Error submitting student grooming:", str(e))
            return jsonify({'error': 'Failed to submit student grooming. Please try again.'}), 500


        #<!-- S.No 5: Students Late Coming -->
    @app.route('/submit_latecoming', methods=['POST'])
    @login_required
    def submit_latecoming():
        try:
            # Get arrays of form data
            late_strs = request.form.getlist('late_str[]')
            late_regs = request.form.getlist('late_reg[]')
            late_def_counts = request.form.getlist('late_def_count[]')
            late_def_pcts = request.form.getlist('late_def_pct[]')
            late_issue_natures = request.form.getlist('late_issue_nature[]')
            late_issue_descs = request.form.getlist('late_issue_desc[]')
            late_comments = request.form.getlist('late_comment[]')

            # Create entries for each row
            for i in range(len(late_strs)):
                late_coming_entry = Team1StudentLateComing(
                    team_id=current_user.team_id,
                    submitted_by=current_user.user_id,
                    late_coming_s_no=5,
                    late_coming_work_activity='Students Late Coming',
                    late_coming_dept_category='PE',
                    late_coming_total_strength=safe_int(late_strs[i]),
                    late_coming_regular_students=safe_int(late_regs[i]),
                    late_coming_defaulters_count=safe_int(late_def_counts[i]),
                    late_coming_defaulters_pct=safe_float(late_def_pcts[i]),
                    late_coming_issue_nature=late_issue_natures[i],
                    late_coming_issue_desc=late_issue_descs[i],
                    late_coming_comments=late_comments[i]
                )

                db.session.add(late_coming_entry)

            db.session.commit()

            return jsonify({'message': 'Student late coming submitted successfully!'})
        except Exception as e:
            db.session.rollback()
            print("Error submitting student late coming:", str(e))
            return jsonify({'error': 'Failed to submit student late coming. Please try again.'}), 500

    # S.No 6: Admission Status
    @app.route('/submit_admission_status', methods=['POST'])
    @login_required
    def submit_admission_status():
        try:
            categories = [
                {
                    "label": "Adm Status - School",
                    "prefix": "school"
                },
                {
                    "label": "Adm. S - Bumble Bee",
                    "prefix": "bb"
                },
                {
                    "label": "Bumble B Leeds Excel",
                    "prefix": "leeds"
                }
            ]

            entries = []
            for cat in categories:
                prefix = cat["prefix"]

                total = safe_int(request.form.get(f'adm_total_{prefix}'))
                walkin = safe_int(request.form.get(f'adm_walkin_{prefix}'))
                appln = safe_int(request.form.get(f'adm_appln_{prefix}'))
                ela = safe_int(request.form.get(f'adm_ela_{prefix}'))
                recommended = safe_int(request.form.get(f'adm_recomm_{prefix}'))
                status = request.form.get(f'adm_status_{prefix}')
                issue_nature = request.form.get(f'adm_issue_nature_{prefix}')
                issue_desc = request.form.get(f'adm_issue_desc_{prefix}')
                comments = request.form.get(f'adm_comment_{prefix}')

                # Skip if everything is empty
                if not (total or walkin or appln or ela or recommended or status or issue_nature or issue_desc or comments):
                    continue

                entry = Team1AdmissionStatus(
                    team_id=current_user.team_id,
                    submitted_by=current_user.user_id,
                    admission_s_no=6,
                    admission_work_activity='Admission Status',
                    admission_dept_category=cat["label"],
                    admission_total=total,
                    admission_walkin=walkin,
                    admission_appln=appln,
                    admission_ela=ela,
                    admission_recommended=recommended,
                    admission_status=status,
                    admission_issue_nature=issue_nature,
                    admission_issue_desc=issue_desc,
                    admission_comments=comments
                )
                entries.append(entry)

            if entries:
                db.session.add_all(entries)
                db.session.commit()

            return jsonify({'message': 'Admission status submitted successfully!'})

        except Exception as e:
            db.session.rollback()
            print("Error submitting admission status:", str(e))
            return jsonify({'error': 'Failed to submit admission status. Please try again.'}), 500


    # S.No 7: Transfer Certificate
    @app.route('/submit_transfer_certificate', methods=['POST'])
    @login_required
    def submit_transfer_certificate():
        try:
            # Get lists from form
            grades = request.form.getlist('tc_grade[]')
            names = request.form.getlist('tc_name[]')
            years = request.form.getlist('tc_year[]')
            reasons = request.form.getlist('tc_reason[]')
            staff = request.form.getlist('tc_staff[]')
            siblings = request.form.getlist('tc_sibling[]')
            issue_natures = request.form.getlist('tc_issue_nature[]')
            issue_descs = request.form.getlist('tc_issue_desc[]')
            comments = request.form.getlist('tc_comment[]')

            entries = []
            for i in range(len(grades)):
                if grades[i].strip() and names[i].strip():  # Only if essential data is present
                    entry = Team1TransferCertificate(
                        team_id=current_user.team_id,
                        submitted_by=current_user.user_id,
                        transfer_certificate_grade=grades[i],
                        transfer_certificate_student_name=names[i],
                        transfer_certificate_year_at_qmis=years[i],
                        transfer_certificate_reason=reasons[i],
                        transfer_certificate_staff_in_charge=staff[i],
                        transfer_certificate_sibling=siblings[i],
                        transfer_certificate_issue_nature=issue_natures[i],
                        transfer_certificate_issue_desc=issue_descs[i],
                        transfer_certificate_comments=comments[i]
                    )
                    entries.append(entry)

            if entries:
                db.session.add_all(entries)
                db.session.commit()
                return jsonify({'message': 'Transfer Certificate data submitted successfully!'})
            else:
                return jsonify({'error': 'No valid rows to submit.'}), 400

        except Exception as e:
            db.session.rollback()
            print("Error in Transfer Certificate submission:", str(e))
            return jsonify({'error': 'Internal server error'}), 500

    #S.No 8: Parent Activity

    @app.route('/submit_parent_activity', methods=['POST'])
    @login_required
    def submit_parent_activity():
        try:
            # Get arrays of form data
            pa_cats = request.form.getlist('pa_cat[]')
            pa_sessions = request.form.getlist('pa_session[]')
            pa_depts = request.form.getlist('pa_dept[]')
            pa_expecteds = request.form.getlist('pa_expected[]')
            pa_reporteds = request.form.getlist('pa_reported[]')
            pa_not_reporteds = request.form.getlist('pa_not_reported[]')
            pa_present_pcts = request.form.getlist('pa_present_pct[]')
            pa_absent_pcts = request.form.getlist('pa_absent_pct[]')
            pa_issue_natures = request.form.getlist('pa_issue_nature[]')
            pa_issue_descs = request.form.getlist('pa_issue_desc[]')
            pa_comments = request.form.getlist('pa_comment[]')

            for i in range(len(pa_cats)):
                # Skip if the entire row is empty
                if not (pa_cats[i] or pa_sessions[i] or pa_depts[i] or pa_expecteds[i] or
                        pa_reporteds[i] or pa_not_reporteds[i] or pa_present_pcts[i] or
                        pa_absent_pcts[i] or pa_issue_natures[i] or pa_issue_descs[i] or pa_comments[i]):
                    continue  

                parent_activity = Team1ParentActivity(
                    team_id=current_user.team_id,
                    submitted_by=current_user.user_id,
                    parent_activity_dept_category=pa_cats[i],
                    parent_activity_session=pa_sessions[i],
                    parent_activity_dept=pa_depts[i],
                    parent_activity_expected=pa_expecteds[i],
                    parent_activity_reported=pa_reporteds[i],
                    parent_activity_not_reported=pa_not_reporteds[i],
                    parent_activity_present_pct=pa_present_pcts[i],
                    parent_activity_absent_pct=pa_absent_pcts[i],
                    parent_activity_issue_nature=pa_issue_natures[i],
                    parent_activity_issue_desc=pa_issue_descs[i],
                    parent_activity_comments=pa_comments[i]
                )
                db.session.add(parent_activity)

            db.session.commit()
            return jsonify({'message': 'Parent activity submitted successfully!'})

        except Exception as e:
            db.session.rollback()
            print("Error submitting parent activity:", str(e))
            return jsonify({'error': 'Failed to submit parent activity. Please try again.'}), 500


    # S.No 9: Parent Visit
    @app.route('/submit_team1_parent_visit', methods=['POST'])
    @login_required
    def submit_team1_parent_visit():
        try:
            # Get arrays of form data
            pv_cats = request.form.getlist('pv_cat[]')
            pv_grades = request.form.getlist('pv_grade[]')
            pv_names = request.form.getlist('pv_name[]')
            pv_years = request.form.getlist('pv_year[]')
            pv_professions = request.form.getlist('pv_profession[]')
            pv_concerns = request.form.getlist('pv_concern[]')
            pv_staffs = request.form.getlist('pv_staff[]')
            pv_issue_natures = request.form.getlist('pv_issue_nature[]')
            pv_issue_descs = request.form.getlist('pv_issue_desc[]')
            pv_comments = request.form.getlist('pv_comment[]')

            for i in range(len(pv_cats)):
                # Check if row is empty (you can adjust the fields considered "required")
                if not (pv_cats[i] or pv_grades[i] or pv_names[i] or pv_years[i] or 
                        pv_professions[i] or pv_concerns[i] or pv_staffs[i] or 
                        pv_issue_natures[i] or pv_issue_descs[i] or pv_comments[i]):
                    continue  # skip completely empty row

                parent_visit = Team1ParentVisit(
                    team_id=current_user.team_id,
                    submitted_by=current_user.user_id,
                    parent_visit_dept_category=pv_cats[i],
                    parent_visit_grade=pv_grades[i],
                    parent_visit_student_name=pv_names[i],
                    parent_visit_year_at_qmis=pv_years[i],
                    parent_visit_parents_profession=pv_professions[i],
                    parent_visit_concern_appreciation=pv_concerns[i],
                    parent_visit_staff_in_charge=pv_staffs[i],
                    parent_visit_issue_nature=pv_issue_natures[i],
                    parent_visit_issue_desc=pv_issue_descs[i],
                    parent_visit_comments=pv_comments[i]
                )
                db.session.add(parent_visit)

            db.session.commit()
            return jsonify({'message': 'Parent visit submitted successfully!'})

        except Exception as e:
            db.session.rollback()
            print("Error submitting parent visit:", str(e))
            return jsonify({'error': 'Failed to submit parent visit. Please try again.'}), 500


    # S.No 10: Exam Schedule

    @app.route('/submit_team1_exam_schedule', methods=['POST'])
    @login_required
    def submit_team1_exam_schedule():
        try:

            # Create exam schedule entry
            exam_schedule = Team1ExamSchedule(
                team_id=current_user.team_id,
                submitted_by=current_user.user_id,
                # Gr 1 to 5
                exam_schedule_g15=request.form.get('exam_sched_g15'),
                exam_str_g15=request.form.get('exam_str_g15'),
                exam_att_g15=request.form.get('exam_att_g15'),
                exam_notatt_g15=request.form.get('exam_notatt_g15'),
                exam_issue_nature_g15=request.form.get('exam_issue_nature_g15'),
                exam_issue_desc_g15=request.form.get('exam_issue_desc_g15'),
                exam_comment_g15=request.form.get('exam_comment_g15'),
                # Gr 6 to 8
                exam_schedule_g68=request.form.get('exam_sched_g68'),
                exam_str_g68=request.form.get('exam_str_g68'),
                exam_att_g68=request.form.get('exam_att_g68'),
                exam_notatt_g68=request.form.get('exam_notatt_g68'),
                exam_issue_nature_g68=request.form.get('exam_issue_nature_g68'),
                exam_issue_desc_g68=request.form.get('exam_issue_desc_g68'),
                exam_comment_g68=request.form.get('exam_comment_g68'),
                # Gr 9 and 10
                exam_schedule_g910=request.form.get('exam_sched_g910'),
                exam_str_g910=request.form.get('exam_str_g910'),
                exam_att_g910=request.form.get('exam_att_g910'),
                exam_notatt_g910=request.form.get('exam_notatt_g910'),
                exam_issue_nature_g910=request.form.get('exam_issue_nature_g910'),
                exam_issue_desc_g910=request.form.get('exam_issue_desc_g910'),
                exam_comment_g910=request.form.get('exam_comment_g910'),
                # Gr 11
                exam_schedule_g11=request.form.get('exam_sched_g11'),
                exam_str_g11=request.form.get('exam_str_g11'),
                exam_att_g11=request.form.get('exam_att_g11'),
                exam_notatt_g11=request.form.get('exam_notatt_g11'),
                exam_issue_nature_g11=request.form.get('exam_issue_nature_g11'),
                exam_issue_desc_g11=request.form.get('exam_issue_desc_g11'),
                exam_comment_g11=request.form.get('exam_comment_g11'),
                # Gr 12
                exam_schedule_g12=request.form.get('exam_sched_g12'),
                exam_str_g12=request.form.get('exam_str_g12'),
                exam_att_g12=request.form.get('exam_att_g12'),
                exam_notatt_g12=request.form.get('exam_notatt_g12'),
                exam_issue_nature_g12=request.form.get('exam_issue_nature_g12'),
                exam_issue_desc_g12=request.form.get('exam_issue_desc_g12'),
                exam_comment_g12=request.form.get('exam_comment_g12')
            )

            # Add to database
            db.session.add(exam_schedule)
            db.session.commit()


            return jsonify({'message': 'Exam schedule submitted successfully!'})
        except Exception as e:
            db.session.rollback()
            print("Error submitting exam schedule:", str(e))
            return jsonify({'error': 'Failed to submit exam schedule. Please try again.'}), 500

    # S.No 11: External Agency Info
    @app.route('/submit_team1_external_info', methods=['POST'])
    @login_required
    def submit_team1_external_info():
        try:
            # Create external info entry
            external_info = Team1ExternalInfo(
                team_id=current_user.team_id,
                submitted_by=current_user.user_id,

                # CIS
                ext_mode_receiving_cis=request.form.get('ext_mode_receiving_cis'),
                ext_mode_sending_cis=request.form.get('ext_mode_sending_cis'),
                ext_subj_cis=request.form.get('ext_subj_cis'),
                ext_from_cis=request.form.get('ext_from_cis'),
                ext_to_cis=request.form.get('ext_to_cis'),
                ext_issue_nature_cis=request.form.get('ext_issue_nature_cis'),
                ext_issue_desc_cis=request.form.get('ext_issue_desc_cis'),
                ext_comment_cis=request.form.get('ext_comment_cis'),

                # CBSE
                ext_mode_receiving_cbse=request.form.get('ext_mode_receiving_cbse'),
                ext_mode_sending_cbse=request.form.get('ext_mode_sending_cbse'),
                ext_subj_cbse=request.form.get('ext_subj_cbse'),
                ext_from_cbse=request.form.get('ext_from_cbse'),
                ext_to_cbse=request.form.get('ext_to_cbse'),
                ext_issue_nature_cbse=request.form.get('ext_issue_nature_cbse'),
                ext_issue_desc_cbse=request.form.get('ext_issue_desc_cbse'),
                ext_comment_cbse=request.form.get('ext_comment_cbse'),

                # CEO/State Government
                ext_mode_receiving_state=request.form.get('ext_mode_receiving_state'),
                ext_mode_sending_state=request.form.get('ext_mode_sending_state'),
                ext_subj_state=request.form.get('ext_subj_state'),
                ext_from_state=request.form.get('ext_from_state'),
                ext_to_state=request.form.get('ext_to_state'),
                ext_issue_nature_state=request.form.get('ext_issue_nature_state'),
                ext_issue_desc_state=request.form.get('ext_issue_desc_state'),
                ext_comment_state=request.form.get('ext_comment_state'),

                # EMIS
                ext_mode_receiving_emis=request.form.get('ext_mode_receiving_emis'),
                ext_mode_sending_emis=request.form.get('ext_mode_sending_emis'),
                ext_subj_emis=request.form.get('ext_subj_emis'),
                ext_from_emis=request.form.get('ext_from_emis'),
                ext_to_emis=request.form.get('ext_to_emis'),
                ext_issue_nature_emis=request.form.get('ext_issue_nature_emis'),
                ext_issue_desc_emis=request.form.get('ext_issue_desc_emis'),
                ext_comment_emis=request.form.get('ext_comment_emis')
            )

            db.session.add(external_info)
            db.session.commit()

            return jsonify({'message': 'External agency information submitted successfully!'})
        except Exception as e:
            db.session.rollback()
            print("Error submitting external agency information:", str(e))
            return jsonify({'error': 'Failed to submit external agency information. Please try again.'}), 500

    # S.No 12: Sick Bay
    @app.route('/submit_team1_sick_bay', methods=['POST'])
    @login_required
    def submit_team1_sick_bay():
        try:
            # Get arrays of form data
            sick_grades = request.form.getlist('sick_grade[]')
            sick_names = request.form.getlist('sick_name[]')
            sick_illnesses = request.form.getlist('sick_illness[]')
            sick_inf_bys = request.form.getlist('sick_inf_by[]')
            sick_inf_tos = request.form.getlist('sick_inf_to[]')
            sick_issue_natures = request.form.getlist('sick_issue_nature[]')
            sick_issue_descs = request.form.getlist('sick_issue_desc[]')
            sick_comments = request.form.getlist('sick_comment[]')

            # Create entries for each row
            for i in range(len(sick_grades)):
                sick_bay_entry = Team1SickBay(
                    team_id=current_user.team_id,
                    submitted_by=current_user.user_id,
                    sick_grade=sick_grades[i],
                    sick_name=sick_names[i],
                    sick_illness=sick_illnesses[i],
                    sick_inf_by=sick_inf_bys[i],
                    sick_inf_to=sick_inf_tos[i],
                    sick_issue_nature=sick_issue_natures[i],
                    sick_issue_desc=sick_issue_descs[i],
                    sick_comment=sick_comments[i]
                )

                db.session.add(sick_bay_entry)

            db.session.commit()

            return jsonify({'message': 'Sick bay information submitted successfully!'})
        except Exception as e:
            db.session.rollback()
            print("Error submitting sick bay information:", str(e))
            return jsonify({'error': 'Failed to submit sick bay information. Please try again.'}), 500

    #S.No 13: Home School Communications 
    @app.route('/submit_team1_home_school_comm', methods=['POST'])
    @login_required
    def submit_team1_home_school_comm():
        try:
            # Get arrays of form data
            hsc_grades = request.form.getlist('hsc_grade[]')
            hsc_plans = request.form.getlist('hsc_plan[]')
            hsc_print_dates = request.form.getlist('hsc_print_date[]')
            hsc_dist_dates = request.form.getlist('hsc_dist_date[]')
            hsc_activities = request.form.getlist('hsc_activity[]')
            hsc_statuses = request.form.getlist('hsc_status[]')
            hsc_issue_natures = request.form.getlist('hsc_issue_nature[]')
            hsc_issue_descs = request.form.getlist('hsc_issue_desc[]')
            hsc_comments = request.form.getlist('hsc_comment[]')

            # Create entries for each row
            for i in range(len(hsc_grades)):
                hsc_entry = Team1HomeSchoolComm(
                    team_id=current_user.team_id,
                    submitted_by=current_user.user_id,
                    hsc_grade=hsc_grades[i],
                    hsc_plan=hsc_plans[i],
                    hsc_print_date=hsc_print_dates[i],
                    hsc_dist_date=hsc_dist_dates[i],
                    hsc_activity=hsc_activities[i],
                    hsc_status=hsc_statuses[i],
                    hsc_issue_nature=hsc_issue_natures[i],
                    hsc_issue_desc=hsc_issue_descs[i],
                    hsc_comment=hsc_comments[i]
                )

                db.session.add(hsc_entry)

            db.session.commit()

            return jsonify({'message': 'Home school communication information submitted successfully!'})
        except Exception as e:
            db.session.rollback()
            print("Error submitting home school communication information:", str(e))
            return jsonify({'error': 'Failed to submit home school communication information. Please try again.'}), 500

    #S.No 14: Disciplinary Measures
    @app.route('/submit_team1_disciplinary', methods=['POST'])
    @login_required
    def submit_team1_disciplinary():
        try:
            # Get arrays of form data
            grades = request.form.getlist('disc_grade[]')
            names = request.form.getlist('disc_name[]')
            issues = request.form.getlist('disc_issue[]')
            actions = request.form.getlist('disc_action[]')
            issue_natures = request.form.getlist('disc_issue_nature[]')
            issue_descs = request.form.getlist('disc_issue_desc[]')
            comments = request.form.getlist('disc_comment[]')

            # Create disciplinary entries for each row
            for i in range(len(grades)):
                if grades[i] or names[i]:  # Only create entry if at least grade or name is provided
                    disc_entry = Team1Disciplinary(
                        team_id=current_user.team_id,
                        submitted_by=current_user.user_id,
                        disc_grade=grades[i],
                        disc_name=names[i],
                        disc_issue=issues[i],
                        disc_action=actions[i],
                        disc_issue_nature=issue_natures[i],
                        disc_issue_desc=issue_descs[i],
                        disc_comment=comments[i]
                    )
                    db.session.add(disc_entry)

            db.session.commit()


            return jsonify({'message': 'Disciplinary measures information submitted successfully!'})
        except Exception as e:
            db.session.rollback()
            print("Error submitting disciplinary measures information:", str(e))
            return jsonify({'error': 'Failed to submit disciplinary measures information. Please try again.'}), 500

    # S.No 15: Logistics 
    @app.route('/submit_team1_logistics', methods=['POST'])
    @login_required
    def submit_team1_logistics():
        try:
            # Get arrays of form data
            log_in_mats = request.form.getlist('log_in_mat[]')
            log_in_qtys = request.form.getlist('log_in_qty[]')
            log_out_mats = request.form.getlist('log_out_mat[]')
            log_out_qtys = request.form.getlist('log_out_qty[]')
            log_sale_qtys = request.form.getlist('log_sale_qty[]')
            log_sale_mats = request.form.getlist('log_sale_mat[]')
            log_issue_natures = request.form.getlist('log_issue_nature[]')
            log_issue_descs = request.form.getlist('log_issue_desc[]')
            log_comments = request.form.getlist('log_comment[]')

            # Create entries for each row
            for i in range(len(log_in_mats)):
                logistics_entry = Team1Logistics(
                    team_id=current_user.team_id,
                    submitted_by=current_user.user_id,
                    log_in_mat=log_in_mats[i],
                    log_in_qty=log_in_qtys[i],
                    log_out_mat=log_out_mats[i],
                    log_out_qty=log_out_qtys[i],
                    log_sale_qty=log_sale_qtys[i],
                    log_sale_mat=log_sale_mats[i],
                    log_issue_nature=log_issue_natures[i],
                    log_issue_desc=log_issue_descs[i],
                    log_comment=log_comments[i]
                )

                db.session.add(logistics_entry)

            db.session.commit()

            return jsonify({'message': 'Logistics information submitted successfully!'})
        except Exception as e:
            db.session.rollback()
            print("Error submitting logistics information:", str(e))
            return jsonify({'error': 'Failed to submit logistics information. Please try again.'}), 500

    #S.No 16: Intra Grade Competition Certificate
    @app.route('/submit_competition_cert', methods=['POST'])
    @login_required
    def submit_competition_cert():
        try:
            # Get arrays of form data
            cert_grades = request.form.getlist('cert_grade[]')
            cert_activities = request.form.getlist('cert_activity[]')
            cert_dates = request.form.getlist('cert_date[]')
            cert_nos = request.form.getlist('cert_no[]')
            cert_statuses = request.form.getlist('cert_status[]')
            cert_issue_natures = request.form.getlist('cert_issue_nature[]')
            cert_issue_descs = request.form.getlist('cert_issue_desc[]')
            cert_comments = request.form.getlist('cert_comment[]')

            # Create entries for each row
            for i in range(len(cert_grades)):
                cert_entry = Team1CompetitionCert(
                    team_id=current_user.team_id,
                    submitted_by=current_user.user_id,
                    cert_grade=cert_grades[i],
                    cert_activity=cert_activities[i],
                    cert_date=cert_dates[i],
                    cert_no=cert_nos[i],
                    cert_status=cert_statuses[i],
                    cert_issue_nature=cert_issue_natures[i],
                    cert_issue_desc=cert_issue_descs[i],
                    cert_comment=cert_comments[i]
                )

                db.session.add(cert_entry)

            db.session.commit()

            return jsonify({'message': 'Competition certificate information submitted successfully!'})
        except Exception as e:
            db.session.rollback()
            print("Error submitting competition certificate information:", str(e))
            return jsonify({'error': 'Failed to submit competition certificate information. Please try again.'}), 500

    #S.No 17: Staff Concern
    @app.route('/submit_staff_concern', methods=['POST'])
    @login_required
    def submit_staff_concern():
        try:
            # Get arrays of form data
            sc_cats = request.form.getlist('sc_cat[]')
            sc_names = request.form.getlist('sc_name[]')
            sc_depts = request.form.getlist('sc_dept[]')
            sc_incharges = request.form.getlist('sc_incharge[]')
            sc_issue_natures = request.form.getlist('sc_issue_nature[]')
            sc_issue_descs = request.form.getlist('sc_issue_desc[]')
            sc_comments = request.form.getlist('sc_comment[]')

            # Create staff concern entries
            for i in range(len(sc_names)):
                if sc_names[i]:  # Only create entry if name is provided
                    staff_concern = Team1StaffConcern(
                        team_id=current_user.team_id,
                        submitted_by=current_user.user_id,
                        sc_cat=sc_cats[i],
                        sc_name=sc_names[i],
                        sc_dept=sc_depts[i],
                        sc_incharge=sc_incharges[i],
                        sc_issue_nature=sc_issue_natures[i],
                        sc_issue_desc=sc_issue_descs[i],
                        sc_comment=sc_comments[i]
                    )
                    db.session.add(staff_concern)

            db.session.commit()



            return jsonify({'message': 'Staff concern information submitted successfully!'})
        except Exception as e:
            db.session.rollback()
            print("Error submitting staff concern information:", str(e))
            return jsonify({'error': 'Failed to submit staff concern information. Please try again.'}), 500

    # S.No 17b: Student Concern
    @app.route('/submit_student_concern', methods=['POST'])
    @login_required
    def submit_student_concern():
        try:
            # Get arrays of form data
            st_cats = request.form.getlist('st_cat[]')
            st_names = request.form.getlist('st_name[]')
            st_classes = request.form.getlist('st_class[]')
            st_incharges = request.form.getlist('st_incharge[]')
            st_issue_natures = request.form.getlist('st_issue_nature[]')
            st_issue_descs = request.form.getlist('st_issue_desc[]')
            st_comments = request.form.getlist('st_comment[]')

            # Create student concern entries
            for i in range(len(st_names)):
                if st_names[i]:  # Only create entry if student name is provided
                    student_concern = Team1StudentConcern(
                        team_id=current_user.team_id,
                        submitted_by=current_user.user_id,
                        st_cat=st_cats[i],
                        st_name=st_names[i],
                        st_class=st_classes[i],
                        st_incharge=st_incharges[i],
                        st_issue_nature=st_issue_natures[i],
                        st_issue_desc=st_issue_descs[i],
                        st_comment=st_comments[i]
                    )
                    db.session.add(student_concern)

            db.session.commit()
            return jsonify({'message': 'Student concern information submitted successfully!'})
        except Exception as e:
            db.session.rollback()
            print("Error submitting student concern information:", str(e))
            return jsonify({'error': 'Failed to submit student concern information. Please try again.'}), 500


    #S.No 18: Parent Concern
    #S.No 18a: Parent Concern Summary
    @app.route('/submit_parent_concern_summary', methods=['POST'])
    @login_required
    def submit_parent_concern_summary():
        try:
            # Get arrays of form data
            pc_summary_cats = request.form.getlist('pc_summary_cat[]')
            pc_summary_nos = request.form.getlist('pc_summary_no[]')
            pc_summary_closeds = request.form.getlist('pc_summary_closed[]')
            pc_summary_loop13s = request.form.getlist('pc_summary_loop13[]')
            pc_summary_loop3pluses = request.form.getlist('pc_summary_loop3plus[]')
            pc_summary_issue_natures = request.form.getlist('pc_summary_issue_nature[]')
            pc_summary_issue_descs = request.form.getlist('pc_summary_issue_desc[]')
            pc_summary_comments = request.form.getlist('pc_summary_comment[]')

            # Create entries for each row
            for i in range(len(pc_summary_cats)):
                summary = Team1ParentConcern(
                    team_id=current_user.team_id,
                    submitted_by=current_user.user_id,
                    pc_cat=pc_summary_cats[i],
                    pc_summary_no=pc_summary_nos[i],
                    pc_summary_closed=pc_summary_closeds[i],
                    pc_summary_loop13=pc_summary_loop13s[i],
                    pc_summary_loop3plus=pc_summary_loop3pluses[i],
                    pc_summary_issue_nature=pc_summary_issue_natures[i],
                    pc_summary_issue_desc=pc_summary_issue_descs[i],
                    pc_summary_comment=pc_summary_comments[i]
                )
                db.session.add(summary)

            db.session.commit()
            return jsonify({'message': 'Parent Concern Summary submitted successfully!'})
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    #S.No 18b: Parent Concern Detail
    @app.route('/submit_parent_concern_detail', methods=['POST'])
    @login_required
    def submit_parent_concern_detail():
        try:
            pc_detail_names = request.form.getlist('pc_detail_name[]')
            pc_detail_grades = request.form.getlist('pc_detail_grade[]')
            pc_detail_concerns = request.form.getlist('pc_detail_concern[]')
            pc_detail_incharges = request.form.getlist('pc_detail_incharge[]')
            pc_detail_issue_natures = request.form.getlist('pc_detail_issue_nature[]')
            pc_detail_comments = request.form.getlist('pc_detail_comment[]')

            # Create parent concern detail entries
            for i in range(len(pc_detail_names)):
                if pc_detail_names[i]:  # Only create entry if name is provided
                    detail = Team1ParentConcernDetail(
                        team_id=current_user.team_id,
                        submitted_by=current_user.user_id,
                        pc_detail_name=pc_detail_names[i],
                        pc_detail_grade=pc_detail_grades[i],
                        pc_detail_concern=pc_detail_concerns[i],
                        pc_detail_incharge=pc_detail_incharges[i],
                        pc_detail_issue_nature=pc_detail_issue_natures[i],
                        pc_detail_comment=pc_detail_comments[i]
                    )
                    db.session.add(detail)

            db.session.commit()
            return jsonify({'message': 'Parent Concern Details submitted successfully!'})
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500


    #S.No 19: AEP Attendance
    @app.route('/submit_aep', methods=['POST'])
    @login_required
    def submit_aep():
        try:
            aep_entry = Team1AEPAttendance(
                team_id=current_user.team_id,
                submitted_by=current_user.user_id,

                # Grade 11
                aep_str_g11=int(request.form.get('aep_str_g11') or 0),
                aep_enr_g11=int(request.form.get('aep_enr_g11') or 0),
                aep_enrpct_g11=float(request.form.get('aep_enrpct_g11') or 0.0),
                aep_prog_g11=request.form.get('aep_prog_g11'),
                aep_exp_g11=int(request.form.get('aep_exp_g11') or 0),
                aep_att_g11=int(request.form.get('aep_att_g11') or 0),
                aep_attpct_g11=float(request.form.get('aep_attpct_g11') or 0.0),

                # Grade 12
                aep_str_g12=int(request.form.get('aep_str_g12') or 0),
                aep_enr_g12=int(request.form.get('aep_enr_g12') or 0),
                aep_enrpct_g12=float(request.form.get('aep_enrpct_g12') or 0.0),
                aep_prog_g12=request.form.get('aep_prog_g12'),
                aep_exp_g12=int(request.form.get('aep_exp_g12') or 0),
                aep_att_g12=int(request.form.get('aep_att_g12') or 0),
                aep_attpct_g12=float(request.form.get('aep_attpct_g12') or 0.0)
            )

            db.session.add(aep_entry)
            db.session.commit()

            return jsonify({'message': 'AEP attendance information submitted successfully!'})

        except Exception as e:
            db.session.rollback()
            print("Error submitting AEP attendance information:", str(e))
            return jsonify({'error': 'Failed to submit AEP attendance information. Please try again.'}), 500


    # S.No 20: Extended Class Attendance
    @app.route('/submit_extended_class', methods=['POST'])
    @login_required
    def submit_extended_class():
        try:
            # Create extended class attendance entry
            ec_entry = Team1ExtendedClassAttendance(
                team_id=current_user.team_id,
                submitted_by=current_user.user_id,
                # Grades 3 to 5
                ec_str_g35=request.form.get('ec_str_g35'),
                ec_enr_g35=request.form.get('ec_enr_g35'),
                ec_enrpct_g35=request.form.get('ec_enrpct_g35'),
                ec_subj_g35=request.form.get('ec_subj_g35'),
                ec_exp_g35=request.form.get('ec_exp_g35'),
                ec_att_g35=request.form.get('ec_att_g35'),
                ec_attpct_g35=request.form.get('ec_attpct_g35'),
                # Grades 6 to 8
                ec_str_g68=request.form.get('ec_str_g68'),
                ec_enr_g68=request.form.get('ec_enr_g68'),
                ec_enrpct_g68=request.form.get('ec_enrpct_g68'),
                ec_subj_g68=request.form.get('ec_subj_g68'),
                ec_exp_g68=request.form.get('ec_exp_g68'),
                ec_att_g68=request.form.get('ec_att_g68'),
                ec_attpct_g68=request.form.get('ec_attpct_g68'),
                # Grades 9 and 10
                ec_str_g910=request.form.get('ec_str_g910'),
                ec_enr_g910=request.form.get('ec_enr_g910'),
                ec_enrpct_g910=request.form.get('ec_enrpct_g910'),
                ec_subj_g910=request.form.get('ec_subj_g910'),
                ec_exp_g910=request.form.get('ec_exp_g910'),
                ec_att_g910=request.form.get('ec_att_g910'),
                ec_attpct_g910=request.form.get('ec_attpct_g910'),
                # Grades 11 and 12
                ec_str_g1112=request.form.get('ec_str_g1112'),
                ec_enr_g1112=request.form.get('ec_enr_g1112'),
                ec_enrpct_g1112=request.form.get('ec_enrpct_g1112'),
                ec_subj_g1112=request.form.get('ec_subj_g1112'),
                ec_exp_g1112=request.form.get('ec_exp_g1112'),
                ec_att_g1112=request.form.get('ec_att_g1112'),
                ec_attpct_g1112=request.form.get('ec_attpct_g1112')
            )

            db.session.add(ec_entry)
            db.session.commit()



            return jsonify({'message': 'Extended class attendance information submitted successfully!'})
        except Exception as e:
            db.session.rollback()
            print("Error submitting extended class attendance information:", str(e))
            return jsonify({'error': 'Failed to submit extended class attendance information. Please try again.'}), 500

    #S.No 21: Training Session
    # S.No 21: Training Session
    @app.route('/submit_training_session', methods=['POST'])
    @login_required
    def submit_training_session():
        try:
            # Get lists of each training field from the form
            teachers = request.form.getlist('train_teacher[]')
            topics = request.form.getlist('train_topic[]')
            conductors = request.form.getlist('train_by[]')
            modes = request.form.getlist('train_mode[]')
            durations = request.form.getlist('train_duration[]')
            reports = request.form.getlist('train_report[]')
            participants = request.form.getlist('train_participants[]')

            # Iterate through the list and create entries
            for i in range(len(teachers)):
                session_entry = Team1TrainingSession(
                    team_id=current_user.team_id,
                    submitted_by=current_user.user_id,
                    train_teacher=teachers[i],
                    train_topic=topics[i],
                    train_by=conductors[i],
                    train_mode=modes[i],
                    train_duration=durations[i],
                    train_report=reports[i],
                    train_participants=int(participants[i]) if participants[i] else None
                )
                db.session.add(session_entry)

            db.session.commit()

            return jsonify({'message': 'Training session(s) submitted successfully!'})
        except Exception as e:
            db.session.rollback()
            print("Error submitting training session:", str(e))
            return jsonify({'error': 'Failed to submit training session. Please try again.'}), 500

    #S.No 22: Team Weekly Meeting

    @app.route('/submit_team_meeting', methods=['POST'])
    @login_required
    def submit_team_meeting():
        try:
            meeting = Team1WeeklyMeeting(
                team_id=current_user.team_id,
                submitted_by=current_user.user_id,

                # KG
                meet_head_kg=request.form.get('meet_head_kg'),
                meet_agenda_kg=request.form.get('meet_agenda_kg'),
                meet_str_kg=request.form.get('meet_str_kg', type=int),
                meet_att_kg=request.form.get('meet_att_kg', type=int),
                meet_attpct_kg=request.form.get('meet_attpct_kg', type=float),

                # Grades 1 and 2
                meet_head_12=request.form.get('meet_head_12'),
                meet_agenda_12=request.form.get('meet_agenda_12'),
                meet_str_12=request.form.get('meet_str_12', type=int),
                meet_att_12=request.form.get('meet_att_12', type=int),
                meet_attpct_12=request.form.get('meet_attpct_12', type=float),

                # Grades 3 to 5
                meet_head_35=request.form.get('meet_head_35'),
                meet_agenda_35=request.form.get('meet_agenda_35'),
                meet_str_35=request.form.get('meet_str_35', type=int),
                meet_att_35=request.form.get('meet_att_35', type=int),
                meet_attpct_35=request.form.get('meet_attpct_35', type=float),

                # Grades 6 to 8
                meet_head_68=request.form.get('meet_head_68'),
                meet_agenda_68=request.form.get('meet_agenda_68'),
                meet_str_68=request.form.get('meet_str_68', type=int),
                meet_att_68=request.form.get('meet_att_68', type=int),
                meet_attpct_68=request.form.get('meet_attpct_68', type=float),

                # Grades 9 and 10
                meet_head_910=request.form.get('meet_head_910'),
                meet_agenda_910=request.form.get('meet_agenda_910'),
                meet_str_910=request.form.get('meet_str_910', type=int),
                meet_att_910=request.form.get('meet_att_910', type=int),
                meet_attpct_910=request.form.get('meet_attpct_910', type=float),

                # Grades 11 and 12
                meet_head_1112=request.form.get('meet_head_1112'),
                meet_agenda_1112=request.form.get('meet_agenda_1112'),
                meet_str_1112=request.form.get('meet_str_1112', type=int),
                meet_att_1112=request.form.get('meet_att_1112', type=int),
                meet_attpct_1112=request.form.get('meet_attpct_1112', type=float)
            )

            db.session.add(meeting)
            db.session.commit()

            return jsonify({'message': 'Weekly meeting data submitted successfully!'})
        except Exception as e:
            db.session.rollback()
            print("Error in weekly meeting submission:", str(e))
            return jsonify({'error': 'Failed to submit weekly meeting data. Please try again.'}), 500


    # ------------------------------------------------------------ #
    # Submit Special Education                                     #
    # ------------------------------------------------------------ #
    @app.route('/submit_special_education', methods=['POST'])
    @login_required
    def submit_special_education():
        try:
            class_names = request.form.getlist('class_name[]')
            total_students_list = request.form.getlist('total_students[]')
            as_on_dates = request.form.getlist('as_on_date[]')
            attended_list = request.form.getlist('attended[]')
            not_attended_list = request.form.getlist('not_attended[]')
            nature_of_issues = request.form.getlist('nature_of_issue[]')
            observations_list = request.form.getlist('observations[]')
            issue_descriptions = request.form.getlist('issue_description[]')
            comments_list = request.form.getlist('comments[]')
            schedules = request.form.getlist('schedule[]')

            for i in range(len(class_names)):
                # Skip empty rows (except class_name & schedule)
                if (
                    not total_students_list[i]
                    and not as_on_dates[i]
                    and not attended_list[i]
                    and not not_attended_list[i]
                    and not nature_of_issues[i]
                    and not observations_list[i].strip()
                    and not issue_descriptions[i].strip()
                    and not comments_list[i].strip()
                ):
                    continue

                entry = Team1SpecialEducation(
                    team_id=current_user.team_id,
                    submitted_by=current_user.user_id,
                    class_name=class_names[i],
                    total_students=int(total_students_list[i]) if total_students_list[i] else None,
                    as_on_date=as_on_dates[i] if as_on_dates[i] else None,
                    attended=int(attended_list[i]) if attended_list[i] else None,
                    not_attended=int(not_attended_list[i]) if not_attended_list[i] else None,
                    nature_of_issue=nature_of_issues[i],
                    observations=observations_list[i],
                    issue_description=issue_descriptions[i],
                    comments=comments_list[i],
                    schedule=schedules[i]
                )
                db.session.add(entry)

            db.session.commit()
            return jsonify({'message': 'Special Education data submitted successfully.'})

        except Exception as e:
            db.session.rollback()
            print("Error submitting Special Education data:", str(e))
            return jsonify({'error': 'Failed to submit Special Education data. Please try again.'}), 500

        # ------------------------------------------------------------ #
    # Submit Hostel Data                                           #
    # ------------------------------------------------------------ #
    @app.route('/submit_hostel', methods=['POST'])
    @login_required
    def submit_hostel():
        try:
            # Fetch lists from the form
            students_list = request.form.getlist('hostel_students[]')
            payment_list = request.form.getlist('hostel_payment[]')
            food_concerns = request.form.getlist('hostel_food_concern[]')
            general_concerns = request.form.getlist('hostel_general_concern[]')

            # Iterate over all rows
            for i in range(len(students_list)):
                # Skip empty rows (if all fields are empty)
                if (
                    not students_list[i].strip()
                    and not payment_list[i].strip()
                    and not food_concerns[i].strip()
                    and not general_concerns[i].strip()
                ):
                    continue

                entry = Team1Hostel(
                    team_id=current_user.team_id,
                    submitted_by=current_user.user_id,
                    hostel_students=students_list[i].strip() if students_list[i] else None,
                    hostel_payment=payment_list[i] if payment_list[i] else None,
                    hostel_food_concern=food_concerns[i].strip() if food_concerns[i] else None,
                    hostel_general_concern=general_concerns[i].strip() if general_concerns[i] else None
                )
                db.session.add(entry)

            db.session.commit()
            return jsonify({'message': 'Hostel data submitted successfully.'})

        except Exception as e:
            db.session.rollback()
            print("Error submitting Hostel data:", str(e))
            return jsonify({'error': 'Failed to submit Hostel data. Please try again.'}), 500

    # S.No 23: SEC
    @app.route('/submit_sec', methods=['POST'])
    @login_required
    def submit_sec():
        try:
            # Get form data as lists
            committees = request.form.getlist('sec_committee[]')
            schedules = request.form.getlist('sec_schedule[]')
            meeting_statuses = request.form.getlist('sec_meeting_status[]')
            md_mom_reviews = request.form.getlist('sec_md_mom_review[]')
            next_meetings = request.form.getlist('sec_next_meeting[]')
            atr_completion_statuses = request.form.getlist('sec_atr_completion_status[]')

            for i in range(len(committees)):
                # Skip empty rows
                if (
                    not committees[i].strip() and
                    not schedules[i].strip() and
                    not meeting_statuses[i].strip() and
                    not md_mom_reviews[i].strip() and
                    not next_meetings[i].strip() and
                    not atr_completion_statuses[i].strip()
                ):
                    continue

                entry = Team1SEC(
                    team_id=current_user.team_id,
                    submitted_by=current_user.user_id,
                    sec_committee=committees[i].strip() if committees[i] else None,
                    sec_schedule=schedules[i] if schedules[i] else None,
                    sec_meeting_status=meeting_statuses[i] if meeting_statuses[i] else None,
                    sec_md_mom_review=md_mom_reviews[i].strip() if md_mom_reviews[i] else None,
                    sec_next_meeting=next_meetings[i] if next_meetings[i] else None,
                    sec_atr_completion_status=atr_completion_statuses[i] if atr_completion_statuses[i] else None
                )
                db.session.add(entry)

            db.session.commit()
            return jsonify({'message': 'SEC data submitted successfully.'})

        except Exception as e:
            db.session.rollback()
            print("Error submitting SEC data:", str(e))
            return jsonify({'error': 'Failed to submit SEC data. Please try again.'}), 500

    # S.No 24: School Counsellor
    @app.route('/submit_school_counsellor', methods=['POST'])
    @login_required
    def submit_school_counsellor():
        try:
            # Extract form data
            rapid_category_list = request.form.getlist('rapid_category[]')
            rapid_subtopic_list = request.form.getlist('rapid_subtopic[]')
            rapid_total_issues_list = request.form.getlist('rapid_total_issues[]')
            rapid_met_so_far_list = request.form.getlist('rapid_met_so_far[]')
            rapid_pending_list = request.form.getlist('rapid_pending[]')
            rapid_follow_up_list = request.form.getlist('rapid_follow_up[]')
            rapid_issue_closed_list = request.form.getlist('rapid_issue_closed[]')
            rapid_critical_list = request.form.getlist('rapid_critical[]')
            rapid_manageable_list = request.form.getlist('rapid_manageable[]')
            rapid_issue_categories_list = request.form.getlist('rapid_issue_categories[]')
            rapid_nature_of_issues_list = request.form.getlist('rapid_nature_of_issues[]')
            rapid_count_list = request.form.getlist('rapid_count[]')
            rapid_duration_list = request.form.getlist('rapid_duration[]')
            rapid_comments_list = request.form.getlist('rapid_comments[]')

            # Loop through rows and insert into DB
            for i in range(len(rapid_category_list)):
                # Skip completely empty rows
                if not (
                    rapid_category_list[i].strip() or
                    rapid_subtopic_list[i].strip() or
                    rapid_total_issues_list[i].strip() or
                    rapid_met_so_far_list[i].strip() or
                    rapid_pending_list[i].strip() or
                    rapid_follow_up_list[i].strip() or
                    rapid_issue_closed_list[i] or
                    rapid_critical_list[i].strip() or
                    rapid_manageable_list[i].strip() or
                    rapid_issue_categories_list[i].strip() or
                    rapid_nature_of_issues_list[i].strip() or
                    rapid_count_list[i].strip() or
                    rapid_duration_list[i].strip() or
                    rapid_comments_list[i].strip()
                ):
                    continue  # Skip empty row

                # Convert issue_closed date if provided
                issue_closed_date = (
                    datetime.strptime(rapid_issue_closed_list[i], '%Y-%m-%d').date()
                    if rapid_issue_closed_list[i] else None
                )

                # Create DB entry
                entry = Team1SchoolCounsellor(
                    team_id=current_user.team_id,
                    submitted_by=current_user.user_id,
                    rapid_category=rapid_category_list[i],
                    rapid_subtopic=rapid_subtopic_list[i],
                    rapid_total_issues=rapid_total_issues_list[i],
                    rapid_met_so_far=rapid_met_so_far_list[i],
                    rapid_pending=rapid_pending_list[i],
                    rapid_follow_up=rapid_follow_up_list[i],
                    rapid_issue_closed=issue_closed_date,
                    rapid_critical=rapid_critical_list[i],
                    rapid_manageable=rapid_manageable_list[i],
                    rapid_issue_categories=rapid_issue_categories_list[i],
                    rapid_nature_of_issues=rapid_nature_of_issues_list[i],
                    rapid_count=rapid_count_list[i],
                    rapid_duration=rapid_duration_list[i],
                    rapid_comments=rapid_comments_list[i]
                )

                db.session.add(entry)

            db.session.commit()
            return jsonify({'message': 'School Counsellor data submitted successfully.'})

        except Exception as e:
            db.session.rollback()
            print("Error submitting School Counsellor data:", str(e))
            return jsonify({'error': 'Failed to submit data. Please try again.'}), 500

        # ------------------------------------------------------------ #
    # Submit Scholorius / Smart Tail Data                        #
    # ------------------------------------------------------------ #
    @app.route('/submit_scholorius', methods=['POST'])
    @login_required
    def submit_scholorius():
        try:
            # Fetch lists from the form
            program_list = request.form.getlist('scholorius_program[]')
            date_list = request.form.getlist('scholorius_date[]')
            status_list = request.form.getlist('scholorius_status[]')
            remark_list = request.form.getlist('scholorius_remark[]')

            # Iterate over all rows
            for i in range(len(program_list)):
                # Skip empty rows (if all fields are empty)
                if (
                    not program_list[i].strip()
                    and not date_list[i]
                    and not status_list[i].strip()
                    and not remark_list[i].strip()
                ):
                    continue

                entry = Team1Scholorius(
                    team_id=current_user.team_id,
                    submitted_by=current_user.user_id,
                    scholorius_program=program_list[i].strip() if program_list[i] else None,
                    scholorius_date=date_list[i] if date_list[i] else None,
                    scholorius_status=status_list[i].strip() if status_list[i] else None,
                    scholorius_remark=remark_list[i].strip() if remark_list[i] else None
                )
                db.session.add(entry)

            db.session.commit()
            return jsonify({'message': 'Scholorius / Smart Tail data submitted successfully.'})

        except Exception as e:
            db.session.rollback()
            print("Error submitting Scholorius data:", str(e))
            return jsonify({'error': 'Failed to submit Scholorius data. Please try again.'}), 500



