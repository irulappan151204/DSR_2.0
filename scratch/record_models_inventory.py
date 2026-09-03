import sys
sys.path.insert(0, '.')

import inspect
import json
import re
import glob
import models
from extensions import db

print("=" * 80)
print("RECORDING COMPREHENSIVE BASELINE INVENTORY OF models.py")
print("=" * 80)

# 1. Inventory all model classes
model_classes = {}
for name, cls in inspect.getmembers(models, inspect.isclass):
    if cls.__module__ == 'models' and issubclass(cls, db.Model):
        table_name = getattr(cls, '__tablename__', None)
        cols = []
        pks = []
        fks = []
        relationships = []
        
        # Inspect columns via SQLAlchemy mapper if mapped
        try:
            mapper = cls.__mapper__
            for col in mapper.column_attrs:
                col_obj = col.columns[0]
                cols.append({
                    'name': col_obj.name,
                    'type': str(col_obj.type),
                    'nullable': col_obj.nullable,
                    'primary_key': col_obj.primary_key
                })
                if col_obj.primary_key:
                    pks.append(col_obj.name)
                for fk in col_obj.foreign_keys:
                    fks.append({
                        'column': col_obj.name,
                        'target': str(fk.target_fullname)
                    })
            for rel in mapper.relationships:
                relationships.append({
                    'name': rel.key,
                    'target': rel.target.name,
                    'uselist': rel.uselist
                })
        except Exception as e:
            # BaseForm or unmapped
            pass
            
        model_classes[name] = {
            'class_name': name,
            'table_name': table_name,
            'columns_count': len(cols),
            'columns': cols,
            'pks': pks,
            'fks': fks,
            'relationships': relationships
        }

print(f"Total SQLAlchemy Model Classes Inventoried: {len(model_classes)}")

# Also record BaseForm
if hasattr(models, 'BaseForm'):
    model_classes['BaseForm'] = {
        'class_name': 'BaseForm',
        'table_name': getattr(models.BaseForm, '__tablename__', None),
        'is_base': True
    }
    print("Inventoried BaseForm abstract class.")

# 2. Record all external files importing from models
external_imports = {}
py_files = sorted([f for f in glob.glob('*.py') + glob.glob('*/*.py') if 'venv' not in f and not f.startswith('scratch')])
for pf in py_files:
    with open(pf, 'r', encoding='utf-8', errors='ignore') as fp:
        content = fp.read()
    matches = re.findall(r'from\s+models\s+import\s+([^\n]+)', content)
    if matches:
        imported_symbols = []
        for m in matches:
            # Clean comments and multi-imports
            cleaned = m.split('#')[0].replace('(', '').replace(')', '')
            for s in cleaned.split(','):
                sym = s.strip()
                if sym:
                    imported_symbols.append(sym)
        external_imports[pf] = imported_symbols

print(f"Total External Files with 'from models import ...': {len(external_imports)}")
for f, syms in external_imports.items():
    print(f"  {f:<25} imports {len(syms)} symbols: {syms[:5]} ...")

inventory_data = {
    'total_classes': len(model_classes),
    'classes': model_classes,
    'external_imports': external_imports
}

with open('scratch/models_baseline_inventory.json', 'w', encoding='utf-8') as fp:
    json.dump(inventory_data, fp, indent=2)

print("\nInventory saved to scratch/models_baseline_inventory.json successfully.")
