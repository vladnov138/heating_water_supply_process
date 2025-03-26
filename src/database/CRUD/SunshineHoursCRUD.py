
from src.database.database import session
from src.database.table_models.SunshineHours import SunshineHours


def create_sunshine(time, start, end, location_ID: int) -> SunshineHours:
    sun = SunshineHours(time=time, start=start, end=end, location_ID=location_ID)
    session.add(sun)
    session.commit()
    session.refresh(sun)
    return sun

def get_sunshine_by_id(sun_id: int) -> SunshineHours:
    return session.query(SunshineHours).filter(SunshineHours.id == sun_id).first()

def get_all_sunshine():
    return session.query(SunshineHours).all()

def update_sunshine(sun_id: int, time=None, start=None, end=None) -> SunshineHours:
    sun = session.query(SunshineHours).filter(SunshineHours.id == sun_id).first()
    if not sun:
        return None
    if time is not None:
        sun.time = time
    if start is not None:
        sun.start = start
    if end is not None:
        sun.end = end
    session.commit()
    return sun

def delete_sunshine(sun_id: int) -> bool:
    sun = session.query(SunshineHours).filter(SunshineHours.id == sun_id).first()
    if not sun:
        return False
    session.delete(sun)
    session.commit()
    return True
