#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import pyqtgraph as pg
from PyQt5.QtWidgets import QWidget, QTextEdit
from PyQt5.QtGui import QFont

from abi.visual.MainWindow import MainWindow
from abi.visual.ComboPlot import ComboPlot
from abi.visual.QHSeperationLine import QHSeperationLine
from abi.visual.ComponentView import ComponentView
from abi.visual.InputFunctionHandler import InputFunctionHandler
from abi.visual.plot_stem import simple_plot_stem

class BaseSignal(QWidget):
    def __init__(self, combo_graph, data, parent=None):
        self.combo_graph = combo_graph
        self.data=data
        super().__init__(parent=parent)
        self.update_plot()

    def update_plot(self):
        self.combo_graph.update_original_plot(self.data)

class StudentRandomizer():
    def __init__(self, studybook_nr, task_nr = 1) -> None:
        self.seed = int(studybook_nr[1:])*task_nr
        self.random = np.random.RandomState(self.seed)

class Task():
    def __init__(self, x=None, studybook_nr=0, task_nr = 1, subtask=1) -> None:
        if x.any():
            self.x=x
        else:
            self.x = np.arange(0, 2*np.pi, 0.02)
        self.sbnr = studybook_nr
        self.sr = StudentRandomizer(self.sbnr, task_nr)
        self.mw = MainWindow()
        self.cg = ComboPlot(grid=self.mw.grid, row=0, x=self.x)
        ComponentView.combo_plot = self.cg
        for _ in range(subtask):
            self.w = BaseSignal(self.cg, self.generate_base_data())
        self.mw.grid.addWidget(self.cg, 0, 1)
        #self.mw.mainLayout.addWidget(self.w) #miks üldse oli vajalik?
        self.mw.grid.addWidget(QHSeperationLine(), 1, 0, 1, -1)

        self.ifh = InputFunctionHandler()
    def show(self):
        self.mw.showMaximized()
    def generate_base_data(self):
        return
    def rint(self, start, stop):
        return self.sr.random.randint(start, stop)

class Task1(Task):
    def __init__(self, x=None, studybook_nr=0, plot_name=None, subtask=1) -> None:
        super().__init__(x=x, studybook_nr=studybook_nr, task_nr=1, subtask=subtask)
        ComponentView(grid=self.mw.grid, row=2, x_values=self.x, sum_comp=True, plot_title="Summeeritav signaal f[x]", plot_name=plot_name, yRange=(-1,1), hide_sliders=[1,2])

    def generate_base_data(self):
        return np.cos(self.x*self.rint(3, 20)*np.pi*2)

class Task2(Task):
    def __init__(self, x=None, studybook_nr=0, plot_name=None, subtask=1) -> None:
        super().__init__(x=x, studybook_nr=studybook_nr, task_nr=2, subtask=subtask)
        ComponentView(grid=self.mw.grid, row=2, x_values=self.x, sum_comp=True, plot_title="Summeeritav signaal f[x]", plot_name=plot_name)
    def generate_base_data(self):
        return self.rint(3, 18)*np.cos(self.x*self.rint(1, 15)*np.pi*2 + np.radians(self.rint(30, 300)))

class Task3(Task):
    def __init__(self, x=None, studybook_nr=0, plot_name=None, subtask=1) -> None:
        super().__init__(x=x, studybook_nr=studybook_nr, task_nr=3, subtask=subtask)
        ComponentView(grid=self.mw.grid, row=2, x_values=self.x, sum_comp=True, plot_title="Summeeritav signaal f[x]", plot_name=plot_name)
        ComponentView(grid=self.mw.grid, row=3, x_values=self.x, sum_comp=True, plot_title="Summeeritav signaal g[x]", plot_name=plot_name)
    def generate_base_data(self):
        return self.rint(10, 20)*np.cos(self.x*self.rint(2, 9)*np.pi*2) + \
            self.rint(2, 9)*np.cos(self.x*self.rint(10, 20)*np.pi*2)

class Task4(Task):
    def __init__(self, x=None, studybook_nr=0, plot_name=None, subtask=1) -> None:
        super().__init__(x=x, studybook_nr=studybook_nr, task_nr=4, subtask=subtask)
        ComponentView(grid=self.mw.grid, row=2, x_values=self.x, sum_comp=True, plot_title="Summeeritav signaal f[x]", plot_name=plot_name)
        ComponentView(grid=self.mw.grid, row=3, x_values=self.x, sum_comp=True, plot_title="Summeeritav signaal g[x]", plot_name=plot_name)
        ComponentView(grid=self.mw.grid, row=4, x_values=self.x, sum_comp=True, plot_title="Summeeritav signaal k[x]", plot_name=plot_name)
    def generate_base_data(self):
        return self.rint(5, 20)*np.cos(self.x*self.rint(2, 9)*np.pi*2 + np.radians(self.rint(30, 300))) + \
            self.rint(4, 9)*np.cos(self.x*self.rint(10, 20)*np.pi*2 + np.radians(self.rint(30, 300))) + self.rint(5, 20)

class Task5(Task):
    def __init__(self, x=None, studybook_nr=0, plot_name=None, subtask=1) -> None:
        super().__init__(x=x, studybook_nr=studybook_nr, task_nr=5, subtask=subtask)
        ComponentView(grid=self.mw.grid, row=2, x_values=self.x, sum_comp=True, plot_title="Summeeritav signaal f[x]", plot_name=plot_name)
        ComponentView(grid=self.mw.grid, row=3, x_values=self.x, sum_comp=True, plot_title="Summeeritav signaal g[x]", plot_name=plot_name)
        ComponentView(grid=self.mw.grid, row=4, x_values=self.x, sum_comp=True, plot_title="Summeeritav signaal k[x]", plot_name=plot_name)
    def generate_base_data(self):
        return self.rint(11, 20)*np.cos(self.x*self.rint(2, 9)*np.pi*2 + np.radians(self.rint(30, 300))) + \
            self.rint(2, 9)*np.cos(self.x*self.rint(10, 20)*np.pi*2 + np.radians(self.rint(30, 300))) + \
            self.rint(2, 20)*np.cos(self.x*self.rint(21, 30)*np.pi*2 + np.radians(self.rint(30, 300)))

