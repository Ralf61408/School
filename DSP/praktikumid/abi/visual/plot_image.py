#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pyqtgraph as pg
from PyQt5 import QtGui
from pyqtgraph import ColorBarItem
import numpy as np


def plot_image(plot_item: pg.graphicsItems.PlotItem, spec_img: np.ndarray, dt: int = 1, df: int = 1, colormap: str = "turbo", phase: bool = False) -> None:
    """
    Funktsioon, mida saate kasutada (kahemõõtmelise) pildi kuvamiseks.

    Argumendid:
    plot_item -- graafiku objekt.
    spec_img  -- kahemõõtmeline np.array.
    dt        -- spektrogrammi ajaline lahutus.
    df        -- spektrogrammi sageduslahutus.
    colormap  -- sõne, mis määrab kasutatava värviskaala.
    phase     -- kas kasutada väärtuste piiramiseks faasile omaseid piire.
    """
    img = pg.ImageItem()
    colorbar = ColorBarItem(colorMap=colormap)
    colorbar.setImageItem(img)
    plot_item.addItem(img)
    img.setImage(spec_img.T)
    min_val = spec_img.min() if not np.isinf(spec_img.min()) else -400
    if phase:
        img.setLevels([-np.pi, np.pi])
    else:
        img.setLevels([min_val/2,spec_img.max()/2])
    img.setTransform(QtGui.QTransform.fromScale(dt, df), True)
