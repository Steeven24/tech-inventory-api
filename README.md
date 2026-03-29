# Tech Inventory API

RESTful API built with FastAPI for managing inventory and sales of technology products.

## PostgreSQL setup

1. Create database:
   - Name: `tech_inventory`
2. Copy `.env.example` to `.env` and adjust credentials.
3. Install dependencies:
   - `pip install -r requirements.txt`
4. Run API:
   - `uvicorn main:app --reload`

## Environment variables

- `DATABASE_URL`: PostgreSQL connection string.
  - Example: `postgresql+psycopg2://postgres:postgres@localhost:5432/tech_inventory`

## Current modules

- `main.py`: API entrypoint
- `database.py`: SQLAlchemy engine/session
- `models/user_model.py`: User table model
- `routes/user_routes.py`: User endpoints
- `services/user_service.py`: User business logic
