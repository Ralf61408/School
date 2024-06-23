#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pyqtgraph as pg
from PyQt5.QtWidgets import QHBoxLayout, QWidget, QSpacerItem, QPushButton, QComboBox
from PyQt5.QtCore import Qt
from dst.visual.plot_filters import plot_filtered_vs_unfiltered_freq, plot_filtered_vs_unfiltered_time, plot_spectrogram
from dst.filter.onedim.frequency import apply_filter

class FilterComboGraph(QWidget):
    def __init__(self, unfiltered_data, grid, row, parent=None, combo_box_items=["Aegruum", "Sagedusruum", "Spektrogramm"]):
        super(FilterComboGraph, self).__init__(parent=parent)
        self.mainLayout = QHBoxLayout(self)
        self.mainLayout.addSpacerItem(QSpacerItem(60, 200)) #The item also restricts the height from getting too small

        self.grid = grid
        self.row = row

        self.unfiltered_data = unfiltered_data
        self.combo_plot = pg.PlotWidget(title="Filtreerimata signaal vs filtreeritud signaal")
        self.combo_plot.addLegend(offset=(0,50))
        self.filtered_data = None
        self.current_plot = "Aegruum"

        self.mainLayout.addWidget(self.combo_plot)

        self.combo_box = QComboBox()
        #self.combo_options = {"Aegruum"}
        self.combo_box.addItems(combo_box_items)
        self.combo_box.currentTextChanged.connect(self.combo_box_text_changed)

        self.domain_button = QPushButton("Kuva aegruumi esitus")
        self.domain_button.setStyleSheet('margin:5px;padding:2px')
        self.domain_button.clicked.connect(self.toggle_plot_domain)

        self.plot_domain_freq = True
        self.grid.addWidget(self.combo_plot, row, 0, 1, 3)

        #self.grid.addWidget(self.domain_button, row, 2, 1, 1, alignment=Qt.AlignmentFlag(34))
        self.grid.addWidget(self.combo_box, row, 2, 1, 1, alignment=Qt.AlignmentFlag(34))


    def combo_box_text_changed(self, text):
        self.current_plot = text
        self.update()


    def update(self):
        self.combo_plot.clear()
        if not self.filtered_data is None and not self.unfiltered_data is None:
            match self.current_plot:
                case "Aegruum":
                    plot_filtered_vs_unfiltered_time(self.combo_plot, self.unfiltered_data, self.filtered_data)
                    self.combo_plot.setTitle("Filtreerimata signaal vs filtreeritud signaal")
                case "Sagedusruum":
                    plot_filtered_vs_unfiltered_freq(self.combo_plot, self.unfiltered_data, self.filtered_data)
                    self.combo_plot.setTitle("Filtreerimata signaal vs filtreeritud signaal")
                case "Spektrogramm":
                    plot_spectrogram(self.combo_plot, self.filtered_data)
                    self.combo_plot.setTitle("Filtreeritud signaali spektrogramm")


    def update_unfiltered_data(self, new_data):
        #self.plot_unfiltered.setData(x=self.x, y=new_data)
        self.unfiltered_data = new_data


    def update_filtered_data(self, filter):
        if not self.unfiltered_data is None:
            self.filtered_data = apply_filter(filter, self.unfiltered_data)
        #self.plot_filtered.setData(x=self.x, y=np.abs(np.fft.rfft(self.filtered_data))/self.filtered_data.size)

    def toggle_plot_domain(self):
        if self.plot_domain_freq:
            self.domain_button.setText("Kuva sagedusruumi esitus")
            self.plot_domain_freq = False
        else:
            self.domain_button.setText("Kuva aegruumi esitus")
            self.plot_domain_freq = True
        self.update()
        self.combo_plot.getViewBox().enableAutoRange()
