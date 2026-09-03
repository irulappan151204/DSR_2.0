# routes/forms/team2_forms.py
from flask import request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from datetime import datetime
from zoneinfo import ZoneInfo
from werkzeug.utils import secure_filename
from extensions import db
from utils.helpers import safe_int, safe_float, safe_date, safe_time
from models import (
    Team2HRAttendance, Team2AdminAttendance, Team2RecruitmentActivity,
    Team2PendingRecruitment, Team2RecruitmentPipeline, Team2StaffStatusUpdates,
    Team2SalaryPending, Team2PoliceVerification, Team2InterviewSchedule,
    Team2ExitInformation, Team2IssuesStaffConcerns, Team2KuralRecitation,
    Team2FrontOfficePhoneCalls, Team2VisitorLog, Team2BSNLPhoneStatus,
    Team2MaterialsInward, Team2MaterialsOutward, Team2MaterialsMovement,
    Team2ReturnableMaterialTracking, Team2ReturnableGoodsReport,
    Team2CampusCameraStatus, Team2VehicleCameraStatus, Team2BusACCameraStatus,
    Team2GPSMonitoring, Team2IssuesIdentifiedMonitoring, Team2IssuesIdentifiedControlRoom,
    Team2CameraFootageEntry, Team2BiometricsAccessCardPunching, Team2WaterTDSDeviation,
    Team2TestingCleaning, Team2WaterLevel, Team2HousekeepingGeneral, Team2PoolTesting,
    Team2WashroomCleanliness, Team2TransportAttendance, Team2ACWorkingStatus,
    Team2LateReporting, Team2MaintenanceServiceIssues, Team2CarMaintenanceCleaning,
    Team2VehicleRenewalsDelays, Team2SpecialTrip, Team2ACTemperatureCheck,
    Team2LaborEbSolarGenset, Team2Motor, Team2PestControl, Team2ACTempDeviation,
    Team2ElectricityConsumption, Team2EBDetails, Team2SolarDetails, Team2GensetDetails,
    Team2CountVerification, Team2AttendanceReplacement, Team2SecurityInfoNote,
    Team2SecurityGovtInout, Team2AlcoholTest, Team2SecurityMaterialsInout,
    Team2SecurityMaterialsOutward, Team2TransportVerification, Team2DocumentsMovement,
    Team2GovtOfficialDocuments, Team2ThoorigaiTeamSocialMedia, Team2WebsiteUpdates,
    Team2MDSocialMedia, Team2IntercomMaintenance, Team2HealthCheckUp,
    Team2NetConnectivityPrintDetails, Team2GeneralMaintenanceITProducts,
    Team2CalendarSchedule, Team2TrainingAttendance, Team2TrainingDetails,
    Team2ManpowerPlanning, Team2OverallConsolidation, Team2UniformDetails,
    Team2DepartmentWiseUniformDetails, Team2TotalHRAttendance, Team2ParentConcernDetail,
    FileStorage
)

