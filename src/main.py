import sys

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from scipy.optimize import linprog
from PyQt5 import QtWidgets, QtCore
from src.models.HeatStorageTank import HeatStorageTank
from src.models.SolarCollectorModel import SolarCollectorSpecs


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Солнечный коллектор: оптимизация и симуляция")
        self.initUI()

    def initUI(self):
        centralWidget = QtWidgets.QWidget(self)
        self.setCentralWidget(centralWidget)

        # Основной горизонтальный layout
        mainLayout = QtWidgets.QHBoxLayout(centralWidget)

        # Панель слева с параметрами (формат: форма)
        self.paramPanel = QtWidgets.QWidget()
        paramLayout = QtWidgets.QFormLayout(self.paramPanel)

        self.ibSpin = QtWidgets.QDoubleSpinBox()
        self.ibSpin.setRange(0, 2000)
        self.ibSpin.setValue(800)
        paramLayout.addRow("Прямая радиация Ib:", self.ibSpin)

        self.idSpin = QtWidgets.QDoubleSpinBox()
        self.idSpin.setRange(0, 1000)
        self.idSpin.setValue(150)
        paramLayout.addRow("Рассеянная радиация Id:", self.idSpin)

        self.rbSpin = QtWidgets.QDoubleSpinBox()
        self.rbSpin.setRange(0, 2)
        self.rbSpin.setValue(1.0)
        paramLayout.addRow("Коэф. rb:", self.rbSpin)

        self.rdSpin = QtWidgets.QDoubleSpinBox()
        self.rdSpin.setRange(0, 2)
        self.rdSpin.setValue(0.2)
        paramLayout.addRow("Коэф. rd:", self.rdSpin)

        self.rrSpin = QtWidgets.QDoubleSpinBox()
        self.rrSpin.setRange(0, 2)
        self.rrSpin.setValue(0.1)
        paramLayout.addRow("Коэф. rr:", self.rrSpin)

        self.tauAlfaBSpin = QtWidgets.QDoubleSpinBox()
        self.tauAlfaBSpin.setRange(0, 1)
        self.tauAlfaBSpin.setValue(0.9)
        paramLayout.addRow("tau_alfa_b:", self.tauAlfaBSpin)

        self.tauAlfaDSpin = QtWidgets.QDoubleSpinBox()
        self.tauAlfaDSpin.setRange(0, 1)
        self.tauAlfaDSpin.setValue(0.85)
        paramLayout.addRow("tau_alfa_d:", self.tauAlfaDSpin)

        self.taSpin = QtWidgets.QDoubleSpinBox()
        self.taSpin.setRange(-50, 50)
        self.taSpin.setValue(20)
        paramLayout.addRow("Темп. Ta:", self.taSpin)

        self.minQUSpin = QtWidgets.QDoubleSpinBox()
        self.minQUSpin.setRange(0, 100000)
        self.minQUSpin.setValue(100)
        paramLayout.addRow("min_QU_required:", self.minQUSpin)

        self.hoursSpin = QtWidgets.QDoubleSpinBox()
        self.hoursSpin.setRange(0, 24)
        self.hoursSpin.setValue(10)
        paramLayout.addRow("hours:", self.hoursSpin)

        self.optimizationModeCombo = QtWidgets.QComboBox()
        self.optimizationModeCombo.addItems(["cost", "energy"])
        paramLayout.addRow("Режим оптимизации:", self.optimizationModeCombo)

        self.updateButton = QtWidgets.QPushButton("Перестроить графики")
        paramLayout.addRow(self.updateButton)
        self.updateButton.clicked.connect(self.updateSimulation)

        mainLayout.addWidget(self.paramPanel)

        # Центральная область для графиков (Matplotlib)
        self.figure, self.ax = plt.subplots(2, 2, figsize=(8, 6))
        self.canvas = FigureCanvas(self.figure)
        mainLayout.addWidget(self.canvas)

        # Нижняя панель для вывода результатов оптимизации
        self.outputText = QtWidgets.QTextEdit()
        self.outputText.setReadOnly(True)
        outputLayout = QtWidgets.QVBoxLayout()
        outputLayout.addWidget(self.outputText)
        mainLayout.addLayout(outputLayout)

        # Инициализация моделей
        self.specs = SolarCollectorSpecs()
        self.tank = HeatStorageTank()

        self.updateSimulation()

    def updateSimulation(self):
        # Чтение параметров из интерфейса
        Ib = self.ibSpin.value()
        Id = self.idSpin.value()
        rb = self.rbSpin.value()
        rd = self.rdSpin.value()
        rr = self.rrSpin.value()
        tau_alfa_b = self.tauAlfaBSpin.value()
        tau_alfa_d = self.tauAlfaDSpin.value()
        Ta = self.taSpin.value()
        min_QU_required = self.minQUSpin.value()

        # Остальные параметры симуляции (фиксированные)
        TFI = 30
        Cp = 4186
        Massa = 50
        Twater = 30
        Twater2 = 60
        Ttank = 40  # начальная температура бака
        V_load_liters = 100
        T_water = 35

        # Симуляция динамики температуры бака за 10 часов
        temps = []
        kpd_hours = []
        QI_hours = []
        QU_hours = []
        Qloss_hours = []
        Qload_hours = []
        Ttank_sim = Ttank
        hours = np.arange(self.hoursSpin.value())
        for _ in hours:
            res = self.specs.simulate_hour(
                Ib, Id, rb, rd, rr,
                tau_alfa_b, tau_alfa_d, 0.92,
                Ta, TFI, Cp, Massa,
                Twater, Twater2,
                Ttank_sim,
                heat_storage_tank=self.tank,
                V_load_liters=V_load_liters,
                T_water=T_water
            )

            Ttank_sim = res["Ttank_new"]
            temps.append(Ttank_sim)
            kpd_hours.append(res["KPD_hourly"])
            QI_hours.append(res["QI"])
            QU_hours.append(res["QU"])
            Qloss_hours.append(res["Q_loss"])
            Qload_hours.append(res["Q_load"])

        # Очистка графиков
        for ax in self.ax.flatten():
            ax.clear()

        # Построение графиков:
        # 1. Верхний левый: QI и QU
        ax0 = self.ax[0, 0]
        ax0.plot(hours, QI_hours, label="QI")
        ax0.plot(hours, QU_hours, label="QU")
        ax0.legend()
        ax0.set_xlabel("Час")
        ax0.set_ylabel("Вт")
        ax0.set_title("Поступающая и полезная энергия")

        # 2. Верхний правый: КПД
        ax1 = self.ax[0, 1]
        ax1.plot(hours, [KPD * 100 for KPD in kpd_hours])
        ax1.set_xlabel("Час")
        ax1.set_ylabel("%")
        ax1.set_title("КПД (%)")

        # 3. Нижний левый: Потери бака и потребление
        ax2 = self.ax[1, 0]
        ax2.plot(hours, Qloss_hours, label="Потери")
        ax2.plot(hours, Qload_hours, label="Потребление")
        ax2.legend()
        ax2.set_xlabel("Час")
        ax2.set_ylabel("Вт")
        ax2.set_title("Потери и потребление")

        # 4. Нижний правый: Температура бака за 10 часов
        ax3 = self.ax[1, 1]
        ax3.plot(hours, temps, marker="o", color="magenta")
        ax3.set_title("Температура бака")
        ax3.set_xlabel("Час")
        ax3.set_ylabel("Темп. (°C)")

        self.figure.tight_layout()
        self.canvas.draw()

        # Оптимизация площади коллектора
        try:
            optimal_area = optimize_collector_area_scipy(
                self.specs, Ib, Id, rb, rd, rr,
                tau_alfa_b, tau_alfa_d,
                0.95*0.97, min_QU_required,
                objective_type=self.optimizationModeCombo.currentText()
            )
            print(self.optimizationModeCombo.currentText())
            opt_text = f"Оптимальная площадь коллектора: {optimal_area:.2f} м²"
        except Exception as e:
            opt_text = f"Ошибка оптимизации: {str(e)}"

        self.outputText.setPlainText(opt_text)

