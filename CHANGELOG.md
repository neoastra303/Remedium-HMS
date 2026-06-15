# Changelog

All notable changes to Remedium HMS are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [Unreleased] - 2026-06-16

### Added
- implement global UX enhancements (Spotlight Search, page transitions, visual feedback) ([`2d122d0`])
- **surgery**: apply soft deletes to Surgery model ([`f212471`])
- **laboratory**: apply soft deletes to LabTest model ([`5863db6`])
- **pharmacy**: apply soft deletes to Prescription model ([`82d8999`])
- **billing**: apply soft deletes to Invoice and Payment models ([`e0f4a00`])
- **appointments**: apply soft deletes to Appointment model ([`19cc0a8`])
- **staff**: apply soft deletes to Staff model ([`4f7b9c1`])
- **patients**: apply soft deletes and PHI encryption to Patient model ([`86848ae`])
- implement project-wide soft delete and timestamp base model ([`ca773ba`])
- implement role-based view routing and context processor with full role flags ([`065a963`])
- create role-specific dashboards for admin, doctor, nurse, receptionist, pharmacist, labtech, surgeon, and default ([`29b438f`])
- implement receptionist toolkit (Check-in, Queue, Bed Map) ([`3e5d8ff`])
- full-stack UI upgrades for flexible data relations ([`d14427e`])
- professional dashboard redesign â€” consistent stat cards, component CSS, appointment rows, fix card-header color ([`9cca972`])
- UI/UX overhaul â€” grouped patient form, login redesign, empty states, card hover fix, form spinners, delete toasts ([`79b2786`])
- UI/UX overhaul â€” tabbed patient detail, crispy forms, print invoices, notification bell, Chart.js vitals, mobile CSS, fix all tests ([`712de13`])
- fix home URL bug, add whitenoise, 24 API tests, invoice counter, changelog CI check ([`2b9ecc2`])
- add REST API for hospital/inventory/surgery/care_monitoring, fix Redis default, add reporting tests, automate changelog ([`6a1fad5`])
- add seed_demo management command for realistic demo data ([`6824b78`])
- add API documentation with drf-spectacular ([`8915812`])
- integrate OpenFDA drug lookup with UI panel ([`168256e`])
- add new API endpoints and audit trails ([`e0c37f9`])
- add invoice auto-numbering and payment tracking ([`0b4b121`])
- add role-based API permissions and fix serializers ([`fda008d`])
- add Docker health checks and CI/CD pipeline ([`394cebf`])
- **pharmacy**: Add tests and improve code quality for pharmacy app ([`11966a9`])
- **billing**: Add tests and improve code quality for billing app ([`dbe3b4c`])
- **staff**: Add tests and improve code quality for staff app ([`07a8222`])

### Changed
- add high-fidelity SVG wireframes for all specialized dashboards ([`c7939cf`])
- modernize README with color-coded diagrams and security lifecycle flow ([`625441f`])
- expand README with clinical workflow, dashboard wireframes, and test accounts ([`fe03468`])
- redesign README with professional enterprise showcase and architecture diagram ([`76c2687`])
- add helper scripts for local admin and receptionist creation ([`526336c`])
- update completion summary with June 2026 refactoring details ([`7d85225`])
- add verification tests for database security and integrity ([`82788c2`])
- add encryption dependency and basic config ([`743e6b5`])
- update README with role-based dashboards, test accounts table, UI/UX design section ([`8551a4b`])
- add management command to create test users for all 13 roles ([`320ea92`])
- enhance list templates (appointments, staff, invoices) and partials (pagination, field, empty-state) ([`b0dbc30`])
- enhance patient templates and views with breadcrumbs, modal deletes, improved UX ([`5c92e73`])
- add scroll-to-top, loading overlay, breadcrumb support, polished login page ([`d3f0847`])
- improve toast stacking, page transitions, loading overlay, form helpers ([`23e71bb`])
- overhaul design system with animations, skeletons, dark mode prep, responsive polish ([`e5ab6e3`])
- update README with new architecture and receptionist toolkit features ([`e970d1d`])
- professionalize codebase with automated formatting and linting ([`366b1c9`])
- professionalize DB and API layers ([`3da4b8e`])
- untrack .coverage and .env (now gitignored) ([`cbff4e3`])
- stage all unstaged working-tree changes from 13-commit backlog ([`14d7246`])
- add full-stack production showcase document ([`5fe06b9`])
- add flake8 configuration file ([`de14bf1`])
- Update crispy-bootstrap5 to available version 2026.3 ([`c1b9a33`])
- Update crispy-bootstrap5 to available version 2026.3 ([`c6ec016`])
- Revise email reporting instructions in SECURITY.md ([`6524a53`])
- rewrite README with architecture diagram, badges, and API documentation ([`e706352`])
- finalize app configuration and management commands ([`b62e336`])
- add comprehensive test suite across all apps (93 tests) ([`d8f4417`])
- improve templates and styling across all apps ([`0119e16`])
- add select_related and pagination to prevent N+1 queries ([`3242505`])
- unify phone validation and fix model constraints ([`61bce23`])
- Add GitHub Actions Python CI/CD workflow ([`cd605fc`])
- Add MIT License ([`4bdcee6`])
- Update completion date to November 18, 2025 ([`c7fac6b`])
- Update last updated date to November 18, 2025 ([`8abf19e`])
- Update CHECKLIST.md ([`0ed1bb7`])
- Delete CHAT_SESSION_SUMMARY.md ([`6e14d6f`])
- Delete .vscode directory ([`85ef679`])
- Delete .qoder directory ([`a57b716`])
- Clean up repository: Remove Python cache files, add API views and serializers, update documentation, and exclude database file from tracking ([`615c4cd`])
- enhanc repo ([`69a5486`])
- **patients, appointments**: Improve code quality and test coverage ([`d907a89`])
- f1_work ([`9174355`])
- up-commit ([`e486e25`])
- Initial commit of project files ([`fbeb48c`])