class Task6(Task):
    def __init__(self, x=None, studybook_nr=0, plot_name=None, subtask=1) -> None:
        super().__init__(x=x, studybook_nr=studybook_nr, task_nr=6, subtask=subtask)
        ComponentView(grid=self.mw.grid, row=2, x_values=self.x, sum_comp=True, plot_title="Summeeritav signaal f[x]", plot_name=plot_name)
        ComponentView(grid=self.mw.grid, row=3, x_values=self.x, sum_comp=True, plot_title="Summeeritav signaal g[x]", plot_name=plot_name)
        ComponentView(grid=self.mw.grid, row=4, x_values=self.x, sum_comp=True, plot_title="Summeeritav signaal k[x]", plot_name=plot_name)
        ComponentView(grid=self.mw.grid, row=5, x_values=self.x, sum_comp=True, plot_title="Summeeritav signaal m[x]", plot_name=plot_name)

        self.dft_plot = pg.PlotWidget(title="Sagedused", row=0, col=0, show=False)
        self.mw.grid.addWidget(self.dft_plot, 0, 0)

    def generate_base_data(self):
        return self.rint(10, 20)*np.cos(self.x*self.rint(2, 9)*np.pi*2 + np.radians(self.rint(30, 300))) + \
            self.rint(2, 9)*np.cos(self.x*self.rint(10, 20)*np.pi*2 + np.radians(self.rint(30, 300))) + \
            self.rint(2, 20)*np.cos(self.x*self.rint(2, 20)*np.pi*2 + np.radians(self.rint(30, 300))) + self.rint(10, 20)
    def show(self):
        self.dft_result = self.ifh.freq_func(self.x, self.w.data)
        self.magnitudes = np.squeeze(self.dft_result[:, [0]])
        self.phases = np.squeeze(self.dft_result[:, [1]]) # Set phase to 0 if magnitude negligible

        simple_plot_stem(self.dft_plot, self.magnitudes)

        self.dft_plot.getPlotItem().getViewBox().setLimits(xMin=-10, xMax=210, yMin=-10, yMax=30)

        for i, phase in np.ndenumerate(self.phases):
            if self.magnitudes[i] > 0.5:
                text = pg.TextItem()
                text.setText("φ={0:.1f}".format(phase))
                text.setColor("#ffc20a")
                text.setAngle(45)
                self.dft_plot.addItem(text)
                text.setPos(i[0], self.magnitudes[i])

        super().show()

class Task7(Task):
    def __init__(self, x=None, studybook_nr=0, plot_name=None, subtask=1) -> None:
        super().__init__(x=x, studybook_nr=studybook_nr, task_nr=7, subtask=subtask)
        self.cg.combo_plot.hide()

        textbox = QTextEdit()
        textbox.setReadOnly(True)
        textbox.setFont(QFont("Arial", 12))
        textbox.setText("7. ülesande lahendamiseks implementeerige ja jooksutage programmifaili 'dst/math/complex_math.py'")
        self.mw.grid.addWidget(textbox, 0, 0)

    def generate_base_data(self):
        return self.x*0

class Task8(Task):
    def __init__(self, x=None, studybook_nr=0, plot_name=None, subtask=1) -> None:
        super().__init__(x=x, studybook_nr=studybook_nr, task_nr=6, subtask=subtask)

        self.dft_plot = pg.PlotWidget(title="Sagedused", row=0, col=0, show=False)
        self.mw.grid.addWidget(self.dft_plot, 0, 0)
        self.cg.plot_sum.hide()

    def generate_base_data(self):
        return self.rint(16, 20)*np.cos(self.x*self.rint(2, 8)*np.pi*2 + np.radians(self.rint(30, 300))) + \
            self.rint(8, 13)*np.cos(self.x*self.rint(10, 18)*np.pi*2 + np.radians(self.rint(30, 300))) + \
            self.rint(2, 5)*np.cos(self.x*self.rint(20, 32)*np.pi*2 + np.radians(self.rint(30, 300))) + self.rint(12, 20)
    def show(self):
        self.dft_result = self.ifh.freq_func(self.x, self.w.data)
        self.magnitudes = np.squeeze(self.dft_result[:, [0]])
        self.phases = np.squeeze(self.dft_result[:, [1]])
        self.complex_result = self.ifh.freq_converter(self.dft_result)

        simple_plot_stem(self.dft_plot, self.magnitudes)

        self.dft_plot.getPlotItem().getViewBox().setLimits(xMin=-10, xMax=210, yMin=-10, yMax=30)

        for i, phase in np.ndenumerate(self.phases):
            if self.magnitudes[i] > 0.5:
                text = pg.TextItem()
                text.setText("r={0:.1f};φ={1:.1f}\n{2:.2f}".format(self.magnitudes[i], phase, self.complex_result[i]))
                text.setColor("#ffc20a")
                text.setAngle(45)

                self.dft_plot.addItem(text)
                text.setPos(i[0], self.magnitudes[i])

        super().show()

tasklist = [Task1, Task2, Task3, Task4, Task5, Task6, Task7, Task8]
