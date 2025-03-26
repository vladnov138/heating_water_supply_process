
import pandas as pd


class SolarCollectorSpecs:
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
