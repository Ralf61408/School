#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np

def ühikimpulsi_loomine(pikkus = 1, nihe = 0, amplituud = 1):
    np_array = np.zeros(pikkus)

    np_array[0]=amplituud

    if nihe < 0:
        nihe *= -1
        
    return(np.roll(np_array, nihe))