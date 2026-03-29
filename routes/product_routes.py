from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from core.database import get_db
from routes.auth_routes import get_current_user, require_roles
from schemas.product_schema import ProductCreate, ProductResponse, ProductUpdate
from services.product_service import ProductService

router = APIRouter(prefix="/products", tags=["Products"])


@router.post("", response_model=ProductResponse, status_code=201)
def create_product(
    product_data: ProductCreate,
    db: Session = Depends(get_db),
    _=Depends(require_roles("admin", "warehouse")),
):
    product_service = ProductService(db)
    try:
        return product_service.create_product(product_data)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@router.get("", response_model=list[ProductResponse])
def get_products(db: Session = Depends(get_db), _=Depends(get_current_user)):
    product_service = ProductService(db)
    return product_service.get_products()


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    product_service = ProductService(db)
    product = product_service.get_product_by_id(product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    product_data: ProductUpdate,
    db: Session = Depends(get_db),
    _=Depends(require_roles("admin", "warehouse")),
):
    product_service = ProductService(db)
    try:
        product = product_service.update_product(product_id, product_data)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error

    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.delete("/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    _=Depends(require_roles("admin", "warehouse")),
):
    product_service = ProductService(db)
    deleted = product_service.delete_product(product_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted successfully"}