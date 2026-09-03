from datetime import datetime, timedelta
from collections import defaultdict
from extensions import db
from models import (
    Team, Team2HRAttendance, Team2TotalHRAttendance, Team2AdminAttendance,
    Team2RecruitmentActivity, Team2PendingRecruitment, Team2RecruitmentPipeline,
    Team2StaffStatusUpdates, Team2SalaryPending, Team2PoliceVerification,
    Team2InterviewSchedule, Team2ExitInformation, Team2IssuesStaffConcerns,
    Team2KuralRecitation, Team2FrontOfficePhoneCalls, Team2VisitorLog,
    Team2BSNLPhoneStatus, Team2MaterialsInward, Team2MaterialsOutward,
    Team2MaterialsMovement, Team2ReturnableMaterialTracking, Team2ReturnableGoodsReport,
    Team2CampusCameraStatus, Team2VehicleCameraStatus, Team2BusACCameraStatus,
    Team2GPSMonitoring, Team2IssuesIdentifiedMonitoring, Team2IssuesIdentifiedControlRoom,
    Team2CameraFootageEntry, Team2BiometricsAccessCardPunching, Team2WaterTDSDeviation,
    Team2TestingCleaning, Team2PoolTesting, Team2WashroomCleanliness,
    Team2TransportAttendance, Team2ACWorkingStatus, Team2LateReporting,
    Team2MaintenanceServiceIssues, Team2CarMaintenanceCleaning,
    Team2VehicleRenewalsDelays, Team2SpecialTrip, Team2ParentConcernDetail,
    Team2ACTemperatureCheck, Team2LaborEbSolarGenset, Team2Motor, Team2PestControl,
    Team2ACTempDeviation, Team2ElectricityConsumption, Team2EBDetails,
    Team2SolarDetails, Team2GensetDetails, Team2CountVerification,
    Team2AttendanceReplacement, Team2SecurityInfoNote, Team2SecurityGovtInout,
    Team2AlcoholTest, Team2SecurityMaterialsInout, Team2SecurityMaterialsOutward,
    Team2TransportVerification, Team2DocumentsMovement, Team2GovtOfficialDocuments,
    Team2ThoorigaiTeamSocialMedia, Team2WebsiteUpdates, Team2MDSocialMedia,
    Team2IntercomMaintenance, Team2HealthCheckUp, Team2NetConnectivityPrintDetails,
    Team2GeneralMaintenanceITProducts, Team2CalendarSchedule, Team2TrainingAttendance,
    Team2TrainingDetails, Team2ManpowerPlanning, Team2OverallConsolidation,
    Team2WaterLevel, Team2HousekeepingGeneral, Team2UniformDetails,
    Team2DepartmentWiseUniformDetails
)

