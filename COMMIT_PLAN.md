# 6-Day Commit Plan — Remedium HMS

> Execute **2 commits per day** for 6 consecutive days. Push on Day 6.
> This turns all accumulated changes into 12 professional commits that maximize your GitHub contribution graph.

---

## Day 1

### Commit 1 — Settings Security

```bash
git add remedium_hms/settings.py remedium_hms/settings_production.py .env.example requirements.txt requirements-prod.txt

git commit -m "fix: resolve settings security issues and rate limiting

- Fix DEBUG environment variable override bug preventing proper production security
- Add HSTS headers and SECURE_PROXY_SSL_HEADER for production deployments
- Configure API rate limiting (100/hr anon, 1000/hr authenticated)
- Add throttle classes for token auth brute-force prevention
- Add drf-spectacular and requests to requirements
- Remove deprecated Django settings (USE_L10N, DEFAULT_X_FRAME_OPTIONS)
- Environment-driven ALLOWED_HOSTS and database credentials"
```

### Commit 2 — Docker & CI/CD

```bash
git add Dockerfile docker-compose.yml .gitignore .github/

git commit -m "feat: add Docker health checks and CI/CD pipeline

- Run container as non-root user (appuser) for security
- Add health checks for both web and db services
- Environment-driven database credentials and DEBUG flag
- Add restart: unless-stopped for production resilience
- Configure gunicorn workers via environment variable
- Add GitHub Actions CI/CD with flake8, bandit, pytest, docker build
- Update .gitignore for logs, env files, and IDE artifacts"
```

---

## Day 2

### Commit 3 — Model Validation

```bash
git add patients/models.py staff/models.py appointments/models.py inventory/models.py

git commit -m "refactor: unify phone validation and fix model constraints

- Standardize phone regex to ^\+?\d{9,15}$ across Patient and Staff models
- Remove full_clean() from all model save() methods - validation at form/serializer layer
- Fix appointment overlap detection with proper range comparison logic
- Fix CheckConstraint deprecation: check= to condition= in inventory and patients
- Add 10MB file size validation to PatientDocument model"
```

### Commit 4 — API Permissions

```bash
git add core/permissions.py patients/serializers.py staff/serializers.py patients/api_views.py staff/views.py appointments/api_views.py

git commit -m "feat: add role-based API permissions and fix serializers

- Create IsClinicalStaff, IsBillingStaff, IsAdminOrDoctor, IsOwnerOrReadOnly permissions
- Add PatientBriefSerializer (non-clinical) and PatientFullSerializer (clinical staff)
- Fix ReadOnlyField source redundancy in Patient and Staff serializers
- Add order_by whitelist validation to prevent SQL injection
- Restrict PatientViewSet to IsClinicalStaff for data protection
- Add secrets.token_urlsafe(12) for staff password reset"
```

---

## Day 3

### Commit 5 — Billing

```bash
git add billing/models.py billing/api_views.py billing/views.py billing/admin.py billing/templates/billing/invoice_detail.html billing/models_payment.py

git commit -m "feat: add invoice auto-numbering and payment tracking

- Auto-generate invoice numbers in INV-YYYY-NNNNN format
- Add Payment model with post_save signal to update invoice paid status
- Add IsBillingStaff permission for billing API endpoints
- mark_paid endpoint creates Payment record instead of modifying invoice directly
- Add select_related and order_by whitelist to InvoiceListView
- Add HistoricalRecords for audit trail on invoices and payments"
```

### Commit 6 — Performance

```bash
git add appointments/views.py patients/views.py care_monitoring/views.py laboratory/views.py surgery/views.py

git commit -m "perf: add select_related and pagination to prevent N+1 queries

- Add select_related for FK fields in all ListViews
- Add order_by whitelist validation to prevent arbitrary column sorting
- Add explicit form classes instead of fields='__all__' in care_monitoring
- Add template_name to all class-based views
- Add paginate_by=10 to AppointmentListView and PatientListView"
```

---

## Day 4

### Commit 7 — New APIs & Apps

```bash
git add laboratory/api_views.py laboratory/serializers.py laboratory/models.py pharmacy/models.py pharmacy/api_views.py pharmacy/serializers.py integration/api_views.py integration/models.py integration/serializers.py medical_records/ notifications/

git commit -m "feat: add new API endpoints and audit trails

- Add LabTestViewSet and PrescriptionViewSet with search and ordering
- Add HistoricalRecords to LabTest, Prescription, Surgery for audit trails
- Add ExternalIntegrationViewSet with IsAdminUser permission
- Encrypt API keys with Fernet in ExternalIntegration model
- Add medical_records app with PatientDocument model (GenericForeignKey)
- Add notifications app with SMS/Email support and mark_sent/mark_failed
- Fix care_monitoring admin list_display fields"
```

### Commit 8 — OpenFDA Integration

