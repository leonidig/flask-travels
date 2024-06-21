from .. import Base
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from flask_login import UserMixin


class User(Base):
    __tablename__ = 'users'
    email: Mapped[str]
    nickname: Mapped[str]
    password: Mapped[str]


    def is_active(self) -> bool:
        return True
    def is_authenticated(self) -> bool:
        return True
    def is_anonymous(self)->bool:
        return False
    def get_id(self)->str:
        return f"{self.id}"