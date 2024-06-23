#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
from dst.math.convolution import convolve_2d


def blur(image, kernel_name):
    """
    Funktsioon, mis udustab pilti kasutades ette antud nimega kernelit.

    Sisendid:
        image: Pilt, millele udustamist rakendatakse.
        kernel_name: Kerneli nimi, mida kasutatakse pildi udustamiseks.

    Tagastab:
        Udustatud pilt 2-mõõtmelise massiivina, milles olevad arvud on uint8 tüüpi
    """
    kernel_map = {
        "box": np.ones((11,11), dtype="float64"),
        "gaussian": np.array((
            [1,  4,  7,  4, 1],
            [4, 16, 26, 16, 4],
            [7, 26, 41, 26, 7],
            [4, 16, 26, 16, 4],
            [1,  4,  7,  4, 1]), dtype="float64")
    }

    print("blur", image.dtype)
    print(image.min(), image.max())
    minu_pilt_max = image.max()
    kernel = kernel_map[kernel_name]
    img = convolve_2d(image.astype(np.float32), kernel)
    img = img.astype(np.float64) / np.max(img)
    img = minu_pilt_max * img
    img = img.astype(np.uint8)
    return img


def detect_edge(image, kernel_name):
    """
    Funktsioon, mis tuvastab pildil olevad servad, kasutades selleks ette antud nimega kernelit.

    Sisendid:
        image: Pilt, millel olevad servad tuvastatakse.
        kernel_name: Kerneli nimi, mida kasutatakse pildil olevate servade tuvastamiseks.

    Tagastab:
        Tuvastatud servadega pilt 2-mõõtmelise massiivina, milles olevad arvud on uint8 tüüpi
    """
    kernel_map = {
        "sobel_x": np.array((
            [-1, 0, 1],
            [-2, 0, 2],
            [-1, 0, 1]), dtype="float64"),
        "sobel_y": np.array((
            [-1, -2, -1],
            [ 0,  0,  0],
            [ 1,  2,  1]), dtype="float64"),
        "laplacian": np.array((
            [0,  1, 0],
            [1, -4, 1],
            [0,  1, 0]), dtype="float64"),
        "Prewitt_x_edge": np.array((
            [-1, 0, 1],
            [-1, 0, 1],
            [-1, 0, 1]), dtype="float64"),
        "Prewitt_y_edge": np.array((
            [-1, -1, -1],
            [0, 0, 0],
            [1, 1, 1]), dtype="float64"),

    }
    #print("edge", image.dtype)
    #print(image.min(), image.max())
    #minu_pilt_max2 = image.max()
    kernel = kernel_map[kernel_name]
    img = convolve_2d(image.astype(np.float32), kernel)
    img = np.absolute(img)
    #img = img.astype(np.float64) / np.max(img) # normaliseerin
    img = np.clip(img.astype(np.float64), 0, 255)
    ##img = minu_pilt_max2 * img # skaleerin tagasi väärtustesse 0 kuni 255

    img = img.astype(np.uint8)
    return img
