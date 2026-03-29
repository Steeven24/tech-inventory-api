from sqlalchemy import Column, Float, Integer, String

from core.database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    brand = Column(String, nullable=False)
    sku = Column(String, unique=True, index=True, nullable=False)
    price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False, default=0)