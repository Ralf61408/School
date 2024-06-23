#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QApplication
import sys

from dst.filter.onedim.frequency import *
from dst.visual.plot_filters import *

from abi.visual.MainWindow import MainWindow
from abi.visual.FilterComboGraph import FilterComboGraph
from abi.visual.FilterView import FilterView, BandFilterView
from abi.visual.AudioPlayer import AudioPlayer

import os

class Task:
    def __init__(self) -> None:
        self.app = QApplication(sys.argv)
        with open(f"{os.path.dirname(__file__)}/styles.qss") as file:
            self.app.setStyleSheet(file.read())
        self.mw = MainWindow()
        self.mw.showMaximized()

    def get_unfiltered_data(self):
        return self.cg.unfiltered_data

    def get_filtered_data(self):
        return self.cg.filtered_data

    def start(self):
        self.app.exec_()

class Task1(Task):
    def __init__(self) -> None:
        super().__init__()
        self.fsg = FilterView(grid=self.mw.grid, row=2, x_values=None, combo_graph=None, plot_title="Madalpääsfiltri kernel ajas", plot_name="")
        self.fsg.f_filter_time = create_lowpass
        self.fsg.f_filter_freq = transform_filter_kernel
        self.fsg.f_plot_time = plot_filter_time
        self.fsg.f_plot_freq = plot_filter_freq
        self.fsg.update_plot()


class Task3(Task):
    def __init__(self, unfiltered_data, sr) -> None:
        super().__init__()
        self.cg = FilterComboGraph(unfiltered_data=unfiltered_data, grid=self.mw.grid, row=1, combo_box_items=["Aegruum", "Sagedusruum"])
        self.fsg = FilterView(grid=self.mw.grid, row=2, x_values=None, combo_graph=self.cg, plot_title="Madalpääsfiltri kernel ajas", plot_name="")
        self.fsg.f_filter_time = create_lowpass
        self.fsg.f_filter_freq = transform_filter_kernel
        self.fsg.f_plot_time = plot_filter_time
        self.fsg.f_plot_freq = plot_filter_freq
        self.fsg.update_plot()
        self.cg.update_unfiltered_data(unfiltered_data)
        self.ap = AudioPlayer(self.mw.grid, 0, self, sr, self.cg)


class Task4(Task):
    def __init__(self) -> None:
        super().__init__()
        self.fsg = FilterView(grid=self.mw.grid, row=2, x_values=None, combo_graph=None, plot_title="Kõrgpääsfiltri kernel ajas", plot_name="")
        self.fsg.f_filter_time = create_highpass_spectral_inversion
        self.fsg.f_filter_freq = transform_filter_kernel
        self.fsg.f_plot_time = plot_filter_time
        self.fsg.f_plot_freq = plot_filter_freq
        self.fsg.update_plot()


class Task5(Task):
    def __init__(self, unfiltered_data, sr) -> None:
        super().__init__()
        self.cg = FilterComboGraph(unfiltered_data=unfiltered_data, grid=self.mw.grid, row=1, combo_box_items=["Aegruum", "Sagedusruum", "Spektrogramm"])
        self.fsg = FilterView(grid=self.mw.grid, row=2, x_values=None, combo_graph=self.cg, plot_title="Kõrgpääsfiltri kernel ajas", plot_name="")
        self.fsg.f_filter_time = create_highpass_spectral_inversion
        self.fsg.f_filter_freq = transform_filter_kernel
        self.fsg.f_plot_time = plot_filter_time
        self.fsg.f_plot_freq = plot_filter_freq
        self.fsg.update_plot()
        self.cg.update_unfiltered_data(unfiltered_data)
        self.ap = AudioPlayer(self.mw.grid, 0, self, sr)


class Task6(Task):
    def __init__(self) -> None:
        super().__init__()
        self.fsg = BandFilterView(grid=self.mw.grid, row=2, x_values=None, combo_graph=None, plot_title="Ribapääsfiltri kernel ajas", plot_name="")
        self.fsg.f_filter_time = create_bandpass
        self.fsg.f_filter_freq = transform_filter_kernel
        self.fsg.f_plot_time = plot_filter_time
        self.fsg.f_plot_freq = plot_filter_freq
        self.fsg.update_plot()


class Task7(Task):
    def __init__(self, unfiltered_data) -> None:
        super().__init__()
        self.cg = FilterComboGraph(unfiltered_data=unfiltered_data, grid=self.mw.grid, row=1, combo_box_items=["Aegruum", "Sagedusruum", "Spektrogramm"])
        self.fsg = BandFilterView(grid=self.mw.grid, row=2, x_values=None, combo_graph=self.cg, plot_title="Ribapääsfiltri kernel ajas", plot_name="")
        self.fsg.f_filter_time = create_bandpass
        self.fsg.f_filter_freq = transform_filter_kernel
        self.fsg.f_plot_time = plot_filter_time
        self.fsg.f_plot_freq = plot_filter_freq
        self.fsg.update_plot()
        self.cg.update_unfiltered_data(unfiltered_data)

class Task8(Task):
    def __init__(self) -> None:
        super().__init__()
        self.fsg = BandFilterView(grid=self.mw.grid, row=2, x_values=None, combo_graph=None, plot_title="Ribatõkkefiltri kernel ajas", plot_name="")
        self.fsg.f_filter_time = create_bandstop
        self.fsg.f_filter_freq = transform_filter_kernel
        self.fsg.f_plot_time = plot_filter_time
        self.fsg.f_plot_freq = plot_filter_freq
        self.fsg.update_plot()

class Task9(Task):
    def __init__(self, unfiltered_data, sr) -> None:
        super().__init__()
        self.cg = FilterComboGraph(unfiltered_data=unfiltered_data, grid=self.mw.grid, row=1, combo_box_items=["Aegruum", "Sagedusruum", "Spektrogramm"])
        self.fsg = BandFilterView(grid=self.mw.grid, row=2, x_values=None, combo_graph=self.cg, plot_title="Ribatõkkefiltri kernel ajas", plot_name="")
        self.fsg.f_filter_time = create_bandstop
        self.fsg.f_filter_freq = transform_filter_kernel
        self.fsg.f_plot_time = plot_filter_time
        self.fsg.f_plot_freq = plot_filter_freq
        self.fsg.update_plot()
        self.cg.update_unfiltered_data(unfiltered_data)
        self.ap = AudioPlayer(self.mw.grid, 0, self, sr)
