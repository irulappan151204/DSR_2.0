import os
import glob
import re
import ast

py_files = sorted([f for f in glob.glob('*.py') if 'venv' not in f and not f.startswith('scratch')])

print("=" * 120)
print(f"{'FILE':<22} | {'LINES':<6} | {'ROUTES':<6} | {'TEMPLATES':<9} | {'MODELS TOUCHED':<14} | {'RISK LEVEL'}")
print("=" * 120)

file_info = {}

for f in py_files:
    with open(f, 'r', encoding='utf-8', errors='ignore') as fp:
        lines = fp.readlines()
    content = "".join(lines)
    
    # Routes
    routes = re.findall(r'@(?:app|[a-zA-Z0-9_]+_bp)\.route\([\'\"]([^\'\"]+)[\'\"]', content)
    
    # Templates
    templates = set(re.findall(r'render_template\([\'\"]([^\'\"]+)[\'\"]', content))
    
    # Models referenced
    models_referenced = set(re.findall(r'\b(Team[123][A-Za-z0-9_]+|User|Team|Issue|Report|Action|CapaFinding|CapaEvent|CapaAttachment|FileStorage|Acknowledgement|BaseForm)\b', content))
    
    # Determine risk level
    line_count = len(lines)
    if line_count > 2000 or f in ['app.py', 'models.py']:
        risk = "HIGH"
    elif line_count > 500 or f in ['critical.py', 'actions.py']:
        risk = "MEDIUM-HIGH"
    elif line_count > 100:
        risk = "MEDIUM"
    else:
        risk = "LOW"
        
    file_info[f] = {
        'lines': line_count,
        'routes': len(routes),
        'route_list': routes,
        'templates': len(templates),
        'template_list': sorted(list(templates)),
        'models_count': len(models_referenced),
        'models_list': sorted(list(models_referenced)),
        'risk': risk
    }
    
    print(f"{f:<22} | {line_count:>6} | {len(routes):>6} | {len(templates):>9} | {len(models_referenced):>14} | {risk}")

print("=" * 120)

for f in ['app.py', 'md_dashboard.py', 'statistics_routes.py', 'actions.py', 'critical.py', 'acknowledgements.py', 'report_routes.py']:
    print(f"\n[{f}]")
    print(f"  Templates ({file_info[f]['templates']}): {file_info[f]['template_list']}")
    print(f"  Routes ({file_info[f]['routes']}): {file_info[f]['route_list'][:10]}")
    if len(file_info[f]['route_list']) > 10:
        print(f"  ... and {len(file_info[f]['route_list']) - 10} more routes")

