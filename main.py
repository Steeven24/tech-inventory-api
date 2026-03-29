from fastapi import FastAPI

from core.database import Base, engine, ensure_user_role_column
from models.inventory_movement_model import InventoryMovement
from models.product_model import Product
from models.sale_model import Sale, SaleItem
from models.user_model import User
from routes.auth_routes import router as auth_router
from routes.inventory_movement_routes import router as inventory_movement_router
from routes.product_routes import router as product_router
from routes.report_routes import router as report_router
from routes.sale_routes import router as sale_router
from routes.user_routes import router as user_router

API_NAME = "Tech Inventory API"
API_VERSION = "1.0.0"
API_PREFIX = "/api/v1"

app = FastAPI(title=API_NAME, version=API_VERSION)

Base.metadata.create_all(bind=engine)
ensure_user_role_column()

app.include_router(user_router, prefix=API_PREFIX)
app.include_router(auth_router, prefix=API_PREFIX)
app.include_router(product_router, prefix=API_PREFIX)
app.include_router(inventory_movement_router, prefix=API_PREFIX)
app.include_router(sale_router, prefix=API_PREFIX)
app.include_router(report_router, prefix=API_PREFIX)

@app.get("/")
def root():
    return {"message": "API working"}


@app.get(f"{API_PREFIX}/version", tags=["Versioning"])
def get_api_version():
    return {"name": API_NAME, "version": API_VERSION}