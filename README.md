# OliveCRM

Modern, affordable CRM application targeting small to mid-sized companies (SMBs). Built with Django 5.0 and Wagtail 6.0.

## Architecture Overview

OliveCRM implements a **hybrid architecture** that combines several modern architectural patterns to create a scalable, maintainable, and feature-rich CRM platform.

### Core Architectural Patterns

#### 1. Modular Monolith Architecture (Primary Pattern)
The application is organized as a single deployable unit with independent, loosely-coupled modules:

```
olivecrm/
├── contacts/          # Contact Management Context
├── sales/            # Sales Pipeline Context  
├── invoicing/        # Billing Context
├── inventory/        # Stock Management Context
├── marketing/        # Campaign Context
├── automation/       # Workflow Automation Context
├── communication/    # Messaging Context
├── reporting/        # Analytics Context
└── core/             # Shared Utilities & Base Models
```

**Benefits**:
- Easier development than microservices (single codebase)
- Clear boundaries between CRM features
- Future-ready - modules can be split into microservices later
- Team scalability - different developers can work on different modules

#### 2. Model-View-Template (MVT) Pattern with HTMX Enhancement
Following Django's native architecture with modern frontend interactions:
- **Models**: Data structure & business logic (`contacts/models.py`)
- **Views**: Request handling & data retrieval (`contacts/views.py`)  
- **Templates**: Presentation layer (`templates/contacts/contact_detail.html`)
- **HTMX**: Partial updates for SPA-like experience while maintaining MVT simplicity

#### 3. Domain-Driven Design (DDD) Influences
Each module represents a clear bounded context with its own:
- Data models and business logic
- Views and URL routing
- Templates and UI components
- Test suites

#### 4. Service Layer Pattern
Complex business logic is encapsulated in service classes:
```python
# core/ai_service.py
class AIService:
    def score_lead(self, contact_data):
        """Complex AI logic separated from models/views"""
        pass
    
    def compose_email(self, context):
        """Email composition as a service"""
        pass
```

**Benefits**:
- Keeps models thin (mostly data structure)
- Keeps views thin (mostly HTTP handling)  
- Services handle business complexity
- Easy to test and maintain

#### 5. Event-Driven Architecture
Sophisticated workflow engine in the automation module:
```python
# automation/models.py
class Workflow(models.Model):
    TRIGGER_TYPES = [
        ('record_created', 'Record Created'),
        ('record_updated', 'Record Updated'), 
        ('field_changed', 'Specific Field Changed'),
        ('date_reached', 'Date Field Reached'),
        ('incoming_email', 'Incoming Email'),
        ('form_submitted', 'Form Submitted'),
    ]
    
    trigger_type = models.CharField(max_length=50, choices=TRIGGER_TYPES)
    trigger_config = models.JSONField()  # Event configuration
    actions = models.JSONField()  # List of actions to perform
```

**Powers**:
- Workflow automation (no-code triggers)
- Webhook integrations  
- Audit logging
- Real-time business process automation

#### 6. RESTful API Layer
Comprehensive REST API using Django REST Framework:
- REST endpoints for all major entities
- Browsable API interface
- Secure authentication and authorization
- Consistent API patterns across all modules

#### 7. Emerging Hexagonal Architecture (Ports & Adapters)
Patterns for easy integration swapping:
- Communication module supports multiple email providers
- AI service abstraction for different AI providers
- Flexible integration points for third-party services

### Data Architecture

#### Persistence Patterns
- **JSON Fields**: Extensive use for flexible configuration (workflow triggers, actions, etc.)
- **Polymorphic Relationships**: Foreign keys between different entity types  
- **Audit Logging**: Comprehensive audit trail system tracking all significant actions
- **Time-Stamped Models**: Abstract base model for consistent created/updated timestamps

#### Database Design
- **Relational Database**: MySQL (production) / SQLite (development)
- **Foreign Key Relationships**: Proper relational integrity
- **Denormalization**: Strategic denormalization for performance (e.g., stage_order in deals)
- **Indexing**: Optimized indexes for common query patterns

### Frontend Architecture

#### Progressive Enhancement
- **Server-Rendered Templates**: Django template language for core functionality
- **HTMX Enhancement**: Modern, interactive UI components without full page reloads
- **PWA Ready**: Mobile-ready progressive web app support

#### UI Component Architecture
- **Template Inheritance**: Well-structured hierarchy with `base.html`
- **Reusable Partials**: Component-based template partials
- **Consistent Styling**: Bootstrap 5 with custom OliveCRM theme
- **Responsive Design**: Mobile-first responsive layouts

### Security Architecture

#### Built-in Protections
- **CSRF Protection**: Django's built-in CSRF middleware
- **XSS Prevention**: Automatic escaping in templates
- **SQL Injection Protection**: ORM-based query building
- **Clickjacking Protection**: X-Frame-Options middleware

#### Access Control
- **Role-Based Access**: Django's permission system integration
- **Authentication**: Django's built-in auth system
- **Authorization**: Fine-grained permission checks
- **Audit Trail**: Comprehensive change tracking

### Deployment Architecture

#### Containerization & Orchestration
- **Docker Support**: Containerized deployment
- **Environment-Based Config**: Separate settings for dev/production
- **WSGI Server**: Gunicorn for production serving
- **Process Management**: Celery for background tasks

#### Scalability Features
- **Redis Integration**: Caching and message brokering
- **Celery Workers**: Background task processing
- **Database Pooling**: Connection management for scale
- **Static File Serving**: CDN-ready static file configuration

### Why This Architecture Works for OliveCRM

| Challenge | Architectural Solution |
|-----------|------------------------|
| SMBs need flexibility | Modular Monolith - easy to customize |
| Must beat competitors on UX | MVT + HTMX - fast, interactive UI |
| Complex workflows | Service Layer + Events - clean logic |
| Multiple integrations | Ports & Adapters - swap providers easily |
| Future growth | Modular - can split to microservices |
| AI features | Service Layer - isolated AI complexity |

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
- **Enhanced Kanban**: Visual board with dynamic owner avatars, status-aware styling, and interactive filter panel.
- **Pipeline Color Coding**: Each Kanban stage has a distinct color scheme for quick visual identification:
  | Stage | Color |
  |---|---|
  | Lead | Blue |
  | Qualified | Yellow |
  | Proposal | Purple |
  | Negotiation | Orange |
  | Closed Won | Green |
- **Probability Badges**: Each deal card displays a color-coded probability badge — 🟢 High (≥80%), 🟡 Medium (40–79%), 🔴 Low (<40%).
- **List Scorecards**: Company list shows Total Contacts, Total Invoices, and Total Invoice Value. Contact list shows Total Contacts, Total Deals, and Total Deal Value.

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