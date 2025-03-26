
import math

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
