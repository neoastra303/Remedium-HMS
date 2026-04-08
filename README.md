# Remedium Hospital Management System

![Django](https://img.shields.io/badge/Django-5.0.9-092E20?style=for-the-badge&logo=django)
![Python](https://img.shields.io/badge/Python-3.13-3776AB?style=for-the-badge&logo=python)
![DRF](https://img.shields.io/badge/DRF-3.14-A30000?style=for-the-badge&logo=django)
![Tests](https://img.shields.io/badge/Tests-93%20Passing-brightgreen?style=for-the-badge)
![Coverage](https://img.shields.io/badge/Coverage-75%25-yellowgreen?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)

Comprehensive REST API-driven Hospital Management System with 14 Django apps, role-based access, FDA drug integration, and interactive API documentation.

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
│              Role-Based Auth  •  Audit Trails                    │
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
- **93 Automated Tests** — 75% coverage across all apps
- **Role-Based Access** — Admin, Doctor, Nurse, Receptionist, Pharmacist, Lab Technician
- **Audit Trails** — Historical records on all clinical models
- **API Documentation** — Swagger UI + ReDoc (OpenAPI 3.0)
- **Docker Support** — Non-root user, health checks, production-ready
- **CI/CD Pipeline** — GitHub Actions with linting, testing, security scanning

## 📊 Tech Stack

| Layer | Technology |
|---|---|
| **Backend** | Django 5.0.9, Python 3.13 |
| **API** | Django REST Framework 3.14 |
| **Database** | SQLite (dev) → PostgreSQL (prod) |
| **Frontend** | Bootstrap 5.3, Bootstrap Icons, Chart.js |
| **API Docs** | drf-spectacular (OpenAPI 3.0) |
| **Testing** | pytest + pytest-cov (93 tests) |
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
python manage.py createsuperuser

# 6. Run server
python manage.py runserver
```

**Access the app:** `http://localhost:8000`  
**Admin panel:** `http://localhost:8000/admin/`

### Docker (Production)

```bash
docker-compose up -d
```

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

**Results:** 93 passed, 0 failed, 75% coverage

## 📁 Project Structure

```
Remedium-HMS/
├── remedium_hms/          # Django project settings
├── core/                  # Health checks, permissions, dashboard
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
├── templates/             # Base templates
├── docker-compose.yml
├── Dockerfile
└── .github/workflows/ci.yml
```

## 🔐 Security Features

- **Rate Limiting** — 100 req/hr (anon), 1000 req/hr (authenticated)
- **Brute-Force Protection** — Throttled token auth endpoint
- **Encrypted API Keys** — Fernet encryption for external integrations
- **HSTS Headers** — HTTPS enforcement in production
- **Role-Based Permissions** — 6 user roles with granular access
- **Non-Root Docker** — Container runs as `appuser`
- **File Validation** — 10MB upload limit, extension whitelist

## 📋 User Roles

| Role | Capabilities |
|---|---|
| **Admin** | Full access to all modules |
| **Doctor** | Patients, appointments, lab tests, prescriptions, surgery, care monitoring |
| **Nurse** | Patients, appointments, care monitoring |
| **Receptionist** | Patient registration, appointments, billing |
| **Pharmacist** | Prescriptions, inventory, patient lookup |
| **Lab Technician** | Lab tests, patient lookup |

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
| **API Endpoints** | 40+ |
| **Tests** | 93 |
| **Coverage** | 75% |
| **Commits** | 100+ |
| **Models** | 25+ |
| **Templates** | 30+ |

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
