

class HeatStorageTank:
    HEAT_TRANSFER_COEFFICIENT = 0.5  # U, Вт/м²·°C
    VOLUME_LITERS = 300              # Объём бака в литрах
    CP = 4186                        # Дж/(кг·°C)
    DENSITY = 1000                   # кг/м³
    SURFACE_AREA = 2.0              # м² — площадь теплообмена

    def __init__(self):
        self.U = self.HEAT_TRANSFER_COEFFICIENT
        self.volume_liters = self.VOLUME_LITERS
        self.volume_m3 = self.volume_liters / 1000
        self.cp = self.CP
        self.rho = self.DENSITY
        self.surface_area = self.SURFACE_AREA
        self.mass = self.volume_m3 * self.rho

    # Q_loss - Теплопотери бака
    def calc_q_loss(self, T_tank, T_ambient):
        return self.U * self.surface_area * (T_tank - T_ambient)

    # Q_load - Энергия, отбираемая потребителем
    def calc_q_load(self, G_load_m3s, T_tank, T_water):
        return self.cp * self.rho * G_load_m3s * (T_tank - T_water)

    def update_temperature(
            self,
            T_tank: float,  # текущая температура воды в баке (°C)
            QI: float,  # поступающая тепловая энергия от солнечного коллектора (Вт);
            T_water: float,  # температура воды, которую хочет потребитель
            T_ambient: float,  # температура воздуха снаружи бака
            V_load_liters: float,  # объем воды, потребляемый за час (литры)
            delta_t: float = 3600  # период времени (1 час = 3600 сек)
    ) -> tuple[float, float, float]:
        G_load = (V_load_liters / 1000) / delta_t  # м³/с

        Q_load = self.calc_q_load(G_load, T_tank, T_water)
        Q_loss = self.calc_q_loss(T_tank, T_ambient)

        # dT/dt по итоговому уравнению
        dT = (QI - Q_load - Q_loss) * delta_t / (self.mass * self.cp)
        T_new = T_tank + dT

        return T_new, Q_loss, Q_load