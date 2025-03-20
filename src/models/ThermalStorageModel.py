

class ThermalStorageModel:
    def __init__(self, U_lost, volume_liters):
        self.U_lost = U_lost
        self.V_m3 = volume_liters / 1000

