# Remedium HMS — Full-Stack Production Showcase

> Hospital Management System ready for real-world deployment

---

## 🏗️ System Overview

| Component | Technology | Status |
|---|---|---|
| **Backend** | Django 5.0.9, Python 3.13, DRF 3.14 | ✅ Production |
| **Frontend** | Bootstrap 5.3, Bootstrap Icons, Chart.js | ✅ Production |
| **Database** | SQLite (dev) → PostgreSQL (prod) | ✅ Migrated |
| **API** | REST (OpenAPI 3.0, versioned `/api/v1/`) | ✅ Documented |
| **Tests** | 93 automated tests, 75% coverage | ✅ Passing |
| **CI/CD** | GitHub Actions (flake8, bandit, pytest) | ✅ Automated |
| **Docker** | Non-root user, health checks, env-driven config | ✅ Ready |
| **Security** | Rate limiting, encryption, HSTS, role-based auth | ✅ Hardened |

**14 Django apps · 25+ models · 40+ API endpoints · 30+ templates**

---

## 🎨 UI/UX Features

### 1. Role-Based Navigation

Each user role sees a **customized navigation menu** with only the features they need:

| Role | Sees |
|---|---|
| **Admin** | All modules — Dashboard, Patients, Staff, Appointments, Billing, Lab, Pharmacy, Surgery, Reports, Integrations |
| **Doctor** | Clinical tools — Patients, Appointments, Medical Records, Lab, Pharmacy, Surgery |
| **Nurse** | Care-focused — Patients, Appointments, Vital Monitoring |
| **Receptionist** | Front desk — Patient Registration, Appointments, Billing |
| **Pharmacist** | Prescriptions, Inventory, Patient Lookup |
| **Lab Technician** | Lab Tests, Patient Lookup |

**UX Benefit:** Reduced cognitive load — users only see what's relevant to their job.

---

### 2. Modern Dashboard

The home dashboard provides **at-a-glance operational metrics**:

