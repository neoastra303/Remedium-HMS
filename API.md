# Remedium HMS API Documentation

## Overview

The Remedium Hospital Management System provides a comprehensive REST API for managing all hospital operations. All API endpoints require authentication.

## Base URL

```
http://localhost:8000/api/
```

## Authentication

All API endpoints require authentication using session authentication or token-based authentication.

### Session Authentication
Include the session cookie from login:
```bash
curl -X GET http://localhost:8000/api/patients/ \
  -H "Cookie: sessionid=your-session-id"
```

### Header Authentication
Include credentials in headers:
```bash
curl -X GET http://localhost:8000/api/patients/ \
  -H "Authorization: Bearer your-token"
```

## API Endpoints

### 1. Patients API

#### List All Patients
```
GET /api/patients/
```

Query Parameters:
- `search`: Search by unique_id, first_name, last_name, email
- `ordering`: Order by admission_date, first_name, last_name
- `page`: Page number for pagination

Example:
```bash
curl -X GET "http://localhost:8000/api/patients/?search=john&page=1"
```

Response:
```json
{
  "count": 100,
  "next": "http://localhost:8000/api/patients/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "unique_id": "PAT001",
      "first_name": "John",
      "last_name": "Doe",
      "full_name": "John Doe",
      "date_of_birth": "1990-05-15",
      "age": 33,
      "gender": "M",
      "address": "123 Main St",
      "phone": "+1234567890",
      "email": "john@example.com",
      "insurance_provider": "Blue Cross",
      "emergency_contact_name": "Jane Doe",
      "emergency_contact_phone": "+1234567891",
      "medical_history": "No known allergies",
      "admission_date": "2024-01-15T10:30:00Z",
      "discharge_date": null,
      "is_admitted": true,
      "ward": 1,
      "room": 5
    }
  ]
}
```

#### Get Patient Details
```
GET /api/patients/{id}/
```

#### Create Patient
```
POST /api/patients/
```

Request Body:
```json
{
  "unique_id": "PAT002",
  "first_name": "Jane",
  "last_name": "Smith",
  "date_of_birth": "1985-03-20",
  "gender": "F",
  "address": "456 Oak Ave",
  "phone": "+1987654321",
  "email": "jane@example.com",
  "insurance_provider": "Aetna",
  "medical_history": "Diabetes Type 2"
}
```

#### Update Patient
```
PUT /api/patients/{id}/
PATCH /api/patients/{id}/
```

#### Delete Patient
```
DELETE /api/patients/{id}/
```

#### Get Admitted Patients
```
GET /api/patients/admitted_patients/
```

#### Discharge Patient
```
POST /api/patients/{id}/discharge/
```

---

### 2. Staff API

#### List All Staff
```
GET /api/staff/
```

Query Parameters:
- `search`: Search by staff_id, first_name, last_name, email, role
- `ordering`: Order by hire_date, first_name, last_name

Example:
```bash
curl -X GET "http://localhost:8000/api/staff/?search=doctor&ordering=first_name"
```

Response:
```json
{
  "count": 50,
  "results": [
    {
      "id": 1,
      "staff_id": "STF001",
      "first_name": "Dr. Robert",
      "last_name": "Johnson",
      "full_name": "Dr. Robert Johnson",
      "role": "DOCTOR",
      "department": "CARDIOLOGY",
      "phone": "+1234567890",
      "email": "robert.johnson@hospital.com",
      "schedule": "Mon-Fri 9AM-5PM",
      "hire_date": "2020-01-15",
      "is_active": true,
      "is_medical_staff": true
    }
  ]
}
```

#### Get Staff Details
```
GET /api/staff/{id}/
```

#### Create Staff Member
```
POST /api/staff/
```

Request Body:
```json
{
  "staff_id": "STF002",
  "first_name": "Sarah",
  "last_name": "Wilson",
  "role": "NURSE",
  "department": "ICU",
  "phone": "+1987654321",
  "email": "sarah.wilson@hospital.com",
  "schedule": "Shifts"
}
```

#### Update Staff
```
PUT /api/staff/{id}/
PATCH /api/staff/{id}/
```

#### Delete Staff
```
DELETE /api/staff/{id}/
```

#### Get Medical Staff Only
```
GET /api/staff/medical_staff/
```

#### Get Staff by Department
```
GET /api/staff/by_department/?department=CARDIOLOGY
```

---

### 3. Appointments API

#### List All Appointments
```
GET /api/appointments/
```

Query Parameters:
- `search`: Search by patient/doctor names
- `ordering`: Order by appointment_date, status
- `page`: Page number

Example:
```bash
curl -X GET "http://localhost:8000/api/appointments/?search=john&status=Scheduled"
```

Response:
```json
{
  "count": 25,
  "results": [
    {
      "id": 1,
      "patient": 1,
      "patient_detail": {
        "id": 1,
        "unique_id": "PAT001",
        "first_name": "John",
        "last_name": "Doe",
        "full_name": "John Doe",
        "email": "john@example.com",
        "phone": "+1234567890"
      },
      "doctor": 1,
      "doctor_detail": {
        "id": 1,
        "staff_id": "STF001",
        "first_name": "Dr. Robert",
        "last_name": "Johnson",
        "full_name": "Dr. Robert Johnson",
        "role": "DOCTOR",
        "department": "CARDIOLOGY"
      },
      "appointment_date": "2024-02-20T14:00:00Z",
      "reason": "Regular checkup",
      "status": "Scheduled"
    }
  ]
}
```

