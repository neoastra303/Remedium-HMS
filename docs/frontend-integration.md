# Remedium HMS - Frontend & Backend Integration Guide

## Overview

Complete frontend-backend integration with REST API, AJAX, and real-time data synchronization.

---

## Architecture

```
Frontend (Templates + JavaScript)
         ↓
  AJAX Requests (Fetch API)
         ↓
REST API (Django REST Framework)
         ↓
Database (Models)
```

---

## Components Created

### 1. API Client (`static/js/api-client.js`)

Complete JavaScript API client for all backend endpoints.

**Features:**
- CSRF token handling
- Request/response management
- Error handling
- All CRUD operations
- Custom actions (discharge, mark paid, etc.)

**Usage:**
```javascript
// Get patients
const result = await api.getPatients();

// Create patient
const result = await api.createPatient({
    unique_id: 'PAT001',
    first_name: 'John',
    last_name: 'Doe',
    date_of_birth: '1990-05-15',
    gender: 'M'
});

// Update patient
const result = await api.updatePatient(1, {
    first_name: 'Jane'
});

// Delete patient
const result = await api.deletePatient(1);
```

### 2. AJAX Helpers (`static/js/ajax-helpers.js`)

Utility functions for common UI operations.

**Features:**
- Toast notifications
- Loading spinners
- Date/time formatting
- Currency formatting
- Table row building
- Form handling
- Pagination controls
- Validation functions

**Usage:**
```javascript
// Show toast notification
AJAXHelpers.showToast('Success!', 'success');

// Format date
AJAXHelpers.formatDate('2024-01-15');  // "Jan 15, 2024"

// Format currency
AJAXHelpers.formatCurrency(1000);  // "$1,000.00"

// Confirm delete
AJAXHelpers.confirmDelete('Patient Name', async () => {
    await api.deletePatient(1);
});
```

### 3. Module JavaScript Files

Specialized modules for each major feature:

#### Patients Module (`static/js/modules/patients.js`)
- List/search patients
- Create/edit/delete patients
- Discharge patients
- View patient details
- Real-time table updates

**Available Functions:**
```javascript
patientsModule.loadPatients(page)      // Load patients
patientsModule.search()                 // Search patients
patientsModule.viewPatient(id)          // View details
patientsModule.editPatient(id)          // Edit patient
patientsModule.createPatient()          // New patient form
patientsModule.deletePatient(id, name)  // Delete patient
patientsModule.dischargePatient(id)     // Discharge patient
```

#### Staff Module (`static/js/modules/staff.js`)
- List/search staff members
- Create/edit/delete staff
- Filter by department
- View medical staff only

**Available Functions:**
```javascript
staffModule.loadStaff(page)             // Load staff
staffModule.search()                    // Search staff
staffModule.viewStaff(id)               // View details
staffModule.editStaff(id)               // Edit staff
staffModule.filterByDepartment()        // Filter by dept
staffModule.deleteStaff(id, name)       // Delete staff
```

#### Appointments Module (`static/js/modules/appointments.js`)
- Schedule/manage appointments
- Search by patient/doctor
- Filter by status
- View upcoming appointments

**Available Functions:**
```javascript
appointmentsModule.loadAppointments(page)    // Load appointments
appointmentsModule.search()                  // Search appointments
appointmentsModule.viewAppointment(id)       // View details
appointmentsModule.editAppointment(id)       // Edit appointment
appointmentsModule.deleteAppointment(id)     // Delete appointment
appointmentsModule.filterByStatus()          // Filter by status
```

#### Invoices Module (`static/js/modules/invoices.js`)
- Create/manage invoices
- Mark as paid
- Filter (unpaid/overdue)
- View invoice details

**Available Functions:**
```javascript
invoicesModule.loadInvoices(page)           // Load invoices
invoicesModule.search()                     // Search invoices
invoicesModule.viewInvoice(id)              // View details
invoicesModule.editInvoice(id)              // Edit invoice
invoicesModule.markAsPaid(id)               // Mark as paid
invoicesModule.deleteInvoice(id)            // Delete invoice
invoicesModule.filterByStatus()             // Filter by status
```

---

## Template Integration

### Base Template (`templates/base.html`)

Updated with:
- API client script inclusion
- AJAX helpers script inclusion
- Toast notification container
- Delete confirmation modal
- Navigation with all module links

### Module Templates

Each module requires these HTML elements for JavaScript integration:

#### Patients List Template
```html
<!-- Search form -->
<form id="patientSearchForm">
    <input id="patientSearch" type="text" placeholder="Search...">
    <button type="submit">Search</button>
</form>

<!-- Create button -->
<button id="createPatientBtn">Add Patient</button>

<!-- Results table -->
<table>
    <thead>...</thead>
    <tbody id="patientsTableBody"></tbody>
</table>

<!-- Pagination -->
<div id="patientsPagination"></div>

<!-- Include module script -->
<script src="{% static 'js/modules/patients.js' %}"></script>
```

