#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np

def hann_window_function(M):
    """
    P07 yl7 loodav Hann’i aknafunktsioon.

    Sisendid:
    M -- Akna pikkus

    Tagastab:
        np.array, M pikkuse aknafunktsiooni.
    """
    result = np.zeros((M))
    for n in range(M):
        result[n] = 0.5 - (0.5 * np.cos(2*np.pi*n/(M-1)))
    return result
