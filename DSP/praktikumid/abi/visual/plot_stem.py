#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import pyqtgraph as pg

def simple_plot_stem(plot, y, x=None, **kwargs):
    if x is None: x = np.arange(y.size)

    # Create a companion for every y value at y=0
    y0_pairs = np.dstack((np.zeros(y.shape[0]), y)).flatten()
    # Set the x coordinate for the created zero value the same as the accompanying non-zero y value
    plot.plot(x=np.repeat(x, 2), y=y0_pairs, connect='pairs', pen=pg.mkPen('w', width=3), **kwargs)
    plot.plot(x=x, y=y, pen=None, symbol='o',symbolBrush="r")


def plot_stem(plot, magnitudes, phases=None, x_plot=None, **kwargs):
    """
    Funktsioon, mida saate kaustada DFT tulemuse graafikule kuvamiseks.

    Argumendid:
    plot -- graafiku objekt.
    magnitudes -- np.array magnituudidest.
    phases -- np.array faasidest.
    x_plot -- np.array vastavatest x telje väärtustest.
    """

    if x_plot is None:
        x_plot = np.arange(magnitudes.size)

    magnitudes = np.array(magnitudes)

    y0_pairs = np.dstack((np.zeros(magnitudes.shape[0]), magnitudes)).flatten()
    plot.plot(x=np.repeat(x_plot, 2), y=y0_pairs, connect='pairs', pen=pg.mkPen('w', width=3), **kwargs)

    if phases is None:
        plot.plot(x=x_plot, y=magnitudes, pen=None, symbol='o', symbolBrush="c")
    else:
        shifted_phase_val = np.mod(phases, 2 * np.pi)
        rounded_phase_deg_val = np.around((np.degrees(shifted_phase_val)), decimals=1)

        cm = pg.colormap.get(
            'CET-CBL2')  # Use another if colour scheme is not good for you: https://colorcet.holoviz.org/user_guide/
        cm_colours = cm.getColors()
        brush_colours = [pg.mkColor(cm_colours[int(s)]) for s in shifted_phase_val / (2 * np.pi) * 205 + 50]

        scatter = pg.ScatterPlotItem(tip = 'x: {x:.0g}\nmagnituud: {y:.1f}\nfaas={data:.1f}'.format)
        scatter.setData(x_plot, magnitudes, data=rounded_phase_deg_val, size=10, hoverable=True, hoverSymbol='s',
                        symbol='o', pen=None, brush=brush_colours)
        plot.addItem(scatter)
