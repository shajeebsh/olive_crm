# REST API Documentation

OliveCRM provides a secure and comprehensive REST API built with **Django REST Framework (DRF)**.

## 1. Overview

The REST API allows external systems to interact with OliveCRM for contact management, sales tracking, and reporting.

- **Base URL**: `/api/`
- **Authentication**: Token-based authentication (default) or session authentication (for browsable API).
- **Format**: JSON

## 2. API Endpoints

The API is organized by business module:

- **Contacts**: `/api/contacts/`
- **Companies**: `/api/companies/`
- **Deals**: `/api/deals/`
- **Invoices**: `/api/invoices/`
- **Inventory**: `/api/inventory/`

## 3. Usage

### Browsable API
The REST API is available at `/api/` in your browser. Use the interactive interface to explore and test the endpoints.

### Postman or cURL
You can also use tools like Postman or `curl` to interact with the API:

```bash
curl -X GET http://localhost:8000/api/contacts/ -H "Authorization: Token <your-token>"
```

## 4. Documentation

Detailed API documentation is generated using DRF's schema generation or third-party tools like Swagger/OpenAPI.
- **API Schema**: `/api/schema/`
- **Swagger UI**: `/api/docs/`
