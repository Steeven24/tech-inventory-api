from fastapi import FastAPI

from core.database import Base, engine
from models.inventory_movement_model import InventoryMovement
from models.product_model import Product
from models.sale_model import Sale, SaleItem
from models.user_model import User
from routes.auth_routes import router as auth_router
from routes.inventory_movement_routes import router as inventory_movement_router
from routes.product_routes import router as product_router
from routes.sale_routes import router as sale_router
from routes.user_routes import router as user_router

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(user_router)
app.include_router(auth_router)
app.include_router(product_router)
app.include_router(inventory_movement_router)
app.include_router(sale_router)

@app.get("/")
def root():
    return {"message": "API working"}