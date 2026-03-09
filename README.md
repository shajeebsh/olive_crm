# OliveCRM

Modern, affordable CRM application targeting small to mid-sized companies (SMBs). Built with Django 5.0 and Wagtail 6.0.

## Tech Stack
- **Backend**: Django 5.0+
- **CMS**: Wagtail 6.0+
- **Frontend**: Bootstrap 5, HTMX
- **Database**: MySQL (Production), SQLite (Local Dev fallback)
- **Other**: Redis, Celery, OpenAI Integration

## Features (Phase 1)
- Modular CRM Architecture (`contacts`, `sales`, `reporting`)
- Contact & Company Management
- Deal Pipeline & Stage Tracking
- AI-Ready Lead Scoring
- Custom Dashboards with flexible widgets
- Premium UI with custom OliveCRM theme

## Setup Instructions

### 1. Prerequisites
- Python 3.11+
- Virtualenv

### 2. Installation
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

### 3. Environment Configuration
Create a `.env` file in the project root:
```env
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///db.sqlite3
ALLOWED_HOSTS=localhost,127.0.0.1
```

### 4. Database Setup
```bash
python manage.py migrate
python manage.py createsuperuser
```

### 5. Run the Server
```bash
python manage.py runserver
```
Access the application at `http://localhost:8000/`.

## Documentation
Phase 1 walkthrough and detailed task lists are available in the [artifacts directory](file:///Users/shajeebs/.gemini/antigravity/brain/acb0b3f9-f1f9-4a55-b1a3-df3d29ef3dea/).
