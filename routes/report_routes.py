from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from core.database import get_db
from routes.auth_routes import require_roles
from schemas.report_schema import (
    DashboardOverviewResponse,
    LowStockProductResponse,
    SalesSummaryResponse,
    TopProductReportItem,
)
from services.report_service import ReportService

router = APIRouter(prefix="/reports", tags=["Reports"])


@router.get(
    "/dashboard-overview",
    response_model=DashboardOverviewResponse,
)
def get_dashboard_overview(
    db: Session = Depends(get_db),
    _=Depends(require_roles("admin")),
):
    report_service = ReportService(db)
    return report_service.get_dashboard_overview()


@router.get(
    "/sales-summary",
    response_model=SalesSummaryResponse,
)
def get_sales_summary(
    start_date: date | None = Query(default=None),
    end_date: date | None = Query(default=None),
    db: Session = Depends(get_db),
    _=Depends(require_roles("admin")),
):
    report_service = ReportService(db)
    return report_service.get_sales_summary(start_date=start_date, end_date=end_date)


@router.get(
    "/top-products",
    response_model=list[TopProductReportItem],
)
def get_top_products(
    limit: int = Query(default=5, ge=1, le=50),
    start_date: date | None = Query(default=None),
    end_date: date | None = Query(default=None),
    db: Session = Depends(get_db),
    _=Depends(require_roles("admin")),
):
    report_service = ReportService(db)
    return report_service.get_top_products(
        limit=limit,
        start_date=start_date,
        end_date=end_date,
    )


@router.get(
    "/low-stock",
    response_model=list[LowStockProductResponse],
)
def get_low_stock_products(
    threshold: int = Query(default=5, ge=0),
    db: Session = Depends(get_db),
    _=Depends(require_roles("admin")),
):
    report_service = ReportService(db)
    return report_service.get_low_stock_products(threshold=threshold)