def get_team2_data(selected_date_obj, start_of_day, end_of_day, show_all_dates):
    team2_hr_attendance_data = []
    team2_total_hr_attendance_data = []
    team2_admin_attendance_data = []
    team2_recruitment_activity_data = []
    team2_pending_recruitment_data = []
    team2_recruitment_pipeline_data = []
    team2_staff_status_updates_data = []
    team2_salary_pending_data = []
    team2_police_verification_data = []
    team2_interview_schedule_data = []
    team2_exit_information_data = []
    team2_issues_staff_concerns_data = []
    team2_kural_recitation_data = []
    team2_front_office_phone_calls_data = []
    team2_visitor_log_data = []
    team2_bsnl_phone_status_data = []
    team2_materials_inward_data = []
    team2_materials_outward_data = []
    team2_materials_movement_data = []
    team2_returnable_material_tracking_data = []
    team2_returnable_goods_report_data = []
    team2_campus_camera_status_data = []
    team2_vehicle_camera_status_data = []
    team2_bus_ac_camera_status_data = []
    team2_gps_monitoring_data = []
    team2_issues_identified_monitoring_data = []
    team2_teachers_late_reporting_data = []
    team2_water_tds_deviation_data = []
    team2_testing_cleaning_data = []
    team2_water_level_data = []
    team2_housekeeping_general_data = []
    team2_pool_testing_data = []
    team2_washroom_cleanliness_data = []
    team2_transport_attendance_data = []
    team2_ac_working_status_data = []
    team2_late_reporting_data = []
    team2_maintenance_service_issues_data = []
    team2_car_maintenance_cleaning_data = []
    team2_vehicle_renewals_delays_data = []
    team2_special_trip_data = []
    team2_parent_concern_detail_data = []
    team2_ac_temperature_data = []
    team2_maintenance_labor_data = []
    team2_motor_data = []
    team2_pest_control_data = []
    team2_ac_temp_deviation_data = []
    team2_electricity_consumption_data = []
    team2_eb_details_data = []
    team2_solar_details_data = []
    team2_genset_details_data = []
    team2_count_verification_data = []
    team2_attendance_replacement_data = []
    team2_security_info_note_data = []
    team2_security_govt_inout_data = []
    team2_alcohol_test_data = []
    team2_security_materials_inward_data = []
    team2_security_materials_outward_data = []
    team2_transport_verification_data = []
    team2_documents_movement_data = []
    team2_govt_official_documents_data = []
    team2_thoorigai_social_media_data = []
    team2_website_updates_data = []
    team2_md_social_media_data = []
    team2_intercom_maintenance_data = []
    team2_health_check_up_data = []
    team2_net_connectivity_print_details_data = []
    team2_general_maintenance_it_data = []
    team2_calendar_schedule_data = []
    team2_training_attendance_data = []
    team2_training_details_data = []
    team2_camera_footage_data = []
    team2_manpower_planning_data = []
    team2_overall_consolidation_data = []
    team2_uniform_details_data = []
    team2_dept_wise_uniform_details_data = []
    team2_biometrics_access_card_punching_data = []

    team2 = Team.query.filter_by(team_name='Team 2').first()
    if team2:
        # Get Team 2 HR Attendance data with proper date filtering
        query = Team2HRAttendance.query.filter(Team2HRAttendance.team_id == team2.team_id)

        if not show_all_dates:

            query = query.filter(

                Team2HRAttendance.submitted_at >= start_of_day,

                Team2HRAttendance.submitted_at <= end_of_day

            )

        hr_data = query.order_by(Team2HRAttendance.submitted_at.desc()).all()
        team2_hr_attendance_data = [{
            'date': item.submitted_at,
            'jr_school': {
                'total': item.hr_att_jr_school_total,
                'present': item.hr_att_jr_school_present,
                'leave': item.hr_att_jr_school_leave,
                'leave_perc': item.hr_att_jr_school_leave_perc,
                'nature': item.hr_att_jr_school_nature,
                'issue_desc': item.hr_att_jr_school_issue_desc,
                'comments': item.hr_att_jr_school_comments
            },
            'sr_school': {
                'total': item.hr_att_sr_school_total,
                'present': item.hr_att_sr_school_present,
                'leave': item.hr_att_sr_school_leave,
                'leave_perc': item.hr_att_sr_school_leave_perc,
                'nature': item.hr_att_sr_school_nature,
                'issue_desc': item.hr_att_sr_school_issue_desc,
                'comments': item.hr_att_sr_school_comments
            },
            'eca': {
                'total': item.hr_att_eca_total,
                'present': item.hr_att_eca_present,
                'leave': item.hr_att_eca_leave,
                'leave_perc': item.hr_att_eca_leave_perc,
                'nature': item.hr_att_eca_nature,
                'issue_desc': item.hr_att_eca_issue_desc,
                'comments': item.hr_att_eca_comments
            },
            'overall': {
                'total': item.hr_att_acad_overall_total,
                'present': item.hr_att_acad_overall_present,
                'leave': item.hr_att_acad_overall_leave,
                'leave_perc': item.hr_att_acad_overall_leave_perc
            }
        } for item in hr_data]

        # Get Team 2 Total HR Attendance data
        query = Team2TotalHRAttendance.query.filter(Team2TotalHRAttendance.team_id == team2.team_id)

        if not show_all_dates:

            query = query.filter(

                Team2TotalHRAttendance.submitted_at >= start_of_day,

                Team2TotalHRAttendance.submitted_at <= end_of_day

            )

        total_hr_data = query.order_by(Team2TotalHRAttendance.submitted_at.desc()).all()
        team2_total_hr_attendance_data = [{
            'date': item.submitted_at,
            'category': item.category,
            'total': item.total,
            'present': item.present,
            'leave': item.leave,
            'leave_perc': item.leave_perc,
            'nature': item.nature_of_issue,
            'issue_desc': item.issue_description,
            'comments': item.comments
        } for item in total_hr_data]
        
        # Query filtered by team ID and exact date (with datetime range for index use)
        query = Team2AdminAttendance.query.filter(Team2AdminAttendance.team_id == team2.team_id)

        if not show_all_dates:

            query = query.filter(

                Team2AdminAttendance.submitted_at >= start_of_day,

                Team2AdminAttendance.submitted_at <= end_of_day

            )

        admin_data = query.order_by(Team2AdminAttendance.submitted_at.desc()).all()

        # Build structured data (without submitter)
        team2_admin_attendance_data = [{
            'date': item.submitted_at,
            'admin_staff': {
                'total': item.hr_att_admin_total,
                'present': item.hr_att_admin_present,
                'leave': item.hr_att_admin_leave,
                'leave_perc': item.hr_att_admin_leave_perc,
                'nature': item.hr_att_admin_nature,
                'issue_desc': item.hr_att_admin_issue_desc,
                'comments': item.hr_att_admin_comments
            },
            'drivers': {
                'total': item.hr_att_drivers_total,
                'present': item.hr_att_drivers_present,
                'leave': item.hr_att_drivers_leave,
                'leave_perc': item.hr_att_drivers_leave_perc,
                'nature': item.hr_att_drivers_nature,
                'issue_desc': item.hr_att_drivers_issue_desc,
                'comments': item.hr_att_drivers_comments
            },
            'security': {
                'total': item.hr_att_sec_total,
                'present': item.hr_att_sec_present,
                'leave': item.hr_att_sec_leave,
                'leave_perc': item.hr_att_sec_leave_perc,
                'nature': item.hr_att_sec_nature,
                'issue_desc': item.hr_att_sec_issue_desc,
                'comments': item.hr_att_sec_comments
            },
            'housekeeping': {
                'total': item.hr_att_hk_total,
                'present': item.hr_att_hk_present,
                'leave': item.hr_att_hk_leave,
                'leave_perc': item.hr_att_hk_leave_perc,
                'nature': item.hr_att_hk_nature,
                'issue_desc': item.hr_att_hk_issue_desc,
                'comments': item.hr_att_hk_comments
            },
            'conductors': {
                'total': item.hr_att_cond_total,
                'present': item.hr_att_cond_present,
                'leave': item.hr_att_cond_leave,
                'leave_perc': item.hr_att_cond_leave_perc,
                'nature': item.hr_att_cond_nature,
                'issue_desc': item.hr_att_cond_issue_desc,
                'comments': item.hr_att_cond_comments
            },
            'overall': {
                'total': item.hr_att_admin_overall_total,
                'present': item.hr_att_admin_overall_present,
                'leave': item.hr_att_admin_overall_leave,
                'leave_perc': item.hr_att_admin_overall_leave_perc
            }
        } for item in admin_data]
        
        # Get Team 2 Recruitment Activity data with proper date filtering
        query = Team2RecruitmentActivity.query.filter(Team2RecruitmentActivity.team_id == team2.team_id)

        if not show_all_dates:

            query = query.filter(

                Team2RecruitmentActivity.submitted_at >= start_of_day,

                Team2RecruitmentActivity.submitted_at <= end_of_day

            )

        recruitment_data = query.order_by(Team2RecruitmentActivity.submitted_at.desc()).all()

        team2_recruitment_activity_data = [{
            'date': item.submitted_at,
            'academic': {
                'vacancies': item.rec_act_acad_vac_nos,
                'positions': item.rec_act_acad_pos,
                'update_text': item.rec_act_acad_update,
                'nature': item.rec_act_acad_nature,
                'issue_desc': item.rec_act_acad_issue_desc,
                'comments': item.rec_act_acad_comments
            },
            'admin': {
                'vacancies': item.rec_act_admin_vac_nos,
                'positions': item.rec_act_admin_pos,
                'update_text': item.rec_act_admin_update,
                'nature': item.rec_act_admin_nature,
                'issue_desc': item.rec_act_admin_issue_desc,
                'comments': item.rec_act_admin_comments
            }
        } for item in recruitment_data]
        
        # Get Team 2 Pending Recruitment data with proper date filtering
        query = Team2PendingRecruitment.query.filter(Team2PendingRecruitment.team_id == team2.team_id)

        if not show_all_dates:

            query = query.filter(

                Team2PendingRecruitment.submitted_at >= start_of_day,

                Team2PendingRecruitment.submitted_at <= end_of_day

            )

        pending_data = query.order_by(Team2PendingRecruitment.submitted_at.desc()).all()

        team2_pending_recruitment_data = [{
            'date': item.submitted_at,
            'academic': {
                'count': item.rec_pend_acad_count,
                'positions': item.rec_pend_acad_pos,
                'closure_date': item.rec_pend_acad_closure,
                'nature': item.rec_pend_acad_nature,
                'issue_desc': item.rec_pend_acad_issue_desc,
                'comments': item.rec_pend_acad_comments
            },
            'admin': {
                'count': item.rec_pend_admin_count,
                'positions': item.rec_pend_admin_pos,
                'closure_date': item.rec_pend_admin_closure,
                'nature': item.rec_pend_admin_nature,
                'issue_desc': item.rec_pend_admin_issue_desc,
                'comments': item.rec_pend_admin_comments
            }
        } for item in pending_data]
        
        # Get Team 2 Recruitment Pipeline data (new schema: one row per position)
        query = Team2RecruitmentPipeline.query.filter(Team2RecruitmentPipeline.team_id == team2.team_id)
        if not show_all_dates:
            query = query.filter(
                Team2RecruitmentPipeline.submitted_at >= start_of_day,
                Team2RecruitmentPipeline.submitted_at <= end_of_day
            )
        pipeline_rows = query.order_by(Team2RecruitmentPipeline.submitted_at.desc()).all()

        # Group rows by submitted date (day) into academic/non-academic buckets
        grouped_pipeline = {}
        for row in pipeline_rows:
            date_key = row.submitted_at.date() if hasattr(row.submitted_at, 'date') else row.submitted_at
            if date_key not in grouped_pipeline:
                grouped_pipeline[date_key] = {
                    'date': date_key,
                    'academic': [],
                    'non_academic': []
                }

            entry = {
                'position': row.position,
                'hired': row.hired,
                'shortlisted': row.shortlisted
            }

            category_value = (row.category or '').lower()
            if category_value.startswith('non'):
                grouped_pipeline[date_key]['non_academic'].append(entry)
            else:
                grouped_pipeline[date_key]['academic'].append(entry)

        # Sort by date descending
        team2_recruitment_pipeline_data = sorted(grouped_pipeline.values(), key=lambda x: x['date'], reverse=True)

        # Get Team 2 Staff Status Updates data
        query = Team2StaffStatusUpdates.query.filter(Team2StaffStatusUpdates.team_id == team2.team_id)

        if not show_all_dates:

            query = query.filter(

                Team2StaffStatusUpdates.submitted_at >= start_of_day,

                Team2StaffStatusUpdates.submitted_at <= end_of_day

            )

        staff_status_updates_data = query.order_by(Team2StaffStatusUpdates.submitted_at.desc()).all()

        team2_staff_status_updates_data = [{
            'date': item.submitted_at,
            'obs_name': item.obs_name,
            'obs_dept': item.obs_dept,  
            'obs_desig': item.obs_desig,
            'obs_doj': item.obs_doj,
            'obs_shadow': item.obs_shadow,
            'obs_completed': item.obs_completed,
            'obs_comments': item.obs_comments,
        } for item in staff_status_updates_data] 
        
        # Get Team 2 Salary Pending data
        query = Team2SalaryPending.query.filter(Team2SalaryPending.team_id == team2.team_id)

        if not show_all_dates:

            query = query.filter(

                Team2SalaryPending.submitted_at >= start_of_day,

                Team2SalaryPending.submitted_at <= end_of_day

            )

        salary_pending_data = query.order_by(Team2SalaryPending.submitted_at.desc()).all()

        team2_salary_pending_data = [{
            'date': item.submitted_at,
            'sal_pend_name': item.sal_pend_name,
            'sal_pend_dept': item.sal_pend_dept,
            'sal_pend_desig': item.sal_pend_desig,
            'sal_pend_comments': item.sal_pend_comments
        } for item in salary_pending_data]  

        
        # Get Team 2 Police Verification data
        query = Team2PoliceVerification.query.filter(Team2PoliceVerification.team_id == team2.team_id)

        if not show_all_dates:

            query = query.filter(

                Team2PoliceVerification.submitted_at >= start_of_day,

                Team2PoliceVerification.submitted_at <= end_of_day

            )

        police_verification_data = query.order_by(Team2PoliceVerification.submitted_at.desc()).all()
        team2_police_verification_data = [{
            'date': item.submitted_at,
            'department': item.department,
            'strength': item.strength,
            'completed': item.completed,
            'pending': item.pending,
            'remarks': item.remarks,
        } for item in police_verification_data] 
        
        # Get Team 2 Interview Schedule data
        query = Team2InterviewSchedule.query.filter(Team2InterviewSchedule.team_id == team2.team_id)

        if not show_all_dates:

            query = query.filter(

                Team2InterviewSchedule.submitted_at >= start_of_day,

                Team2InterviewSchedule.submitted_at <= end_of_day

            )

        interview_schedule_data = query.order_by(Team2InterviewSchedule.submitted_at.desc()).all()
        team2_interview_schedule_data = [{
            'date': item.submitted_at,
            'department_category': item.department_category,
            'candidate_count': item.candidate_count,
            'interview_completion': item.interview_completion,
            'interview_status': item.interview_status,
            'nature_of_issue': item.nature_of_issue,
            'issue_description': item.issue_description,
            'comments': item.comments,
        } for item in interview_schedule_data]
        
        # Get Team 2 Exit Information data
        query = Team2ExitInformation.query.filter(Team2ExitInformation.team_id == team2.team_id)

        if not show_all_dates:

            query = query.filter(

                Team2ExitInformation.submitted_at >= start_of_day,

                Team2ExitInformation.submitted_at <= end_of_day

            )

        exit_information_data = query.order_by(Team2ExitInformation.submitted_at.desc()).all()
        team2_exit_information_data = [{
            'date': item.submitted_at,
            'exit_activity': item.exit_activity,
            'exit_department': item.exit_department,
            'exit_notice': item.exit_notice,
            'exit_name': item.exit_name,
            'exit_dept': item.exit_dept,
            'exit_reason': item.exit_reason,
            'exit_nature': item.exit_nature,
            'exit_issue_desc': item.exit_issue_desc,
            'exit_comments': item.exit_comments,
        } for item in exit_information_data]
        
      # Get Team 2 Issues / Staff Concerns data
        query = Team2IssuesStaffConcerns.query.filter(
            Team2IssuesStaffConcerns.team_id == team2.team_id,
            Team2IssuesStaffConcerns.submitted_at.isnot(None)
        )
        if not show_all_dates:
            query = query.filter(
                Team2IssuesStaffConcerns.submitted_at >= start_of_day,
                Team2IssuesStaffConcerns.submitted_at <= end_of_day
            )
        issues_staff_concerns_data = query.order_by(Team2IssuesStaffConcerns.submitted_at.desc()).all()
        team2_issues_staff_concerns_data = [{
            'date': item.submitted_at,
            'sno': item.concern_sno,
            'activity': item.concern_activity,
            'dept': item.concern_dept,
            'person': item.concern_person,
            'incharge': item.concern_incharge,
            'nature': item.concern_nature,
            'issue_desc': item.concern_issue_desc,
            'comments': item.concern_comments
        } for item in issues_staff_concerns_data]


        # Get Team 2 Kural Recitation data
        query = Team2KuralRecitation.query.filter(Team2KuralRecitation.team_id == team2.team_id)

        if not show_all_dates:

            query = query.filter(

                Team2KuralRecitation.submitted_at >= start_of_day,

                Team2KuralRecitation.submitted_at <= end_of_day

            )

        kural_recitation_data = query.order_by(Team2KuralRecitation.submitted_at.desc()).all()
        team2_kural_recitation_data = [{
            'date': item.submitted_at,
            'team': item.kural_team,
            'name': item.kural_name,
            'happened': item.kural_happened,
            'not_happened_reason': item.kural_not_happened_reason,
            'nature': item.kural_nature,
            'issue_desc': item.kural_issue_desc,
            'comments': item.kural_comments
        } for item in kural_recitation_data]
        
        # Get Team 2 Front Office Phone Calls data
        query = Team2FrontOfficePhoneCalls.query.filter(Team2FrontOfficePhoneCalls.team_id == team2.team_id)

        if not show_all_dates:

            query = query.filter(

                Team2FrontOfficePhoneCalls.submitted_at >= start_of_day,

                Team2FrontOfficePhoneCalls.submitted_at <= end_of_day

            )

        front_office_phone_calls_data = query.order_by(Team2FrontOfficePhoneCalls.submitted_at.desc()).all()
        team2_front_office_phone_calls_data = [{
            'date': item.submitted_at,
            'category': item.category,
            'incoming': item.incoming,
            'outgoing': item.outgoing,
            'nature': item.nature,
            'issue_description': item.issue_description,
            'comments': item.comments
        } for item in front_office_phone_calls_data]
        
        # Get Team 2 Visitor Log data
        query = Team2VisitorLog.query.filter(Team2VisitorLog.team_id == team2.team_id)

        if not show_all_dates:

            query = query.filter(

                Team2VisitorLog.submitted_at >= start_of_day,

                Team2VisitorLog.submitted_at <= end_of_day

            )

        visitor_log_data = query.order_by(Team2VisitorLog.submitted_at.desc()).all()
        team2_visitor_log_data = [{
            'date': item.submitted_at,
            'visitor_type': item.visitor_type,
            'purpose': item.purpose,
            'person_met': item.person_met,
            'nature': item.nature,
            'issue_description': item.issue_description,
            'comments': item.comments
        } for item in visitor_log_data]
        
        # Get Team 2 BSNL Phone Status data
        query = Team2BSNLPhoneStatus.query.filter(Team2BSNLPhoneStatus.team_id == team2.team_id)

        if not show_all_dates:

            query = query.filter(

                Team2BSNLPhoneStatus.submitted_at >= start_of_day,

                Team2BSNLPhoneStatus.submitted_at <= end_of_day

            )

        bsnl_phone_status_data = query.order_by(Team2BSNLPhoneStatus.submitted_at.desc()).all()
        team2_bsnl_phone_status_data = [{
            'date': item.submitted_at,
            'department': item.department,
            'working': item.working,
            'not_working': item.not_working,
            'rectified': item.rectified,
            'nature': item.nature,
            'issue_description': item.issue_description,
            'comments': item.comments
        } for item in bsnl_phone_status_data]
        
        # Get Team 2 Materials Inward data
        query = Team2MaterialsInward.query.filter(Team2MaterialsInward.team_id == team2.team_id)

        if not show_all_dates:

            query = query.filter(

                Team2MaterialsInward.submitted_at >= start_of_day,

                Team2MaterialsInward.submitted_at <= end_of_day

            )

        materials_inward_data = query.order_by(Team2MaterialsInward.submitted_at.desc()).all()
        team2_materials_inward_data = [{
            'date': item.submitted_at,
            'work_activity': item.work_activity,
            'department_category': item.department_category,
            'product_material': item.product_material,
            'in_time': item.in_time.strftime('%H:%M:%S') if item.in_time else None,
            'vendor': item.vendor,
            'description': item.description,
            'quantity': item.quantity,
            'nature': item.nature,
            'issue_description': item.issue_description,
            'comments': item.comments
        } for item in materials_inward_data]
        
        # Get Team 2 Materials Outward data
        query = Team2MaterialsOutward.query.filter(Team2MaterialsOutward.team_id == team2.team_id)

        if not show_all_dates:

            query = query.filter(

                Team2MaterialsOutward.submitted_at >= start_of_day,

                Team2MaterialsOutward.submitted_at <= end_of_day

            )

        materials_outward_data = query.order_by(Team2MaterialsOutward.submitted_at.desc()).all()
        team2_materials_outward_data = [{
            'date': item.submitted_at,
            'product_material': item.product_material,
            'out_time': item.out_time.strftime('%H:%M:%S') if item.out_time else None,
            'vendor': item.vendor,
            'description': item.description,
            'quantity': item.quantity,
            'nature': item.nature,
            'issue_description': item.issue_description,
            'comments': item.comments
        } for item in materials_outward_data]
        
        # Get Team 2 Materials Movement data
        query = Team2MaterialsMovement.query.filter(Team2MaterialsMovement.team_id == team2.team_id)

        if not show_all_dates:

            query = query.filter(

                Team2MaterialsMovement.submitted_at >= start_of_day,

                Team2MaterialsMovement.submitted_at <= end_of_day

            )

        materials_movement_data = query.order_by(Team2MaterialsMovement.submitted_at.desc()).all()
        team2_materials_movement_data = [{
            'date': item.submitted_at,
            'returnable': item.returnable,
            'non_returnable': item.non_returnable,
            'nature': item.nature,
            'issue_description': item.issue_description,
            'comments': item.comments
        } for item in materials_movement_data]
        
        # Get Team 2 Returnable Material Tracking data
        query = Team2ReturnableMaterialTracking.query.filter(Team2ReturnableMaterialTracking.team_id == team2.team_id)

        if not show_all_dates:

            query = query.filter(

                Team2ReturnableMaterialTracking.submitted_at >= start_of_day,

                Team2ReturnableMaterialTracking.submitted_at <= end_of_day

            )

        returnable_material_tracking_data = query.order_by(Team2ReturnableMaterialTracking.submitted_at.desc()).all()
        team2_returnable_material_tracking_data = [{
            'date': item.submitted_at,
            'description': item.description,
            'quantity': item.quantity,
            'issue_date': item.issue_date.strftime('%Y-%m-%d') if item.issue_date else None,
            'return_date': item.return_date.strftime('%Y-%m-%d') if item.return_date else None,
            'nature': item.nature,
            'issue_description': item.issue_description,
            'comments': item.comments
        } for item in returnable_material_tracking_data]
        
        # Get Team 2 Returnable Goods Report data
        query = Team2ReturnableGoodsReport.query.filter(Team2ReturnableGoodsReport.team_id == team2.team_id)

        if not show_all_dates:

            query = query.filter(

                Team2ReturnableGoodsReport.submitted_at >= start_of_day,

                Team2ReturnableGoodsReport.submitted_at <= end_of_day

            )

        returnable_goods_report_data = query.order_by(Team2ReturnableGoodsReport.submitted_at.desc()).all()
        team2_returnable_goods_report_data = [{
            'date': item.submitted_at,
            'description': item.description,
            'quantity': item.quantity,
            'issue_date': item.issue_date.strftime('%Y-%m-%d') if item.issue_date else None,
            'return_date': item.return_date.strftime('%Y-%m-%d') if item.return_date else None,
            'nature': item.nature,
            'issue_description': item.issue_description,
            'comments': item.comments
        } for item in returnable_goods_report_data]

        # Get Team 2 Campus Camera Status data
        query = Team2CampusCameraStatus.query.filter(Team2CampusCameraStatus.team_id == team2.team_id)

        if not show_all_dates:

            query = query.filter(

                Team2CampusCameraStatus.submitted_at >= start_of_day,

                Team2CampusCameraStatus.submitted_at <= end_of_day

            )

        campus_camera_status_data = query.order_by(Team2CampusCameraStatus.submitted_at.desc()).all()
        team2_campus_camera_status_data = [{
            'date': item.submitted_at,
            'particulars': item.particulars,
            'total_cameras': item.total_cameras,
            'working_cameras': item.working_cameras,
            'not_working_details': item.not_working_details,
            'nature_of_issue': item.nature_of_issue,
            'issue_description': item.issue_description,
            'comments': item.comments
        } for item in campus_camera_status_data]
        
        # Get Team 2 Vehicle Camera Status data
        query = Team2VehicleCameraStatus.query.filter(Team2VehicleCameraStatus.team_id == team2.team_id)

        if not show_all_dates:

            query = query.filter(

                Team2VehicleCameraStatus.submitted_at >= start_of_day,

                Team2VehicleCameraStatus.submitted_at <= end_of_day

            )

        vehicle_camera_status_data = query.order_by(Team2VehicleCameraStatus.submitted_at.desc()).all()
        team2_vehicle_camera_status_data = [{
            'date': item.submitted_at,
            'particulars': item.particulars,
            'route_numbers': item.route_numbers,
            'camera_id': item.camera_id,
            'working_status': item.working_status,
            'not_working_details': item.not_working_details,
            'nature_of_issue': item.nature_of_issue,
            'issue_description': item.issue_description,
            'comments': item.comments
        } for item in vehicle_camera_status_data]

        # Get Team 2 Bus AC Camera Status data
        query = Team2BusACCameraStatus.query.filter(Team2BusACCameraStatus.team_id == team2.team_id)

        if not show_all_dates:

            query = query.filter(

                Team2BusACCameraStatus.submitted_at >= start_of_day,

                Team2BusACCameraStatus.submitted_at <= end_of_day

            )

        bus_ac_camera_status_data = query.order_by(Team2BusACCameraStatus.submitted_at.desc()).all()
        team2_bus_ac_camera_status_data = [{
            'date': item.submitted_at,
            'particulars': item.particulars,
            'route': item.route,
            'camera_id': item.camera_id,
            'working_status': item.working_status,
            'not_working_details': item.not_working_details,
            'nature_of_issue': item.nature_of_issue,
            'issue_description': item.issue_description,
            'comments': item.comments
        } for item in bus_ac_camera_status_data]

