import subprocess
import sys
sys.path.insert(0, '.')

c = subprocess.check_output(['git', 'show', '0d72caf:app.py'], text=True, encoding='utf-8')
with open('scratch/temp_baseline_app.py', 'w', encoding='utf-8') as f:
    f.write(c)

import scratch.temp_baseline_app as old_app_mod
old_rules = set((r.rule, r.endpoint) for r in old_app_mod.app.url_map.iter_rules())

import app
new_rules = set((r.rule, r.endpoint) for r in app.app.url_map.iter_rules())

print(f"Baseline rules count: {len(old_rules)}")
print(f"Current rules count:  {len(new_rules)}")

missing = old_rules - new_rules
print("Missing from current:")
for m in missing:
    print(" ", m)

added = new_rules - old_rules
print("Added in current:")
for a in added:
    print(" ", a)