```bash
git add pharmacy/openfda_service.py pharmacy/templates/pharmacy/prescription_form.html

git commit -m "feat: integrate OpenFDA drug lookup with UI panel

- Add search_drug_label() to fetch FDA drug info (generic/brand names, warnings, dosage, interactions)
- Add search_adverse_events() for top reported side effects
- Cache results for 24 hours to reduce API calls
- Add drug-info and adverse-events API endpoints to PrescriptionViewSet
- Build live search UI with accordion sections in prescription form
- Auto-lookup when drug name field changes (1s debounce)
- Display adverse event reports with count badges"
```

---

## Day 5

### Commit 9 — API Documentation

```bash
git add remedium_hms/urls.py

git commit -m "feat: add API documentation with drf-spectacular

- Add /api/v1/schema/ for OpenAPI 3.0 JSON schema
- Add /api/v1/docs/ for interactive Swagger UI (no auth required)
- Add /api/v1/redoc/ for ReDoc documentation
- Version API endpoints under /api/v1/ for future compatibility
- Configure SPECTACULAR_SETTINGS with title, description, auth guide
- Fix serializer type hints: replace ReadOnlyField with CharField/IntegerField/BooleanField
- Remove SerializerMethodField where model properties suffice"
```

### Commit 10 — UI & Templates

```bash
git add templates/base.html templates/index.html templates/registration/login.html templates/registration/logged_out.html static/css/custom.css patients/templates/ staff/templates/ appointments/templates/ care_monitoring/templates/ integration/templates/

git commit -m "ui: improve templates and styling across all apps

- Update base template with Bootstrap 5.3 and Bootstrap Icons
- Add role-based navigation menus (admin, doctor, nurse, receptionist)
- Improve login/logout pages with centered cards and icons
- Add patient history view template
- Add shift management templates for staff scheduling
- Add vital trends chart template for care monitoring
- Update custom CSS with modern card styles and transitions
- Add user management templates for staff administration"
```

---

## Day 6

### Commit 11 — Test Suite

```bash
git add core/tests.py surgery/tests.py care_monitoring/tests.py medical_records/tests.py notifications/tests.py pharmacy/tests.py hospital/tests.py billing/tests.py appointments/tests.py patients/tests.py staff/tests.py integration/tests.py integration/tests_features.py laboratory/tests.py conftest.py pytest.ini

git commit -m "test: add comprehensive test suite across all apps (93 tests)

- Add surgery tests: creation, status, unique room scheduling
- Add care_monitoring tests: vital signs, BP validation, BMI calculation
- Add medical_records tests: document creation, file extension validation
- Add notifications tests: mark_sent/failed, patient relations, ordering
- Add OpenFDA service tests: drug lookup, adverse events, error handling
- Add API integration tests: permissions, drug-info, adverse-events endpoints
- Add API documentation tests: schema, Swagger UI, ReDoc accessibility
- Add project-wide conftest.py with shared api_client fixture
- Configure pytest with coverage reporting"
```

### Commit 12 — Final Configuration

```bash
git add core/management/commands/create_groups.py core/urls.py core/views.py core/context_processors.py core/apps.py surgery/admin.py surgery/urls.py staff/forms.py staff/admin.py patients/urls.py appointments/urls.py billing/urls.py laboratory/urls.py hospital/urls.py integration/urls.py inventory/urls.py reporting/urls.py care_monitoring/urls.py pharmacy/urls.py staff/urls.py core/templates/

git commit -m "chore: finalize app configuration and management commands

- Update create_groups with billing and medical_records permissions
- Add Health check endpoint (/health/) with DB connectivity test
- Add app_name namespace to all 14 app url configs
- Register LabTest/Prescription ViewSets in API router
- Add context processors for role-based template variables
- Register Surgery model in admin
- Fix staff form validation and admin list_display
- Remove deprecated setup_roles management command"
```

### Push Everything

```bash
git push origin main
```

---

## After Push — Profile Setup

1. Go to your GitHub profile
2. Click **"Customize your pins"**
3. Pin `Remedium-HMS` repository
4. Add topics under repo **About** section:
   ```
   django, python, hospital-management, drf, rest-api, healthcare, 
   bootstrap, pytest, openapi, docker, healthcare-it
   ```

---

## Expected Result

```
12 commits across 6 days
6 green squares on contribution graph
93 tests passing
Production-ready hospital management system
Professional git log for recruiters
```

## Commit Message Pattern

| Prefix | Meaning | Examples Used |
|--------|---------|---------------|
| `fix:` | Bug fix or security issue | settings, model constraints |
| `feat:` | New feature | Docker CI/CD, OpenFDA, API docs, permissions, billing |
| `refactor:` | Code restructuring | phone validation |
| `perf:` | Performance improvement | N+1 query fixes |
| `ui:` | Frontend/template changes | Bootstrap, styling |
| `test:` | Test additions | 93 tests across all apps |
| `chore:` | Config, tooling, maintenance | management commands, URLs, admin |
