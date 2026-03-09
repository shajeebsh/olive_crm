# OliveCRM

Modern, affordable CRM application targeting small to mid-sized companies (SMBs). Built with Django 5.0 and Wagtail 6.0.

## Tech Stack
- **Backend**: Django 5.0+
- **CMS**: Wagtail 6.0+
- **Frontend**: Bootstrap 5, HTMX
- **Database**: MySQL (Production), SQLite (Local Dev fallback)
- **Other**: Redis, Celery, OpenAI Integration

## Features

### Phase 1: Core Foundation
- Modular CRM Architecture (`contacts`, `sales`, `reporting`)
- Contact & Company Management
- Deal Pipeline & Stage Tracking
- Custom Dashboards with flexible widgets
- Premium UI with custom OliveCRM theme

### Phase 2: Growth & Automation
- **Wagtail-Powered Marketing**: Build Landing Pages and Email Campaigns within the CMS.
- **Communication Sync**: IMAP Email synchronization and WhatsApp tracking.
- **Automation**: No-code workflow engine for record-based triggers and actions.
- **AI Intelligence**: Built-in lead scoring and email composition via OpenAI.

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

# Phase 2: AI Integration
OPENAI_API_KEY=your-openai-api-key
```

### 4. Database Setup
```bash
python manage.py migrate
python manage.py createsuperuser
```

### 5. Running Email Sync
To sync external emails into the CRM as interactions:
```bash
python manage.py sync_email
```

### 6. Run the Server
```bash
python manage.py runserver
```
Access the application at `http://localhost:8000/`.

## Documentation
Walkthroughs and detailed task lists are available in the [artifacts directory](file:///Users/shajeebs/.gemini/antigravity/brain/acb0b3f9-f1f9-4a55-b1a3-df3d29ef3dea/).
- [Phase 1 & 2 Walkthrough](file:///Users/shajeebs/.gemini/antigravity/brain/acb0b3f9-f1f9-4a55-b1a3-df3d29ef3dea/walkthrough.md)
