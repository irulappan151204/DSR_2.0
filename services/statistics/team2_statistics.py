from models import (
    Team2HRAttendance,
    Team2AdminAttendance,
    Team2RecruitmentActivity,
    Team2PendingRecruitment,
    Team2RecruitmentPipeline,
    Team2StaffStatusUpdates,
    Team2SalaryPending,
    Team2PoliceVerification,
    Team2InterviewSchedule,
    Team2ExitInformation,
    Team2IssuesStaffConcerns,
    Team2KuralRecitation,
    Team2FrontOfficePhoneCalls,
    Team2VisitorLog,
    Team2BSNLPhoneStatus,
    Team2MaterialsInward,
    Team2MaterialsOutward,
    Team2MaterialsMovement,
    Team2ReturnableMaterialTracking,
    Team2ReturnableGoodsReport,
    Team2WaterTDSDeviation,
    Team2TestingCleaning,
    Team2PoolTesting,
    Team2WaterLevel,
    Team2WashroomCleanliness,
    Team2TransportAttendance,
    Team2ACWorkingStatus,
    Team2LateReporting,
    Team2MaintenanceServiceIssues,
    Team2CarMaintenanceCleaning,
    Team2VehicleRenewalsDelays,
    Team2SpecialTrip,
    Team2ACTemperatureCheck,
    Team2LaborEbSolarGenset,
    Team2Motor,
    Team2PestControl,
    Team2ACTempDeviation,
    Team2ElectricityConsumption,
    Team2EBDetails,
    Team2SolarDetails,
    Team2GensetDetails,
    Team2CountVerification,
    Team2AttendanceReplacement,
    Team2SecurityInfoNote,
    Team2SecurityGovtInout,
    Team2AlcoholTest,
    Team2SecurityMaterialsInout,
    Team2SecurityMaterialsOutward,
    Team2TransportVerification,
    Team2DocumentsMovement,
    Team2GovtOfficialDocuments,
    Team2ThoorigaiTeamSocialMedia,
    Team2WebsiteUpdates,
    Team2MDSocialMedia,
    Team2IntercomMaintenance,
    Team2HealthCheckUp,
    Team2NetConnectivityPrintDetails,
    Team2GeneralMaintenanceITProducts,
    Team2CalendarSchedule,
    Team2TrainingAttendance,
    Team2TrainingDetails,
    Team2BiometricsAccessCardPunching,
    Team2CampusCameraStatus,
    Team2VehicleCameraStatus,
    Team2BusACCameraStatus,
    Team2GPSMonitoring,
    Team2IssuesIdentifiedMonitoring,
    Team2IssuesIdentifiedControlRoom
)

TEAM2_MODELS = [
    Team2HRAttendance,
    Team2AdminAttendance,
    Team2RecruitmentActivity,
    Team2PendingRecruitment,
    Team2RecruitmentPipeline,
    Team2StaffStatusUpdates,
    Team2SalaryPending,
    Team2PoliceVerification,
    Team2InterviewSchedule,
    Team2ExitInformation,
    Team2IssuesStaffConcerns,
    Team2KuralRecitation,
    Team2FrontOfficePhoneCalls,
    Team2VisitorLog,
    Team2BSNLPhoneStatus,
    Team2MaterialsInward,
    Team2MaterialsOutward,
    Team2MaterialsMovement,
    Team2ReturnableMaterialTracking,
    Team2ReturnableGoodsReport,
    Team2WaterTDSDeviation,
    Team2TestingCleaning,
    Team2PoolTesting,
    Team2WaterLevel,
    Team2WashroomCleanliness,
    Team2TransportAttendance,
    Team2ACWorkingStatus,
    Team2LateReporting,
    Team2MaintenanceServiceIssues,
    Team2CarMaintenanceCleaning,
    Team2VehicleRenewalsDelays,
    Team2SpecialTrip,
    Team2ACTemperatureCheck,
    Team2LaborEbSolarGenset,
    Team2Motor,
    Team2PestControl,
    Team2ACTempDeviation,
    Team2ElectricityConsumption,
    Team2EBDetails,
    Team2SolarDetails,
    Team2GensetDetails,
    Team2CountVerification,
    Team2AttendanceReplacement,
    Team2SecurityInfoNote,
    Team2SecurityGovtInout,
    Team2AlcoholTest,
    Team2SecurityMaterialsInout,
    Team2SecurityMaterialsOutward,
    Team2TransportVerification,
    Team2DocumentsMovement,
    Team2GovtOfficialDocuments,
    Team2ThoorigaiTeamSocialMedia,
    Team2WebsiteUpdates,
    Team2MDSocialMedia,
    Team2IntercomMaintenance,
    Team2HealthCheckUp,
    Team2NetConnectivityPrintDetails,
    Team2GeneralMaintenanceITProducts,
    Team2CalendarSchedule,
    Team2TrainingAttendance,
    Team2TrainingDetails,
    Team2BiometricsAccessCardPunching,
    Team2CampusCameraStatus,
    Team2VehicleCameraStatus,
    Team2BusACCameraStatus,
    Team2GPSMonitoring,
    Team2IssuesIdentifiedMonitoring,
    Team2IssuesIdentifiedControlRoom
]

def get_initial_team2_issue_nature():
    return {
    'jr_school': {'all_well': 0, 'manageable': 0, 'critical': 0},
    'sr_school': {'all_well': 0, 'manageable': 0, 'critical': 0},
    'eca': {'all_well': 0, 'manageable': 0, 'critical': 0}, 
    'admin_staff': {'all_well': 0, 'manageable': 0, 'critical': 0},
    'drivers': {'all_well': 0, 'manageable': 0, 'critical': 0},
    'security': {'all_well': 0, 'manageable': 0, 'critical': 0},
    'housekeeping': {'all_well': 0, 'manageable': 0, 'critical': 0},
    'conductors': {'all_well': 0, 'manageable': 0, 'critical': 0},
    'hr_overall': {'all_well': 0, 'manageable': 0, 'critical': 0},
    'recruitment_academic': {'all_well': 0, 'manageable': 0, 'critical': 0},
    'recruitment_admin': {'all_well': 0, 'manageable': 0, 'critical': 0},
    'pending_academic': {'all_well': 0, 'manageable': 0, 'critical': 0},
    'pending_admin': {'all_well': 0, 'manageable': 0, 'critical': 0},   
    'interview_schedule': {'all_well': 0, 'manageable': 0, 'critical': 0},
    'exit_information': {'all_well': 0, 'manageable': 0, 'critical': 0},
    'issues_staff_concerns': {'all_well': 0, 'manageable': 0, 'critical': 0},
    'kural_recitation': {'all_well': 0, 'manageable': 0, 'critical': 0},
    'front_office_phone_calls_academics': {'all_well': 0, 'manageable': 0, 'critical': 0},
    'front_office_phone_calls_admin': {'all_well': 0, 'manageable': 0, 'critical': 0},
    'front_office_phone_calls_general': {'all_well': 0, 'manageable': 0, 'critical': 0},
    'visitor_log': {'all_well': 0, 'manageable': 0, 'critical': 0},
    'bsnl_phone_status': {'all_well': 0, 'manageable': 0, 'critical': 0},
    'materials_inward': {'all_well': 0, 'manageable': 0, 'critical': 0},
    'materials_outward': {'all_well': 0, 'manageable': 0, 'critical': 0},
    'materials_movement': {'all_well': 0, 'manageable': 0, 'critical': 0},
    'returnable_material_tracking': {'all_well': 0, 'manageable': 0, 'critical': 0},
    'returnable_goods_report': {'all_well': 0, 'manageable': 0, 'critical': 0},
    'campus_camera_status': {'all_well': 0, 'manageable': 0, 'critical': 0},
    'vehicle_camera_status': {'all_well': 0, 'manageable': 0, 'critical': 0},
    'bus_ac_camera_status': {'all_well': 0, 'manageable': 0, 'critical': 0},
    'gps_monitoring': {'all_well': 0, 'manageable': 0, 'critical': 0},
    'issues_identified_monitoring': {'all_well': 0, 'manageable': 0, 'critical': 0},
    'teachers_late_reporting': {'all_well': 0, 'manageable': 0, 'critical': 0},
    'biometrics_access_card_punching': {'all_well': 0, 'manageable': 0, 'critical': 0},
    'water_tds_deviation': {'all_well': 0, 'manageable': 0, 'critical': 0},
    'testing_cleaning_general': {'all_well': 0, 'manageable': 0, 'critical': 0},
    'testing_cleaning_pool': {'all_well': 0, 'manageable': 0, 'critical': 0},
    'water_level_checking': {'all_well': 0, 'manageable': 0, 'critical': 0},
    'washroom_cleanliness': {'all_well': 0, 'manageable': 0, 'critical': 0},
    'transport_attendance': {'all_well': 0, 'manageable': 0, 'critical': 0},
    'transport_ac_status': {'all_well': 0, 'manageable': 0, 'critical': 0},
    'late_reporting': {'all_well': 0, 'manageable': 0, 'critical': 0},
    'maintenance_service_issues': {'all_well': 0, 'manageable': 0, 'critical': 0},
    'car_maintenance_cleaning': {'all_well': 0, 'manageable': 0, 'critical': 0},
    'vehicle_renewals_delays': {'all_well': 0, 'manageable': 0, 'critical': 0},
    'delayed_halt': {'all_well': 0, 'manageable': 0, 'critical': 0},
    'fc_renewal': {'all_well': 0, 'manageable': 0, 'critical': 0},
    'road_tax': {'all_well': 0, 'manageable': 0, 'critical': 0},
    'permit': {'all_well': 0, 'manageable': 0, 'critical': 0},
    'insurance': {'all_well': 0, 'manageable': 0, 'critical': 0},
    'special_trip': {'all_well': 0, 'manageable': 0, 'critical': 0},
    'ac_temp_first_floor': {'all_well': 0, 'manageable': 0, 'critical': 0},
    'ac_temp_second_floor': {'all_well': 0, 'manageable': 0, 'critical': 0},
    'ac_temp_third_floor': {'all_well': 0, 'manageable': 0, 'critical': 0},
    'ac_temp_ground_floor': {'all_well': 0, 'manageable': 0, 'critical': 0},
    'maintenance_labor': {'all_well': 0, 'manageable': 0, 'critical': 0},
    'motor': {'all_well': 0, 'manageable': 0, 'critical': 0},
    'pest_control': {'all_well': 0, 'manageable': 0, 'critical': 0},
    'ac_temp_deviation': {'all_well': 0, 'manageable': 0, 'critical': 0},
    'electricity_consumption': {'all_well': 0, 'manageable': 0, 'critical': 0},
    'eb_details': {'all_well': 0, 'manageable': 0, 'critical': 0},
    'solar_details': {'all_well': 0, 'manageable': 0, 'critical': 0},
    'genset_details': {'all_well': 0, 'manageable': 0, 'critical': 0},      
    'security_count_verification': {'all_well': 0, 'manageable': 0, 'critical': 0},
    'security_attendance_replacement': {'all_well': 0, 'manageable': 0, 'critical': 0},
    'security_info_note': {'all_well': 0, 'manageable': 0, 'critical': 0},
    'govt_officials_inout': {'all_well': 0, 'manageable': 0, 'critical': 0},
    'security_materials_inward': {'all_well': 0, 'manageable': 0, 'critical': 0},
    'security_materials_outward': {'all_well': 0, 'manageable': 0, 'critical': 0},
    'security_transport_verification': {'all_well': 0, 'manageable': 0, 'critical': 0},
    'documents_movement': {'all_well': 0, 'manageable': 0, 'critical': 0},
    'govt_official_documents': {'all_well': 0, 'manageable': 0, 'critical': 0},
    'digital_marketing_thoorigai_social_media': {'all_well': 0, 'manageable': 0, 'critical': 0},
    'digital_marketing_thoorigai_website_updates': {'all_well': 0, 'manageable': 0, 'critical': 0},
    'digital_marketing_md_social_media': {'all_well': 0, 'manageable': 0, 'critical': 0},
    'intercom_maintenance': {'all_well': 0, 'manageable': 0, 'critical': 0},
    'health_check_up': {'all_well': 0, 'manageable': 0, 'critical': 0},
    'net_connectivity_print_details': {'all_well': 0, 'manageable': 0, 'critical': 0},
    'general_maintenance_it_products': {'all_well': 0, 'manageable': 0, 'critical': 0},
    'calendar_schedule_admin': {'all_well': 0, 'manageable': 0, 'critical': 0},
    'calendar_schedule_house_keeping': {'all_well': 0, 'manageable': 0, 'critical': 0},
    'calendar_schedule_security': {'all_well': 0, 'manageable': 0, 'critical': 0},
    'calendar_schedule_transport': {'all_well': 0, 'manageable': 0, 'critical': 0},
    'training_attendance_academics_jr': {'all_well': 0, 'manageable': 0, 'critical': 0},
    'training_attendance_academics_sr': {'all_well': 0, 'manageable': 0, 'critical': 0},
    'training_attendance_admin': {'all_well': 0, 'manageable': 0, 'critical': 0},
    'training_attendance_drivers': {'all_well': 0, 'manageable': 0, 'critical': 0},
    'training_attendance_securities': {'all_well': 0, 'manageable': 0, 'critical': 0},
    'training_attendance_drivers_sub': {'all_well': 0, 'manageable': 0, 'critical': 0},
    'training_attendance_conductors': {'all_well': 0, 'manageable': 0, 'critical': 0},
    'training_details_cbse_cis_external': {'all_well': 0, 'manageable': 0, 'critical': 0},
    'overall': {'all_well': 0, 'manageable': 0, 'critical': 0}
}


