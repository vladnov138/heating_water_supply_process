from datetime import datetime, date, time

from src.database.CRUD.AmblentTamperatureCRUD import create_temperature, get_all_temperatures
from src.database.CRUD.LocationCRUD import create_location, get_all_locations, update_location, get_location_data, \
    create_all_measurements
from src.database.CRUD.SolarRadiationCRUD import create_solar_radiation, get_all_solar
from src.database.CRUD.SunshineHoursCRUD import create_sunshine, get_all_sunshine
from src.database.database import Base, engine, session

# Создание таблиц (если их ещё нет)
Base.metadata.create_all(engine)

# Шаг 1: добавляем локацию
# Добавляем локацию
loc = create_location("Test City", 51.5074, -0.1278)

# Единый timestamp
now = datetime.now()

# Добавляем солнечную радиацию и температуру
result = create_all_measurements(
    location_ID=loc.id,
    timestamp=now,
    GT=312.7,
    temperature=22
)

print("Добавлена солнечная радиация:", result["solar"].GT)
print("Добавлена температура:", result["temperature"].temperature)

# Добавляем солнечные часы отдельно
from datetime import date, time

sun = create_sunshine(
    time=time(6, 0),
    start=date(2025, 3, 1),
    end=date(2025, 3, 31),
    location_ID=loc.id
)

print("Добавлены солнечные часы:", sun.start, "–", sun.end)


location_id = 1
start_time = datetime(2025, 3, 1)
end_time = datetime(2025, 3, 31)

data = get_location_data(location_id, start_time=start_time, end_time=end_time)

if data:
    print(f"Данные локации: {data['location'].name} в период {start_time.date()} — {end_time.date()}")

    print("\nСолнечная радиация в период:")
    for solar in data['solar_radiations']:
        print(f"  GT: {solar.GT}, Время: {solar.time}")

    print("\nТемпература в период:")
    for temp in data['ambient_temperatures']:
        print(f"  {temp.temperature}°C, Время: {temp.time}")

    print("\nСолнечные часы, перекрывающие период:")
    for sun in data['sunshine_hours']:
        print(f"  {sun.time}, с {sun.start} по {sun.end}")
else:
    print("Локация не найдена.")