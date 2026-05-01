"""Fix float validators to Decimal in care_monitoring/models.py"""
import pathlib
from decimal import Decimal

f = pathlib.Path('care_monitoring/models.py')
txt = f.read_text(encoding='utf-8')

# Add Decimal import
if 'from decimal import Decimal' not in txt:
    txt = txt.replace(
        'from django.core.validators import MinValueValidator, MaxValueValidator',
        'from decimal import Decimal\nfrom django.core.validators import MinValueValidator, MaxValueValidator'
    )

# Replace float validator values with Decimal
replacements = [
    ('MinValueValidator(35.0)', 'MinValueValidator(Decimal("35.0"))'),
    ('MaxValueValidator(45.0)', 'MaxValueValidator(Decimal("45.0"))'),
    ('MinValueValidator(0.00)', 'MinValueValidator(Decimal("0.00"))'),
    ('MaxValueValidator(100.00)', 'MaxValueValidator(Decimal("100.00"))'),
    ('MinValueValidator(0.1)', 'MinValueValidator(Decimal("0.1"))'),
    ('MaxValueValidator(500.0)', 'MaxValueValidator(Decimal("500.0"))'),
    ('MaxValueValidator(250.0)', 'MaxValueValidator(Decimal("250.0"))'),
]
for old, new in replacements:
    txt = txt.replace(old, new)

f.write_text(txt, encoding='utf-8')
print('Done')
