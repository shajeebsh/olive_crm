# OliveCRM

Modern, affordable CRM application targeting small to mid-sized companies (SMBs). Built with Django 5.0 and Wagtail 6.0.

## Tech Stack
- **Backend**: Django 5.0+, Django Rest Framework
- **CMS**: Wagtail 6.0+
- **Frontend**: Bootstrap 5, HTMX, PWA Ready
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

### Phase 3: ERP Lite & API
- **Invoicing & Payments**: Full billing cycle management with detail views, PDF-ready status tracking, and CRUD.
- **Inventory Management**: Stock tracking across multiple warehouses with title-aware index views.
- **REST API**: Secure endpoints for all core modules.

### Phase 4: Ecosystem & Optimization
- **Audit Logs**: Enterprise-grade change tracking.
- **Partner Program**: Affiliate and referral management.
- **PWA**: Mobile-ready with progressive web app support.

### Phase 8: UX Polish & QA (Latest)
- **Advanced Lists**: 3-dot dropdown "Actions" menu for every list view (Contacts, Deals, Invoices, etc.).
- **Live Metrics**: Dashboard widgets powered by real-time querysets (no hardcoded data).
- **Consistent UI**: Custom `currency` filter ($1,234.56) and text-truncation on Kanban cards.
- **Detailed Invoicing**: High-fidelity detail page for invoices with line-item summaries and action buttons.
- **Enhanced Kanban**: Visual board with dynamic owner avatars and status-aware styling.

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

### 6. Automated Testing
To ensure the system is functioning correctly, you can run the automated test suite.

#### a. Run All Tests
```bash
source venv/bin/activate
python manage.py test
```

#### b. Run Tests for Specific Modules
If you are working on a specific area, you can run tests for just that module:
```bash
# Core & AI logic
python manage.py test olivecrm.core

# CRM & Sales
python manage.py test olivecrm.contacts olivecrm.sales

# ERP (Invoicing & Inventory)
python manage.py test olivecrm.invoicing olivecrm.inventory

# Marketing & Automation
python manage.py test olivecrm.marketing olivecrm.automation olivecrm.communication
```

The test suite covers:
- **Core**: AI Service mocking and Audit Logging.
- **CRM**: Contact and Company relationships.
- **Sales**: Pipeline stage transitions and Task management.
- **ERP**: Invoice total calculations and automated payment processing.
- **Marketing**: Campaign targeting and Mailing List segmentation.
- **Automation**: Workflow trigger and action configurations.

### 7. API Documentation
The REST API is available at `/api/`. Use the browsable API or tools like Postman.

### 7. Run the Server
```bash
python manage.py runserver
```
Access the application at `http://localhost:8000/`.

## End-to-End (E2E) Testing Scenarios

Validate the full system integration by following these core workflows:

### 1. Lead Capture & AI Scoring
1. Navigate to a **Wagtail Landing Page** (e.g., `/marketing/demo-page/`).
2. Submit the lead capture form with a new email.
3. **Verify**: A new `Contact` is created in the CRM.
4. **Verify**: The `AIService` automatically runs, assigns a lead score, and generates a personalized follow-up in the interaction log.

### 2. Marketing Campaign Execution
1. Create a `Mailing List` and add the new contact.
2. Design an `Email Campaign` using the Wagtail StreamField editor.
3. Schedule/Send the campaign.
4. **Verify**: Interaction records are created for all contacts in the list.

### 3. Sales Pipeline & ERP Lifecycle
1. Convert a `Contact` into a `Deal` within a sales `Pipeline`.
2. Open the **Pipeline Kanban** view and observe the dynamic user avatars and text truncation.
3. Click on a card to navigate to the **Deal Detail** page.
4. Move the `Deal` to the "Won" stage and use the **3-dot Actions menu** to create an Invoice.
5. Generate an `Invoice` with at least two `Line Items` and view the high-fidelity **Invoice Detail** page.
6. Record a `Payment` against the invoice or use the "Mark as Paid" action.
7. **Verify**: Invoice status changes to "Paid", all amounts are formatted with the `currency` filter, and a `StockLevel` deduction is triggered.

### 4. Communication & Audit
1. Run `python manage.py sync_email`.
2. **Verify**: External emails from configured `EmailAccounts` appear as `Interactions` under the matching `Contact`.
3. Modify a `Contact` record.
4. **Verify**: An entry is created in the `AuditLog` (visible in Django Admin) detailing the fields changed.

### 5. API Integration
1. Authenticate via the REST API (Token or Session).
2. Perform a `GET` request to `/api/contacts/`.
3. Perform a `POST` request to `/api/invoices/` to create a new billing record.
4. **Verify**: JSON responses return correct model data.

## Documentation
Full project walkthrough and detailed task lists are available in the [artifacts directory](file:///Users/shajeebs/.gemini/antigravity/brain/acb0b3f9-f1f9-4a55-b1a3-df3d29ef3dea/).
- [Full Project Walkthrough](file:///Users/shajeebs/.gemini/antigravity/brain/acb0b3f9-f1f9-4a55-b1a3-df3d29ef3dea/walkthrough.md)
