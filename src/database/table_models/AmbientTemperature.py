from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from src.database.database import Base


class AmbientTemperature(Base):
    __tablename__ = 'ambient_temperature'
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    temperature = Column(Integer)
    time = Column(DateTime)
    location_ID = Column(Integer, ForeignKey('locations.id'))

    location = relationship("Location", back_populates="ambient_temperatures")