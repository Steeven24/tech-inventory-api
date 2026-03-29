from sqlalchemy.orm import Session

from models.product_model import Product


class ProductService:
    def __init__(self, db: Session):
        self.db = db

    def _sanitize_product(self, product: Product) -> dict:
        return {
            "id": product.id,
            "name": product.name,
            "category": product.category,
            "brand": product.brand,
            "sku": product.sku,
            "price": product.price,
            "stock": product.stock,
        }

    def sku_exists(self, sku: str, exclude_product_id: int | None = None) -> bool:
        query = self.db.query(Product).filter(Product.sku.ilike(sku))

        if exclude_product_id is not None:
            query = query.filter(Product.id != exclude_product_id)

        return self.db.query(query.exists()).scalar()

    def create_product(self, product_data):
        if self.sku_exists(product_data.sku):
            raise ValueError("SKU already registered")

        product = Product(
            name=product_data.name,
            category=product_data.category,
            brand=product_data.brand,
            sku=product_data.sku,
            price=product_data.price,
            stock=product_data.stock,
        )

        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        return self._sanitize_product(product)

    def get_products(self):
        products = self.db.query(Product).all()
        return [self._sanitize_product(product) for product in products]

    def get_product_by_id(self, product_id: int):
        product = self.db.query(Product).filter(Product.id == product_id).first()
        if product is None:
            return None
        return self._sanitize_product(product)

    def update_product(self, product_id: int, product_data):
        product = self.db.query(Product).filter(Product.id == product_id).first()
        if product is None:
            return None

        if product_data.name is not None:
            product.name = product_data.name

        if product_data.category is not None:
            product.category = product_data.category

        if product_data.brand is not None:
            product.brand = product_data.brand

        if product_data.sku is not None:
            if self.sku_exists(product_data.sku, exclude_product_id=product_id):
                raise ValueError("SKU already registered")
            product.sku = product_data.sku

        if product_data.price is not None:
            product.price = product_data.price

        if product_data.stock is not None:
            product.stock = product_data.stock

        self.db.commit()
        self.db.refresh(product)
        return self._sanitize_product(product)

    def delete_product(self, product_id: int) -> bool:
        product = self.db.query(Product).filter(Product.id == product_id).first()
        if product is None:
            return False

        self.db.delete(product)
        self.db.commit()
        return True