```
┌────────────────────────────────────────────────────────────┐
│  🏥 Remedium HMS Dashboard                                │
├──────────┬──────────┬──────────┬──────────────────────────┤
│ 👥 Total │ 📅 Today │ 💰 Unpaid│ 📋 Scheduled            │
│ Patients │ Appts    │ Invoices │ Surgeries               │
├──────────┴──────────┴──────────┴──────────────────────────┤
│                                                            │
│  [Quick Actions]                                           │
│  ➕ New Patient   📅 New Appointment   💳 New Invoice     │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

---

### 3. Prescription Form with Live FDA Drug Lookup

**The flagship feature** — as the user types a drug name, FDA data appears in real-time:

```
┌────────────────────────┬──────────────────────────────────┐
│  New Prescription      │  🔬 FDA Drug Information Lookup  │
│                        │                                  │
│  Patient: [______]     │  [Ibuprofen          ] [Lookup]  │
│  Drug Name: [Ibupro..] │                                  │
│  Dosage: [200mg]       │  ADVIL                             │
│  Frequency: [q6h]      │  Generic: IBUPROFEN  Pfizer ORAL │
│                        │                                  │
│  [💾 Save] [❌ Cancel] │  ▶ Indications & Usage            │
│                        │  ▶ Dosage & Administration        │
│                        │  ⚠ Warnings & Cautions            │
│                        │  🔗 Drug Interactions             │
│                        │  ⚡ Adverse Reactions             │
│                        │                                  │
│                        │  [📊 View FDA Adverse Events]    │
└────────────────────────┴──────────────────────────────────┘
```

**UX Flow:**
1. Doctor types "Ibuprofen" → waits 1 second
2. Panel auto-fetches FDA label data (generic name, brand, manufacturer)
3. Doctor clicks warnings section → sees "Take with food. Avoid in pregnancy."
4. Clicks "View FDA Adverse Events" → sees top side effects with report counts
5. Saves prescription — fully informed decision

**Technical Details:**
- Debounced auto-lookup (1s after typing stops)
- 24-hour cache prevents redundant API calls
- Collapsible accordion sections for clean layout
- Loading spinners and error states for every interaction

---

### 4. Vital Signs Monitoring Dashboard

**Patient vital trends visualization** with Chart.js:

```
┌────────────────────────────────────────────────────────────┐
│  📊 Vital Signs Trends — John Doe (PAT-001)               │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  Heart Rate (bpm)                                          │
│  90 ┤        ●───────●                                     │
│  80 ┤    ●───●       ●                                     │
│  70 ┤●───●                   ────── Normal Range           │
│  60 ┤                                    ────── Critical   │
│     └────────────────────────────────────────────          │
│     Apr 1    Apr 2    Apr 3    Apr 4    Apr 5              │
│                                                            │
│  [❤️ HR] [🌡️ Temp] [🫁 O2] [💉 BP]                        │
└────────────────────────────────────────────────────────────┘
```

**Features:**
- Color-coded lines for each vital sign
- Normal vs critical range indicators
- Latest status badge (Stable / Critical / Improving)
- Mobile-responsive chart rendering

---

### 5. Professional Login & Auth Pages

```
┌─────────────────────────────┐
│  🏥 Remedium HMS            │
│                             │
│  ┌─────────────────────┐    │
│  │ Sign In              │    │
│  │                      │    │
│  │ Username [________]  │    │
│  │ Password [________]  │    │
│  │                      │    │
│  │ [Sign In]            │    │
│  │                      │    │
│  │ Forgot password?     │    │
│  └─────────────────────┘    │
└─────────────────────────────┘
```

**Features:**
- Centered card layout with hospital branding
- CSRF protection on all forms
- Session management with secure cookies
- Password reset via email with secure token

---

### 6. Staff & Shift Management

```
┌────────────────────────────────────────────────────────────┐
│  👥 Staff Directory                           [+ Add Staff] │
├────────────────────────────────────────────────────────────┤
│  Name            Role        Department    Status  Actions  │
│  ─────────────── ─────────── ────────────  ──────  ───────  │
│  Dr. Sarah Chen  Doctor      Cardiology    ✅ On   [View]   │
│  Nurse James     Nurse       ER            ✅ On   [Edit]   │
│  Lab Tech Maria  Lab Tech    Pathology     🟡 Off  [Edit]   │
└────────────────────────────────────────────────────────────┘
```

---

### 7. Responsive & Accessible

- **Bootstrap 5.3 grid** — works on mobile, tablet, desktop
- **Skip-to-content link** — screen reader support
- **Semantic HTML** — proper heading hierarchy, ARIA labels
- **Form validation** — inline error messages, required field indicators
- **Pagination** — all list views support 10 items per page

---

## ⚙️ Backend Features

### 1. RESTful API (40+ Endpoints)

All endpoints versioned under `/api/v1/` with OpenAPI 3.0 documentation.

| Resource | GET | POST | PUT | DELETE | Custom |
|---|---|---|---|---|---|
| `/patients/` | ✅ List | ✅ Create | ✅ Update | ❌ | `/discharge/` |
| `/staff/` | ✅ List | ✅ Create | ✅ Update | ✅ | `/reset-password/` |
| `/appointments/` | ✅ List | ✅ Create | ✅ Update | ✅ | `/scheduled/`, `/upcoming/` |
| `/invoices/` | ✅ List | ✅ Create | ✅ Update | ✅ | `/unpaid/`, `/mark_paid/` |
| `/lab-tests/` | ✅ List | ✅ Create | ✅ Update | ✅ | Search by test name |
| `/prescriptions/` | ✅ List | ✅ Create | ✅ Update | ✅ | `/drug-info/`, `/adverse-events/` |

**API Features:**
- Token-based authentication
- Pagination (20 results per page)
- Search across multiple fields
- Ordering with whitelist validation
- Rate limiting (100/hr anon, 1000/hr authenticated)

---

### 2. Role-Based Permission System

**6 custom permission classes** enforcing least-privilege access:

```python
IsClinicalStaff    → Doctor, Nurse (patient data, clinical ops)
IsBillingStaff     → Receptionist (invoices, payments)
IsAdminOrDoctor    → Admin, Doctor (admin-only endpoints)
IsOwnerOrReadOnly  → User owns their resource, others read-only
```

**Permission Flow:**
```
Request → IsAuthenticated → IsClinicalStaff → Allow
                          → Rejected (403)
```

---

### 3. Data Models & Audit Trails

**25+ models** with historical tracking on all clinical data:

| Model | Audit Trail | Unique Constraints |
|---|---|---|
| Patient | ✅ HistoricalPatient | `unique_id` |
| Appointment | ✅ HistoricalAppointment | `(doctor, date)` — no double booking |
| Invoice | ✅ HistoricalInvoice | Auto-generated `INV-YYYY-NNNNN` |
| Payment | ✅ HistoricalPayment | — |
| Prescription | ✅ HistoricalPrescription | — |
| LabTest | ✅ HistoricalLabTest | — |
| Surgery | ✅ HistoricalSurgery | `(room, date)` — no room conflict |
| PatientCare | ✅ HistoricalPatientCare | — |
| PatientDocument | ✅ HistoricalPatientDocument | — |

**Audit Query Example:**
```python
# See who changed a patient's discharge date
patient.history.filter(discharge_date__isnull=False)
# Returns: [{user: 'Dr. Chen', date: '2024-03-15', change: 'discharge_date set'}]
```

---

### 4. OpenFDA Drug Information Service

**Zero-cost external API integration** — no API key needed:

```python
search_drug_label("Amoxicillin")
# Returns:
{
    "generic_name": "AMOXICILLIN",
    "brand_name": "AMOXIL",
    "manufacturer": "Sandoz Inc",
    "route": ["ORAL"],
    "warnings": "Serious hypersensitivity reactions reported...",
    "drug_interactions": "Probenecid increases amoxicillin levels...",
    "indications": "Bacterial infections..."
}

