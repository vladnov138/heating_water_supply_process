

class HeatStorageTank:
    HEAT_TRANSFER_COEFFICIENT = 0.5  # U, Вт/м²·°C
    VOLUME_LITERS = 100  # Объём, литров

    def __init__(self):
        self.U = self.HEAT_TRANSFER_COEFFICIENT
        self.volume_liters = self.VOLUME_LITERS
        self.volume_m3 = self.volume_liters / 1000  # Перевод в м³ при необходимости