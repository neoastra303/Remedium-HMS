# Remedium HMS - Complete Setup Guide

Welcome to Remedium Hospital Management System. This guide will walk you through the complete setup process.

## System Requirements

- **Python**: 3.13 or higher
- **Operating System**: Windows, macOS, or Linux
- **RAM**: Minimum 2GB (4GB recommended)
- **Disk Space**: Minimum 2GB
- **Database**: SQLite (development) or PostgreSQL (production)

## Prerequisites

### Windows
1. Download and install Python 3.13+ from [python.org](https://www.python.org/)
   - **Important**: Check "Add Python to PATH" during installation
2. Download and install Git from [git-scm.com](https://git-scm.com/)
3. Open Command Prompt and verify:
   ```
   python --version
   git --version
   ```

### macOS
1. Install Homebrew (if not already installed):
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

2. Install Python:
   ```bash
   brew install python@3.13
   ```

3. Install Git:
   ```bash
   brew install git
   ```

### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install python3.13 python3-pip python3-venv git
```

## Step-by-Step Installation

### 1. Clone the Repository

**Windows:**
```cmd
git clone https://github.com/neoastra303/Remedium-HMS.git
cd Remedium-HMS
```

**macOS/Linux:**
```bash
git clone https://github.com/neoastra303/Remedium-HMS.git
cd Remedium-HMS
```

### 2. Create Virtual Environment

**Windows:**
```cmd
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` prefix in your terminal prompt after activation.

### 3. Upgrade pip (Recommended)

**Windows:**
```cmd
python -m pip install --upgrade pip
```

**macOS/Linux:**
```bash
python3 -m pip install --upgrade pip
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables

1. Copy the example environment file:
   ```bash
   copy .env.example .env  # Windows
   cp .env.example .env    # macOS/Linux
   ```

2. Open `.env` file and configure:
   ```env
   SECRET_KEY=generate-a-secure-key-see-below
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   ```

3. Generate a secure SECRET_KEY:
   ```bash
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```
   Copy the output and paste it in the `SECRET_KEY` field.

### 6. Initialize Database

Run migrations:
```bash
python manage.py migrate
```

Create user groups and permissions:
```bash
python manage.py create_groups
```

You should see output like:
```
Creating default user groups...
Group 'Admin' created.
Group 'Doctor' created.
Group 'Nurse' created.
Group 'Receptionist' created.
Group 'Pharmacist' created.
Group 'Lab Technician' created.
Default user groups and permissions setup complete.
```

### 7. Create Superuser (Admin Account)

```bash
python manage.py createsuperuser
```

Follow the prompts:
```
Username: admin
Email: admin@hospital.com
Password: ••••••••
Password (again): ••••••••
Superuser created successfully.
```

### 8. Create Logs Directory

**Windows:**
```cmd
mkdir logs
```

**macOS/Linux:**
```bash
mkdir logs
```

### 9. Run Development Server

```bash
python manage.py runserver
```

You should see:
```
Django version 5.2.7
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

### 10. Access the Application

Open your browser and navigate to:
- **Web Application**: http://localhost:8000
- **Admin Panel**: http://localhost:8000/admin
- **API**: http://localhost:8000/api

Login with the superuser credentials you created in step 7.

---

## Post-Installation Setup

### 1. Add Sample Data

You can add sample data through the admin panel:

1. Go to http://localhost:8000/admin
2. Login with superuser credentials
3. Click on "Patients" and add sample patient records
4. Click on "Staff" and add sample staff members
5. Create appointments by linking patients with doctors

### 2. Assign User Groups

To assign roles to users:

1. Go to Admin Panel
2. Select "Users"
3. Edit a user
4. In "Groups" section, add them to appropriate group (Doctor, Nurse, etc.)
5. Save

### 3. Configure Email (Optional)

Edit `.env` file:
```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=your-email@gmail.com
```

For Gmail, you need to:
1. Enable 2-Factor Authentication
2. Generate App Password
3. Use the App Password (not your regular password)

---

## Common Issues & Troubleshooting

### Issue: "Python not found" or "python is not recognized"

**Solution:**
- Ensure Python is installed and added to PATH
- Try `python3` instead of `python`
- Restart terminal/command prompt after installing Python

### Issue: Virtual environment won't activate

**Solution:**
- Windows: Try `python -m venv venv` to create fresh environment
- macOS/Linux: Make sure the path is correct: `source venv/bin/activate`

### Issue: "No module named 'django'"

**Solution:**
- Ensure virtual environment is activated (check for `(venv)` prefix)
- Run: `pip install -r requirements.txt`

### Issue: "No such table: auth_user"

**Solution:**
- Run: `python manage.py migrate`
- Database migrations haven't been applied

### Issue: Port 8000 already in use

**Solution:**
- Use a different port: `python manage.py runserver 8001`
- Or kill the process using the port

### Issue: Static files not loading (404 errors)

**Solution:**
- Run: `python manage.py collectstatic --noinput`
- Check `DEBUG=True` in `.env` for development

### Issue: Permission denied when accessing database

**Solution:**
- On Windows: Run Command Prompt as Administrator
- Ensure `logs/` directory exists and is writable
- Check file permissions on `db.sqlite3`

---

## Development Workflow

### Daily Startup

```bash
# Activate virtual environment
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

# Run development server
python manage.py runserver
```

### Making Database Changes

1. Modify models in `app_name/models.py`
2. Create migrations: `python manage.py makemigrations`
3. Review migrations: `python manage.py showmigrations`
4. Apply migrations: `python manage.py migrate`

### Running Tests

```bash
python manage.py test
```

### Creating Management Commands

Place scripts in `app_name/management/commands/script_name.py`

Example:
```python
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Description of what the command does'
    
    def add_arguments(self, parser):
        parser.add_argument('arg_name', type=str)
    
    def handle(self, *args, **options):
        self.stdout.write("Processing...")
```

Run with: `python manage.py script_name arg_value`

---

## Project Structure

```
Remedium-HMS/
├── appointments/          # Appointment management app
├── billing/              # Billing and invoicing app
├── care_monitoring/      # Patient care monitoring
├── core/                 # Core application
├── hospital/             # Hospital ward and room management
├── integration/          # External system integration
├── inventory/            # Medical supply inventory
├── laboratory/           # Lab tests management
├── patients/             # Patient management
├── pharmacy/             # Pharmacy management
├── reporting/            # Reports generation
├── staff/                # Staff management
├── surgery/              # Surgery scheduling
├── templates/            # HTML templates
├── static/               # CSS, JavaScript, images
├── remedium_hms/         # Project settings
├── manage.py             # Django management script
├── requirements.txt      # Python dependencies
├── .env.example          # Environment variables template
└── README.md             # Project readme
```

---

## Database Information

### Default Database (SQLite)
- Location: `db.sqlite3` in project root
- No authentication needed for development
- Not suitable for production

### Switching to PostgreSQL

1. Install PostgreSQL
2. Create database and user:
   ```bash
   psql -U postgres
   CREATE DATABASE remedium_hms;
   CREATE USER remedium_user WITH PASSWORD 'secure_password';
   GRANT ALL PRIVILEGES ON DATABASE remedium_hms TO remedium_user;
   ```

3. Update `.env`:
   ```env
   DB_ENGINE=django.db.backends.postgresql
   DB_NAME=remedium_hms
   DB_USER=remedium_user
   DB_PASSWORD=secure_password
   DB_HOST=localhost
   DB_PORT=5432
   ```

4. Install PostgreSQL adapter: `pip install psycopg2-binary`
5. Run migrations: `python manage.py migrate`

---

## Next Steps

1. Read the [API Documentation](API.md) to understand API endpoints
2. Review [Deployment Guide](DEPLOYMENT.md) for production setup
3. Check [Contributing Guide](CONTRIBUTING.md) for development practices
4. Explore Admin Panel to understand the application structure

---

## Getting Help

- **Documentation**: See [README.md](README.md) for overview
- **API Help**: See [API.md](API.md) for API endpoint details
- **Deployment**: See [DEPLOYMENT.md](DEPLOYMENT.md) for production setup
- **GitHub Issues**: Report bugs or request features on GitHub
- **Email**: Contact the development team

---

## Security Checklist for Development

- ✅ Never commit `.env` file with real credentials
- ✅ Use strong SECRET_KEY (already randomized)
- ✅ Keep dependencies updated: `pip install --upgrade -r requirements.txt`
- ✅ Run security checks: `python manage.py check --deploy`
- ✅ Change default admin username and password
- ✅ Don't enable DEBUG in production

---

## Success!

You should now have Remedium HMS running on your local machine. Start exploring the application and get familiar with its features.

For detailed information about specific features or modules, refer to the documentation in each app directory.