# Get GPS Monitoring data
        query = Team2GPSMonitoring.query.filter(Team2GPSMonitoring.team_id == team2.team_id)

        if not show_all_dates:

            query = query.filter(

                Team2GPSMonitoring.submitted_at >= start_of_day,

                Team2GPSMonitoring.submitted_at <= end_of_day

            )

        gps_monitoring_data = query.order_by(Team2GPSMonitoring.submitted_at.desc()).all()
        team2_gps_monitoring_data = []
        for item in gps_monitoring_data:
            team2_gps_monitoring_data.append({
                'date': item.submitted_at,
                'particulars': item.particulars,
                'vehicles': item.vehicles,
                'halt_2_mins': item.halt_2_mins,
                'over_speed': item.over_speed,
                'footage': f'/file/{item.footage_file_id}' if item.footage_file_id else None,
                'nature_of_issue': item.nature_of_issue,
                'issue_description': item.issue_description,    
                'comments': item.comments
            })

        # Get Issues Identified (Monitoring) data
        query = Team2IssuesIdentifiedMonitoring.query.filter(Team2IssuesIdentifiedMonitoring.team_id == team2.team_id)

        if not show_all_dates:

            query = query.filter(

                Team2IssuesIdentifiedMonitoring.submitted_at >= start_of_day,

                Team2IssuesIdentifiedMonitoring.submitted_at <= end_of_day

            )

        issues_identified_monitoring_data = query.order_by(Team2IssuesIdentifiedMonitoring.submitted_at.desc()).all()
        team2_issues_identified_monitoring_data = []
        for item in issues_identified_monitoring_data:
            team2_issues_identified_monitoring_data.append({
                'date': item.submitted_at,
                'particulars': item.particulars,
                'venue': item.venue,
                'time': item.time,
                'nature_of_issue': item.nature_of_issue,
                'escalated_to': item.escalated_to,
                'action_taken': item.action_taken,
                'any_issues_on_observation': item.any_issues_on_observation
            })

        # Get Teachers Late Reporting data
        query = Team2IssuesIdentifiedControlRoom.query.filter(Team2IssuesIdentifiedControlRoom.team_id == team2.team_id)

        if not show_all_dates:

            query = query.filter(

                Team2IssuesIdentifiedControlRoom.submitted_at >= start_of_day,

                Team2IssuesIdentifiedControlRoom.submitted_at <= end_of_day

            )

        teachers_late_reporting_data = query.order_by(Team2IssuesIdentifiedControlRoom.submitted_at.desc()).all()
        team2_teachers_late_reporting_data = [{
             'date': item.submitted_at,
             'particulars': item.particulars,
             'no_of_late_reports': item.no_of_late_reports,
             'no_of_members_entered_reason': item.no_of_members_entered_reason,
             'on_time_acknowledgement': item.on_time_acknowledgement,
             'nature_of_issue': item.nature_of_issue,
             'escalated_to': item.escalated_to,
             'action_taken': item.action_taken
        } for item in teachers_late_reporting_data]

         # team2_issues_camera_footage
        query = Team2CameraFootageEntry.query.filter(Team2CameraFootageEntry.team_id == team2.team_id)

        if not show_all_dates:

            query = query.filter(

                Team2CameraFootageEntry.submitted_at >= start_of_day,

                Team2CameraFootageEntry.submitted_at <= end_of_day

            )

        camera_footage_data = query.order_by(Team2CameraFootageEntry.submitted_at.desc()).all()
        team2_camera_footage_data = [{
            'date': item.submitted_at,
            'particulars': item.particulars,
            'name': item.name,
            'comments': item.comments
        } for item in camera_footage_data]

        # Get Team 2 Biometrics Access Card Punching data
        query = Team2BiometricsAccessCardPunching.query.filter(Team2BiometricsAccessCardPunching.team_id == team2.team_id)

        if not show_all_dates:

            query = query.filter(

                Team2BiometricsAccessCardPunching.submitted_at >= start_of_day,

                Team2BiometricsAccessCardPunching.submitted_at <= end_of_day

            )

        biometrics_data = query.order_by(Team2BiometricsAccessCardPunching.submitted_at.desc()).all()
        team2_biometrics_access_card_punching_data = [
            {
                'date': item.submitted_at,
                'particulars': item.particulars,  # Use particulars instead of category
                'total': item.total_punching,
                'absent': item.absent_punching,
                'punched': item.punched_punching,
                'not_punched': item.not_punching,
                'nature_of_issue': item.nature_of_issue,
                'issue_description': item.issue_description,
                'comments': item.comments
            }
            for item in biometrics_data
        ]



 # Get Water TDS Deviation data

        query = Team2WaterTDSDeviation.query.filter(Team2WaterTDSDeviation.team_id == team2.team_id)


        if not show_all_dates:


            query = query.filter(


                Team2WaterTDSDeviation.submitted_at >= start_of_day,


                Team2WaterTDSDeviation.submitted_at <= end_of_day


            )


        water_tds_deviation_data = query.order_by(Team2WaterTDSDeviation.submitted_at.desc()).all()
        team2_water_tds_deviation_data = [{
            'date': item.submitted_at,
            'particulars': item.particulars,
            'ro_details': item.ro_details,
            'tds': item.tds,
            'ph': item.ph,
            'nature_of_issue': item.nature_of_issue,
            'issue_description': item.issue_description,
            'comments': item.comments
        } for item in water_tds_deviation_data]

