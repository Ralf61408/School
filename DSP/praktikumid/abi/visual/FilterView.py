#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
from abi.visual.SliderPlot import SliderPlot

class FilterView(SliderPlot):
    def __init__(self, grid, row, x_values, parent=None, combo_graph=None, plot_title = "No name plot", plot_name=None, yRange=None, label="", hide_sliders=[]):
        self.f_filter_time = lambda a,b : np.zeros(0)
        self.f_filter_freq = lambda a : np.zeros(0)
        self.f_plot_time = lambda plot_item, data, name = "": None
        self.f_plot_freq = lambda plot_item, data, dB_scale = False, name = "" : None
        self.f_compare = lambda a,b : 0
        self.combo_graph = combo_graph
        super().__init__(grid, row, x_values=None, parent=parent, plot_title=plot_title, plot_name=plot_name, yRange=yRange, label=label)
        self.time_plot = self.plot
        self.win.nextRow()
        self.freq_plot = self.win.addPlot(title="Filter sagedusruumis")
        self.win.nextRow()
        self.freq_db_plot = self.win.addPlot(title="Filter sagedusruumis (db)")

        self.hide_sliders(hide_sliders)
        #self.update_plot()

    def update_plot(self):
        self.cut_freq = self.sliders[0].x
        self.bandwidth = self.sliders[1].x
        self.filter = self.f_filter_time(self.cut_freq, self.bandwidth)
        if self.filter is not None:
            self.freq = self.f_filter_freq(self.filter)

            self.time_plot.clear()
            self.freq_plot.clear()
            self.freq_db_plot.clear()
            self.f_plot_time(self.time_plot, self.filter)
            self.f_plot_freq(self.freq_plot, self.freq)
            self.f_plot_freq(self.freq_db_plot, self.freq, dB_scale=True)
            #self.curve.setData(self.data)
            if self.combo_graph and self.filter.any():
                self.combo_graph.update_filtered_data(self.filter)
                self.combo_graph.update()

    def init_sliders(self):
        self.add_slider(1, 4999, self.update_plot, label_text="Mahalõikesagedus\n[fc]", scaler=0.0001, start_value=250, tracking=False)
        self.add_slider(1, 1000, self.update_plot, label_text="Siirdeala laius\n[bandwidth]", start_value=50, scaler=0.0001, tracking=False)

    def hide_slider(self, index):
        self.sliders[index].hide()

    def hide_sliders(self, indexes):
        for i in indexes:
            self.hide_slider(i)


class BandFilterView(FilterView):
    def __init__(self, grid, row, x_values, parent=None, combo_graph=None, plot_title = "No name plot", plot_name=None, yRange=None, label="", hide_sliders=[]):
        super().__init__(grid, row, x_values, parent=parent,combo_graph=combo_graph, plot_title=plot_title, plot_name=plot_name, yRange=yRange, hide_sliders=hide_sliders)
        self.f_filter_time = lambda a,b,c : np.zeros(0)

    def update_plot(self):
        self.low_freq, self.high_freq, self.bandwidth, *_  = [s.x for s in self.sliders]
        self.data = self.f_filter_time(self.low_freq, self.high_freq, self.bandwidth)
        if self.data is not None:
            freq = self.f_filter_freq(self.data)

            self.time_plot.clear()
            self.freq_plot.clear()
            self.freq_db_plot.clear()
            self.f_plot_time(self.time_plot, self.data)
            self.f_plot_freq(self.freq_plot, freq)
            self.f_plot_freq(self.freq_db_plot, freq, dB_scale=True)
            #self.curve.setData(self.data)
            if self.combo_graph and self.data.any():
                self.combo_graph.update_filtered_data(self.data)
                self.combo_graph.update()
                #self.combo_graph.update(self.data, apply_filter(self.data, ))

    def init_sliders(self):
        self.add_slider(1, 5000, self.update_plot, label_text="Alampiir\n[f_lower]", scaler=0.0001, start_value=150, tracking=False)
        self.add_slider(1, 5000, self.update_plot, label_text="Ülempiir\n[f_upper]", scaler=0.0001, start_value=250, tracking=False)
        self.add_slider(1, 1000, self.update_plot, label_text="Siirdeala laius\n[bandwidth]", start_value=50, scaler=0.0001, tracking=False)
