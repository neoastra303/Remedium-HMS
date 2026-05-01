"""Replace bare form rendering with crispy forms in all *_form.html templates."""
import pathlib, re

CRISPY_TEMPLATE = """{{% extends 'base.html' %}}
{{% load crispy_forms_tags %}}

{{% block content %}}
<div class="row justify-content-center">
    <div class="col-lg-8">
        <div class="card border-0 shadow-sm">
            <div class="card-header bg-white border-0 py-3 px-4">
                <h5 class="fw-bold mb-0">
                    <i class="bi bi-pencil-square me-2 text-primary"></i>{title}
                </h5>
            </div>
            <div class="card-body p-4">
                <form method="post"{enctype} novalidate>
                    {{% csrf_token %}}
                    {{% crispy form %}}
                </form>
            </div>
        </div>
    </div>
</div>
{{% endblock %}}
"""

forms_to_fix = {
    'appointments/templates/appointments/appointment_form.html': ('Appointment', ''),
    'billing/templates/billing/invoice_form.html': ('Invoice', ''),
    'billing/templates/billing/payment_form.html': ('Record Payment', ''),
    'care_monitoring/templates/care_monitoring/patientcare_form.html': ('Patient Care Record', ''),
    'inventory/templates/inventory/inventoryitem_form.html': ('Inventory Item', ''),
    'laboratory/templates/laboratory/labtest_form.html': ('Lab Test', ''),
    'medical_records/templates/medical_records/patient_document_form.html': ('Upload Document', ' enctype="multipart/form-data"'),
    'pharmacy/templates/pharmacy/prescription_form.html': ('Prescription', ''),
    'reporting/templates/reporting/report_form.html': ('Report', ''),
    'surgery/templates/surgery/surgery_form.html': ('Surgery', ''),
}

for path, (title, enctype) in forms_to_fix.items():
    f = pathlib.Path(path)
    if not f.exists():
        print(f'SKIP: {path}')
        continue
    content = f.read_text(encoding='utf-8')
    # Only rewrite if it doesn't already use crispy
    if 'crispy_forms_tags' not in content:
        f.write_text(CRISPY_TEMPLATE.format(title=title, enctype=enctype), encoding='utf-8')
        print(f'Fixed: {path}')
    else:
        print(f'Already crispy: {path}')
