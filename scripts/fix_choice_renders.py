"""Fix raw choice field renders across templates."""

import pathlib, re

fixes = [
    # (file, old, new)
    (
        "patients/templates/patients/patient_detail.html",
        "{{ patient.gender }}",
        "{{ patient.get_gender_display }}",
    ),
    (
        "staff/templates/staff/staff_detail.html",
        "{{ staff.role }}",
        "{{ staff.get_role_display }}",
    ),
    (
        "staff/templates/staff/staff_list.html",
        "{{ member.role }}",
        "{{ member.get_role_display }}",
    ),
    (
        "appointments/templates/appointments/appointment_list.html",
        "{{ appointment.status }}",
        "{{ appointment.get_status_display }}",
    ),
    (
        "billing/templates/billing/invoice_list.html",
        "{{ invoice.status }}",
        '{% if invoice.paid %}<span class="badge bg-success rounded-pill">Paid</span>{% else %}<span class="badge bg-warning text-dark rounded-pill">Unpaid</span>{% endif %}',
    ),
    (
        "laboratory/templates/laboratory/labtest_detail.html",
        "{{ lab_test.status }}",
        "{{ lab_test.get_status_display }}",
    ),
    (
        "laboratory/templates/laboratory/labtest_list.html",
        "{{ test.status }}",
        "{{ test.get_status_display }}",
    ),
    (
        "surgery/templates/surgery/surgery_detail.html",
        "{{ surgery.status }}",
        "{{ surgery.get_status_display }}",
    ),
    (
        "surgery/templates/surgery/surgery_list.html",
        "{{ surgery.status }}",
        "{{ surgery.get_status_display }}",
    ),
]

for path, old, new in fixes:
    f = pathlib.Path(path)
    if not f.exists():
        print(f"SKIP (not found): {path}")
        continue
    txt = f.read_text(encoding="utf-8")
    if old in txt:
        f.write_text(txt.replace(old, new), encoding="utf-8")
        print(f"Fixed: {path}")
    else:
        print(f"Already fixed or not found: {path}")
