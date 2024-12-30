from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from ..db_conn import db
from datetime import datetime

class Refresh(db.Model):
    id: Mapped[int] = mapped_column(Integer)
    uuid : Mapped[str] = mapped_column(String)
    jti: Mapped[str] = mapped_column(String, nullable=False, primary_key=True)
    expires_at: Mapped[str] = mapped_column(String, nullable=False)


    #GET THE USER ID by UUID FROM USER TABLE, COMPARE THIS ID TO THE SUB IN THE AUTH JWT
    def is_expired(self):
        return datetime.now() > datetime.fromisoformat(self.expires_at)
    
    def __str__(self):
        return f"{{id: {self.id}, uuid: {self.user_uuid}, jti: {self.jti}}}"

    def as_dict(self):
        return {"id": self.id, "key": self.key}