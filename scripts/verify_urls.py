import django, os, sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ["DJANGO_SETTINGS_MODULE"] = "remedium_hms.settings"
django.setup()
from django.urls import reverse, NoReverseMatch

# All URL names referenced in templates
to_check = [
    # plain names
    ("appointment_delete", [1]),
    ("appointment_list", []),
    ("appointment_create", []),
    ("appointment_detail", [1]),
    ("appointment_update", [1]),
    ("home", []),
    ("integration_list", []),
    ("inventoryitem_list", []),
    ("invoice_list", []),
    ("labtest_list", []),
    ("notification_list", []),
    ("patient_list", []),
    ("prescription_list", []),
    ("report_list", []),
    ("staff_list", []),
    ("surgery_list", []),
    ("user_list", []),
    ("audit_log", []),
    ("invoice_create", []),
    ("patient_create", []),
    ("patient_detail", [1]),
    ("staff_create", []),
    ("integration_delete", [1]),
    ("integration_create", []),
    ("integration_detail", [1]),
    ("integration_update", [1]),
    ("inventoryitem_delete", [1]),
    ("inventoryitem_create", []),
    ("inventoryitem_detail", [1]),
    ("inventoryitem_update", [1]),
    ("invoice_delete", [1]),
    ("invoice_update", [1]),
    ("record_payment", [1]),
    ("invoice_detail", [1]),
    ("labtest_delete", [1]),
    ("labtest_create", []),
    ("labtest_detail", [1]),
    ("labtest_update", [1]),
    ("patient_delete", [1]),
    ("patient_history", [1]),
    ("patient_update", [1]),
    ("patient_document_list", [1]),
    ("patient_document_upload", [1]),
    ("prescription_delete", [1]),
    ("prescription_list", []),
    ("prescription_create", []),
    ("prescription_detail", [1]),
    ("prescription_update", [1]),
    ("report_detail", [1]),
    ("report_download", [1]),
    ("report_generate", []),
    ("shift_create", [1]),
    ("shift_delete", [1]),
    ("staff_delete", [1]),
    ("staff_detail", [1]),
    ("staff_update", [1]),
    ("surgery_delete", [1]),
    ("surgery_create", []),
    ("surgery_detail", [1]),
    ("surgery_update", [1]),
    ("user_create", []),
    ("user_password_reset", [1]),
    ("user_status_toggle", [1]),
    # namespaced
    ("care_monitoring:patientcare_list", []),
    ("care_monitoring:patientcare_create", []),
    ("care_monitoring:patientcare_detail", [1]),
    ("care_monitoring:patientcare_update", [1]),
    ("care_monitoring:patientcare_delete", [1]),
    ("care_monitoring:patient_vital_trends", [1]),
    ("billing:invoice_print", [1]),
    # non-namespaced care_monitoring (used in patientcare_detail.html)
    ("patientcare_list", []),
    ("patientcare_update", [1]),
    ("patientcare_delete", [1]),
    # hospital
    ("ward_list", []),
    ("ward_create", []),
    ("ward_detail", [1]),
    ("ward_update", [1]),
    ("ward_delete", [1]),
    ("room_list", []),
    ("room_create", []),
    ("room_detail", [1]),
    ("room_update", [1]),
    ("room_delete", [1]),
    # integration sync
    ("integration_sync", [1]),
    # auth
    ("login", []),
    ("logout", []),
    ("password_change", []),
    ("password_reset", []),
]

missing = []
for name, args in to_check:
    try:
        reverse(name, args=args) if args else reverse(name)
    except NoReverseMatch:
        missing.append(name)

if missing:
    print("MISSING URLs:")
    for m in missing:
        print(f"  {m}")
else:
    print("All URLs OK!")
