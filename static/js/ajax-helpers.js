/**
 * Remedium HMS - AJAX Helpers
 * Utility functions for common AJAX operations
 */

class AJAXHelpers {
    /**
     * Show toast notification
     */
    static showToast(message, type = 'success') {
        const toastHTML = `
            <div class="toast align-items-center text-white bg-${type} border-0" role="alert" aria-live="assertive" aria-atomic="true">
                <div class="d-flex">
                    <div class="toast-body">
                        ${message}
                    </div>
                    <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
                </div>
            </div>
        `;
        
        const container = document.querySelector('.toast-container') || document.body;
        const toastElement = document.createElement('div');
        toastElement.innerHTML = toastHTML;
        container.appendChild(toastElement.firstElementChild);
        
        const toast = new bootstrap.Toast(toastElement.firstElementChild);
        toast.show();
        
        // Remove element after toast is hidden
        toastElement.firstElementChild.addEventListener('hidden.bs.toast', () => {
            toastElement.firstElementChild.remove();
        });
    }

    /**
     * Show loading spinner
     */
    static showLoader(elementId) {
        const element = document.getElementById(elementId);
        if (element) {
            element.innerHTML = `
                <div class="text-center">
                    <div class="spinner-border text-primary" role="status">
                        <span class="visually-hidden">Loading...</span>
                    </div>
                </div>
            `;
        }
    }

    /**
     * Hide loading spinner
     */
    static hideLoader(elementId) {
        const element = document.getElementById(elementId);
        if (element) {
            element.innerHTML = '';
        }
    }

