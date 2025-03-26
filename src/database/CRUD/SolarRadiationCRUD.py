
from src.database.database import session
from src.database.table_models.SolarRadiation import SolarRadiation


def create_solar_radiation(GT: float, time, location_ID: int) -> SolarRadiation:
    solar = SolarRadiation(GT=GT, time=time, location_ID=location_ID)
    session.add(solar)
    session.commit()
    session.refresh(solar)
    return solar

def get_solar_by_id(solar_id: int) -> SolarRadiation:
    return session.query(SolarRadiation).filter(SolarRadiation.id == solar_id).first()

def get_all_solar():
    return session.query(SolarRadiation).all()

def update_solar(solar_id: int, GT: float = None, time=None) -> SolarRadiation:
    solar = session.query(SolarRadiation).filter(SolarRadiation.id == solar_id).first()
    if not solar:
        return None
    if GT is not None:
        solar.GT = GT
    if time is not None:
        solar.time = time
    session.commit()
    return solar

def delete_solar(solar_id: int) -> bool:
    solar = session.query(SolarRadiation).filter(SolarRadiation.id == solar_id).first()
    if not solar:
        return False
    session.delete(solar)
    session.commit()
    return True