def populate_team2_issue_nature(team2, date_filter_fn):
    team2_issue_nature = get_initial_team2_issue_nature()
    if not team2:
        return team2_issue_nature

    # Get Team 2 HR Attendance data
    query_filters = [Team2HRAttendance.team_id == team2.team_id] + date_filter_fn(Team2HRAttendance)
    hr_data = Team2HRAttendance.query.filter(*query_filters).all()
    
    for item in hr_data:
        # Process Jr. School data
        if item.hr_att_jr_school_nature:
            nature = item.hr_att_jr_school_nature.lower()
            if ('all_well' in nature or 'all well' in nature):
                team2_issue_nature['jr_school']['all_well'] += 1
                team2_issue_nature['overall']['all_well'] += 1
            elif ('manageable' in nature):
                team2_issue_nature['jr_school']['manageable'] += 1
                team2_issue_nature['overall']['manageable'] += 1
            elif ('critical' in nature):
                team2_issue_nature['jr_school']['critical'] += 1
                team2_issue_nature['overall']['critical'] += 1
        
        # Process Sr. School data
        if item.hr_att_sr_school_nature:
            nature = item.hr_att_sr_school_nature.lower()
            if ('all_well' in nature or 'all well' in nature):
                team2_issue_nature['sr_school']['all_well'] += 1
                team2_issue_nature['overall']['all_well'] += 1
            elif ('manageable' in nature):
                team2_issue_nature['sr_school']['manageable'] += 1
                team2_issue_nature['overall']['manageable'] += 1
            elif ('critical' in nature):
                team2_issue_nature['sr_school']['critical'] += 1
                team2_issue_nature['overall']['critical'] += 1
        
        # Process ECA data
        if item.hr_att_eca_nature:
            nature = item.hr_att_eca_nature.lower()
            if ('all_well' in nature or 'all well' in nature):
                team2_issue_nature['eca']['all_well'] += 1
                team2_issue_nature['overall']['all_well'] += 1
            elif ('manageable' in nature):
                team2_issue_nature['eca']['manageable'] += 1
                team2_issue_nature['overall']['manageable'] += 1
            elif ('critical' in nature):
                team2_issue_nature['eca']['critical'] += 1
                team2_issue_nature['overall']['critical'] += 1
    
    # Get Team 2 Admin Attendance data
    query_filters = [Team2AdminAttendance.team_id == team2.team_id] + date_filter_fn(Team2AdminAttendance)
    admin_data = Team2AdminAttendance.query.filter(*query_filters).all()
    
    for item in admin_data:
        # Process Admin Staff data
        if item.hr_att_admin_nature:
            nature = item.hr_att_admin_nature.lower()
            if ('all_well' in nature or 'all well' in nature):
                team2_issue_nature['admin_staff']['all_well'] += 1
                team2_issue_nature['overall']['all_well'] += 1
            elif ('manageable' in nature):
                team2_issue_nature['admin_staff']['manageable'] += 1
                team2_issue_nature['overall']['manageable'] += 1
            elif ('critical' in nature):
                team2_issue_nature['admin_staff']['critical'] += 1
                team2_issue_nature['overall']['critical'] += 1
        
        # Process Drivers data
        if item.hr_att_drivers_nature:
            nature = item.hr_att_drivers_nature.lower()
            if ('all_well' in nature or 'all well' in nature):
                team2_issue_nature['drivers']['all_well'] += 1
                team2_issue_nature['overall']['all_well'] += 1
            elif ('manageable' in nature):
                team2_issue_nature['drivers']['manageable'] += 1
                team2_issue_nature['overall']['manageable'] += 1
            elif ('critical' in nature):
                team2_issue_nature['drivers']['critical'] += 1
                team2_issue_nature['overall']['critical'] += 1
        
        # Process Security data
        if item.hr_att_sec_nature:
            nature = item.hr_att_sec_nature.lower()
            if ('all_well' in nature or 'all well' in nature):
                team2_issue_nature['security']['all_well'] += 1
                team2_issue_nature['overall']['all_well'] += 1
            elif ('manageable' in nature):
                team2_issue_nature['security']['manageable'] += 1
                team2_issue_nature['overall']['manageable'] += 1
            elif ('critical' in nature):
                team2_issue_nature['security']['critical'] += 1
                team2_issue_nature['overall']['critical'] += 1
        
        # Process Housekeeping data
        if item.hr_att_hk_nature:
            nature = item.hr_att_hk_nature.lower()
            if ('all_well' in nature or 'all well' in nature):
                team2_issue_nature['housekeeping']['all_well'] += 1
                team2_issue_nature['overall']['all_well'] += 1
            elif ('manageable' in nature):
                team2_issue_nature['housekeeping']['manageable'] += 1
                team2_issue_nature['overall']['manageable'] += 1
            elif ('critical' in nature):
                team2_issue_nature['housekeeping']['critical'] += 1
                team2_issue_nature['overall']['critical'] += 1
        
        # Process Conductors data
        if item.hr_att_cond_nature:
            nature = item.hr_att_cond_nature.lower()
            if ('all_well' in nature or 'all well' in nature):
                team2_issue_nature['conductors']['all_well'] += 1
                team2_issue_nature['overall']['all_well'] += 1
            elif ('manageable' in nature):
                team2_issue_nature['conductors']['manageable'] += 1
                team2_issue_nature['overall']['manageable'] += 1
            elif ('critical' in nature):
                team2_issue_nature['conductors']['critical'] += 1
                team2_issue_nature['overall']['critical'] += 1

    # Compute HR Overall after HR/Admin attendance sections
    team2_issue_nature['hr_overall']['all_well'] = (
        team2_issue_nature['jr_school']['all_well'] + team2_issue_nature['sr_school']['all_well'] +
        team2_issue_nature['eca']['all_well'] + team2_issue_nature['admin_staff']['all_well'] +
        team2_issue_nature['drivers']['all_well'] + team2_issue_nature['security']['all_well'] +
        team2_issue_nature['housekeeping']['all_well'] + team2_issue_nature['conductors']['all_well']
    )
    team2_issue_nature['hr_overall']['manageable'] = (
        team2_issue_nature['jr_school']['manageable'] + team2_issue_nature['sr_school']['manageable'] +
        team2_issue_nature['eca']['manageable'] + team2_issue_nature['admin_staff']['manageable'] +
        team2_issue_nature['drivers']['manageable'] + team2_issue_nature['security']['manageable'] +
        team2_issue_nature['housekeeping']['manageable'] + team2_issue_nature['conductors']['manageable']
    )
    team2_issue_nature['hr_overall']['critical'] = (
        team2_issue_nature['jr_school']['critical'] + team2_issue_nature['sr_school']['critical'] +
        team2_issue_nature['eca']['critical'] + team2_issue_nature['admin_staff']['critical'] +
        team2_issue_nature['drivers']['critical'] + team2_issue_nature['security']['critical'] +
        team2_issue_nature['housekeeping']['critical'] + team2_issue_nature['conductors']['critical']
    )

    # Get Team 2 Recruitment Activity data
    query_filters = [Team2RecruitmentActivity.team_id == team2.team_id] + date_filter_fn(Team2RecruitmentActivity)
    rec_data = Team2RecruitmentActivity.query.filter(*query_filters).all()
    
    for item in rec_data:
        # Process Academic Recruitment data
        if item.rec_act_acad_nature:
            nature = item.rec_act_acad_nature.lower()
            if ('all_well' in nature or 'all well' in nature):
                team2_issue_nature['recruitment_academic']['all_well'] += 1
                team2_issue_nature['overall']['all_well'] += 1
            elif ('manageable' in nature):
                team2_issue_nature['recruitment_academic']['manageable'] += 1
                team2_issue_nature['overall']['manageable'] += 1
            elif ('critical' in nature):
                team2_issue_nature['recruitment_academic']['critical'] += 1
                team2_issue_nature['overall']['critical'] += 1
        
        # Process Admin Recruitment data
        if item.rec_act_admin_nature:
            nature = item.rec_act_admin_nature.lower()
            if ('all_well' in nature or 'all well' in nature):
                team2_issue_nature['recruitment_admin']['all_well'] += 1
                team2_issue_nature['overall']['all_well'] += 1
            elif ('manageable' in nature):
                team2_issue_nature['recruitment_admin']['manageable'] += 1
                team2_issue_nature['overall']['manageable'] += 1
            elif ('critical' in nature):
                team2_issue_nature['recruitment_admin']['critical'] += 1
                team2_issue_nature['overall']['critical'] += 1

    # Get Team 2 Pending Recruitment data
    query_filters = [Team2PendingRecruitment.team_id == team2.team_id] + date_filter_fn(Team2PendingRecruitment)
    pending_data = Team2PendingRecruitment.query.filter(*query_filters).all()
    
    for item in pending_data:
        # Process Academic Pending data
        if item.rec_pend_acad_nature:
            nature = item.rec_pend_acad_nature.lower()
            if ('all_well' in nature or 'all well' in nature):
                team2_issue_nature['pending_academic']['all_well'] += 1
                team2_issue_nature['overall']['all_well'] += 1
            elif ('manageable' in nature):
                team2_issue_nature['pending_academic']['manageable'] += 1
                team2_issue_nature['overall']['manageable'] += 1
            elif ('critical' in nature):
                team2_issue_nature['pending_academic']['critical'] += 1
                team2_issue_nature['overall']['critical'] += 1
        
        # Process Admin Pending data
        if item.rec_pend_admin_nature:
            nature = item.rec_pend_admin_nature.lower()
            if ('all_well' in nature or 'all well' in nature):
                team2_issue_nature['pending_admin']['all_well'] += 1
                team2_issue_nature['overall']['all_well'] += 1
            elif ('manageable' in nature):
                team2_issue_nature['pending_admin']['manageable'] += 1
                team2_issue_nature['overall']['manageable'] += 1
            elif ('critical' in nature):
                team2_issue_nature['pending_admin']['critical'] += 1
                team2_issue_nature['overall']['critical'] += 1

    # Get Team 2 Interview Schedule data
    query_filters = [Team2InterviewSchedule.team_id == team2.team_id] + date_filter_fn(Team2InterviewSchedule)
    interview_data = Team2InterviewSchedule.query.filter(*query_filters).all()
    
    for item in interview_data:
        # Process Interview Schedule data - using the correct field name
        if item.nature_of_issue:
            nature = item.nature_of_issue.lower()
            if ('all_well' in nature or 'all well' in nature):
                team2_issue_nature['interview_schedule']['all_well'] += 1
                team2_issue_nature['overall']['all_well'] += 1
            elif ('manageable' in nature):
                team2_issue_nature['interview_schedule']['manageable'] += 1
                team2_issue_nature['overall']['manageable'] += 1
            elif ('critical' in nature):
                team2_issue_nature['interview_schedule']['critical'] += 1
                team2_issue_nature['overall']['critical'] += 1  

     # Get Team 2  Exit Information data
    query_filters = [Team2ExitInformation.team_id == team2.team_id] + date_filter_fn(Team2ExitInformation)
    exit_information_data = Team2ExitInformation.query.filter(*query_filters).all()
    
    for item in exit_information_data:
        # Process Exit Information data - using the correct field name
        if item.exit_nature:
            nature = item.exit_nature.lower()
            if ('all_well' in nature or 'all well' in nature):
                team2_issue_nature['exit_information']['all_well'] += 1
                team2_issue_nature['overall']['all_well'] += 1
            elif ('manageable' in nature):
                team2_issue_nature['exit_information']['manageable'] += 1
                team2_issue_nature['overall']['manageable'] += 1
            elif ('critical' in nature):
                team2_issue_nature['exit_information']['critical'] += 1
                team2_issue_nature['overall']['critical'] += 1

    # Get Team 2  5a Issues / Staff Concerns
    query_filters = [Team2IssuesStaffConcerns.team_id == team2.team_id] + date_filter_fn(Team2IssuesStaffConcerns)
    issues_staff_concerns_data = Team2IssuesStaffConcerns.query.filter(*query_filters).all()

    for item in issues_staff_concerns_data:
        # Single concern nature field in current schema
        if item.concern_nature:
            nature = item.concern_nature.lower()
            if ('all_well' in nature or 'all well' in nature):
                team2_issue_nature['issues_staff_concerns']['all_well'] += 1
                team2_issue_nature['overall']['all_well'] += 1
            elif ('manageable' in nature):
                team2_issue_nature['issues_staff_concerns']['manageable'] += 1
                team2_issue_nature['overall']['manageable'] += 1
            elif ('critical' in nature):
                team2_issue_nature['issues_staff_concerns']['critical'] += 1
                team2_issue_nature['overall']['critical'] += 1

    # Process Kural Recitation data
    query_filters = [Team2KuralRecitation.team_id == team2.team_id] + date_filter_fn(Team2KuralRecitation)
    kural_recitation_data = Team2KuralRecitation.query.filter(*query_filters).all()

    for item in kural_recitation_data:
        if item.kural_nature:
            nature = item.kural_nature.lower()
            if ('all_well' in nature or 'all well' in nature):
                team2_issue_nature['kural_recitation']['all_well'] += 1
                team2_issue_nature['overall']['all_well'] += 1
            elif ('manageable' in nature):
                team2_issue_nature['kural_recitation']['manageable'] += 1
                team2_issue_nature['overall']['manageable'] += 1
            elif ('critical' in nature):
                team2_issue_nature['kural_recitation']['critical'] += 1
                team2_issue_nature['overall']['critical'] += 1

    # Get Team 2- 6 


    # Process Front Office Phone Calls data
    query_filters = [Team2FrontOfficePhoneCalls.team_id == team2.team_id] + date_filter_fn(Team2FrontOfficePhoneCalls)
    front_office_phone_calls_data = Team2FrontOfficePhoneCalls.query.filter(*query_filters).all()

    for item in front_office_phone_calls_data:
        if item.nature:
            nature = item.nature.lower()
            category = item.category.lower()
            if ('all_well' in nature or 'all well' in nature):
                team2_issue_nature[f'front_office_phone_calls_{category}']['all_well'] += 1
                team2_issue_nature['overall']['all_well'] += 1
            elif ('manageable' in nature):
                team2_issue_nature[f'front_office_phone_calls_{category}']['manageable'] += 1
                team2_issue_nature['overall']['manageable'] += 1
            elif ('critical' in nature):
                team2_issue_nature[f'front_office_phone_calls_{category}']['critical'] += 1
                team2_issue_nature['overall']['critical'] += 1

    # Process Visitor Log data
    query_filters = [Team2VisitorLog.team_id == team2.team_id] + date_filter_fn(Team2VisitorLog)
    visitor_log_data = Team2VisitorLog.query.filter(*query_filters).all()

    for item in visitor_log_data:
        if item.nature:
            nature = item.nature.lower()
            if ('all_well' in nature or 'all well' in nature):
                team2_issue_nature['visitor_log']['all_well'] += 1
                team2_issue_nature['overall']['all_well'] += 1
            elif ('manageable' in nature):
                team2_issue_nature['visitor_log']['manageable'] += 1
                team2_issue_nature['overall']['manageable'] += 1
            elif ('critical' in nature):
                team2_issue_nature['visitor_log']['critical'] += 1
                team2_issue_nature['overall']['critical'] += 1

    # Process BSNL Phone Status data
    query_filters = [Team2BSNLPhoneStatus.team_id == team2.team_id] + date_filter_fn(Team2BSNLPhoneStatus)
    bsnl_phone_status_data = Team2BSNLPhoneStatus.query.filter(*query_filters).all()

    for item in bsnl_phone_status_data:
        if item.nature:
            nature = item.nature.lower()
            if ('all_well' in nature or 'all well' in nature):
                team2_issue_nature['bsnl_phone_status']['all_well'] += 1
                team2_issue_nature['overall']['all_well'] += 1
            elif ('manageable' in nature):
                team2_issue_nature['bsnl_phone_status']['manageable'] += 1
                team2_issue_nature['overall']['manageable'] += 1
            elif ('critical' in nature):
                team2_issue_nature['bsnl_phone_status']['critical'] += 1
                team2_issue_nature['overall']['critical'] += 1


        # team 2 7
    # Process Materials Inward data
    query_filters = [Team2MaterialsInward.team_id == team2.team_id] + date_filter_fn(Team2MaterialsInward)
    materials_inward_data = Team2MaterialsInward.query.filter(*query_filters).all()

    for item in materials_inward_data:
        if item.nature:
            nature = item.nature.lower()
            if ('all_well' in nature or 'all well' in nature):
                team2_issue_nature['materials_inward']['all_well'] += 1
                team2_issue_nature['overall']['all_well'] += 1
            elif ('manageable' in nature):
                team2_issue_nature['materials_inward']['manageable'] += 1
                team2_issue_nature['overall']['manageable'] += 1
            elif ('critical' in nature):
                team2_issue_nature['materials_inward']['critical'] += 1
                team2_issue_nature['overall']['critical'] += 1

    # Process Materials Outward data
    query_filters = [Team2MaterialsOutward.team_id == team2.team_id] + date_filter_fn(Team2MaterialsOutward)
    materials_outward_data = Team2MaterialsOutward.query.filter(*query_filters).all()

    for item in materials_outward_data:
        if item.nature:
            nature = item.nature.lower()
            if ('all_well' in nature or 'all well' in nature):
                team2_issue_nature['materials_outward']['all_well'] += 1
                team2_issue_nature['overall']['all_well'] += 1
            elif ('manageable' in nature):
                team2_issue_nature['materials_outward']['manageable'] += 1
                team2_issue_nature['overall']['manageable'] += 1
            elif ('critical' in nature):
                team2_issue_nature['materials_outward']['critical'] += 1
                team2_issue_nature['overall']['critical'] += 1

    # Process Materials Movement data
    query_filters = [Team2MaterialsMovement.team_id == team2.team_id] + date_filter_fn(Team2MaterialsMovement)
    materials_movement_data = Team2MaterialsMovement.query.filter(*query_filters).all()

    for item in materials_movement_data:
        if item.nature:
            nature = item.nature.lower()
            if ('all_well' in nature or 'all well' in nature):
                team2_issue_nature['materials_movement']['all_well'] += 1
                team2_issue_nature['overall']['all_well'] += 1
            elif ('manageable' in nature):
                team2_issue_nature['materials_movement']['manageable'] += 1
                team2_issue_nature['overall']['manageable'] += 1
            elif ('critical' in nature):
                team2_issue_nature['materials_movement']['critical'] += 1
                team2_issue_nature['overall']['critical'] += 1

    # Process Returnable Material Tracking data
    query_filters = [Team2ReturnableMaterialTracking.team_id == team2.team_id] + date_filter_fn(Team2ReturnableMaterialTracking)
    returnable_material_tracking_data = Team2ReturnableMaterialTracking.query.filter(*query_filters).all()

    for item in returnable_material_tracking_data:
        if item.nature:
            nature = item.nature.lower()
            if ('all_well' in nature or 'all well' in nature):
                team2_issue_nature['returnable_material_tracking']['all_well'] += 1
                team2_issue_nature['overall']['all_well'] += 1
            elif ('manageable' in nature):
                team2_issue_nature['returnable_material_tracking']['manageable'] += 1
                team2_issue_nature['overall']['manageable'] += 1
            elif ('critical' in nature):
                team2_issue_nature['returnable_material_tracking']['critical'] += 1
                team2_issue_nature['overall']['critical'] += 1

    # Process Returnable Goods Report data
    query_filters = [Team2ReturnableGoodsReport.team_id == team2.team_id] + date_filter_fn(Team2ReturnableGoodsReport)
    returnable_goods_report_data = Team2ReturnableGoodsReport.query.filter(*query_filters).all()

    for item in returnable_goods_report_data:
        if item.nature:
            nature = item.nature.lower()
            if ('all_well' in nature or 'all well' in nature):
                team2_issue_nature['returnable_goods_report']['all_well'] += 1
                team2_issue_nature['overall']['all_well'] += 1
            elif ('manageable' in nature):
                team2_issue_nature['returnable_goods_report']['manageable'] += 1
                team2_issue_nature['overall']['manageable'] += 1
            elif ('critical' in nature):
                team2_issue_nature['returnable_goods_report']['critical'] += 1
                team2_issue_nature['overall']['critical'] += 1

                # team 2 8
    # Process Campus Camera Status data
    query_filters = [Team2CampusCameraStatus.team_id == team2.team_id] + date_filter_fn(Team2CampusCameraStatus)
    campus_camera_status_data = Team2CampusCameraStatus.query.filter(*query_filters).all()

    for item in campus_camera_status_data:
        if item.nature_of_issue:
            nature = item.nature_of_issue.lower()
            if ('all_well' in nature or 'all well' in nature):
                team2_issue_nature['campus_camera_status']['all_well'] += 1
                team2_issue_nature['overall']['all_well'] += 1
            elif ('manageable' in nature):
                team2_issue_nature['campus_camera_status']['manageable'] += 1
                team2_issue_nature['overall']['manageable'] += 1
            elif ('critical' in nature):
                team2_issue_nature['campus_camera_status']['critical'] += 1
                team2_issue_nature['overall']['critical'] += 1

    # Process Vehicle Camera Status data
    query_filters = [Team2VehicleCameraStatus.team_id == team2.team_id] + date_filter_fn(Team2VehicleCameraStatus)
    vehicle_camera_status_data = Team2VehicleCameraStatus.query.filter(*query_filters).all()

    for item in vehicle_camera_status_data:
        if item.nature_of_issue:
            nature = item.nature_of_issue.lower()
            if ('all_well' in nature or 'all well' in nature):
                team2_issue_nature['vehicle_camera_status']['all_well'] += 1
                team2_issue_nature['overall']['all_well'] += 1
            elif ('manageable' in nature):
                team2_issue_nature['vehicle_camera_status']['manageable'] += 1
                team2_issue_nature['overall']['manageable'] += 1
            elif ('critical' in nature):
                team2_issue_nature['vehicle_camera_status']['critical'] += 1
                team2_issue_nature['overall']['critical'] += 1

    # Process Bus AC Camera Status data
    query_filters = [Team2BusACCameraStatus.team_id == team2.team_id] + date_filter_fn(Team2BusACCameraStatus)
    bus_ac_camera_status_data = Team2BusACCameraStatus.query.filter(*query_filters).all()

    for item in bus_ac_camera_status_data:
        if item.nature_of_issue:
            nature = item.nature_of_issue.lower()
            if ('all_well' in nature or 'all well' in nature):
                team2_issue_nature['bus_ac_camera_status']['all_well'] += 1
                team2_issue_nature['overall']['all_well'] += 1
            elif ('manageable' in nature):
                team2_issue_nature['bus_ac_camera_status']['manageable'] += 1
                team2_issue_nature['overall']['manageable'] += 1
            elif ('critical' in nature):
                team2_issue_nature['bus_ac_camera_status']['critical'] += 1
                team2_issue_nature['overall']['critical'] += 1

    # Process GPS Monitoring data
    query_filters = [Team2GPSMonitoring.team_id == team2.team_id] + date_filter_fn(Team2GPSMonitoring)
    gps_monitoring_data = Team2GPSMonitoring.query.filter(*query_filters).all()

    for item in gps_monitoring_data:
        if item.nature_of_issue:
            nature = item.nature_of_issue.lower()
            if ('all_well' in nature or 'all well' in nature):
                team2_issue_nature['gps_monitoring']['all_well'] += 1
                team2_issue_nature['overall']['all_well'] += 1
            elif ('manageable' in nature):
                team2_issue_nature['gps_monitoring']['manageable'] += 1
                team2_issue_nature['overall']['manageable'] += 1
            elif ('critical' in nature):
                team2_issue_nature['gps_monitoring']['critical'] += 1
                team2_issue_nature['overall']['critical'] += 1

    # Process Issues Identified Monitoring data
    query_filters = [Team2IssuesIdentifiedMonitoring.team_id == team2.team_id] + date_filter_fn(Team2IssuesIdentifiedMonitoring)
    issues_identified_monitoring_data = Team2IssuesIdentifiedMonitoring.query.filter(*query_filters).all()

    for item in issues_identified_monitoring_data:
        if item.nature_of_issue:
            nature = item.nature_of_issue.lower()
            if ('all_well' in nature or 'all well' in nature):
                team2_issue_nature['issues_identified_monitoring']['all_well'] += 1
                team2_issue_nature['overall']['all_well'] += 1
            elif ('manageable' in nature):
                team2_issue_nature['issues_identified_monitoring']['manageable'] += 1
                team2_issue_nature['overall']['manageable'] += 1
            elif ('critical' in nature):
                team2_issue_nature['issues_identified_monitoring']['critical'] += 1
                team2_issue_nature['overall']['critical'] += 1

    # Process Teachers Late Reporting data
    query_filters = [Team2IssuesIdentifiedControlRoom.team_id == team2.team_id] + date_filter_fn(Team2IssuesIdentifiedControlRoom)
    teachers_late_reporting_data = Team2IssuesIdentifiedControlRoom.query.filter(*query_filters).all()

    for item in teachers_late_reporting_data:
        if item.nature_of_issue:
            nature = item.nature_of_issue.lower()
            if ('all_well' in nature or 'all well' in nature):
                team2_issue_nature['teachers_late_reporting']['all_well'] += 1
                team2_issue_nature['overall']['all_well'] += 1
            elif ('manageable' in nature):
                team2_issue_nature['teachers_late_reporting']['manageable'] += 1
                team2_issue_nature['overall']['manageable'] += 1
            elif ('critical' in nature):
                team2_issue_nature['teachers_late_reporting']['critical'] += 1
                team2_issue_nature['overall']['critical'] += 1

    # Process Biometrics Access Card Punching data
    query_filters = [Team2BiometricsAccessCardPunching.team_id == team2.team_id] + date_filter_fn(Team2BiometricsAccessCardPunching)
    biometrics_data = Team2BiometricsAccessCardPunching.query.filter(*query_filters).all()

    for item in biometrics_data:
        if item.nature_of_issue:
            nature = item.nature_of_issue.lower()
            if ('all_well' in nature or 'all well' in nature):
                team2_issue_nature['biometrics_access_card_punching']['all_well'] += 1
                team2_issue_nature['overall']['all_well'] += 1
            elif ('manageable' in nature):
                team2_issue_nature['biometrics_access_card_punching']['manageable'] += 1
                team2_issue_nature['overall']['manageable'] += 1
            elif ('critical' in nature):
                team2_issue_nature['biometrics_access_card_punching']['critical'] += 1
                team2_issue_nature['overall']['critical'] += 1

    # Process Water TDS Deviation data
    query_filters = [Team2WaterTDSDeviation.team_id == team2.team_id] + date_filter_fn(Team2WaterTDSDeviation)
    water_tds_data = Team2WaterTDSDeviation.query.filter(*query_filters).all()

    for item in water_tds_data:
        if item.nature_of_issue:
            nature = item.nature_of_issue.lower()
            if ('all_well' in nature or 'all well' in nature):
                team2_issue_nature['water_tds_deviation']['all_well'] += 1
                team2_issue_nature['overall']['all_well'] += 1
            elif ('manageable' in nature):
                team2_issue_nature['water_tds_deviation']['manageable'] += 1
                team2_issue_nature['overall']['manageable'] += 1
            elif ('critical' in nature):
                team2_issue_nature['water_tds_deviation']['critical'] += 1
                team2_issue_nature['overall']['critical'] += 1

    # Process Testing & Cleaning data
    query_filters = [Team2TestingCleaning.team_id == team2.team_id] + date_filter_fn(Team2TestingCleaning)
    testing_cleaning_data = Team2TestingCleaning.query.filter(*query_filters).all()

    for item in testing_cleaning_data:
        if item.nature_of_issue:
            nature = item.nature_of_issue.lower()
            if ('all_well' in nature or 'all well' in nature):
                team2_issue_nature['testing_cleaning_general']['all_well'] += 1
                team2_issue_nature['overall']['all_well'] += 1
            elif ('manageable' in nature):
                team2_issue_nature['testing_cleaning_general']['manageable'] += 1
                team2_issue_nature['overall']['manageable'] += 1
            elif ('critical' in nature):
                team2_issue_nature['testing_cleaning_general']['critical'] += 1
                team2_issue_nature['overall']['critical'] += 1

    # Process Pool Testing data
    query_filters = [Team2PoolTesting.team_id == team2.team_id] + date_filter_fn(Team2PoolTesting)
    pool_testing_data = Team2PoolTesting.query.filter(*query_filters).all()
    # Process Water Level Checking
    query_filters = [Team2WaterLevel.team_id == team2.team_id] + date_filter_fn(Team2WaterLevel)
    water_level_data = Team2WaterLevel.query.filter(*query_filters).all()

    for item in water_level_data:
        if item.nature_of_issue:
            nature = item.nature_of_issue.lower()
            if ('all_well' in nature or 'all well' in nature):
                team2_issue_nature['water_level_checking']['all_well'] += 1
                team2_issue_nature['overall']['all_well'] += 1
            elif ('manageable' in nature):
                team2_issue_nature['water_level_checking']['manageable'] += 1
                team2_issue_nature['overall']['manageable'] += 1
            elif ('critical' in nature):
                team2_issue_nature['water_level_checking']['critical'] += 1
                team2_issue_nature['overall']['critical'] += 1

    # Process Washroom Cleanliness (derive from cleanliness field)
    query_filters = [Team2WashroomCleanliness.team_id == team2.team_id] + date_filter_fn(Team2WashroomCleanliness)
    washroom_data = Team2WashroomCleanliness.query.filter(*query_filters).all()

    for item in washroom_data:
        value = (getattr(item, 'cleanliness', None) or '').lower()
        if value:
            if ('all_well' in value or 'all well' in value):
                team2_issue_nature['washroom_cleanliness']['all_well'] += 1
                team2_issue_nature['overall']['all_well'] += 1
            elif 'manageable' in value:
                team2_issue_nature['washroom_cleanliness']['manageable'] += 1
                team2_issue_nature['overall']['manageable'] += 1
            elif 'critical' in value:
                team2_issue_nature['washroom_cleanliness']['critical'] += 1
                team2_issue_nature['overall']['critical'] += 1

    for item in pool_testing_data:
        if item.nature_of_issue:
            nature = item.nature_of_issue.lower()
            if ('all_well' in nature or 'all well' in nature):
                team2_issue_nature['testing_cleaning_pool']['all_well'] += 1
                team2_issue_nature['overall']['all_well'] += 1
            elif ('manageable' in nature):
                team2_issue_nature['testing_cleaning_pool']['manageable'] += 1
                team2_issue_nature['overall']['manageable'] += 1
            elif ('critical' in nature):
                team2_issue_nature['testing_cleaning_pool']['critical'] += 1
                team2_issue_nature['overall']['critical'] += 1

    # Team 2 - Section 13: Transport (12 sub-sections)
    # 1. Transport Attendance
    query_filters = [Team2TransportAttendance.team_id == team2.team_id] + date_filter_fn(Team2TransportAttendance)
    attendance_data = Team2TransportAttendance.query.filter(*query_filters).all()
    for item in attendance_data:
        if item.nature_of_issue:
            nature = item.nature_of_issue.lower()
            if ('all_well' in nature or 'all well' in nature):
                team2_issue_nature['transport_attendance']['all_well'] += 1
                team2_issue_nature['overall']['all_well'] += 1
            elif ('manageable' in nature):
                team2_issue_nature['transport_attendance']['manageable'] += 1
                team2_issue_nature['overall']['manageable'] += 1
            elif ('critical' in nature):
                team2_issue_nature['transport_attendance']['critical'] += 1
                team2_issue_nature['overall']['critical'] += 1

    # 2. Transport AC Status
    query_filters = [Team2ACWorkingStatus.team_id == team2.team_id] + date_filter_fn(Team2ACWorkingStatus)
    ac_status_data = Team2ACWorkingStatus.query.filter(*query_filters).all()
    for item in ac_status_data:
        if item.nature_of_issue:
            nature = item.nature_of_issue.lower()
            if ('all_well' in nature or 'all well' in nature):
                team2_issue_nature['transport_ac_status']['all_well'] += 1
                team2_issue_nature['overall']['all_well'] += 1
            elif ('manageable' in nature):
                team2_issue_nature['transport_ac_status']['manageable'] += 1
                team2_issue_nature['overall']['manageable'] += 1
            elif ('critical' in nature):
                team2_issue_nature['transport_ac_status']['critical'] += 1
                team2_issue_nature['overall']['critical'] += 1

    # 3. Late Reporting
    query_filters = [Team2LateReporting.team_id == team2.team_id] + date_filter_fn(Team2LateReporting)
    late_reporting_data = Team2LateReporting.query.filter(*query_filters).all()
    for item in late_reporting_data:
        if item.nature_of_issue:
            nature = item.nature_of_issue.lower()
            if ('all_well' in nature or 'all well' in nature):
                team2_issue_nature['late_reporting']['all_well'] += 1
                team2_issue_nature['overall']['all_well'] += 1
            elif ('manageable' in nature):
                team2_issue_nature['late_reporting']['manageable'] += 1
                team2_issue_nature['overall']['manageable'] += 1
            elif ('critical' in nature):
                team2_issue_nature['late_reporting']['critical'] += 1
                team2_issue_nature['overall']['critical'] += 1

    # 4. Maintenance / Service / Issues
    query_filters = [Team2MaintenanceServiceIssues.team_id == team2.team_id] + date_filter_fn(Team2MaintenanceServiceIssues)
    maintenance_service_data = Team2MaintenanceServiceIssues.query.filter(*query_filters).all()
    for item in maintenance_service_data:
        if item.nature_of_issue:
            nature = item.nature_of_issue.lower()
            if ('all_well' in nature or 'all well' in nature):
                team2_issue_nature['maintenance_service_issues']['all_well'] += 1
                team2_issue_nature['overall']['all_well'] += 1
            elif ('manageable' in nature):
                team2_issue_nature['maintenance_service_issues']['manageable'] += 1
                team2_issue_nature['overall']['manageable'] += 1
            elif ('critical' in nature):
                team2_issue_nature['maintenance_service_issues']['critical'] += 1
                team2_issue_nature['overall']['critical'] += 1

    # 5. Car Maintenance/Cleaning
    query_filters = [Team2CarMaintenanceCleaning.team_id == team2.team_id] + date_filter_fn(Team2CarMaintenanceCleaning)
    car_maintenance_data = Team2CarMaintenanceCleaning.query.filter(*query_filters).all()
    for item in car_maintenance_data:
        if item.nature_of_issue:
            nature = item.nature_of_issue.lower()
            if ('all_well' in nature or 'all well' in nature):
                team2_issue_nature['car_maintenance_cleaning']['all_well'] += 1
                team2_issue_nature['overall']['all_well'] += 1
            elif ('manageable' in nature):
                team2_issue_nature['car_maintenance_cleaning']['manageable'] += 1
                team2_issue_nature['overall']['manageable'] += 1
            elif ('critical' in nature):
                team2_issue_nature['car_maintenance_cleaning']['critical'] += 1
                team2_issue_nature['overall']['critical'] += 1

    # 6. Vehicle Renewals / Delays (with 5 subtypes)
    query_filters = [Team2VehicleRenewalsDelays.team_id == team2.team_id] + date_filter_fn(Team2VehicleRenewalsDelays)
    vehicle_renewals_data = Team2VehicleRenewalsDelays.query.filter(*query_filters).all()
    for item in vehicle_renewals_data:
        if item.particulars:
            key = None
            particulars = item.particulars.lower()
            if 'delayed halt' in particulars:
                key = 'delayed_halt'
            elif 'fc renewal' in particulars:
                key = 'fc_renewal'
            elif 'road tax' in particulars:
                key = 'road_tax'
            elif 'permit' in particulars:
                key = 'permit'
            elif 'insurance' in particulars:
                key = 'insurance'
            else:
                key = 'vehicle_renewals_delays'
            if item.nature_of_issue:
                nature = item.nature_of_issue.lower()
                if ('all_well' in nature or 'all well' in nature):
                    team2_issue_nature[key]['all_well'] += 1
                    team2_issue_nature['overall']['all_well'] += 1
                elif ('manageable' in nature):
                    team2_issue_nature[key]['manageable'] += 1
                    team2_issue_nature['overall']['manageable'] += 1
                elif ('critical' in nature):
                    team2_issue_nature[key]['critical'] += 1
                    team2_issue_nature['overall']['critical'] += 1

    # 7. Special Trip
    query_filters = [Team2SpecialTrip.team_id == team2.team_id] + date_filter_fn(Team2SpecialTrip)
    special_trip_data = Team2SpecialTrip.query.filter(*query_filters).all()
    for item in special_trip_data:
        if item.nature_of_issue:
            nature = item.nature_of_issue.lower()
            if ('all_well' in nature or 'all well' in nature):
                team2_issue_nature['special_trip']['all_well'] += 1
                team2_issue_nature['overall']['all_well'] += 1
            elif ('manageable' in nature):
                team2_issue_nature['special_trip']['manageable'] += 1
                team2_issue_nature['overall']['manageable'] += 1
            elif ('critical' in nature):
                team2_issue_nature['special_trip']['critical'] += 1
                team2_issue_nature['overall']['critical'] += 1

            
    # Team 2 Section 14: AC Temperature Check (by floor)
    query_filters = [Team2ACTemperatureCheck.team_id == team2.team_id] + date_filter_fn(Team2ACTemperatureCheck)
    ac_temp_data = Team2ACTemperatureCheck.query.filter(*query_filters).all()
    for item in ac_temp_data:
        # Floor mapping: 1=First, 2=Second, 3=Third, 4=Ground
        floor_map = {
            '1': 'ac_temp_first_floor',
            '2': 'ac_temp_second_floor',
            '3': 'ac_temp_third_floor',
            '4': 'ac_temp_ground_floor',
            'First Floor': 'ac_temp_first_floor',
            'Second Floor': 'ac_temp_second_floor',
            'Third Floor': 'ac_temp_third_floor',
            'Ground Floor': 'ac_temp_ground_floor',
        }
        floor_key = floor_map.get(str(item.floor).strip(), None)
        if floor_key and item.nature_of_issue:
            nature = item.nature_of_issue.lower()
            if ('all_well' in nature or 'all well' in nature):
                team2_issue_nature[floor_key]['all_well'] += 1
                team2_issue_nature['overall']['all_well'] += 1
            elif ('manageable' in nature):
                team2_issue_nature[floor_key]['manageable'] += 1
                team2_issue_nature['overall']['manageable'] += 1
            elif ('critical' in nature):
                team2_issue_nature[floor_key]['critical'] += 1
                team2_issue_nature['overall']['critical'] += 1

    # Team 2 Section 15: Labor, EB, Solar, Genset, Motor/Pest, AC Temp Deviation, Electricity Consumption
    # 15.1 Maintenance Labor
    query_filters = [Team2LaborEbSolarGenset.team_id == team2.team_id] + date_filter_fn(Team2LaborEbSolarGenset)
    labor_data = Team2LaborEbSolarGenset.query.filter(*query_filters).all()
    for item in labor_data:
        if item.nature_of_issue:
            nature = item.nature_of_issue.lower()
            if ('all_well' in nature or 'all well' in nature):
                team2_issue_nature['maintenance_labor']['all_well'] += 1
                team2_issue_nature['overall']['all_well'] += 1
            elif ('manageable' in nature):
                team2_issue_nature['maintenance_labor']['manageable'] += 1
                team2_issue_nature['overall']['manageable'] += 1
            elif ('critical' in nature):
                team2_issue_nature['maintenance_labor']['critical'] += 1
                team2_issue_nature['overall']['critical'] += 1

    # 15.2a Motor Control
    query_filters = [Team2Motor.team_id == team2.team_id] + date_filter_fn(Team2Motor)
    motor_data = Team2Motor.query.filter(*query_filters).all()
    for item in motor_data:
        if item.nature_of_issue:
            nature = item.nature_of_issue.lower()
            if ('all_well' in nature or 'all well' in nature):
                team2_issue_nature['motor']['all_well'] += 1
                team2_issue_nature['overall']['all_well'] += 1
            elif ('manageable' in nature):
                team2_issue_nature['motor']['manageable'] += 1
                team2_issue_nature['overall']['manageable'] += 1
            elif ('critical' in nature):
                team2_issue_nature['motor']['critical'] += 1
                team2_issue_nature['overall']['critical'] += 1

    # 15.2b Pest Control
    query_filters = [Team2PestControl.team_id == team2.team_id] + date_filter_fn(Team2PestControl)
    pest_control_data = Team2PestControl.query.filter(*query_filters).all()
    for item in pest_control_data:
        if item.nature_of_issue:
            nature = item.nature_of_issue.lower()
            if ('all_well' in nature or 'all well' in nature):
                team2_issue_nature['pest_control']['all_well'] += 1
                team2_issue_nature['overall']['all_well'] += 1
            elif ('manageable' in nature):
                team2_issue_nature['pest_control']['manageable'] += 1
                team2_issue_nature['overall']['manageable'] += 1
            elif ('critical' in nature):
                team2_issue_nature['pest_control']['critical'] += 1
                team2_issue_nature['overall']['critical'] += 1

    # 15.3 AC Temp Deviation
    query_filters = [Team2ACTempDeviation.team_id == team2.team_id] + date_filter_fn(Team2ACTempDeviation)
    ac_temp_dev_data = Team2ACTempDeviation.query.filter(*query_filters).all()
    for item in ac_temp_dev_data:
        if item.nature_of_issue:
            nature = item.nature_of_issue.lower()
            if ('all_well' in nature or 'all well' in nature):
                team2_issue_nature['ac_temp_deviation']['all_well'] += 1
                team2_issue_nature['overall']['all_well'] += 1
            elif ('manageable' in nature):
                team2_issue_nature['ac_temp_deviation']['manageable'] += 1
                team2_issue_nature['overall']['manageable'] += 1
            elif ('critical' in nature):
                team2_issue_nature['ac_temp_deviation']['critical'] += 1
                team2_issue_nature['overall']['critical'] += 1

    # 15.4 Electricity Consumption
    query_filters = [Team2ElectricityConsumption.team_id == team2.team_id] + date_filter_fn(Team2ElectricityConsumption)
    elec_data = Team2ElectricityConsumption.query.filter(*query_filters).all()
    for item in elec_data:
        # No nature_of_issue field, but overall_issue_desc may contain nature
        if hasattr(item, 'overall_issue_desc') and item.overall_issue_desc:
            nature = item.overall_issue_desc.lower()
            if ('all_well' in nature or 'all well' in nature):
                team2_issue_nature['electricity_consumption']['all_well'] += 1
                team2_issue_nature['overall']['all_well'] += 1
            elif ('manageable' in nature):
                team2_issue_nature['electricity_consumption']['manageable'] += 1
                team2_issue_nature['overall']['manageable'] += 1
            elif ('critical' in nature):
                team2_issue_nature['electricity_consumption']['critical'] += 1
                team2_issue_nature['overall']['critical'] += 1

    # 15.5 EB Details
    query_filters = [Team2EBDetails.team_id == team2.team_id] + date_filter_fn(Team2EBDetails)
    eb_details_data = Team2EBDetails.query.filter(*query_filters).all()
    for item in eb_details_data:
        if item.nature_of_issue:
            nature = item.nature_of_issue.lower()
            if ('all_well' in nature or 'all well' in nature):
                team2_issue_nature['eb_details']['all_well'] += 1
                team2_issue_nature['overall']['all_well'] += 1
            elif ('manageable' in nature):
                team2_issue_nature['eb_details']['manageable'] += 1
                team2_issue_nature['overall']['manageable'] += 1
            elif ('critical' in nature):
                team2_issue_nature['eb_details']['critical'] += 1
                team2_issue_nature['overall']['critical'] += 1

    # 15.6 Solar Details
    query_filters = [Team2SolarDetails.team_id == team2.team_id] + date_filter_fn(Team2SolarDetails)
    solar_details_data = Team2SolarDetails.query.filter(*query_filters).all()
    for item in solar_details_data:
        if item.nature_of_issue:
            nature = item.nature_of_issue.lower()
            if ('all_well' in nature or 'all well' in nature):
                team2_issue_nature['solar_details']['all_well'] += 1
                team2_issue_nature['overall']['all_well'] += 1
            elif ('manageable' in nature):
                team2_issue_nature['solar_details']['manageable'] += 1
                team2_issue_nature['overall']['manageable'] += 1
            elif ('critical' in nature):
                team2_issue_nature['solar_details']['critical'] += 1
                team2_issue_nature['overall']['critical'] += 1

    # 15.7 Genset Details
    query_filters = [Team2GensetDetails.team_id == team2.team_id] + date_filter_fn(Team2GensetDetails)
    genset_details_data = Team2GensetDetails.query.filter(*query_filters).all()
    for item in genset_details_data:
        if item.nature_of_issue:
            nature = item.nature_of_issue.lower()
            if ('all_well' in nature or 'all well' in nature):
                team2_issue_nature['genset_details']['all_well'] += 1
                team2_issue_nature['overall']['all_well'] += 1
            elif ('manageable' in nature):
                team2_issue_nature['genset_details']['manageable'] += 1
                team2_issue_nature['overall']['manageable'] += 1
            elif ('critical' in nature):
                team2_issue_nature['genset_details']['critical'] += 1
                team2_issue_nature['overall']['critical'] += 1


    # Team 2 Section 16: Security Issue Nature Aggregation

    # 16.a Count Verification (Security)
    query_filters = [Team2CountVerification.team_id == team2.team_id] + date_filter_fn(Team2CountVerification)
    count_verification_data = Team2CountVerification.query.filter(*query_filters).all()
    for item in count_verification_data:
        if item.nature_of_issue:
            nature = item.nature_of_issue.lower()
            if ('all_well' in nature or 'all well' in nature):
                team2_issue_nature['security_count_verification']['all_well'] += 1
                team2_issue_nature['overall']['all_well'] += 1
            elif ('manageable' in nature):
                team2_issue_nature['security_count_verification']['manageable'] += 1
                team2_issue_nature['overall']['manageable'] += 1
            elif ('critical' in nature):
                team2_issue_nature['security_count_verification']['critical'] += 1
                team2_issue_nature['overall']['critical'] += 1

    # 16.b Attendance Replacement (Security)
    query_filters = [Team2AttendanceReplacement.team_id == team2.team_id] + date_filter_fn(Team2AttendanceReplacement)
    attendance_replacement_data = Team2AttendanceReplacement.query.filter(*query_filters).all()
    for item in attendance_replacement_data:
        if item.nature_of_issue:
            nature = item.nature_of_issue.lower()
            if ('all_well' in nature or 'all well' in nature):
                team2_issue_nature['security_attendance_replacement']['all_well'] += 1
                team2_issue_nature['overall']['all_well'] += 1
            elif ('manageable' in nature):
                team2_issue_nature['security_attendance_replacement']['manageable'] += 1
                team2_issue_nature['overall']['manageable'] += 1
            elif ('critical' in nature):
                team2_issue_nature['security_attendance_replacement']['critical'] += 1
                team2_issue_nature['overall']['critical'] += 1

    # 16.c Security Info Note
    query_filters = [Team2SecurityInfoNote.team_id == team2.team_id] + date_filter_fn(Team2SecurityInfoNote)
    security_info_note_data = Team2SecurityInfoNote.query.filter(*query_filters).all()
    for item in security_info_note_data:
        if item.nature_of_issue:
            nature = item.nature_of_issue.lower()
            if ('all_well' in nature or 'all well' in nature):
                team2_issue_nature['security_info_note']['all_well'] += 1
                team2_issue_nature['overall']['all_well'] += 1
            elif ('manageable' in nature):
                team2_issue_nature['security_info_note']['manageable'] += 1
                team2_issue_nature['overall']['manageable'] += 1
            elif ('critical' in nature):
                team2_issue_nature['security_info_note']['critical'] += 1
                team2_issue_nature['overall']['critical'] += 1

    # 16.d Govt Officials In/Out
    query_filters = [Team2SecurityGovtInout.team_id == team2.team_id] + date_filter_fn(Team2SecurityGovtInout)
    govt_inout_data = Team2SecurityGovtInout.query.filter(*query_filters).all()
    for item in govt_inout_data:
        if item.nature_of_issue:
            nature = item.nature_of_issue.lower()
            if ('all_well' in nature or 'all well' in nature):
                team2_issue_nature['govt_officials_inout']['all_well'] += 1
                team2_issue_nature['overall']['all_well'] += 1
            elif ('manageable' in nature):
                team2_issue_nature['govt_officials_inout']['manageable'] += 1
                team2_issue_nature['overall']['manageable'] += 1
            elif ('critical' in nature):
                team2_issue_nature['govt_officials_inout']['critical'] += 1
                team2_issue_nature['overall']['critical'] += 1

    # 16.f Materials Inward (Security)
    query_filters = [Team2SecurityMaterialsInout.team_id == team2.team_id] + date_filter_fn(Team2SecurityMaterialsInout)
    materials_inward_data = Team2SecurityMaterialsInout.query.filter(*query_filters).all()
    for item in materials_inward_data:
        if item.nature_of_issue:
            nature = item.nature_of_issue.lower()
            if ('all_well' in nature or 'all well' in nature):
                team2_issue_nature['security_materials_inward']['all_well'] += 1
                team2_issue_nature['overall']['all_well'] += 1
            elif ('manageable' in nature):
                team2_issue_nature['security_materials_inward']['manageable'] += 1
                team2_issue_nature['overall']['manageable'] += 1
            elif ('critical' in nature):
                team2_issue_nature['security_materials_inward']['critical'] += 1
                team2_issue_nature['overall']['critical'] += 1

    # 16.g Materials Outward (Security)
    query_filters = [Team2SecurityMaterialsOutward.team_id == team2.team_id] + date_filter_fn(Team2SecurityMaterialsOutward)
    materials_outward_data = Team2SecurityMaterialsOutward.query.filter(*query_filters).all()
    for item in materials_outward_data:
        if item.nature_of_issue:
            nature = item.nature_of_issue.lower()
            if ('all_well' in nature or 'all well' in nature):
                team2_issue_nature['security_materials_outward']['all_well'] += 1
                team2_issue_nature['overall']['all_well'] += 1
            elif ('manageable' in nature):
                team2_issue_nature['security_materials_outward']['manageable'] += 1
                team2_issue_nature['overall']['manageable'] += 1
            elif ('critical' in nature):
                team2_issue_nature['security_materials_outward']['critical'] += 1
                team2_issue_nature['overall']['critical'] += 1

    # 16.h Transport Verification (Security)
    query_filters = [Team2TransportVerification.team_id == team2.team_id] + date_filter_fn(Team2TransportVerification)
    transport_verification_data = Team2TransportVerification.query.filter(*query_filters).all()
    for item in transport_verification_data:
        if item.nature_of_issue:
            nature = item.nature_of_issue.lower()
            if ('all_well' in nature or 'all well' in nature):
                team2_issue_nature['security_transport_verification']['all_well'] += 1
                team2_issue_nature['overall']['all_well'] += 1
            elif ('manageable' in nature):
                team2_issue_nature['security_transport_verification']['manageable'] += 1
                team2_issue_nature['overall']['manageable'] += 1
            elif ('critical' in nature):
                team2_issue_nature['security_transport_verification']['critical'] += 1
                team2_issue_nature['overall']['critical'] += 1

    # 17. Documents Movement (Team 2)
    query_filters = [Team2DocumentsMovement.team_id == team2.team_id] + date_filter_fn(Team2DocumentsMovement)
    documents_movement_data = Team2DocumentsMovement.query.filter(*query_filters).all()
    for item in documents_movement_data:
        # Row 1: New File / Document Entry
        if item.doc_new_nature:
            nature = item.doc_new_nature.lower()
            if ('all_well' in nature or 'all well' in nature):
                team2_issue_nature['documents_movement']['all_well'] += 1
                team2_issue_nature['overall']['all_well'] += 1
            elif ('manageable' in nature):
                team2_issue_nature['documents_movement']['manageable'] += 1
                team2_issue_nature['overall']['manageable'] += 1
            elif ('critical' in nature):
                team2_issue_nature['documents_movement']['critical'] += 1
                team2_issue_nature['overall']['critical'] += 1
        # Row 2: Non-Returnable File / Document
        if item.doc_nonret_nature:
            nature = item.doc_nonret_nature.lower()
            if ('all_well' in nature or 'all well' in nature):
                team2_issue_nature['documents_movement']['all_well'] += 1
                team2_issue_nature['overall']['all_well'] += 1
            elif ('manageable' in nature):
                team2_issue_nature['documents_movement']['manageable'] += 1
                team2_issue_nature['overall']['manageable'] += 1
            elif ('critical' in nature):
                team2_issue_nature['documents_movement']['critical'] += 1
                team2_issue_nature['overall']['critical'] += 1
        # Row 3: Original File / Doc Movement
        if item.doc_orig_nature:
            nature = item.doc_orig_nature.lower()
            if ('all_well' in nature or 'all well' in nature):
                team2_issue_nature['documents_movement']['all_well'] += 1
                team2_issue_nature['overall']['all_well'] += 1
            elif ('manageable' in nature):
                team2_issue_nature['documents_movement']['manageable'] += 1
                team2_issue_nature['overall']['manageable'] += 1
            elif ('critical' in nature):
                team2_issue_nature['documents_movement']['critical'] += 1
                team2_issue_nature['overall']['critical'] += 1

    # 18. Govt Official Documents (Team 2)
    query_filters = [Team2GovtOfficialDocuments.team_id == team2.team_id] + date_filter_fn(Team2GovtOfficialDocuments)
    govt_official_documents_data = Team2GovtOfficialDocuments.query.filter(*query_filters).all()
    for item in govt_official_documents_data:
        if item.nature_of_issue:
            nature = item.nature_of_issue.lower()
            if ('all_well' in nature or 'all well' in nature):
                team2_issue_nature['govt_official_documents']['all_well'] += 1
                team2_issue_nature['overall']['all_well'] += 1
            elif ('manageable' in nature):
                team2_issue_nature['govt_official_documents']['manageable'] += 1
                team2_issue_nature['overall']['manageable'] += 1
            elif ('critical' in nature):
                team2_issue_nature['govt_official_documents']['critical'] += 1
                team2_issue_nature['overall']['critical'] += 1

    # 19.a Thoorigai Team Social Media (Team 2)
    query_filters = [Team2ThoorigaiTeamSocialMedia.team_id == team2.team_id] + date_filter_fn(Team2ThoorigaiTeamSocialMedia)
    thoorigai_social_media_data = Team2ThoorigaiTeamSocialMedia.query.filter(*query_filters).all()
    for item in thoorigai_social_media_data:
        if item.nature_of_issue:
            nature = item.nature_of_issue.lower()
            if ('all_well' in nature or 'all well' in nature):
                team2_issue_nature['digital_marketing_thoorigai_social_media']['all_well'] += 1
                team2_issue_nature['overall']['all_well'] += 1
            elif ('manageable' in nature):
                team2_issue_nature['digital_marketing_thoorigai_social_media']['manageable'] += 1
                team2_issue_nature['overall']['manageable'] += 1
            elif ('critical' in nature):
                team2_issue_nature['digital_marketing_thoorigai_social_media']['critical'] += 1
                team2_issue_nature['overall']['critical'] += 1

    # 19.b Thoorigai Website Updates (Team 2)
    query_filters = [Team2WebsiteUpdates.team_id == team2.team_id] + date_filter_fn(Team2WebsiteUpdates)
    thoorigai_website_updates_data = Team2WebsiteUpdates.query.filter(*query_filters).all()
    for item in thoorigai_website_updates_data:
        if item.nature_of_issue:
            nature = item.nature_of_issue.lower()
            if ('all_well' in nature or 'all well' in nature):
                team2_issue_nature['digital_marketing_thoorigai_website_updates']['all_well'] += 1
                team2_issue_nature['overall']['all_well'] += 1
            elif ('manageable' in nature):
                team2_issue_nature['digital_marketing_thoorigai_website_updates']['manageable'] += 1
                team2_issue_nature['overall']['manageable'] += 1
            elif ('critical' in nature):
                team2_issue_nature['digital_marketing_thoorigai_website_updates']['critical'] += 1
                team2_issue_nature['overall']['critical'] += 1

    # 19.c MD Social Media (Team 2)
    query_filters = [Team2MDSocialMedia.team_id == team2.team_id] + date_filter_fn(Team2MDSocialMedia)
    md_social_media_data = Team2MDSocialMedia.query.filter(*query_filters).all()
    for item in md_social_media_data:
        if item.nature_of_issue:
            nature = item.nature_of_issue.lower()
            if ('all_well' in nature or 'all well' in nature):
                team2_issue_nature['digital_marketing_md_social_media']['all_well'] += 1
                team2_issue_nature['overall']['all_well'] += 1
            elif ('manageable' in nature):
                team2_issue_nature['digital_marketing_md_social_media']['manageable'] += 1
                team2_issue_nature['overall']['manageable'] += 1
            elif ('critical' in nature):
                team2_issue_nature['digital_marketing_md_social_media']['critical'] += 1
                team2_issue_nature['overall']['critical'] += 1

    
    # 20. Intercom Maintenance (Team 2)
    query_filters = [Team2IntercomMaintenance.team_id == team2.team_id] + date_filter_fn(Team2IntercomMaintenance)
    intercom_maintenance_data = Team2IntercomMaintenance.query.filter(*query_filters).all()
    for item in intercom_maintenance_data:
        if item.nature_of_issue:
            nature = item.nature_of_issue.lower()
            if ('all_well' in nature or 'all well' in nature):
                team2_issue_nature['intercom_maintenance']['all_well'] += 1
                team2_issue_nature['overall']['all_well'] += 1
            elif ('manageable' in nature):
                team2_issue_nature['intercom_maintenance']['manageable'] += 1
                team2_issue_nature['overall']['manageable'] += 1
            elif ('critical' in nature):
                team2_issue_nature['intercom_maintenance']['critical'] += 1
                team2_issue_nature['overall']['critical'] += 1

    # 21. Health Check Up (Team 2)
    query_filters = [Team2HealthCheckUp.team_id == team2.team_id] + date_filter_fn(Team2HealthCheckUp)
    health_check_up_data = Team2HealthCheckUp.query.filter(*query_filters).all()
    for item in health_check_up_data:
        if item.nature_of_issue:
            nature = item.nature_of_issue.lower()
            if ('all_well' in nature or 'all well' in nature):
                team2_issue_nature['health_check_up']['all_well'] += 1
                team2_issue_nature['overall']['all_well'] += 1
            elif ('manageable' in nature):
                team2_issue_nature['health_check_up']['manageable'] += 1
                team2_issue_nature['overall']['manageable'] += 1
            elif ('critical' in nature):
                team2_issue_nature['health_check_up']['critical'] += 1
                team2_issue_nature['overall']['critical'] += 1

    # 22. Net Connectivity & Print Details (Team 2)
    query_filters = [Team2NetConnectivityPrintDetails.team_id == team2.team_id] + date_filter_fn(Team2NetConnectivityPrintDetails)
    net_connectivity_data = Team2NetConnectivityPrintDetails.query.filter(*query_filters).all()
    for item in net_connectivity_data:
        if item.nature_of_issue:
            nature = item.nature_of_issue.lower()
            if ('all_well' in nature or 'all well' in nature):
                team2_issue_nature['net_connectivity_print_details']['all_well'] += 1
                team2_issue_nature['overall']['all_well'] += 1
            elif ('manageable' in nature):
                team2_issue_nature['net_connectivity_print_details']['manageable'] += 1
                team2_issue_nature['overall']['manageable'] += 1
            elif ('critical' in nature):
                team2_issue_nature['net_connectivity_print_details']['critical'] += 1
                team2_issue_nature['overall']['critical'] += 1

    # 23. General Maintenance - IT Products (Team 2)
    query_filters = [Team2GeneralMaintenanceITProducts.team_id == team2.team_id] + date_filter_fn(Team2GeneralMaintenanceITProducts)
    general_maintenance_it_data = Team2GeneralMaintenanceITProducts.query.filter(*query_filters).all()
    for item in general_maintenance_it_data:
        if item.nature_of_issue:
            nature = item.nature_of_issue.lower()
            if ('all_well' in nature or 'all well' in nature):
                team2_issue_nature['general_maintenance_it_products']['all_well'] += 1
                team2_issue_nature['overall']['all_well'] += 1
            elif ('manageable' in nature):
                team2_issue_nature['general_maintenance_it_products']['manageable'] += 1
                team2_issue_nature['overall']['manageable'] += 1
            elif ('critical' in nature):
                team2_issue_nature['general_maintenance_it_products']['critical'] += 1
                team2_issue_nature['overall']['critical'] += 1

    # 24. Calendar Schedule (Team 2)
    query_filters = [Team2CalendarSchedule.team_id == team2.team_id] + date_filter_fn(Team2CalendarSchedule)
    calendar_schedule_data = Team2CalendarSchedule.query.filter(*query_filters).all()
    for item in calendar_schedule_data:
        if item.nature_of_issue:
            nature = item.nature_of_issue.lower()
            # Map department to the correct key in team2_issue_nature
            dept_map = {
                'admin': 'calendar_schedule_admin',
                'house keeping': 'calendar_schedule_house_keeping',
                'security': 'calendar_schedule_security',
                'transport': 'calendar_schedule_transport'
            }
            dept_key = dept_map.get((item.department or '').strip().lower())
            if dept_key:
                if ('all_well' in nature or 'all well' in nature):
                    team2_issue_nature[dept_key]['all_well'] += 1
                    team2_issue_nature['overall']['all_well'] += 1
                elif ('manageable' in nature):
                    team2_issue_nature[dept_key]['manageable'] += 1
                    team2_issue_nature['overall']['manageable'] += 1
                elif ('critical' in nature):
                    team2_issue_nature[dept_key]['critical'] += 1
                    team2_issue_nature['overall']['critical'] += 1

    # 25. Training Attendance (Team 2)
    query_filters = [Team2TrainingAttendance.team_id == team2.team_id] + date_filter_fn(Team2TrainingAttendance)
    training_attendance_data = Team2TrainingAttendance.query.filter(*query_filters).all()
    for item in training_attendance_data:
        if item.nature_of_issue:
            nature = item.nature_of_issue.lower()
            # Map department_group and dept to the correct key in team2_issue_nature
            dept_map = {
                ('academics', 'academics - jr.school'): 'training_attendance_academics_jr',
                ('academics', 'academics - sr.school'): 'training_attendance_academics_sr',
                ('admin', 'admin - admin'): 'training_attendance_admin',
                ('admin', 'admin - drivers'): 'training_attendance_drivers',
                ('admin', 'admin - securities'): 'training_attendance_securities',
                ('admin', 'admin - drivers (sub)'): 'training_attendance_drivers_sub',
                ('admin', 'admin - conductors'): 'training_attendance_conductors',
            }
            dept_group = (item.department_group or '').strip().lower()
            dept = (item.dept or '').strip().lower()
            dept_key = dept_map.get((dept_group, dept))
            if dept_key:
                if ('all_well' in nature or 'all well' in nature):
                    team2_issue_nature[dept_key]['all_well'] += 1
                    team2_issue_nature['overall']['all_well'] += 1
                elif ('manageable' in nature):
                    team2_issue_nature[dept_key]['manageable'] += 1
                    team2_issue_nature['overall']['manageable'] += 1
                elif ('critical' in nature):
                    team2_issue_nature[dept_key]['critical'] += 1
                    team2_issue_nature['overall']['critical'] += 1

    # 26. Training Details (CBSE/CIS/External) (Team 2)
    query_filters = [Team2TrainingDetails.team_id == team2.team_id] + date_filter_fn(Team2TrainingDetails)
    training_details_data = Team2TrainingDetails.query.filter(*query_filters).all()
    for item in training_details_data:
        if item.nature_of_issue:
            nature = item.nature_of_issue.lower()
            key = 'training_details_cbse_cis_external'
            if ('all_well' in nature or 'all well' in nature):
                team2_issue_nature[key]['all_well'] += 1
                team2_issue_nature['overall']['all_well'] += 1
            elif ('manageable' in nature):
                team2_issue_nature[key]['manageable'] += 1
                team2_issue_nature['overall']['manageable'] += 1
            elif ('critical' in nature):
                team2_issue_nature[key]['critical'] += 1
                team2_issue_nature['overall']['critical'] += 1


    return team2_issue_nature
