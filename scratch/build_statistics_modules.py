import os
import re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
src_path = os.path.join(ROOT, 'statistics_routes.py')

with open(src_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 1. Team 1
t1_init_dict = lines[93:131]
t1_body = lines[237:769]
t1_models_lines = lines[2079:2110]

# Extract imported model names
t1_models = []
for l in t1_models_lines:
    m = re.findall(r'Team1[A-Za-z0-9_]+', l)
    if m:
        t1_models.extend(m)

t1_content = []
t1_content.append("from models import (\n    " + ",\n    ".join(t1_models) + "\n)\n\n")
t1_content.append("TEAM1_MODELS = [\n    " + ",\n    ".join(t1_models) + "\n]\n\n")
t1_content.append("def get_initial_team1_issue_nature():\n    return {\n")
for l in t1_init_dict[1:]:
    t1_content.append(l[4:] if l.startswith('    ') else l)
t1_content.append("\n\ndef populate_team1_issue_nature(team1, date_filter_fn):\n")
t1_content.append("    team1_issue_nature = get_initial_team1_issue_nature()\n")
t1_content.append("    if not team1:\n        return team1_issue_nature\n\n")

for l in t1_body:
    # replace build_date_filter with date_filter_fn
    mod_l = l.replace('build_date_filter', 'date_filter_fn')
    # adjustment of indentation: in statistics_routes.py, line had 8 or 4 leading spaces
    t1_content.append(mod_l[4:] if mod_l.startswith('    ') else mod_l)

t1_content.append("\n    return team1_issue_nature\n")

t1_file_path = os.path.join(ROOT, 'services', 'statistics', 'team1_statistics.py')
with open(t1_file_path, 'w', encoding='utf-8') as f:
    f.writelines(t1_content)
print(f"Generated {t1_file_path} ({len(t1_content)} lines)")

# 2. Team 2
t2_init_dict = lines[132:226]
t2_body = lines[774:2031]
t2_models_lines = lines[2111:2183]

t2_models = []
for l in t2_models_lines:
    m = re.findall(r'Team2[A-Za-z0-9_]+', l)
    if m:
        t2_models.extend(m)

t2_content = []
t2_content.append("from models import (\n    " + ",\n    ".join(t2_models) + "\n)\n\n")
t2_content.append("TEAM2_MODELS = [\n    " + ",\n    ".join(t2_models) + "\n]\n\n")
t2_content.append("def get_initial_team2_issue_nature():\n    return {\n")
for l in t2_init_dict[1:]:
    t2_content.append(l[4:] if l.startswith('    ') else l)
t2_content.append("\n\ndef populate_team2_issue_nature(team2, date_filter_fn):\n")
t2_content.append("    team2_issue_nature = get_initial_team2_issue_nature()\n")
t2_content.append("    if not team2:\n        return team2_issue_nature\n\n")

for idx, l in enumerate(t2_body):
    mod_l = l.replace('build_date_filter', 'date_filter_fn')
    actual_line_idx = 775 + idx
    if actual_line_idx >= 909:
        # Keep as is (already has 4 spaces)
        t2_content.append(mod_l)
    else:
        # Strip 4 spaces from 8 spaces to make it 4 spaces
        t2_content.append(mod_l[4:] if mod_l.startswith('    ') else mod_l)

t2_content.append("\n    return team2_issue_nature\n")

t2_file_path = os.path.join(ROOT, 'services', 'statistics', 'team2_statistics.py')
with open(t2_file_path, 'w', encoding='utf-8') as f:
    f.writelines(t2_content)
print(f"Generated {t2_file_path} ({len(t2_content)} lines)")
