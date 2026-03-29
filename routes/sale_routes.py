from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from core.database import get_db
from routes.auth_routes import get_current_user
from schemas.sale_schema import SaleCreate, SaleResponse
from services.sale_service import SaleService

router = APIRouter(prefix="/sales", tags=["Sales"])


@router.post("", response_model=SaleResponse, status_code=201)
def create_sale(
    sale_data: SaleCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    sale_service = SaleService(db)
    try:
        return sale_service.create_sale(current_user.id, sale_data)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@router.get("", response_model=list[SaleResponse])
def get_sales(db: Session = Depends(get_db), _=Depends(get_current_user)):
    sale_service = SaleService(db)
    return sale_service.get_sales()


@router.get("/{sale_id}", response_model=SaleResponse)
def get_sale(sale_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    sale_service = SaleService(db)
    sale = sale_service.get_sale_by_id(sale_id)
    if sale is None:
        raise HTTPException(status_code=404, detail="Sale not found")
    return sale