def optimize_collector_area_scipy(solar_spec: SolarCollectorSpecs,
                                  Ib, Id, rb, rd, rr,
                                  tau_alfa_b, tau_alfa_d,
                                  Ta,
                                  min_QU_required: float,
                                  objective_type: str = 'energy'):
    """
    Оптимизирует площадь коллектора A с использованием scipy.optimize.linprog.

    Формулы из документа:
      IT = I_b * r_b + I_d * r_d + (I_b + I_d) * r_r
      S  = I_b * r_b * tau_alfa_b + (I_d * r_d + (I_b + I_d) * r_r) * tau_alfa_d
      QU = A * (IT * tau_alfa - S)

    Ограничение: QU >= min_QU_required  <=>  A * (IT * tau_alfa - S) >= min_QU_required

    objective_type:
      - 'cost': минимизация затрат: cost = cost_per_m2 * A
      - 'energy': максимизация полезной энергии, что эквивалентно минимизации -QU.
    """
    IT = solar_spec.calc_total_radiation(Ib, Id, rb, rd, rr)
    S = solar_spec.calc_effective_intensity(Ib, Id, rb, rd, rr, tau_alfa_b, tau_alfa_d)

    # QU = A * (IT * tau_alfa - S)
    coeff = IT * Ta - S

    # Границы для площади коллектора (от 2 до 100 м²)
    min_area = 2
    max_area = 100
    bounds = [(min_area, max_area)]

    if objective_type == 'cost':
        # Минимизируем затраты: cost = cost_per_m2 * A
        cost_per_m2 = 100
        c = [cost_per_m2]
    elif objective_type == 'energy':
        # Максимизируем QU
        c = [-coeff]
    else:
        raise ValueError("Неверный тип целевой функции. Выберите 'cost' или 'energy'.")

    # Ограничение: A * coeff >= min_QU_required  =>  -A * coeff <= -min_QU_required
    A_ub = [[-coeff]]
    b_ub = [-min_QU_required]

    res = linprog(c=c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method='highs')

    if res.success:
        optimal_area = res.x[0]
    else:
        raise ValueError("Оптимизация не удалась " + res.message)

    return optimal_area

