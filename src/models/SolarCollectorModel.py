
import math

class SolarCollectorModel:
    def __init__(self, area, Ut, Ub, Us, FR, tau_alpha_b, tau_alpha_d, tau_alpha):
        self.Ap = area
        self.Ut = Ut
        self.Ub = Ub
        self.Us = Us
        self.UL = Ut + Ub + Us
        self.FR = FR
        self.tau_alpha_b = tau_alpha_b
        self.tau_alpha_d = tau_alpha_d
        self.tau_alpha = tau_alpha


    def collector_efficiency(self, T_in, T_ambient, S):
        if S <= 0:
            return 0.0
        eta = self.FR * (1 - (self.UL * (T_in - T_ambient)) / S)
        return max(min(eta, 1.0), 0.0)


    def thermal_power_output(self, tau_alpha_b, tau_alpha_d, Ib, Id, tilt_angle_deg, T_in, T_ambient):
        K_theta = max(math.cos(math.radians(tilt_angle_deg)), 0)

        S = Ib * K_theta * tau_alpha_b + Id * tau_alpha_d

        Q_u = self.Ap * self.FR * (S - self.UL * (T_in - T_ambient))
        return max(Q_u, 0)