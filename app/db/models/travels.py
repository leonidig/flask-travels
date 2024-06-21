# from typing import List
from .. import Base
from sqlalchemy.orm import Mapped


from datetime import date



class Travel(Base):
    __tablename__ = "travels"

    title: Mapped[str]
    description: Mapped[str]
    start_date: Mapped[date]
    end_date: Mapped[date]
    price: Mapped[float]
#   photo: Mapped[str] = mapped_column(nullable=True)
#   cities: Mapped[List]
