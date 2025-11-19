/**
 * Remedium HMS - Patients Module
 * Handles patient-related API operations and UI updates
 */

class PatientsModule {
    constructor() {
        this.currentPage = 1;
        this.searchQuery = '';
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.loadPatients();
    }

    setupEventListeners() {
        // Search form
        const searchForm = document.getElementById('patientSearchForm');
        if (searchForm) {
            searchForm.addEventListener('submit', (e) => {
                e.preventDefault();
                this.search();
            });
        }

        // Create patient button
        const createBtn = document.getElementById('createPatientBtn');
        if (createBtn) {
            createBtn.addEventListener('click', () => this.showCreateModal());
        }

        // Form submission
        const patientForm = document.getElementById('patientForm');
        if (patientForm) {
            patientForm.addEventListener('submit', (e) => {
                e.preventDefault();
                this.submitForm();
            });
        }
    }

    async loadPatients(page = 1) {
        AJAXHelpers.showLoader('patientsList');
        
        const result = await api.getPatients({
            search: this.searchQuery,
            page: page
        });

        if (result.success) {
            this.displayPatients(result.data.results);
            this.displayPagination(result.data, page);
            this.currentPage = page;
        } else {
            AJAXHelpers.showAlert('Error', 'Failed to load patients', 'danger');
        }
        
        AJAXHelpers.hideLoader('patientsList');
    }

    displayPatients(patients) {
        const tbody = document.getElementById('patientsTableBody');
        if (!tbody) return;

        const columns = [
            { key: 'unique_id', type: 'text' },
            { key: 'full_name', type: 'text' },
            { key: 'date_of_birth', type: 'date' },
            { key: 'gender', type: 'text' },
            { key: 'phone', type: 'text' },
            { key: 'email', type: 'text' }
        ];

        const actionHtml = (patient) => `
            <div class="btn-group btn-group-sm" role="group">
                <button type="button" class="btn btn-info btn-sm" onclick="patientsModule.viewPatient(${patient.id})">
                    <i class="bi bi-eye"></i> View
                </button>
                <button type="button" class="btn btn-warning btn-sm" onclick="patientsModule.editPatient(${patient.id})">
                    <i class="bi bi-pencil"></i> Edit
                </button>
                <button type="button" class="btn btn-danger btn-sm" onclick="patientsModule.deletePatient(${patient.id}, '${patient.full_name}')">
                    <i class="bi bi-trash"></i> Delete
                </button>
            </div>
        `;

        tbody.innerHTML = AJAXHelpers.buildTableRows(patients, columns, actionHtml);
    }

    displayPagination(response, currentPage) {
        const paginationDiv = document.getElementById('patientsPagination');
        if (paginationDiv) {
            paginationDiv.innerHTML = AJAXHelpers.buildPaginationControls(
                response,
                currentPage,
                'patientsModule.loadPatients'
            );
        }
    }

    search() {
        const searchInput = document.getElementById('patientSearch');
        if (searchInput) {
            this.searchQuery = searchInput.value;
        }
        this.currentPage = 1;
        this.loadPatients();
    }

    async viewPatient(id) {
        const result = await api.getPatient(id);
        
        if (result.success) {
            const patient = result.data;
            const modal = new bootstrap.Modal(document.getElementById('patientDetailModal'));
            
            document.getElementById('patientDetailContent').innerHTML = `
                <div class="row">
                    <div class="col-md-6">
                        <p><strong>ID:</strong> ${patient.unique_id}</p>
                        <p><strong>Name:</strong> ${patient.full_name}</p>
                        <p><strong>DOB:</strong> ${AJAXHelpers.formatDate(patient.date_of_birth)}</p>
                        <p><strong>Age:</strong> ${patient.age} years</p>
                        <p><strong>Gender:</strong> ${patient.gender}</p>
                    </div>
                    <div class="col-md-6">
                        <p><strong>Phone:</strong> ${AJAXHelpers.formatPhoneNumber(patient.phone)}</p>
                        <p><strong>Email:</strong> ${patient.email || '-'}</p>
                        <p><strong>Insurance:</strong> ${patient.insurance_provider || '-'}</p>
                        <p><strong>Status:</strong> ${patient.is_admitted ? '<span class="badge bg-danger">Admitted</span>' : '<span class="badge bg-success">Discharged</span>'}</p>
                    </div>
                </div>
                <hr>
                <p><strong>Medical History:</strong></p>
                <p>${patient.medical_history || 'No medical history recorded'}</p>
                ${patient.is_admitted ? `<button class="btn btn-warning" onclick="patientsModule.dischargePatient(${patient.id})">Discharge Patient</button>` : ''}
            `;
            
            modal.show();
        } else {
            AJAXHelpers.showAlert('Error', 'Failed to load patient details', 'danger');
        }
    }

    async editPatient(id) {
        const result = await api.getPatient(id);
        
        if (result.success) {
            const patient = result.data;
            AJAXHelpers.populateForm('patientForm', patient);
            document.getElementById('patientFormTitle').textContent = 'Edit Patient';
            document.getElementById('patientId').value = id;
            
            const modal = new bootstrap.Modal(document.getElementById('patientFormModal'));
            modal.show();
        } else {
            AJAXHelpers.showAlert('Error', 'Failed to load patient', 'danger');
        }
    }

    showCreateModal() {
        AJAXHelpers.clearForm('patientForm');
        document.getElementById('patientFormTitle').textContent = 'Create New Patient';
        document.getElementById('patientId').value = '';
        
        const modal = new bootstrap.Modal(document.getElementById('patientFormModal'));
        modal.show();
    }

    async submitForm() {
        const patientId = document.getElementById('patientId').value;
        const formData = {
            unique_id: document.querySelector('[name="unique_id"]').value,
            first_name: document.querySelector('[name="first_name"]').value,
            last_name: document.querySelector('[name="last_name"]').value,
            date_of_birth: document.querySelector('[name="date_of_birth"]').value,
            gender: document.querySelector('[name="gender"]').value,
            phone: document.querySelector('[name="phone"]').value,
            email: document.querySelector('[name="email"]').value,
            medical_history: document.querySelector('[name="medical_history"]').value
        };

        let result;
        if (patientId) {
            result = await api.updatePatient(patientId, formData);
        } else {
            result = await api.createPatient(formData);
        }

        if (result.success) {
            AJAXHelpers.showToast('Patient saved successfully!', 'success');
            bootstrap.Modal.getInstance(document.getElementById('patientFormModal')).hide();
            this.loadPatients(this.currentPage);
        } else {
            AJAXHelpers.showToast(`Error: ${result.error}`, 'danger');
        }
    }

    async deletePatient(id, name) {
        AJAXHelpers.confirmDelete(name, async () => {
            const result = await api.deletePatient(id);
            
            if (result.success) {
                AJAXHelpers.showToast('Patient deleted successfully!', 'success');
                this.loadPatients(this.currentPage);
            } else {
                AJAXHelpers.showToast(`Error: ${result.error}`, 'danger');
            }
            
            bootstrap.Modal.getInstance(document.getElementById('confirmDeleteModal')).hide();
        });
    }

    async dischargePatient(id) {
        if (confirm('Are you sure you want to discharge this patient?')) {
            const result = await api.dischargePatient(id);
            
            if (result.success) {
                AJAXHelpers.showToast('Patient discharged successfully!', 'success');
                this.loadPatients(this.currentPage);
            } else {
                AJAXHelpers.showToast(`Error: ${result.error}`, 'danger');
            }
        }
    }
}

// Initialize on page load
let patientsModule;
document.addEventListener('DOMContentLoaded', () => {
    patientsModule = new PatientsModule();
});