    /**
     * Format date string
     */
    static formatDate(dateString) {
        if (!dateString) return '';
        const date = new Date(dateString);
        return date.toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric'
        });
    }

    /**
     * Format datetime string
     */
    static formatDateTime(dateTimeString) {
        if (!dateTimeString) return '';
        const date = new Date(dateTimeString);
        return date.toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    }

    /**
     * Format currency
     */
    static formatCurrency(value) {
        if (!value) return '$0.00';
        return new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: 'USD'
        }).format(value);
    }

    /**
     * Build table rows from data
     */
    static buildTableRows(items, columns, actionCallback = null) {
        if (!items || items.length === 0) {
            return '<tr><td colspan="' + (columns.length + 1) + '" class="text-center text-muted">No items found</td></tr>';
        }

        let html = '';
        items.forEach(item => {
            html += '<tr>';
            columns.forEach(col => {
                let value = item[col.key];
                
                if (col.type === 'date') {
                    value = this.formatDate(value);
                } else if (col.type === 'datetime') {
                    value = this.formatDateTime(value);
                } else if (col.type === 'currency') {
                    value = this.formatCurrency(value);
                } else if (col.type === 'boolean') {
                    value = value ? '<span class="badge bg-success">Yes</span>' : '<span class="badge bg-danger">No</span>';
                }
                
                html += `<td>${value || '-'}</td>`;
            });

            if (actionCallback) {
                html += '<td>' + actionCallback(item) + '</td>';
            }

            html += '</tr>';
        });

        return html;
    }

    /**
     * Confirm delete action
     */
    static confirmDelete(itemName, callback) {
        const modal = document.getElementById('confirmDeleteModal');
        if (modal) {
            const modalBody = modal.querySelector('.modal-body');
            modalBody.textContent = `Are you sure you want to delete "${itemName}"? This action cannot be undone.`;
            
            const confirmButton = modal.querySelector('#confirmDeleteButton');
            confirmButton.onclick = callback;
            
            const bootstrapModal = new bootstrap.Modal(modal);
            bootstrapModal.show();
        } else {
            if (confirm(`Are you sure you want to delete "${itemName}"?`)) {
                callback();
            }
        }
    }

    /**
     * Handle form submission via AJAX
     */
    static async submitForm(formId, apiMethod, apiEndpoint) {
        const form = document.getElementById(formId);
        if (!form) return;

        const formData = new FormData(form);
        const data = Object.fromEntries(formData);

        let result;
        if (apiMethod === 'POST') {
            result = await api.post(apiEndpoint, data);
        } else if (apiMethod === 'PATCH') {
            result = await api.patch(apiEndpoint, data);
        } else if (apiMethod === 'PUT') {
            result = await api.put(apiEndpoint, data);
        }

        if (result.success) {
            this.showToast('Operation successful!', 'success');
            return result.data;
        } else {
            this.showToast(`Error: ${result.error}`, 'danger');
            return null;
        }
    }

    /**
     * Disable form during submission
     */
    static disableForm(formId, disabled = true) {
        const form = document.getElementById(formId);
        if (form) {
            const inputs = form.querySelectorAll('input, textarea, select, button');
            inputs.forEach(input => {
                input.disabled = disabled;
            });
        }
    }

    /**
     * Clear form
     */
    static clearForm(formId) {
        const form = document.getElementById(formId);
        if (form) {
            form.reset();
        }
    }

    /**
     * Populate form from data
     */
    static populateForm(formId, data) {
        const form = document.getElementById(formId);
        if (!form) return;

        Object.keys(data).forEach(key => {
            const input = form.querySelector(`[name="${key}"]`);
            if (input) {
                if (input.type === 'checkbox') {
                    input.checked = data[key];
                } else if (input.type === 'radio') {
                    const radio = form.querySelector(`[name="${key}"][value="${data[key]}"]`);
                    if (radio) radio.checked = true;
                } else {
                    input.value = data[key] || '';
                }
            }
        });
    }

    /**
     * Build pagination controls
     */
    static buildPaginationControls(response, pageNumber, onPageChange) {
        if (!response.next && !response.previous) {
            return '';
        }

        let html = '<nav aria-label="Page navigation"><ul class="pagination justify-content-center">';

        if (response.previous) {
            html += `<li class="page-item"><a class="page-link" href="#" onclick="event.preventDefault(); ${onPageChange}(${pageNumber - 1})">Previous</a></li>`;
        } else {
            html += '<li class="page-item disabled"><span class="page-link">Previous</span></li>';
        }

        html += `<li class="page-item active"><span class="page-link">${pageNumber}</span></li>`;

        if (response.next) {
            html += `<li class="page-item"><a class="page-link" href="#" onclick="event.preventDefault(); ${onPageChange}(${pageNumber + 1})">Next</a></li>`;
        } else {
            html += '<li class="page-item disabled"><span class="page-link">Next</span></li>';
        }

        html += '</ul></nav>';
        return html;
    }

    /**
     * Validate email
     */
    static isValidEmail(email) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    }

    /**
     * Validate phone number
     */
    static isValidPhone(phone) {
        const re = /^\+?1?\d{9,15}$/;
        return re.test(phone.replace(/\D/g, ''));
    }

    /**
     * Show alert modal
     */
    static showAlert(title, message, type = 'info') {
        const alertHTML = `
            <div class="alert alert-${type} alert-dismissible fade show" role="alert">
                <strong>${title}</strong><br>${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
            </div>
        `;
        
        const container = document.getElementById('alert-container') || document.body;
        container.insertAdjacentHTML('afterbegin', alertHTML);
    }

    /**
     * Format phone number
     */
    static formatPhoneNumber(phone) {
        if (!phone) return '';
        const digits = phone.replace(/\D/g, '');
        if (digits.length === 10) {
            return `(${digits.slice(0, 3)}) ${digits.slice(3, 6)}-${digits.slice(6)}`;
        } else if (digits.length === 11 && digits[0] === '1') {
            return `+1 (${digits.slice(1, 4)}) ${digits.slice(4, 7)}-${digits.slice(7)}`;
        }
        return phone;
    }
}

// Make helpers globally available
window.AJAXHelpers = AJAXHelpers;
