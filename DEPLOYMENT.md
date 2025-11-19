# Deployment Guide - Remedium HMS

This guide covers deployment options for Remedium Hospital Management System.

## Local Development Setup

### Prerequisites
- Python 3.13+
- Git
- Virtual environment

### Quick Start

1. Clone the repository:
```bash
git clone https://github.com/neoastra303/Remedium-HMS.git
cd Remedium-HMS
```

2. Create and activate virtual environment:
```bash
python -m venv venv
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` file from `.env.example`:
```bash
cp .env.example .env
```

5. Edit `.env` with your settings:
```env
SECRET_KEY=your-secure-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

6. Run migrations:
```bash
python manage.py migrate
```

7. Create user groups:
```bash
python manage.py create_groups
```

8. Create superuser:
```bash
python manage.py createsuperuser
```

9. Run development server:
```bash
python manage.py runserver
```

Access the application at `http://localhost:8000`

---

## Docker Deployment

### Prerequisites
- Docker
- Docker Compose

### Quick Deploy with Docker

1. Prepare environment:
```bash
cp .env.example .env
```

2. Edit `.env` with production values:
```env
DEBUG=False
SECRET_KEY=your-very-secure-secret-key
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DB_ENGINE=django.db.backends.postgresql
```

3. Build and start containers:
```bash
docker-compose up -d
```

4. Run migrations:
```bash
docker-compose exec web python manage.py migrate
```

5. Create superuser:
```bash
docker-compose exec web python manage.py createsuperuser
```

6. Access the application at `http://localhost:8000`

### Stopping Containers
```bash
docker-compose down
```

---

## Production Deployment (Heroku)

### Prerequisites
- Heroku CLI
- Heroku account

### Steps

1. Initialize Heroku app:
```bash
heroku login
heroku create your-app-name
```

2. Set environment variables:
```bash
heroku config:set SECRET_KEY=your-secure-secret-key
heroku config:set DEBUG=False
heroku config:set ALLOWED_HOSTS=your-app-name.herokuapp.com
```

3. Add PostgreSQL addon:
```bash
heroku addons:create heroku-postgresql:hobby-dev
```

4. Deploy:
```bash
git push heroku main
```

5. Run migrations:
```bash
heroku run python manage.py migrate
heroku run python manage.py create_groups
heroku run python manage.py createsuperuser
```

6. Collect static files:
```bash
heroku run python manage.py collectstatic --noinput
```

### View Logs
```bash
heroku logs --tail
```

---

## Production Deployment (DigitalOcean App Platform)

### Prerequisites
- DigitalOcean account
- GitHub repository

### Steps

1. Connect GitHub repository to DigitalOcean
2. Create new App from GitHub
3. Configure environment variables:
   - `DEBUG=False`
   - `SECRET_KEY=your-secret-key`
   - `ALLOWED_HOSTS=your-domain.com`
   - `DB_ENGINE=django.db.backends.postgresql`

4. Add PostgreSQL database service
5. Deploy

---

## Production Deployment (AWS EC2)

### Prerequisites
- AWS account
- EC2 instance (Ubuntu 22.04)
- Domain name

### Setup Steps

1. SSH into instance:
```bash
ssh -i your-key.pem ubuntu@your-instance-ip
```

2. Update system:
```bash
sudo apt update && sudo apt upgrade -y
```

3. Install dependencies:
```bash
sudo apt install -y python3-pip python3-venv postgresql postgresql-contrib nginx git
```

4. Clone repository:
```bash
cd /home/ubuntu
git clone https://github.com/neoastra303/Remedium-HMS.git
cd Remedium-HMS
```

5. Create virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

6. Install Python packages:
```bash
pip install -r requirements-prod.txt
```

7. Configure PostgreSQL:
```bash
sudo -u postgres psql
CREATE DATABASE remedium_hms;
CREATE USER remedium_user WITH PASSWORD 'secure_password';
ALTER ROLE remedium_user SET client_encoding TO 'utf8';
GRANT ALL PRIVILEGES ON DATABASE remedium_hms TO remedium_user;
\q
```

8. Create `.env` file:
```bash
cat > .env << EOF
DEBUG=False
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DB_ENGINE=django.db.backends.postgresql
DB_NAME=remedium_hms
DB_USER=remedium_user
DB_PASSWORD=secure_password
DB_HOST=localhost
DB_PORT=5432
EOF
```

9. Run migrations:
```bash
python manage.py migrate
python manage.py create_groups
```

10. Collect static files:
```bash
python manage.py collectstatic --noinput
```

11. Configure Nginx:
```bash
sudo cp nginx.conf /etc/nginx/sites-available/remedium
sudo ln -s /etc/nginx/sites-available/remedium /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

12. Set up Gunicorn with Systemd:
```bash
sudo cat > /etc/systemd/system/remedium.service << EOF
[Unit]
Description=Remedium HMS Application
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/Remedium-HMS
ExecStart=/home/ubuntu/Remedium-HMS/venv/bin/gunicorn remedium_hms.wsgi:application --bind 127.0.0.1:8000
Restart=always

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable remedium
sudo systemctl start remedium
```

13. Set up SSL with Certbot:
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

---

## Backup & Restore

### PostgreSQL Backup
```bash
pg_dump remedium_hms > backup_$(date +%Y%m%d_%H%M%S).sql
```

### PostgreSQL Restore
```bash
psql remedium_hms < backup_YYYYMMDD_HHMMSS.sql
```

### Docker Backup
```bash
docker-compose exec postgres pg_dump -U postgres remedium_hms > backup.sql
```

---

## Health Checks

Monitor application health:

```bash
# Application status
curl http://localhost:8000/

# API health
curl http://localhost:8000/api/

# Admin panel
http://localhost:8000/admin/
```

---

## Performance Optimization

1. Enable caching in production `.env`:
```env
CACHES='{"default":{"BACKEND":"django.core.cache.backends.locmem.LocMemCache"}}'
```

2. Use CDN for static files (CloudFront, Cloudflare)

3. Enable gzip compression in Nginx:
```nginx
gzip on;
gzip_types text/plain text/css text/javascript application/json;
gzip_min_length 1000;
```

4. Set appropriate database pool size
5. Enable database query optimization
6. Monitor application with New Relic or DataDog

---

## Troubleshooting

### 502 Bad Gateway
- Check Gunicorn is running: `systemctl status remedium`
- Check logs: `sudo tail -f /var/log/nginx/error.log`

### Static Files Not Loading
- Run `python manage.py collectstatic --noinput`
- Check Nginx static file path configuration

### Database Connection Issues
- Verify DATABASE_URL environment variable
- Check PostgreSQL service is running
- Verify database credentials

### Permission Denied Errors
- Ensure proper file permissions: `chown -R www-data:www-data /app`
- Check systemd service user permissions

---

## Security Checklist

- [ ] Set `DEBUG=False` in production
- [ ] Use strong `SECRET_KEY` (generate with: `python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'`)
- [ ] Enable HTTPS/SSL certificates
- [ ] Configure ALLOWED_HOSTS properly
- [ ] Use strong database password
- [ ] Enable SECURE_SSL_REDIRECT
- [ ] Set SESSION_COOKIE_SECURE=True
- [ ] Set CSRF_COOKIE_SECURE=True
- [ ] Configure firewall rules
- [ ] Regular backups configured
- [ ] Monitor application logs
- [ ] Keep dependencies updated

---

## Support

For issues or questions, please refer to the README.md or open an issue on GitHub.
