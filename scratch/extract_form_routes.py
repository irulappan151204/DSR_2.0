import os

print("=" * 80)
print("EXTRACTING FORM SUBMISSION ROUTES FROM app.py")
print("=" * 80)

with open('app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Line numbers (0-indexed):
# Team 1: line 858 (index 858) to line 2371 (index 2371)
# Team 2: line 2371 (index 2371) to line 5762 (index 5762)
# Team 3: line 5762 (index 5762) to line 5880 (index 5880)

team1_body = lines[858:2371]
team2_body = lines[2371:5762]
team3_body = lines[5762:5880]

os.makedirs('routes/forms', exist_ok=True)

# 1. Team 1 Forms
team1_content = [
    "# routes/forms/team1_forms.py\n",
    "from flask import request, redirect, url_for, flash, jsonify\n",
    "from flask_login import login_required, current_user\n",
    "from datetime import datetime\n",
    "from zoneinfo import ZoneInfo\n",
    "from werkzeug.utils import secure_filename\n",
    "from extensions import db\n",
    "from utils.helpers import safe_int, safe_float, safe_date, safe_time\n",
    "from models import (\n",
    "    Team1CalendarSchedule, Team1StudentAttendance, Team1ParentConcernDetail,\n",
    "    Team1ASAActivities, Team1ASASports, Team1ASAGeneral, Team1StudentGrooming,\n",
    "    Team1StudentLateComing, Team1AdmissionStatus, Team1TransferCertificate,\n",
    "    Team1ParentActivity, Team1ParentVisit, Team1ExamSchedule, Team1ExternalInfo,\n",
    "    Team1SickBay, Team1HomeSchoolComm, Team1Disciplinary, Team1Logistics,\n",
    "    Team1CompetitionCert, Team1StaffConcern, Team1ParentConcern, Team1StudentConcern,\n",
    "    Team1AEPAttendance, Team1ExtendedClassAttendance, Team1TrainingSession,\n",
    "    Team1WeeklyMeeting, Team1SpecialEducation, Team1Hostel, Team1SEC,\n",
    "    Team1SchoolCounsellor, Team1Scholorius, FileStorage\n",
    ")\n\n",
    "def register_team1_forms(app):\n",
    '    """Register all 31 Team 1 (Academics) form submission routes."""\n'
]
# Indent each line by 4 spaces
for line in team1_body:
    team1_content.append("    " + line if line.strip() else "\n")

with open('routes/forms/team1_forms.py', 'w', encoding='utf-8') as f:
    f.writelines(team1_content)
print(f"Created routes/forms/team1_forms.py ({len(team1_content)} lines)")

# 2. Team 2 Forms
team2_content = [
    "# routes/forms/team2_forms.py\n",
    "from flask import request, redirect, url_for, flash, jsonify\n",
    "from flask_login import login_required, current_user\n",
    "from datetime import datetime\n",
    "from zoneinfo import ZoneInfo\n",
    "from werkzeug.utils import secure_filename\n",
    "from extensions import db\n",
    "from utils.helpers import safe_int, safe_float, safe_date, safe_time\n",
    "from models import (\n",
    "    Team2HRAttendance, Team2AdminAttendance, Team2RecruitmentActivity,\n",
    "    Team2PendingRecruitment, Team2RecruitmentPipeline, Team2StaffStatusUpdates,\n",
    "    Team2SalaryPending, Team2PoliceVerification, Team2InterviewSchedule,\n",
    "    Team2ExitInformation, Team2IssuesStaffConcerns, Team2KuralRecitation,\n",
    "    Team2FrontOfficePhoneCalls, Team2VisitorLog, Team2BSNLPhoneStatus,\n",
    "    Team2MaterialsInward, Team2MaterialsOutward, Team2MaterialsMovement,\n",
    "    Team2ReturnableMaterialTracking, Team2ReturnableGoodsReport,\n",
    "    Team2CampusCameraStatus, Team2VehicleCameraStatus, Team2BusACCameraStatus,\n",
    "    Team2GPSMonitoring, Team2IssuesIdentifiedMonitoring, Team2IssuesIdentifiedControlRoom,\n",
    "    Team2CameraFootageEntry, Team2BiometricsAccessCardPunching, Team2WaterTDSDeviation,\n",
    "    Team2TestingCleaning, Team2WaterLevel, Team2HousekeepingGeneral, Team2PoolTesting,\n",
    "    Team2WashroomCleanliness, Team2TransportAttendance, Team2ACWorkingStatus,\n",
    "    Team2LateReporting, Team2MaintenanceServiceIssues, Team2CarMaintenanceCleaning,\n",
    "    Team2VehicleRenewalsDelays, Team2SpecialTrip, Team2ACTemperatureCheck,\n",
    "    Team2LaborEbSolarGenset, Team2Motor, Team2PestControl, Team2ACTempDeviation,\n",
    "    Team2ElectricityConsumption, Team2EBDetails, Team2SolarDetails, Team2GensetDetails,\n",
    "    Team2CountVerification, Team2AttendanceReplacement, Team2SecurityInfoNote,\n",
    "    Team2SecurityGovtInout, Team2AlcoholTest, Team2SecurityMaterialsInout,\n",
    "    Team2SecurityMaterialsOutward, Team2TransportVerification, Team2DocumentsMovement,\n",
    "    Team2GovtOfficialDocuments, Team2ThoorigaiTeamSocialMedia, Team2WebsiteUpdates,\n",
    "    Team2MDSocialMedia, Team2IntercomMaintenance, Team2HealthCheckUp,\n",
    "    Team2NetConnectivityPrintDetails, Team2GeneralMaintenanceITProducts,\n",
    "    Team2CalendarSchedule, Team2TrainingAttendance, Team2TrainingDetails,\n",
    "    Team2ManpowerPlanning, Team2OverallConsolidation, Team2UniformDetails,\n",
    "    Team2DepartmentWiseUniformDetails, Team2TotalHRAttendance, Team2ParentConcernDetail,\n",
    "    FileStorage\n",
    ")\n\n",
    "def register_team2_forms(app):\n",
    '    """Register all 75 Team 2 (Admin) form submission routes."""\n'
]
for line in team2_body:
    team2_content.append("    " + line if line.strip() else "\n")

with open('routes/forms/team2_forms.py', 'w', encoding='utf-8') as f:
    f.writelines(team2_content)
print(f"Created routes/forms/team2_forms.py ({len(team2_content)} lines)")

# 3. Team 3 Forms
team3_content = [
    "# routes/forms/team3_forms.py\n",
    "from flask import request, redirect, url_for, flash, jsonify\n",
    "from flask_login import login_required, current_user\n",
    "from datetime import datetime\n",
    "from werkzeug.utils import secure_filename\n",
    "from extensions import db\n",
    "from critical import can_audit\n",
    "from models import Team3Audit, Team3NewAudit, FileStorage\n\n",
    "def register_team3_forms(app):\n",
    '    """Register all Team 3 (Audit) form submission routes."""\n'
]
for line in team3_body:
    team3_content.append("    " + line if line.strip() else "\n")

with open('routes/forms/team3_forms.py', 'w', encoding='utf-8') as f:
    f.writelines(team3_content)
print(f"Created routes/forms/team3_forms.py ({len(team3_content)} lines)")

# 4. routes/forms/__init__.py
init_content = [
    "# routes/forms/__init__.py\n",
    "from .team1_forms import register_team1_forms\n",
    "from .team2_forms import register_team2_forms\n",
    "from .team3_forms import register_team3_forms\n\n",
    "def register_all_form_routes(app):\n",
    '    """Register all 108 form submission handlers on the Flask app."""\n',
    "    register_team1_forms(app)\n",
    "    register_team2_forms(app)\n",
    "    register_team3_forms(app)\n"
]
with open('routes/forms/__init__.py', 'w', encoding='utf-8') as f:
    f.writelines(init_content)
print("Created routes/forms/__init__.py")

# 5. Update app.py: replace lines 858 to 5880 with the single registration call
app_top = lines[:858]
app_bottom = lines[5880:]
replacement_block = [
    "\n",
    "# ==========================================================================\n",
    "# Form submission routes (108 handlers: Team 1 Academics, Team 2 Admin, Team 3 Audit)\n",
    "# ==========================================================================\n",
    "from routes.forms import register_all_form_routes\n",
    "register_all_form_routes(app)\n",
    "\n"
]

new_app_lines = app_top + replacement_block + app_bottom
with open('app.py', 'w', encoding='utf-8') as f:
    f.writelines(new_app_lines)
print(f"Updated app.py: reduced from {len(lines)} lines to {len(new_app_lines)} lines!")
