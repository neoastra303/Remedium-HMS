def user_roles(request):
    """
    Adds user role identification flags to all templates.
    """
    if not request.user.is_authenticated:
        return {}

    is_admin = request.user.is_superuser or request.user.groups.filter(name='Admin').exists()
    is_doctor = request.user.groups.filter(name='Doctor').exists()
    is_nurse = request.user.groups.filter(name='Nurse').exists()
    is_receptionist = request.user.groups.filter(name='Receptionist').exists()
    is_pharmacist = request.user.groups.filter(name='Pharmacist').exists()
    is_lab_tech = request.user.groups.filter(name='Lab Technician').exists()

    # If the user is linked to a staff profile, use that as secondary check
    staff_profile = getattr(request.user, 'staff_profile', None)
    if staff_profile:
        if staff_profile.role == 'DOCTOR': is_doctor = True
        if staff_profile.role == 'NURSE': is_nurse = True
        if staff_profile.role == 'ADMIN': is_admin = True
        if staff_profile.role == 'RECEPTIONIST': is_receptionist = True
        if staff_profile.role == 'PHARMACIST': is_pharmacist = True
        if staff_profile.role == 'LAB_TECH': is_lab_tech = True

    return {
        'is_hms_admin': is_admin,
        'is_hms_doctor': is_doctor,
        'is_hms_nurse': is_nurse,
        'is_hms_receptionist': is_receptionist,
        'is_hms_pharmacist': is_pharmacist,
        'is_hms_lab_tech': is_lab_tech,
    }
