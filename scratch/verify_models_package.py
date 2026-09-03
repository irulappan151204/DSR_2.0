import sys
sys.path.insert(0, '.')

import json
import inspect
import models

print("=" * 80)
print("VERIFYING models/ PACKAGE AGAINST BASELINE INVENTORY")
print("=" * 80)

with open('scratch/models_baseline_inventory.json', 'r', encoding='utf-8') as fp:
    baseline = json.load(fp)

# 1. Verify all 120 classes are present in models package
missing_classes = []
for cname, cinfo in baseline['classes'].items():
    if not hasattr(models, cname):
        missing_classes.append(cname)
    else:
        cls = getattr(models, cname)
        if not cinfo.get('is_base'):
            assert cls.__tablename__ == cinfo['table_name'], f"Table name mismatch for {cname}: {cls.__tablename__} != {cinfo['table_name']}"

print(f"Total classes checked: {len(baseline['classes'])}")
print(f"Missing classes: {len(missing_classes)}")
if missing_classes:
    print("  MISSING:", missing_classes)
assert len(missing_classes) == 0, f"Missing {len(missing_classes)} classes from models package!"
print("  [PASS] All 120 model classes are present with identical __tablename__!")

# 2. Test direct imports across all modules
print("\n--- Testing Core Model Imports ---")
from models import User, Team, Issue, Report, Action, CapaFinding, CapaEvent, CapaAttachment, FileStorage, Acknowledgement, BaseForm
print(f"  [PASS] Successfully imported: User, Team, Issue, Report, Action, CapaFinding, CapaEvent, CapaAttachment, FileStorage, Acknowledgement, BaseForm")

# 3. Test form model imports
print("\n--- Testing Form Model Imports ---")
from models import Team1CalendarSchedule, Team1StudentAttendance, Team2HRAttendance, Team2ACTemperatureCheck, Team3Audit, Team3NewAudit
print(f"  [PASS] Successfully imported sample Team 1, Team 2, and Team 3 form models")

# 4. Test external imports from inventory
print("\n--- Testing All External Import Sites from Inventory ---")
for filename, symbols in baseline['external_imports'].items():
    for sym in symbols:
        assert hasattr(models, sym), f"External import failure: {filename} imports {sym} which is missing in models package!"
print(f"  [PASS] All symbols required by all {len(baseline['external_imports'])} external files are verified!")

print("\n" + "=" * 80)
print("MODELS PACKAGE 100% VERIFIED!")
print("=" * 80)
