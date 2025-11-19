/**
 * Remedium HMS - API Client
 * Handles communication between frontend and backend API
 */

class APIClient {
    constructor(baseUrl = '/api') {
        this.baseUrl = baseUrl;
        this.csrfToken = this.getCsrfToken();
    }

    /**
     * Get CSRF token from cookie
     */
    getCsrfToken() {
        const name = 'csrftoken';
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    /**
     * Make API request
     */
    async request(endpoint, options = {}) {
        const url = `${this.baseUrl}${endpoint}`;
        const headers = {
            'Content-Type': 'application/json',
            'X-CSRFToken': this.csrfToken,
            ...options.headers
        };

        try {
            const response = await fetch(url, {
                method: options.method || 'GET',
                headers: headers,
                body: options.body ? JSON.stringify(options.body) : undefined,
                credentials: 'same-origin'
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            return { success: true, data };
        } catch (error) {
            console.error('API Error:', error);
            return { success: false, error: error.message };
        }
    }

    /**
     * GET request
     */
    async get(endpoint) {
        return this.request(endpoint, { method: 'GET' });
    }

    /**
     * POST request
     */
    async post(endpoint, data) {
        return this.request(endpoint, { method: 'POST', body: data });
    }

    /**
     * PUT request
     */
    async put(endpoint, data) {
        return this.request(endpoint, { method: 'PUT', body: data });
    }

    /**
     * PATCH request
     */
    async patch(endpoint, data) {
        return this.request(endpoint, { method: 'PATCH', body: data });
    }

    /**
     * DELETE request
     */
    async delete(endpoint) {
        return this.request(endpoint, { method: 'DELETE' });
    }

    /**
     * Get all patients
     */
    async getPatients(filters = {}) {
        let endpoint = '/patients/';
        const params = new URLSearchParams();
        
        if (filters.search) params.append('search', filters.search);
        if (filters.page) params.append('page', filters.page);
        if (filters.ordering) params.append('ordering', filters.ordering);
        
        if (params.toString()) {
            endpoint += '?' + params.toString();
        }
        
        return this.get(endpoint);
    }

    /**
     * Get single patient
     */
    async getPatient(id) {
        return this.get(`/patients/${id}/`);
    }

    /**
     * Create patient
     */
    async createPatient(data) {
        return this.post('/patients/', data);
    }

    /**
     * Update patient
     */
    async updatePatient(id, data) {
        return this.patch(`/patients/${id}/`, data);
    }

    /**
     * Delete patient
     */
    async deletePatient(id) {
        return this.delete(`/patients/${id}/`);
    }

    /**
     * Get admitted patients
     */
    async getAdmittedPatients() {
        return this.get('/patients/admitted_patients/');
    }

    /**
     * Discharge patient
     */
    async dischargePatient(id) {
        return this.post(`/patients/${id}/discharge/`, {});
    }

    /**
     * Get all staff
     */
    async getStaff(filters = {}) {
        let endpoint = '/staff/';
        const params = new URLSearchParams();
        
        if (filters.search) params.append('search', filters.search);
        if (filters.page) params.append('page', filters.page);
        if (filters.department) params.append('department', filters.department);
        
        if (params.toString()) {
            endpoint += '?' + params.toString();
        }
        
        return this.get(endpoint);
    }

    /**
     * Get single staff member
     */
    async getStaffMember(id) {
        return this.get(`/staff/${id}/`);
    }

    /**
     * Create staff member
     */
    async createStaff(data) {
        return this.post('/staff/', data);
    }

    /**
     * Update staff member
     */
    async updateStaff(id, data) {
        return this.patch(`/staff/${id}/`, data);
    }

    /**
     * Delete staff member
     */
    async deleteStaff(id) {
        return this.delete(`/staff/${id}/`);
    }

    /**
     * Get medical staff only
     */
    async getMedicalStaff() {
        return this.get('/staff/medical_staff/');
    }

    /**
     * Get staff by department
     */
    async getStaffByDepartment(department) {
        return this.get(`/staff/by_department/?department=${department}`);
    }

    /**
     * Get all appointments
     */
    async getAppointments(filters = {}) {
        let endpoint = '/appointments/';
        const params = new URLSearchParams();
        
        if (filters.search) params.append('search', filters.search);
        if (filters.page) params.append('page', filters.page);
        if (filters.status) params.append('status', filters.status);
        
        if (params.toString()) {
            endpoint += '?' + params.toString();
        }
        
        return this.get(endpoint);
    }

    /**
     * Get single appointment
     */
    async getAppointment(id) {
        return this.get(`/appointments/${id}/`);
    }

    /**
     * Create appointment
     */
    async createAppointment(data) {
        return this.post('/appointments/', data);
    }

    /**
     * Update appointment
     */
    async updateAppointment(id, data) {
        return this.patch(`/appointments/${id}/`, data);
    }

    /**
     * Delete appointment
     */
    async deleteAppointment(id) {
        return this.delete(`/appointments/${id}/`);
    }

    /**
     * Get scheduled appointments
     */
    async getScheduledAppointments() {
        return this.get('/appointments/scheduled/');
    }

    /**
     * Get upcoming appointments
     */
    async getUpcomingAppointments() {
        return this.get('/appointments/upcoming/');
    }

    /**
     * Get all invoices
     */
    async getInvoices(filters = {}) {
        let endpoint = '/invoices/';
        const params = new URLSearchParams();
        
        if (filters.search) params.append('search', filters.search);
        if (filters.page) params.append('page', filters.page);
        if (filters.status) params.append('status', filters.status);
        
        if (params.toString()) {
            endpoint += '?' + params.toString();
        }
        
        return this.get(endpoint);
    }

    /**
     * Get single invoice
     */
    async getInvoice(id) {
        return this.get(`/invoices/${id}/`);
    }

    /**
     * Create invoice
     */
    async createInvoice(data) {
        return this.post('/invoices/', data);
    }

    /**
     * Update invoice
     */
    async updateInvoice(id, data) {
        return this.patch(`/invoices/${id}/`, data);
    }

    /**
     * Delete invoice
     */
    async deleteInvoice(id) {
        return this.delete(`/invoices/${id}/`);
    }

    /**
     * Get unpaid invoices
     */
    async getUnpaidInvoices() {
        return this.get('/invoices/unpaid/');
    }

    /**
     * Get overdue invoices
     */
    async getOverdueInvoices() {
        return this.get('/invoices/overdue/');
    }

    /**
     * Mark invoice as paid
     */
    async markInvoiceAsPaid(id) {
        return this.post(`/invoices/${id}/mark_paid/`, {});
    }
}

// Initialize global API client
const api = new APIClient();
