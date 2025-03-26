
from src.database.database import session
from src.database.table_models.AmbientTemperature import AmbientTemperature


def create_temperature(temperature: int, time, location_ID: int) -> AmbientTemperature:
    temp = AmbientTemperature(temperature=temperature, time=time, location_ID=location_ID)
    session.add(temp)
    session.commit()
    session.refresh(temp)
    return temp

def get_temperature_by_id(temp_id: int) -> AmbientTemperature:
    return session.query(AmbientTemperature).filter(AmbientTemperature.id == temp_id).first()

def get_all_temperatures():
    return session.query(AmbientTemperature).all()

def update_temperature(temp_id: int, temperature: int = None, time=None) -> AmbientTemperature:
    temp = session.query(AmbientTemperature).filter(AmbientTemperature.id == temp_id).first()
    if not temp:
        return None
    if temperature is not None:
        temp.temperature = temperature
    if time is not None:
        temp.time = time
    session.commit()
    return temp

def delete_temperature(temp_id: int) -> bool:
    temp = session.query(AmbientTemperature).filter(AmbientTemperature.id == temp_id).first()
    if not temp:
        return False
    session.delete(temp)
    session.commit()
    return True