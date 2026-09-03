import models as models_module
from sqlalchemy import or_

# Define all 108 BaseForm models plus CapaFinding
BASE_FORM_MODELS = [
    'Team1CalendarSchedule', 'Team1ASAActivities', 'Team1ASASports', 'Team1ASAGeneral',
    'Team1StudentAttendance', 'Team1StudentGrooming', 'Team1StudentLateComing',
    'Team1AdmissionStatus', 'Team1TransferCertificate', 'Team1ParentActivity',
    'Team1ParentVisit', 'Team1ExamSchedule', 'Team1ExternalInfo', 'Team1SickBay',
    'Team1HomeSchoolComm', 'Team1Disciplinary', 'Team1Logistics', 'Team1CompetitionCert',
    'Team1StaffConcern', 'Team1ParentConcern', 'Team1StudentConcern', 'Team1AEPAttendance',
    'Team1ExtendedClassAttendance', 'Team1TrainingSession', 'Team1WeeklyMeeting',
    'Team1SpecialEducation', 'Team1Hostel', 'Team1SEC', 'Team1SchoolCounsellor',
    'Team1Scholorius', 'Team1ParentConcernDetail',
    'Team2HRAttendance', 'Team2AdminAttendance', 'Team2TotalHRAttendance',
    'Team2RecruitmentActivity', 'Team2PendingRecruitment', 'Team2RecruitmentPipeline',
    'Team2StaffStatusUpdates', 'Team2SalaryPending', 'Team2PoliceVerification',
    'Team2InterviewSchedule', 'Team2ExitInformation', 'Team2IssuesStaffConcerns',
    'Team2KuralRecitation', 'Team2FrontOfficePhoneCalls', 'Team2VisitorLog',
    'Team2BSNLPhoneStatus', 'Team2MaterialsInward', 'Team2MaterialsOutward',
    'Team2MaterialsMovement', 'Team2ReturnableMaterialTracking', 'Team2ReturnableGoodsReport',
    'Team2CampusCameraStatus', 'Team2VehicleCameraStatus', 'Team2BusACCameraStatus',
    'Team2GPSMonitoring', 'Team2IssuesIdentifiedMonitoring', 'Team2IssuesIdentifiedControlRoom',
    'Team2CameraFootageEntry', 'Team2BiometricsAccessCardPunching', 'Team2WaterTDSDeviation',
    'Team2TestingCleaning', 'Team2WaterLevel', 'Team2HousekeepingGeneral', 'Team2PoolTesting', 'Team2WashroomCleanliness',
    'Team2TransportAttendance', 'Team2ACWorkingStatus', 'Team2LateReporting',
    'Team2MaintenanceServiceIssues', 'Team2CarMaintenanceCleaning', 'Team2VehicleRenewalsDelays',
    'Team2SpecialTrip', 'Team2ACTemperatureCheck', 'Team2LaborEbSolarGenset',
    'Team2Motor', 'Team2PestControl', 'Team2ACTempDeviation', 'Team2ElectricityConsumption',
    'Team2EBDetails', 'Team2SolarDetails', 'Team2GensetDetails', 'Team2CountVerification',
    'Team2AttendanceReplacement', 'Team2SecurityInfoNote', 'Team2SecurityGovtInout',
    'Team2AlcoholTest', 'Team2SecurityMaterialsInout', 'Team2SecurityMaterialsOutward',
    'Team2TransportVerification', 'Team2DocumentsMovement', 'Team2GovtOfficialDocuments',
    'Team2ThoorigaiTeamSocialMedia', 'Team2WebsiteUpdates', 'Team2MDSocialMedia',
    'Team2IntercomMaintenance', 'Team2HealthCheckUp', 'Team2NetConnectivityPrintDetails',
    'Team2GeneralMaintenanceITProducts', 'Team2CalendarSchedule', 'Team2TrainingAttendance',
    'Team2TrainingDetails', 'Team2ParentConcernDetail', 'Team2ManpowerPlanning', 'Team2OverallConsolidation', 
    'Team2UniformDetails', 'Team2DepartmentWiseUniformDetails', 'Team3Audit', 'Team3NewAudit',
    'CapaFinding'
]

def fetch_history_records(user_id, start_dt=None, end_dt=None, form_query=None):
    """Query user submission records across all form models and CapaFinding."""
    results_by_model = []
    
    for model_name in BASE_FORM_MODELS:
        if form_query and model_name != form_query:
            continue
        try:
            model_cls = getattr(models_module, model_name)
            if model_name == 'CapaFinding':
                q = model_cls.query.filter(
                    or_(
                        model_cls.submitted_by == user_id,
                        model_cls.capa_1_submitted_by == user_id,
                        model_cls.recipient_id == user_id
                    )
                )
            else:
                q = model_cls.query.filter_by(submitted_by=user_id)
            if start_dt:
                q = q.filter(model_cls.submitted_at >= start_dt)
            if end_dt:
                q = q.filter(model_cls.submitted_at < end_dt)
            q = q.order_by(model_cls.submitted_at.desc())
            records = q.limit(500).all()
            if records:
                results_by_model.append((model_name, records))
        except Exception:
            continue

    return results_by_model
