
import pandas as pd


class SolarCollectorSpecs:
    FR = 0.95

    def __init__(
        self,
        Ut: float = 2.889,
        Ub: float = 0.017,
        Us: float = 0.005,
        transmittance: float = 0.97,
        absorptance: float = 0.95,
        area: float = 4
    ):
        self.Ut = Ut
        self.Ub = Ub
        self.Us = Us
        self.UL = Ut + Ub + Us  # Общий коэффициент теплопередачи
        self.transmittance = transmittance
        self.absorptance = absorptance
        self.area = area

    @staticmethod
    def read_hourly_data(file_path: str) -> pd.DataFrame:
        df = pd.read_excel(file_path)
        df = df.rename(columns={
            'Прямая, Вт/м2': 'direct',
            'Рассеянная, Вт/м2': 'diffuse',
            'Суммарная, Вт/м2': 'total',
            'Температура, Град. Ц.': 'temperature'
        })

        return df

    @staticmethod
    def from_hourly_data(file_path: str):
        df = pd.read_excel(file_path)
        df = df.rename(columns={
            'Прямая, Вт/м2': 'direct',
            'Рассеянная, Вт/м2': 'diffuse',
            'Суммарная, Вт/м2': 'total',
            'Температура, Град. Ц.': 'temperature'
        })

        return SolarCollectorSpecs(Ut=df["direct"], Ub=df["diffuse"], Us=df["total"])

    # IT Суммарная радиация на СК, Вт / м2
    def calc_total_radiation(self, Ib1, Id1, rb, rd, rr):
        return Ib1 * rb + Id1 * rd + (Ib1 + Id1) * rr

    # Приведенная интенсивность, Вт / м2
    def calc_effective_intensity(self, Ib1, Id1, rb, rd, rr, tau_alfa_b, tau_alfa_d):
        return Ib1 * rb * tau_alfa_b + (Id1 * rd + (Ib1 + Id1) * rr) * tau_alfa_d

    # Tpm Равновесная температура, Град. Ц.
    def calc_equilibrium_temp(self, S, Ta1):
        return (S / self.UL) + Ta1

    # Тепловая мощность коллектора, Вт
    def calc_thermal_power(self, IT, tau_alfa):
        return IT * tau_alfa * self.area

    # QI Скорость потерь тепла
    def calc_losses(self, Tpm, Ta1):
        Qt = self.Ut * self.area * (Tpm - Ta1)
        Qs = self.Us * self.area * (Tpm - Ta1)
        Qb = self.Ub * self.area * (Tpm - Ta1)
        return Qt + Qs + Qb

    # QU Полезная энергия
    def calc_useful_energy(self, QI, Ql):
        return QI - Ql

    # TFO Производительность коллектора (литры в час)
    def calc_output_temp(self, QU, TFI, Massa, Cp):
        return TFI + ((QU / Massa) * Cp)

    # KPD_hourly Температура теплоносителя на выходе из коллектора
    def calc_efficiency(self, QU, IT):
        return QU / (self.area * IT)

    # V_ac Расчет бака накопителя
    def calc_productivity(self, QU, Cp, Massa, Twater2, Twater):
        return QU / (Cp * Massa * (Twater2 - Twater))

    # Энергия, поступающая от солнечного коллектора:
    def calc_tin(self, QU, TFI, Massa, Cp):
        return TFI + (QU / (Massa * Cp))

    def calc_qin(self, Tin, Ttank, Massa, Cp):
        return Massa * Cp * (Tin - Ttank)


    def calculate_hourly_performance(
            self,
            Ib1, Id1, rb, rd, rr,
            tau_alfa_b, tau_alfa_d,
            tau_alfa,
            Ta1, TFI, Cp, Massa,
            Twater, Twater2,
            Ttank  # температура воды в баке
    ):
        IT = self.calc_total_radiation(Ib1, Id1, rb, rd, rr)
        S = self.calc_effective_intensity(Ib1, Id1, rb, rd, rr, tau_alfa_b, tau_alfa_d)
        Tpm = self.calc_equilibrium_temp(S, Ta1)
        QI = self.calc_thermal_power(IT, tau_alfa)
        Ql = self.calc_losses(Tpm, Ta1)
        QU = self.calc_useful_energy(QI, Ql)
        TFO = self.calc_output_temp(QU, TFI, Massa, Cp)
        KPD_hourly = self.calc_efficiency(QU, IT)
        g_collector = self.calc_productivity(QU, Cp, Massa, Twater2, Twater)

        Tin = self.calc_tin(QU, TFI, Massa, Cp)
        Qin = self.calc_qin(Tin, Ttank, Massa, Cp)


        return {
            "IT": IT,
            "S": S,
            "Tpm": Tpm,
            "QI": QI,
            "Ql": Ql,
            "QU": QU,
            "TFO": TFO,
            "KPD_hourly": KPD_hourly,
            "g_collector": g_collector,
            "Tin": Tin,
            "Qin": Qin,
        }


    def simulate_hour(
            self,
            Ib1, Id1, rb, rd, rr,
            tau_alfa_b, tau_alfa_d,
            tau_alfa,
            Ta1, TFI, Cp, Massa,
            Twater, Twater2,
            Ttank,
            heat_storage_tank,  # объект HeatStorageTank
            V_load_liters,  # объем забора воды за час
            T_water  # желаемая температура потребителя
    ):
        # 1. Расчёты от коллектора
        performance = self.calculate_hourly_performance(
            Ib1, Id1, rb, rd, rr,
            tau_alfa_b, tau_alfa_d,
            tau_alfa,
            Ta1, TFI, Cp, Massa,
            Twater, Twater2,
            Ttank
        )

        QI = performance["QI"]

        # 2. Расчёты по баку
        Ttank_new, Q_loss, Q_load = heat_storage_tank.update_temperature(
            T_tank=Ttank,
            QI=QI,
            T_water=T_water,
            T_ambient=Ta1,
            V_load_liters=V_load_liters
        )

        # 3. Возвращаем объединённый результат
        return {
            **performance,
            "Ttank_new": Ttank_new,
            "Q_loss": Q_loss,
            "Q_load": Q_load
        }
