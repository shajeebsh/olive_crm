# Architecture Overview

OliveCRM implements a **hybrid architecture** that combines several modern architectural patterns to create a scalable, maintainable, and feature-rich CRM platform.

## Core Architectural Patterns

### 1. Modular Monolith Architecture (Primary Pattern)
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

### 2. Model-View-Template (MVT) Pattern with HTMX Enhancement
Following Django's native architecture with modern frontend interactions:
- **Models**: Data structure & business logic (`contacts/models.py`)
- **Views**: Request handling & data retrieval (`contacts/views.py`)  
- **Templates**: Presentation layer (`templates/contacts/contact_detail.html`)
- **HTMX**: Partial updates for SPA-like experience while maintaining MVT simplicity

### 3. Domain-Driven Design (DDD) Influences
Each module represents a clear bounded context with its own:
- Data models and business logic
- Views and URL routing
- Templates and UI components
- Test suites

### 4. Service Layer Pattern
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

### 5. Event-Driven Architecture
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

### 6. RESTful API Layer
Comprehensive REST API using Django REST Framework:
- REST endpoints for all major entities
- Browsable API interface
- Secure authentication and authorization
- Consistent API patterns across all modules

### 7. Emerging Hexagonal Architecture (Ports & Adapters)
Patterns for easy integration swapping:
- Communication module supports multiple email providers
- AI service abstraction for different AI providers
- Flexible integration points for third-party services

## Data Architecture

### Persistence Patterns
- **JSON Fields**: Extensive use for flexible configuration (workflow triggers, actions, etc.)
- **Polymorphic Relationships**: Foreign keys between different entity types  
- **Audit Logging**: Comprehensive audit trail system tracking all significant actions
- **Time-Stamped Models**: Abstract base model for consistent created/updated timestamps

### Database Design
- **Relational Database**: MySQL (production) / SQLite (development)
- **Foreign Key Relationships**: Proper relational integrity
- **Denormalization**: Strategic denormalization for performance (e.g., stage_order in deals)
- **Indexing**: Optimized indexes for common query patterns

## Frontend Architecture

### Progressive Enhancement
- **Server-Rendered Templates**: Django template language for core functionality
- **HTMX Enhancement**: Modern, interactive UI components without full page reloads
- **PWA Ready**: Mobile-ready progressive web app support

### UI Component Architecture
- **Template Inheritance**: Well-structured hierarchy with `base.html`
- **Reusable Partials**: Component-based template partials
- **Consistent Styling**: Bootstrap 5 with custom OliveCRM theme
- **Responsive Design**: Mobile-first responsive layouts

## Security Architecture

### Built-in Protections
- **CSRF Protection**: Django's built-in CSRF middleware
- **XSS Prevention**: Automatic escaping in templates
- **SQL Injection Protection**: ORM-based query building
- **Clickjacking Protection**: X-Frame-Options middleware

### Access Control
- **Role-Based Access**: Django's permission system integration
- **Authentication**: Django's built-in auth system
- **Authorization**: Fine-grained permission checks
- **Audit Trail**: Comprehensive change tracking

## Deployment Architecture

### Containerization & Orchestration
- **Docker Support**: Containerized deployment
- **Environment-Based Config**: Separate settings for dev/production
- **WSGI Server**: Gunicorn for production serving
- **Process Management**: Celery for background tasks

### Scalability Features
- **Redis Integration**: Caching and message brokering
- **Celery Workers**: Background task processing
- **Database Pooling**: Connection management for scale
- **Static File Serving**: CDN-ready static file configuration

## Why This Architecture Works for OliveCRM

| Challenge | Architectural Solution |
|-----------|------------------------|
| SMBs need flexibility | Modular Monolith - easy to customize |
| Must beat competitors on UX | MVT + HTMX - fast, interactive UI |
| Complex workflows | Service Layer + Events - clean logic |
| Multiple integrations | Ports & Adapters - swap providers easily |
| Future growth | Modular - can split to microservices |
| AI features | Service Layer - isolated AI complexity |
