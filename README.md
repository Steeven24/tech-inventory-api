# Tech Inventory API

[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-009485?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.13+-3776ab?style=for-the-badge&logo=python)](https://www.python.org)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14+-336791?style=for-the-badge&logo=postgresql)](https://www.postgresql.org)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0+-d52b1e?style=for-the-badge)](https://www.sqlalchemy.org)

A production-oriented RESTful API for managing technology inventory, stock movements, and sales (phones, computers, consoles), built with FastAPI, PostgreSQL, and SQLAlchemy.

## Overview

This API provides:
- JWT authentication
- Role-based permissions (`admin`, `seller`, `warehouse`)
- Product management
- Inventory movement tracking (`in` and `out`)
- Sales with automatic stock impact
- Reports and dashboard endpoints
- Automated tests and CI pipeline

## Route Versioning

The API uses route versioning with a global prefix:

- `v1` base path: `/api/v1`

Examples:
- `/api/v1/auth/login`
- `/api/v1/products`
- `/api/v1/sales`
- `/api/v1/reports/dashboard-overview`
- `/api/v1/version`

Versioning policy:
- Semantic Versioning is used for the API release (`MAJOR.MINOR.PATCH`).
- Backward-compatible changes increment `MINOR`/`PATCH`.
- Breaking changes increment `MAJOR` and should ship under a new route namespace (e.g. `/api/v2`).

## Tech Stack

- Python 3.13+
- FastAPI
- PostgreSQL
- SQLAlchemy
- Pydantic
- passlib + bcrypt
- python-jose (JWT)
- pytest
- GitHub Actions

## Project Structure

```text
tech-inventory-api/
|-- .github/
|   |-- workflows/
|   |   `-- ci.yml
|-- main.py
|-- requirements.txt
|-- requirements-dev.txt
|-- pytest.ini
|-- .env.example
|-- README.md
|-- core/
|   |-- database.py
|   `-- security.py
|-- models/
|   |-- user_model.py
|   |-- product_model.py
|   |-- inventory_movement_model.py
|   `-- sale_model.py
|-- schemas/
|   |-- auth_schema.py
|   |-- user_schema.py
|   |-- product_schema.py
|   |-- inventory_movement_schema.py
|   |-- sale_schema.py
|   `-- report_schema.py
|-- services/
|   |-- user_service.py
|   |-- product_service.py
|   |-- inventory_movement_service.py
|   |-- sale_service.py
|   `-- report_service.py
|-- routes/
|   |-- auth_routes.py
|   |-- user_routes.py
|   |-- product_routes.py
|   |-- inventory_movement_routes.py
|   |-- sale_routes.py
|   `-- report_routes.py
`-- tests/
    |-- conftest.py
    |-- test_auth_roles.py
    `-- test_business_flow.py
```

## Quick Start

1. Clone repository

```bash
git clone https://github.com/Steeven24/tech-inventory-api.git
cd tech-inventory-api
```

2. Create and activate virtual environment

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

3. Install dependencies

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

4. Create PostgreSQL database

```sql
CREATE DATABASE tech_inventory;
```

5. Configure environment

```bash
cp .env.example .env
```

Example `.env`:

```env
DATABASE_URL=postgresql+psycopg2://postgres:your_password@localhost:5432/tech_inventory
SECRET_KEY=your_strong_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

## Database Migrations

Current status:
- Tables are created with `Base.metadata.create_all(...)`.
- A startup compatibility helper ensures the `users.role` column exists.

Recommended next step for production:
- Introduce Alembic for explicit versioned schema migrations.
- Keep migration scripts in source control and apply them in CI/CD before app startup.

## Run

```bash
uvicorn main:app --reload
```

Available at:
- API: http://localhost:8000
- Swagger: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Authentication

1. Create user: `POST /api/v1/users`
2. Login: `POST /api/v1/auth/login`
3. Use token in header:

```text
Authorization: Bearer <access_token>
```

## Permission Matrix

| Module | admin | seller | warehouse |
|---|---|---|---|
| Users management | Yes | No | No |
| Product create/update/delete | Yes | No | Yes |
| Product read | Yes | Yes | Yes |
| Inventory movements | Yes | No | Yes |
| Sales | Yes | Yes | No |
| Reports | Yes | No | No |

## API Endpoints (v1)

Auth:
- `POST /api/v1/auth/login`
- `GET /api/v1/auth/me`

Users:
- `POST /api/v1/users` (public signup)
- `GET /api/v1/users` (admin)
- `GET /api/v1/users/{user_id}` (admin)
- `PUT /api/v1/users/{user_id}` (admin)
- `DELETE /api/v1/users/{user_id}` (admin)

Products:
- `POST /api/v1/products` (admin, warehouse)
- `GET /api/v1/products` (authenticated)
- `GET /api/v1/products/{product_id}` (authenticated)
- `PUT /api/v1/products/{product_id}` (admin, warehouse)
- `DELETE /api/v1/products/{product_id}` (admin, warehouse)

Inventory Movements:
- `POST /api/v1/inventory-movements` (admin, warehouse)
- `GET /api/v1/inventory-movements` (admin, warehouse)
- `GET /api/v1/inventory-movements/{movement_id}` (admin, warehouse)
- `GET /api/v1/inventory-movements/product/{product_id}` (admin, warehouse)

Sales:
- `POST /api/v1/sales` (admin, seller)
- `GET /api/v1/sales` (admin, seller)
- `GET /api/v1/sales/{sale_id}` (admin, seller)

Reports (admin):
- `GET /api/v1/reports/dashboard-overview`
- `GET /api/v1/reports/sales-summary?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD`
- `GET /api/v1/reports/top-products?limit=5&start_date=YYYY-MM-DD&end_date=YYYY-MM-DD`
- `GET /api/v1/reports/low-stock?threshold=5`

Version:
- `GET /api/v1/version`

## Business Rules

- Email must be unique.
- Public signup role is always `seller`.
- SKU must be unique.
- Stock cannot go below zero.
- Inventory movement `out` requires available stock.
- Sales require at least one item.
- Discount cannot exceed subtotal.
- Sales automatically create `out` inventory movements.

## Testing and CI

Local tests:

```bash
pytest
```

Quiet mode:

```bash
pytest -q
```

Coverage includes:
- Auth and role permissions
- Public signup behavior
- Product/inventory/sales business flow
- Insufficient stock checks

CI:
- GitHub Actions workflow at `.github/workflows/ci.yml`
- Runs on push and pull request
- Installs app + dev dependencies and executes pytest

## Error Catalog

Common HTTP status codes:
- `200 OK`: successful read operation
- `201 Created`: successful create operation
- `400 Bad Request`: validation/business rule error
- `401 Unauthorized`: missing or invalid bearer token
- `403 Forbidden`: authenticated user without required role
- `404 Not Found`: resource does not exist

Common business-rule examples:
- `Email already registered`
- `SKU already registered`
- `Insufficient stock for this movement`
- `Insufficient stock for product id <id>`
- `Discount cannot be greater than subtotal`

## Deployment Notes

Minimum production recommendations:
- Set secure environment variables (`DATABASE_URL`, `SECRET_KEY`, token lifetime).
- Run behind a reverse proxy and HTTPS.
- Use managed PostgreSQL and regular backups.
- Run tests in CI before deployment.
- Prefer migration-based database changes (Alembic) over implicit schema creation.

## Troubleshooting

`DATABASE_URL is not configured`:
- Ensure `.env` exists in project root.
- Ensure `DATABASE_URL` is set.

PostgreSQL connection refused:
- Verify PostgreSQL service is running.
- Validate credentials, host, and port.

Port already in use:

```bash
uvicorn main:app --reload --port 8001
```

## Roadmap

- Refresh token and logout
- Pagination, filtering, and sorting
- Alembic migrations
- Purchase orders and suppliers
- Returns and refunds
- Docker deployment profiles

## Author

Steven Loor
GitHub: https://github.com/Steeven24

Last updated: March 29, 2026
