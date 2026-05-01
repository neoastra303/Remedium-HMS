"""
Rewrite all list templates with clean modern structure:
- Fix broken pagination remnants
- Add card wrapper around table
- Add proper empty state
- Fix action button hierarchy (View=outline-primary, Edit=outline-warning, Delete=outline-danger sm)
- Add page header with create button
"""
import pathlib, re

# Config: (template_path, title, icon, context_var, create_url, create_label, columns, row_template, empty_icon, empty_msg)
TEMPLATES = {
    'surgery/templates/surgery/surgery_list.html': {
        'title': 'Surgeries', 'icon': 'bi-scissors', 'ctx': 'surgeries',
        'create_url': 'surgery_create', 'create_label': 'Schedule Surgery',
        'cols': ['Patient', 'Surgeon', 'Procedure', 'Scheduled', 'Status', ''],
        'row': lambda: '''                <tr>
                    <td class="ps-4">{{ surgery.patient }}</td>
                    <td>{{ surgery.surgeon }}</td>
                    <td class="fw-medium">{{ surgery.procedure }}</td>
                    <td class="d-mobile-none">{{ surgery.scheduled_date|date:"M d, Y H:i" }}</td>
                    <td>
                        {% if surgery.status == 'Scheduled' %}<span class="badge bg-primary rounded-pill">{{ surgery.get_status_display }}</span>
                        {% elif surgery.status == 'Completed' %}<span class="badge bg-success rounded-pill">{{ surgery.get_status_display }}</span>
                        {% else %}<span class="badge bg-secondary rounded-pill">{{ surgery.get_status_display }}</span>{% endif %}
                    </td>
                    <td class="pe-4 text-end">
                        <a href="{% url 'surgery_detail' surgery.pk %}" class="btn btn-sm btn-outline-primary"><i class="bi bi-eye"></i></a>
                        <a href="{% url 'surgery_update' surgery.pk %}" class="btn btn-sm btn-outline-warning"><i class="bi bi-pencil"></i></a>
                        <a href="{% url 'surgery_delete' surgery.pk %}" class="btn btn-sm btn-outline-danger"><i class="bi bi-trash"></i></a>
                    </td>
                </tr>''',
        'for_var': 'surgery', 'empty_icon': 'bi-scissors', 'empty_msg': 'No surgeries scheduled.',
    },
    'staff/templates/staff/staff_list.html': {
        'title': 'Staff', 'icon': 'bi-person-badge', 'ctx': 'staff_list',
        'create_url': 'staff_create', 'create_label': 'Add Staff',
        'cols': ['Name', 'Role', 'Department', 'Email', ''],
        'row': lambda: '''                <tr>
                    <td class="ps-4 fw-medium">{{ member.first_name }} {{ member.last_name }}</td>
                    <td>{{ member.get_role_display }}</td>
                    <td class="d-mobile-none text-muted small">{{ member.get_department_display|default:"—" }}</td>
                    <td class="d-mobile-none text-muted small">{{ member.email|default:"—" }}</td>
                    <td class="pe-4 text-end">
                        <a href="{% url 'staff_detail' member.pk %}" class="btn btn-sm btn-outline-primary"><i class="bi bi-eye"></i></a>
                        <a href="{% url 'staff_update' member.pk %}" class="btn btn-sm btn-outline-warning"><i class="bi bi-pencil"></i></a>
                        <a href="{% url 'staff_delete' member.pk %}" class="btn btn-sm btn-outline-danger"><i class="bi bi-trash"></i></a>
                    </td>
                </tr>''',
        'for_var': 'member', 'empty_icon': 'bi-person-badge', 'empty_msg': 'No staff members found.',
    },
    'appointments/templates/appointments/appointment_list.html': {
        'title': 'Appointments', 'icon': 'bi-calendar-event', 'ctx': 'appointments',
        'create_url': 'appointment_create', 'create_label': 'Book Appointment',
        'cols': ['Patient', 'Doctor', 'Date & Time', 'Status', ''],
        'row': lambda: '''                <tr>
                    <td class="ps-4 fw-medium">{{ appointment.patient }}</td>
                    <td>{{ appointment.doctor }}</td>
                    <td>{{ appointment.appointment_date|date:"M d, Y H:i" }}</td>
                    <td>
                        {% if appointment.status == 'Scheduled' %}<span class="badge bg-primary rounded-pill">{{ appointment.get_status_display }}</span>
                        {% elif appointment.status == 'Completed' %}<span class="badge bg-success rounded-pill">{{ appointment.get_status_display }}</span>
                        {% else %}<span class="badge bg-secondary rounded-pill">{{ appointment.get_status_display }}</span>{% endif %}
                    </td>
                    <td class="pe-4 text-end">
                        <a href="{% url 'appointment_detail' appointment.pk %}" class="btn btn-sm btn-outline-primary"><i class="bi bi-eye"></i></a>
                        <a href="{% url 'appointment_update' appointment.pk %}" class="btn btn-sm btn-outline-warning"><i class="bi bi-pencil"></i></a>
                        <a href="{% url 'appointment_delete' appointment.pk %}" class="btn btn-sm btn-outline-danger"><i class="bi bi-trash"></i></a>
                    </td>
                </tr>''',
        'for_var': 'appointment', 'empty_icon': 'bi-calendar-x', 'empty_msg': 'No appointments scheduled.',
    },
    'laboratory/templates/laboratory/labtest_list.html': {
        'title': 'Lab Tests', 'icon': 'bi-microscope', 'ctx': 'lab_tests',
        'create_url': 'labtest_create', 'create_label': 'Order Test',
        'cols': ['Patient', 'Test', 'Requested', 'Status', ''],
        'row': lambda: '''                <tr>
                    <td class="ps-4 fw-medium">{{ test.patient }}</td>
                    <td>{{ test.test_name }}</td>
                    <td class="d-mobile-none text-muted small">{{ test.requested_date|date:"M d, Y" }}</td>
                    <td><span class="badge bg-secondary rounded-pill">{{ test.get_status_display }}</span></td>
                    <td class="pe-4 text-end">
                        <a href="{% url 'labtest_detail' test.pk %}" class="btn btn-sm btn-outline-primary"><i class="bi bi-eye"></i></a>
                        <a href="{% url 'labtest_update' test.pk %}" class="btn btn-sm btn-outline-warning"><i class="bi bi-pencil"></i></a>
                        <a href="{% url 'labtest_delete' test.pk %}" class="btn btn-sm btn-outline-danger"><i class="bi bi-trash"></i></a>
                    </td>
                </tr>''',
        'for_var': 'test', 'empty_icon': 'bi-microscope', 'empty_msg': 'No lab tests ordered.',
    },
    'pharmacy/templates/pharmacy/prescription_list.html': {
        'title': 'Prescriptions', 'icon': 'bi-capsule', 'ctx': 'prescriptions',
        'create_url': 'prescription_create', 'create_label': 'New Prescription',
        'cols': ['Patient', 'Drug', 'Dosage', 'Date', ''],
        'row': lambda: '''                <tr>
                    <td class="ps-4 fw-medium">{{ prescription.patient }}</td>
                    <td>{{ prescription.drug_name }}</td>
                    <td class="d-mobile-none text-muted small">{{ prescription.dosage }}</td>
                    <td class="d-mobile-none text-muted small">{{ prescription.prescribed_date|date:"M d, Y" }}</td>
                    <td class="pe-4 text-end">
                        <a href="{% url 'prescription_detail' prescription.pk %}" class="btn btn-sm btn-outline-primary"><i class="bi bi-eye"></i></a>
                        <a href="{% url 'prescription_update' prescription.pk %}" class="btn btn-sm btn-outline-warning"><i class="bi bi-pencil"></i></a>
                        <a href="{% url 'prescription_delete' prescription.pk %}" class="btn btn-sm btn-outline-danger"><i class="bi bi-trash"></i></a>
                    </td>
                </tr>''',
        'for_var': 'prescription', 'empty_icon': 'bi-capsule', 'empty_msg': 'No prescriptions found.',
    },
    'inventory/templates/inventory/inventoryitem_list.html': {
        'title': 'Inventory', 'icon': 'bi-box-seam', 'ctx': 'inventory_items',
        'create_url': 'inventoryitem_create', 'create_label': 'Add Item',
        'cols': ['Name', 'Category', 'Quantity', 'Status', ''],
        'row': lambda: '''                <tr>
                    <td class="ps-4 fw-medium">{{ item.name }}</td>
                    <td class="d-mobile-none">{{ item.get_category_display }}</td>
                    <td>{{ item.quantity }} {{ item.get_unit_display }}</td>
                    <td>
                        {% if item.needs_reorder %}<span class="badge bg-warning text-dark rounded-pill">Reorder</span>
                        {% elif item.is_expired %}<span class="badge bg-danger rounded-pill">Expired</span>
                        {% else %}<span class="badge bg-success rounded-pill">OK</span>{% endif %}
                    </td>
                    <td class="pe-4 text-end">
                        <a href="{% url 'inventoryitem_detail' item.pk %}" class="btn btn-sm btn-outline-primary"><i class="bi bi-eye"></i></a>
                        <a href="{% url 'inventoryitem_update' item.pk %}" class="btn btn-sm btn-outline-warning"><i class="bi bi-pencil"></i></a>
                        <a href="{% url 'inventoryitem_delete' item.pk %}" class="btn btn-sm btn-outline-danger"><i class="bi bi-trash"></i></a>
                    </td>
                </tr>''',
        'for_var': 'item', 'empty_icon': 'bi-box-seam', 'empty_msg': 'No inventory items found.',
    },
    'care_monitoring/templates/care_monitoring/patientcare_list.html': {
        'title': 'Care Monitoring', 'icon': 'bi-heart-pulse', 'ctx': 'patientcares',
        'create_url': 'care_monitoring:patientcare_create', 'create_label': 'New Record',
        'cols': ['Patient', 'Status', 'Date', 'HR', 'Temp', ''],
        'row': lambda: '''                <tr>
                    <td class="ps-4 fw-medium">{{ patientcare.patient }}</td>
                    <td>
                        {% if patientcare.status == 'CRITICAL' %}<span class="badge bg-danger rounded-pill">{{ patientcare.get_status_display }}</span>
                        {% elif patientcare.status == 'STABLE' %}<span class="badge bg-success rounded-pill">{{ patientcare.get_status_display }}</span>
                        {% else %}<span class="badge bg-secondary rounded-pill">{{ patientcare.get_status_display }}</span>{% endif %}
                    </td>
                    <td class="d-mobile-none text-muted small">{{ patientcare.monitoring_date|date:"M d, H:i" }}</td>
                    <td class="d-mobile-none">{% if patientcare.heart_rate %}{{ patientcare.heart_rate }} bpm{% else %}—{% endif %}</td>
                    <td class="d-mobile-none">{% if patientcare.temperature %}{{ patientcare.temperature }}°C{% else %}—{% endif %}</td>
                    <td class="pe-4 text-end">
                        <a href="{% url 'care_monitoring:patientcare_detail' patientcare.pk %}" class="btn btn-sm btn-outline-primary"><i class="bi bi-eye"></i></a>
                        <a href="{% url 'care_monitoring:patientcare_update' patientcare.pk %}" class="btn btn-sm btn-outline-warning"><i class="bi bi-pencil"></i></a>
                        <a href="{% url 'care_monitoring:patientcare_delete' patientcare.pk %}" class="btn btn-sm btn-outline-danger"><i class="bi bi-trash"></i></a>
                    </td>
                </tr>''',
        'for_var': 'patientcare', 'empty_icon': 'bi-heart-pulse', 'empty_msg': 'No care records found.',
    },
    'reporting/templates/reporting/report_list.html': {
        'title': 'Reports', 'icon': 'bi-bar-chart', 'ctx': 'reports',
        'create_url': 'report_generate', 'create_label': 'New Report',
        'cols': ['Title', 'Type', 'Created', ''],
        'row': lambda: '''                <tr>
                    <td class="ps-4 fw-medium">{{ report.title }}</td>
                    <td>{{ report.report_type }}</td>
                    <td class="d-mobile-none text-muted small">{{ report.created_at|date:"M d, Y" }}</td>
                    <td class="pe-4 text-end">
                        <a href="{% url 'report_detail' report.pk %}" class="btn btn-sm btn-outline-primary"><i class="bi bi-eye"></i></a>
                        <a href="{% url 'report_download' report.pk %}" class="btn btn-sm btn-outline-success"><i class="bi bi-download"></i></a>
                        <a href="{% url 'report_delete' report.pk %}" class="btn btn-sm btn-outline-danger"><i class="bi bi-trash"></i></a>
                    </td>
                </tr>''',
        'for_var': 'report', 'empty_icon': 'bi-bar-chart', 'empty_msg': 'No reports generated yet.',
    },
    'integration/templates/integration/integration_list.html': {
        'title': 'Integrations', 'icon': 'bi-plug', 'ctx': 'integrations',
        'create_url': 'integration_create', 'create_label': 'Add Integration',
        'cols': ['System', 'Type', 'Status', 'Last Sync', ''],
        'row': lambda: '''                <tr>
                    <td class="ps-4 fw-medium">{{ integration.system_name }}</td>
                    <td class="d-mobile-none">{{ integration.get_system_type_display }}</td>
                    <td>
                        {% if integration.status == 'Active' %}<span class="badge bg-success rounded-pill">Active</span>
                        {% else %}<span class="badge bg-secondary rounded-pill">{{ integration.status }}</span>{% endif %}
                    </td>
                    <td class="d-mobile-none text-muted small">{{ integration.last_sync|date:"M d, H:i"|default:"Never" }}</td>
                    <td class="pe-4 text-end">
                        <a href="{% url 'integration_detail' integration.pk %}" class="btn btn-sm btn-outline-primary"><i class="bi bi-eye"></i></a>
                        <a href="{% url 'integration_update' integration.pk %}" class="btn btn-sm btn-outline-warning"><i class="bi bi-pencil"></i></a>
                        <a href="{% url 'integration_delete' integration.pk %}" class="btn btn-sm btn-outline-danger"><i class="bi bi-trash"></i></a>
                    </td>
                </tr>''',
        'for_var': 'integration', 'empty_icon': 'bi-plug', 'empty_msg': 'No integrations configured.',
    },
}

