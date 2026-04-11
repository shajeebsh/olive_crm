# OliveCRM

Modern, affordable CRM application targeting small to mid-sized companies (SMBs). Built with **Django 5.0** and **Wagtail 6.0**.

---

## Quick Links

- [🚀 Setup & Installation](docs/setup.md)
- [🏗️ Architecture Overview](docs/architecture.md)
- [🧪 Testing & QA](docs/testing.md)
- [📡 REST API Documentation](docs/api.md)
- [📝 AI Context Documentation](docs/ai_context.md)

---

## Project Overview

**OliveCRM** provides an enterprise-grade Customer Relationship Management (CRM) system. It features a modular architecture designed for flexibility and scalability.

### Key Modules
- **Contacts**: Contact & Company Management
- **Sales**: Deal Pipeline & Stage Tracking
- **Invoicing**: Full billing cycle and payments
- **Inventory**: Stock tracking and multi-warehouse management
- **Marketing**: Wagtail-powered landing pages and email campaigns
- **Automation**: No-code workflow engine for business processes
- **AI Intelligence**: Lead scoring and email composition via OpenAI
- **Reporting**: Dashboards and analytics with HTMX

---

## Tech Stack

- **Backend**: Django 5.0+, Django Rest Framework
- **CMS**: Wagtail 6.0+
- **Frontend**: Bootstrap 5, HTMX, PWA Ready
- **Database**: MySQL (Production), SQLite (Dev)
- **Infrastructure**: Redis, Celery, OpenAI Integration

---

## Setup (Quick Start)

```bash
# Install dependencies
pip install -r requirements.txt

# Database setup
python manage.py migrate
python manage.py createsuperuser

# Run server
python manage.py runserver
```

For detailed instructions, see [docs/setup.md](docs/setup.md).

---

## License

Copyright © 2026 OliveCRM Team. All rights reserved.