# specs = SolarCollectorSpecs()
# tank = HeatStorageTank()
#
#
# # Начальные данные
# Ttank = 40  # начальная температура воды в баке
#
# # Метео и параметры
# Ib1 = 800
# Id1 = 150
# rb, rd, rr = 1.0, 0.2, 0.1
# tau_alfa_b, tau_alfa_d, tau_alfa = 0.9, 0.85, 0.92
# Ta1 = 20       # температура окружающей среды
# TFI = 30       # вход теплоносителя
# Cp = 4186
# Massa = 50     # кг
# Twater = 30
# Twater2 = 60
#
# # Потребление
# V_load_liters = 100  # литров в час
# T_water = 35         # требуемая температура воды потребителем
#
# # Расчёт
# result = specs.simulate_hour(
#     Ib1, Id1, rb, rd, rr,
#     tau_alfa_b, tau_alfa_d, tau_alfa,
#     Ta1, TFI, Cp, Massa,
#     Twater, Twater2,
#     Ttank,
#     heat_storage_tank=tank,
#     V_load_liters=V_load_liters,
#     T_water=T_water
# )
#
# # Вывод результатов
# print(f"QI (поступающая энергия): {result['QI']:.2f} Вт")
# print(f"QU (полезная энергия): {result['QU']:.2f} Вт")
# print(f"КПД: {result['KPD_hourly'] * 100:.2f} %")
# print(f"Потери бака Q_loss: {result['Q_loss']:.2f} Вт")
# print(f"Потребление Q_load: {result['Q_load']:.2f} Вт")
# print(f"Температура бака после часа: {result['Ttank_new']:.2f} °C")
#
#
# # Инициализация
# Ttank = 40  # начальная температура
# temps = []
#
# # Прогон симуляции на 10 часов
# for hour in range(10):
#     result = specs.simulate_hour(
#         Ib1=800, Id1=150, rb=1.0, rd=0.2, rr=0.1,
#         tau_alfa_b=0.9, tau_alfa_d=0.85, tau_alfa=0.92,
#         Ta1=20, TFI=30, Cp=4186, Massa=50,
#         Twater=30, Twater2=60,
#         Ttank=Ttank,
#         heat_storage_tank=tank,
#         V_load_liters=100,
#         T_water=35
#     )
#
#     Ttank = result["Ttank_new"]  # обновляем для следующего часа
#     temps.append(Ttank)
#
# # Результаты
# for i, t in enumerate(temps):
#     print(f"Час {i+1}: Ttank = {t:.2f} °C")
#
# objective_type = "energy" # energy | cost
# solar_spec = SolarCollectorSpecs(Ut=2.889, Ub=0.017, Us=0.005, area=4)
# optimal_area = optimize_collector_area_scipy(solar_spec, Ib1, Id1, rb, rd, rr,
#                                                tau_alfa_b, tau_alfa_d,
#                                                0.97*0.95, 200, objective_type)
# print(f"Оптимальная площадь коллектора (objective='{objective_type}'): {optimal_area:.2f} м²")
#
# # Расчитаем полезную энергию с оптимизированной площадью
# QU = solar_spec.calc_useful_energy_by_area(IT=solar_spec.calc_total_radiation(Ib1, Id1, rb, rd, rr),
#                                      S=solar_spec.calc_effective_intensity(Ib1, Id1, rb, rd, rr, tau_alfa_b, tau_alfa_d),
#                                      area=optimal_area)
# print(f"Полезная энергия при оптимальной площади: {QU:.2f} условных единиц")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())