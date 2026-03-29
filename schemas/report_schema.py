from datetime import date

from pydantic import BaseModel


class SalesSummaryResponse(BaseModel):
    start_date: date | None
    end_date: date | None
    sales_count: int
    total_revenue: float
    average_ticket: float


class TopProductReportItem(BaseModel):
    product_id: int
    name: str
    sku: str
    total_quantity: int
    total_revenue: float


class LowStockProductResponse(BaseModel):
    id: int
    name: str
    sku: str
    category: str
    brand: str
    stock: int


class DashboardOverviewResponse(BaseModel):
    products_count: int
    total_stock_units: int
    low_stock_count: int
    sales_count: int
    total_revenue: float
    today_sales_count: int
    today_revenue: float