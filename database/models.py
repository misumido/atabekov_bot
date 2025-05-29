from sqlalchemy import (Column, Integer,
                        String, DateTime)
from database import Base

class User(Base):
    __tablename__ = "user"
    user_id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    tg_id = Column(Integer, unique=True)
    phone_number = Column(String)
    language = Column(String)
    reg_date = Column(DateTime)

class Promos(Base):
    __tablename__ = "promos"
    promo_id = Column(Integer, primary_key=True, autoincrement=True)
    promocode = Column(String, unique=True)
    owner = Column(Integer, nullable=True)
    promo_reg_date = Column(DateTime, nullable=True)




