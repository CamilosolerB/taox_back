from sqlalchemy.orm import Session
from app.domain.entities.product_model import Product
from app.domain.ports.out.product_repository import ProductRepository
from app.infrastructure.db.models.products_orm import Product as ProductORM


class ProductORMRepository(ProductRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_all_products(self) -> list[Product]:
        products = self.session.query(ProductORM).all()
        return [
            Product(
                id_product=product.id_product,
                name=product.name,
                generic_name=product.generic_name,
                price=float(product.price),
                unit_measure=product.unit_measure,
                unit_price=float(product.unit_price),
                min_unit_price=float(product.min_unit_price),
                lead_time_days=int(product.lead_time_days),
                restorage=product.restorage,
                company_id=product.company_id
            )
            for product in products
        ]

    def get_product_by_id(self, id_product: str) -> Product:
        product = self.session.query(ProductORM).filter(ProductORM.id_product == id_product).first()
        if product is None:
            return None
        return Product(
            id_product=product.id_product,
            name=product.name,
            generic_name=product.generic_name,
            price=float(product.price),
            unit_measure=product.unit_measure,
            unit_price=float(product.unit_price),
            min_unit_price=float(product.min_unit_price),
            lead_time_days=int(product.lead_time_days),
            restorage=product.restorage,
            company_id=product.company_id
        )

    def get_products_by_company_id(self, company_id: str) -> list[Product]:
        products = self.session.query(ProductORM).filter(ProductORM.company_id == company_id).all()
        return [
            Product(
                id_product=product.id_product,
                name=product.name,
                generic_name=product.generic_name,
                price=float(product.price),
                unit_measure=product.unit_measure,
                unit_price=float(product.unit_price),
                min_unit_price=float(product.min_unit_price),
                lead_time_days=int(product.lead_time_days),
                restorage=product.restorage,
                company_id=product.company_id
            )
            for product in products
        ]

    def create_product(self, product: Product) -> Product:
        product_orm = ProductORM(
            id_product=product.id_product,
            name=product.name,
            generic_name=product.generic_name,
            price=str(product.price),
            unit_measure=product.unit_measure,
            unit_price=str(product.unit_price),
            min_unit_price=str(product.min_unit_price),
            lead_time_days=str(product.lead_time_days),
            restorage=product.restorage,
            company_id=product.company_id
        )
        self.session.add(product_orm)
        self.session.commit()
        self.session.refresh(product_orm)
        return Product(
            id_product=product_orm.id_product,
            name=product_orm.name,
            generic_name=product_orm.generic_name,
            price=float(product_orm.price),
            unit_measure=product_orm.unit_measure,
            unit_price=float(product_orm.unit_price),
            min_unit_price=float(product_orm.min_unit_price),
            lead_time_days=int(product_orm.lead_time_days),
            restorage=product_orm.restorage,
            company_id=product_orm.company_id
        )

    def update_product(self, id_product: str, product_data: dict) -> Product:
        product_orm = self.session.query(ProductORM).filter(ProductORM.id_product == id_product).first()
        if product_orm is None:
            return None
        for key, value in product_data.items():
            if value is not None:
                # Convert numeric fields to string for ORM storage
                if key in ['price', 'unit_price', 'min_unit_price', 'lead_time_days']:
                    setattr(product_orm, key, str(value))
                else:
                    setattr(product_orm, key, value)
        self.session.commit()
        self.session.refresh(product_orm)
        return Product(
            id_product=product_orm.id_product,
            name=product_orm.name,
            generic_name=product_orm.generic_name,
            price=float(product_orm.price),
            unit_measure=product_orm.unit_measure,
            unit_price=float(product_orm.unit_price),
            min_unit_price=float(product_orm.min_unit_price),
            lead_time_days=int(product_orm.lead_time_days),
            restorage=product_orm.restorage,
            company_id=product_orm.company_id
        )

    def delete_product(self, id_product: str) -> None:
        product_orm = self.session.query(ProductORM).filter(ProductORM.id_product == id_product).first()
        if product_orm:
            self.session.delete(product_orm)
            self.session.commit()