def register_team2_forms(app):
    """Register all 75 Team 2 (Admin) form submission routes."""
    # Team 2 
    # HR Attendance
    @app.route('/submit_hr_attendance', methods=['POST'])
    @login_required
    def submit_hr_attendance():
        try:
            # Create HR attendance entry
            hr_entry = Team2HRAttendance(
                team_id=current_user.team_id,
                submitted_by=current_user.user_id,
                # Jr. School
                hr_att_jr_school_total=safe_int(request.form.get('hr_att_jr_school_total')),
                hr_att_jr_school_present=safe_int(request.form.get('hr_att_jr_school_present')),
                hr_att_jr_school_leave=safe_int(request.form.get('hr_att_jr_school_leave')),
                hr_att_jr_school_leave_perc=safe_float(request.form.get('hr_att_jr_school_leave_perc')),
                hr_att_jr_school_nature=request.form.get('hr_att_jr_school_nature'),
                hr_att_jr_school_issue_desc=request.form.get('hr_att_jr_school_issue_desc'),
                hr_att_jr_school_comments=request.form.get('hr_att_jr_school_comments'),
                # Sr. School
                hr_att_sr_school_total=safe_int(request.form.get('hr_att_sr_school_total')),
                hr_att_sr_school_present=safe_int(request.form.get('hr_att_sr_school_present')),
                hr_att_sr_school_leave=safe_int(request.form.get('hr_att_sr_school_leave')),
                hr_att_sr_school_leave_perc=safe_float(request.form.get('hr_att_sr_school_leave_perc')),
                hr_att_sr_school_nature=request.form.get('hr_att_sr_school_nature'),
                hr_att_sr_school_issue_desc=request.form.get('hr_att_sr_school_issue_desc'),
                hr_att_sr_school_comments=request.form.get('hr_att_sr_school_comments'),
                # ECA
                hr_att_eca_total=safe_int(request.form.get('hr_att_eca_total')),
                hr_att_eca_present=safe_int(request.form.get('hr_att_eca_present')),
                hr_att_eca_leave=safe_int(request.form.get('hr_att_eca_leave')),
                hr_att_eca_leave_perc=safe_float(request.form.get('hr_att_eca_leave_perc')),
                hr_att_eca_nature=request.form.get('hr_att_eca_nature'),
                hr_att_eca_issue_desc=request.form.get('hr_att_eca_issue_desc'),
                hr_att_eca_comments=request.form.get('hr_att_eca_comments'),
                # Academics Overall
                hr_att_acad_overall_total=safe_int(request.form.get('hr_att_acad_overall_total')),
                hr_att_acad_overall_present=safe_int(request.form.get('hr_att_acad_overall_present')),
                hr_att_acad_overall_leave=safe_int(request.form.get('hr_att_acad_overall_leave')),
                hr_att_acad_overall_leave_perc=safe_float(request.form.get('hr_att_acad_overall_leave_perc'))
            )

            # Create Admin attendance entry
            admin_entry = Team2AdminAttendance(
                team_id=current_user.team_id,
                submitted_by=current_user.user_id,
                # Admin Staff
                hr_att_admin_total=safe_int(request.form.get('hr_att_admin_total')),
                hr_att_admin_present=safe_int(request.form.get('hr_att_admin_present')),
                hr_att_admin_leave=safe_int(request.form.get('hr_att_admin_leave')),
                hr_att_admin_leave_perc=safe_float(request.form.get('hr_att_admin_leave_perc')),
                hr_att_admin_nature=request.form.get('hr_att_admin_nature'),
                hr_att_admin_issue_desc=request.form.get('hr_att_admin_issue_desc'),
                hr_att_admin_comments=request.form.get('hr_att_admin_comments'),
                # Drivers
                hr_att_drivers_total=safe_int(request.form.get('hr_att_drivers_total')),
                hr_att_drivers_present=safe_int(request.form.get('hr_att_drivers_present')),
                hr_att_drivers_leave=safe_int(request.form.get('hr_att_drivers_leave')),
                hr_att_drivers_leave_perc=safe_float(request.form.get('hr_att_drivers_leave_perc')),
                hr_att_drivers_nature=request.form.get('hr_att_drivers_nature'),
                hr_att_drivers_issue_desc=request.form.get('hr_att_drivers_issue_desc'),
                hr_att_drivers_comments=request.form.get('hr_att_drivers_comments'),
                # Securities
                hr_att_sec_total=safe_int(request.form.get('hr_att_sec_total')),
                hr_att_sec_present=safe_int(request.form.get('hr_att_sec_present')),
                hr_att_sec_leave=safe_int(request.form.get('hr_att_sec_leave')),
                hr_att_sec_leave_perc=safe_float(request.form.get('hr_att_sec_leave_perc')),
                hr_att_sec_nature=request.form.get('hr_att_sec_nature'),
                hr_att_sec_issue_desc=request.form.get('hr_att_sec_issue_desc'),
                hr_att_sec_comments=request.form.get('hr_att_sec_comments'),
                # Housekeeping
                hr_att_hk_total=safe_int(request.form.get('hr_att_hk_total')),
                hr_att_hk_present=safe_int(request.form.get('hr_att_hk_present')),
                hr_att_hk_leave=safe_int(request.form.get('hr_att_hk_leave')),
                hr_att_hk_leave_perc=safe_float(request.form.get('hr_att_hk_leave_perc')),
                hr_att_hk_nature=request.form.get('hr_att_hk_nature'),
                hr_att_hk_issue_desc=request.form.get('hr_att_hk_issue_desc'),
                hr_att_hk_comments=request.form.get('hr_att_hk_comments'),
                # Conductors
                hr_att_cond_total=safe_int(request.form.get('hr_att_cond_total')),
                hr_att_cond_present=safe_int(request.form.get('hr_att_cond_present')),
                hr_att_cond_leave=safe_int(request.form.get('hr_att_cond_leave')),
                hr_att_cond_leave_perc=safe_float(request.form.get('hr_att_cond_leave_perc')),
                hr_att_cond_nature=request.form.get('hr_att_cond_nature'),
                hr_att_cond_issue_desc=request.form.get('hr_att_cond_issue_desc'),
                hr_att_cond_comments=request.form.get('hr_att_cond_comments'),
                # Admin Overall
                hr_att_admin_overall_total=safe_int(request.form.get('hr_att_admin_overall_total')),
                hr_att_admin_overall_present=safe_int(request.form.get('hr_att_admin_overall_present')),
                hr_att_admin_overall_leave=safe_int(request.form.get('hr_att_admin_overall_leave')),
                hr_att_admin_overall_leave_perc=safe_float(request.form.get('hr_att_admin_overall_leave_perc'))
            )

            db.session.add(hr_entry)
            db.session.add(admin_entry)
            db.session.commit()

            return jsonify({'message': 'Attendance data submitted successfully!'})
        except Exception as e:
            db.session.rollback()
            print("Error submitting attendance:", str(e))
            return jsonify({'error': 'Failed to submit attendance data. Please try again.'}), 500

    # team 2: 1 d Total HR Attendance
    @app.route('/submit_total_hr_attendance', methods=['POST'])
    @login_required
    def submit_total_hr_attendance():
        try:
            total = int(request.form.get('hr_att_overall_total') or 0)
            present = int(request.form.get('hr_att_overall_present') or 0)
            leave = int(request.form.get('hr_att_overall_leave') or 0)
            leave_perc = round((leave / total * 100), 1) if total > 0 else 0.0

            form_entry = Team2TotalHRAttendance(
                team_id=current_user.team_id,
                submitted_by=current_user.user_id,
                category="HR Overall Attendance",
                total=total,
                present=present,
                leave=leave,
                leave_perc=leave_perc,
                nature_of_issue=request.form.get('hr_att_overall_nature'),
                issue_description=request.form.get('hr_att_overall_issue_desc'),
                comments=request.form.get('hr_att_overall_comments')
            )

            db.session.add(form_entry)
            db.session.commit()

            return jsonify({'message': 'HR Attendance submitted successfully!'})

        except Exception as e:
            db.session.rollback()
            print("Error submitting HR Attendance:", str(e))
            return jsonify({'error': 'Failed to submit HR Attendance. Please try again.'}), 500


    # team 2 recruitemnt_activity

    @app.route('/submit_recruitment_activity', methods=['POST'])
    @login_required
    def submit_recruitment_activity():
        try:
            form_entry = Team2RecruitmentActivity(
                team_id=current_user.team_id,
                submitted_by=current_user.user_id,
                # Academics
                rec_act_acad_vac_nos=request.form.get('rec_act_acad_vac_nos'),
                rec_act_acad_pos=request.form.get('rec_act_acad_pos'),
                rec_act_acad_update=request.form.get('rec_act_acad_update'),
                rec_act_acad_nature=request.form.get('rec_act_acad_nature'),
                rec_act_acad_issue_desc=request.form.get('rec_act_acad_issue_desc'),
                rec_act_acad_comments=request.form.get('rec_act_acad_comments'),
                # Admin
                rec_act_admin_vac_nos=request.form.get('rec_act_admin_vac_nos'),
                rec_act_admin_pos=request.form.get('rec_act_admin_pos'),
                rec_act_admin_update=request.form.get('rec_act_admin_update'),
                rec_act_admin_nature=request.form.get('rec_act_admin_nature'),
                rec_act_admin_issue_desc=request.form.get('rec_act_admin_issue_desc'),
                rec_act_admin_comments=request.form.get('rec_act_admin_comments')
            )

            db.session.add(form_entry)
            db.session.commit()

            return jsonify({'message': 'Recruitment activity submitted successfully!'})
        except Exception as e:
            db.session.rollback()
            print("Error submitting recruitment activity:", str(e))
            return jsonify({'error': 'Failed to submit recruitment activity. Please try again.'}), 500

    # team 2 pending recruitment

    @app.route('/submit_pending_recruitment', methods=['POST'])
    @login_required
    def submit_pending_recruitment():
        try:
            form_entry = Team2PendingRecruitment(
                team_id=current_user.team_id,
                submitted_by=current_user.user_id,
                # Academics
                rec_pend_acad_count=request.form.get('rec_pend_acad_count'),
                rec_pend_acad_pos=request.form.get('rec_pend_acad_pos'),
                rec_pend_acad_closure=datetime.strptime(request.form.get('rec_pend_acad_closure'), '%Y-%m-%d').date() if request.form.get('rec_pend_acad_closure') else None,
                rec_pend_acad_nature=request.form.get('rec_pend_acad_nature'),
                rec_pend_acad_issue_desc=request.form.get('rec_pend_acad_issue_desc'),
                rec_pend_acad_comments=request.form.get('rec_pend_acad_comments'),
                # Admin
                rec_pend_admin_count=request.form.get('rec_pend_admin_count'),
                rec_pend_admin_pos=request.form.get('rec_pend_admin_pos'),
                rec_pend_admin_closure=datetime.strptime(request.form.get('rec_pend_admin_closure'), '%Y-%m-%d').date() if request.form.get('rec_pend_admin_closure') else None,
                rec_pend_admin_nature=request.form.get('rec_pend_admin_nature'),
                rec_pend_admin_issue_desc=request.form.get('rec_pend_admin_issue_desc'),
                rec_pend_admin_comments=request.form.get('rec_pend_admin_comments')
            )

            db.session.add(form_entry)
            db.session.commit()

            return jsonify({'message': 'Pending recruitment submitted successfully!'})
        except Exception as e:
            db.session.rollback()
            print("Error submitting pending recruitment:", str(e))
            return jsonify({'error': 'Failed to submit pending recruitment. Please try again.'}), 500

    @app.route('/submit_recruitment_pipeline', methods=['POST'])
    @login_required
    def submit_recruitment_pipeline():
        try:
            # Expect form data like:
            # category[], position[], hired[], shortlisted[]
            categories = request.form.getlist('category[]')
            positions = request.form.getlist('position[]')
            hired_list = request.form.getlist('hired[]')
            shortlisted_list = request.form.getlist('shortlisted[]')

            for category, pos, hired, short in zip(categories, positions, hired_list, shortlisted_list):
                if any([pos, hired, short]):  # Avoid empty rows
                    entry = Team2RecruitmentPipeline(
                        team_id=current_user.team_id,
                        submitted_by=current_user.user_id,
                        category=category,
                        position=pos,
                        hired=hired,
                        shortlisted=short
                    )
                    db.session.add(entry)

            db.session.commit()
            return jsonify({'message': 'Recruitment pipeline submitted successfully!'})

        except Exception as e:
            db.session.rollback()
            print("Error submitting recruitment pipeline:", str(e))
            return jsonify({'error': 'Failed to submit recruitment pipeline. Please try again.'}), 500


    # team 2 staff status updates
    @app.route('/submit_staff_status_updates', methods=['POST'])
    @login_required
    def submit_staff_status_updates():
        try:
            names = request.form.getlist('obs_name[]')
            depts = request.form.getlist('obs_dept[]')
            desigs = request.form.getlist('obs_desig[]')
            dojs = request.form.getlist('obs_doj[]')
            shadows = request.form.getlist('obs_shadow[]')
            completed_dates = request.form.getlist('obs_completed[]')
            comments = request.form.getlist('obs_comments[]')

            entries = []

            for i in range(len(names)):
                # Skip empty rows
                if not any([names[i], depts[i], desigs[i], dojs[i], shadows[i], completed_dates[i], comments[i]]):
                    continue

                entry = Team2StaffStatusUpdates(
                    team_id=current_user.team_id,
                    submitted_by=current_user.user_id,
                    obs_name=names[i],
                    obs_dept=depts[i],
                    obs_desig=desigs[i],
                    obs_doj=datetime.strptime(dojs[i], '%Y-%m-%d').date() if dojs[i] else None,
                    obs_shadow=shadows[i],
                    obs_completed=datetime.strptime(completed_dates[i], '%Y-%m-%d').date() if completed_dates[i] else None,
                    obs_comments=comments[i]
                )
                entries.append(entry)

            if entries:
                db.session.add_all(entries)
                db.session.commit()
                return jsonify({'message': 'Staff status updates submitted successfully!'})
            else:
                return jsonify({'message': 'No data submitted.'})

        except Exception as e:
            db.session.rollback()
            print("Error submitting staff status updates:", str(e))
            return jsonify({'error': 'Failed to submit staff status updates. Please try again.'}), 500

    # team 2 salary pending
    @app.route('/submit_salary_pending', methods=['POST'])
    @login_required
    def submit_salary_pending():
        try:
            names = request.form.getlist('sal_pend_name[]')
            depts = request.form.getlist('sal_pend_dept[]')
            desigs = request.form.getlist('sal_pend_desig[]')
            comments = request.form.getlist('sal_pend_comments[]')

            entries = []
            for name, dept, desig, comment in zip(names, depts, desigs, comments):
                # Skip completely empty rows
                if not (name.strip() or dept.strip() or desig.strip() or comment.strip()):
                    continue

                entry = Team2SalaryPending(
                    team_id=current_user.team_id,
                    submitted_by=current_user.user_id,
                    sal_pend_name=name.strip(),
                    sal_pend_dept=dept.strip(),
                    sal_pend_desig=desig.strip(),
                    sal_pend_comments=comment.strip()
                )
                entries.append(entry)

            if entries:
                db.session.add_all(entries)
                db.session.commit()

            return jsonify({'message': 'Salary pending submitted successfully!'})
        except Exception as e:
            db.session.rollback()
            print("Error submitting salary pending:", str(e))
            return jsonify({'error': 'Failed to submit salary pending. Please try again.'}), 500


    # team 2 police verification
    @app.route('/submit_police_verification', methods=['POST'])
    @login_required
    def submit_police_verification():
        try:
            # Get lists from the form (all rows)
            # s_no_list = request.form.getlist('pv_sno[]')
            # name_list = request.form.getlist('pv_name[]')
            dept_list = request.form.getlist('pv_dept[]')
            strength_list = request.form.getlist('pv_strength[]')
            completed_list = request.form.getlist('pv_completed[]')
            pending_list = request.form.getlist('pv_pending[]')
            remarks_list = request.form.getlist('pv_remarks[]')

            # Loop through all rows and create entries
            for i in range(len(dept_list)):
                if not dept_list[i].strip():
                    continue  # skip empty rows

                record = Team2PoliceVerification(
                    team_id=current_user.team_id,
                    submitted_by=current_user.user_id,
                    # s_no=s_no_list[i] if s_no_list[i] else None,
                    # name=name_list[i].strip(),
                    department=dept_list[i].strip() if dept_list[i] else None,
                    strength=int(strength_list[i]) if strength_list[i].isdigit() else None,
                    completed=completed_list[i].strip() if completed_list[i] else None,
                    pending=pending_list[i].strip() if pending_list[i] else None,
                    remarks=remarks_list[i].strip() if remarks_list[i] else None
                )
                db.session.add(record)

            db.session.commit()
            return jsonify({'message': 'Police verification submitted successfully!'}), 200

        except Exception as e:
            db.session.rollback()
            print("Error submitting police verification:", str(e))
            return jsonify({'error': 'Failed to submit police verification. Please try again.'}), 500

    # team 2 interview schedule
    @app.route('/submit_interview_schedule', methods=['POST'])
    @login_required
    def submit_interview_schedule():
        try:
            departments = request.form.getlist('int_sch_department[]')
            counts = request.form.getlist('int_sch_count[]')
            completions = request.form.getlist('int_sch_comp[]')
            statuses = request.form.getlist('int_sch_status[]')
            natures = request.form.getlist('int_sch_nature[]')
            issue_descs = request.form.getlist('int_sch_issue_desc[]')
            comments = request.form.getlist('int_sch_comments[]')

            for i in range(len(departments)):
                if not departments[i].strip():
                    continue  # skip empty rows

                form_entry = Team2InterviewSchedule(
                    team_id=current_user.team_id,
                    submitted_by=current_user.user_id,
                    department_category=departments[i],
                    candidate_count=counts[i] if counts[i] else None,
                    interview_completion=completions[i],
                    interview_status=statuses[i],
                    nature_of_issue=natures[i],
                    issue_description=issue_descs[i],
                    comments=comments[i]
                )
                db.session.add(form_entry)

            db.session.commit()
            return jsonify({'message': 'Interview schedule submitted successfully!'})

        except Exception as e:
            db.session.rollback()
            print("Error submitting interview schedule:", str(e))
            return jsonify({'error': 'Failed to submit interview schedule. Please try again.'}), 500


    # team 2 exit form
    @app.route('/submit_exit_information', methods=['POST'])
    @login_required
    def submit_exit_information():
        try:
            # Get all rows as lists
            departments = request.form.getlist('exit_department[]')
            notices = request.form.getlist('exit_notice[]')
            names = request.form.getlist('exit_name[]')
            depts = request.form.getlist('exit_dept[]')
            reasons = request.form.getlist('exit_reason[]')
            natures = request.form.getlist('exit_nature[]')
            issue_descs = request.form.getlist('exit_issue_desc[]')
            comments = request.form.getlist('exit_comments[]')

            for idx in range(len(departments)):
                if not any([departments[idx], notices[idx], names[idx]]):
                    # Skip empty rows
                    continue

                row = Team2ExitInformation(
                    team_id=current_user.team_id,
                    submitted_by=current_user.user_id,
                    exit_activity="Exit",
                    exit_department=departments[idx],
                    exit_notice=notices[idx],
                    exit_name=names[idx],
                    exit_dept=depts[idx],
                    exit_reason=reasons[idx],
                    exit_nature=natures[idx],
                    exit_issue_desc=issue_descs[idx],
                    exit_comments=comments[idx]
                )
                db.session.add(row)

            db.session.commit()
            return jsonify({'message': 'Exit information submitted successfully!'})

        except Exception as e:
            db.session.rollback()
            print("Error submitting exit information:", str(e))
            return jsonify({'error': 'Failed to submit exit information. Please try again.'}), 500

    # team 2 issues staff concerns

    @app.route('/submit_issues_staff_concerns', methods=['POST'])
    @login_required
    def submit_issues_staff_concerns():
        try:
            # Extract lists from the form
            concern_snos = request.form.getlist('concern_sno[]')
            concern_activities = request.form.getlist('concern_activity[]')
            concern_depts = request.form.getlist('concern_dept[]')
            concern_persons = request.form.getlist('concern_person[]')
            concern_incharges = request.form.getlist('concern_incharge[]')
            concern_natures = request.form.getlist('concern_nature[]')
            concern_issue_descs = request.form.getlist('concern_issue_desc[]')
            concern_comments = request.form.getlist('concern_comments[]')

            # Iterate over rows
            for i in range(len(concern_snos)):
                dept = concern_depts[i].strip()
                person = concern_persons[i].strip()
                incharge = concern_incharges[i].strip()
                nature = concern_natures[i].strip()
                issue_desc = concern_issue_descs[i].strip()
                comments = concern_comments[i].strip()

                # Skip empty rows (if all fields except sno & activity are empty)
                if not (dept or person or incharge or nature or issue_desc or comments):
                    continue

                new_concern = Team2IssuesStaffConcerns(
                    team_id=current_user.team_id,
                    submitted_by=current_user.user_id,
                    concern_sno=concern_snos[i],
                    concern_activity=concern_activities[i],
                    concern_dept=dept,
                    concern_person=person,
                    concern_incharge=incharge,
                    concern_nature=nature,
                    concern_issue_desc=issue_desc,
                    concern_comments=comments
                )

                db.session.add(new_concern)

            db.session.commit()
            return jsonify({'message': 'Issues / Staff Concerns submitted successfully!'})

        except Exception as e:
            db.session.rollback()
            print("Error submitting Issues / Staff Concerns:", str(e))
            return jsonify({'error': 'Failed to submit Issues / Staff Concerns. Please try again.'}), 500


    # team 2 kural recitation

    @app.route('/submit_kural_recitation', methods=['POST'])
    @login_required
    def submit_kural_recitation():
        try:
            new_kural_recitation = Team2KuralRecitation(
                team_id=current_user.team_id,
                submitted_by=current_user.user_id,
                kural_team=request.form.get('kural_team'),
                kural_name=request.form.get('kural_name'),
                kural_happened=request.form.get('kural_happened'),
                kural_not_happened_reason=request.form.get('kural_not_happened_reason'),
                kural_nature=request.form.get('kural_nature'),
                kural_issue_desc=request.form.get('kural_issue_desc'),
                kural_comments=request.form.get('kural_comments')
            )

            db.session.add(new_kural_recitation)
            db.session.commit()

            return jsonify({'message': 'Kural recitation submitted successfully!'})
        except Exception as e:
            db.session.rollback()
            print("Error submitting kural recitation:", str(e))
            return jsonify({'error': 'Failed to submit kural recitation. Please try again.'}), 500

    # team 2 Submit Front Office Phone Calls
    @app.route('/submit_front_office_phone_calls', methods=['POST'])
    @login_required
    def submit_front_office_phone_calls():
        try:
            categories = [
                ('Academics', 'fo_phone_acad_in', 'fo_phone_acad_out', 'fo_phone_acad_nature', 'fo_phone_acad_issue', 'fo_phone_acad_comments'),
                ('Admin', 'fo_phone_admin_in', 'fo_phone_admin_out', 'fo_phone_admin_nature', 'fo_phone_admin_issue', 'fo_phone_admin_comments'),
                ('General', 'fo_phone_gen_in', 'fo_phone_gen_out', 'fo_phone_gen_nature', 'fo_phone_gen_issue', 'fo_phone_gen_comments'),
            ]
            for cat, in_field, out_field, nature_field, issue_field, comments_field in categories:
                incoming = request.form.get(in_field)
                outgoing = request.form.get(out_field)
                nature = request.form.get(nature_field)
                issue_description = request.form.get(issue_field)
                comments = request.form.get(comments_field)
                # Only save if at least one field is filled
                if any([incoming, outgoing, nature, issue_description, comments]):
                    new_call = Team2FrontOfficePhoneCalls(
                        team_id=current_user.team_id,
                        submitted_by=current_user.user_id,
                        category=cat,
                        incoming=incoming,
                        outgoing=outgoing,
                        nature=nature,
                        issue_description=issue_description,
                        comments=comments
                    )
                    db.session.add(new_call)
            db.session.commit()
            return jsonify({'message': 'Front Office Phone Calls submitted successfully!'})
        except Exception as e:
            db.session.rollback()
            print("Error submitting front office phone calls:", str(e))
            return jsonify({'error': 'Failed to submit front office phone calls. Please try again.'}), 500

    # # team 2 Submit Visitor Log
    @app.route('/submit_visitor_log', methods=['POST'])
    @login_required
    def submit_visitor_log():
        try:
            # Get all rows from form arrays
            poc_list = request.form.getlist('vis_poc[]')
            purpose_list = request.form.getlist('vis_purpose[]')
            met_list = request.form.getlist('vis_met[]')
            nature_list = request.form.getlist('vis_nature[]')
            issue_list = request.form.getlist('vis_issue_desc[]')
            comments_list = request.form.getlist('vis_comments[]')

            for poc, purpose, met, nature, issue, comments in zip(
                poc_list, purpose_list, met_list, nature_list, issue_list, comments_list
            ):
                # Only save if at least one field is filled
                if any([poc.strip(), purpose.strip(), met.strip(), nature.strip(), issue.strip(), comments.strip()]):
                    new_visitor_log = Team2VisitorLog(
                        team_id=current_user.team_id,
                        submitted_by=current_user.user_id,
                        visitor_type=poc.strip(),
                        purpose=purpose.strip(),
                        person_met=met.strip(),
                        nature=nature.strip(),
                        issue_description=issue.strip(),
                        comments=comments.strip()
                    )
                    db.session.add(new_visitor_log)

            db.session.commit()
            return jsonify({'message': 'Visitor Log submitted successfully!'})

        except Exception as e:
            db.session.rollback()
            print("Error submitting visitor log:", str(e))
            return jsonify({'error': 'Failed to submit visitor log. Please try again.'}), 500


    # Submit BSNL Phone Status
    @app.route('/submit_bsnl_phone_status', methods=['POST'])
    @login_required
    def submit_bsnl_phone_status():
        try:
            new_bsnl_phone_status = Team2BSNLPhoneStatus(
                team_id=current_user.team_id,
                submitted_by=current_user.user_id,
                department='Front Office BSNL Phone',
                working=request.form.get('bsnl_working'),
                not_working=request.form.get('bsnl_not_working'),
                rectified=request.form.get('bsnl_rectified'),
                nature=request.form.get('bsnl_nature'),
                issue_description=request.form.get('bsnl_issue_desc'),
                comments=request.form.get('bsnl_comments')
            )
            db.session.add(new_bsnl_phone_status)
            db.session.commit()
            return jsonify({'message': 'BSNL Phone Status submitted successfully!'})
        except Exception as e:
            db.session.rollback()
            print("Error submitting BSNL phone status:", str(e))
            return jsonify({'error': 'Failed to submit BSNL phone status. Please try again.'}), 500

    # Submit Materials Inward
    @app.route('/submit_materials_inward', methods=['POST'])
    @login_required
    def submit_materials_inward():
        try:
            # Get all entries from form fields as lists
            products = request.form.getlist('mat_in_prod[]')
            times = request.form.getlist('mat_in_time[]')
            vendors = request.form.getlist('mat_in_vendor[]')
            descriptions = request.form.getlist('mat_in_desc[]')
            quantities = request.form.getlist('mat_in_qty[]')
            natures = request.form.getlist('mat_in_nature[]')
            issues = request.form.getlist('mat_in_issue[]')
            comments = request.form.getlist('mat_in_comments[]')

            # Loop through rows using length of product list
            for i in range(len(products)):
                if not products[i].strip():
                    continue  # Skip completely empty rows

                new_materials_inward = Team2MaterialsInward(
                    team_id=current_user.team_id,
                    submitted_by=current_user.user_id,
                    work_activity='Materials Inward',
                    department_category='Stores',
                    product_material=products[i],
                    in_time=times[i],
                    vendor=vendors[i],
                    description=descriptions[i],
                    quantity=safe_int(quantities[i]),
                    nature=natures[i],
                    issue_description=issues[i],
                    comments=comments[i]
                )
                db.session.add(new_materials_inward)

            db.session.commit()
            return jsonify({'message': 'Materials Inward submitted successfully!'})

        except Exception as e:
            db.session.rollback()
            print("Error submitting materials inward:", str(e))
            return jsonify({'error': 'Failed to submit materials inward. Please try again.'}), 500
    # team 2 materials outward
    from datetime import datetime

    @app.route('/submit_materials_outward', methods=['POST'])
    @login_required
    def submit_materials_outward():
        try:
            # Extract form field lists
            products = request.form.getlist('mat_out_prod[]')
            times = request.form.getlist('mat_out_time[]')
            vendors = request.form.getlist('mat_out_vendor[]')
            descriptions = request.form.getlist('mat_out_desc[]')
            quantities = request.form.getlist('mat_out_qty[]')
            natures = request.form.getlist('mat_out_nature[]')
            issues = request.form.getlist('mat_out_issue[]')
            comments = request.form.getlist('mat_out_comments[]')

            for i in range(len(products)):
                if not products[i].strip():
                    continue  # Skip empty rows

                # Parse time if provided
                out_time = None
                if times[i]:
                    try:
                        out_time = datetime.strptime(times[i], '%H:%M').time()
                    except ValueError:
                        pass  # Invalid time format will be stored as None

                new_outward = Team2MaterialsOutward(
                    team_id=current_user.team_id,
                    submitted_by=current_user.user_id,
                    work_activity='Materials Outward',
                    department='Materials',
                    product_material=products[i],
                    out_time=out_time,
                    vendor=vendors[i],
                    description=descriptions[i],
                    quantity=safe_int(quantities[i]),
                    nature=natures[i],
                    issue_description=issues[i],
                    comments=comments[i]
                )
                db.session.add(new_outward)

            db.session.commit()
            return jsonify({'message': 'Materials outward submitted successfully!'})

        except Exception as e:
            db.session.rollback()
            print("Error submitting materials outward:", str(e))
            return jsonify({'error': 'Failed to submit materials outward. Please try again.'}), 500


    # Submit Materials Movement
    @app.route('/submit_materials_movement', methods=['POST'])
    @login_required
    def submit_materials_movement():
        try:
            # Get all the row-wise field lists
            returnables = request.form.getlist('mat_move_ret[]')
            non_returnables = request.form.getlist('mat_move_nonret[]')
            natures = request.form.getlist('mat_move_nature[]')
            issues = request.form.getlist('mat_move_issue[]')
            comments = request.form.getlist('mat_move_comments[]')

            for ret, nonret, nature, issue, comment in zip(returnables, non_returnables, natures, issues, comments):
                # Skip empty rows (e.g., if all fields are blank)
                if not any([ret.strip(), nonret.strip(), nature.strip(), issue.strip(), comment.strip()]):
                    continue

                entry = Team2MaterialsMovement(
                    team_id=current_user.team_id,
                    submitted_by=current_user.user_id,
                    returnable=ret.strip(),
                    non_returnable=nonret.strip(),
                    nature=nature.strip(),
                    issue_description=issue.strip(),
                    comments=comment.strip()
                )
                db.session.add(entry)

            db.session.commit()
            return jsonify({'message': 'Materials Movement submitted successfully!'})

        except Exception as e:
            db.session.rollback()
            print("Error submitting materials movement:", str(e))
            return jsonify({'error': 'Failed to submit materials movement. Please try again.'}), 500

    # Submit Returnable Material Tracking
    @app.route('/submit_returnable_material_tracking', methods=['POST'])
    @login_required
    def submit_returnable_material_tracking():
        try:
            descriptions = request.form.getlist('returnable_desc[]')
            quantities = request.form.getlist('returnable_qty[]')
            issue_dates = request.form.getlist('returnable_issue_date[]')
            return_dates = request.form.getlist('returnable_return_date[]')
            natures = request.form.getlist('returnable_nature[]')
            issues = request.form.getlist('returnable_issue[]')
            comments_list = request.form.getlist('returnable_comments[]')

            for i in range(len(descriptions)):
                if not descriptions[i].strip():  # Skip empty rows
                    continue

                entry = Team2ReturnableMaterialTracking(
                    team_id=current_user.team_id,
                    submitted_by=current_user.user_id,
                    description=descriptions[i],
                    quantity=safe_int(quantities[i]),
                    issue_date=safe_date(issue_dates[i]),
                    return_date=safe_date(return_dates[i]),
                    nature=natures[i],
                    issue_description=issues[i],
                    comments=comments_list[i]
                )
                db.session.add(entry)

            db.session.commit()
            return jsonify({'message': 'Returnable Material Tracking submitted successfully!'})

        except Exception as e:
            db.session.rollback()
            print("Error submitting returnable material tracking:", str(e))
            return jsonify({'error': 'Failed to submit returnable material tracking. Please try again.'}), 500


    # team 2 returnable_goods_report
    @app.route('/submit_returnable_goods_report', methods=['POST'])
    @login_required
    def submit_returnable_goods_report():
        try:
            # We'll support up to 20 rows; adjust as needed
            max_rows = 20
            rows_added = 0
            for i in range(1, max_rows + 1):
                desc = request.form.get(f'returnable_report_desc_{i}')
                qty = request.form.get(f'returnable_report_qty_{i}')
                issue_date = request.form.get(f'returnable_report_issue_date_{i}')
                return_date = request.form.get(f'returnable_report_return_date_{i}')
                nature = request.form.get(f'returnable_report_nature_{i}')
                issue = request.form.get(f'returnable_report_issue_{i}')
                comments = request.form.get(f'returnable_report_comments_{i}')

                # Only save rows that have at least a description or quantity
                if desc or qty or issue_date or return_date or nature or issue or comments:
                    new_returnable_goods_report = Team2ReturnableGoodsReport(
                        team_id=current_user.team_id,
                        submitted_by=current_user.user_id,
                        description=desc,
                        quantity=safe_int(qty),
                        issue_date=safe_date(issue_date),
                        return_date=safe_date(return_date),
                        nature=nature,
                        issue_description=issue,
                        comments=comments
                    )
                    db.session.add(new_returnable_goods_report)
                    rows_added += 1
            if rows_added > 0:
                db.session.commit()
                return jsonify({'message': f'{rows_added} Returnable Goods Report row(s) submitted successfully!'})
            else:
                return jsonify({'error': 'No data to submit.'}), 400
        except Exception as e:
            db.session.rollback()
            print("Error submitting returnable goods report:", str(e))
            return jsonify({'error': 'Failed to submit returnable goods report. Please try again.'}), 500

    # team 2 campus_camera_status
    @app.route('/submit_campus_camera_status', methods=['POST'])
    @login_required
    def submit_campus_camera_status():
        try:
            # Get lists from the form
            particulars_list = request.form.getlist('cam_particulars[]')
            total_list = request.form.getlist('cam_total[]')
            working_list = request.form.getlist('cam_working[]')
            notworking_list = request.form.getlist('cam_notworking[]')
            nature_list = request.form.getlist('cam_nature[]')
            issue_desc_list = request.form.getlist('cam_issue_desc[]')
            comments_list = request.form.getlist('cam_comments[]')

            for i in range(len(particulars_list)):
                particulars = particulars_list[i].strip()
                total = total_list[i].strip()
                working = working_list[i].strip()
                notworking = notworking_list[i].strip()
                nature = nature_list[i].strip()
                issue_desc = issue_desc_list[i].strip()
                comments = comments_list[i].strip()

                # Skip empty rows (if no significant data entered)
                if not (particulars or total or working or notworking or nature or issue_desc or comments):
                    continue

                new_entry = Team2CampusCameraStatus(
                    team_id=current_user.team_id,
                    submitted_by=current_user.user_id,
                    work_activity='Camera & Monitoring',
                    department='Control Room',
                    particulars=particulars,
                    total_cameras=safe_int(total),
                    working_cameras=safe_int(working),
                    not_working_details=notworking,
                    nature_of_issue=nature,
                    issue_description=issue_desc,
                    comments=comments
                )
                db.session.add(new_entry)

            db.session.commit()
            return jsonify({'message': 'Campus Camera Status submitted successfully!'})

        except Exception as e:
            db.session.rollback()
            print("Error submitting campus camera status:", str(e))
            return jsonify({'error': 'Failed to submit campus camera status. Please try again.'}), 500

    # team 2 vehicle_camera_status
    @app.route('/submit_vehicle_camera_status', methods=['POST'])
    @login_required
    def submit_vehicle_camera_status():
        try:
            # Get lists from the form
            routes_list = request.form.getlist('cam_veh_route[]')
            camera_ids = request.form.getlist('cam_veh_camid[]')
            working_status_list = request.form.getlist('cam_veh_work[]')
            not_working_list = request.form.getlist('cam_veh_notwork[]')
            nature_list = request.form.getlist('cam_veh_nature[]')
            issue_desc_list = request.form.getlist('cam_veh_issue[]')
            comments_list = request.form.getlist('cam_veh_comments[]')

            # Iterate over rows
            for i in range(len(routes_list)):
                route_numbers = routes_list[i].strip()
                camera_id = camera_ids[i].strip()
                working_status = working_status_list[i].strip()
                not_working_details = not_working_list[i].strip()
                nature_of_issue = nature_list[i].strip()
                issue_description = issue_desc_list[i].strip()
                comments = comments_list[i].strip()

                # Skip empty rows (if all fields are blank)
                if not (route_numbers or camera_id or working_status or not_working_details or nature_of_issue or issue_description or comments):
                    continue

                # Create new entry
                entry = Team2VehicleCameraStatus(
                    team_id=current_user.team_id,
                    submitted_by=current_user.user_id,
                    work_activity='Camera & Monitoring',
                    department='Control Room',
                    particulars='Vehicles',
                    route_numbers=route_numbers,
                    camera_id=camera_id,
                    working_status=working_status,
                    not_working_details=not_working_details,
                    nature_of_issue=nature_of_issue,
                    issue_description=issue_description,
                    comments=comments
                )
                db.session.add(entry)

            # Commit all rows
            db.session.commit()
            return jsonify({'message': 'Vehicle Camera Status submitted successfully!'})

        except Exception as e:
            db.session.rollback()
            print("Error submitting vehicle camera status:", str(e))
            return jsonify({'error': 'Failed to submit vehicle camera status. Please try again.'}), 500

    # team 2 
    @app.route('/submit_bus_ac_camera_status', methods=['POST'])
    @login_required
    def submit_bus_ac_camera_status():
        try:
            # There are two rows: Morning and Evening
            periods = [('morn', 'Bus AC - Morning'), ('eve', 'Bus AC - Evening')]
            for period_key, particulars in periods:
                route = request.form.get(f'cam_busac_{period_key}_route')
                camera_id = request.form.get(f'cam_busac_{period_key}_camid')
                working_status = request.form.get(f'cam_busac_{period_key}_work')
                not_working_details = request.form.get(f'cam_busac_{period_key}_notwork')
                nature_of_issue = request.form.get(f'cam_busac_{period_key}_nature')
                issue_description = request.form.get(f'cam_busac_{period_key}_issue')
                comments = request.form.get(f'cam_busac_{period_key}_comments')

                # Only save if at least one field is filled
                if any([route, camera_id, working_status, not_working_details, nature_of_issue, issue_description, comments]):
                    entry = Team2BusACCameraStatus(
                        team_id=current_user.team_id,
                        submitted_by=current_user.user_id,
                        work_activity='Camera & Monitoring',
                        department='Control Room',
                        particulars=particulars,
                        route=route,
                        camera_id=camera_id,
                        working_status=working_status,
                        not_working_details=not_working_details,
                        nature_of_issue=nature_of_issue,
                        issue_description=issue_description,
                        comments=comments
                    )
                    db.session.add(entry)
            db.session.commit()
            return jsonify({'message': 'Bus AC Camera Status submitted successfully!'})
        except Exception as e:
            db.session.rollback()
            print("Error submitting bus AC camera status:", str(e))
            return jsonify({'error': 'Failed to submit bus AC camera status. Please try again.'}), 500

    # team 2 gps monitoring

    @app.route('/submit_gps_monitoring', methods=['POST'])
    @login_required
    def submit_gps_monitoring():
        try:
            import os
            from werkzeug.utils import secure_filename

            # Get lists from form
            vehicles_list = request.form.getlist('gps_vehicle[]')
            halt_list = request.form.getlist('gps_halt[]')
            speed_list = request.form.getlist('gps_speed[]')
            nature_list = request.form.getlist('gps_nature[]')
            issue_desc_list = request.form.getlist('gps_issue[]')
            comments_list = request.form.getlist('gps_comments[]')

            # Get files
            footage_files = request.files.getlist('gps_footage[]')

            # Iterate through rows
            for i in range(len(vehicles_list)):
                vehicles = vehicles_list[i].strip()
                halt_2_mins = halt_list[i].strip()
                over_speed = speed_list[i].strip()
                nature_of_issue = nature_list[i].strip()
                issue_description = issue_desc_list[i].strip()
                comments = comments_list[i].strip()

                # Handle file upload - Store as BLOB in database
                footage_file_id = None
                if i < len(footage_files) and footage_files[i]:
                    file = footage_files[i]
                    if file.filename:
                        # Check file size (200MB = 200 * 1024 * 1024 bytes)
                        file.seek(0, 2)  # Seek to end
                        file_size = file.tell()
                        file.seek(0)  # Reset to beginning

                        if file_size > 200 * 1024 * 1024:  # 200MB limit
                            return jsonify({'error': f'File {file.filename} is too large. Maximum size is 200MB.'}), 400

                        # Read file data
                        file_data = file.read()

                        # Secure the filename
                        original_filename = secure_filename(file.filename)
                        # Add timestamp to make filename unique
                        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                        filename = f"{timestamp}_{original_filename}"

                        # Determine MIME type
                        mime_type = file.content_type or 'application/octet-stream'

                        # Create file storage record
                        file_record = FileStorage(
                            filename=filename,
                            original_filename=original_filename,
                            file_data=file_data,
                            file_size=file_size,
                            mime_type=mime_type,
                            uploaded_by=current_user.user_id
                        )
                        db.session.add(file_record)
                        db.session.flush()  # Get the file_id

                        footage_file_id = file_record.file_id

                # Skip empty rows
                if not (vehicles or halt_2_mins or over_speed or footage_file_id or nature_of_issue or issue_description or comments):
                    continue

                # Create new entry
                entry = Team2GPSMonitoring(
                    team_id=current_user.team_id,
                    submitted_by=current_user.user_id,
                    work_activity='Camera & Monitoring',
                    department='Control Room',
                    particulars='GPS',
                    vehicles=vehicles,
                    halt_2_mins=halt_2_mins,
                    over_speed=over_speed,
                    footage_file_id=footage_file_id,
                    nature_of_issue=nature_of_issue,
                    issue_description=issue_description,
                    comments=comments
                )
                db.session.add(entry)

            # Commit all entries
            db.session.commit()
            return jsonify({'message': 'GPS Monitoring submitted successfully!'})

        except Exception as e:
            db.session.rollback()
            print("Error submitting GPS monitoring:", str(e))
            return jsonify({'error': 'Failed to submit GPS monitoring. Please try again.'}), 500


    # team 2 issues identified monitoring
    @app.route('/submit_issues_identified_monitoring', methods=['POST'])
    @login_required
    def submit_issues_identified_monitoring():
        try:
            # Get lists from the form
            venues = request.form.getlist('issid_venue[]')
            times = request.form.getlist('issid_time[]')
            natures = request.form.getlist('issid_nature[]')
            escalated_list = request.form.getlist('issid_escalated[]')
            actions = request.form.getlist('issid_action[]')
            any_issues_list = request.form.getlist('issid_observation[]')
            for i in range(len(venues)):
                venue = venues[i].strip()
                time = times[i].strip()
                nature_of_issue = natures[i].strip()
                escalated_to = escalated_list[i].strip()
                action_taken = actions[i].strip()
                any_issues_on_observation = any_issues_list[i].strip()
                # Skip empty rows
                if not (venue or time or nature_of_issue or escalated_to or action_taken):
                    continue

                # Create entry
                entry = Team2IssuesIdentifiedMonitoring(
                    team_id=current_user.team_id,
                    submitted_by=current_user.user_id,
                    work_activity='Camera & Monitoring',
                    department='Control Room',
                    particulars='Issues Identified',
                    venue=venue,
                    time=safe_time(time),
                    nature_of_issue=nature_of_issue,
                    escalated_to=escalated_to,
                    action_taken=action_taken,
                    any_issues_on_observation=any_issues_on_observation
                )
                db.session.add(entry)

            db.session.commit()
            return jsonify({'message': 'Issues Identified (Monitoring) submitted successfully!'})

        except Exception as e:
            db.session.rollback()
            print("Error submitting issues identified monitoring:", str(e))
            return jsonify({'error': 'Failed to submit issues identified monitoring. Please try again.'}), 500



    # team 2 teachers late reporting
    @app.route('/submit_teachers_late_reporting', methods=['POST'])
    @login_required
    def submit_teachers_late_reporting():
        try:
            # Get all form data as lists
            late_counts = request.form.getlist('late_teach_count[]')
            reason_counts = request.form.getlist('late_teach_reason_entered[]')
            acks = request.form.getlist('late_teach_ack[]')
            natures = request.form.getlist('late_teach_nature[]')
            escalated_list = request.form.getlist('late_teach_escalated[]')
            actions = request.form.getlist('late_teach_action[]')

            for i in range(len(late_counts)):
                no_of_late_reports = late_counts[i].strip()
                no_of_members_entered_reason = reason_counts[i].strip()
                ack = acks[i].strip()
                nature_of_issue = natures[i].strip()
                escalated_to = escalated_list[i].strip()
                action_taken = actions[i].strip()

                # Skip empty rows (all fields empty)
                if not (no_of_late_reports or no_of_members_entered_reason or ack or nature_of_issue or escalated_to or action_taken):
                    continue

                entry = Team2IssuesIdentifiedControlRoom(
                    team_id=current_user.team_id,
                    submitted_by=current_user.user_id,
                    work_activity='Camera & Monitoring',
                    department='Control Room',
                    particulars='Teachers Late reporting to class',
                    no_of_late_reports=safe_int(no_of_late_reports),
                    no_of_members_entered_reason=safe_int(no_of_members_entered_reason),
                    on_time_acknowledgement=ack,
                    nature_of_issue=nature_of_issue,
                    escalated_to=escalated_to,
                    action_taken=action_taken
                )
                db.session.add(entry)

            db.session.commit()
            return jsonify({'message': 'Teachers Late Reporting to Class submitted successfully!'})

        except Exception as e:
            db.session.rollback()
            print("Error submitting teachers late reporting:", str(e))
            return jsonify({'error': 'Failed to submit teachers late reporting. Please try again.'}), 500

    # team 2 camera footage entry
    @app.route('/submit_camera_footage', methods=['POST'])
    @login_required
    def submit_camera_footage():
        try:
            particulars_list = request.form.getlist('footage_particulars[]')
            names_list = request.form.getlist('footage_name[]')
            comments_list = request.form.getlist('footage_comments[]')

            for i in range(len(particulars_list)):
                particulars = particulars_list[i].strip()
                name = names_list[i].strip()
                comments = comments_list[i].strip()

                # Skip empty rows
                if not (particulars or name or comments):
                    continue

                entry = Team2CameraFootageEntry(
                    team_id=current_user.team_id,
                    submitted_by=current_user.user_id,
                    work_activity='Camera & Monitoring',
                    department='Control Room',
                    particulars=particulars,
                    name=name,
                    comments=comments
                )
                db.session.add(entry)

            db.session.commit()
            return jsonify({'message': 'Camera & Monitoring Footage Data submitted successfully!'})

        except Exception as e:
            db.session.rollback()
            print("Error submitting camera footage data:", str(e))
            return jsonify({'error': 'Failed to submit camera footage data. Please try again.'}), 500



    # team 2 9 biometrics punching
    @app.route('/submit_biometrics_punching', methods=['POST'])
    @login_required
    def submit_biometrics_punching():
        try:
            # Get all list-based form entries
            categories = request.form.getlist('bio_category[]')
            totals = request.form.getlist('bio_total[]')
            absents = request.form.getlist('bio_absent[]')
            puncheds = request.form.getlist('bio_punched[]')
            not_puncheds = request.form.getlist('bio_notpunched[]')
            natures = request.form.getlist('bio_nature[]')
            issues = request.form.getlist('bio_issue[]')
            comments = request.form.getlist('bio_comments[]')

            entries = []

            for i in range(len(categories)):
                category = categories[i].strip()

                if not category:
                    continue  # skip empty rows

                new_entry = Team2BiometricsAccessCardPunching(
                    team_id=current_user.team_id,
                    submitted_by=current_user.user_id,
                    particulars=category,
                    total_punching=safe_int(totals[i]),
                    absent_punching=safe_int(absents[i]),
                    punched_punching=safe_int(puncheds[i]),
                    not_punching=safe_int(not_puncheds[i]),
                    nature_of_issue=natures[i],
                    issue_description=issues[i],
                    comments=comments[i]
                )
                entries.append(new_entry)

            # Commit all entries at once
            if entries:
                db.session.add_all(entries)
                db.session.commit()

            return jsonify({'message': 'Biometrics Access Card Punching data submitted successfully!'})

        except Exception as e:
            db.session.rollback()
            print("Error submitting biometrics punching:", str(e))
            return jsonify({'error': 'Failed to submit biometrics punching. Please try again.'}), 500


    # Flask route to handle Water TDS Deviation submission
    @app.route('/submit_water_tds_deviation', methods=['POST'])
    @login_required
    def submit_water_tds_deviation():
        try:
            tds_floors = request.form.getlist('tds_floor[]')
            tds_values = request.form.getlist('tds_value[]')
            ph_values = request.form.getlist('ph_value[]')
            tds_natures = request.form.getlist('tds_nature[]')
            tds_issues = request.form.getlist('tds_issue[]')
            tds_comments = request.form.getlist('tds_comments[]')

            for i in range(len(tds_floors)):
                # Extract individual row fields
                floor = tds_floors[i]
                tds = tds_values[i]
                ph = ph_values[i]
                nature = tds_natures[i]
                issue_desc = tds_issues[i]
                comments = tds_comments[i]

                # Only save if at least one field is filled
                if any([floor, tds, ph, nature, issue_desc, comments]):
                    entry = Team2WaterTDSDeviation(
                        team_id=current_user.team_id,
                        submitted_by=current_user.user_id,
                        particulars='RO Water Quality',
                        ro_details=floor,
                        tds=float(tds) if tds else None,
                        ph=float(ph) if ph else None,
                        nature_of_issue=nature,
                        issue_description=issue_desc,
                        comments=comments
                    )
                    db.session.add(entry)

            db.session.commit()
            return jsonify({'message': 'Water TDS Deviation submitted successfully!'})

        except Exception as e:
            db.session.rollback()
            print("Error submitting Water TDS Deviation:", str(e))
            return jsonify({'error': 'Failed to submit Water TDS Deviation. Please try again.'}), 500


    #11. Testing & Cleaning and Pool Testing

    @app.route('/submit_testing_cleaning', methods=['POST'])
    @login_required
    def submit_testing_cleaning():  
        try:
            # Create new record for general cleaning section
            general_cleaning = Team2TestingCleaning(
            team_id=current_user.team_id,
            submitted_by=current_user.user_id,
            particulars='Cleaning',
            regular_process=request.form.get('clean_regular'),
            deep_cleaning=request.form.get('clean_deep'),
            event_arrangement=request.form.get('clean_event'),
            nature_of_issue=request.form.get('clean_nature'),
            issue_description=request.form.get('clean_issue'),
            comments=request.form.get('clean_comments')
            )

            db.session.add(general_cleaning)
            db.session.commit()

            return jsonify({'message': 'Testing & Cleaning details submitted successfully!'})
        except Exception as e:
            db.session.rollback()
            print("Error submitting testing & cleaning:", str(e))
            return jsonify({'error': 'Failed to submit testing & cleaning. Please try again.'}), 500

        # Water Level Checking
    @app.route('/submit_water_level', methods=['POST'])
    @login_required
    def submit_water_level():
        try:
            work_activities = request.form.getlist('water_work_activity[]')
            departments = request.form.getlist('water_department[]')
            particulars_list = request.form.getlist('water_particulars[]')
            floors = request.form.getlist('water_floor[]')
            venues = request.form.getlist('water_venue[]')
            nature_list = request.form.getlist('water_nature[]')
            issue_descriptions = request.form.getlist('water_issue_desc[]')
            comments_list = request.form.getlist('water_comments[]')

            for i in range(len(work_activities)):
                # Extract row data
                work_activity = work_activities[i].strip()
                department = departments[i].strip()
                particulars = particulars_list[i].strip()
                floor = floors[i].strip()
                venue = venues[i].strip()
                nature_of_issue = nature_list[i].strip()
                issue_description = issue_descriptions[i].strip()
                comments = comments_list[i].strip()

                # ✅ Skip row if all fields are empty
                if not any([work_activity, department, particulars, floor, venue, nature_of_issue, issue_description, comments]):
                    continue

                entry = Team2WaterLevel(
                    team_id=current_user.team_id,
                    submitted_by=current_user.user_id,
                    work_activity=work_activity,
                    department=department,
                    particulars=particulars,
                    floor=floor,
                    venue=venue,
                    nature_of_issue=nature_of_issue,
                    issue_description=issue_description,
                    comments=comments
                )

                db.session.add(entry)

            db.session.commit()
            return jsonify({'message': 'Water Level Checking details submitted successfully!'})

        except Exception as e:
            db.session.rollback()
            print("Error submitting water level:", str(e))
            return jsonify({'error': 'Failed to submit water level details. Please try again.'}), 500

        # Housekeeping General
    @app.route('/submit_housekeeping_general', methods=['POST'])
    @login_required
    def submit_housekeeping_general():
        try:
            work_activities = request.form.getlist('hk_work_activity[]')
            departments = request.form.getlist('hk_department[]')
            particulars_list = request.form.getlist('hk_particulars[]')
            names = request.form.getlist('hk_name[]')
            observations = request.form.getlist('hk_observation[]')
            remarks_list = request.form.getlist('hk_remark[]')

            for i in range(len(work_activities)):
                work_activity = work_activities[i].strip()
                department = departments[i].strip()
                particulars = particulars_list[i].strip()
                name = names[i].strip()
                observation = observations[i].strip()
                remark = remarks_list[i].strip()

                # Skip empty rows
                if not any([work_activity, department, particulars, name, observation, remark]):
                    continue

                entry = Team2HousekeepingGeneral(
                    team_id=current_user.team_id,
                    submitted_by=current_user.user_id,
                    work_activity=work_activity,
                    department=department,
                    particulars=particulars,
                    name=name,
                    observation=observation,
                    remark=remark
                )

                db.session.add(entry)

            db.session.commit()
            return jsonify({'message': 'Housekeeping General details submitted successfully!'})

        except Exception as e:
            db.session.rollback()
            print("Error submitting housekeeping general:", str(e))
            return jsonify({'error': 'Failed to submit housekeeping general details. Please try again.'}), 500



    #11. Testing & Cleaning and Pool Testing

    @app.route('/submit_pool_testing', methods=['POST'])
    @login_required
    def submit_pool_testing():
        try:
            pool_testing = Team2PoolTesting(
            team_id=current_user.team_id,
            submitted_by=current_user.user_id,
            particulars='Wading Pool',
            chlorine_level=safe_float(request.form.get('pool_chlorine')),
            ph_level=safe_float(request.form.get('pool_ph')),
            water_cleanliness=request.form.get('pool_cleanliness'),
            nature_of_issue=request.form.get('pool_nature'),
            issue_description=request.form.get('pool_issue'),
            comments=request.form.get('pool_comments')
            )

            db.session.add(pool_testing)
            db.session.commit()

            return jsonify({'message': 'Pool Testing details submitted successfully!'})
        except Exception as e:
            db.session.rollback()
            print("Error submitting pool testing:", str(e))
            return jsonify({'error': 'Failed to submit pool testing. Please try again.'}), 500

    # ============================
    # Route: Submit Washroom Cleanliness (Section 12)
    # ============================
    @app.route('/submit_washroom_cleanliness', methods=['POST'])
    @login_required
    def submit_washroom_cleanliness():
        try:
            # Collect lists from the dynamic form
            floors = request.form.getlist('wr_floor[]')
            particulars_list = request.form.getlist('wr_particulars[]')
            boys_list = request.form.getlist('wr_boys[]')
            girls_list = request.form.getlist('wr_girls[]')
            cleanliness_list = request.form.getlist('wr_cleanliness[]')
            smell_list = request.form.getlist('wr_smell[]')
            equipment_list = request.form.getlist('wr_equipment[]')

            entries = []

            for i in range(len(floors)):
                floor = floors[i].strip()
                particulars = particulars_list[i].strip()
                boys = boys_list[i].strip()
                girls = girls_list[i].strip()
                cleanliness = cleanliness_list[i].strip()
                smell = smell_list[i].strip()
                equipment = equipment_list[i].strip()

                # ✅ Skip empty row if all fields are blank
                if not any([floor, particulars, boys, girls, cleanliness, smell, equipment]):
                    continue

                entry = Team2WashroomCleanliness(
                    team_id=current_user.team_id,
                    submitted_by=current_user.user_id,
                    floor=floor,
                    particulars=particulars,
                    boys_washroom=boys,
                    girls_washroom=girls,
                    cleanliness=cleanliness,
                    smell=smell,
                    restroom_equipment=equipment
                )
                entries.append(entry)

            if entries:
                db.session.add_all(entries)
                db.session.commit()
                return jsonify({'message': 'Washroom Cleanliness report submitted successfully!'})
            else:
                return jsonify({'message': 'No valid rows submitted.'}), 400

        except Exception as e:
            db.session.rollback()
            print("Error submitting washroom cleanliness:", str(e))
            return jsonify({'error': 'Failed to submit washroom cleanliness. Please try again.'}), 500

    # ============================================
    # Route: Submit Transport Attendance (Section 13 - Part 1)
    # ============================================
    @app.route('/submit_transport_attendance', methods=['POST'])
    @login_required
    def submit_transport_attendance():
        try:
            attendance_entry = Team2TransportAttendance(
            team_id=current_user.team_id,
            submitted_by=current_user.user_id,
            particulars='Overall Attendance',
            students_morning=request.form.get('trans_att_stud_morn'),
            students_evening=request.form.get('trans_att_stud_eve'),
            staff_morning=request.form.get('trans_att_staff_morn'),
            staff_evening=request.form.get('trans_att_staff_eve'),
            nature_of_issue=request.form.get('trans_att_nature'),
            issue_description=request.form.get('trans_att_issue'),
            comments=request.form.get('trans_att_comments')
        )

            db.session.add(attendance_entry)
            db.session.commit()

            return jsonify({'message': 'Transport attendance submitted successfully!'})
        except Exception as e:
            db.session.rollback()
            print("Error submitting transport attendance:", str(e))
            return jsonify({'error': 'Failed to submit transport attendance. Please try again.'}), 500

    # ================================================
    # Route: Submit AC Working Status (Section 13 - Part 2)
    # ================================================
    @app.route('/submit_transport_ac_status', methods=['POST'])
    @login_required
    def submit_transport_ac_status():
        try:
            ac_status_entry = Team2ACWorkingStatus(
            team_id=current_user.team_id,
                submitted_by=current_user.user_id,
            particulars='AC - Working / Not working',
            route_numbers=request.form.get('trans_ac_routes'),
            nature_of_issue=request.form.get('trans_ac_nature'),
            issue_description=request.form.get('trans_ac_issue'),
            comments=request.form.get('trans_ac_comments')
        )

            db.session.add(ac_status_entry)
            db.session.commit()

            return jsonify({'message': 'AC working status submitted successfully!'})
        except Exception as e:
            db.session.rollback()
            print("Error submitting AC working status:", str(e))
            return jsonify({'error': 'Failed to submit AC working status. Please try again.'}), 500

    # =================================================
    # Route: Submit Late Reporting (Section 13 - Part 3)
    # =================================================
    @app.route('/submit_late_reporting', methods=['POST'])
    @login_required
    def submit_late_reporting():
        try:
            late_report = Team2LateReporting(
            team_id=current_user.team_id,
            submitted_by=current_user.user_id,
            particulars='Late Reporting Mention If beyond 8.40 am',
            route_numbers=request.form.get('trans_late_routes'),
            nature_of_issue=request.form.get('trans_late_nature'),
            issue_description=request.form.get('trans_late_issue'),
            comments=request.form.get('trans_late_comments')
            )

            db.session.add(late_report)
            db.session.commit()

            return jsonify({'message': 'Late reporting submitted successfully!'})
        except Exception as e:
            db.session.rollback()
            print("Error submitting late reporting:", str(e))
            return jsonify({'error': 'Failed to submit late reporting. Please try again.'}), 500

    # =====================================================================
    # Route: Submit Maintenance / Service / Issues (Section 13 - Part 4)
    # =====================================================================
    @app.route('/submit_maintenance_service', methods=['POST'])
    @login_required
    def submit_maintenance_service():
        try:
            # Get lists from form
            routes = request.form.getlist('trans_maint_route[]')
            natures = request.form.getlist('trans_maint_nature[]')
            venues = request.form.getlist('trans_maint_venue[]')
            statuses = request.form.getlist('trans_maint_status[]')
            issues_nature = request.form.getlist('trans_maint_issnature[]')
            issue_desc = request.form.getlist('trans_maint_issue[]')
            comments = request.form.getlist('trans_maint_comments[]')

            entries = []

            for i in range(len(routes)):
                # Skip completely empty rows
                if any([routes[i], natures[i], venues[i], statuses[i], issue_desc[i], comments[i]]):
                    entry = Team2MaintenanceServiceIssues(
                        team_id=current_user.team_id,
                        submitted_by=current_user.user_id,
                        particulars='Maintenance / Service / Issues [If any]',
                        route_numbers=routes[i],
                        work_nature=natures[i],
                        venue=venues[i],
                        work_status=statuses[i],
                        nature_of_issue=issues_nature[i],
                        issue_description=issue_desc[i],
                        comments=comments[i]
                    )
                    entries.append(entry)

            if entries:
                db.session.add_all(entries)
                db.session.commit()

            return jsonify({'message': 'Maintenance / Service issues submitted successfully!'})

        except Exception as e:
            db.session.rollback()
            print("Error submitting maintenance service:", str(e))
            return jsonify({'error': 'Failed to submit maintenance service. Please try again.'}), 500


    # ------------------- Part 13 - Transport - Part 5: Car Maintenance/Cleaning -------------------

    @app.route('/submit_car_maintenance', methods=['POST'])
    @login_required
    def submit_car_maintenance():
        try:
            car_numbers = ['TN 58 BL 1248', 'TN 11 E 6333', 'TN 58 BL 2732', 'TN 36 AS 5995', 'TN 58 BK 5035']
            for i, car_number in enumerate(car_numbers, 1):
                entry = Team2CarMaintenanceCleaning(
                team_id=current_user.team_id,
                submitted_by=current_user.user_id,
                particulars='Car',
                car_number=car_number,
                cleaned_by=request.form.get(f'car_clean_{i}'),
                maintenance_service_issues=request.form.get(f'car_maint_{i}'),
                nature_of_issue=request.form.get(f'car_nature_{i}'),
                issue_description=request.form.get(f'car_issue_{i}'),
                comments=request.form.get(f'car_comments_{i}'),

                )
                db.session.add(entry)
                db.session.commit()
            return jsonify({'message': 'Car maintenance submitted successfully!'})
        except Exception as e:
            db.session.rollback()
            print("Error submitting car maintenance:", str(e))
            return jsonify({'error': 'Failed to submit car maintenance. Please try again.'}), 500

    # ------------------- Part 13 - Transport - Part 6: Vehicle Renewals / Delays -------------------

    @app.route('/submit_renewals', methods=['POST'])
    @login_required
    def submit_renewals():
        try:
            rows = [
                ('Delayed Halt', 'trans_delay_vehicles', 'trans_delay_routes', 'trans_delay_nature', 'trans_delay_issue', 'trans_delay_comments'),
                ('FC Renewal [1 Month prior from expiry]', 'trans_fc_vehicles', 'trans_fc_routes', 'trans_fc_nature', 'trans_fc_issue', 'trans_fc_comments'),
                ('Road Tax [1 Month prior from expiry]', 'trans_tax_vehicles', 'trans_tax_routes', 'trans_tax_nature', 'trans_tax_issue', 'trans_tax_comments'),
                ('Permit [1 Month prior from expiry]', 'trans_permit_vehicles', 'trans_permit_routes', 'trans_permit_nature', 'trans_permit_issue', 'trans_permit_comments'),
                ('Insurance [1 Month prior from expiry]', 'trans_ins_vehicles', 'trans_ins_routes', 'trans_ins_nature', 'trans_ins_issue', 'trans_ins_comments')
            ]

            entries = []
            for particulars, veh_field, route_field, nature_field, issue_field, comment_field in rows:
                entry = Team2VehicleRenewalsDelays(
                    team_id=current_user.team_id,
                    submitted_by=current_user.user_id,
                    particulars=particulars,
                    vehicle_numbers=request.form.get(veh_field),
                    route_numbers=request.form.get(route_field),
                    nature_of_issue=request.form.get(nature_field),
                    issue_description=request.form.get(issue_field),
                    comments=request.form.get(comment_field),
                )
                entries.append(entry)

            db.session.add_all(entries)
            db.session.commit()
            return jsonify({'message': 'Vehicle renewals submitted successfully!'})
        except Exception as e:
            db.session.rollback()
            print("Error submitting vehicle renewals:", str(e))
            return jsonify({'error': 'Failed to submit vehicle renewals. Please try again.'}), 500

    # ------------------- Part 13 - Transport - Part 7: Special Trip -------------------
    @app.route('/submit_special_trip', methods=['POST'])
    @login_required
    def submit_special_trip():
        try:
            entries = []

            routes = request.form.getlist('trans_trip_route[]')
            times = request.form.getlist('trans_trip_time[]')
            natures = request.form.getlist('trans_trip_nature[]')
            issues = request.form.getlist('trans_trip_issue[]')
            comments_list = request.form.getlist('trans_trip_comments[]')

            for route, time, nature, issue, comments in zip(routes, times, natures, issues, comments_list):
                # Only save if at least one field is filled
                if any([route.strip(), time.strip(), nature.strip(), issue.strip(), comments.strip()]):
                    entry = Team2SpecialTrip(
                        team_id=current_user.team_id,
                        submitted_by=current_user.user_id,
                        particulars='Special Trip planned time',
                        route_numbers=route.strip(),
                        actual_out_time=time.strip(),
                        nature_of_issue=nature.strip(),
                        issue_description=issue.strip(),
                        comments=comments.strip(),
                    )
                    entries.append(entry)

            if entries:
                db.session.add_all(entries)
                db.session.commit()

            return jsonify({'message': 'Special trip submitted successfully!'})

        except Exception as e:
            db.session.rollback()
            print("Error submitting special trip:", str(e))
            return jsonify({'error': 'Failed to submit special trip. Please try again.'}), 500

    # ------------------- Part 13 - Transport - Part 8: Parent Concern Details -------------------
    @app.route('/team_2_submit_parent_concern_detail', methods=['POST'])
    @login_required
    def team_2_submit_parent_concern_detail():
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
                    detail = Team2ParentConcernDetail(
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


        # =========================
    # Route: AC Temperature Check (Section 14)
    # =========================
    @app.route('/submit_ac_temp', methods=['POST'])
    @login_required
    def submit_ac_temp():
        try:
            floor = request.form.get('ac_floor')  # Dropdown applies to all rows

            # Debug: Print form data
            print("Form data received:", dict(request.form))
            print("Floor selected:", floor)

            # Process 9 rows (CR1-CR8 + Others)
            entries_added = 0
            for i in range(1, 10):
                temperature = request.form.get(f'ac_temp_{i}')
                hot_cold_normal = request.form.get(f'ac_status_{i}')
                working_condition = request.form.get(f'ac_working_{i}')
                nature_of_issue = request.form.get(f'ac_nature_{i}')
                issue_description = request.form.get(f'ac_issue_{i}')
                comments = request.form.get(f'ac_comments_{i}')

                # Debug: Print row data
                print(f"Row {i} data: temp={temperature}, status={hot_cold_normal}, working={working_condition}, nature={nature_of_issue}, issue={issue_description}, comments={comments}")

                # Skip row if all fields are empty
                if not any([temperature, hot_cold_normal, working_condition, nature_of_issue, issue_description, comments]):
                    print(f"Row {i} skipped - all fields empty")
                    continue

                # Map classroom names
                classroom_names = ['CR1', 'CR2', 'CR3', 'CR4', 'CR5', 'CR6', 'CR7', 'CR8', 'Others']
                classroom_name = classroom_names[i-1]

                entry = Team2ACTemperatureCheck(
                    team_id=current_user.team_id,
                    submitted_by=current_user.user_id,
                    floor=floor,
                    particulars='Maintenance and Service',
                    classroom=classroom_name,
                    temperature=temperature,
                    hot_cold_normal=hot_cold_normal,
                    working_condition=working_condition,
                    nature_of_issue=nature_of_issue,
                    issue_description=issue_description,
                    comments=comments,
                )
                db.session.add(entry)
                entries_added += 1
                print(f"Added entry for {classroom_name}")

            db.session.commit()
            print(f"Successfully committed {entries_added} entries to database")
            return jsonify({'message': 'AC Temperature Check submitted successfully.'})
        except Exception as e:
            db.session.rollback()
            print("Error submitting AC Temperature Check:", str(e))
            return jsonify({'error': 'Failed to submit AC Temperature Check. Please try again.'}), 500

    # ============================
    # Route: Section 15 - Part 1
    # Labor, EB, Solar, Genset
    # ============================
    @app.route('/submit_labor_eb_solar_genset', methods=['POST'])
    @login_required
    def submit_labor_eb_solar_genset():
        try:
            works = request.form.getlist('maint_labor_work[]')
            counts = request.form.getlist('maint_labor_count[]')
            venues = request.form.getlist('maint_labor_venue[]')
            natures = request.form.getlist('maint_labor_nature[]')
            issues = request.form.getlist('maint_labor_issue[]')
            comments = request.form.getlist('maint_labor_comments[]')

            # Ensure all lists are the same length
            row_count = len(works)

            for i in range(row_count):
                # Skip empty rows (check if all fields are empty)
                if not (works[i] or counts[i] or venues[i] or issues[i] or comments[i]):
                    continue

                entry = Team2LaborEbSolarGenset(
                    team_id=current_user.team_id,
                    submitted_by=current_user.user_id,
                    nature_of_work=works[i],
                    no_of_labours=counts[i],
                    venue=venues[i],
                    nature_of_issue=natures[i],
                    issue_description=issues[i],
                    comments=comments[i]
                )
                db.session.add(entry)

            db.session.commit()
            return jsonify({'message': 'Labor, EB, Solar, Genset submitted successfully.'})

        except Exception as e:
            db.session.rollback()
            print("Error submitting labor, EB, Solar, Genset:", str(e))
            return jsonify({'error': 'Failed to submit labor, EB, Solar, Genset. Please try again.'}), 500


    # ============================
    # Route: Section 15 - Part 2a
    # Motor Control
    # ============================
    @app.route('/submit_motor', methods=['POST'])
    @login_required
    def submit_motor():
        try:
            on_times = request.form.getlist('motor_on_time[]')
            off_times = request.form.getlist('motor_off_time[]')
            natures = request.form.getlist('motor_nature[]')
            issues = request.form.getlist('motor_issue[]')
            comments = request.form.getlist('motor_comments[]')

            # Create an entry for each row
            for i in range(len(on_times)):
                if on_times[i] or off_times[i] or natures[i] or issues[i] or comments[i]:  # Only create if at least one field has data
                    motor_entry = Team2Motor(
                        team_id=current_user.team_id,
                        submitted_by=current_user.user_id,
                        on_time=on_times[i] if on_times[i] else None,
                        off_time=off_times[i] if off_times[i] else None,
                        nature_of_issue=natures[i] if natures[i] else None,
                        issue_description=issues[i] if issues[i] else None,
                        comments=comments[i] if comments[i] else None
                    )
                    db.session.add(motor_entry)

            db.session.commit()
            return jsonify({'message': 'Motor Control submitted successfully.'})
        except Exception as e:
            db.session.rollback()
            print("Error submitting Motor Control:", str(e))
            return jsonify({'error': 'Failed to submit Motor Control. Please try again.'}), 500

    # ============================
    # Route: Section 15 - Part 2b
    # Pest Control
    # ============================
    @app.route('/submit_pest_control', methods=['POST'])
    @login_required
    def submit_pest_control():
        try:
            in_times = request.form.getlist('pest_in_time[]')
            out_times = request.form.getlist('pest_out_time[]')
            areas = request.form.getlist('pest_area[]')
            natures = request.form.getlist('pest_nature[]')
            issues = request.form.getlist('pest_issue[]')
            comments = request.form.getlist('pest_comments[]')

            # Create an entry for each row
            for i in range(len(in_times)):
                if in_times[i] or out_times[i] or areas[i] or natures[i] or issues[i] or comments[i]:  # Only create if at least one field has data
                    pest_entry = Team2PestControl(
                        team_id=current_user.team_id,
                        submitted_by=current_user.user_id,
                        in_time=in_times[i] if in_times[i] else None,
                        out_time=out_times[i] if out_times[i] else None,
                        area_covered=areas[i] if areas[i] else None,
                        nature_of_issue=natures[i] if natures[i] else None,
                        issue_description=issues[i] if issues[i] else None,
                        comments=comments[i] if comments[i] else None
                    )
                    db.session.add(pest_entry)

            db.session.commit()
            return jsonify({'message': 'Pest Control submitted successfully.'})
        except Exception as e:
            db.session.rollback()
            print("Error submitting Pest Control:", str(e))
            return jsonify({'error': 'Failed to submit Pest Control. Please try again.'}), 500
    # -----------------------------
    # FORM 15 PART 3: AC Temp Deviation (>27°C)
    # -----------------------------
    @app.route('/submit_ac_temp_deviation', methods=['POST'])
    @login_required
    def submit_ac_temp_deviation():
        try:
            venues = request.form.getlist('maint_acdev_venue[]')
            natures = request.form.getlist('maint_acdev_nature[]')
            issues = request.form.getlist('maint_acdev_issue[]')
            comments_list = request.form.getlist('maint_acdev_comments[]')

            entries = []

            for i in range(len(venues)):
                venue = venues[i].strip() if venues[i] else ''
                nature = natures[i] if i < len(natures) else ''
                issue = issues[i].strip() if i < len(issues) else ''
                comments = comments_list[i].strip() if i < len(comments_list) else ''

                # Skip empty rows
                if not (venue or nature or issue or comments):
                    continue

                entry = Team2ACTempDeviation(
                    team_id=current_user.team_id,
                    submitted_by=current_user.user_id,
                    particulars='AC Temp deviation if any above 27°C',
                    venue=venue,
                    nature_of_issue=nature,
                    issue_description=issue,
                    comments=comments
                )
                entries.append(entry)

            if entries:
                db.session.add_all(entries)
                db.session.commit()

            return jsonify({'message': 'AC Temp deviation data submitted successfully.'}), 200

        except Exception as e:
            db.session.rollback()
            print("[AC Temp Deviation] Error:", str(e))
            return jsonify({'error': 'Failed to submit AC Temp deviation. Please try again.'}), 500

    # -----------------------------
    # FORM 15 PART 4: Electricity Consumption
    # -----------------------------
    @app.route('/submit_electricity_consumption', methods=['POST'])
    @login_required
    def submit_electricity_consumption():
        try:
            total_units = request.form.get('elec_total_units')
            eb_units = request.form.get('elec_eb_units')
            solar_units = request.form.get('elec_solar_units')
            genset_units = request.form.get('elec_genset_units')
            eb_nature = request.form.get('elec_eb_nature')
            solar_nature = request.form.get('elec_solar_nature')
            genset_nature = request.form.get('elec_genset_nature')
            issue_description = request.form.get('elec_issue')
            comments = request.form.get('elec_comments')

            new_record = Team2ElectricityConsumption(
                team_id=current_user.team_id,
                submitted_by=current_user.user_id,
                category='Electricity',
                total_units=total_units,
                eb=eb_units,
                solar=solar_units,
                genset=genset_units,
                solar_issue=solar_nature,
                genset_issue=genset_nature,
                eb_issue=eb_nature,
                overall_issue_desc=issue_description,
                overall_comments=comments
            )

            db.session.add(new_record)
            db.session.commit()

            return jsonify({'message': 'Electricity consumption submitted successfully.'}), 200

        except Exception as e:
            db.session.rollback()
            print("Error submitting electricity consumption:", str(e))
            return jsonify({'error': 'Failed to submit electricity consumption. Please try again.'}), 500


    # ---------------------------- #
    # Route: Submit EB Details    #
    # Form 15 - Part 4            #
    # ---------------------------- #
    @app.route('/submit_eb_details', methods=['POST'])
    @login_required
    def submit_eb_details():
        try:
            eb_detail = Team2EBDetails(
                team_id=current_user.team_id,
                submitted_by=current_user.user_id,
                category='EB',
                rw_230_240=request.form.get('eb_rw'),
                yw_230_240=request.form.get('eb_yw'),
                bw_230_240=request.form.get('eb_bw'),
                max_demand_104=request.form.get('eb_max_demand'),
                units_per_day=request.form.get('eb_units_day'),
                nature_of_issue=request.form.get('eb_nature'),

            )

            db.session.add(eb_detail)
            db.session.commit()

            return jsonify({'message': 'EB details submitted successfully.'}), 200

        except Exception as e:
            db.session.rollback()
            print("Error submitting EB details:", str(e))
            return jsonify({'error': 'Failed to submit EB details. Please try again.'}), 500


    # ---------------------------- #
    # Route: Submit Solar Details #
    # Form 15 - Part 5            #
    # ---------------------------- #
    @app.route('/submit_solar_details', methods=['POST'])
    @login_required
    def submit_solar_details():
        try:
            capacities = ['20', '40', '60']
            entries = []

            for cap in capacities:
                units = request.form.get(f'solar_{cap}_units')
                remarks = request.form.get(f'solar_{cap}_remarks')
                time = request.form.get(f'solar_{cap}_time')
                max_prod = request.form.get(f'solar_{cap}_maxprod')
                nature = request.form.get(f'solar_{cap}_nature')
                issue = request.form.get(f'solar_{cap}_issue')
                comments = request.form.get(f'solar_{cap}_comments')

                # Skip if all fields are empty
                if not any([units, remarks, time, max_prod, nature, issue, comments]):
                    continue

                entry = Team2SolarDetails(
                    team_id=current_user.team_id,
                    submitted_by=current_user.user_id,
                    category='Solar',
                    capacity=f"{cap} kw",
                    units_per_day=units,
                    remarks=remarks,
                    time=time,
                    max_production=max_prod,
                    nature_of_issue=nature,
                    issue_description=issue,
                    comments=comments
                )
                entries.append(entry)

            if entries:
                db.session.add_all(entries)
                db.session.commit()

            return jsonify({'message': 'Solar details submitted successfully.'}), 200

        except Exception as e:
            db.session.rollback()
            print("Error submitting solar details:", str(e))
            return jsonify({'error': 'Failed to submit solar details. Please try again.'}), 500


    # ------------------------------- #
    # Route: Submit Genset Details   #
    # Form 15 - Part 6               #
    # ------------------------------- #
    @app.route('/submit_genset_details', methods=['POST'])
    @login_required
    def submit_genset_details():
        try:
            genset_detail = Team2GensetDetails(
                team_id=current_user.team_id,
                submitted_by=current_user.user_id,
                category='Genset',
                on_time=request.form.get('genset_on_time'),
                off_time=request.form.get('genset_off_time'),
                battery_voltage=request.form.get('genset_battery_volt'),
                coolant_temp=request.form.get('genset_coolant_temp'),
                nature_of_issue=request.form.get('genset_nature'),
                issue_description=request.form.get('genset_issue'),
                comments=request.form.get('genset_comments')
            )

            db.session.add(genset_detail)
            db.session.commit()

            return jsonify({'message': 'Genset details submitted successfully.'}), 200

        except Exception as e:
            db.session.rollback()
            print("Error submitting genset details:", str(e))
            return jsonify({'error': 'Failed to submit genset details. Please try again.'}), 500

    # ---------------------------------------------------- #
    # 16.a Count Verification Route                        #
    # ---------------------------------------------------- #
    @app.route('/submit_security_count_verification', methods=['POST'])
    @login_required
    def submit_security_count_verification():
        try:
            entries = []

            # Define the two categories and their prefixes
            security_items = [
                ('Walkie Talkie', 'sec_wt'),
                ('Key Note', 'sec_key')
            ]

            for particulars, prefix in security_items:
                total = request.form.get(f'{prefix}_total', '').strip()
                received = request.form.get(f'{prefix}_received', '').strip()
                submitted_val = request.form.get(f'{prefix}_submitted', '').strip()
                nature_of_issue = request.form.get(f'{prefix}_nature', 'All Well').strip()
                issue_description = request.form.get(f'{prefix}_issue', '').strip()
                comments = request.form.get(f'{prefix}_comments', '').strip()

                # ✅ Skip if all key fields are empty
                if any([total, received, submitted_val, issue_description, comments]):
                    entry = Team2CountVerification(
                        team_id=current_user.team_id,
                        submitted_by=current_user.user_id,
                        work_activity='Count Verification',
                        department='Security',
                        category='Security',
                        particulars=particulars,
                        total=total,
                        received=received,
                        submitted=submitted_val,
                        nature_of_issue=nature_of_issue,
                        issue_description=issue_description,
                        comments=comments
                    )
                    entries.append(entry)

            if entries:  # ✅ Only commit if valid rows exist
                db.session.add_all(entries)
                db.session.commit()

            return jsonify({'message': 'Security count verification submitted successfully.'})

        except Exception as e:
            db.session.rollback()
            print("Error submitting security count verification:", str(e))
            return jsonify({'error': 'Failed to submit security count verification. Please try again.'}), 500


    # ---------------------------------------------------- #
    # 16.b Attendance Replacement Submission Route         #
    # ---------------------------------------------------- #
    @app.route('/submit_security_attendance_replacement', methods=['POST'])
    @login_required
    def submit_security_attendance_replacement():
        try:
            security_rows = [
                ('Gate 1 Morning', 'g1m'),
                ('Gate 1 Evening', 'g1e'),
                ('Gate 2 Morning', 'g2m'),
                ('Gate 2 Evening', 'g2e'),
                ('Gate 3 Morning', 'g3m'),
                ('Gate 3 Evening', 'g3e'),
                ('Turn Style Morning', 'bwm'),
                ('Turn Style Evening', 'bwe')
            ]

            entries = []

            for particulars, prefix in security_rows:
                allotted = request.form.get(f"sec_{prefix}_allot", '').strip()
                replaced = request.form.get(f"sec_{prefix}_repl", '').strip()
                nature_of_issue = request.form.get(f"sec_{prefix}_nature", 'All Well').strip()
                issue_description = request.form.get(f"sec_{prefix}_issue", '').strip()
                comments = request.form.get(f"sec_{prefix}_comments", '').strip()

                # ✅ Skip completely empty rows
                if any([allotted, replaced, issue_description, comments]):
                    entry = Team2AttendanceReplacement(
                        team_id=current_user.team_id,
                        submitted_by=current_user.user_id,
                        work_activity='Attendance Replacement',
                        department='Security',
                        particulars=particulars,
                        allotted=allotted,
                        replaced=replaced,
                        nature_of_issue=nature_of_issue,
                        issue_description=issue_description,
                        comments=comments
                    )
                    entries.append(entry)

            if entries:  # ✅ Only commit if there are valid entries
                db.session.add_all(entries)
                db.session.commit()

            return jsonify({'message': 'Security info note submitted successfully.'})

        except Exception as e:
            db.session.rollback()
            print("Error submitting attendance replacement:", str(e))
            return jsonify({'error': 'Failed to submit attendance replacement. Please try again.'}), 500



    # ---------------------------------------------------- #
    # 16.c Security Info Note Submission Route             #
    # ---------------------------------------------------- #
    @app.route('/submit_security_info_note', methods=['POST'])
    @login_required
    def submit_security_info_note():
        try:
            # Extract lists from the form
            departments = request.form.getlist('sec_info_dept[]')
            info_by_list = request.form.getlist('sec_info_by[]')
            information_list = request.form.getlist('sec_info_info[]')
            nature_list = request.form.getlist('sec_info_nature[]')
            issue_list = request.form.getlist('sec_info_issue[]')
            comments_list = request.form.getlist('sec_info_comments[]')

            # Loop through all rows
            for i in range(len(departments)):
                dept = departments[i].strip()
                info_by = info_by_list[i].strip() if i < len(info_by_list) else ''
                information = information_list[i].strip() if i < len(information_list) else ''

                # Skip empty rows (both dept & information are blank)
                if not dept and not information:
                    continue

                record = Team2SecurityInfoNote(
                    team_id=current_user.team_id,
                    submitted_by=current_user.user_id,
                    work_activity='Security Info Note',
                    department=dept,
                    particulars='Security Info Note',
                    info_by=info_by,
                    information=information,
                    nature_of_issue=nature_list[i] if i < len(nature_list) else '',
                    issue_description=issue_list[i] if i < len(issue_list) else '',
                    comments=comments_list[i] if i < len(comments_list) else '',
                )
                db.session.add(record)

            db.session.commit()
            return jsonify({'message': 'Security info note submitted successfully.'})

        except Exception as e:
            db.session.rollback()
            print("Error submitting security info note:", str(e))
            return jsonify({'error': 'Failed to submit security info note. Please try again.'}), 500


    # ---------------------------------------------------- #
    # 16.d Govt In/Out Submission Route                    #
    # ---------------------------------------------------- #
    @app.route('/submit_govt_inout', methods=['POST'])
    @login_required
    def submit_govt_inout():
        try:
            # Get all arrays from the form
            in_times = request.form.getlist('sec_govt_in[]')
            out_times = request.form.getlist('sec_govt_out[]')
            purposes = request.form.getlist('sec_govt_purpose[]')
            natures = request.form.getlist('sec_govt_nature[]')
            issues = request.form.getlist('sec_govt_issue[]')
            comments = request.form.getlist('sec_govt_comments[]')

            for i in range(len(in_times)):
                # Skip empty rows (both in_time and out_time missing)
                if not in_times[i] and not out_times[i]:
                    continue

                record = Team2SecurityGovtInout(
                    team_id=current_user.team_id,
                    submitted_by=current_user.user_id,
                    work_activity='Inward/Outward Govt Officials',
                    department='Security',
                    particulars='Government Officials',
                    in_time=in_times[i],
                    out_time=out_times[i],
                    purpose=purposes[i],
                    nature_of_issue=natures[i],
                    issue_description=issues[i],
                    comments=comments[i],
                )
                db.session.add(record)

            db.session.commit()
            return jsonify({'message': 'Govt in/out submitted successfully.'})

        except Exception as e:
            db.session.rollback()
            print("Error submitting govt in/out:", str(e))
            return jsonify({'error': 'Failed to submit govt in/out. Please try again.'}), 500


    # ---------------------------------------------------- #
    # 16.e Alcohol Test Submission Route                   #
    # ---------------------------------------------------- #
    @app.route('/submit_alcohol_test', methods=['POST'])
    @login_required
    def submit_alcohol_test():
        try:
            # Get all rows from form (arrays)
            names = request.form.getlist('sec_alc_name[]')
            times = request.form.getlist('sec_alc_time[]')
            readings = request.form.getlist('sec_alc_reading[]')
            comments = request.form.getlist('sec_alc_comments[]')

            for i in range(len(names)):
                name = names[i].strip()
                time = times[i].strip()
                reading = readings[i].strip()
                comment = comments[i].strip()

                # Skip empty rows (no name and no time)
                if not name and not time:
                    continue

                record = Team2AlcoholTest(
                    team_id=current_user.team_id,
                    submitted_by=current_user.user_id,
                    work_activity='Alcohol Test',
                    department='Security',
                    name=name,
                    time=time,
                    reading=reading,
                    comments=comment
                )
                db.session.add(record)

            db.session.commit()
            return jsonify({'message': 'Alcohol test submitted successfully.'})

        except Exception as e:
            db.session.rollback()
            print("Error submitting alcohol test:", str(e))
            return jsonify({'error': 'Failed to submit alcohol test. Please try again.'}), 500


    # ---------------------------------------------------- #
    # 16.f Materials Inward Submission Route               #
    # ---------------------------------------------------- #
    @app.route('/submit_security_materials_inward', methods=['POST'])
    @login_required
    def submit_security_materials_inward():
        try:
            # Get all lists from form
            products = request.form.getlist('sec_mat_in_prod[]')
            times = request.form.getlist('sec_mat_in_time[]')
            vendors = request.form.getlist('sec_mat_in_vendor[]')
            descriptions = request.form.getlist('sec_mat_in_desc[]')
            quantities = request.form.getlist('sec_mat_in_qty[]')
            natures = request.form.getlist('sec_mat_in_nature[]')
            issues = request.form.getlist('sec_mat_in_issue[]')
            comments = request.form.getlist('sec_mat_in_comments[]')

            # Iterate through all rows
            for i in range(len(products)):
                # Skip completely empty rows
                if not any([products[i], times[i], vendors[i], descriptions[i], quantities[i], natures[i], issues[i], comments[i]]):
                    continue

                record = Team2SecurityMaterialsInout(
                    team_id=current_user.team_id,
                    submitted_by=current_user.user_id,
                    work_activity='Materials Inward/Outward (Security)',
                    department='Security',
                    product=products[i],
                    in_time=times[i],
                    vendor=vendors[i],
                    description=descriptions[i],
                    quantity=quantities[i],
                    nature_of_issue=natures[i],
                    issue_description=issues[i],
                    comments=comments[i]
                )
                db.session.add(record)

            db.session.commit()
            return jsonify({'message': 'Security materials inward submitted successfully.'})

        except Exception as e:
            db.session.rollback()
            print("Error submitting materials inward:", str(e))
            return jsonify({'error': 'Failed to submit security materials inward. Please try again.'}), 500

    # ---------------------------------------------------- #
    # 16.g Materials Outward Submission Route              #
    # ---------------------------------------------------- #
    @app.route('/submit_security_materials_outward', methods=['POST'])
    @login_required
    def submit_security_materials_outward():
        try:
            # Get lists of all dynamic rows from form
            products = request.form.getlist('sec_mat_out_prod[]')
            times = request.form.getlist('sec_mat_out_time[]')
            vendors = request.form.getlist('sec_mat_out_vendor[]')
            descriptions = request.form.getlist('sec_mat_out_desc[]')
            quantities = request.form.getlist('sec_mat_out_qty[]')
            natures = request.form.getlist('sec_mat_out_nature[]')
            issues = request.form.getlist('sec_mat_out_issue[]')
            comments = request.form.getlist('sec_mat_out_comments[]')

            # Iterate through rows
            for i in range(len(products)):
                # Skip empty rows
                if not (products[i] or vendors[i] or times[i]):
                    continue

                record = Team2SecurityMaterialsOutward(
                    team_id=current_user.team_id,
                    submitted_by=current_user.user_id,
                    work_activity='Materials Outward',
                    department='Security',
                    product=products[i],
                    out_time=times[i],
                    vendor=vendors[i],
                    description=descriptions[i],
                    quantity=int(quantities[i]) if quantities[i] else None,
                    nature_of_issue=natures[i],
                    issue_description=issues[i],
                    comments=comments[i]
                )
                db.session.add(record)

            db.session.commit()
            return jsonify({'message': 'Security materials outward submitted successfully.'})

        except Exception as e:
            db.session.rollback()
            print("Error submitting materials outward:", str(e))
            return jsonify({'error': 'Failed to submit security materials outward. Please try again.'}), 500


    # ---------------------------------------------------- #
    # 16.h Transport Verification Submission Route         #
    # ---------------------------------------------------- #
    @app.route('/submit_transport_verification', methods=['POST'])
    @login_required
    def submit_transport_verification():
        try:
            # Get all data from arrays
            vehicles = request.form.getlist('sec_trans_veh[]')
            damages = request.form.getlist('sec_trans_damage[]')
            escalated_list = request.form.getlist('sec_trans_escalated[]')
            natures = request.form.getlist('sec_trans_nature[]')
            issues = request.form.getlist('sec_trans_issue[]')
            comments_list = request.form.getlist('sec_trans_comments[]')

            # Iterate over all rows
            for i in range(len(vehicles)):
                # Skip empty rows
                if not vehicles[i] and not damages[i] and not escalated_list[i]:
                    continue

                record = Team2TransportVerification(
                    team_id=current_user.team_id,
                    submitted_by=current_user.user_id,
                    work_activity='Transport Verification',
                    department='Security',
                    vehicle_number=vehicles[i],
                    damage_location=damages[i],
                    escalated_to=escalated_list[i],
                    nature_of_issue=natures[i],
                    issue_description=issues[i],
                    comments=comments_list[i],
                )
                db.session.add(record)

            db.session.commit()
            return jsonify({'message': 'Transport verification submitted successfully.'})
        except Exception as e:
            db.session.rollback()
            print("Error submitting transport verification:", str(e))
            return jsonify({'error': 'Failed to submit transport verification. Please try again.'}), 500

    # ------------------------------------------------------------ #
    # 17. Documents Movement Submission Route                      #
    # ------------------------------------------------------------ #
    @app.route('/submit_document_movement', methods=['POST'])
    @login_required
    def submit_document_movement():
        try:
            # Row 1: New File / Document Entry
            doc_new_dept = request.form.get('doc_new_dept_1')
            doc_new_name = request.form.get('doc_new_name_1')
            doc_new_submitby = request.form.get('doc_new_submitby_1')
            doc_new_nature = request.form.get('doc_new_nature_1')
            doc_new_issue = request.form.get('doc_new_issue_1')
            doc_new_comments = request.form.get('doc_new_comments_1')

            # Row 2: Non-Returnable File / Document
            doc_nonret_dept = request.form.get('doc_nonret_dept_1')
            doc_nonret_name = request.form.get('doc_nonret_name_1')
            doc_nonret_issuedto = request.form.get('doc_nonret_issuedto_1')
            doc_nonret_nature = request.form.get('doc_nonret_nature_1')
            doc_nonret_issue = request.form.get('doc_nonret_issue_1')
            doc_nonret_comments = request.form.get('doc_nonret_comments_1')

            # Row 3: Original File / Document Movement
            doc_orig_naturedoc = request.form.get('doc_orig_naturedoc_1')
            doc_orig_issuedto = request.form.get('doc_orig_issuedto_1')
            doc_orig_purpose = request.form.get('doc_orig_purpose_1')
            doc_orig_nature = request.form.get('doc_orig_nature_1')
            doc_orig_issue = request.form.get('doc_orig_issue_1')
            doc_orig_comments = request.form.get('doc_orig_comments_1')

            # Skip saving if all rows are empty
            if not (doc_new_dept or doc_nonret_dept or doc_orig_naturedoc):
                return jsonify({'message': 'No data to save.'})

            # Create and save record
            record = Team2DocumentsMovement(
                team_id=current_user.team_id,
                submitted_by=current_user.user_id,
                work_activity='Documents Movement',
                department='File Room',

                # Row 1
                doc_new_dept=doc_new_dept,
                doc_new_name=doc_new_name,
                doc_new_submitby=doc_new_submitby,
                doc_new_nature=doc_new_nature,
                doc_new_issue=doc_new_issue,
                doc_new_comments=doc_new_comments,

                # Row 2
                doc_nonret_dept=doc_nonret_dept,
                doc_nonret_name=doc_nonret_name,
                doc_nonret_issuedto=doc_nonret_issuedto,
                doc_nonret_nature=doc_nonret_nature,
                doc_nonret_issue=doc_nonret_issue,
                doc_nonret_comments=doc_nonret_comments,

                # Row 3
                doc_orig_naturedoc=doc_orig_naturedoc,
                doc_orig_issuedto=doc_orig_issuedto,
                doc_orig_purpose=doc_orig_purpose,
                doc_orig_nature=doc_orig_nature,
                doc_orig_issue=doc_orig_issue,
                doc_orig_comments=doc_orig_comments,
            )

            db.session.add(record)
            db.session.commit()
            return jsonify({'message': 'Document movement submitted successfully.'})

        except Exception as e:
            db.session.rollback()
            print("Error submitting document movement:", str(e))
            return jsonify({'error': 'Failed to submit document movement. Please try again.'}), 500


    # ------------------------------------------------------------ #
    # 18. Govt Official Documents Submission Route                 #
    # ------------------------------------------------------------ #
    @app.route('/submit_govt_official_documents', methods=['POST'])
    @login_required
    def submit_govt_official_documents():
        try:
            # Extract all rows as lists
            doc_names = request.form.getlist('govtdoc_name[]')
            expiries = request.form.getlist('govtdoc_expiry[]')
            renewals = request.form.getlist('govtdoc_exp_renewal[]')
            natures = request.form.getlist('govtdoc_nature[]')
            issues = request.form.getlist('govtdoc_issue[]')
            comments_list = request.form.getlist('govtdoc_comments[]')

            for i in range(len(doc_names)):
                # Skip empty rows
                if not (doc_names[i] or expiries[i] or renewals[i] or issues[i] or comments_list[i]):
                    continue

                record = Team2GovtOfficialDocuments(
                    team_id=current_user.team_id,
                    submitted_by=current_user.user_id,
                    work_activity='Govt Official Documents',
                    department='PRO',
                    document_name=doc_names[i],
                    expiry_date=expiries[i] or None,
                    expected_renewal_date=renewals[i] or None,
                    nature_of_issue=natures[i],
                    issue_description=issues[i],
                    comments=comments_list[i],
                )
                db.session.add(record)

            db.session.commit()
            return jsonify({'message': 'Govt official documents submitted successfully.'})

        except Exception as e:
            db.session.rollback()
            print("Error submitting govt official documents:", str(e))
            return jsonify({'error': 'Failed to submit govt official documents. Please try again.'}), 500


    # ------------------------------------------------------------ #
    # 19.a Thoorigai Team Social Media                             #
    # ------------------------------------------------------------ #
    @app.route('/submit_thoorigai_social_media', methods=['POST'])
    @login_required
    def submit_thoorigai_social_media():
        try:
            platforms = ['fb', 'ig', 'yt', 'wa']
            platform_map = {
                'fb': 'Facebook',
                'ig': 'Instagram',
                'yt': 'YouTube',
                'wa': 'Whatsapp'
            }

            for p in platforms:
                video_status = request.form.get(f'dm_t_{p}_vid')
                post_status = request.form.get(f'dm_t_{p}_post')
                update_status = request.form.get(f'dm_t_{p}_update')
                nature = request.form.get(f'dm_t_{p}_nature')
                issue = request.form.get(f'dm_t_{p}_issue')
                comments = request.form.get(f'dm_t_{p}_comments')

                # ✅ Skip if all fields are empty
                if not any([video_status, post_status, update_status, nature, issue, comments]):
                    continue

                entry = Team2ThoorigaiTeamSocialMedia(
                    team_id=current_user.team_id,
                    submitted_by=current_user.user_id,
                    platform=platform_map[p],
                    video_status=video_status,
                    post_status=post_status,
                    update_status=update_status,
                    nature_of_issue=nature,
                    issue_description=issue,
                    comments=comments,
                )
                db.session.add(entry)

            db.session.commit()
            return jsonify({'message': 'Thoorigai Social Media details submitted successfully.'})

        except Exception as e:
            db.session.rollback()
            print("Error submitting thoorigai social media:", str(e))
            return jsonify({'error': 'Failed to submit thoorigai social media. Please try again.'}), 500


    # ------------------------------------------------------------ #
    # 19.b Thoorigai Website Updates                               #
    # ------------------------------------------------------------ #
    @app.route('/submit_thoorigai_website_updates', methods=['POST'])
    @login_required
    def submit_thoorigai_website_updates():
        try:
            inclusions = request.form.getlist('dm_t_web_inc[]')
            deletions = request.form.getlist('dm_t_web_del[]')
            others_list = request.form.getlist('dm_t_web_oth[]')
            natures = request.form.getlist('dm_t_web_nature[]')
            issues = request.form.getlist('dm_t_web_issue[]')
            comments_list = request.form.getlist('dm_t_web_comments[]')

            for i in range(len(inclusions)):
                # Skip empty rows (all fields empty)
                if not any([
                    inclusions[i].strip(),
                    deletions[i].strip(),
                    others_list[i].strip(),
                    natures[i].strip(),
                    issues[i].strip(),
                    comments_list[i].strip()
                ]):
                    continue

                record = Team2WebsiteUpdates(
                    team_id=current_user.team_id,
                    submitted_by=current_user.user_id,
                    inclusion=inclusions[i],
                    deletion=deletions[i],
                    others=others_list[i],
                    nature_of_issue=natures[i],
                    issue_description=issues[i],
                    comments=comments_list[i],
                )
                db.session.add(record)

            db.session.commit()
            return jsonify({'message': 'Thoorigai Website Update details submitted successfully.'})

        except Exception as e:
            db.session.rollback()
            print("Error submitting thoorigai website updates:", str(e))
            return jsonify({'error': 'Failed to submit thoorigai website updates. Please try again.'}), 500

    # ------------------------------------------------------------ #
    # 19.c MD Social Media                                         #
    # ------------------------------------------------------------ #
    @app.route('/submit_md_social_media', methods=['POST'])
    @login_required
    def submit_md_social_media():
        try:
            platforms = ['fb', 'ig', 'tw', 'li', 'wa']
            platform_map = {
                'fb': 'Facebook',
                'ig': 'Instagram',
                'tw': 'Twitter',
                'li': 'Linked In',
                'wa': 'Whatsapp'
            }

            for p in platforms:
                video = request.form.get(f'dm_md_{p}_vid')
                post = request.form.get(f'dm_md_{p}_post')
                update = request.form.get(f'dm_md_{p}_update')
                nature = request.form.get(f'dm_md_{p}_nature')
                issue = request.form.get(f'dm_md_{p}_issue')
                comments = request.form.get(f'dm_md_{p}_comments')

                # ✅ Skip row if all fields are empty
                if not any([video, post, update, issue, comments]):
                    continue

                entry = Team2MDSocialMedia(
                    team_id=current_user.team_id,
                    submitted_by=current_user.user_id,
                    platform=platform_map[p],
                    video=video,
                    post=post,
                    update=update,
                    nature_of_issue=nature,
                    issue_description=issue,
                    comments=comments,
                )
                db.session.add(entry)

            db.session.commit()
            return jsonify({'message': 'MD Social Media details submitted successfully.'})

        except Exception as e:
            db.session.rollback()
            print("Error submitting md social media:", str(e))
            return jsonify({'error': 'Failed to submit md social media. Please try again.'}), 500


    # ------------------------------------------------------------ #
    # Submit Intercom Maintenance                                  #
    # ------------------------------------------------------------ #
    @app.route('/submit_intercom_maintenance', methods=['POST'])
    @login_required
    def submit_intercom_maintenance():
        try:
            # Get lists of values from the form (due to [] in input names)
            working_list = request.form.getlist('int_working[]')
            not_working_list = request.form.getlist('int_not_working[]')
            rectified_list = request.form.getlist('int_rectified[]')
            nature_list = request.form.getlist('int_nature[]')
            issue_list = request.form.getlist('int_issue[]')
            comments_list = request.form.getlist('int_comments[]')

            # Loop through each row based on the length of working_list
            for i in range(len(working_list)):
                # Extract values for this row
                working = working_list[i].strip()
                not_working = not_working_list[i].strip()
                rectified = rectified_list[i].strip()
                nature = nature_list[i].strip()
                issue = issue_list[i].strip()
                comments = comments_list[i].strip()

                # Skip empty rows (where all main fields are blank)
                if not (working or not_working or rectified or issue or comments):
                    continue

                # Create new record
                record = Team2IntercomMaintenance(
                    team_id=current_user.team_id,
                    submitted_by=current_user.user_id,
                    working=working,
                    not_working=not_working,
                    rectified=rectified,
                    nature_of_issue=nature,
                    issue_description=issue,
                    comments=comments,
                )

                db.session.add(record)

            db.session.commit()
            return jsonify({'message': 'Intercom Maintenance data submitted successfully.'})

        except Exception as e:
            db.session.rollback()
            print("Error submitting intercom maintenance:", str(e))
            return jsonify({'error': 'Failed to submit intercom maintenance. Please try again.'}), 500

    # ------------------------------------------------------------ #
    # Submit Health Check Up                                       #
    # ------------------------------------------------------------ #
    @app.route('/submit_health_check_up', methods=['POST'])
    @login_required
    def submit_health_check_up():
        try:
            # Get lists of all rows submitted
            depts = request.form.getlist('health_dept[]')
            names = request.form.getlist('health_name[]')
            illnesses = request.form.getlist('health_illness[]')
            informed_bys = request.form.getlist('health_inform[]')
            actions = request.form.getlist('health_action[]')
            natures = request.form.getlist('health_nature[]')
            issues = request.form.getlist('health_issue[]')
            comments_list = request.form.getlist('health_comments[]')

            entries = []

            for i in range(len(names)):
                # Skip empty rows
                if not any([
                    depts[i], names[i], illnesses[i],
                    informed_bys[i], actions[i],
                    issues[i], comments_list[i]
                ]):
                    continue

                entry = Team2HealthCheckUp(
                    team_id=current_user.team_id,
                    submitted_by=current_user.user_id,
                    department_staff=depts[i],
                    staff_name=names[i],
                    illness=illnesses[i],
                    informed_by=informed_bys[i],
                    action_taken=actions[i],
                    nature_of_issue=natures[i],
                    issue_description=issues[i],
                    comments=comments_list[i],
                )
                entries.append(entry)

            if entries:
                db.session.add_all(entries)
                db.session.commit()

            return jsonify({'message': 'Health Check Up data submitted successfully.'})

        except Exception as e:
            db.session.rollback()
            print("Error submitting health check up:", str(e))
            return jsonify({'error': 'Failed to submit health check up. Please try again.'}), 500


    # =========================================================
    # SECTION 22: Net Connectivity & Print Details Submission
    # =========================================================
    @app.route('/submit_net_connectivity', methods=['POST'])
    @login_required
    def submit_net_connectivity():
        try:
            entries = []

            # Get all row data as lists
            net_speeds = request.form.getlist('net_speed[]')
            no_of_prints_list = request.form.getlist('net_prints[]')
            comp_venues = request.form.getlist('net_comp_venue[]')
            comp_issues = request.form.getlist('net_comp_issue[]')
            work_issues = request.form.getlist('net_work_issue[]')
            natures = request.form.getlist('net_nature[]')
            issue_descs = request.form.getlist('net_issue_desc[]')
            comments_list = request.form.getlist('net_comments[]')

            for i in range(len(net_speeds)):
                net_speed = net_speeds[i].strip() if net_speeds[i] else ''
                no_of_prints = no_of_prints_list[i].strip() if no_of_prints_list[i] else ''
                comp_venue = comp_venues[i].strip() if comp_venues[i] else ''
                comp_issue = comp_issues[i].strip() if comp_issues[i] else ''
                work_issue = work_issues[i].strip() if work_issues[i] else ''
                nature = natures[i] if natures[i] else ''
                issue_desc = issue_descs[i].strip() if issue_descs[i] else ''
                comments = comments_list[i].strip() if comments_list[i] else ''

                # Skip completely empty rows
                if not (net_speed or no_of_prints or comp_venue or comp_issue or work_issue or issue_desc or comments):
                    continue

                complaints_combined = f"Venue: {comp_venue}\nIssue: {comp_issue}\nWork/Issue: {work_issue}"

                entry = Team2NetConnectivityPrintDetails(
                    team_id=current_user.team_id,
                    submitted_by=current_user.user_id,
                    net_speed=net_speed,
                    no_of_prints=int(no_of_prints) if no_of_prints.isdigit() else None,
                    complaints=complaints_combined,
                    nature_of_issue=nature,
                    issue_description=issue_desc,
                    comments=comments
                )

                entries.append(entry)

            if entries:
                db.session.add_all(entries)
                db.session.commit()

            return jsonify({'message': 'Net Connectivity & Print Details submitted successfully.'})

        except Exception as e:
            db.session.rollback()
            print(f"[Net Connectivity] Error: {str(e)}")
            return jsonify({'error': 'Failed to submit net connectivity & print details.'}), 500


    # =====================================================
    # SECTION 23: General Maintenance – IT Products
    # =====================================================
    @app.route('/submit_it_maintenance', methods=['POST'])
    @login_required
    def submit_it_maintenance():
        try:
            # Get lists of all form inputs
            issues_list = request.form.getlist('it_maint_issue[]')
            complaint_dt_list = request.form.getlist('it_maint_comp_dt[]')
            solved_dt_list = request.form.getlist('it_maint_solv_dt[]')
            nature_list = request.form.getlist('it_maint_nature[]')
            issue_desc_list = request.form.getlist('it_maint_issue_desc[]')
            comments_list = request.form.getlist('it_maint_comments[]')

            entries = []
            for i in range(len(issues_list)):
                issue = issues_list[i].strip() if issues_list[i] else ''
                complaint_dt = complaint_dt_list[i].strip() if complaint_dt_list[i] else ''
                solved_dt = solved_dt_list[i].strip() if solved_dt_list[i] else ''
                nature = nature_list[i].strip() if nature_list[i] else ''
                issue_desc = issue_desc_list[i].strip() if issue_desc_list[i] else ''
                comments = comments_list[i].strip() if comments_list[i] else ''

                # Skip completely empty rows
                if not any([issue, complaint_dt, solved_dt, nature, issue_desc, comments]):
                    continue

                entry = Team2GeneralMaintenanceITProducts(
                    team_id=current_user.team_id,
                    submitted_by=current_user.user_id,
                    issues=issue,
                    complaintdate=complaint_dt or None,
                    solveddate=solved_dt or None,
                    nature_of_issue=nature,
                    issue_description=issue_desc,
                    comments=comments
                )
                entries.append(entry)

            # Commit only if there are valid entries
            if entries:
                db.session.add_all(entries)
                db.session.commit()

            return jsonify({'message': 'General Maintenance – IT Products submitted successfully.'})

        except Exception as e:
            db.session.rollback()
            print(f"[IT Maintenance] Error: {str(e)}")
            return jsonify({'error': 'Failed to submit general maintenance – IT products.'}), 500


    # =====================================================
    # SECTION 24: Calendar Schedule Submission
    # =====================================================
    @app.route('/submit_calendar_schedule', methods=['POST'])
    @login_required
    def submit_calendar_schedule():
        try:
            department_prefixes = {
                'Admin': 'admin',
                'House Keeping': 'hk',
                'Security': 'sec',
                'Transport': 'trans'
            }

            entries = []

            for dept, prefix in department_prefixes.items():
                activity = request.form.get(f'cal_{prefix}_activity', '').strip()
                category = request.form.get(f'cal_{prefix}_category', '').strip()
                in_charge = request.form.get(f'cal_{prefix}_incharge', '').strip()
                planned = request.form.get(f'cal_{prefix}_planned', '').strip()
                unplanned = request.form.get(f'cal_{prefix}_unplanned', '').strip()
                nature = request.form.get(f'cal_{prefix}_nature', '').strip()
                issue_desc = request.form.get(f'cal_{prefix}_issue', '').strip()
                comments = request.form.get(f'cal_{prefix}_comments', '').strip()

                # Skip the section if all fields are empty
                if not any([activity, category, in_charge, planned, unplanned, nature, issue_desc, comments]):
                    continue

                entries.append(
                    Team2CalendarSchedule(
                        team_id=current_user.team_id,
                        submitted_by=current_user.user_id,
                        department=dept,
                        session=activity,
                        category=category,
                        in_charge=in_charge,
                        planned=planned,
                        unplanned=unplanned,
                        nature_of_issue=nature,
                        issue_description=issue_desc,
                        comments=comments
                    )
                )

            if entries:
                db.session.add_all(entries)
                db.session.commit()

            return jsonify({'message': 'Calendar Schedule details submitted successfully.'})

        except Exception as e:
            db.session.rollback()
            print(f"[Calendar Schedule] Error: {str(e)}")
            return jsonify({'error': 'Failed to submit calendar schedule.'}), 500

    # =====================================================
    # SECTION 25: Training Attendance Submission
    # =====================================================
    @app.route('/submit_training_attendance', methods=['POST'])
    @login_required
    def submit_training_attendance():
        try:
            # Debug: Print received form data
            print(f"[Training Attendance] Received form data: {dict(request.form)}")

            rows = [
                ('trn_att_acad_jr', 'Academics', 'Academics - Jr.School'),
                ('trn_att_acad_sr', 'Academics', 'Academics - Sr.School'),
                ('trn_att_admin_adm', 'Admin', 'Admin - Admin'),
                ('trn_att_admin_dri', 'Admin', 'Admin - Drivers'),
                ('trn_att_admin_sec', 'Admin', 'Admin - Securities'),
                ('trn_att_admin_dri2', 'Admin', 'Admin - Drivers (Sub)'),
                ('trn_att_admin_con', 'Admin', 'Admin - Conductors'),
            ]

            entries = []

            for prefix, dept_group, dept in rows:
                topic = request.form.get(f'{prefix}_topic', '').strip()
                total = request.form.get(f'{prefix}_total', '').strip()
                present = request.form.get(f'{prefix}_present', '').strip()
                leave = request.form.get(f'{prefix}_leave', '').strip()
                leave_perc = request.form.get(f'{prefix}_leave_perc', '').strip()
                nature = request.form.get(f'{prefix}_nature', '').strip()
                issue = request.form.get(f'{prefix}_issue', '').strip()
                comments = request.form.get(f'{prefix}_comments', '').strip()

                # Skip row if all fields are empty
                if not any([topic, total, present, leave, leave_perc, nature, issue, comments]):
                    continue

                # Convert numeric fields safely
                total_int = int(total) if total.isdigit() else None
                present_int = int(present) if present.isdigit() else None
                leave_int = int(leave) if leave.isdigit() else None

                # Calculate leave and leave percentage if not provided but calculable
                if total_int and present_int and total_int >= present_int:
                    calculated_leave = total_int - present_int
                    if not leave_int:
                        leave_int = calculated_leave
                    if not leave_perc:
                        leave_perc = f"{(calculated_leave / total_int) * 100:.1f}%"
                elif total_int and leave_int and total_int > 0:
                    # If leave is manually entered, calculate percentage
                    if not leave_perc:
                        leave_perc = f"{(leave_int / total_int) * 100:.1f}%"

                entries.append(
                    Team2TrainingAttendance(
                        team_id=current_user.team_id,
                        submitted_by=current_user.user_id,
                        work_activity='Training Attendance',
                        department_group=dept_group,
                        dept=dept,
                        topic=topic,
                        total=total_int,
                        present=present_int,
                        leave=leave_int,
                        leave_percentage=leave_perc,
                        nature_of_issue=nature,
                        issue_description=issue,
                        comments=comments
                    )
                )

            if entries:
                db.session.add_all(entries)
                db.session.commit()

            return jsonify({'message': 'Training Attendance details submitted successfully.'})

        except Exception as e:
            db.session.rollback()
            print(f"[Training Attendance] Error: {str(e)}")
            return jsonify({'error': 'Failed to submit training attendance.'}), 500

    # =====================================================
    # SECTION 26: Training Details Submission
    # =====================================================
    @app.route('/submit_training_details', methods=['POST'])
    @login_required
    def submit_training_details():
        try:
            names = request.form.getlist('trn_det_person[]')
            depts = request.form.getlist('trn_det_dept[]')
            topics = request.form.getlist('trn_det_topic[]')
            durations = request.form.getlist('trn_det_duration[]')
            natures = request.form.getlist('trn_det_nature[]')
            issues = request.form.getlist('trn_det_issue[]')
            comments_list = request.form.getlist('trn_det_comments[]')

            entries = []

            for i in range(len(names)):
                name = names[i].strip()
                dept = depts[i].strip() if i < len(depts) else ''
                topic = topics[i].strip() if i < len(topics) else ''
                duration = durations[i].strip() if i < len(durations) else ''
                nature = natures[i].strip() if i < len(natures) else ''
                issue = issues[i].strip() if i < len(issues) else ''
                comments = comments_list[i].strip() if i < len(comments_list) else ''

                # Skip empty rows (only name and topic are mandatory for considering a row)
                if not name and not topic:
                    continue

                entry = Team2TrainingDetails(
                    team_id=current_user.team_id,
                    submitted_by=current_user.user_id,
                    name=name,
                    dept=dept,
                    topic=topic,
                    no_of_days_hrs=int(duration) if duration.isdigit() else None,
                    nature_of_issue=nature,
                    issue_description=issue,
                    comments=comments
                )
                entries.append(entry)

            if entries:
                db.session.add_all(entries)
                db.session.commit()

            return jsonify({'message': 'Training details submitted successfully!'})

        except Exception as e:
            db.session.rollback()
            print(f"[Training Details] Error: {str(e)}")
            return jsonify({'error': 'Failed to submit training details.'}), 500


    # =====================================================
    # SECTION 27: Manpower Planning Submission
    # =====================================================
    @app.route('/submit_manpower_planning', methods=['POST'])
    @login_required
    def submit_manpower_planning():
        try:
            # Get all rows from the form
            departments = request.form.getlist('mp_department[]')
            staff_names = request.form.getlist('mp_staff_name[]')
            designations = request.form.getlist('mp_designation[]')
            grades = request.form.getlist('mp_grades[]')
            relieve_dates = request.form.getlist('mp_relieve_date[]')
            budgets = request.form.getlist('mp_budget[]')
            new_finds = request.form.getlist('mp_new_find[]')

            for idx in range(len(departments)):
                if not any([departments[idx], staff_names[idx], designations[idx]]):
                    # Skip completely empty rows
                    continue

                row = Team2ManpowerPlanning(
                    team_id=current_user.team_id,
                    submitted_by=current_user.user_id,
                    mp_department=departments[idx],
                    mp_staff_name=staff_names[idx],
                    mp_designation=designations[idx],
                    mp_grades=grades[idx],
                    mp_relieve_date=relieve_dates[idx] if relieve_dates[idx] else None,
                    mp_budget=float(budgets[idx]) if budgets[idx] else None,
                    mp_new_find=new_finds[idx]
                )
                db.session.add(row)

            db.session.commit()
            return jsonify({'message': 'Manpower planning data submitted successfully!'})

        except Exception as e:
            db.session.rollback()
            print("Error submitting manpower planning data:", str(e))
            return jsonify({'error': 'Failed to submit manpower planning data. Please try again.'}), 500

    # =====================================================
    # SECTION 28: Overall Consolidation Submission
    # =====================================================

    @app.route('/submit_overall_consolidation', methods=['POST'])
    @login_required
    def submit_overall_consolidation():
        try:
            departments = request.form.getlist('oc_department[]')
            totals = request.form.getlist('oc_total[]')
            requireds = request.form.getlist('oc_required[]')
            shortlisted = request.form.getlist('oc_shortlisted[]')
            waiting_lists = request.form.getlist('oc_waiting_list[]')
            yet_to_finds = request.form.getlist('oc_yet_to_find[]')

            for i in range(len(departments)):
                # Skip rows where no department is selected
                if not departments[i]:
                    continue

                consolidation_entry = Team2OverallConsolidation(
                    team_id=current_user.team_id,
                    submitted_by=current_user.user_id,
                    oc_department=departments[i],
                    oc_total=int(totals[i]) if totals[i] else None,
                    oc_required=int(requireds[i]) if requireds[i] else None,
                    oc_shortlisted=int(shortlisted[i]) if shortlisted[i] else None,
                    oc_waiting_list=int(waiting_lists[i]) if waiting_lists[i] else None,
                    oc_yet_to_find=int(yet_to_finds[i]) if yet_to_finds[i] else None
                )
                db.session.add(consolidation_entry)

            db.session.commit()
            return jsonify({'message': 'Overall Consolidation data submitted successfully!'})
        except Exception as e:
            db.session.rollback()
            print(f'Error submitting overall consolidation: {str(e)}')
            return jsonify({'error': 'Failed to submit overall consolidation.'}), 500

        # =====================================================
    # SECTION XX: Uniform Details Submission
    # =====================================================

    @app.route('/submit_uniform_details', methods=['POST'])
    @login_required
    def submit_uniform_details():
        try:
            uniforms = request.form.getlist('ud_uniform[]')
            designations = request.form.getlist('ud_designation[]')
            details_list = request.form.getlist('ud_details[]')
            remarks_list = request.form.getlist('ud_remarks[]')
            closure_dates = request.form.getlist('ud_closure_date[]')

            for i in range(len(uniforms)):
                # Skip rows without uniform name
                if not uniforms[i]:
                    continue

                closure_date = None
                if closure_dates[i]:
                    try:
                        closure_date = datetime.strptime(closure_dates[i], '%Y-%m-%d').date()
                    except ValueError:
                        closure_date = None  # Or handle invalid date format differently

                uniform_entry = Team2UniformDetails(
                    team_id=current_user.team_id,
                    submitted_by=current_user.user_id,
                    ud_uniform=uniforms[i],
                    ud_designation=designations[i],
                    ud_details=details_list[i],
                    ud_remarks=remarks_list[i],
                    ud_closure_date=closure_date
                )
                db.session.add(uniform_entry)

            db.session.commit()
            return jsonify({'message': 'Uniform Details submitted successfully!'})
        except Exception as e:
            db.session.rollback()
            print(f'Error submitting uniform details: {str(e)}')
            return jsonify({'error': 'Failed to submit uniform details.'}), 500


    # =====================================================
    # SECTION XX: Department Wise Uniform Details Submission
    # =====================================================

    @app.route('/submit_department_wise_uniform_details', methods=['POST'])
    @login_required
    def submit_department_wise_uniform_details():
        try:
            departments = request.form.getlist('dwud_department[]')
            totals = request.form.getlist('dwud_total[]')
            completeds = request.form.getlist('dwud_completed[]')
            pendings = request.form.getlist('dwud_pending[]')
            names_list = request.form.getlist('dwud_names[]')
            dress_codes = request.form.getlist('dwud_dress_code[]')
            statuses = request.form.getlist('dwud_status[]')

            for i in range(len(departments)):
                # Skip rows without department name
                if not departments[i]:
                    continue

                dept_uniform_entry = Team2DepartmentWiseUniformDetails(
                    team_id=current_user.team_id,
                    submitted_by=current_user.user_id,
                    dwud_department=departments[i],
                    dwud_total=int(totals[i]) if totals[i] else None,
                    dwud_completed=int(completeds[i]) if completeds[i] else None,
                    dwud_pending=int(pendings[i]) if pendings[i] else None,
                    dwud_names=names_list[i],
                    dwud_dress_code=dress_codes[i],
                    dwud_status=statuses[i]
                )
                db.session.add(dept_uniform_entry)

            db.session.commit()
            return jsonify({'message': 'Department Wise Uniform Details submitted successfully!'})
        except Exception as e:
            db.session.rollback()
            print(f'Error submitting department wise uniform details: {str(e)}')
            return jsonify({'error': 'Failed to submit department wise uniform details.'}), 500


    # =====================================================
    #  Team 3 Audit Submission
    # =====================================================

