import pyqtgraph as pg
from PyQt5.QtWidgets import QHBoxLayout, QWidget

class ComboPlot(QWidget):
    def __init__(self, grid, row, x, parent=None):
        super().__init__(parent=parent)
        self.mainLayout = QHBoxLayout(self)
        self.sliders = []
        self.x = x

        self.grid = grid
        self.row = row

        self.combo_plot = pg.PlotWidget(title="Algsignaal ja summeeritud signaal")
        self.combo_plot.addLegend(offset=(20,0))
        self.plot_original = self.combo_plot.plot(name="Algsignaal", pen='c')
        self.plot_sum = self.combo_plot.plot(name="Summeeritud signaal", pen='y')
        self.combo_plot.plot()
        self.grid.addWidget(self.combo_plot, row, 2)
        self.grid.setRowMinimumHeight(self.row, 200)
        self.orig_data = None

    def add_slider_graph(self, slider_graph):
        self.mainLayout.addWidget(slider_graph)

    def update_original_plot(self, new_data):
        self.plot_original.setData(new_data)
        self.orig_data = new_data

    def update_sum_plot(self, new_data):
        self.plot_sum.setData(new_data)
