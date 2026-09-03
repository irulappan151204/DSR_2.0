import glob
import re

html_files = glob.glob('templates/**/*.html', recursive=True) + glob.glob('static/**/*.js', recursive=True)
url_for_submits = []
action_submits = []

for hf in html_files:
    with open(hf, 'r', encoding='utf-8', errors='ignore') as fp:
        c = fp.read()
    for m in re.finditer(r'url_for\([\'"]([^\'"]*submit[^\'"]*)[\'"]', c):
        url_for_submits.append((hf, m.group(1)))
    for m in re.finditer(r'[\'"](/submit[^\'"]*)[\'"]', c):
        action_submits.append((hf, m.group(1)))

print(f"Templates/JS using url_for with submit: {len(url_for_submits)}")
for u in url_for_submits:
    print(" ", u)
print(f"Templates/JS using literal /submit_*: {len(action_submits)}")
for a in action_submits[:10]:
    print(" ", a)