# Get Testing & Cleaning data
        query = Team2TestingCleaning.query.filter(Team2TestingCleaning.team_id == team2.team_id)

        if not show_all_dates:

            query = query.filter(

                Team2TestingCleaning.submitted_at >= start_of_day,

                Team2TestingCleaning.submitted_at <= end_of_day

            )

        testing_cleaning_data = query.order_by(Team2TestingCleaning.submitted_at.desc()).all()
        team2_testing_cleaning_data = [{
            'date': item.submitted_at,
            'particulars': item.particulars,
            'regular_process': item.regular_process,
            'deep_cleaning': item.deep_cleaning,
            'event_arrangement': item.event_arrangement,
            'nature_of_issue': item.nature_of_issue,
            'issue_description': item.issue_description,
            'comments': item.comments
        } for item in testing_cleaning_data]

        # Get Water Level Checking data
            # Query water level data for the team and date range
        query = Team2WaterLevel.query.filter(Team2WaterLevel.team_id == team2.team_id)

        if not show_all_dates:

            query = query.filter(

                Team2WaterLevel.submitted_at >= start_of_day,

                Team2WaterLevel.submitted_at <= end_of_day

            )

        water_level_data = query.order_by(Team2WaterLevel.submitted_at.desc()).all()

        # Convert to a structured list of dicts for JSON or template rendering
        team2_water_level_data = [{
            'date': item.submitted_at,
            'work_activity': item.work_activity,
            'department': item.department,
            'particulars': item.particulars,
            'floor': item.floor,
            'venue': item.venue,
            'nature_of_issue': item.nature_of_issue,
            'issue_description': item.issue_description,
            'comments': item.comments
        } for item in water_level_data]

        # Get Housekeeping General data
        # Query housekeeping general data for the team and date range
        query = Team2HousekeepingGeneral.query.filter(Team2HousekeepingGeneral.team_id == team2.team_id)

        if not show_all_dates:

            query = query.filter(

                Team2HousekeepingGeneral.submitted_at >= start_of_day,

                Team2HousekeepingGeneral.submitted_at <= end_of_day

            )

        housekeeping_general_data = query.order_by(Team2HousekeepingGeneral.submitted_at.desc()).all()

        # Convert to a structured list of dicts for JSON or template rendering
        team2_housekeeping_general_data = [{
            'date': item.submitted_at,
            'work_activity': item.work_activity,
            'department': item.department,
            'particulars': item.particulars,
            'name': item.name,
            'observation': item.observation,
            'remark': item.remark
        } for item in housekeeping_general_data]


# Get Pool Testing data
        query = Team2PoolTesting.query.filter(Team2PoolTesting.team_id == team2.team_id)

        if not show_all_dates:

            query = query.filter(

                Team2PoolTesting.submitted_at >= start_of_day,

                Team2PoolTesting.submitted_at <= end_of_day

            )

        pool_testing_data = query.order_by(Team2PoolTesting.submitted_at.desc()).all()
        team2_pool_testing_data = [{
            'date': item.submitted_at,
            'particulars': item.particulars,
            'chlorine_level': item.chlorine_level,
            'ph_level': item.ph_level,
            'water_cleanliness': item.water_cleanliness,
            'nature_of_issue': item.nature_of_issue,
            'issue_description': item.issue_description,
            'comments': item.comments
        } for item in pool_testing_data]

 # Get Washroom Cleanliness data
        query = Team2WashroomCleanliness.query.filter(Team2WashroomCleanliness.team_id == team2.team_id)

        if not show_all_dates:

            query = query.filter(

                Team2WashroomCleanliness.submitted_at >= start_of_day,

                Team2WashroomCleanliness.submitted_at <= end_of_day

            )

        washroom_cleanliness_data = query.order_by(Team2WashroomCleanliness.submitted_at.desc()).all()
        team2_washroom_cleanliness_data = [{
            'date': item.submitted_at,
            'floor': item.floor,
            'particulars': item.particulars,
            'boys_washroom': item.boys_washroom,
            'girls_washroom': item.girls_washroom,
            'cleanliness': item.cleanliness,
            'smell': item.smell,
            'restroom_equipment': item.restroom_equipment
        } for item in washroom_cleanliness_data]

# get Transport Attendance  for team lead 2
        query = Team2TransportAttendance.query.filter(Team2TransportAttendance.team_id == team2.team_id)

        if not show_all_dates:

            query = query.filter(

                Team2TransportAttendance.submitted_at >= start_of_day,

                Team2TransportAttendance.submitted_at <= end_of_day

            )

        transport_attendance_data = query.order_by(Team2TransportAttendance.submitted_at.desc()).all()
        team2_transport_attendance_data = [{
            'date': item.submitted_at,
            'work_activity': item.work_activity,
            'department': item.department,
            'particulars': item.particulars,
            'students_morning': item.students_morning,
            'students_evening': item.students_evening,
            'staff_morning': item.staff_morning,
            'staff_evening': item.staff_evening,
            'nature_of_issue': item.nature_of_issue,
            'issue_description': item.issue_description,
            'comments': item.comments
        } for item in transport_attendance_data]

 #get AC Working Status  for team lead 2
        query = Team2ACWorkingStatus.query.filter(Team2ACWorkingStatus.team_id == team2.team_id)

        if not show_all_dates:

            query = query.filter(

                Team2ACWorkingStatus.submitted_at >= start_of_day,

                Team2ACWorkingStatus.submitted_at <= end_of_day

            )

        ac_working_status_data = query.order_by(Team2ACWorkingStatus.submitted_at.desc()).all()
        team2_ac_working_status_data = [{
            'date': item.submitted_at,
            'work_activity': item.work_activity,
            'department': item.department,
            'particulars': item.particulars,
            'route_numbers': item.route_numbers,
            'nature_of_issue': item.nature_of_issue,
            'issue_description': item.issue_description,
            'comments': item.comments
        } for item in ac_working_status_data]

# Late Reporting  for team lead 2
        query = Team2LateReporting.query.filter(Team2LateReporting.team_id == team2.team_id)

        if not show_all_dates:

            query = query.filter(

                Team2LateReporting.submitted_at >= start_of_day,

                Team2LateReporting.submitted_at <= end_of_day

            )

        late_reporting_data = query.order_by(Team2LateReporting.submitted_at.desc()).all()
        team2_late_reporting_data = [{
            'date': item.submitted_at,
            'work_activity': item.work_activity,
            'department': item.department,
            'particulars': item.particulars,
            'route_numbers': item.route_numbers,
            'nature_of_issue': item.nature_of_issue,
            'issue_description': item.issue_description,
            'comments': item.comments
        } for item in late_reporting_data]

# Maintenance / Service / Issues  for team lead 2
        query = Team2MaintenanceServiceIssues.query.filter(Team2MaintenanceServiceIssues.team_id == team2.team_id)

        if not show_all_dates:

            query = query.filter(

                Team2MaintenanceServiceIssues.submitted_at >= start_of_day,

                Team2MaintenanceServiceIssues.submitted_at <= end_of_day

            )

        maintenance_service_issues_data = query.order_by(Team2MaintenanceServiceIssues.submitted_at.desc()).all()
        team2_maintenance_service_issues_data = [{
            'date': item.submitted_at,
            'work_activity': item.work_activity,
            'department': item.department,
            'particulars': item.particulars,
            'route_numbers': item.route_numbers,
            'work_nature': item.work_nature,
            'venue': item.venue,
            'work_status': item.work_status,
            'nature_of_issue': item.nature_of_issue,
            'issue_description': item.issue_description,
            'comments': item.comments
        } for item in maintenance_service_issues_data]

