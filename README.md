# Remedium Hospital Management System (HMS)

<div align="center">

![Remedium Logo](https://raw.githubusercontent.com/neoastra303/Remedium-HMS/main/static/img/hero-logo.png)

**An Enterprise-Grade, HIPAA-Ready Modular Monolith for Modern Healthcare.**

[![Django](https://img.shields.io/badge/Django-5.2.14-092E20?style=for-the-badge&logo=django)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.13-3776AB?style=for-the-badge&logo=python)](https://www.python.org/)
[![DRF](https://img.shields.io/badge/DRF-3.16-A30000?style=for-the-badge&logo=django)](https://www.django-rest-framework.org/)
[![Security](https://img.shields.io/badge/Security-PHI_Encrypted-blue?style=for-the-badge&logo=googlesheets)](https://github.com/neoastra303/Remedium-HMS)
[![Tests](https://img.shields.io/badge/Tests-113_Passing-brightgreen?style=for-the-badge)](https://github.com/neoastra303/Remedium-HMS)
[![Coverage](https://img.shields.io/badge/Coverage-83%25-success?style=for-the-badge)](https://github.com/neoastra303/Remedium-HMS)

[**Explore API Docs**](http://localhost:8000/api/v1/docs/) • [**Quick Start**](#-quick-start) • [**Role Dashboards**](#-intelligent-role-dashboards) • [**Architecture**](#-architectural-vision)

</div>

---

## 💎 The Remedium Difference

Remedium-HMS is not just another CRUD app. It is a high-security, auditable, and modular enterprise platform designed to handle the complexities of modern hospital operations.

### **🛡️ Security-First Core**
*   **PHI Encryption at Rest:** Sensitive Patient Health Information (Phone, Email, Medical History) is encrypted at the database layer using industry-standard Fernet symmetric encryption.
*   **Immutable Audit Trails:** Powered by `simple-history`, every clinical change is tracked. Soft-delete logic ensures records are never lost, only archived for legal compliance.
*   **Granular RBAC:** 13 distinct user roles with 8 tailored dashboards ensure clinical staff see what they need, while administrative staff manage what they must.

### **🏥 Clinical Excellence**
*   **OpenFDA Integration:** Real-time drug information and adverse event tracking via the official FDA API.
*   **Intelligent Care Monitoring:** Vital signs visualization with BMI calculation and critical condition flagging.
*   **Conflict-Aware Scheduling:** Smart appointment engine that prevents doctor double-booking and respects work shifts.

### **✨ Glassmorphic UI/UX**
*   A premium, modern interface utilizing **Backdrop Blurs**, **Staggered Animations**, and **Shimmer Skeletons** to provide a fluid, "living" application feel that moves beyond standard Bootstrap.

---

## 🏗️ Architectural Vision

Remedium follows a **Modular Monolith** pattern, ensuring strict boundaries between 14 specialized domains while maintaining a unified, high-performance core.

```mermaid
graph TD
    subgraph Core_Layer [Platform Foundation]
        A[Core & RBAC]:::core
        S[Staff & Auth]:::core
    end

    subgraph Clinical_Domain [Clinical Excellence]
        B1[Patients]:::clinical
        B2[Medical Records]:::clinical
        B3[Laboratory]:::clinical
        B4[Care Monitoring]:::clinical
    end
    
    subgraph Operations_Domain [Operations & Finance]
        C1[Appointments]:::ops
        C2[Billing & Ledger]:::ops
        C3[Pharmacy]:::ops
        C4[Surgery]:::ops
    end
    
    subgraph Support_Domain [Infrastructure]
        D1[Inventory]:::infra
        D2[Reporting]:::infra
        D3[Integration]:::infra
        D4[Hospital Units]:::infra
    end

    A --> Clinical_Domain
    A --> Operations_Domain
    A --> Support_Domain

    classDef core fill:#f9f,stroke:#333,stroke-width:2px,color:#000
    classDef clinical fill:#bbf,stroke:#333,stroke-width:2px,color:#000
    classDef ops fill:#dfd,stroke:#333,stroke-width:2px,color:#000
    classDef infra fill:#ffd,stroke:#333,stroke-width:2px,color:#000
```

### **🔄 The Patient Journey (Full-Cycle Flow)**

```mermaid
sequenceDiagram
    autonumber
    participant P as 👤 Patient
    participant R as 🏢 Reception
    participant D as 🩺 Doctor
    participant L as 🔬 Lab/Pharmacy
    participant B as 💰 Billing (Ledger)

    P->>R: Initial Registration & Triage
    Note right of R: RBAC: Receptionist Role
    R->>D: Digital Queue Assignment
    D->>P: Physical Consultation
    rect rgb(240, 240, 255)
        Note over D,P: Vitals Capture & PHI Encryption
    end
    D->>L: Electronic Order (Lab/Rx)
    L-->>D: Results Entry / Medication Dispense
    D->>B: Finalize Encounter
    B->>P: Immutable Ledger Invoice Generated
```

---

## 🛡️ Security & Integrity Lifecycle

Every record in Remedium follows a strictly protected lifecycle to ensure data privacy (HIPAA compliance ready) and legal auditability.

```mermaid
stateDiagram-v2
    [*] --> PlainText: Input Data
    PlainText --> DB: Field-Level Encryption (Fernet)
    state DB {
        [*] --> Active: "is_deleted = False"
        Active --> SoftDeleted: User Clicks Delete
        SoftDeleted --> Active: Admin Restore
        SoftDeleted --> Archival: "is_deleted = True"
    }
    DB --> Output: Transparent Decryption (Python Layer)
    Output --> [*]
```

---

## 🎨 Professional Interface Showcase

The frontend utilizes a custom **Glassmorphic Design System** that prioritizes clinical focus and visual comfort.

<div align="center">

| **The Clinical Cockpit (Doctor)** | **Administrative Analytics** |
|:---:|:---:|
| ![Doctor View](https://raw.githubusercontent.com/neoastra303/Remedium-HMS/main/design/wireframes/doctor-view.png) | ![Admin View](https://raw.githubusercontent.com/neoastra303/Remedium-HMS/main/design/wireframes/admin-view.png) |
| *High-density data visualization for rapid clinical decision-making.* | *Real-time hospital occupancy and revenue stream tracking.* |

| **Ward Management (Nurse)** | **Pharmacy Control** |
|:---:|:---:|
| ![Nurse View](https://raw.githubusercontent.com/neoastra303/Remedium-HMS/main/design/wireframes/nurse-view.png) | ![Pharmacy View](https://raw.githubusercontent.com/neoastra303/Remedium-HMS/main/design/wireframes/pharmacy-view.png) |
| *Visual bed map and urgent medication countdown trackers.* | *OpenFDA integrated drug search and dispense queue management.* |

| **Laboratory Information** | **Reception & Gateway** |
|:---:|:---:|
| ![Lab View](https://raw.githubusercontent.com/neoastra303/Remedium-HMS/main/design/wireframes/lab-view.png) | ![Reception View](https://raw.githubusercontent.com/neoastra303/Remedium-HMS/main/design/wireframes/receptionist-view.png) |
| *Automated test queue with critical range flagging and rapid entry.* | *Streamlined patient registration and ledger-based rapid billing.* |

</div>

---

## 📊 Tech Stack

| Layer | Technology |
|---|---|
| **Backend** | Django 5.2.14, Python 3.13, DRF 3.16 |
| **Database** | SQLite (Dev) • PostgreSQL (Prod) • PHI Encryption |
| **Frontend** | Bootstrap 5.3, Custom Glassmorphism, Chart.js, Vanilla JS/jQuery |
| **DevOps** | Docker (Non-Root), Gunicorn, WhiteNoise, GitHub Actions |
| **API Docs** | OpenAPI 3.0 (Swagger UI + ReDoc) |
| **Integrations** | OpenFDA API, SMTP Console/Gmail |

---

## 👥 Intelligent Role Dashboards

Each role is granted unique permissions and a specialized landing page.

| Role | Interface | Key Features |
|:---:|:---|---|
| **Doctor** | `doctor_dashboard.html` | Schedule, active patients, vitals visualization, rapid Rx. |
| **Nurse** | `nurse_dashboard.html` | Ward tracking, vitals log, admission management. |
| **Admin** | `admin_dashboard.html` | Revenue analytics, department load, staff management. |
| **Pharmacist** | `pharmacist_dashboard.html` | Stock alerts, Rx queue, OpenFDA lookups. |
| **Reception** | `reception_dashboard.html` | Check-in queue, billing flow, doctor availability. |

### **🔐 Test Accounts (Demo Seeding)**

Run `python manage.py create_role_users` to explore the system with any of these pre-configured roles:

| Username | Role | Dashboard Access | Password |
|:---|:---|:---|:---|
| `admin` | Administrator | Full Analytics & Operations | `password123` |
| `doctor` | Doctor | Clinical Consultation & vitals | `password123` |
| `nurse` | Nurse | In-patient monitoring | `password123` |
| `pharmacist` | Pharmacist | Inventory & OpenFDA Portal | `password123` |
| `labtech` | Lab Technician | Result Entry & Queue | `password123` |
| `receptionist` | Receptionist | Check-in & Ledger Billing | `password123` |

---

## 🚀 Quick Start

### 1. Setup Environment
```bash
git clone https://github.com/neoastra303/Remedium-HMS.git
cd Remedium-HMS
python -m venv venv
source venv/bin/activate  # venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### 2. Initialize Database
```bash
python manage.py migrate
python manage.py create_groups  # Essential for RBAC
python manage.py create_role_users  # Optional: Seed test accounts
```

### 3. Launch
```bash
python manage.py runserver
```
Access at `http://localhost:8000`. Login with `admin` / `password123` if you seeded test accounts.

---

## 📡 API Ecosystem

All endpoints are versioned under `/api/v1/`.

*   **Swagger UI:** `/api/v1/docs/`
*   **ReDoc:** `/api/v1/redoc/`
*   **Auth:** JWT-based or Token-based headers.

**Key Endpoint Groups:**
*   `/patients/` — Demographics & Discharge logic.
*   `/prescriptions/` — Rx management + OpenFDA search.
*   `/invoices/` — Ledger-based billing.

---

## 🧪 Quality Assurance

We maintain a high bar for reliability:
```bash
python -m pytest --cov=. --cov-report=term-missing
```
**Current Status:** 113+ Tests • 83% Coverage • Zero Critical Vulnerabilities.

---

## 🤝 Contributing & Support

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) and [SECURITY.md](SECURITY.md).

**Remedium HMS** — *Empowering Healthcare, One System at a Time.*

Built with ❤️ by [neoastra303](https://github.com/neoastra303)
