# Remedium Hospital Management System

![Django](https://img.shields.io/badge/Django-5.2.14-092E20?style=for-the-badge&logo=django)
![Python](https://img.shields.io/badge/Python-3.13-3776AB?style=for-the-badge&logo=python)
![DRF](https://img.shields.io/badge/DRF-3.16-A30000?style=for-the-badge&logo=django)
![Tests](https://img.shields.io/badge/Tests-113%20Passing-brightgreen?style=for-the-badge)
![Coverage](https://img.shields.io/badge/Coverage-75%25-yellowgreen?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)

Comprehensive REST API-driven Hospital Management System with 14 Django apps, role-based dashboards, FDA drug integration, and interactive API documentation.

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Remedium HMS                              │
├────────────┬────────────┬───────────────┬───────────────────────┤
│  Core Apps │  Clinical  │  Operations   │  Support              │
├────────────┼────────────┼───────────────┼───────────────────────┤
│ core       │ patients   │ appointments  │ hospital              │
│ staff      │ medical_   │ billing       │ inventory             │
│            │ records    │ pharmacy      │ reporting             │
│            │ laboratory │ surgery       │ integration           │
│            │ care_      │ notifications │                       │
│            │ monitoring │               │                       │
├────────────┴────────────┴───────────────┴───────────────────────┤
│              REST API (DRF)  •  OpenAPI 3.0 Docs                 │
│         Role-Based Dashboards  •  Glassmorphic UI               │
├─────────────────────────────────────────────────────────────────┤
│              SQLite (dev)  →  PostgreSQL (prod)                  │
└─────────────────────────────────────────────────────────────────┘
```

## 🌟 Key Features

### Clinical
- **Patient Management** — Full demographics, medical history, admission/discharge tracking
- **Appointment Scheduling** — Intelligent conflict prevention with real-time availability
- **Lab Test Management** — Test ordering, results tracking, LOINC-ready
- **Prescription Management** — Drug tracking with **OpenFDA integration** for live drug info
- **Care Monitoring** — Vital signs tracking, BMI calculation, critical condition alerts
- **Surgery Management** — Operating room scheduling, surgeon assignment
- **Medical Records** — Document management with file upload (PDF, images)

### Operations
- **Billing & Invoicing** — Auto-numbered invoices (`INV-YYYY-NNNNN`), payment tracking
- **Staff Management** — Shift scheduling, role-based permissions, password reset
- **Inventory Control** — Stock tracking, reorder alerts, cost-per-unit
- **Ward & Room Management** — Bed allocation, ward capacity tracking

### Platform
- **14 Django Apps** — Modular, maintainable architecture
- **113 Automated Tests** — 75% coverage across all apps
- **Role-Based Dashboards** — 8 tailored dashboards for every role
- **Audit Trails** — Historical records on all clinical models
- **API Documentation** — Swagger UI + ReDoc (OpenAPI 3.0)
- **Docker Support** — Non-root user, health checks, production-ready
- **CI/CD Pipeline** — GitHub Actions with linting, testing, security scanning

## 📊 Tech Stack

| Layer | Technology |
|---|---|
| **Backend** | Django 5.2.14, Python 3.13 |
| **API** | Django REST Framework 3.16 |
| **Database** | SQLite (dev) → PostgreSQL (prod) |
| **Frontend** | Bootstrap 5.3, Bootstrap Icons, Chart.js, Glassmorphic Design System |
| **API Docs** | drf-spectacular (OpenAPI 3.0) |
| **Testing** | pytest + pytest-cov (113 tests) |
| **Security** | Rate limiting, Fernet encryption, HSTS |
| **Deployment** | Docker, Gunicorn, Whitenoise |
| **CI/CD** | GitHub Actions (flake8, bandit, pytest) |
| **External APIs** | OpenFDA (drug labels, adverse events) |

## 🚀 Quick Start

### Local Development

```bash
# 1. Clone and setup
git clone https://github.com/neoastra303/Remedium-HMS.git
cd Remedium-HMS

# 2. Virtual environment
python -m venv venv
venv\Scripts\activate   # Windows
# source venv/bin/activate  # Linux/Mac

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Edit .env and set SECRET_KEY (or leave blank for auto-generation)

# 5. Database setup
python manage.py migrate
python manage.py create_groups

# 6. Seed demo data (optional — creates users for all 13 roles)
python manage.py create_role_users

# 7. Run server
python manage.py runserver
```

**Access the app:** `http://localhost:8000`  
**Admin panel:** `http://localhost:8000/admin/`

### Docker (Production)

```bash
docker-compose up -d
```

## 👥 Role-Specific Dashboards

Each role gets a tailored dashboard on login with relevant stats, quick actions, and data:

| Role | Dashboard | Key Metrics |
|------|-----------|-------------|
| **Administrator** | `admin_dashboard.html` | Revenue, dept load, active staff, recent invoices, admin links |
| **Doctor** | `doctor_dashboard.html` | Today's schedule, active patients, recent vitals, prescriptions |
| **Nurse** | `nurse_dashboard.html` | Critical/stable patients, vitals log, new admissions |
| **Receptionist** | `receptionist_dashboard.html` | Appointments, check-ins, doctor availability, queue tracker |
| **Pharmacist** | `pharmacist_dashboard.html` | Pending rx, low stock, dispensed today, inventory alerts |
| **Lab Technician** | `labtech_dashboard.html` | Pending/completed tests, results queue, today's requests |
| **Surgeon / Anesthesiologist** | `surgeon_dashboard.html` | Surgery schedule, pre-op patients, completed surgeries |
| **Other roles** | `default_dashboard.html` | General stats and quick links |

## 🔐 Test Accounts

Run `python manage.py create_role_users` to seed one user per role:

| Username | Role | Password |
|----------|------|----------|
| `admin` | Administrator | `password123` |
| `doctor` | Doctor | `password123` |
| `nurse` | Nurse | `password123` |
| `surgeon` | Surgeon | `password123` |
| `anesthesiologist` | Anesthesiologist | `password123` |
| `radiologist` | Radiologist | `password123` |
| `receptionist` | Receptionist | `password123` |
| `pharmacist` | Pharmacist | `password123` |
| `labtech` | Lab Technician | `password123` |
| `technician` | Technician | `password123` |
| `security` | Security | `password123` |
| `maintenance` | Maintenance | `password123` |
| `other` | Other | `password123` |

## 🎨 UI/UX Design

The frontend features a custom **glassmorphic design system** built on Bootstrap 5.3:

- **Glassmorphism** — Frosted-glass cards with backdrop blur and subtle borders
- **Animations** — Fade-in-up entrance, stagger-children, shimmer skeletons, floating login blobs
- **Design Tokens** — CSS custom properties for colors, radii, shadows, and transitions
- **Responsive** — Mobile-optimized tables, stacked nav, touch-friendly buttons
- **Accessibility** — Focus rings, skip-to-content, ARIA labels, semantic HTML
- **Feedback** — Stacking toasts, button spinners, loading overlay, scroll-to-top
- **Scrollbar** — Custom thin scrollbar for WebKit browsers

## 📡 API

All API endpoints are versioned under `/api/v1/`.

### Authentication
```bash
# Get token
curl -X POST http://localhost:8000/api-token-auth/ \
  -d '{"username":"admin","password":"password"}'

# Use token
curl -H "Authorization: Token YOUR_TOKEN" \
  http://localhost:8000/api/v1/patients/
```

### API Documentation

| Endpoint | Description |
|---|---|
| `/api/v1/docs/` | Interactive Swagger UI (Swagger.js) |
| `/api/v1/redoc/` | ReDoc documentation |
| `/api/v1/schema/` | Raw OpenAPI 3.0 JSON |

### Key API Endpoints

| Resource | Endpoints |
|---|---|
| **Patients** | `/api/v1/patients/`, `/api/v1/patients/{id}/discharge/` |
| **Staff** | `/api/v1/staff/`, `/api/v1/staff/{id}/reset-password/` |
| **Appointments** | `/api/v1/appointments/`, `/api/v1/appointments/scheduled/` |
| **Invoices** | `/api/v1/invoices/`, `/api/v1/invoices/{id}/mark_paid/` |
| **Lab Tests** | `/api/v1/lab-tests/` |
| **Prescriptions** | `/api/v1/prescriptions/`, `/api/v1/prescriptions/drug-info/`, `/api/v1/prescriptions/adverse-events/` |

## 🧪 Testing

```bash
# Run all tests
python -m pytest --tb=line -q

# Run with coverage
python -m pytest --cov=. --cov-report=term-missing

# Run specific app
python -m pytest pharmacy/tests.py -v
```

**Results:** 113 passed, 0 failed, 75% coverage

## 📁 Project Structure

```
Remedium-HMS/
├── remedium_hms/          # Django project settings
├── core/                  # Health checks, permissions, dashboard views
├── patients/              # Patient management
├── staff/                 # Staff & user management
├── appointments/          # Scheduling system
├── billing/               # Invoices & payments
├── pharmacy/              # Prescriptions + OpenFDA integration
├── laboratory/            # Lab test management
├── surgery/               # Operating room scheduling
├── care_monitoring/       # Vital signs tracking
├── medical_records/       # Document management
├── notifications/         # SMS/Email notifications
├── integration/           # External API integrations
├── inventory/             # Stock management
├── hospital/              # Ward & room management
├── reporting/             # Analytics & reports
├── templates/
│   ├── base.html          # Master layout with glassmorphic nav
│   ├── index.html         # Public landing page
│   ├── dashboards/        # 8 role-specific dashboard templates
│   └── partials/          # Reusable breadcrumb, pagination, field components
├── static/
│   ├── css/custom.css     # Glassmorphic design system (1200+ lines)
│   └── js/                # API client, AJAX helpers, UI feedback
├── docker-compose.yml
├── Dockerfile
└── .github/workflows/ci.yml
```

## 🔐 Security Features

- **Rate Limiting** — 100 req/hr (anon), 1000 req/hr (authenticated)
- **Brute-Force Protection** — Throttled token auth endpoint
- **Encrypted API Keys** — Fernet encryption for external integrations
- **HSTS Headers** — HTTPS enforcement in production
- **Role-Based Permissions** — 13 user roles with granular access controls
- **Non-Root Docker** — Container runs as `appuser`
- **File Validation** — 10MB upload limit, extension whitelist

## 📋 User Roles

| Role | Dashboard | Capabilities |
|------|-----------|-------------|
| **Admin** | Full admin dashboard | Full system access, all modules, admin panel |
| **Doctor** | Clinical dashboard | Patients, appointments, vitals, prescriptions, surgery |
| **Nurse** | Nursing dashboard | Patients, appointments, care monitoring, vitals |
| **Surgeon** | Surgery dashboard | Surgery schedule, patients, appointments, vitals |
| **Anesthesiologist** | Surgery dashboard | Surgery schedule, patients |
| **Radiologist** | Default dashboard | Clinical tools, patients |
| **Receptionist** | Reception dashboard | Patient registration, appointments, billing, queue |
| **Pharmacist** | Pharmacy dashboard | Prescriptions, inventory, patient lookup |
| **Lab Technician** | Lab dashboard | Lab tests, results, patient lookup |
| **Technician** | Default dashboard | General access |
| **Security** | Default dashboard | Limited access |
| **Maintenance** | Default dashboard | Limited access |
| **Other** | Default dashboard | General access |

## 🌍 Deployment

### Environment Variables

```env
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgresql://user:pass@db:5432/remedium
```

### Production Stack

```
Nginx → Gunicorn → Django → PostgreSQL
              ↓
          Redis (caching - planned)
          Celery (async tasks - planned)
```

See `DEPLOYMENT.md` for full production guide.

## 📊 Project Stats

| Metric | Value |
|---|---|
| **Django Apps** | 14 |
| **API Endpoints** | 50+ |
| **Tests** | 118 |
| **Coverage** | 83% |
| **Templates** | 78+ (8 role-specific dashboards) |
| **User Roles** | 13 |
| **Commits** | 100+ |
| **Models** | 25+ |

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Make your changes
4. Run tests: `python -m pytest --tb=line -q`
5. Push and open a Pull Request

See `CONTRIBUTING.md` for detailed guidelines.

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **OpenFDA** — Free drug label and adverse event data
- **Bootstrap** — Modern UI components
- **Chart.js** — Vital signs visualization

---

**Remedium HMS** — Empowering Healthcare, One System at a Time

Built with ❤️ by [neoastra303](https://github.com/neoastra303)