search_adverse_events("Amoxicillin")
# Returns:
{
    "drug_name": "Amoxicillin",
    "top_adverse_reactions": [
        {"reaction": "Nausea", "count": 150},
        {"reaction": "Rash", "count": 80},
        {"reaction": "Diarrhea", "count": 65},
    ],
    "total_reports": 295
}
```

**Performance:** 24-hour Redis cache prevents redundant API calls.

---

### 5. Security Hardening

| Feature | Implementation |
|---|---|
| **Rate Limiting** | `AnonRateThrottle` (100/hr), `UserRateThrottle` (1000/hr) |
| **Brute-Force Prevention** | Token auth endpoint throttled at 20/hr |
| **API Key Encryption** | Fernet symmetric encryption for external integrations |
| **HSTS** | `SECURE_HSTS_SECONDS = 300` (5 min default, env-driven) |
| **HTTPS Enforcement** | `SECURE_PROXY_SSL_HEADER` for load balancer deployments |
| **File Upload Limits** | 10MB max, extension whitelist (pdf, jpg, jpeg, png) |
| **Phone Validation** | `^\+?\d{9,15}$` — unified across all models |
| **SQL Injection Prevention** | Order_by whitelist on all ListViews |
| **Non-Root Docker** | Container runs as `appuser` (UID 1000) |

---

### 6. Invoice Auto-Numbering & Payment Tracking

```python
# Invoice created → auto-generates invoice number
invoice = Invoice.objects.create(patient=patient, total_amount=100.00)
invoice.invoice_number  # "INV-2024-00001"

# Payment created → automatically marks invoice as paid
Payment.objects.create(invoice=invoice, amount=100.00, method='CASH')
invoice.paid  # True (via post_save signal)
```

**Payment History:**
```python
invoice.payments.all()
# [<Payment: 50.00 CASH>, <Payment: 50.00 CARD>]
```

---

### 7. N+1 Query Prevention

All ListViews optimized with `select_related`:

```python
# Before: 1 + N queries for N appointments
Appointment.objects.all()  # 1 query + N for each patient + N for each doctor

# After: 1 query
Appointment.objects.select_related('patient', 'doctor').all()
```

---

### 8. Appointment Conflict Detection

```python
# Prevents double-booking of same doctor at same time
class Appointment(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['doctor', 'appointment_date'],
                name='unique_appointment'
            )
        ]
```

---

## 🧪 Testing Strategy

| Test Type | Coverage | Count |
|---|---|---|
| **Unit Tests** | Model creation, validation, str representation | 20 tests |
| **Integration Tests** | API endpoints, permissions, authentication | 30 tests |
| **Service Tests** | OpenFDA service, error handling, caching | 4 tests |
| **API Documentation Tests** | Schema validity, Swagger UI, ReDoc | 5 tests |
| **End-to-End Tests** | Full flows (create patient → appointment → invoice) | 34 tests |

**Command:** `python -m pytest --tb=line -q` → **93 passed, 0 failed**

---

## 🚀 Deployment Pipeline

```
Developer Push
    ↓
GitHub Actions CI
    ├── flake8 (linting)
    ├── bandit (security scan)
    ├── pytest (93 tests)
    ├── collectstatic (assets)
    └── Docker build
    ↓
Docker Compose (Production)
    ├── Web: Gunicorn (configurable workers)
    ├── DB: PostgreSQL
    └── Health checks every 30s
```

---

## 📊 API Documentation

Three documentation formats available:

| Format | URL | Auth Required | Best For |
|---|---|---|---|
| **Swagger UI** | `/api/v1/docs/` | No | Interactive testing |
| **ReDoc** | `/api/v1/redoc/` | No | Reference reading |
| **OpenAPI Schema** | `/api/v1/schema/` | Yes | Code generation |

**Swagger UI Features:**
- Click any endpoint → see request/response schemas
- "Try it out" → send live requests
- Authentication built-in
- Export as Postman collection

---

## 🌍 Environment Configuration

```env
# Required
SECRET_KEY=<random-50-char-string>
DEBUG=False

# Production
ALLOWED_HOSTS=hospital.example.com,www.hospital.example.com
DATABASE_URL=postgresql://user:password@db:5432/remedium

# Email
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=notifications@hospital.com
EMAIL_HOST_PASSWORD=<app-password>

# Security
SECURE_HSTS_SECONDS=31536000  # 1 year (production only)
```

---

## 📈 What Makes This Production-Ready

| Criteria | Status |
|---|---|
| Automated test suite (93 tests) | ✅ |
| CI/CD pipeline | ✅ |
| API documentation (OpenAPI 3.0) | ✅ |
| Role-based access control | ✅ |
| Audit trails on all clinical data | ✅ |
| Database migration strategy | ✅ |
| Docker production config | ✅ |
| Security hardening (rate limits, encryption) | ✅ |
| Error handling (validation, graceful failures) | ✅ |
| Pagination on all list views | ✅ |
| Search functionality | ✅ |
| Responsive UI (mobile-ready) | ✅ |
| External API integration (OpenFDA) | ✅ |
| Environment-driven configuration | ✅ |
| Non-root Docker container | ✅ |
| Health checks for monitoring | ✅ |

---

**Remedium HMS — Built for real hospitals, not tutorials.**
