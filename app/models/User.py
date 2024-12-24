import uuid
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from ..db_conn import db

class User(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    # uuid: Mapped[str] = mapped_column(String, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)

    def __str__(self):
        return f"{{id: {self.id}, username: {self.username}, password: {self.password}, uuid: {self.uuid}}}"

    def as_dict(self):
        return {"id": self.id, "username": self.username, "uuid": self.uuid}