# Quick Start Guide - Remedium HMS

Get Remedium Hospital Management System running in 5 minutes.

## Windows Quick Start

```cmd
# 1. Clone and navigate
git clone https://github.com/neoastra303/Remedium-HMS.git
cd Remedium-HMS

# 2. Create virtual environment and activate
python -m venv venv
venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Setup configuration
copy .env.example .env

# 5. Initialize database
python manage.py migrate
python manage.py create_groups

# 6. Create admin user
python manage.py createsuperuser

# 7. Run server
python manage.py runserver
```

Open: http://localhost:8000

---

## macOS/Linux Quick Start

```bash
# 1. Clone and navigate
git clone https://github.com/neoastra303/Remedium-HMS.git
cd Remedium-HMS

# 2. Create virtual environment and activate
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Setup configuration
cp .env.example .env

# 5. Initialize database
python manage.py migrate
python manage.py create_groups

# 6. Create admin user
python manage.py createsuperuser

# 7. Run server
python manage.py runserver
```

Open: http://localhost:8000

---

## Docker Quick Start

```bash
# 1. Clone
git clone https://github.com/neoastra303/Remedium-HMS.git
cd Remedium-HMS

# 2. Start containers
docker-compose up -d

# 3. Create admin user
docker-compose exec web python manage.py createsuperuser

# 4. Access application
```

Open: http://localhost:8000

---

## First Steps After Installation

1. **Login to Admin**: http://localhost:8000/admin
   - Username and password: created during setup

2. **Add Sample Data**:
   - Patients: Admin → Patients → Add Patient
   - Staff: Admin → Staff → Add Staff
   - Appointments: Admin → Appointments → Add Appointment

3. **Access API**: http://localhost:8000/api/
   - View available endpoints
   - Test endpoints using browsable API

4. **Review Documentation**:
   - Full Setup: [SETUP.md](SETUP.md)
   - API Docs: [API.md](API.md)
   - Deployment: [DEPLOYMENT.md](DEPLOYMENT.md)

---

## Key Features Ready to Use

✅ **Patient Management** - Create, view, update, discharge patients  
✅ **Staff Management** - Manage doctors, nurses, technicians  
✅ **Appointments** - Schedule and track appointments  
✅ **Billing** - Create and manage invoices  
✅ **REST API** - Full JSON API for all major functions  
✅ **Admin Panel** - Comprehensive admin interface  
✅ **User Groups** - Pre-configured roles (Doctor, Nurse, Admin, etc.)  

---

## Common Commands

```bash
# View all available API endpoints
python manage.py showurls

# Create new app
python manage.py startapp app_name

# Make database changes
python manage.py makemigrations
python manage.py migrate

# Run tests
python manage.py test

# Collect static files (production)
python manage.py collectstatic --noinput

# Check for issues
python manage.py check

# Run management commands
python manage.py create_groups
python manage.py createsuperuser
```

---

## API Examples

### Get all patients
```bash
curl -X GET "http://localhost:8000/api/patients/" \
  -H "Authorization: Bearer your-token"
```

### Create patient
```bash
curl -X POST "http://localhost:8000/api/patients/" \
  -H "Content-Type: application/json" \
  -d '{
    "unique_id": "PAT001",
    "first_name": "John",
    "last_name": "Doe",
    "date_of_birth": "1990-05-15",
    "gender": "M"
  }'
```

### Get admitted patients
```bash
curl -X GET "http://localhost:8000/api/patients/admitted_patients/"
```

### Schedule appointment
```bash
curl -X POST "http://localhost:8000/api/appointments/" \
  -H "Content-Type: application/json" \
  -d '{
    "patient": 1,
    "doctor": 1,
    "appointment_date": "2024-02-20T14:00:00Z",
    "reason": "Checkup"
  }'
```

---

## Stopping the Application

**Development Server:**
```
Press CTRL+C in terminal
```

**Docker Containers:**
```bash
docker-compose down
```

---

## Need Help?

- **Installation Issues**: See [SETUP.md](SETUP.md)
- **API Questions**: See [API.md](API.md)
- **Deployment**: See [DEPLOYMENT.md](DEPLOYMENT.md)
- **Issues Found**: See [ISSUES_FIXED.md](ISSUES_FIXED.md)

---

## Default Credentials

After setup, use the credentials you created during `createsuperuser`.

Example:
- Username: `admin`
- Password: `(what you entered)`

---

## Next: Production Deployment

When ready to deploy to production:
1. Read [DEPLOYMENT.md](DEPLOYMENT.md)
2. Set up `.env` with production values
3. Use Docker or follow platform-specific instructions
4. Enable HTTPS/SSL
5. Use PostgreSQL database
6. Set up backups

---

## Support

- GitHub: https://github.com/neoastra303/Remedium-HMS
- Issues: https://github.com/neoastra303/Remedium-HMS/issues
- Contributing: [CONTRIBUTING.md](CONTRIBUTING.md)

---

**Ready to get started? Follow the Quick Start section above for your OS.**
