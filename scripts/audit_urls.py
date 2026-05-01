import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'remedium_hms.settings'
os.environ['SECRET_KEY'] = 'test-key-audit'
import django
django.setup()
from django.urls import reverse, NoReverseMatch

names = [
    'appointment_list', 'labtest_list', 'surgery_list', 'staff_list',
    'inventoryitem_list', 'prescription_list', 'patient_document_list',
    'integration_list', 'report_list', 'notification_list',
    'invoice_list', 'patient_list',
]
for n in names:
    try:
        reverse(n)
        print(f'OK: {n}')
    except NoReverseMatch:
        print(f'MISSING: {n}')
