/**
 * Remedium HMS - Appointments Module
 * Handles appointment-related API operations and UI updates
 */

class AppointmentsModule {
    constructor() {
        this.currentPage = 1;
        this.searchQuery = '';
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.loadAppointments();
    }

    setupEventListeners() {
        // Search form
        const searchForm = document.getElementById('appointmentSearchForm');
        if (searchForm) {
            searchForm.addEventListener('submit', (e) => {
                e.preventDefault();
                this.search();
            });
        }

        // Create appointment button
        const createBtn = document.getElementById('createAppointmentBtn');
        if (createBtn) {
            createBtn.addEventListener('click', () => this.showCreateModal());
        }

        // Form submission
        const appointmentForm = document.getElementById('appointmentForm');
        if (appointmentForm) {
            appointmentForm.addEventListener('submit', (e) => {
                e.preventDefault();
                this.submitForm();
            });
        }

        // Status filter
        const statusFilter = document.getElementById('statusFilter');
        if (statusFilter) {
            statusFilter.addEventListener('change', () => this.filterByStatus());
        }
    }

    async loadAppointments(page = 1) {
        AJAXHelpers.showLoader('appointmentsList');
        
        const result = await api.getAppointments({
            search: this.searchQuery,
            page: page
        });

        if (result.success) {
            this.displayAppointments(result.data.results);
            this.displayPagination(result.data, page);
            this.currentPage = page;
        } else {
            AJAXHelpers.showAlert('Error', 'Failed to load appointments', 'danger');
        }
        
        AJAXHelpers.hideLoader('appointmentsList');
    }

    displayAppointments(appointments) {
        const tbody = document.getElementById('appointmentsTableBody');
        if (!tbody) return;

        if (appointments.length === 0) {
            tbody.innerHTML = '<tr><td colspan="5" class="text-center text-muted">No appointments found</td></tr>';
            return;
        }

        let html = '';
        appointments.forEach(apt => {
            const statusBadge = `<span class="badge bg-${this.getStatusColor(apt.status)}">${apt.status}</span>`;
            html += `
                <tr>
                    <td>${apt.patient_detail.full_name}</td>
                    <td>${apt.doctor_detail.full_name}</td>
                    <td>${AJAXHelpers.formatDateTime(apt.appointment_date)}</td>
                    <td>${apt.reason || '-'}</td>
                    <td>${statusBadge}</td>
                    <td>
                        <div class="btn-group btn-group-sm" role="group">
                            <button type="button" class="btn btn-info btn-sm" onclick="appointmentsModule.viewAppointment(${apt.id})">
                                <i class="bi bi-eye"></i>
                            </button>
                            <button type="button" class="btn btn-warning btn-sm" onclick="appointmentsModule.editAppointment(${apt.id})">
                                <i class="bi bi-pencil"></i>
                            </button>
                            <button type="button" class="btn btn-danger btn-sm" onclick="appointmentsModule.deleteAppointment(${apt.id})">
                                <i class="bi bi-trash"></i>
                            </button>
                        </div>
                    </td>
                </tr>
            `;
        });

        tbody.innerHTML = html;
    }

    getStatusColor(status) {
        const colors = {
            'Scheduled': 'primary',
            'Completed': 'success',
            'Cancelled': 'danger'
        };
        return colors[status] || 'secondary';
    }

    displayPagination(response, currentPage) {
        const paginationDiv = document.getElementById('appointmentsPagination');
        if (paginationDiv) {
            paginationDiv.innerHTML = AJAXHelpers.buildPaginationControls(
                response,
                currentPage,
                'appointmentsModule.loadAppointments'
            );
        }
    }

    search() {
        const searchInput = document.getElementById('appointmentSearch');
        if (searchInput) {
            this.searchQuery = searchInput.value;
        }
        this.currentPage = 1;
        this.loadAppointments();
    }

    async filterByStatus() {
        const statusFilter = document.getElementById('statusFilter');
        if (statusFilter && statusFilter.value) {
            this.loadAppointments(1);
        }
    }

    async viewAppointment(id) {
        const result = await api.getAppointment(id);
        
        if (result.success) {
            const apt = result.data;
            const modal = new bootstrap.Modal(document.getElementById('appointmentDetailModal'));
            
            document.getElementById('appointmentDetailContent').innerHTML = `
                <div class="row">
                    <div class="col-md-6">
                        <p><strong>Patient:</strong> ${apt.patient_detail.full_name}</p>
                        <p><strong>Doctor:</strong> ${apt.doctor_detail.full_name}</p>
                        <p><strong>Date & Time:</strong> ${AJAXHelpers.formatDateTime(apt.appointment_date)}</p>
                    </div>
                    <div class="col-md-6">
                        <p><strong>Reason:</strong> ${apt.reason || '-'}</p>
                        <p><strong>Status:</strong> <span class="badge bg-${this.getStatusColor(apt.status)}">${apt.status}</span></p>
                    </div>
                </div>
            `;
            
            modal.show();
        } else {
            AJAXHelpers.showAlert('Error', 'Failed to load appointment', 'danger');
        }
    }

    async editAppointment(id) {
        const result = await api.getAppointment(id);
        
        if (result.success) {
            const apt = result.data;
            AJAXHelpers.populateForm('appointmentForm', apt);
            document.getElementById('appointmentFormTitle').textContent = 'Edit Appointment';
            document.getElementById('appointmentId').value = id;
            
            const modal = new bootstrap.Modal(document.getElementById('appointmentFormModal'));
            modal.show();
        } else {
            AJAXHelpers.showAlert('Error', 'Failed to load appointment', 'danger');
        }
    }

    showCreateModal() {
        AJAXHelpers.clearForm('appointmentForm');
        document.getElementById('appointmentFormTitle').textContent = 'Schedule New Appointment';
        document.getElementById('appointmentId').value = '';
        
        const modal = new bootstrap.Modal(document.getElementById('appointmentFormModal'));
        modal.show();
    }

    async submitForm() {
        const appointmentId = document.getElementById('appointmentId').value;
        const formData = {
            patient: document.querySelector('[name="patient"]').value,
            doctor: document.querySelector('[name="doctor"]').value,
            appointment_date: document.querySelector('[name="appointment_date"]').value,
            reason: document.querySelector('[name="reason"]').value,
            status: document.querySelector('[name="status"]').value
        };

        let result;
        if (appointmentId) {
            result = await api.updateAppointment(appointmentId, formData);
        } else {
            result = await api.createAppointment(formData);
        }

        if (result.success) {
            AJAXHelpers.showToast('Appointment saved successfully!', 'success');
            bootstrap.Modal.getInstance(document.getElementById('appointmentFormModal')).hide();
            this.loadAppointments(this.currentPage);
        } else {
            AJAXHelpers.showToast(`Error: ${result.error}`, 'danger');
        }
    }

    async deleteAppointment(id) {
        AJAXHelpers.confirmDelete('this appointment', async () => {
            const result = await api.deleteAppointment(id);
            
            if (result.success) {
                AJAXHelpers.showToast('Appointment deleted successfully!', 'success');
                this.loadAppointments(this.currentPage);
            } else {
                AJAXHelpers.showToast(`Error: ${result.error}`, 'danger');
            }
            
            bootstrap.Modal.getInstance(document.getElementById('confirmDeleteModal')).hide();
        });
    }
}

// Initialize on page load
let appointmentsModule;
document.addEventListener('DOMContentLoaded', () => {
    appointmentsModule = new AppointmentsModule();
});
