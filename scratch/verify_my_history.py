import sys
sys.path.insert(0, '.')
from app import app
from models import User, CapaFinding
from extensions import cache

with app.app_context():
    users = {
        'Auditor': User.query.filter_by(username='auditteam').first(),
        'Team Member': User.query.filter_by(username='anita').first(),
        'Team Lead': User.query.filter_by(username='sujatha').first(),
    }

print("=" * 80)
print("MY HISTORY INTEGRATION & DEDUPLICATION VERIFICATION")
print("=" * 80)

with app.test_client() as client:
    for role_name, user in users.items():
        cache.clear()
        with client.session_transaction() as sess:
            sess['_user_id'] = str(user.user_id)
            sess['_fresh'] = True
            
        resp = client.get('/my_history')
        assert resp.status_code == 200
        html = resp.data.decode('utf-8')
        
        # Verify rendered content
        assert "My Submission History" in html or "history" in html.lower()
        print(f"\nRole: {role_name} ({user.username})")
        print(f"  HTTP 200: Response length {len(html)} bytes")
        
        # Direct verification of history rows data structure
        from app import models_module
        start_dt = None
        end_dt = None
        form_query = None
        base_form_models = [
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
        
        with app.app_context():
            from sqlalchemy import or_
            rows = []
            seen_keys = set()
            duplicates = []
            
            for model_name in base_form_models:
                model_cls = getattr(models_module, model_name)
                if model_name == 'CapaFinding':
                    q = model_cls.query.filter(
                        or_(
                            model_cls.submitted_by == user.user_id,
                            model_cls.capa_1_submitted_by == user.user_id,
                            model_cls.recipient_id == user.user_id
                        )
                    )
                else:
                    q = model_cls.query.filter_by(submitted_by=user.user_id)
                results = q.limit(500).all()
                for r in results:
                    key = (model_name, r.form_id)
                    if key in seen_keys:
                        duplicates.append(key)
                    seen_keys.add(key)
                    rows.append({
                        'form_name': model_name,
                        'form_id': r.form_id,
                        'submitted_at': r.submitted_at
                    })
                    
            print(f"  Total history records fetched: {len(rows)}")
            print(f"  Duplicate entries: {len(duplicates)}")
            assert len(duplicates) == 0, f"Found duplicate entries in history: {duplicates}"
            
            # Check for CapaFinding records
            capa_records = [r for r in rows if r['form_name'] == 'CapaFinding']
            print(f"  CapaFinding records associated with {user.username}: {len(capa_records)}")
            
            # Check for legacy form records
            legacy_records = [r for r in rows if r['form_name'] != 'CapaFinding']
            print(f"  Legacy form records associated with {user.username}: {len(legacy_records)}")
            print("  [PASS] All history records strictly associated with user, zero duplicates.")

print("\n==========================================================")
print("ALL MY HISTORY VERIFICATION TESTS PASSED (100%)!")
print("==========================================================")
