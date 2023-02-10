from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from db.db_setup import Base

class Athlete(Base):
    __tablename__ = "athletes"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    license = Column(String, unique=True, nullable=False)
    birthday = Column(Date, nullable=False)
    category = Column(String, nullable=False)

    marks = relationship('Mark', back_populates='athlete')

class Mark(Base):
    __tablename__ = 'marks'

    id = Column(Integer, primary_key=True, index=True)
    value = Column(Integer) # In miliseconds or cents of a second
    date = Column(Date)
    event = Column(String)
    athlete_id = Column(Integer, ForeignKey('athletes.id'), nullable=False)

    athlete = relationship('Athlete', back_populates='marks')

class Event(Base):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    section = relationship('Section', back_populates='name')
    section_id = Column(Integer, ForeignKey('sections.id'), nullable=False)

class Section(Base):
    __tablename__ = 'sections'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)