#### Get Appointment Details
```
GET /api/appointments/{id}/
```

#### Create Appointment
```
POST /api/appointments/
```

Request Body:
```json
{
  "patient": 1,
  "doctor": 1,
  "appointment_date": "2024-02-20T14:00:00Z",
  "reason": "Regular checkup",
  "status": "Scheduled"
}
```

#### Update Appointment
```
PUT /api/appointments/{id}/
PATCH /api/appointments/{id}/
```

#### Delete Appointment
```
DELETE /api/appointments/{id}/
```

#### Get Scheduled Appointments
```
GET /api/appointments/scheduled/
```

#### Get Upcoming Appointments
```
GET /api/appointments/upcoming/
```

---

### 4. Billing API

#### List All Invoices
```
GET /api/invoices/
```

Query Parameters:
- `search`: Search by patient unique_id, first_name, last_name
- `ordering`: Order by issue_date, due_date, total_amount
- `page`: Page number

Example:
```bash
curl -X GET "http://localhost:8000/api/invoices/?ordering=-issue_date"
```

Response:
```json
{
  "count": 150,
  "results": [
    {
      "id": 1,
      "patient": 1,
      "patient_detail": {
        "id": 1,
        "unique_id": "PAT001",
        "first_name": "John",
        "last_name": "Doe",
        "full_name": "John Doe"
      },
      "issue_date": "2024-01-15",
      "due_date": "2024-02-15",
      "total_amount": "5000.00",
      "paid": false,
      "insurance_claimed": false,
      "details": "Hospital admission charges"
    }
  ]
}
```

#### Get Invoice Details
```
GET /api/invoices/{id}/
```

#### Create Invoice
```
POST /api/invoices/
```

Request Body:
```json
{
  "patient": 1,
  "issue_date": "2024-01-15",
  "due_date": "2024-02-15",
  "total_amount": "5000.00",
  "paid": false,
  "insurance_claimed": false,
  "details": "Hospital admission charges"
}
```

#### Update Invoice
```
PUT /api/invoices/{id}/
PATCH /api/invoices/{id}/
```

#### Delete Invoice
```
DELETE /api/invoices/{id}/
```

#### Get Unpaid Invoices
```
GET /api/invoices/unpaid/
```

#### Get Overdue Invoices
```
GET /api/invoices/overdue/
```

#### Mark Invoice as Paid
```
POST /api/invoices/{id}/mark_paid/
```

---

## Error Responses

All error responses follow this format:

### 400 Bad Request
```json
{
  "error": "Invalid request data",
  "details": {
    "field_name": ["Error message"]
  }
}
```

### 401 Unauthorized
```json
{
  "detail": "Authentication credentials were not provided."
}
```

### 403 Forbidden
```json
{
  "detail": "You do not have permission to perform this action."
}
```

### 404 Not Found
```json
{
  "detail": "Not found."
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error."
}
```

---

## Pagination

By default, API responses are paginated with 20 items per page. Use the `page` parameter to navigate:

```bash
curl -X GET "http://localhost:8000/api/patients/?page=2"
```

Response includes:
- `count`: Total number of items
- `next`: URL to next page
- `previous`: URL to previous page
- `results`: Array of items

---

## Filtering & Searching

### Search
Use the `search` parameter to search across multiple fields:

```bash
curl -X GET "http://localhost:8000/api/patients/?search=john"
```

### Ordering
Use the `ordering` parameter to sort results (prefix with `-` for descending):

```bash
curl -X GET "http://localhost:8000/api/appointments/?ordering=-appointment_date"
```

---

## Rate Limiting

Currently, there is no rate limiting implemented. In production, consider adding:
- Django REST Framework's throttling
- API key-based rate limiting
- IP-based rate limiting

---

## Examples

### Get all admitted patients
```bash
curl -X GET "http://localhost:8000/api/patients/admitted_patients/" \
  -H "Authorization: Bearer your-token"
```

### Schedule a new appointment
```bash
curl -X POST "http://localhost:8000/api/appointments/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-token" \
  -d '{
    "patient": 1,
    "doctor": 1,
    "appointment_date": "2024-02-25T15:00:00Z",
    "reason": "Follow-up consultation",
    "status": "Scheduled"
  }'
```

### Mark invoice as paid
```bash
curl -X POST "http://localhost:8000/api/invoices/1/mark_paid/" \
  -H "Authorization: Bearer your-token"
```

### Get all unpaid invoices sorted by due date
```bash
curl -X GET "http://localhost:8000/api/invoices/unpaid/?ordering=due_date" \
  -H "Authorization: Bearer your-token"
```

---

## API Testing Tools

- **Postman**: Import the API endpoints for easy testing
- **curl**: Command-line HTTP client
- **Thunder Client**: VS Code extension for API testing
- **Insomnia**: Modern API client
- **httpie**: User-friendly command-line HTTP client

---

## Support

For API issues or questions, please open an issue on GitHub or contact the development team.
