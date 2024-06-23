#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np, math


def roots_of_unity(n):
    """
    Sisend: positiivne täisarv n (>0)
    Tagastab: 'complex' tüüpi NumPy massiiv kõigist arvu 1 n-astme juurtest
    """

    vastus = []
    # Itereerime läbi kõik juurte indeksid (0 kuni n-1)
    for hulk in range(0, n):
        # Arvutame Euleri valemi kompleksi osa
        kompleks = -(2*np.pi*1j/n)
        # Arvutame Euleri valemi baasil komplekseksponendi
        euleri = pow(math.e, kompleks)
        # Tõstame euleri väärtuse hulk astmesse, et saada järjekordne juur.
        astme_alus = pow(euleri, hulk)
        #print("b", pow(astme_alus, 7))  # Lisame leitud komplekshulga vastuste nimekirja
        vastus.append(astme_alus)

    
    #print("1_ylesannde arvutuse vastus: ", vastus)


    return vastus
