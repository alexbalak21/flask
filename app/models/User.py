from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from ..db import db


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] = mapped_column(nullable=False)
    # email: Mapped[str]

    def __str__(self):
        return "{" + f"id:{self.id}, username:{self.username}, password:{self.password}" + "}"

    # def as_dict(self):
    #     return {c.name: getattr(self, c.name)
    #             for c in self.__table__.columns}

    def as_dict(self):
        return {"id": self.id, "username": self.username}
