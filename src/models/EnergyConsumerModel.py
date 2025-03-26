

class EnergyConsumption:
    # Встроенные константы
    DAILY_WATER_USAGE = 100       # л/день
    COLD_WATER_TEMP = 10          # Tхол, °C
    HOT_WATER_TEMP = 60           # Tгор, °C
    SPECIFIC_HEAT_WATER = 4186    # Дж/(кг·°C), теплоемкость воды

    def __init__(self):
        self.daily_water_usage_liters = self.DAILY_WATER_USAGE
        self.T_cold = self.COLD_WATER_TEMP
        self.T_hot = self.HOT_WATER_TEMP

        # Перевод объема в массу: 1 л воды ≈ 1 кг
        self.mass_of_water = self.daily_water_usage_liters  # кг


    def calculate_daily_energy_demand(self) -> float:
        delta_T = self.T_hot - self.T_cold
        energy_joules = self.mass_of_water * self.SPECIFIC_HEAT_WATER * delta_T
        energy_kWh = energy_joules / 3_600_000  # Перевод из Дж в кВт·ч
        return energy_kWh