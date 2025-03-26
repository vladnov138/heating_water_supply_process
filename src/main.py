from src.models.ClimateIndicatorModel import ClimateIndicatorsModel

file_path = "../data/data.xlsx"
hourly_df = ClimateIndicatorsModel.read_hourly_data(file_path)
daily_data = ClimateIndicatorsModel.calculate_daily_indicators(hourly_df)

# Вывод данных для первых 5 дней
for i, indicator in enumerate(daily_data[:5], start=1):
    print(f"День {i}: GT = {indicator.GT} Вт/м2, Ta = {indicator.Ta}, "
          f"Солнечных часов = {indicator.sunshine_hours}")