# Car Maintenance/Cleaning  for team lead 2
        query = Team2CarMaintenanceCleaning.query.filter(Team2CarMaintenanceCleaning.team_id == team2.team_id)

        if not show_all_dates:

            query = query.filter(

                Team2CarMaintenanceCleaning.submitted_at >= start_of_day,

                Team2CarMaintenanceCleaning.submitted_at <= end_of_day

            )

        car_maintenance_cleaning_data = query.order_by(Team2CarMaintenanceCleaning.submitted_at.desc()).all()
        team2_car_maintenance_cleaning_data = [{
            'date': item.submitted_at,
            'work_activity': item.work_activity,
            'department': item.department,
            'particulars': item.particulars,
            'car_number': item.car_number,
            'cleaned_by': item.cleaned_by,
            'maintenance_service_issues': item.maintenance_service_issues,
            'nature_of_issue': item.nature_of_issue,
            'issue_description': item.issue_description,
            'comments': item.comments
        } for item in car_maintenance_cleaning_data]

 # Vehicle Renewals / Delays  for team lead 2
        query = Team2VehicleRenewalsDelays.query.filter(Team2VehicleRenewalsDelays.team_id == team2.team_id)

        if not show_all_dates:

            query = query.filter(

                Team2VehicleRenewalsDelays.submitted_at >= start_of_day,

                Team2VehicleRenewalsDelays.submitted_at <= end_of_day

            )

        vehicle_renewals_delays_data = query.order_by(Team2VehicleRenewalsDelays.submitted_at.desc()).all()
        team2_vehicle_renewals_delays_data = [{
            'date': item.submitted_at,
            'work_activity': item.work_activity,
            'department': item.department,
            'particulars': item.particulars,
            'vehicle_numbers': item.vehicle_numbers,
            'route_numbers': item.route_numbers,
            'nature_of_issue': item.nature_of_issue,
            'issue_description': item.issue_description,
            'comments': item.comments
        } for item in vehicle_renewals_delays_data]

 # Special Trip  for team lead 2

        query = Team2SpecialTrip.query.filter(Team2SpecialTrip.team_id == team2.team_id)


        if not show_all_dates:


            query = query.filter(


                Team2SpecialTrip.submitted_at >= start_of_day,


                Team2SpecialTrip.submitted_at <= end_of_day


            )


        special_trip_data = query.order_by(Team2SpecialTrip.submitted_at.desc()).all()
        team2_special_trip_data = [{
            'date': item.submitted_at,
            'work_activity': item.work_activity,
            'department': item.department,
            'particulars': item.particulars,
            'route_numbers': item.route_numbers,
            'actual_out_time': item.actual_out_time,
            'nature_of_issue': item.nature_of_issue,
            'issue_description': item.issue_description,
            'comments': item.comments
        } for item in special_trip_data]

        # Parent Concern Details  for team lead 2 # Get Team 1 Parent Concern Details data with proper date filtering
        query = Team2ParentConcernDetail.query.filter(Team2ParentConcernDetail.team_id == team2.team_id)

        if not show_all_dates:

            query = query.filter(

                Team2ParentConcernDetail.submitted_at >= start_of_day,

                Team2ParentConcernDetail.submitted_at <= end_of_day

            )

        parent_concern_detail_data = query.order_by(Team2ParentConcernDetail.submitted_at.desc()).all()
        team2_parent_concern_detail_data = [{
            
            'date': item.submitted_at,
            'work_activity': item.pc_work_activity,
            'student_name': item.pc_detail_name,
            'grade': item.pc_detail_grade,
            'concern_expressed': item.pc_detail_concern,
            'incharges_handled': item.pc_detail_incharge,
            'nature_of_issue': item.pc_detail_issue_nature,
            'comments': item.pc_detail_comment
        } for item in parent_concern_detail_data]

#get AC Temperature  for team lead 2
        query = Team2ACTemperatureCheck.query.filter(Team2ACTemperatureCheck.team_id == team2.team_id)

        if not show_all_dates:

            query = query.filter(

                Team2ACTemperatureCheck.submitted_at >= start_of_day,

                Team2ACTemperatureCheck.submitted_at <= end_of_day

            )

        ac_temperature_data = query.order_by(Team2ACTemperatureCheck.submitted_at.desc()).all()
        team2_ac_temperature_data = [{
            'date': item.submitted_at,
            'work_activity': item.work_activity,
            'department': item.department,
            'floor': item.floor,
            'particulars': item.particulars,
            'classroom': item.classroom,
            'temperature': item.temperature,
            'hot_cold_normal': item.hot_cold_normal,
            'working_condition': item.working_condition,
            'nature_of_issue': item.nature_of_issue,
            'issue_description': item.issue_description,
            'comments': item.comments
        } for item in ac_temperature_data]

# get Section 15: Labor, EB, Solar, Genset

# Labor, EB, Solar, Genset - Maintenance Labor

        query = Team2LaborEbSolarGenset.query.filter(Team2LaborEbSolarGenset.team_id == team2.team_id)


        if not show_all_dates:


            query = query.filter(


                Team2LaborEbSolarGenset.submitted_at >= start_of_day,


                Team2LaborEbSolarGenset.submitted_at <= end_of_day


            )


        labor_eb_solar_genset_data = query.order_by(Team2LaborEbSolarGenset.submitted_at.desc()).all()
        team2_maintenance_labor_data = [{
            'date': item.submitted_at,
            'work_activity': item.work_activity,
            'department': item.department,
            'nature_of_work': item.nature_of_work,
            'no_of_labours': item.no_of_labours,
            'venue': item.venue,
            'nature_of_issue': item.nature_of_issue,
            'issue_description': item.issue_description,
            'comments': item.comments
        } for item in labor_eb_solar_genset_data]

# Motor Control for team lead 2
        query = Team2Motor.query.filter(Team2Motor.team_id == team2.team_id)

        if not show_all_dates:

            query = query.filter(

                Team2Motor.submitted_at >= start_of_day,

                Team2Motor.submitted_at <= end_of_day

            )

        motor_data = query.order_by(Team2Motor.submitted_at.desc()).all()
        team2_motor_data = [{
            'date': item.submitted_at,
            'work_activity': item.work_activity,
            'department': item.department,
            'on_time': item.on_time,
            'off_time': item.off_time,
            'nature_of_issue': item.nature_of_issue,
            'issue_description': item.issue_description,
            'comments': item.comments
        } for item in motor_data]

# Pest Control for team lead 2
        query = Team2PestControl.query.filter(Team2PestControl.team_id == team2.team_id)

        if not show_all_dates:

            query = query.filter(

                Team2PestControl.submitted_at >= start_of_day,

                Team2PestControl.submitted_at <= end_of_day

            )

        pest_control_data = query.order_by(Team2PestControl.submitted_at.desc()).all()
        team2_pest_control_data = [{
            'date': item.submitted_at,
            'work_activity': item.work_activity,
            'department': item.department,
            'in_time': item.in_time,
            'out_time': item.out_time,
            'area_covered': item.area_covered,
            'nature_of_issue': item.nature_of_issue,
            'issue_description': item.issue_description,
            'comments': item.comments
        } for item in pest_control_data]

# AC Temp Deviation (>27°C)  for team lead 2
        query = Team2ACTempDeviation.query.filter(Team2ACTempDeviation.team_id == team2.team_id)

        if not show_all_dates:

            query = query.filter(

                Team2ACTempDeviation.submitted_at >= start_of_day,

                Team2ACTempDeviation.submitted_at <= end_of_day

            )

        ac_temp_deviation_data = query.order_by(Team2ACTempDeviation.submitted_at.desc()).all()
        team2_ac_temp_deviation_data = [{
            'date': item.submitted_at,
            'work_activity': item.work_activity,
            'department': item.department,
            'venue': item.venue,
            'nature_of_issue': item.nature_of_issue,
            'issue_description': item.issue_description,
            'comments': item.comments
        } for item in ac_temp_deviation_data]

 # Electricity Consumption  for team lead 2
        query = Team2ElectricityConsumption.query.filter(Team2ElectricityConsumption.team_id == team2.team_id)

        if not show_all_dates:

            query = query.filter(

                Team2ElectricityConsumption.submitted_at >= start_of_day,

                Team2ElectricityConsumption.submitted_at <= end_of_day

            )

        electricity_consumption_data = query.order_by(Team2ElectricityConsumption.submitted_at.desc()).all()
        team2_electricity_consumption_data = [{
            'date': item.submitted_at,
            'work_activity': item.work_activity,
            'department': item.department,
            'category': item.category,
            'total_units': item.total_units,
            'eb': item.eb,
            'solar': item.solar,
            'genset': item.genset,
            'eb_issue': item.eb_issue,
            'solar_issue': item.solar_issue,
            'genset_issue': item.genset_issue,
            'overall_issue_desc': item.overall_issue_desc,
            'overall_comments': item.overall_comments
        } for item in electricity_consumption_data]

 # EB Details  for team lead 2
        query = Team2EBDetails.query.filter(Team2EBDetails.team_id == team2.team_id)

        if not show_all_dates:

            query = query.filter(

                Team2EBDetails.submitted_at >= start_of_day,

                Team2EBDetails.submitted_at <= end_of_day

            )

        eb_details_data = query.order_by(Team2EBDetails.submitted_at.desc()).all()
        team2_eb_details_data = [{
            'date': item.submitted_at,
            'work_activity': item.work_activity,
            'department': item.department,
            'category': item.category,
            'rw_230_240': item.rw_230_240,
            'yw_230_240': item.yw_230_240,
            'bw_230_240': item.bw_230_240,
            'max_demand_104': item.max_demand_104,
            'units_per_day': item.units_per_day,
            'nature_of_issue': item.nature_of_issue
        } for item in eb_details_data]

# Solar Details  for team lead 2
        query = Team2SolarDetails.query.filter(Team2SolarDetails.team_id == team2.team_id)

        if not show_all_dates:

            query = query.filter(

                Team2SolarDetails.submitted_at >= start_of_day,

                Team2SolarDetails.submitted_at <= end_of_day

            )

        solar_details_data = query.order_by(Team2SolarDetails.submitted_at.desc()).all()
        team2_solar_details_data = [{
            'date': item.submitted_at,
            'work_activity': item.work_activity,
            'department': item.department,
            'category': item.category,
            'capacity': item.capacity,
            'units_per_day': item.units_per_day,
            'remarks': item.remarks,
            'time': item.time,
            'max_production': item.max_production,
            'nature_of_issue': item.nature_of_issue,
            'issue_description': item.issue_description,
            'comments': item.comments
        } for item in solar_details_data]

