from core.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column


class Product(Base):
    name: Mapped[str]
    description: Mapped[str]
    price: Mapped[int]
