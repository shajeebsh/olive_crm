# Setup and Installation

This guide provides step-by-step instructions for setting up the OliveCRM development environment.

## 1. Prerequisites

- Python 3.11+
- Virtualenv
- MySQL (optional, for production parity)
- Redis (for Celery and caching)

## 2. Installation

```bash
# Clone the repository
git clone <repo-url>
cd olive_crm

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## 3. Environment Configuration

Create a `.env` file in the project root:

```env
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///db.sqlite3
ALLOWED_HOSTS=localhost,127.0.0.1

# Phase 2: AI Integration
OPENAI_API_KEY=your-openai-api-key
```

## 4. Database Setup

```bash
# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

## 5. Running the Server

```bash
# Start development server
python manage.py runserver
```

Access the application at `http://localhost:8000/`.

## 6. Running Email Sync

To sync external emails into the CRM as interactions:

```bash
python manage.py sync_email
```

## 7. Celery and Background Tasks

If you're using features that require background tasks (AI scoring, email sync):

```bash
# Ensure Redis is running
redis-server

# Start Celery worker
celery -A olivecrm worker -l info
```
