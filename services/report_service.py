from datetime import date, datetime, time

from sqlalchemy import func
from sqlalchemy.orm import Session

from models.product_model import Product
from models.sale_model import Sale, SaleItem


class ReportService:
    def __init__(self, db: Session):
        self.db = db

    def _date_bounds(self, start_date: date | None, end_date: date | None):
        start_dt = datetime.combine(start_date, time.min) if start_date else None
        end_dt = datetime.combine(end_date, time.max) if end_date else None
        return start_dt, end_dt

    def _apply_sale_date_filter(self, query, start_date: date | None, end_date: date | None):
        start_dt, end_dt = self._date_bounds(start_date, end_date)

        if start_dt is not None:
            query = query.filter(Sale.created_at >= start_dt)

        if end_dt is not None:
            query = query.filter(Sale.created_at <= end_dt)

        return query

    def get_sales_summary(self, start_date: date | None = None, end_date: date | None = None):
        query = self.db.query(Sale)
        query = self._apply_sale_date_filter(query, start_date, end_date)

        sales_count = query.count()
        total_revenue = query.with_entities(func.coalesce(func.sum(Sale.total), 0.0)).scalar()
        average_ticket = (total_revenue / sales_count) if sales_count > 0 else 0.0

        return {
            "start_date": start_date,
            "end_date": end_date,
            "sales_count": sales_count,
            "total_revenue": float(total_revenue),
            "average_ticket": float(average_ticket),
        }

    def get_top_products(self, limit: int = 5, start_date: date | None = None, end_date: date | None = None):
        query = (
            self.db.query(
                Product.id.label("product_id"),
                Product.name,
                Product.sku,
                func.coalesce(func.sum(SaleItem.quantity), 0).label("total_quantity"),
                func.coalesce(func.sum(SaleItem.line_total), 0.0).label("total_revenue"),
            )
            .join(SaleItem, SaleItem.product_id == Product.id)
            .join(Sale, Sale.id == SaleItem.sale_id)
        )

        query = self._apply_sale_date_filter(query, start_date, end_date)
        query = query.group_by(Product.id, Product.name, Product.sku)
        query = query.order_by(func.sum(SaleItem.quantity).desc()).limit(limit)

        rows = query.all()

        return [
            {
                "product_id": row.product_id,
                "name": row.name,
                "sku": row.sku,
                "total_quantity": int(row.total_quantity),
                "total_revenue": float(row.total_revenue),
            }
            for row in rows
        ]

    def get_low_stock_products(self, threshold: int = 5):
        products = (
            self.db.query(Product)
            .filter(Product.stock <= threshold)
            .order_by(Product.stock.asc(), Product.name.asc())
            .all()
        )

        return [
            {
                "id": product.id,
                "name": product.name,
                "sku": product.sku,
                "category": product.category,
                "brand": product.brand,
                "stock": product.stock,
            }
            for product in products
        ]

    def get_dashboard_overview(self):
        today = date.today()
        start_today = datetime.combine(today, time.min)
        end_today = datetime.combine(today, time.max)

        products_count = self.db.query(Product).count()
        total_stock_units = self.db.query(func.coalesce(func.sum(Product.stock), 0)).scalar()
        low_stock_count = self.db.query(Product).filter(Product.stock <= 5).count()

        sales_count = self.db.query(Sale).count()
        total_revenue = self.db.query(func.coalesce(func.sum(Sale.total), 0.0)).scalar()

        today_sales_query = self.db.query(Sale).filter(
            Sale.created_at >= start_today,
            Sale.created_at <= end_today,
        )
        today_sales_count = today_sales_query.count()
        today_revenue = today_sales_query.with_entities(
            func.coalesce(func.sum(Sale.total), 0.0)
        ).scalar()

        return {
            "products_count": products_count,
            "total_stock_units": int(total_stock_units),
            "low_stock_count": low_stock_count,
            "sales_count": sales_count,
            "total_revenue": float(total_revenue),
            "today_sales_count": today_sales_count,
            "today_revenue": float(today_revenue),
        }