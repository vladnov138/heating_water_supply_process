from src.models.ClimateIndicatorModel import ClimateIndicatorsModel
from src.models.HeatStorageTank import HeatStorageTank
from src.models.SolarCollectorModel import SolarCollectorSpecs

# file_path = "../data/data.xlsx"
# hourly_df = ClimateIndicatorsModel.read_hourly_data(file_path)
# daily_data = ClimateIndicatorsModel.calculate_daily_indicators(hourly_df)
#
# # Вывод данных для первых 5 дней
# for i, indicator in enumerate(daily_data[:5], start=1):
#     print(f"День {i}: GT = {indicator.GT} Вт/м2, Ta = {indicator.Ta}, "
#           f"Солнечных часов = {indicator.sunshine_hours}")
#

# решение задачи
specs = SolarCollectorSpecs()
tank = HeatStorageTank()


# Начальные данные
Ttank = 40  # начальная температура воды в баке

# Метео и параметры
Ib1 = 800
Id1 = 150
rb, rd, rr = 1.0, 0.2, 0.1
tau_alfa_b, tau_alfa_d, tau_alfa = 0.9, 0.85, 0.92
Ta1 = 20       # температура окружающей среды
TFI = 30       # вход теплоносителя
Cp = 4186
Massa = 50     # кг
Twater = 30
Twater2 = 60

# Потребление
V_load_liters = 100  # литров в час
T_water = 35         # требуемая температура воды потребителем

# Расчёт
result = specs.simulate_hour(
    Ib1, Id1, rb, rd, rr,
    tau_alfa_b, tau_alfa_d, tau_alfa,
    Ta1, TFI, Cp, Massa,
    Twater, Twater2,
    Ttank,
    heat_storage_tank=tank,
    V_load_liters=V_load_liters,
    T_water=T_water
)

# Вывод результатов
print(f"QI (поступающая энергия): {result['QI']:.2f} Вт")
print(f"QU (полезная энергия): {result['QU']:.2f} Вт")
print(f"КПД: {result['KPD_hourly'] * 100:.2f} %")
print(f"Потери бака Q_loss: {result['Q_loss']:.2f} Вт")
print(f"Потребление Q_load: {result['Q_load']:.2f} Вт")
print(f"Температура бака после часа: {result['Ttank_new']:.2f} °C")


# Инициализация
Ttank = 40  # начальная температура
temps = []

# Прогон симуляции на 10 часов
for hour in range(10):
    result = specs.simulate_hour(
        Ib1=800, Id1=150, rb=1.0, rd=0.2, rr=0.1,
        tau_alfa_b=0.9, tau_alfa_d=0.85, tau_alfa=0.92,
        Ta1=20, TFI=30, Cp=4186, Massa=50,
        Twater=30, Twater2=60,
        Ttank=Ttank,
        heat_storage_tank=tank,
        V_load_liters=100,
        T_water=35
    )

    Ttank = result["Ttank_new"]  # обновляем для следующего часа
    temps.append(Ttank)

# Результаты
for i, t in enumerate(temps):
    print(f"Час {i+1}: Ttank = {t:.2f} °C")