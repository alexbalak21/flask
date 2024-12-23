from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db_conn import db

class Article(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    content: Mapped[str] = mapped_column(nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)

    user = relationship("User", back_populates="articles")

    def __str__(self):
        return f"{{id: {self.id}, title: {self.title}, content: {self.content}, user_id: {self.user_id}}}"

    def as_dict(self):
        return {"id": self.id, "title": self.title, "content": self.content, "user_id": self.user_id}