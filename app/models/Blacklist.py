from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from ..db_conn import db

class Blacklist(db.Model):
    __tablename__ = 'blacklist'
    
    jti: Mapped[str] = mapped_column(String, primary_key=True)

    def __init__(self, jti):
        self.jti = jti

    def __repr__(self):
        return f"<Blacklist(jti={self.jti})>"