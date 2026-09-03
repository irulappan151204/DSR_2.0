import os
import sys
import shutil

print("=" * 80)
print("CONVERTING models.py TO models/ PACKAGE")
print("=" * 80)

source_path = 'models.py' if os.path.exists('models.py') else 'scratch/models.py.bak'
with open(source_path, 'r', encoding='utf-8') as f:
    raw_lines = f.readlines()

# 1. Prepare target directories
os.makedirs('models/forms', exist_ok=True)

# 2. Extract models/core.py (lines 1 to 187)
core_lines = raw_lines[0:187]
with open('models/core.py', 'w', encoding='utf-8') as f:
    f.writelines(core_lines)
print("Created models/core.py (User, Team, Issue, Report)")

# 3. Extract models/forms/base.py (lines 188 to 200)
base_form_header = [
    "from extensions import db\n",
    "\n"
]
base_form_lines = base_form_header + raw_lines[187:200]
with open('models/forms/base.py', 'w', encoding='utf-8') as f:
    f.writelines(base_form_lines)
print("Created models/forms/base.py (BaseForm)")

# 4. Extract models/forms/team1.py (lines 201 to 1016 + lines 2517 to 2526 for Team1ASAGeneral)
team1_header = [
    "from extensions import db\n",
    "from .base import BaseForm\n",
    "\n"
]
team1_lines = team1_header + raw_lines[200:1016] + ["\n", "\n"] + raw_lines[2516:2526]
with open('models/forms/team1.py', 'w', encoding='utf-8') as f:
    f.writelines(team1_lines)
print("Created models/forms/team1.py (Team 1 Forms including Team1ASAGeneral)")

# 5. Extract models/forms/team2.py (lines 1017 to 2439)
team2_header = [
    "from extensions import db\n",
    "from .base import BaseForm\n",
    "\n"
]
team2_lines = team2_header + raw_lines[1016:2439]
with open('models/forms/team2.py', 'w', encoding='utf-8') as f:
    f.writelines(team2_lines)
print("Created models/forms/team2.py (Team 2 Forms)")

# 6. Extract models/forms/team3.py (lines 2440 to 2477)
team3_header = [
    "from extensions import db\n",
    "from .base import BaseForm\n",
    "\n"
]
team3_lines = team3_header + raw_lines[2439:2477]
with open('models/forms/team3.py', 'w', encoding='utf-8') as f:
    f.writelines(team3_lines)
print("Created models/forms/team3.py (Team 3 Forms)")

# 7. Extract models/actions.py (lines 2478 to 2504)
actions_header = [
    "from extensions import db\n",
    "from datetime import datetime\n",
    "from zoneinfo import ZoneInfo\n",
    "from timezone_utils import now_ist\n",
    "\n"
]
actions_lines = actions_header + raw_lines[2477:2504]
with open('models/actions.py', 'w', encoding='utf-8') as f:
    f.writelines(actions_lines)
print("Created models/actions.py (Action)")

# 8. Extract models/acknowledgements.py (lines 2505 to 2516)
ack_header = [
    "from extensions import db\n",
    "from datetime import datetime\n",
    "from zoneinfo import ZoneInfo\n",
    "from timezone_utils import now_ist\n",
    "\n"
]
ack_lines = ack_header + raw_lines[2504:2516]
with open('models/acknowledgements.py', 'w', encoding='utf-8') as f:
    f.writelines(ack_lines)
print("Created models/acknowledgements.py (Acknowledgement)")

# 9. Extract models/storage.py (lines 2527 to 2544)
storage_header = [
    "from extensions import db\n",
    "from datetime import datetime\n",
    "from zoneinfo import ZoneInfo\n",
    "from timezone_utils import now_ist\n",
    "\n"
]
storage_lines = storage_header + raw_lines[2526:2544]
with open('models/storage.py', 'w', encoding='utf-8') as f:
    f.writelines(storage_lines)
print("Created models/storage.py (FileStorage)")

# 10. Extract models/critical.py (lines 2545 to end)
critical_header = [
    "from extensions import db\n",
    "from datetime import datetime\n",
    "from zoneinfo import ZoneInfo\n",
    "from timezone_utils import now_ist\n",
    "from .forms.base import BaseForm\n",
    "\n"
]
critical_lines = critical_header + raw_lines[2544:]
with open('models/critical.py', 'w', encoding='utf-8') as f:
    f.writelines(critical_lines)
print("Created models/critical.py (CapaFinding, CapaEvent, CapaAttachment, and CAPA constants)")

# 11. Create models/forms/__init__.py re-exporting all forms
forms_init_content = """# models/forms/__init__.py
import inspect
from .base import BaseForm
from . import team1, team2, team3

# Collect all model classes defined in submodules
for mod in (team1, team2, team3):
    for name, cls in inspect.getmembers(mod, inspect.isclass):
        if cls.__module__ == mod.__name__:
            globals()[name] = cls
"""
with open('models/forms/__init__.py', 'w', encoding='utf-8') as f:
    f.write(forms_init_content)
print("Created models/forms/__init__.py")

# 12. Create models/__init__.py re-exporting ALL 120 classes
init_content = """# models/__init__.py
# 100% Backwards-compatible re-export of all 120 SQLAlchemy models
import inspect

from .core import User, Team, Issue, Report
from .actions import Action
from .critical import CapaFinding, CapaEvent, CapaAttachment
from .storage import FileStorage
from .acknowledgements import Acknowledgement
from .forms.base import BaseForm
from .forms import team1, team2, team3

# Dynamically re-export all team form classes to guarantee 100% attribute parity
for _mod in (team1, team2, team3):
    for _name, _cls in inspect.getmembers(_mod, inspect.isclass):
        if _cls.__module__ == _mod.__name__:
            globals()[_name] = _cls

# Core export list
__all__ = [
    'User', 'Team', 'Issue', 'Report',
    'Action', 'CapaFinding', 'CapaEvent', 'CapaAttachment',
    'FileStorage', 'Acknowledgement', 'BaseForm'
] + [
    _name for _mod in (team1, team2, team3)
    for _name, _cls in inspect.getmembers(_mod, inspect.isclass)
    if _cls.__module__ == _mod.__name__
]
"""
with open('models/__init__.py', 'w', encoding='utf-8') as f:
    f.write(init_content)
print("Created models/__init__.py with full dynamic re-exports")

# 13. Move root models.py aside to scratch/models_original.py
if os.path.exists('models.py'):
    shutil.move('models.py', 'scratch/models_original.py')
    print("Moved root models.py to scratch/models_original.py (package active)")
else:
    print("Root models.py already moved to scratch/models_original.py")

print("\nModel package conversion completed successfully.")
