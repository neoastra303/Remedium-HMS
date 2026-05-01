import pathlib
f = pathlib.Path('remedium_hms/settings.py')
txt = f.read_text(encoding='utf-8')
old = "    'ENUM_NAME_OVERRIDES': {\n        'PatientGenderEnum': 'patients.models.Patient.GENDER_CHOICES',\n    },"
new = """    'ENUM_NAME_OVERRIDES': {
        'PatientGenderEnum': 'patients.models.Patient.GENDER_CHOICES',
        'AppointmentStatusEnum': [('Scheduled', 'Scheduled'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled')],
        'SurgeryStatusEnum': [('Scheduled', 'Scheduled'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled')],
        'PatientCareStatusEnum': 'care_monitoring.models.PatientCare.STATUS_CHOICES',
        'NotificationStatusEnum': 'notifications.models.Notification.STATUSES',
    },"""
if old in txt:
    f.write_text(txt.replace(old, new), encoding='utf-8')
    print('Done')
else:
    print('Pattern not found')
    print(repr(txt[txt.find("ENUM_NAME"):txt.find("ENUM_NAME")+200]))
