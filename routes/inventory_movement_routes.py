from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from core.database import get_db
from routes.auth_routes import get_current_user
from schemas.inventory_movement_schema import (
    InventoryMovementCreate,
    InventoryMovementResponse,
)
from services.inventory_movement_service import InventoryMovementService

router = APIRouter(prefix="/inventory-movements", tags=["Inventory Movements"])


@router.post("", response_model=InventoryMovementResponse, status_code=201)
def create_inventory_movement(
    movement_data: InventoryMovementCreate,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    movement_service = InventoryMovementService(db)
    try:
        return movement_service.create_movement(movement_data)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@router.get("", response_model=list[InventoryMovementResponse])
def get_inventory_movements(db: Session = Depends(get_db), _=Depends(get_current_user)):
    movement_service = InventoryMovementService(db)
    return movement_service.get_movements()


@router.get("/{movement_id}", response_model=InventoryMovementResponse)
def get_inventory_movement(
    movement_id: int,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    movement_service = InventoryMovementService(db)
    movement = movement_service.get_movement_by_id(movement_id)
    if movement is None:
        raise HTTPException(status_code=404, detail="Inventory movement not found")
    return movement


@router.get("/product/{product_id}", response_model=list[InventoryMovementResponse])
def get_inventory_movements_by_product(
    product_id: int,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    movement_service = InventoryMovementService(db)
    return movement_service.get_movements_by_product(product_id)