/**
 * Remedium HMS - Invoices Module
 * Handles invoice-related API operations and UI updates
 */

class InvoicesModule {
    constructor() {
        this.currentPage = 1;
        this.searchQuery = '';
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.loadInvoices();
    }

    setupEventListeners() {
        // Search form
        const searchForm = document.getElementById('invoiceSearchForm');
        if (searchForm) {
            searchForm.addEventListener('submit', (e) => {
                e.preventDefault();
                this.search();
            });
        }

        // Create invoice button
        const createBtn = document.getElementById('createInvoiceBtn');
        if (createBtn) {
            createBtn.addEventListener('click', () => this.showCreateModal());
        }

        // Form submission
        const invoiceForm = document.getElementById('invoiceForm');
        if (invoiceForm) {
            invoiceForm.addEventListener('submit', (e) => {
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

    async loadInvoices(page = 1) {
        AJAXHelpers.showLoader('invoicesList');
        
        const result = await api.getInvoices({
            search: this.searchQuery,
            page: page
        });

        if (result.success) {
            this.displayInvoices(result.data.results);
            this.displayPagination(result.data, page);
            this.currentPage = page;
        } else {
            AJAXHelpers.showAlert('Error', 'Failed to load invoices', 'danger');
        }
        
        AJAXHelpers.hideLoader('invoicesList');
    }

    displayInvoices(invoices) {
        const tbody = document.getElementById('invoicesTableBody');
        if (!tbody) return;

        if (invoices.length === 0) {
            tbody.innerHTML = '<tr><td colspan="7" class="text-center text-muted">No invoices found</td></tr>';
            return;
        }

        let html = '';
        invoices.forEach(invoice => {
            const statusBadge = invoice.paid ? 
                '<span class="badge bg-success">Paid</span>' : 
                '<span class="badge bg-warning">Unpaid</span>';
            
            html += `
                <tr>
                    <td>${invoice.patient_detail.full_name}</td>
                    <td>${AJAXHelpers.formatCurrency(invoice.total_amount)}</td>
                    <td>${AJAXHelpers.formatDate(invoice.issue_date)}</td>
                    <td>${AJAXHelpers.formatDate(invoice.due_date)}</td>
                    <td>${statusBadge}</td>
                    <td>${invoice.insurance_claimed ? '<span class="badge bg-info">Yes</span>' : '<span class="badge bg-secondary">No</span>'}</td>
                    <td>
                        <div class="btn-group btn-group-sm" role="group">
                            <button type="button" class="btn btn-info btn-sm" onclick="invoicesModule.viewInvoice(${invoice.id})">
                                <i class="bi bi-eye"></i>
                            </button>
                            <button type="button" class="btn btn-warning btn-sm" onclick="invoicesModule.editInvoice(${invoice.id})">
                                <i class="bi bi-pencil"></i>
                            </button>
                            ${!invoice.paid ? `<button type="button" class="btn btn-success btn-sm" onclick="invoicesModule.markAsPaid(${invoice.id})"><i class="bi bi-check"></i></button>` : ''}
                            <button type="button" class="btn btn-danger btn-sm" onclick="invoicesModule.deleteInvoice(${invoice.id})">
                                <i class="bi bi-trash"></i>
                            </button>
                        </div>
                    </td>
                </tr>
            `;
        });

        tbody.innerHTML = html;
    }

    displayPagination(response, currentPage) {
        const paginationDiv = document.getElementById('invoicesPagination');
        if (paginationDiv) {
            paginationDiv.innerHTML = AJAXHelpers.buildPaginationControls(
                response,
                currentPage,
                'invoicesModule.loadInvoices'
            );
        }
    }

    search() {
        const searchInput = document.getElementById('invoiceSearch');
        if (searchInput) {
            this.searchQuery = searchInput.value;
        }
        this.currentPage = 1;
        this.loadInvoices();
    }

    async filterByStatus() {
        const statusFilter = document.getElementById('statusFilter');
        if (statusFilter && statusFilter.value === 'unpaid') {
            AJAXHelpers.showLoader('invoicesList');
            const result = await api.getUnpaidInvoices();
            if (result.success) {
                this.displayInvoices(result.data);
            }
            AJAXHelpers.hideLoader('invoicesList');
        } else if (statusFilter && statusFilter.value === 'overdue') {
            AJAXHelpers.showLoader('invoicesList');
            const result = await api.getOverdueInvoices();
            if (result.success) {
                this.displayInvoices(result.data);
            }
            AJAXHelpers.hideLoader('invoicesList');
        } else {
            this.loadInvoices(1);
        }
    }

    async viewInvoice(id) {
        const result = await api.getInvoice(id);
        
        if (result.success) {
            const invoice = result.data;
            const modal = new bootstrap.Modal(document.getElementById('invoiceDetailModal'));
            
            document.getElementById('invoiceDetailContent').innerHTML = `
                <div class="row">
                    <div class="col-md-6">
                        <p><strong>Invoice #:</strong> ${invoice.id}</p>
                        <p><strong>Patient:</strong> ${invoice.patient_detail.full_name}</p>
                        <p><strong>Total Amount:</strong> ${AJAXHelpers.formatCurrency(invoice.total_amount)}</p>
                    </div>
                    <div class="col-md-6">
                        <p><strong>Issue Date:</strong> ${AJAXHelpers.formatDate(invoice.issue_date)}</p>
                        <p><strong>Due Date:</strong> ${AJAXHelpers.formatDate(invoice.due_date)}</p>
                        <p><strong>Status:</strong> ${invoice.paid ? '<span class="badge bg-success">Paid</span>' : '<span class="badge bg-warning">Unpaid</span>'}</p>
                    </div>
                </div>
                ${invoice.details ? `<hr><p><strong>Details:</strong></p><p>${invoice.details}</p>` : ''}
                ${!invoice.paid ? `<button class="btn btn-success" onclick="invoicesModule.markAsPaid(${invoice.id})">Mark as Paid</button>` : ''}
            `;
            
            modal.show();
        } else {
            AJAXHelpers.showAlert('Error', 'Failed to load invoice', 'danger');
        }
    }

    async editInvoice(id) {
        const result = await api.getInvoice(id);
        
        if (result.success) {
            const invoice = result.data;
            AJAXHelpers.populateForm('invoiceForm', invoice);
            document.getElementById('invoiceFormTitle').textContent = 'Edit Invoice';
            document.getElementById('invoiceId').value = id;
            
            const modal = new bootstrap.Modal(document.getElementById('invoiceFormModal'));
            modal.show();
        } else {
            AJAXHelpers.showAlert('Error', 'Failed to load invoice', 'danger');
        }
    }

    showCreateModal() {
        AJAXHelpers.clearForm('invoiceForm');
        document.getElementById('invoiceFormTitle').textContent = 'Create New Invoice';
        document.getElementById('invoiceId').value = '';
        
        const modal = new bootstrap.Modal(document.getElementById('invoiceFormModal'));
        modal.show();
    }

    async submitForm() {
        const invoiceId = document.getElementById('invoiceId').value;
        const formData = {
            patient: document.querySelector('[name="patient"]').value,
            issue_date: document.querySelector('[name="issue_date"]').value,
            due_date: document.querySelector('[name="due_date"]').value,
            total_amount: document.querySelector('[name="total_amount"]').value,
            paid: document.querySelector('[name="paid"]').checked,
            insurance_claimed: document.querySelector('[name="insurance_claimed"]').checked,
            details: document.querySelector('[name="details"]').value
        };

        let result;
        if (invoiceId) {
            result = await api.updateInvoice(invoiceId, formData);
        } else {
            result = await api.createInvoice(formData);
        }

        if (result.success) {
            AJAXHelpers.showToast('Invoice saved successfully!', 'success');
            bootstrap.Modal.getInstance(document.getElementById('invoiceFormModal')).hide();
            this.loadInvoices(this.currentPage);
        } else {
            AJAXHelpers.showToast(`Error: ${result.error}`, 'danger');
        }
    }

    async deleteInvoice(id) {
        AJAXHelpers.confirmDelete('this invoice', async () => {
            const result = await api.deleteInvoice(id);
            
            if (result.success) {
                AJAXHelpers.showToast('Invoice deleted successfully!', 'success');
                this.loadInvoices(this.currentPage);
            } else {
                AJAXHelpers.showToast(`Error: ${result.error}`, 'danger');
            }
            
            bootstrap.Modal.getInstance(document.getElementById('confirmDeleteModal')).hide();
        });
    }

    async markAsPaid(id) {
        const result = await api.markInvoiceAsPaid(id);
        
        if (result.success) {
            AJAXHelpers.showToast('Invoice marked as paid!', 'success');
            this.loadInvoices(this.currentPage);
        } else {
            AJAXHelpers.showToast(`Error: ${result.error}`, 'danger');
        }
    }
}

// Initialize on page load
let invoicesModule;
document.addEventListener('DOMContentLoaded', () => {
    invoicesModule = new InvoicesModule();
});
