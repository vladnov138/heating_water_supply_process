# Природно климатические показатели
import pandas as pd


class ClimateIndicatorsModel:
    GT: float             # Интенсивность солнечной радиации
    Ta: float             # Температура окружающей среды
    sunshine_hours: float # Кол-во солнечных часов

    def __init__(self, GT, Ta, sunshine_hours):
        self.GT = GT
        self.Ta = Ta
        self.sunshine_hours = sunshine_hours


    @staticmethod
    def calculate_daily_indicators(hourly_df: pd.DataFrame, radiation_threshold: float = 50) -> list:
        num_days = len(hourly_df) // 24
        daily_indicators = []

        for day in range(num_days):
            day_data = hourly_df.iloc[day * 24:(day + 1) * 24]
            GT = day_data['total'].mean()
            Ta = day_data['temperature'].mean()
            # Считаем часы, когда суммарная радиация превышает заданный порог
            sunshine_hours = int((day_data['total'] > radiation_threshold).sum())
            daily_indicators.append(
                ClimateIndicatorsModel(GT=GT, Ta=Ta, sunshine_hours=sunshine_hours)
            )

        return daily_indicators