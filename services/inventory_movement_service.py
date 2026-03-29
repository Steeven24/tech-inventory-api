from sqlalchemy.orm import Session

from models.inventory_movement_model import InventoryMovement
from models.product_model import Product


class InventoryMovementService:
    def __init__(self, db: Session):
        self.db = db

    def _sanitize_movement(self, movement: InventoryMovement) -> dict:
        return {
            "id": movement.id,
            "product_id": movement.product_id,
            "movement_type": movement.movement_type,
            "quantity": movement.quantity,
            "note": movement.note,
            "created_at": movement.created_at,
        }

    def create_movement(self, movement_data):
        product = self.db.query(Product).filter(Product.id == movement_data.product_id).first()
        if product is None:
            raise ValueError("Product not found")

        if movement_data.movement_type == "out" and product.stock < movement_data.quantity:
            raise ValueError("Insufficient stock for this movement")

        if movement_data.movement_type == "in":
            product.stock += movement_data.quantity
        else:
            product.stock -= movement_data.quantity

        movement = InventoryMovement(
            product_id=movement_data.product_id,
            movement_type=movement_data.movement_type,
            quantity=movement_data.quantity,
            note=movement_data.note,
        )

        self.db.add(movement)
        self.db.commit()
        self.db.refresh(movement)
        return self._sanitize_movement(movement)

    def get_movements(self):
        movements = self.db.query(InventoryMovement).order_by(InventoryMovement.id.desc()).all()
        return [self._sanitize_movement(movement) for movement in movements]

    def get_movement_by_id(self, movement_id: int):
        movement = self.db.query(InventoryMovement).filter(InventoryMovement.id == movement_id).first()
        if movement is None:
            return None
        return self._sanitize_movement(movement)

    def get_movements_by_product(self, product_id: int):
        movements = (
            self.db.query(InventoryMovement)
            .filter(InventoryMovement.product_id == product_id)
            .order_by(InventoryMovement.id.desc())
            .all()
        )
        return [self._sanitize_movement(movement) for movement in movements]