### Fixed
- resolve XML parsing errors by explicitly writing SVGs with UTF-8 encoding and XML headers ([`0902923`])
- CI/CD â€” align Python versions, split dev deps, fix gitignore, drop python-ci.yml ([`9f9b993`])
- media serving, 404/500 pages, README stats, audit log, vital trends redirect, +9 tests (113 total, 75% coverage) ([`112a6a3`])
- dashboard â€” add admitted_patients stat, fix progress bar normalization, fix now context, fix status badge, replace dark admin card with light ([`1cadeda`])
- modernize all list/delete templates, fix validators, fix migration deprecations, fix ordering warnings, fix enum naming ([`04c8297`])
- create all missing templates, rebuild old-style detail pages, add hospital templates ([`476efa4`])
- resolve all broken URL names â€” remove app_name from urls.py files, register all CRUD routes globally ([`36f95ed`])
- register all missing list URLs, add InventoryItemDetailView, fix integration views, fix surgery select_related bug ([`d488831`])
- add missing timezone import to billing/models.py ([`2ceec0a`])
- add missing timezone import to patients/models.py ([`a66a328`])
- update crispy-bootstrap5 to compatible existing version 2025.6 ([`8a70b02`])
- update crispy-bootstrap5 to compatible existing version 2025.6 ([`0c0bd95`])
- resolve django-crispy-forms and crispy-bootstrap5 dependency conflict in requirements.txt ([`79109d5`])
- resolve django-crispy-forms and crispy-bootstrap5 dependency conflict ([`08dce19`])
- resolve settings security issues and rate limiting ([`1ed5b98`])


## [1.1.0] - 2026-05-01

### Added
- REST API for `hospital` app: `WardViewSet`, `RoomViewSet` — endpoints `/api/v1/wards/`, `/api/v1/rooms/`
- REST API for `inventory` app: `InventoryItemViewSet` — endpoint `/api/v1/inventory/` with `/low_stock/` action
- REST API for `surgery` app: `SurgeryViewSet` — endpoint `/api/v1/surgeries/` with `/scheduled/` action
- REST API for `care_monitoring` app: `PatientCareViewSet` — endpoint `/api/v1/care-monitoring/` with `/critical/` action
- Serializers for all four new API apps (`hospital`, `inventory`, `surgery`, `care_monitoring`)
- `report_list` URL (`/reports/`) was missing from `reporting/urls.py` — added
- 7 tests for `reporting` app covering model CRUD, `__str__`, ordering, auth enforcement, and file download

### Changed
- `REDIS_ENABLED` now defaults to `False` in `settings.py` — dev installs no longer require a running Redis instance
- `django-redis==5.4.0` and `redis==5.0.1` moved to base `requirements.txt` (were only in `requirements-prod.txt`)
- Deduplicated `django-redis` and `redis` entries in `requirements.txt`
- Registered 5 new ViewSets in `remedium_hms/urls.py`

### Removed
- `.qwen/` AI tool artifact directory deleted and added to `.gitignore`
- `appointments/models_fixed.py` leftover patch file deleted and added to `.gitignore`

### Fixed
- `db.sqlite3` confirmed not git-tracked (already in `.gitignore`)
- Indentation inconsistency in `remedium_hms/urls.py` (`path("api/v1/", ...)` was misaligned)

---

## [1.0.0] - 2026-04-08

### Added
- 14 Django apps: `core`, `patients`, `staff`, `appointments`, `billing`, `pharmacy`, `laboratory`, `surgery`, `care_monitoring`, `medical_records`, `notifications`, `integration`, `inventory`, `hospital`, `reporting`
- REST API with DRF across 7 apps, JWT authentication via `djangorestframework-simplejwt`
- Role-based permissions: Admin, Doctor, Nurse, Receptionist, Pharmacist, Lab Technician
- OpenFDA drug label and adverse event integration with 24-hour caching
- Audit trails on all clinical models via `django-simple-history`
- Auto-numbered invoices (`INV-YYYY-NNNNN`) with race-condition-safe generation
- Appointment conflict detection with 30-minute slot overlap logic
- Vital signs tracking with BMI calculation and critical condition alerts
- 93 automated tests, 75% coverage
- OpenAPI 3.0 documentation via `drf-spectacular` (Swagger UI + ReDoc)
- Docker support with non-root user and health checks
- GitHub Actions CI/CD: flake8, bandit, pytest, Docker build verification
- Rate limiting: 100 req/hr anonymous, 1000 req/hr authenticated
- Fernet encryption for external API keys
- File upload support for medical records (PDF, images, 10MB limit)
- `seed_demo` management command for realistic demo data
