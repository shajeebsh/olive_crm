# Testing and Quality Assurance

OliveCRM includes a comprehensive test suite to ensure the stability and reliability of its features.

## 1. Automated Testing

To ensure the system is functioning correctly, run the automated test suite.

### a. Run All Tests
```bash
source venv/bin/activate
python manage.py test
```

### b. Run Tests for Specific Modules
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

## 2. Test Coverage

The test suite covers:
- **Core**: AI Service mocking and Audit Logging.
- **CRM**: Contact and Company relationships.
- **Sales**: Pipeline stage transitions and Task management.
- **ERP**: Invoice total calculations and automated payment processing.
- **Marketing**: Campaign targeting and Mailing List segmentation.
- **Automation**: Workflow trigger and action configurations.

## 3. End-to-End (E2E) Testing Scenarios

Validate the full system integration by following these core workflows:

### Scenario 1: Lead Capture & AI Scoring
1. Navigate to a **Wagtail Landing Page** (e.g., `/marketing/demo-page/`).
2. Submit the lead capture form with a new email.
3. **Verify**: A new `Contact` is created in the CRM.
4. **Verify**: The `AIService` automatically runs, assigns a lead score, and generates a personalized follow-up in the interaction log.

### Scenario 2: Pipeline Stage Transitions
1. Create a new `Deal`.
2. Move the deal across different pipeline stages (Lead -> Qualified -> Proposal -> Negotiation -> Closed Won).
3. **Verify**: The probability and color-coding update correctly in the Kanban view.

### Scenario 3: Invoicing Workflow
1. Create an `Invoice` for a `Contact`.
2. Add line items and verify the total calculation.
3. **Verify**: The PDF view renders correctly and the status updates upon payment.
