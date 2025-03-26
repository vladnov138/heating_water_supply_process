class HeatTransferFluid:

    # Встроенные константы
    MASS_FLOW_RATE = 25.9           # кг/(м²·ч)
    SPECIFIC_HEAT_CAPACITY = 0.69   # Дж/(кг·°C)

    def __init__(self, Ta: float, Twater: float, Twater2: float):
        self.TFI = Ta                   # Температура на входе в СК (первичная)
        self.T1 = Twater + 5            # Температура теплоносителя на входе
        self.T2 = Twater2 + 5           # Температура теплоносителя на выходе

