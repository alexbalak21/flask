from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from ..db_conn import db

class Connection(db.Model):
    id: Mapped[int] = mapped_column(Integer)
    key: Mapped[str] = mapped_column(String, nullable=False)

    def __str__(self):
        return f"{{id: {self.id}, key: {self.key}}}"

    def as_dict(self):
        return {"id": self.id, "key": self.key}