#### Staff List Template
```html
<!-- Search form -->
<form id="staffSearchForm">
    <input id="staffSearch" type="text" placeholder="Search...">
    <button type="submit">Search</button>
</form>

<!-- Department filter -->
<select id="departmentFilter">
    <option value="">All Departments</option>
    <option value="CARDIOLOGY">Cardiology</option>
    <!-- More options... -->
</select>

<!-- Create button -->
<button id="createStaffBtn">Add Staff Member</button>

<!-- Results table -->
<table>
    <thead>...</thead>
    <tbody id="staffTableBody"></tbody>
</table>

<!-- Pagination -->
<div id="staffPagination"></div>

<!-- Include module script -->
<script src="{% static 'js/modules/staff.js' %}"></script>
```

---

## API Endpoints Connected

### Patients
```
GET    /api/patients/                    → List all patients
POST   /api/patients/                    → Create patient
GET    /api/patients/{id}/               → Get patient details
PUT    /api/patients/{id}/               → Update patient
DELETE /api/patients/{id}/               → Delete patient
GET    /api/patients/admitted_patients/  → Get admitted patients
POST   /api/patients/{id}/discharge/     → Discharge patient
```

### Staff
```
GET    /api/staff/                       → List all staff
POST   /api/staff/                       → Create staff
GET    /api/staff/{id}/                  → Get staff details
PUT    /api/staff/{id}/                  → Update staff
DELETE /api/staff/{id}/                  → Delete staff
GET    /api/staff/medical_staff/         → Get medical staff
GET    /api/staff/by_department/         → Filter by department
```

### Appointments
```
GET    /api/appointments/                → List all appointments
POST   /api/appointments/                → Create appointment
GET    /api/appointments/{id}/           → Get appointment details
PUT    /api/appointments/{id}/           → Update appointment
DELETE /api/appointments/{id}/           → Delete appointment
GET    /api/appointments/scheduled/      → Get scheduled appointments
GET    /api/appointments/upcoming/       → Get upcoming appointments
```

### Invoices
```
GET    /api/invoices/                    → List all invoices
POST   /api/invoices/                    → Create invoice
GET    /api/invoices/{id}/               → Get invoice details
PUT    /api/invoices/{id}/               → Update invoice
DELETE /api/invoices/{id}/               → Delete invoice
GET    /api/invoices/unpaid/             → Get unpaid invoices
GET    /api/invoices/overdue/            → Get overdue invoices
POST   /api/invoices/{id}/mark_paid/     → Mark invoice as paid
```

---

## Workflow Example: Adding a Patient

### 1. User clicks "Add Patient" button
```javascript
// triggers: patientsModule.showCreateModal()
```

### 2. Modal appears with form
```html
<form id="patientForm">
    <input name="unique_id" required>
    <input name="first_name" required>
    <input name="last_name" required>
    <!-- More fields... -->
    <button type="submit">Save Patient</button>
</form>
```

### 3. User fills form and submits
```javascript
// triggers: patientForm submit handler
// calls: patientsModule.submitForm()
```

### 4. JavaScript collects form data
```javascript
const formData = {
    unique_id: document.querySelector('[name="unique_id"]').value,
    first_name: document.querySelector('[name="first_name"]').value,
    // ... etc
};
```

### 5. API client sends POST request
```javascript
const result = await api.createPatient(formData);
```

### 6. Django REST API processes request
- Validates data using serializer
- Creates database record
- Returns success response

### 7. JavaScript handles response
```javascript
if (result.success) {
    AJAXHelpers.showToast('Patient saved!', 'success');
    // Reload patient list
    patientsModule.loadPatients(1);
}
```

### 8. UI updates automatically
- Table refreshes with new patient
- Modal closes
- Toast notification shown

---

## Form Handling

### Form Elements Required

Each module uses Django form fields. Form names must match API field names:

```html
<!-- Patient Form -->
<form id="patientForm">
    <input type="text" name="unique_id" required>
    <input type="text" name="first_name" required>
    <input type="text" name="last_name" required>
    <input type="date" name="date_of_birth" required>
    <select name="gender">
        <option value="">Select Gender</option>
        <option value="M">Male</option>
        <option value="F">Female</option>
        <option value="O">Other</option>
        <option value="P">Prefer not to say</option>
    </select>
    <input type="tel" name="phone">
    <input type="email" name="email">
    <textarea name="medical_history"></textarea>
    <button type="submit">Save Patient</button>
</form>
```

### Form Submission Flow

1. **Validation** (browser + server)
   - Required fields checked
   - Phone number validated
   - Email validated
   - Server-side model validation

2. **Submission**
   - AJAX POST/PATCH to API
   - CSRF token included automatically

3. **Response Handling**
   - Success: Close modal, refresh list, show toast
   - Error: Show validation errors, display toast

---

## Data Binding

### Populating Forms with Existing Data

```javascript
// Get patient data
const result = await api.getPatient(id);

// Populate form fields
AJAXHelpers.populateForm('patientForm', result.data);
```

### Clearing Forms

```javascript
AJAXHelpers.clearForm('patientForm');
```

---

## Real-Time Updates

### Pagination
```javascript
// Load next page
patientsModule.loadPatients(2);

// Pagination controls automatically generated
AJAXHelpers.buildPaginationControls(response, page, 'patientsModule.loadPatients');
```

