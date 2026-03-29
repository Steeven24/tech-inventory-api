from sqlalchemy.orm import Session

from models.inventory_movement_model import InventoryMovement
from models.product_model import Product
from models.sale_model import Sale, SaleItem


class SaleService:
    def __init__(self, db: Session):
        self.db = db

    def _sanitize_sale(self, sale: Sale, items: list[SaleItem]) -> dict:
        return {
            "id": sale.id,
            "user_id": sale.user_id,
            "subtotal": sale.subtotal,
            "discount": sale.discount,
            "total": sale.total,
            "created_at": sale.created_at,
            "items": [
                {
                    "id": item.id,
                    "product_id": item.product_id,
                    "quantity": item.quantity,
                    "unit_price": item.unit_price,
                    "line_total": item.line_total,
                }
                for item in items
            ],
        }

    def create_sale(self, user_id: int, sale_data):
        product_map: dict[int, Product] = {}
        subtotal = 0.0

        for item in sale_data.items:
            product = self.db.query(Product).filter(Product.id == item.product_id).first()
            if product is None:
                raise ValueError(f"Product with id {item.product_id} not found")

            if product.stock < item.quantity:
                raise ValueError(f"Insufficient stock for product id {item.product_id}")

            product_map[item.product_id] = product
            subtotal += product.price * item.quantity

        total = subtotal - sale_data.discount
        if total < 0:
            raise ValueError("Discount cannot be greater than subtotal")

        sale = Sale(
            user_id=user_id,
            subtotal=subtotal,
            discount=sale_data.discount,
            total=total,
        )
        self.db.add(sale)
        self.db.flush()

        sale_items: list[SaleItem] = []

        for item in sale_data.items:
            product = product_map[item.product_id]
            product.stock -= item.quantity

            line_total = product.price * item.quantity
            sale_item = SaleItem(
                sale_id=sale.id,
                product_id=product.id,
                quantity=item.quantity,
                unit_price=product.price,
                line_total=line_total,
            )
            sale_items.append(sale_item)
            self.db.add(sale_item)

            movement = InventoryMovement(
                product_id=product.id,
                movement_type="out",
                quantity=item.quantity,
                note=f"Sale #{sale.id}",
            )
            self.db.add(movement)

        self.db.commit()

        self.db.refresh(sale)
        for item in sale_items:
            self.db.refresh(item)

        return self._sanitize_sale(sale, sale_items)

    def get_sales(self):
        sales = self.db.query(Sale).order_by(Sale.id.desc()).all()

        result = []
        for sale in sales:
            items = self.db.query(SaleItem).filter(SaleItem.sale_id == sale.id).all()
            result.append(self._sanitize_sale(sale, items))

        return result

    def get_sale_by_id(self, sale_id: int):
        sale = self.db.query(Sale).filter(Sale.id == sale_id).first()
        if sale is None:
            return None

        items = self.db.query(SaleItem).filter(SaleItem.sale_id == sale.id).all()
        return self._sanitize_sale(sale, items)
