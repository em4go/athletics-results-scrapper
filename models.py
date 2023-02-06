from sqlalchemy import Column, Integer, String, Float
from database import Base

class Athlete(Base):
    __tablename__ = "athletes"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    license = Column(String, unique=True)
    birthday = Column(String)
    category = Column(String)

class Mark(Base):
    __tablename__ = 'marks'
    id = Column(Integer, primary_key=True, index=True)
    value = Column(Float) # In seconds / meters