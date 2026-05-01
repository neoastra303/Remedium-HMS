import django, os
os.environ['DJANGO_SETTINGS_MODULE'] = 'remedium_hms.settings'
django.setup()
from django.urls import reverse, NoReverseMatch
names = ['appointment_list','labtest_list','surgery_list','staff_list',
         'inventoryitem_list','prescription_list','integration_list',
         'report_list','notification_list','invoice_list','patient_list','home']
for n in names:
    try:
        print(f'OK: {n} -> {reverse(n)}')
    except NoReverseMatch:
        print(f'MISSING: {n}')
