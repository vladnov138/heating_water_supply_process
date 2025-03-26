from sqlalchemy import Column, Integer, Time, Date, ForeignKey
from sqlalchemy.orm import relationship

from src.database.database import Base


class SunshineHours(Base):
    __tablename__ = 'sunshine_hours'
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    time = Column(Time)
    start = Column(Date)
    end = Column(Date)
    location_ID = Column(Integer, ForeignKey('locations.id'))

    location = relationship("Location", back_populates="sunshine_hours")