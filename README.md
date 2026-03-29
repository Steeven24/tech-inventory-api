# Tech Inventory API

[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-009485?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.13+-3776ab?style=for-the-badge&logo=python)](https://www.python.org)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14+-336791?style=for-the-badge&logo=postgresql)](https://www.postgresql.org)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0+-d52b1e?style=for-the-badge)](https://www.sqlalchemy.org)

A production-oriented RESTful API for managing inventory, stock movements, and sales of technology products (phones, computers, and consoles), built with FastAPI, PostgreSQL, and SQLAlchemy.

## Table of Contents

- [Overview](#overview)
- [Business Scope](#business-scope)
- [Feature Set](#feature-set)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Quick Start](#quick-start)
- [Environment Variables](#environment-variables)
- [Run the API](#run-the-api)
- [Authentication](#authentication)
- [Role and Permission Matrix](#role-and-permission-matrix)
- [API Endpoints](#api-endpoints)
- [Business Rules](#business-rules)
- [Reports and Dashboard](#reports-and-dashboard)
- [Response and Error Conventions](#response-and-error-conventions)
- [Operational Notes](#operational-notes)
- [Troubleshooting](#troubleshooting)
- [Roadmap](#roadmap)
- [Author](#author)

## Overview

Tech Inventory API centralizes operational workflows for a small-to-medium technology business:
- User authentication and access control
- Product catalog and stock lifecycle
- Sales registration with inventory impact
- Reporting for daily operations and decision-making

The API uses a clear layered structure (routes -> services -> models), enforcing business constraints like SKU uniqueness, role permissions, and stock integrity.

## Business Scope

This backend supports end-to-end inventory and sales operations:
- Product onboarding and maintenance
- Incoming and outgoing inventory movements
- Sales transactions with multiple line items
- Dashboard KPIs and report queries
- Segregation of duties through roles: admin, seller, warehouse

## Feature Set

### Authentication and Authorization
- Public signup and secure login
- JWT access token flow (Bearer)
- Password hashing with bcrypt (passlib)
- Role-based access control via reusable permission dependency

### User Management
- CRUD operations for users
- Roles: admin, seller, warehouse
- Public signup hardening: role is always forced to seller

### Product Management
- Product CRUD
- Unique SKU validation
- Required fields: name, category, brand, SKU, price, stock

### Inventory Movements
- Manual stock movement registration (in/out)
- Validation to prevent negative stock
- Product-level movement history

### Sales
- Multi-item sales creation
- Discount support at sale level
- Automatic subtotal and total calculation
- Automatic stock deduction per sale item
- Automatic out inventory movement audit per sale line

### Reports and Dashboard
- Sales summary by date range
- Top-selling products by quantity and revenue
- Low stock report with configurable threshold
- Dashboard overview metrics

## Architecture

Layered architecture:
- routes/: HTTP contracts, dependencies, authorization policy
- services/: business logic and domain validation
- models/: SQLAlchemy persistence models
- schemas/: request and response contracts (Pydantic)
- core/: database/session setup and JWT utilities

Design principles:
- Thin routes, explicit service layer
- Clear separation between persistence and API contracts
- Role checks at route boundaries
- Inventory traceability through movement records

## Tech Stack

- Python 3.13+
- FastAPI
- PostgreSQL
- SQLAlchemy
- Pydantic
- python-jose (JWT)
- passlib (bcrypt)
- python-dotenv
- uvicorn

## Project Structure

```text
tech-inventory-api/
├── main.py
├── requirements.txt
├── .env.example
├── README.md
├── core/
│   ├── database.py
│   └── security.py
├── models/
│   ├── user_model.py
│   ├── product_model.py
│   ├── inventory_movement_model.py
│   └── sale_model.py
├── schemas/
│   ├── auth_schema.py
│   ├── user_schema.py
│   ├── product_schema.py
│   ├── inventory_movement_schema.py
│   ├── sale_schema.py
│   └── report_schema.py
├── services/
│   ├── user_service.py
│   ├── product_service.py
│   ├── inventory_movement_service.py
│   ├── sale_service.py
│   └── report_service.py
└── routes/
        ├── auth_routes.py
        ├── user_routes.py
        ├── product_routes.py
        ├── inventory_movement_routes.py
        ├── sale_routes.py
        └── report_routes.py
```

## Quick Start

### 1. Clone repository

```bash
git clone https://github.com/Steeven24/tech-inventory-api.git
cd tech-inventory-api
```

### 2. Create and activate virtual environment

Windows:
```bash
python -m venv venv
venv\Scripts\Activate.ps1
```

Linux/macOS:
```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create PostgreSQL database

```sql
CREATE DATABASE tech_inventory;
```

### 5. Configure environment

```bash
cp .env.example .env
```

## Environment Variables

Example .env:

```env
DATABASE_URL=postgresql+psycopg2://postgres:your_password@localhost:5432/tech_inventory
SECRET_KEY=your_strong_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

Variable reference:
- DATABASE_URL: SQLAlchemy database connection string
- SECRET_KEY: key used to sign JWT tokens
- ALGORITHM: JWT signing algorithm (HS256)
- ACCESS_TOKEN_EXPIRE_MINUTES: token lifetime in minutes

## Run the API

Development mode:

```bash
uvicorn main:app --reload
```

Application URLs:
- http://localhost:8000
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Authentication

1. Register user via POST /users
2. Login via POST /auth/login
3. Send token as:

```text
Authorization: Bearer <access_token>
```

Sample login response:

```json
{
    "access_token": "<jwt>",
    "token_type": "bearer"
}
```

## Role and Permission Matrix

| Module | admin | seller | warehouse |
|---|---|---|---|
| Users management | Yes | No | No |
| Product create/update/delete | Yes | No | Yes |
| Product read | Yes | Yes | Yes |
| Inventory movements | Yes | No | Yes |
| Sales | Yes | Yes | No |
| Reports | Yes | No | No |

## API Endpoints

### Auth
- POST /auth/login
- GET /auth/me

### Users
- POST /users (public signup)
- GET /users (admin)
- GET /users/{user_id} (admin)
- PUT /users/{user_id} (admin)
- DELETE /users/{user_id} (admin)

### Products
- POST /products (admin, warehouse)
- GET /products (authenticated)
- GET /products/{product_id} (authenticated)
- PUT /products/{product_id} (admin, warehouse)
- DELETE /products/{product_id} (admin, warehouse)

### Inventory Movements
- POST /inventory-movements (admin, warehouse)
- GET /inventory-movements (admin, warehouse)
- GET /inventory-movements/{movement_id} (admin, warehouse)
- GET /inventory-movements/product/{product_id} (admin, warehouse)

### Sales
- POST /sales (admin, seller)
- GET /sales (admin, seller)
- GET /sales/{sale_id} (admin, seller)

### Reports (admin)
- GET /reports/dashboard-overview
- GET /reports/sales-summary?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD
- GET /reports/top-products?limit=5&start_date=YYYY-MM-DD&end_date=YYYY-MM-DD
- GET /reports/low-stock?threshold=5

## Business Rules

### User Rules
- Email must be unique
- Password is stored hashed
- Public signup cannot escalate role (always seller)

### Product Rules
- SKU must be unique
- Price must be greater than 0
- Stock cannot be negative

### Inventory Movement Rules
- Allowed movement types: in, out
- Quantity must be greater than 0
- Out movement requires enough stock

### Sales Rules
- A sale must include at least one item
- Every sale item product must exist
- Every sale item quantity must be greater than 0
- Discount cannot exceed subtotal
- Stock is deducted atomically with sale registration
- Out movements are created for traceability

## Reports and Dashboard

Available analytics:
- Sales count, revenue, and average ticket
- Top products by sold quantity and total revenue
- Low stock monitoring by configurable threshold
- Daily and global dashboard KPIs

Date filtering behavior:
- start_date and end_date are optional
- If omitted, reports run over all available data

## Response and Error Conventions

Common success codes:
- 200 OK: read operations
- 201 Created: create operations

Common error codes:
- 400 Bad Request: validation or business rule violations
- 401 Unauthorized: missing or invalid token
- 403 Forbidden: authenticated but insufficient role
- 404 Not Found: missing resources

Typical error payload:

```json
{
    "detail": "Error message"
}
```

## Operational Notes

- Existing databases are backward-compatible for user roles through startup check (ensure_user_role_column)
- Base.metadata.create_all(...) is used for table creation
- For production-grade schema evolution, add Alembic migrations
- Keep SECRET_KEY private and rotate it per environment

## Example cURL

Create product:

```bash
curl -X POST http://localhost:8000/products \
    -H "Authorization: Bearer <token>" \
    -H "Content-Type: application/json" \
    -d '{
        "name": "iPhone 15 Pro",
        "category": "Smartphones",
        "brand": "Apple",
        "sku": "IPHONE15PRO001",
        "price": 999.99,
        "stock": 25
    }'
```

Create sale:

```bash
curl -X POST http://localhost:8000/sales \
    -H "Authorization: Bearer <token>" \
    -H "Content-Type: application/json" \
    -d '{
        "discount": 10,
        "items": [
            {"product_id": 1, "quantity": 2},
            {"product_id": 2, "quantity": 1}
        ]
    }'
```

Get dashboard overview:

```bash
curl -X GET "http://localhost:8000/reports/dashboard-overview" \
    -H "Authorization: Bearer <admin_token>"
```

## Troubleshooting

DATABASE_URL is not configured:
- Ensure .env exists in project root
- Ensure DATABASE_URL is defined

PostgreSQL connection refused:
- Ensure PostgreSQL service is running
- Validate credentials, host, and port

Port 8000 already in use:

```bash
uvicorn main:app --reload --port 8001
```

## Roadmap

- Refresh token and logout
- Advanced filtering, sorting, and pagination
- Automated tests and CI pipeline
- Alembic migrations
- Purchase orders and suppliers
- Returns and refunds
- Observability (metrics and logging)
- Docker and deployment profiles

## Author

Steven Loor  
GitHub: https://github.com/Steeven24

Last updated: March 29, 2026
# Tech Inventory API

[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-009485?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.13+-3776ab?style=for-the-badge&logo=python)](https://www.python.org)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14+-336791?style=for-the-badge&logo=postgresql)](https://www.postgresql.org)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0+-d52b1e?style=for-the-badge)](https://www.sqlalchemy.org)

A production-oriented RESTful API for managing inventory, stock movements, and sales of technology products (phones, computers, and consoles), built with FastAPI, PostgreSQL, and SQLAlchemy.

## Table of Contents

- [Overview](#overview)
- [Business Scope](#business-scope)
- [Feature Set](#feature-set)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Quick Start](#quick-start)
- [Environment Variables](#environment-variables)
- [Run the API](#run-the-api)
- [Authentication](#authentication)
- [Role and Permission Matrix](#role-and-permission-matrix)
- [API Endpoints](#api-endpoints)
- [Business Rules](#business-rules)
- [Reports and Dashboard](#reports-and-dashboard)
- [Response and Error Conventions](#response-and-error-conventions)
- [Operational Notes](#operational-notes)
- [Troubleshooting](#troubleshooting)
- [Roadmap](#roadmap)
- [Author](#author)

## Overview

Tech Inventory API centralizes operational workflows for a small-to-medium technology business:
- User authentication and access control
- Product catalog and stock lifecycle
- Sales registration with inventory impact
- Reporting for daily operation and management decisions

The API is designed around clear modules (routes -> services -> models) and enforces domain constraints such as SKU uniqueness, stock integrity, and role-based authorization.

## Business Scope

This backend supports end-to-end inventory and sales operations:
- Product onboarding and maintenance
- Incoming/outgoing inventory movements
- Sales transactions with multiple line items
- Dashboard KPIs and report queries for decision-making
- Segregation of duties through roles: `admin`, `seller`, `warehouse`

## Feature Set

### Authentication and Authorization
- Public signup and secure login
- JWT access token flow (`Bearer`)
- Password hashing with bcrypt (`passlib`)
- Role-based access control via reusable permission dependency

### User Management
- CRUD operations for users
- Role support: `admin`, `seller`, `warehouse`
- Public signup hardening: role is forced to `seller`

### Product Management
- Product CRUD
- Unique SKU validation
- Required fields: name, category, brand, SKU, price, stock

### Sales
- Multi-item sales creation
- Discount support at sale level
- Automatic subtotal and total calculation
- Automatic stock deduction by sale item
- Automatic `out` inventory movement audit per sale line

### Inventory Movements
- Manual stock movement registration (`in` / `out`)
- Validation to prevent negative stock
- Product-level movement history

### Reports and Dashboard
- Sales summary in optional date range
- Top-selling products by quantity and revenue
- Low stock report with configurable threshold
- Dashboard overview metrics for operations

## Architecture

Layered architecture:
- `routes/`: transport layer (HTTP contracts, dependency wiring, access policy)
- `services/`: business logic and validation rules
- `models/`: persistence models (SQLAlchemy)
- `schemas/`: request/response contracts (Pydantic)
- `core/`: database/session setup and JWT utilities

Design principles used:
- Thin routes, explicit service layer
- Clear separation between persistence and API schemas
- Consistent role checks at route boundaries
- Auditability through inventory movement logs

## Tech Stack

- Python 3.13+
- FastAPI
- PostgreSQL
- SQLAlchemy
- Pydantic
- python-jose (JWT)
- passlib (bcrypt)
- python-dotenv
- uvicorn

## Project Structure

```text
tech-inventory-api/
├── main.py
├── requirements.txt
├── .env.example
├── README.md
├── core/
│   ├── database.py
│   └── security.py
├── models/
│   ├── user_model.py
│   ├── product_model.py
│   ├── inventory_movement_model.py
│   └── sale_model.py
├── schemas/
│   ├── auth_schema.py
│   ├── user_schema.py
│   ├── product_schema.py
│   ├── inventory_movement_schema.py
│   ├── sale_schema.py
│   └── report_schema.py
├── services/
│   ├── user_service.py
│   ├── product_service.py
│   ├── inventory_movement_service.py
│   ├── sale_service.py
│   └── report_service.py
└── routes/
    ├── auth_routes.py
## Quick Start
    ├── product_routes.py
### 1. Clone repository
    ├── sale_routes.py
    └── report_routes.py
```

## Setup

### 2. Create and activate virtual environment

```bash
git clone https://github.com/Steeven24/tech-inventory-api.git
cd tech-inventory-api
```

### 2. Create and activate virtual environment

Windows:
```bash
python -m venv venv
venv\Scripts\Activate.ps1
```

Linux/macOS:
```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create PostgreSQL database

```sql
CREATE DATABASE tech_inventory;
```

### 5. Configure environment

Copy:
```bash
cp .env.example .env
```

## Environment Variables

Example `.env`:

```env
DATABASE_URL=postgresql+psycopg2://postgres:your_password@localhost:5432/tech_inventory
SECRET_KEY=your_strong_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

Variable reference:
- `DATABASE_URL`: SQLAlchemy database connection string
- `SECRET_KEY`: key used to sign JWT tokens
- `ALGORITHM`: JWT signing algorithm (`HS256`)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: token lifetime in minutes

## Run the API

Development mode:

```bash
uvicorn main:app --reload
```

Application URLs:
- http://localhost:8000
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Authentication

1. Register user via `POST /users`
2. Login via `POST /auth/login`
3. Send token as:

```text
Authorization: Bearer <access_token>
```

Sample login response:

```json
{
    "access_token": "<jwt>",
    "token_type": "bearer"
}
```

## Role and Permission Matrix

| Module | admin | seller | warehouse |
|---|---|---|---|
| Users management | Yes | No | No |
| Product create/update/delete | Yes | No | Yes |
| Product read | Yes | Yes | Yes |
| Inventory movements | Yes | No | Yes |
| Sales | Yes | Yes | No |
| Reports | Yes | No | No |

## API Endpoints

### Auth
- POST /auth/login
- GET /auth/me

### Users
- POST /users (public signup)
- GET /users (admin)
- GET /users/{user_id} (admin)
- PUT /users/{user_id} (admin)
- DELETE /users/{user_id} (admin)

### Products
- POST /products (admin, warehouse)
- GET /products (authenticated)
- GET /products/{product_id} (authenticated)
- PUT /products/{product_id} (admin, warehouse)
- DELETE /products/{product_id} (admin, warehouse)

### Inventory Movements
- POST /inventory-movements (admin, warehouse)
- GET /inventory-movements (admin, warehouse)
- GET /inventory-movements/{movement_id} (admin, warehouse)
- GET /inventory-movements/product/{product_id} (admin, warehouse)

### Sales
- POST /sales (admin, seller)
- GET /sales (admin, seller)
- GET /sales/{sale_id} (admin, seller)

### Reports (admin)
- GET /reports/dashboard-overview
- GET /reports/sales-summary?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD
- GET /reports/top-products?limit=5&start_date=YYYY-MM-DD&end_date=YYYY-MM-DD
- GET /reports/low-stock?threshold=5

## Business Rules

### User Rules
- Email must be unique
- Password is stored hashed
- Public signup cannot escalate role (always `seller`)

### Product Rules
- SKU must be unique
- Price must be greater than 0
- Stock cannot be negative

### Inventory Movement Rules
- Movement types allowed: `in`, `out`
- Quantity must be > 0
- `out` movement requires enough stock

### Sales Rules
- A sale must include at least one item
- Every item product must exist
- Every item quantity must be > 0
- Discount cannot exceed subtotal
- Stock is deducted atomically with sale registration
- Out movements are created for traceability

## Reports and Dashboard

Available analytics:
- Sales count, revenue, and average ticket
- Top products by sold quantity and total revenue
- Low stock monitoring by configurable threshold
- Daily and global dashboard KPIs

Date filtering behavior:
- `start_date` and `end_date` are optional
- If omitted, reports run over all available data

## Response and Error Conventions

Common success codes:
- `200 OK`: read operations
- `201 Created`: create operations

Common error codes:
- `400 Bad Request`: validation or business rule violations
- `401 Unauthorized`: missing/invalid token
- `403 Forbidden`: authenticated but insufficient role
- `404 Not Found`: missing resources

Typical error payload:

```json
{
    "detail": "Error message"
}
```

## Operational Notes

- Existing databases are backward-compatible for user roles through startup check (`ensure_user_role_column`)
- `Base.metadata.create_all(...)` is used for table creation
- For production-grade schema evolution, adding Alembic migrations is strongly recommended
- Keep `SECRET_KEY` private and rotate it per environment

## Example cURL

Create product:

```bash
curl -X POST http://localhost:8000/products \
    -H "Authorization: Bearer <token>" \
    -H "Content-Type: application/json" \
    -d '{
        "name": "iPhone 15 Pro",
        "category": "Smartphones",
        "brand": "Apple",
        "sku": "IPHONE15PRO001",
        "price": 999.99,
        "stock": 25
    }'
```

Create sale:

```bash
curl -X POST http://localhost:8000/sales \
    -H "Authorization: Bearer <token>" \
    -H "Content-Type: application/json" \
    -d '{
        "discount": 10,
        "items": [
            {"product_id": 1, "quantity": 2},
            {"product_id": 2, "quantity": 1}
        ]
    }'
```

Fetch dashboard:

```bash
curl -X GET "http://localhost:8000/reports/dashboard-overview" \
    -H "Authorization: Bearer <admin_token>"
```

## Troubleshooting

DATABASE_URL is not configured:
- Ensure .env exists in project root
- Ensure DATABASE_URL is defined

PostgreSQL connection refused:
- Ensure PostgreSQL service is running
- Validate credentials, host, and port

Port 8000 already in use:

```bash
uvicorn main:app --reload --port 8001
```

## Roadmap

- Refresh token and logout
- Advanced filtering, sorting, and pagination
- Automated tests and CI pipeline
- Alembic migrations
- Purchase orders and suppliers
- Returns and refunds
- Observability (metrics/logging)
- Docker and deployment profiles

## License

This project is intended for portfolio and educational use unless otherwise specified by the repository owner.

## Author

Steven Loor
GitHub: https://github.com/Steeven24

Last updated: March 29, 2026
