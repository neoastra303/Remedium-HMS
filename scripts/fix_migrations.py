import pathlib, re

files = [
    'inventory/migrations/0003_inventoryitem_cost_per_unit_and_more.py',
    'patients/migrations/0004_alter_patient_address_alter_patient_admission_date_and_more.py',
]
for path in files:
    f = pathlib.Path(path)
    txt = f.read_text(encoding='utf-8')
    # Replace check= with condition= in CheckConstraint
    new = re.sub(r'CheckConstraint\(\s*check=', 'CheckConstraint(\n                condition=', txt)
    if new != txt:
        f.write_text(new, encoding='utf-8')
        print(f'Fixed: {path}')
    else:
        print(f'No change: {path}')
