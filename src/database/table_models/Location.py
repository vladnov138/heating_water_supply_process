from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship

from src.database.database import Base


class Location(Base):
    __tablename__ = 'locations'
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    name = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)

    solar_radiations = relationship("SolarRadiation", back_populates="location")
    ambient_temperatures = relationship("AmbientTemperature", back_populates="location")
    sunshine_hours = relationship("SunshineHours", back_populates="location")