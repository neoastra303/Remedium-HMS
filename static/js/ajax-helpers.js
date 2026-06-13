class AJAXHelpers {
    static escapeHTML(value) {
        if (value === null || value === undefined) return '';
        return String(value).replace(/[&<>"']/g, (char) => ({
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            "'": '&#39;'
        }[char]));
    }

    static showToast(message, type = 'success') {
        if (window.showToast) {
            window.showToast(message, type);
            return;
        }
        const container = document.getElementById('toastContainer') || document.body;
        const id = 'toast-' + Date.now();
        const html = [
            '<div id="' + id + '" class="toast align-items-center text-white bg-' + type + ' border-0 animate-fade-in" role="alert" aria-live="assertive" aria-atomic="true">',
            '<div class="d-flex">',
            '<div class="toast-body">' + this.escapeHTML(message) + '</div>',
            '<button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>',
            '</div>',
            '</div>'
        ].join('');
        container.insertAdjacentHTML('beforeend', html);
        const toastEl = document.getElementById(id);
        const toast = new bootstrap.Toast(toastEl, { autohide: true, delay: 4000 });
        toast.show();
        toastEl.addEventListener('hidden.bs.toast', () => toastEl.remove());
    }

    static showLoader(elementId) {
        const element = document.getElementById(elementId);
        if (element) {
            element.innerHTML = [
                '<div class="text-center py-4">',
                '<div class="spinner-border text-primary mb-2" role="status">',
                '<span class="visually-hidden">Loading...</span>',
                '</div>',
                '<p class="text-muted small mb-0">Loading data\u2026</p>',
                '</div>'
            ].join('');
        }
    }

    static hideLoader(elementId) {
        const element = document.getElementById(elementId);
        if (element) element.innerHTML = '';
    }

    static formatDate(dateString) {
        if (!dateString) return '';
        const date = new Date(dateString);
        if (isNaN(date.getTime())) return dateString;
        return date.toLocaleDateString('en-US', {
            year: 'numeric', month: 'short', day: 'numeric'
        });
    }

    static formatDateTime(dateTimeString) {
        if (!dateTimeString) return '';
        const date = new Date(dateTimeString);
        if (isNaN(date.getTime())) return dateTimeString;
        return date.toLocaleDateString('en-US', {
            year: 'numeric', month: 'short', day: 'numeric',
            hour: '2-digit', minute: '2-digit'
        });
    }

    static formatCurrency(value) {
        if (!value && value !== 0) return '$0.00';
        return new Intl.NumberFormat('en-US', {
            style: 'currency', currency: 'USD'
        }).format(value);
    }

    static buildTableRows(items, columns, actionCallback = null) {
        if (!items || items.length === 0) {
            return '<tr><td colspan="' + (columns.length + (actionCallback ? 1 : 0)) + '" class="text-center py-4 text-muted small">No items found</td></tr>';
        }
        let html = '';
        items.forEach(item => {
            html += '<tr>';
            columns.forEach(col => {
                let value = item[col.key];
                if (col.type === 'date') value = this.formatDate(value);
                else if (col.type === 'datetime') value = this.formatDateTime(value);
                else if (col.type === 'currency') value = this.formatCurrency(value);
                else if (col.type === 'boolean') {
                    value = value
                        ? '<span class="badge bg-success rounded-pill">Yes</span>'
                        : '<span class="badge bg-danger rounded-pill">No</span>';
                }
                html += '<td class="small">' + (value != null ? this.escapeHTML(String(value)) : '-') + '</td>';
            });
            if (actionCallback) {
                html += '<td class="text-end">' + actionCallback(item) + '</td>';
            }
            html += '</tr>';
        });
        return html;
    }

    static confirmDelete(itemName, callback) {
        const modal = document.getElementById('confirmDeleteModal');
        if (modal) {
            const nameEl = modal.querySelector('#deleteItemName');
            if (nameEl) nameEl.textContent = itemName;
            const confirmButton = modal.querySelector('#confirmDeleteButton');
            confirmButton.onclick = callback;
            const bootstrapModal = new bootstrap.Modal(modal);
            bootstrapModal.show();
        } else {
            if (confirm('Are you sure you want to delete "' + itemName + '"?')) {
                callback();
            }
        }
    }

    static async submitForm(formId, apiMethod, apiEndpoint) {
        const form = document.getElementById(formId);
        if (!form) return null;
        const formData = new FormData(form);
        const data = Object.fromEntries(formData);
        let result;
        try {
            if (apiMethod === 'POST') result = await api.post(apiEndpoint, data);
            else if (apiMethod === 'PATCH') result = await api.patch(apiEndpoint, data);
            else if (apiMethod === 'PUT') result = await api.put(apiEndpoint, data);
            else return null;
        } catch (e) {
            this.showToast('Network error: ' + e.message, 'danger');
            return null;
        }
        if (result && result.success) {
            this.showToast('Operation successful!', 'success');
            return result.data;
        } else {
            this.showToast('Error: ' + (result ? result.message || result.error : 'Unknown error'), 'danger');
            return null;
        }
    }

    static disableForm(formId, disabled = true) {
        const form = document.getElementById(formId);
        if (form) {
            form.querySelectorAll('input, textarea, select, button').forEach(input => {
                input.disabled = disabled;
            });
        }
    }

    static clearForm(formId) {
        const form = document.getElementById(formId);
        if (form) form.reset();
    }

    static populateForm(formId, data) {
        const form = document.getElementById(formId);
        if (!form) return;
        Object.keys(data).forEach(key => {
            const input = form.querySelector('[name="' + key + '"]');
            if (!input) return;
            if (input.type === 'checkbox') input.checked = !!data[key];
            else if (input.type === 'radio') {
                const radio = form.querySelector('[name="' + key + '"][value="' + data[key] + '"]');
                if (radio) radio.checked = true;
            } else {
                input.value = data[key] || '';
            }
        });
    }

    static buildPaginationControls(response, pageNumber, onPageChange) {
        if (!response.next && !response.previous) return '';
        let html = '<nav aria-label="Page navigation"><ul class="pagination justify-content-center gap-1">';
        if (response.previous) {
            html += '<li class="page-item"><a class="page-link" href="#" onclick="event.preventDefault(); (' + onPageChange + ')(' + (pageNumber - 1) + ')">Previous</a></li>';
        } else {
            html += '<li class="page-item disabled"><span class="page-link">Previous</span></li>';
        }
        html += '<li class="page-item active"><span class="page-link">' + pageNumber + '</span></li>';
        if (response.next) {
            html += '<li class="page-item"><a class="page-link" href="#" onclick="event.preventDefault(); (' + onPageChange + ')(' + (pageNumber + 1) + ')">Next</a></li>';
        } else {
            html += '<li class="page-item disabled"><span class="page-link">Next</span></li>';
        }
        html += '</ul></nav>';
        return html;
    }

    static isValidEmail(email) {
        return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
    }

    static isValidPhone(phone) {
        return /^\+?1?\d{9,15}$/.test(phone.replace(/\D/g, ''));
    }

    static showAlert(title, message, type = 'info') {
        const alertHTML = [
            '<div class="alert alert-' + type + ' alert-dismissible fade show d-flex align-items-center" role="alert">',
            '<i class="bi bi-' + (type === 'success' ? 'check-circle' : type === 'danger' ? 'exclamation-circle' : 'info-circle') + ' me-2"></i>',
            '<div><strong>' + this.escapeHTML(title) + '</strong><br>' + this.escapeHTML(message) + '</div>',
            '<button type="button" class="btn-close ms-auto" data-bs-dismiss="alert" aria-label="Close"></button>',
            '</div>'
        ].join('');
        const container = document.getElementById('alert-container') || document.body;
        container.insertAdjacentHTML('afterbegin', alertHTML);
    }

    static formatPhoneNumber(phone) {
        if (!phone) return '';
        const digits = phone.replace(/\D/g, '');
        if (digits.length === 10) {
            return '(' + digits.slice(0, 3) + ') ' + digits.slice(3, 6) + '-' + digits.slice(6);
        } else if (digits.length === 11 && digits[0] === '1') {
            return '+1 (' + digits.slice(1, 4) + ') ' + digits.slice(4, 7) + '-' + digits.slice(7);
        }
        return phone;
    }
}

window.AJAXHelpers = AJAXHelpers;
