from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from ..db_conn import db
import datetime

class Connection(db.Model):
    id: Mapped[int] = mapped_column(Integer)
    key: Mapped[str] = mapped_column(String, nullable=False, primary_key=True)
    expires_at: Mapped[str] = mapped_column(String)
    

    def __str__(self):
        return f"{{id: {self.id}, key: {self.key}}}"

    def as_dict(self):
        return {"id": self.id, "key": self.key}
    
    def is_expired(self):
        return datetime.now() > datetime.fromisoformat(self.expires_at)