TEMPLATE = """{{% extends 'base.html' %}}
{{% block content %}}
<div class="d-flex justify-content-between align-items-center mb-4">
    <h4 class="fw-bold mb-0"><i class="bi {icon} me-2 text-primary"></i>{title}</h4>
    <a href="{{% url '{create_url}' %}}" class="btn btn-sm btn-primary"><i class="bi bi-plus-circle me-1"></i>{create_label}</a>
</div>

<div class="card border-0 shadow-sm" style="background:#fff;">
    <div class="table-responsive">
        <table class="table table-hover align-middle mb-0">
            <thead class="table-light">
                <tr>
{header_cols}
                </tr>
            </thead>
            <tbody>
                {{% for {for_var} in {ctx} %}}
{row}
                {{% empty %}}
                {{% include 'partials/empty_state.html' with icon="{empty_icon}" message="{empty_msg}" colspan="{colspan}" %}}
                {{% endfor %}}
            </tbody>
        </table>
    </div>
</div>

{{% include 'partials/pagination.html' %}}
{{% endblock %}}
"""

for path, cfg in TEMPLATES.items():
    cols = cfg['cols']
    header_cols = '\n'.join(
        f'                    <th class="{"ps-4 " if i == 0 else ""}{"pe-4 text-end" if i == len(cols)-1 else "d-mobile-none" if i > 1 else ""}">{c}</th>'
        for i, c in enumerate(cols)
    )
    content = TEMPLATE.format(
        icon=cfg['icon'], title=cfg['title'], create_url=cfg['create_url'],
        create_label=cfg['create_label'], header_cols=header_cols,
        for_var=cfg['for_var'], ctx=cfg['ctx'],
        row=cfg['row'](), empty_icon=cfg['empty_icon'],
        empty_msg=cfg['empty_msg'], colspan=len(cols),
    )
    pathlib.Path(path).write_text(content, encoding='utf-8')
    print(f'Written: {path}')
