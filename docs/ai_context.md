# OliveCRM - Project Context Documentation

> **Last Updated**: April 2026  
> **Maintained by**: Development Team

---

## 1. Project Overview

**OliveCRM** is an enterprise-grade Customer Relationship Management (CRM) system built on Django 5.0 and Wagtail CMS. It provides a comprehensive suite of tools for managing contacts, sales pipelines, invoicing, inventory, and business reporting.

### Technology Stack

| Layer | Technology | Version |
|-------|-----------|--------|
| Backend | Django | 5.0.14 |
| CMS | Wagtail | 6.x |
| Database | SQLite (dev) / MySQL (prod) |
| Frontend | Bootstrap 5, HTMX, Chart.js |
| Authentication | Django Auth |
| CSS Framework | Bootstrap 5.3 + Custom Theme |

### Additional Infrastructure

| Service | Purpose |
|---------|---------|
| Redis | Caching and Celery broker |
| Celery | Asynchronous tasks (email sync, AI scoring, workflow execution) |
| OpenAI API | AI lead scoring and email composition |
| Docker | Containerized development and production environments |

---

## 2. Project Structure

```
olive_crm/
├── manage.py                 # Django management script
├── requirements.txt        # Python dependencies
├── db.sqlite3          # Development database
├── venv/              # Virtual environment
│
├── docs/              # Documentation (ai_context.md, ai_task.md)
│
├── home/              # Wagtail home app (CMS pages)
├── search/            # Global search functionality
│
└── olivecrm/         # Main project
    ├── settings/      # Django settings
    ├── urls.py       # URL routing
    ├── wsgi.py      # WSGI config
    │
    ├── core/           # Core functionality (dashboard, profile, settings)
    ├── contacts/        # Contacts & Companies management
    ├── sales/         # Deals, Tasks, Pipeline
    ├── invoicing/     # Invoices & Payments
    ├── inventory/     # Stock & Products
    ├── reporting/     # Reports & Analytics
    ├── communication/  # Email/Chat integration
    ├── automation/    # Workflow automation
    ├── marketing/     # Marketing campaigns
    ├── operations    # Operations tracking
    ├── service      # Customer service
    ├── api          # REST API
    ├── crm_cms      # Wagtail CMS pages
    │
    ├── static/        # CSS, JS, Images
    │   └── css/
    │       ├── theme.css          # "Trusted Innovator" theme
    │       ├── olive-theme.css  # Legacy styling
    │       └── index.css        # Utility styles
    │
    └── templates/      # Django templates
        ├── base.html           # Two-row shell layout
        ├── core/             # Dashboard, profile
        ├── contacts/          # Contact/company views
        ├── sales/            # Deals, tasks, pipeline
        ├── reporting/       # Reports with partials
        └── ...
```

---

## 3. URL Routing

| Path | App | Purpose |
|------|-----|---------|
| `/` | core | Dashboard (`dashboard`) |
| `/accounts/` | django.contrib.auth | Login/logout |
| `/django-admin/` | admin | Django admin |
| `/admin/` | wagtail | Wagtail CMS |
| `/search/` | search | Global search |
| `/api/` | api | REST API endpoints |
| `/contacts/` | contacts | Contacts & Companies |
| `/sales/` | sales | Deals, Tasks, Pipeline |
| `/invoicing/` | invoicing | Invoices |
| `/reports/` | reporting | Reports (index, sales, revenue, contacts, performance) |
| `/pipeline/` | sales | Kanban pipeline view |
| `/communications/` | communication | Communications |
| `/automation/` | automation | Workflow automation |
| `/inventory/` | inventory | Inventory management |
| `/settings/` | core:settings | Settings pages |
| `/profile/` | core | User profile |

### Namespace Usage

- Use `reporting:index`, `reporting:sales`, etc. (namespace required)
- Use `sales:deal_list`, `sales:task_list`, etc.
- Use `contacts:contact_list`, `contacts:company_list`
- Use `core:index` for settings

---

## 4. Key Features

### 4.1 Dashboard
- KPI cards with vertical-accent styling
- Recent deals table
- Upcoming tasks
- Period filters (today, week, month, quarter, year)

### 4.2 Two-Row Shell Layout
- **Row 1** (56px): Utility bar - Brand, HTMX search, user menu
- **Row 2** (48px): Module navigation ribbon
- Mobile responsive with hamburger menu

### 4.3 Reporting Module
- HTMX-powered tab switching (Sales, Revenue, Contacts, Performance)
- CSV export with date filtering
- Direct URL access redirects to full index page
- Chart.js visualization

### 4.4 "Trusted Innovator" Theme

| Role | Color | Hex |
|------|-------|-----|
| Primary Action | Deep Teal | `#008080` |
| Navigation | Dark Indigo | `#003566` |
| Background | Cloud Dancer | `#F8F9FA` |
| Card Border | Subtle Gray | `#E9ECEF` |
| Success | Emerald | `#10b981` |
| Danger | Terracotta | `#c2412c` |
| Warning | Amber | `#f59e0b` |

---

## 5. Recent Changes (2026)

### Feature: Design System Integration
- Branch: `feature/design-system-integration`
- Ported Olive ERP design system
- Two-row shell layout implemented
- KPI Grid pattern for dashboards
- Form standardization with `.form-grid`

### Theme Update: Trusted Innovator
- Updated CSS variables in `olive-theme.css`
- New `theme.css` with semantic colors
- Navy (#003566) navigation header
- Teal (#008080) primary buttons

### Reporting Module Fixes
- Navigation links to full index (`reporting:index`)
- Non-HTMX direct access redirects to styled page
- CSV export includes date_from/date_to
- Removed redundant Chart.js scripts

---

## 6. Common Patterns

### 6.1 HTMX Tab Switching
```html
<a hx-get="{% url 'reporting:sales' %}?period={{ period }}"
   hx-target="#report-content"
   class="nav-link">Sales</a>
```

### 6.2 KPI Card Pattern
```html
<div class="kpi-card kpi-green">
    <div class="kpi-icon"><i class="bi bi-cash"></i></div>
    <div class="kpi-content">
        <span class="kpi-label">Revenue</span>
        <span class="kpi-value">${{ amount }}</span>
    </div>
</div>
```

### 6.3 View Redirect Pattern (HTMX Detection)
```python
def get(self, request):
    if not request.headers.get('HX-Request'):
        return redirect(f"{reverse('reporting:index')}?tab=sales")
    # ... render partial
```

---

## 7. Development Commands

```bash
# Run server
python manage.py runserver

# Django check
python manage.py check

# Apply migrations
python manage.py migrate
```

---

## 8. Related Documentation

- `docs/ai_task.md` - Active task tracking
- `olivecrm/static/css/theme.css` - Theme variables
- `olivecrm/static/css/olive-theme.css` - Component styles
- `olivecrm/templates/base.html` - Layout (inline CSS)

---

## 9. Notes for New Team Members

1. **Static files** in `olivecrm/static/` are git-ignored
2. **Wagtail CMS** runs at `/admin/`
3. **HTMX** handles partial page updates
4. **Reporting** uses redirect pattern for non-HTMX requests
5. **Theme colors** are in CSS variables - update there, not inline

---

*This document is a live reference. Append new changes above with date and description.*