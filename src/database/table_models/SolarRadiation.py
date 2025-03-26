from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from src.database.database import Base


class SolarRadiation(Base):
    __tablename__ = 'solar_radiations'
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    GT = Column(Float)
    time = Column(DateTime)
    location_ID = Column(Integer, ForeignKey('locations.id'))

    location = relationship("Location", back_populates="solar_radiations")