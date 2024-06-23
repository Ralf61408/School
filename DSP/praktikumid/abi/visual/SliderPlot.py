import pyqtgraph as pg
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget, QLabel

from abi.visual.Slider import Slider

class SliderPlot(QWidget):
    def __init__(self, grid, row, x_values=None, parent=None, plot_title = "No name plot", plot_name = None, yRange=None, label=None):
        super().__init__(parent=parent)
        self.mainLayout = QHBoxLayout(self)
        self.sliderLayout = QVBoxLayout()
        self.sliders = []
        self.x = x_values
        self.grid = grid
        self.row = row

        self.grid.addLayout(self.sliderLayout, self.row, 0)

        if label is not None:
            self.label = QLabel()
            self.label.setText(label)
            self.grid.addWidget(self.label, row, 1)

        self.win = pg.GraphicsLayoutWidget(title=plot_title)
        self.win.ci.setContentsMargins(0., 0., 0., 0.)
        self.grid.addWidget(self.win, self.row, 2)
        self.plot = self.win.addPlot(name=plot_name, title=plot_title)
        if yRange != None:
            self.plot.setYRange(yRange[0], yRange[1])
        self.plot.addLegend()
        self.curve = self.plot.plot(name=plot_name,pen='y')
        self.init_sliders()

    def init_sliders(self):
        return

    def add_slider(self, start, stop, func, label_text="notext", start_value=0, scaler=1, tracking=True):
        w1 = Slider(start, stop, label_text=label_text, start_value=start_value, scaler=scaler, tracking=tracking)
        w1.slider.valueChanged.connect(func)
        self.sliders.append(w1)
        self.sliderLayout.addWidget(w1)

    def update_plot(self):
        return
