from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from core.models.base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.models.post import Post
    from core.models.profile import Profile


class User(Base):
    username: Mapped[str] = mapped_column(String(35), unique=True)

    posts: Mapped[list["Post"]] = relationship("Post", back_populates="user")
    profile: Mapped["Profile"] = relationship("Profile", back_populates="user")

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id!r}, username={self.username!r})"

    def __repr__(self):
        return str(self)