# Genset Details  for team lead 2
        query = Team2GensetDetails.query.filter(Team2GensetDetails.team_id == team2.team_id)

        if not show_all_dates:

            query = query.filter(

                Team2GensetDetails.submitted_at >= start_of_day,

                Team2GensetDetails.submitted_at <= end_of_day

            )

        genset_details_data = query.order_by(Team2GensetDetails.submitted_at.desc()).all()
        team2_genset_details_data = [{
            'date': item.submitted_at,
            'work_activity': item.work_activity,
            'department': item.department,
            'category': item.category,
            'on_time': item.on_time,
            'off_time': item.off_time,
            'battery_voltage': item.battery_voltage,
            'coolant_temp': item.coolant_temp,
            'nature_of_issue': item.nature_of_issue,
            'issue_description': item.issue_description,
            'comments': item.comments
        } for item in genset_details_data]

# Count Verification  for team lead 2

        query = Team2CountVerification.query.filter(Team2CountVerification.team_id == team2.team_id)


        if not show_all_dates:


            query = query.filter(


                Team2CountVerification.submitted_at >= start_of_day,


                Team2CountVerification.submitted_at <= end_of_day


            )


        count_verification_data = query.order_by(Team2CountVerification.submitted_at.desc()).all()
        team2_count_verification_data = [{
            'date': item.submitted_at,
            'work_activity': item.work_activity,
            'department': item.department,
            'category': item.category,
            'particulars': item.particulars,
            'total': item.total,
            'received': item.received,
            'submitted': item.submitted,
            'nature_of_issue': item.nature_of_issue,
            'issue_description': item.issue_description,
            'comments': item.comments
        } for item in count_verification_data]

#Attendance Replacement  for team lead 2
        query = Team2AttendanceReplacement.query.filter(Team2AttendanceReplacement.team_id == team2.team_id)

        if not show_all_dates:

            query = query.filter(

                Team2AttendanceReplacement.submitted_at >= start_of_day,

                Team2AttendanceReplacement.submitted_at <= end_of_day

            )

        attendance_replacement_data = query.order_by(Team2AttendanceReplacement.submitted_at.desc()).all()
        team2_attendance_replacement_data = [{
            'date': item.submitted_at,
            'work_activity': item.work_activity,
            'department': item.department,
            'particulars': item.particulars,
            'allotted': item.allotted,
            'replaced': item.replaced,
            'nature_of_issue': item.nature_of_issue,
            'issue_description': item.issue_description,
            'comments': item.comments
        } for item in attendance_replacement_data]

#Security Info Note  for team lead 2
        query = Team2SecurityInfoNote.query.filter(Team2SecurityInfoNote.team_id == team2.team_id)

        if not show_all_dates:

            query = query.filter(

                Team2SecurityInfoNote.submitted_at >= start_of_day,

                Team2SecurityInfoNote.submitted_at <= end_of_day

            )

        security_info_note_data = query.order_by(Team2SecurityInfoNote.submitted_at.desc()).all()
        team2_security_info_note_data = [{
            'date': item.submitted_at,
            'work_activity': item.work_activity,
            'department': item.department,
            'particulars': item.particulars,
            'info_by': item.info_by,
            'information': item.information,
            'nature_of_issue': item.nature_of_issue,
            'issue_description': item.issue_description,
            'comments': item.comments
        } for item in security_info_note_data]

# Security Govt Officials In/Out  for team lead 2
        query = Team2SecurityGovtInout.query.filter(Team2SecurityGovtInout.team_id == team2.team_id)

        if not show_all_dates:

            query = query.filter(

                Team2SecurityGovtInout.submitted_at >= start_of_day,

                Team2SecurityGovtInout.submitted_at <= end_of_day

            )

        security_govt_inout_data = query.order_by(Team2SecurityGovtInout.submitted_at.desc()).all()
        team2_security_govt_inout_data = [{
            'date': item.submitted_at,
            'work_activity': item.work_activity,
            'department': item.department,
            'particulars': item.particulars,
            'in_time': item.in_time,
            'out_time': item.out_time,
            'purpose': item.purpose,
            'nature_of_issue': item.nature_of_issue,
            'issue_description': item.issue_description,
            'comments': item.comments
        } for item in security_govt_inout_data]

# Security Alcohol Test  for team lead 2
        query = Team2AlcoholTest.query.filter(Team2AlcoholTest.team_id == team2.team_id)

        if not show_all_dates:

            query = query.filter(

                Team2AlcoholTest.submitted_at >= start_of_day,

                Team2AlcoholTest.submitted_at <= end_of_day

            )

        alcohol_test_data = query.order_by(Team2AlcoholTest.submitted_at.desc()).all()
        team2_alcohol_test_data = [{
            'date': item.submitted_at,
            'work_activity': item.work_activity,
            'department': item.department,
            'name': item.name,
            'time': item.time,
            'reading': item.reading,
            'comments': item.comments
        } for item in alcohol_test_data]

# Security Materials Inward  for team lead 2
        query = Team2SecurityMaterialsInout.query.filter(Team2SecurityMaterialsInout.team_id == team2.team_id)

        if not show_all_dates:

            query = query.filter(

                Team2SecurityMaterialsInout.submitted_at >= start_of_day,

                Team2SecurityMaterialsInout.submitted_at <= end_of_day

            )

        materials_inward_data = query.order_by(Team2SecurityMaterialsInout.submitted_at.desc()).all()
        team2_security_materials_inward_data = [{
            'date': item.submitted_at,
            'work_activity': item.work_activity,
            'department': item.department,
            'product': item.product,
            'in_time': item.in_time,
            'vendor': item.vendor,
            'description': item.description,
            'quantity': item.quantity,
            'nature_of_issue': item.nature_of_issue,
            'issue_description': item.issue_description,
            'comments': item.comments
        } for item in materials_inward_data]

# Security Materials Outward  for team lead 2

        query = Team2SecurityMaterialsOutward.query.filter(Team2SecurityMaterialsOutward.team_id == team2.team_id)


        if not show_all_dates:


            query = query.filter(


                Team2SecurityMaterialsOutward.submitted_at >= start_of_day,


                Team2SecurityMaterialsOutward.submitted_at <= end_of_day


            )


        materials_outward_data = query.order_by(Team2SecurityMaterialsOutward.submitted_at.desc()).all()
        team2_security_materials_outward_data = [{
            'date': item.submitted_at,
            'work_activity': item.work_activity,
            'department': item.department,
            'product': item.product,
            'out_time': item.out_time,
            'vendor': item.vendor,
            'description': item.description,
            'quantity': item.quantity,
            'nature_of_issue': item.nature_of_issue,
            'issue_description': item.issue_description,
            'comments': item.comments
        } for item in materials_outward_data]

# Security Transport Verification  for team lead 2

        query = Team2TransportVerification.query.filter(Team2TransportVerification.team_id == team2.team_id)


        if not show_all_dates:


            query = query.filter(


                Team2TransportVerification.submitted_at >= start_of_day,


                Team2TransportVerification.submitted_at <= end_of_day


            )


        transport_verification_data = query.order_by(Team2TransportVerification.submitted_at.desc()).all()
        team2_transport_verification_data = [{
            'date': item.submitted_at,
            'work_activity': item.work_activity,
            'department': item.department,
            'vehicle_number': item.vehicle_number,
            'damage_location': item.damage_location,
            'escalated_to': item.escalated_to,
            'nature_of_issue': item.nature_of_issue,
            'issue_description': item.issue_description,
            'comments': item.comments
        } for item in transport_verification_data]

# Documents Movement  for team lead 2

        query = Team2DocumentsMovement.query.filter(Team2DocumentsMovement.team_id == team2.team_id)


        if not show_all_dates:


            query = query.filter(


                Team2DocumentsMovement.submitted_at >= start_of_day,


                Team2DocumentsMovement.submitted_at <= end_of_day


            )


        documents_movement_data = query.order_by(Team2DocumentsMovement.submitted_at.desc()).all()
        team2_documents_movement_data = [{
            'date': item.submitted_at,
            'work_activity': item.work_activity,
            'department': item.department,
            
    # Row 1: New File / Document Entry
            'doc_new_dept': item.doc_new_dept,
            'doc_new_name': item.doc_new_name,
            'doc_new_submitby': item.doc_new_submitby,
            'doc_new_nature': item.doc_new_nature,
            'doc_new_issue': item.doc_new_issue,
            'doc_new_comments': item.doc_new_comments,
    
    # Row 2: Non-Returnable File / Document
            'doc_nonret_dept': item.doc_nonret_dept,
            'doc_nonret_name': item.doc_nonret_name,
            'doc_nonret_issuedto': item.doc_nonret_issuedto,
            'doc_nonret_nature': item.doc_nonret_nature,
            'doc_nonret_issue': item.doc_nonret_issue,
            'doc_nonret_comments': item.doc_nonret_comments,
    
    # Row 3: Original File / Doc Movement
            'doc_orig_naturedoc': item.doc_orig_naturedoc,
            'doc_orig_issuedto': item.doc_orig_issuedto,
            'doc_orig_purpose': item.doc_orig_purpose,
            'doc_orig_nature': item.doc_orig_nature,
            'doc_orig_issue': item.doc_orig_issue,
            'doc_orig_comments': item.doc_orig_comments
        } for item in documents_movement_data]

# Govt Official Documents  for team lead 2
        query = Team2GovtOfficialDocuments.query.filter(Team2GovtOfficialDocuments.team_id == team2.team_id)

        if not show_all_dates:

            query = query.filter(

                Team2GovtOfficialDocuments.submitted_at >= start_of_day,

                Team2GovtOfficialDocuments.submitted_at <= end_of_day

            )

        govt_official_documents_data = query.order_by(Team2GovtOfficialDocuments.submitted_at.desc()).all()
        team2_govt_official_documents_data = [{
            'date': item.submitted_at,
            'work_activity': item.work_activity,
            'department': item.department,
    'document_name': item.document_name,
            'expiry_date': item.expiry_date,
            'expected_renewal_date': item.expected_renewal_date,
            'nature_of_issue': item.nature_of_issue,
            'issue_description': item.issue_description,
            'comments': item.comments
        } for item in govt_official_documents_data]

 # Thoorigai Team Social Media

        query = Team2ThoorigaiTeamSocialMedia.query.filter(Team2ThoorigaiTeamSocialMedia.team_id == team2.team_id)


        if not show_all_dates:


            query = query.filter(


                Team2ThoorigaiTeamSocialMedia.submitted_at >= start_of_day,


                Team2ThoorigaiTeamSocialMedia.submitted_at <= end_of_day


            )


        thoorigai_social_media_data = query.order_by(Team2ThoorigaiTeamSocialMedia.submitted_at.desc()).all()
        team2_thoorigai_social_media_data = [{
            'date': item.submitted_at,
            'work_activity': item.work_activity,
            'department': item.department,
            'platform': item.platform,
            'video_status': item.video_status,
            'post_status': item.post_status,
            'update_status': item.update_status,
            'nature_of_issue': item.nature_of_issue,
            'issue_description': item.issue_description,
            'comments': item.comments
        } for item in thoorigai_social_media_data]

