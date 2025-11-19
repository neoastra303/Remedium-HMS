/**
 * Remedium HMS - Staff Module
 * Handles staff-related API operations and UI updates
 */

class StaffModule {
    constructor() {
        this.currentPage = 1;
        this.searchQuery = '';
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.loadStaff();
    }

    setupEventListeners() {
        // Search form
        const searchForm = document.getElementById('staffSearchForm');
        if (searchForm) {
            searchForm.addEventListener('submit', (e) => {
                e.preventDefault();
                this.search();
            });
        }

        // Create staff button
        const createBtn = document.getElementById('createStaffBtn');
        if (createBtn) {
            createBtn.addEventListener('click', () => this.showCreateModal());
        }

        // Form submission
        const staffForm = document.getElementById('staffForm');
        if (staffForm) {
            staffForm.addEventListener('submit', (e) => {
                e.preventDefault();
                this.submitForm();
            });
        }

        // Department filter
        const departmentFilter = document.getElementById('departmentFilter');
        if (departmentFilter) {
            departmentFilter.addEventListener('change', () => this.filterByDepartment());
        }
    }

    async loadStaff(page = 1) {
        AJAXHelpers.showLoader('staffList');
        
        const result = await api.getStaff({
            search: this.searchQuery,
            page: page
        });

        if (result.success) {
            this.displayStaff(result.data.results);
            this.displayPagination(result.data, page);
            this.currentPage = page;
        } else {
            AJAXHelpers.showAlert('Error', 'Failed to load staff', 'danger');
        }
        
        AJAXHelpers.hideLoader('staffList');
    }

    displayStaff(staff) {
        const tbody = document.getElementById('staffTableBody');
        if (!tbody) return;

        const columns = [
            { key: 'staff_id', type: 'text' },
            { key: 'full_name', type: 'text' },
            { key: 'role', type: 'text' },
            { key: 'department', type: 'text' },
            { key: 'phone', type: 'text' },
            { key: 'email', type: 'text' }
        ];

        const actionHtml = (member) => `
            <div class="btn-group btn-group-sm" role="group">
                <button type="button" class="btn btn-info btn-sm" onclick="staffModule.viewStaff(${member.id})">
                    <i class="bi bi-eye"></i> View
                </button>
                <button type="button" class="btn btn-warning btn-sm" onclick="staffModule.editStaff(${member.id})">
                    <i class="bi bi-pencil"></i> Edit
                </button>
                <button type="button" class="btn btn-danger btn-sm" onclick="staffModule.deleteStaff(${member.id}, '${member.full_name}')">
                    <i class="bi bi-trash"></i> Delete
                </button>
            </div>
        `;

        tbody.innerHTML = AJAXHelpers.buildTableRows(staff, columns, actionHtml);
    }

    displayPagination(response, currentPage) {
        const paginationDiv = document.getElementById('staffPagination');
        if (paginationDiv) {
            paginationDiv.innerHTML = AJAXHelpers.buildPaginationControls(
                response,
                currentPage,
                'staffModule.loadStaff'
            );
        }
    }

    search() {
        const searchInput = document.getElementById('staffSearch');
        if (searchInput) {
            this.searchQuery = searchInput.value;
        }
        this.currentPage = 1;
        this.loadStaff();
    }

    async filterByDepartment() {
        const departmentFilter = document.getElementById('departmentFilter');
        if (departmentFilter) {
            const department = departmentFilter.value;
            if (department) {
                AJAXHelpers.showLoader('staffList');
                const result = await api.getStaffByDepartment(department);
                if (result.success) {
                    this.displayStaff(result.data);
                }
                AJAXHelpers.hideLoader('staffList');
            } else {
                this.loadStaff();
            }
        }
    }

    async viewStaff(id) {
        const result = await api.getStaffMember(id);
        
        if (result.success) {
            const member = result.data;
            const modal = new bootstrap.Modal(document.getElementById('staffDetailModal'));
            
            document.getElementById('staffDetailContent').innerHTML = `
                <div class="row">
                    <div class="col-md-6">
                        <p><strong>ID:</strong> ${member.staff_id}</p>
                        <p><strong>Name:</strong> ${member.full_name}</p>
                        <p><strong>Role:</strong> ${member.role}</p>
                        <p><strong>Department:</strong> ${member.department || '-'}</p>
                    </div>
                    <div class="col-md-6">
                        <p><strong>Phone:</strong> ${AJAXHelpers.formatPhoneNumber(member.phone)}</p>
                        <p><strong>Email:</strong> ${member.email || '-'}</p>
                        <p><strong>Hire Date:</strong> ${AJAXHelpers.formatDate(member.hire_date)}</p>
                        <p><strong>Status:</strong> ${member.is_active ? '<span class="badge bg-success">Active</span>' : '<span class="badge bg-danger">Inactive</span>'}</p>
                    </div>
                </div>
                ${member.schedule ? `<hr><p><strong>Schedule:</strong></p><p>${member.schedule}</p>` : ''}
            `;
            
            modal.show();
        } else {
            AJAXHelpers.showAlert('Error', 'Failed to load staff details', 'danger');
        }
    }

    async editStaff(id) {
        const result = await api.getStaffMember(id);
        
        if (result.success) {
            const member = result.data;
            AJAXHelpers.populateForm('staffForm', member);
            document.getElementById('staffFormTitle').textContent = 'Edit Staff Member';
            document.getElementById('staffId').value = id;
            
            const modal = new bootstrap.Modal(document.getElementById('staffFormModal'));
            modal.show();
        } else {
            AJAXHelpers.showAlert('Error', 'Failed to load staff', 'danger');
        }
    }

    showCreateModal() {
        AJAXHelpers.clearForm('staffForm');
        document.getElementById('staffFormTitle').textContent = 'Add New Staff Member';
        document.getElementById('staffId').value = '';
        
        const modal = new bootstrap.Modal(document.getElementById('staffFormModal'));
        modal.show();
    }

    async submitForm() {
        const staffId = document.getElementById('staffId').value;
        const formData = {
            staff_id: document.querySelector('[name="staff_id"]').value,
            first_name: document.querySelector('[name="first_name"]').value,
            last_name: document.querySelector('[name="last_name"]').value,
            role: document.querySelector('[name="role"]').value,
            department: document.querySelector('[name="department"]').value,
            phone: document.querySelector('[name="phone"]').value,
            email: document.querySelector('[name="email"]').value,
            schedule: document.querySelector('[name="schedule"]').value
        };

        let result;
        if (staffId) {
            result = await api.updateStaff(staffId, formData);
        } else {
            result = await api.createStaff(formData);
        }

        if (result.success) {
            AJAXHelpers.showToast('Staff saved successfully!', 'success');
            bootstrap.Modal.getInstance(document.getElementById('staffFormModal')).hide();
            this.loadStaff(this.currentPage);
        } else {
            AJAXHelpers.showToast(`Error: ${result.error}`, 'danger');
        }
    }

    async deleteStaff(id, name) {
        AJAXHelpers.confirmDelete(name, async () => {
            const result = await api.deleteStaff(id);
            
            if (result.success) {
                AJAXHelpers.showToast('Staff member deleted successfully!', 'success');
                this.loadStaff(this.currentPage);
            } else {
                AJAXHelpers.showToast(`Error: ${result.error}`, 'danger');
            }
            
            bootstrap.Modal.getInstance(document.getElementById('confirmDeleteModal')).hide();
        });
    }
}

// Initialize on page load
let staffModule;
document.addEventListener('DOMContentLoaded', () => {
    staffModule = new StaffModule();
});
