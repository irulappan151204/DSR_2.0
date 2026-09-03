import sys
sys.path.insert(0, '.')

import app
routes = [rule.rule for rule in app.app.url_map.iter_rules()]
print(f"Application started successfully!")
print(f"Total routes registered: {len(routes)}")
assert len(routes) == 152, f"Expected 152 routes, got {len(routes)}"

from utils.helpers import safe_int, safe_float, safe_date, safe_time
assert safe_int('123') == 123
assert safe_float('12.34') == 12.34
assert str(safe_date('2026-09-03')) == '2026-09-03'
assert str(safe_time('14:30')) == '14:30:00'

from utils.filters import json_escape
assert json_escape('hello "world" \n test') == 'hello \\"world\\" \\n test'

print("Step 1 sanity checks passed 100%!")