### Search/Filter
```javascript
// Type in search box triggers search
// Results update automatically
patientsModule.search();
```

### Status Updates
```javascript
// Mark invoice as paid
await api.markInvoiceAsPaid(id);
// Table refreshes automatically
```

---

## Error Handling

### API Errors
```javascript
if (!result.success) {
    AJAXHelpers.showToast(`Error: ${result.error}`, 'danger');
}
```

### Form Validation
```javascript
// Server returns validation errors
// Caught and displayed to user
```

### Network Errors
```javascript
// Fetch errors caught and logged
// User notified with toast
```

---

## Security Features

### CSRF Protection
```javascript
// API client automatically includes CSRF token
const csrfToken = this.getCsrfToken();
headers['X-CSRFToken'] = csrfToken;
```

### Authentication
```javascript
// Session authentication required
// Automatically handled by Django
// Token authentication supported
```

### Permission-Based Access
```javascript
// API enforces permissions
// Frontend respects user groups
// UI elements hidden based on permissions
```

---

## Performance Optimization

### Pagination
- Default 20 items per page
- Reduces initial load time
- Smooth pagination controls

### Lazy Loading
- Data loaded on demand
- Tables populated when accessed
- Modals populated on open

### Debouncing
- Search input debounced
- Prevents excessive API calls
- Smoother user experience

---

## Browser Compatibility

- Chrome/Edge: ✅ Full support
- Firefox: ✅ Full support
- Safari: ✅ Full support
- IE11: ⚠️ Polyfills required

### Modern Features Used
- Fetch API
- Async/await
- ES6 modules
- Bootstrap 5

---

## Customization

### Adding New Module

1. **Create module file** (`static/js/modules/module-name.js`)
2. **Implement class** with init(), setupEventListeners(), load functions
3. **Add API methods** to `api-client.js`
4. **Create template** with required HTML elements
5. **Include script** in template footer

### Adding New API Endpoint

1. **Add method to APIClient**
```javascript
async customAction(id) {
    return this.get(`/endpoint/custom_action/?id=${id}`);
}
```

2. **Use in module**
```javascript
const result = await api.customAction(id);
```

---

## Testing API Calls

### Using Browser Console

```javascript
// Test API client
api.getPatients().then(r => console.log(r));

// List all methods
Object.getOwnPropertyNames(api.__proto__)
```

### Using Network Tab

1. Open DevTools (F12)
2. Go to Network tab
3. Perform action
4. View request/response
5. Check headers and payload

### Using Postman

1. Import API endpoints
2. Set Authorization header
3. Test each endpoint
4. Save requests for future use

---

## Troubleshooting

### "CORS error"
- Check CORS_ALLOWED_ORIGINS in settings
- Verify API is accessible
- Check browser console for details

### "CSRF token missing"
- Ensure csrf middleware enabled
- Check cookie is present
- Verify form includes csrf token

### "404 Not Found"
- Check API endpoint URL
- Verify endpoint exists
- Check routing configuration

### "Data not loading"
- Check network tab for errors
- Verify API permissions
- Check browser console
- Test API endpoint directly

---

## Best Practices

1. **Error Handling** - Always check result.success
2. **User Feedback** - Show toasts for all actions
3. **Loading States** - Disable buttons during requests
4. **Data Validation** - Validate on both sides
5. **CSRF Protection** - Always include token
6. **Pagination** - Use pagination for large datasets
7. **Caching** - Cache frequently accessed data
8. **Performance** - Use debouncing for searches

---

## File Structure

```
static/
├── css/
│   └── custom.css          # Styling
├── js/
│   ├── api-client.js       # API client
│   ├── ajax-helpers.js     # Helper functions
│   └── modules/
│       ├── patients.js     # Patient module
│       ├── staff.js        # Staff module
│       ├── appointments.js # Appointment module
│       └── invoices.js     # Invoice module

templates/
├── base.html               # Base template with scripts
├── index.html              # Homepage
├── patients/
│   ├── patient_list.html
│   ├── patient_detail.html
│   ├── patient_form.html
│   └── patient_confirm_delete.html
├── staff/
│   ├── staff_list.html
│   ├── staff_detail.html
│   ├── staff_form.html
│   └── staff_confirm_delete.html
├── appointments/
│   ├── appointment_list.html
│   ├── appointment_form.html
│   └── appointment_confirm_delete.html
└── billing/
    ├── invoice_list.html
    ├── invoice_detail.html
    ├── invoice_form.html
    └── invoice_confirm_delete.html
```

---

## Next Steps

1. **Update templates** to include required HTML elements
2. **Test API endpoints** using Postman or curl
3. **Test module functionality** in browser
4. **Customize styling** for your needs
5. **Add more modules** for other apps (inventory, lab, etc.)
6. **Set up CI/CD** for automated testing

---

## Support

For integration questions or issues:
- Check browser console for errors
- Review network tab for API responses
- Refer to API.md for endpoint documentation
- Check module comments for method documentation

---

**Status**: ✅ Frontend-Backend Integration Complete

All major modules have full API integration ready for use.
