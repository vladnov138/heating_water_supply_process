
from src.database.database import session
from src.database.table_models.AmbientTemperature import AmbientTemperature
from src.database.table_models.Location import Location
from src.database.table_models.SolarRadiation import SolarRadiation
from src.database.table_models.SunshineHours import SunshineHours


def create_location(name: str, latitude: float, longitude: float) -> Location:
    location = Location(name=name, latitude=latitude, longitude=longitude)
    session.add(location)
    session.commit()
    session.refresh(location)
    return location

def get_location_by_id(location_id: int) -> Location:
    return session.query(Location).filter(Location.id == location_id).first()

def get_all_locations():
    return session.query(Location).all()

def update_location(location_id: int, name: str = None, latitude: float = None, longitude: float = None) -> Location:
    location = session.query(Location).filter(Location.id == location_id).first()
    if not location:
        return None
    if name is not None:
        location.name = name
    if latitude is not None:
        location.latitude = latitude
    if longitude is not None:
        location.longitude = longitude
    session.commit()
    return location

def delete_location(location_id: int) -> bool:
    location = session.query(Location).filter(Location.id == location_id).first()
    if not location:
        return False
    session.delete(location)
    session.commit()
    return True


def get_location_data(location_id: int, start_time=None, end_time=None):
    location = session.query(Location).filter(Location.id == location_id).first()
    if not location:
        return None

    solar_query = session.query(SolarRadiation).filter(SolarRadiation.location_ID == location_id)
    temp_query = session.query(AmbientTemperature).filter(AmbientTemperature.location_ID == location_id)
    sunshine_query = session.query(SunshineHours).filter(SunshineHours.location_ID == location_id)

    if start_time and end_time:
        solar_query = solar_query.filter(SolarRadiation.time.between(start_time, end_time))
        temp_query = temp_query.filter(AmbientTemperature.time.between(start_time, end_time))
        sunshine_query = sunshine_query.filter(SunshineHours.start <= end_time, SunshineHours.end >= start_time)

    return {
        "location": location,
        "solar_radiations": solar_query.all(),
        "ambient_temperatures": temp_query.all(),
        "sunshine_hours": sunshine_query.all()
    }


def create_all_measurements(location_ID: int, timestamp, GT: float, temperature: int):
    solar = SolarRadiation(GT=GT, time=timestamp, location_ID=location_ID)
    temp = AmbientTemperature(temperature=temperature, time=timestamp, location_ID=location_ID)

    session.add_all([solar, temp])
    session.commit()
    return {
        "solar": solar,
        "temperature": temp
    }