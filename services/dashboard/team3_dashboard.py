from datetime import datetime, timedelta, date as dt_date
from flask import url_for
from sqlalchemy import func
from extensions import db, cache
from models import *

def get_team3_data(selected_date_obj, start_of_day, end_of_day, show_all_dates, current_user):
    team3_audit_data = []
    team3_new_audit_data = []
    unack_count = 0

    team3 = Team.query.filter_by(team_name='Team 3').first()
    if team3:
        query = Team3Audit.query.filter(Team3Audit.team_id == team3.team_id)

        if not show_all_dates:

            query = query.filter(

                Team3Audit.submitted_at >= start_of_day,

                Team3Audit.submitted_at <= end_of_day

            )

        audit_data = query.order_by(Team3Audit.submitted_at.desc()).all()
        team3_audit_data = [{
            'date': item.submitted_at,
            'frequency': item.frequency,
            'audit_components': item.audit_components,
            'audit_by': item.audit_by,
            'audit_time': item.audit_time,
            'issue_nature': item.issue_nature,
            'audit_remarks': item.audit_remarks,
        } for item in audit_data]

        query = Team3NewAudit.query.filter(Team3NewAudit.team_id == team3.team_id)
        if not show_all_dates:
            query = query.filter(
                Team3NewAudit.submitted_at >= start_of_day,
                Team3NewAudit.submitted_at <= end_of_day
            )
        new_audit_rows = query.order_by(Team3NewAudit.submitted_at.desc()).all()
        for row in new_audit_rows:
            team3_new_audit_data.append({
                'date': row.submitted_at,
                'frequency': row.frequency,
                'component': row.component,
                'audited_by': row.audited_by,
                'staff_name': row.staff_name,
                'grade': row.grade,
                'section': row.section,
                'specification': row.specification,
                'issue_nature': row.issue_nature,
                'remark': row.remark,
                'media_url': (url_for('serve_file', file_id=row.media_file_id) if row.media_file_id else None),
                'media_name': (row.media if hasattr(row, 'media') else None)
            })




    available_dates = []

    # List of all Team 1 models
    team1_models = [
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
        Team1Hostel,
        Team1SEC,
        Team1SchoolCounsellor,
        Team1Scholorius
    ]


    team2_models = [
        Team2HRAttendance,
        Team2TotalHRAttendance,
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
        Team2ManpowerPlanning,
        Team2OverallConsolidation,
        Team2BiometricsAccessCardPunching,
        Team2CampusCameraStatus,
        Team2VehicleCameraStatus,
        Team2BusACCameraStatus,
        Team2GPSMonitoring,
        Team2IssuesIdentifiedMonitoring,
        Team2IssuesIdentifiedControlRoom,
        Team2ParentConcernDetail,
        Team2WaterLevel,
        Team2HousekeepingGeneral,
        Team2UniformDetails,
        Team2DepartmentWiseUniformDetails
    ]


    # TEAM 3 MODELS
    team3_models = [
        Team3Audit,
        Team3NewAudit
    ]

    # Add unacknowledged count for banner - cached to eliminate 72 queries per request
    today = dt_date.today()
    unack_cache_key = f"unack_count:{current_user.user_id}:{today.isoformat()}"
    cached_unack = None
    try:
        cached_unack = cache.get(unack_cache_key)
    except Exception:
        pass

    if cached_unack is not None:
        unack_count = cached_unack
    else:
        start_date = today - timedelta(days=30)
        report_dates = set()

        def add_report_dates_from_model(model, team_id):
            try:
                rows = db.session.query(
                    func.date(model.submitted_at)
                ).filter(
                    model.team_id == team_id,
                    func.date(model.submitted_at) >= start_date,
                    func.date(model.submitted_at) <= today
                ).distinct().all()
                for row in rows:
                    report_dates.add(row[0])
            except Exception as e:
                print(f"Error processing model {model.__name__}: {e}")

        if current_user.role == 'MD':
            for model in team1_models:
                add_report_dates_from_model(model, 1)
            for model in team2_models:
                add_report_dates_from_model(model, 2)
            for model in team3_models:
                add_report_dates_from_model(model, 3)
        elif current_user.is_team_lead:
            if current_user.team_id == 1:
                for model in team1_models:
                    add_report_dates_from_model(model, 1)
            elif current_user.team_id == 2:
                for model in team2_models:
                    add_report_dates_from_model(model, 2)
            elif current_user.team_id == 3:
                for model in team3_models:
                    add_report_dates_from_model(model, 3)

        try:
            user_acks = {a.date: a for a in Acknowledgement.query.filter_by(user_id=current_user.user_id).all()}
            pending_dates = [d for d in sorted(report_dates) if not (user_acks.get(d) and user_acks.get(d).acknowledged_at)]
            unack_count = len(pending_dates)
            try:
                cache.set(unack_cache_key, unack_count, timeout=300)
            except Exception:
                pass
        except Exception as e:
            print(f"Error calculating unacknowledged count: {e}")
            unack_count = 0

    return {
        'team3_audit_data': team3_audit_data,
        'team3_new_audit_data': team3_new_audit_data,
        'unack_count': unack_count,
    }
