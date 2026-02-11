from core.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

# from core.models.order_product_association import order_product_association_table
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.models.order import Order
    from core.models.order_product_association import OrderProductAssociation


class Product(Base):
    # __tablename__ = "products"
    name: Mapped[str]
    description: Mapped[str]
    price: Mapped[int]

    # orders: Mapped[list["Order"]] = relationship(
    #     "Order",
    #     secondary="order_product_association",
    #     back_populates="products",
    # )
    orders_details: Mapped[list["OrderProductAssociation"]] = relationship(
        back_populates="product",
    )