# Thoorigai Website Updates  for team lead 2

        query = Team2WebsiteUpdates.query.filter(Team2WebsiteUpdates.team_id == team2.team_id)


        if not show_all_dates:


            query = query.filter(


                Team2WebsiteUpdates.submitted_at >= start_of_day,


                Team2WebsiteUpdates.submitted_at <= end_of_day


            )


        website_updates_data = query.order_by(Team2WebsiteUpdates.submitted_at.desc()).all()
        team2_website_updates_data = [{
            'date': item.submitted_at,
            'work_activity': item.work_activity,
            'department': item.department,
            'particulars': item.particulars,
            'inclusion': item.inclusion,
            'deletion': item.deletion,
            'others': item.others,
            'nature_of_issue': item.nature_of_issue,
            'issue_description': item.issue_description,
            'comments': item.comments
        } for item in website_updates_data]

# MD Social Media  for team lead 2

        query = Team2MDSocialMedia.query.filter(Team2MDSocialMedia.team_id == team2.team_id)


        if not show_all_dates:


            query = query.filter(


                Team2MDSocialMedia.submitted_at >= start_of_day,


                Team2MDSocialMedia.submitted_at <= end_of_day


            )


        md_social_media_data = query.order_by(Team2MDSocialMedia.submitted_at.desc()).all()
        team2_md_social_media_data = [{
            'date': item.submitted_at,
            'work_activity': item.work_activity,
            'department': item.department,
            'platform': item.platform,
            'video': item.video,
            'post': item.post,
            'update': item.update,
            'nature_of_issue': item.nature_of_issue,
            'issue_description': item.issue_description,
            'comments': item.comments
        } for item in md_social_media_data]

# 20: Intercom Maintenance  for team lead 2

        query = Team2IntercomMaintenance.query.filter(Team2IntercomMaintenance.team_id == team2.team_id)


        if not show_all_dates:


            query = query.filter(


                Team2IntercomMaintenance.submitted_at >= start_of_day,


                Team2IntercomMaintenance.submitted_at <= end_of_day


            )


        intercom_maintenance_data = query.order_by(Team2IntercomMaintenance.submitted_at.desc()).all()
        team2_intercom_maintenance_data = [{
            'date': item.submitted_at,
            'work_activity': item.work_activity,
            'department': item.department,
            'working': item.working,
            'not_working': item.not_working,
            'rectified': item.rectified,
            'nature_of_issue': item.nature_of_issue,
            'issue_description': item.issue_description,
            'comments': item.comments
        } for item in intercom_maintenance_data]

# 21: Health Check Up  for team lead 2
        query = Team2HealthCheckUp.query.filter(Team2HealthCheckUp.team_id == team2.team_id)

        if not show_all_dates:

            query = query.filter(

                Team2HealthCheckUp.submitted_at >= start_of_day,

                Team2HealthCheckUp.submitted_at <= end_of_day

            )

        health_check_up_data = query.order_by(Team2HealthCheckUp.submitted_at.desc()).all()
        team2_health_check_up_data = [{
            'date': item.submitted_at,
            'work_activity': item.work_activity,
            'department': item.department,
            'department_staff': item.department_staff,
            'staff_name': item.staff_name,
            'illness': item.illness,
            'informed_by': item.informed_by,
            'action_taken': item.action_taken,
            'nature_of_issue': item.nature_of_issue,
            'issue_description': item.issue_description,
            'comments': item.comments
        } for item in health_check_up_data]

# 22: Net Connectivity & Print Details  for team lead 2
        query = Team2NetConnectivityPrintDetails.query.filter(Team2NetConnectivityPrintDetails.team_id == team2.team_id)

        if not show_all_dates:

            query = query.filter(

                Team2NetConnectivityPrintDetails.submitted_at >= start_of_day,

                Team2NetConnectivityPrintDetails.submitted_at <= end_of_day

            )

        net_connectivity_print_details_data = query.order_by(Team2NetConnectivityPrintDetails.submitted_at.desc()).all()
        team2_net_connectivity_print_details_data = [{
            'date': item.submitted_at,
            'work_activity': item.work_activity,
            'department': item.department,
            'particulars': item.particulars,
            'net_speed': item.net_speed,
            'no_of_prints': item.no_of_prints,
            'complaints': item.complaints,
            'nature_of_issue': item.nature_of_issue,
            'issue_description': item.issue_description,
            'comments': item.comments
        } for item in net_connectivity_print_details_data]

# 23: General Maintenance - IT Products  for team lead 2
        query = Team2GeneralMaintenanceITProducts.query.filter(Team2GeneralMaintenanceITProducts.team_id == team2.team_id)

        if not show_all_dates:

            query = query.filter(

                Team2GeneralMaintenanceITProducts.submitted_at >= start_of_day,

                Team2GeneralMaintenanceITProducts.submitted_at <= end_of_day

            )

        general_maintenance_it_data = query.order_by(Team2GeneralMaintenanceITProducts.submitted_at.desc()).all()
        team2_general_maintenance_it_data = [{
            'date': item.submitted_at,
            'work_activity': item.work_activity,
            'department': item.department,
            'particulars': item.particulars,
            'issues': item.issues,
            'complaintdate': item.complaintdate,
            'solveddate': item.solveddate,
            'nature_of_issue': item.nature_of_issue,
            'issue_description': item.issue_description,
            'comments': item.comments
        } for item in general_maintenance_it_data]

# 24: Calendar Schedule  for team lead 2
        query = Team2CalendarSchedule.query.filter(Team2CalendarSchedule.team_id == team2.team_id)

        if not show_all_dates:

            query = query.filter(

                Team2CalendarSchedule.submitted_at >= start_of_day,

                Team2CalendarSchedule.submitted_at <= end_of_day

            )

        calendar_schedule_data = query.order_by(Team2CalendarSchedule.submitted_at.desc()).all()
        team2_calendar_schedule_data = [{
            'date': item.submitted_at,
            'work_activity': item.work_activity,
            'department': item.department,
            'session': item.session,
            'category': item.category,
            'in_charge': item.in_charge,
            'planned': item.planned,
            'unplanned': item.unplanned,
            'nature_of_issue': item.nature_of_issue,
            'issue_description': item.issue_description,
            'comments': item.comments
        } for item in calendar_schedule_data]

# 25: Training Attendance  for team lead 2
        query = Team2TrainingAttendance.query.filter(Team2TrainingAttendance.team_id == team2.team_id)

        if not show_all_dates:

            query = query.filter(

                Team2TrainingAttendance.submitted_at >= start_of_day,

                Team2TrainingAttendance.submitted_at <= end_of_day

            )

        training_attendance_data = query.order_by(Team2TrainingAttendance.submitted_at.desc()).all()
        grouped_training = defaultdict(lambda: {
            'date': None,
            'academics_jr': None,
            'academics_sr': None,
            'admin_staff': None,
            'drivers': None,
            'security': None,
            'drivers_sub': None,
            'conductors': None,
        })
        for item in training_attendance_data:
            date_key = item.submitted_at.date()
            entry = grouped_training[date_key]
            entry['date'] = item.submitted_at
            dept_group = (item.department_group or '').strip().lower()
            dept = (item.dept or '').strip().lower()
            data = {
                'topic': item.topic,
                'total': item.total,
                'present': item.present,
                'leave': item.leave,
                'leave_percentage': item.leave_percentage,
                'nature': item.nature_of_issue,
                'issue_desc': item.issue_description,
                'comments': item.comments,
            }
            if dept_group == 'academics' and dept == 'academics - jr.school':
                entry['academics_jr'] = data
            elif dept_group == 'academics' and dept == 'academics - sr.school':
                entry['academics_sr'] = data
            elif dept_group == 'admin' and dept == 'admin - admin':
                entry['admin_staff'] = data
            elif dept_group == 'admin' and dept == 'admin - drivers':
                entry['drivers'] = data
            elif dept_group == 'admin' and dept == 'admin - securities':
                entry['security'] = data
            elif dept_group == 'admin' and dept == 'admin - drivers (sub)':
                entry['drivers_sub'] = data
            elif dept_group == 'admin' and dept == 'admin - conductors':
                entry['conductors'] = data
        team2_training_attendance_data = list(grouped_training.values())


# 26: Training Details  for team lead 2
        query = Team2TrainingDetails.query.filter(Team2TrainingDetails.team_id == team2.team_id)

        if not show_all_dates:

            query = query.filter(

                Team2TrainingDetails.submitted_at >= start_of_day,

                Team2TrainingDetails.submitted_at <= end_of_day

            )

        training_details_data = query.order_by(Team2TrainingDetails.submitted_at.desc()).all()
        team2_training_details_data = [{
            'date': item.submitted_at,
            'work_activity': item.work_activity,
            'department': item.department,
            'name': item.name,
            'dept': item.dept,
            'topic': item.topic,
            'no_of_days_hrs': item.no_of_days_hrs,
            'nature_of_issue': item.nature_of_issue,
            'issue_description': item.issue_description,
            'comments': item.comments
        } for item in training_details_data]

# 27: Manpower Planning  for team lead 2
        query = Team2ManpowerPlanning.query.filter(Team2ManpowerPlanning.team_id == team2.team_id)

        if not show_all_dates:

            query = query.filter(

                Team2ManpowerPlanning.submitted_at >= start_of_day,

                Team2ManpowerPlanning.submitted_at <= end_of_day

            )

        manpower_planning_data = query.order_by(Team2ManpowerPlanning.submitted_at.desc()).all()
        team2_manpower_planning_data = [{   
            'date': item.submitted_at,
            'mp_department': item.mp_department,
            'mp_staff_name': item.mp_staff_name,
            'mp_designation': item.mp_designation,
            'mp_grades': item.mp_grades,
            'mp_relieve_date': item.mp_relieve_date,    
            'mp_budget': item.mp_budget,
            'mp_new_find': item.mp_new_find
        } for item in manpower_planning_data]

# 28: Overall Consolidation  for team lead 2    
        query = Team2OverallConsolidation.query.filter(Team2OverallConsolidation.team_id == team2.team_id)

        if not show_all_dates:

            query = query.filter(

                Team2OverallConsolidation.submitted_at >= start_of_day,

                Team2OverallConsolidation.submitted_at <= end_of_day

            )

        overall_consolidation_data = query.order_by(Team2OverallConsolidation.submitted_at.desc()).all()
        team2_overall_consolidation_data = [{     
            'date': item.submitted_at,
            'oc_department': item.oc_department,
            'oc_total': item.oc_total,
            'oc_required': item.oc_required,
            'oc_shortlisted': item.oc_shortlisted,
            'oc_waiting_list': item.oc_waiting_list,    
            'oc_yet_to_find': item.oc_yet_to_find
        } for item in overall_consolidation_data]
        
