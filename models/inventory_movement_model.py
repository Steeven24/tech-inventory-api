from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String

from core.database import Base


class InventoryMovement(Base):
    __tablename__ = "inventory_movements"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, index=True)
    movement_type = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    note = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)