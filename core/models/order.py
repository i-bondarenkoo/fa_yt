from core.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from sqlalchemy import func

# from core.models.order_product_association import order_product_association_table
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.models.product import Product
    from core.models.order_product_association import OrderProductAssociation


class Order(Base):
    # __tablename__ = "orders"
    promocode: Mapped[str | None]
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), default=datetime.now
    )
    # products: Mapped[list["Product"]] = relationship(
    #     "Product",
    #     secondary="order_product_association",
    #     back_populates="orders",
    # )
    products_details: Mapped[list["OrderProductAssociation"]] = relationship(
        back_populates="order",
    )