# 29: Uniform Details  for team lead 2
        query = Team2UniformDetails.query.filter(Team2UniformDetails.team_id == team2.team_id)

        if not show_all_dates:

            query = query.filter(

                Team2UniformDetails.submitted_at >= start_of_day,

                Team2UniformDetails.submitted_at <= end_of_day

            )

        uniform_details_data = query.order_by(Team2UniformDetails.submitted_at.desc()).all()
        team2_uniform_details_data = [{
            'date': item.submitted_at,
            'uniform': item.ud_uniform,
            'designation': item.ud_designation,
            'details': item.ud_details,
            'remarks': item.ud_remarks,
            'closure_date': item.ud_closure_date
        } for item in uniform_details_data]

# 30: Department Wise Uniform Details  for team lead 2

        query = Team2DepartmentWiseUniformDetails.query.filter(Team2DepartmentWiseUniformDetails.team_id == team2.team_id)


        if not show_all_dates:


            query = query.filter(


                Team2DepartmentWiseUniformDetails.submitted_at >= start_of_day,


                Team2DepartmentWiseUniformDetails.submitted_at <= end_of_day


            )


        dept_wise_uniform_details_data = query.order_by(Team2DepartmentWiseUniformDetails.submitted_at.desc()).all()
        team2_dept_wise_uniform_details_data = [{
            'date': item.submitted_at,
            'department': item.dwud_department,
            'total': item.dwud_total,
            'completed': item.dwud_completed,
            'pending': item.dwud_pending,
            'names': item.dwud_names,
            'dress_code': item.dwud_dress_code,
            'status': item.dwud_status
        } for item in dept_wise_uniform_details_data]


# Get Team 3 audit data if selected team is 'all' or 'team3'

    return {
        'team2_hr_attendance_data': team2_hr_attendance_data,
        'team2_total_hr_attendance_data': team2_total_hr_attendance_data,
        'team2_admin_attendance_data': team2_admin_attendance_data,
        'team2_recruitment_activity_data': team2_recruitment_activity_data,
        'team2_pending_recruitment_data': team2_pending_recruitment_data,
        'team2_recruitment_pipeline_data': team2_recruitment_pipeline_data,
        'team2_staff_status_updates_data': team2_staff_status_updates_data,
        'team2_salary_pending_data': team2_salary_pending_data,
        'team2_police_verification_data': team2_police_verification_data,
        'team2_interview_schedule_data': team2_interview_schedule_data,
        'team2_exit_information_data': team2_exit_information_data,
        'team2_issues_staff_concerns_data': team2_issues_staff_concerns_data,
        'team2_kural_recitation_data': team2_kural_recitation_data,
        'team2_front_office_phone_calls_data': team2_front_office_phone_calls_data,
        'team2_visitor_log_data': team2_visitor_log_data,
        'team2_bsnl_phone_status_data': team2_bsnl_phone_status_data,
        'team2_materials_inward_data': team2_materials_inward_data,
        'team2_materials_outward_data': team2_materials_outward_data,
        'team2_materials_movement_data': team2_materials_movement_data,
        'team2_returnable_material_tracking_data': team2_returnable_material_tracking_data,
        'team2_returnable_goods_report_data': team2_returnable_goods_report_data,
        'team2_campus_camera_status_data': team2_campus_camera_status_data,
        'team2_vehicle_camera_status_data': team2_vehicle_camera_status_data,
        'team2_bus_ac_camera_status_data': team2_bus_ac_camera_status_data,
        'team2_gps_monitoring_data': team2_gps_monitoring_data,
        'team2_issues_identified_monitoring_data': team2_issues_identified_monitoring_data,
        'team2_teachers_late_reporting_data': team2_teachers_late_reporting_data,
        'team2_water_tds_deviation_data': team2_water_tds_deviation_data,
        'team2_testing_cleaning_data': team2_testing_cleaning_data,
        'team2_water_level_data': team2_water_level_data,
        'team2_housekeeping_general_data': team2_housekeeping_general_data,
        'team2_pool_testing_data': team2_pool_testing_data,
        'team2_washroom_cleanliness_data': team2_washroom_cleanliness_data,
        'team2_transport_attendance_data': team2_transport_attendance_data,
        'team2_ac_working_status_data': team2_ac_working_status_data,
        'team2_late_reporting_data': team2_late_reporting_data,
        'team2_maintenance_service_issues_data': team2_maintenance_service_issues_data,
        'team2_car_maintenance_cleaning_data': team2_car_maintenance_cleaning_data,
        'team2_vehicle_renewals_delays_data': team2_vehicle_renewals_delays_data,
        'team2_special_trip_data': team2_special_trip_data,
        'team2_parent_concern_detail_data': team2_parent_concern_detail_data,
        'team2_ac_temperature_data': team2_ac_temperature_data,
        'team2_maintenance_labor_data': team2_maintenance_labor_data,
        'team2_motor_data': team2_motor_data,
        'team2_pest_control_data': team2_pest_control_data,
        'team2_ac_temp_deviation_data': team2_ac_temp_deviation_data,
        'team2_electricity_consumption_data': team2_electricity_consumption_data,
        'team2_eb_details_data': team2_eb_details_data,
        'team2_solar_details_data': team2_solar_details_data,
        'team2_genset_details_data': team2_genset_details_data,
        'team2_count_verification_data': team2_count_verification_data,
        'team2_attendance_replacement_data': team2_attendance_replacement_data,
        'team2_security_info_note_data': team2_security_info_note_data,
        'team2_security_govt_inout_data': team2_security_govt_inout_data,
        'team2_alcohol_test_data': team2_alcohol_test_data,
        'team2_security_materials_inward_data': team2_security_materials_inward_data,
        'team2_security_materials_outward_data': team2_security_materials_outward_data,
        'team2_transport_verification_data': team2_transport_verification_data,
        'team2_documents_movement_data': team2_documents_movement_data,
        'team2_govt_official_documents_data': team2_govt_official_documents_data,
        'team2_thoorigai_social_media_data': team2_thoorigai_social_media_data,
        'team2_website_updates_data': team2_website_updates_data,
        'team2_md_social_media_data': team2_md_social_media_data,
        'team2_intercom_maintenance_data': team2_intercom_maintenance_data,
        'team2_health_check_up_data': team2_health_check_up_data,
        'team2_net_connectivity_print_details_data': team2_net_connectivity_print_details_data,
        'team2_general_maintenance_it_data': team2_general_maintenance_it_data,
        'team2_calendar_schedule_data': team2_calendar_schedule_data,
        'team2_training_attendance_data': team2_training_attendance_data,
        'team2_training_details_data': team2_training_details_data,
        'team2_camera_footage_data': team2_camera_footage_data,
        'team2_manpower_planning_data': team2_manpower_planning_data,
        'team2_overall_consolidation_data': team2_overall_consolidation_data,
        'team2_uniform_details_data': team2_uniform_details_data,
        'team2_dept_wise_uniform_details_data': team2_dept_wise_uniform_details_data,
        'team2_biometrics_access_card_punching_data': team2_biometrics_access_card_punching_data,
    }

def get_empty_team2_data():
    return {
        'team2_hr_attendance_data': [],
        'team2_total_hr_attendance_data': [],
        'team2_admin_attendance_data': [],
        'team2_recruitment_activity_data': [],
        'team2_pending_recruitment_data': [],
        'team2_recruitment_pipeline_data': [],
        'team2_staff_status_updates_data': [],
        'team2_salary_pending_data': [],
        'team2_police_verification_data': [],
        'team2_interview_schedule_data': [],
        'team2_exit_information_data': [],
        'team2_issues_staff_concerns_data': [],
        'team2_kural_recitation_data': [],
        'team2_front_office_phone_calls_data': [],
        'team2_visitor_log_data': [],
        'team2_bsnl_phone_status_data': [],
        'team2_materials_inward_data': [],
        'team2_materials_outward_data': [],
        'team2_materials_movement_data': [],
        'team2_returnable_material_tracking_data': [],
        'team2_returnable_goods_report_data': [],
        'team2_campus_camera_status_data': [],
        'team2_vehicle_camera_status_data': [],
        'team2_bus_ac_camera_status_data': [],
        'team2_gps_monitoring_data': [],
        'team2_issues_identified_monitoring_data': [],
        'team2_teachers_late_reporting_data': [],
        'team2_water_tds_deviation_data': [],
        'team2_testing_cleaning_data': [],
        'team2_water_level_data': [],
        'team2_housekeeping_general_data': [],
        'team2_pool_testing_data': [],
        'team2_washroom_cleanliness_data': [],
        'team2_transport_attendance_data': [],
        'team2_ac_working_status_data': [],
        'team2_late_reporting_data': [],
        'team2_maintenance_service_issues_data': [],
        'team2_car_maintenance_cleaning_data': [],
        'team2_vehicle_renewals_delays_data': [],
        'team2_special_trip_data': [],
        'team2_parent_concern_detail_data': [],
        'team2_ac_temperature_data': [],
        'team2_maintenance_labor_data': [],
        'team2_motor_data': [],
        'team2_pest_control_data': [],
        'team2_ac_temp_deviation_data': [],
        'team2_electricity_consumption_data': [],
        'team2_eb_details_data': [],
        'team2_solar_details_data': [],
        'team2_genset_details_data': [],
        'team2_count_verification_data': [],
        'team2_attendance_replacement_data': [],
        'team2_security_info_note_data': [],
        'team2_security_govt_inout_data': [],
        'team2_alcohol_test_data': [],
        'team2_security_materials_inward_data': [],
        'team2_security_materials_outward_data': [],
        'team2_transport_verification_data': [],
        'team2_documents_movement_data': [],
        'team2_govt_official_documents_data': [],
        'team2_thoorigai_social_media_data': [],
        'team2_website_updates_data': [],
        'team2_md_social_media_data': [],
        'team2_intercom_maintenance_data': [],
        'team2_health_check_up_data': [],
        'team2_net_connectivity_print_details_data': [],
        'team2_general_maintenance_it_data': [],
        'team2_calendar_schedule_data': [],
        'team2_training_attendance_data': [],
        'team2_training_details_data': [],
        'team2_camera_footage_data': [],
        'team2_manpower_planning_data': [],
        'team2_overall_consolidation_data': [],
        'team2_uniform_details_data': [],
        'team2_dept_wise_uniform_details_data': [],
        'team2_biometrics_access_card_punching_data': [],
    }
